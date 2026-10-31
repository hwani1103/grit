import 'dart:io';
import 'dart:ui' as ui;
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/psat.dart';
import 'package:grit/psat_model.dart';
import 'package:grit/psat_sets.dart';
import 'package:grit/psat_text.dart';
import 'package:grit/store.dart';
import 'store_test.dart' show MemoryPersistence;

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  late List<PsatQuestion> added;
  setUpAll(() async {
    final c = await loadPsatCatalog();
    added = c.sets
        .singleWhere((s) => s.id == 'psat-verbal-018')
        .questionIds
        .map((id) => c.questions[id]!)
        .toList();
    for (final name in ['Roboto', 'Ahem']) {
      await (FontLoader(name)..addFont(
            Future.value(
              ByteData.sublistView(
                File('C:/Windows/Fonts/malgun.ttf').readAsBytesSync(),
              ),
            ),
          ))
          .load();
    }
    await (FontLoader('MaterialIcons')..addFont(
          Future.value(
            ByteData.sublistView(
              File(
                'C:/tools/flutter/bin/cache/artifacts/material_fonts/MaterialIcons-Regular.otf',
              ).readAsBytesSync(),
            ),
          ),
        ))
        .load();
  });
  test('verbal Set18 preserves official keys, five marked ranges, book title and blanks', () {
    const keys = [2,4,3,4,3,5,3,2,5,1];
    expect(added.length, 10);
    expect(added.map((q)=>q.number).toList(), List.generate(10,(i)=>i+1));
    for (var i=0;i<10;i++) {
      final q=added[i];
      expect(q.answer, keys[i]);
      expect(q.steps.length,5);expect(q.reasons.length,5);
      expect(PsatQuestion.fromJson(q.toJson()).toJson(),q.toJson());
      expect(q.data['examDate'],'2026-03-07');
      expect(q.body.contains(RegExp(r'[\uE000-\uF8FF\u2024]')),isFalse);
      for(final u in q.underlines) {
        expect(q.body.split(u).length-1,1);
        expect(psatInlineSpans(q.body,q.underlines).any((s)=>s.style?.decoration==TextDecoration.underline && (s.text??'').contains(u)),isTrue);
      }
      expect(File(q.original).lengthSync(),greaterThan(1000));
    }
    expect(added[4].body,contains('『나바호 암호 통신병 사전』'));
    expect(added[6].underlines.length,5);
    expect(added[7].body.split('[빈칸]').length,3);
    expect(added[8].body.split('[빈칸]').length,2);
    expect(added.every((q)=>q.tables.isEmpty && q.figures.isEmpty),isTrue);
  });
  testWidgets('verbal Set18 special text fits cover and opened fold', (
    t,
  ) async {
    t.view.devicePixelRatio = 1;
    addTearDown(t.view.resetDevicePixelRatio);
    addTearDown(t.view.resetPhysicalSize);
    final c = AppController(MemoryPersistence());
    for (final size in [const Size(360, 840), const Size(752, 834)]) {
      t.view.physicalSize = size;
      for (final n in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]) {
        final q = added[n];
        final boundary = GlobalKey();
        await t.pumpWidget(
          MaterialApp(
            theme: ThemeData(fontFamily: 'Roboto'),
            home: RepaintBoundary(
              key: boundary,
              child: PsatReader(
                key: ValueKey('$n-$size'),
                controller: c,
                question: q,
              ),
            ),
          ),
        );
        await t.pumpAndSettle();
        final needle={0:'이들 중 상재상이',1:'그러나 비기계식',2:'이중적인 지위를 갖는다',3:'국제적인 생산 네트워크',4:'알파벳 각각에 여러 개',5:'같은 맥락에서 북유럽',6:'‘쟤는 나를 싫어해’가 아니라',7:'(가) [빈칸]',8:'비추어 볼 때 [빈칸]',9:'공동체 단위의 경작'}[n]!;
        final target=find.byWidgetPredicate((w)=>w is PsatText && w.text.contains(needle));
        await t.scrollUntilVisible(
          target,
          350,
          scrollable: find.byType(Scrollable).first,
          maxScrolls: 100,
        );
        await t.pumpAndSettle();
        expect(target, findsOneWidget);
        final r = t.getRect(target);
        expect(r.left, greaterThanOrEqualTo(0));
        expect(r.right, lessThanOrEqualTo(size.width));
        await t.runAsync(() async {
          final im =
              await (boundary.currentContext!.findRenderObject()!
                      as RenderRepaintBoundary)
                  .toImage(pixelRatio: 1.5);
          final b = await im.toByteData(format: ui.ImageByteFormat.png);
          final f = File(
            'artifacts/psat600_20261028/verbal18/screens/q${q.number}-${size.width.toInt()}.png',
          );
          f.parent.createSync(recursive: true);
          f.writeAsBytesSync(b!.buffer.asUint8List());
          im.dispose();
        });
        expect(t.takeException(), isNull, reason: '$n $size');
        await t.pumpWidget(const SizedBox());
      }
    }
    c.dispose();
  });
}
