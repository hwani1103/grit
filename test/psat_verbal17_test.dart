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
        .singleWhere((s) => s.id == 'psat-verbal-017')
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
  test(
    'verbal Set17 preserves shared passage, table, underlines and source metadata',
    () {
      const keys = [2,5,1,2,3,3,4,1,3,5];
      expect(added.length, 10);
      for (final q in added) {
        expect(q.answer, keys[added.indexOf(q)]);
        expect(q.steps.length, 5);
        expect(q.reasons.length, 5);
        expect(PsatQuestion.fromJson(q.toJson()).toJson(), q.toJson());
        for (final u in q.underlines) {
          expect(q.body.split(u).length - 1, 1);
          expect(
            psatInlineSpans(q.body, q.underlines).any(
              (s) =>
                  s.style?.decoration == TextDecoration.underline &&
                  (s.text ?? '').contains(u),
            ),
            isTrue,
          );
        }
      }
      expect(added.take(6).every((q)=>q.data['examDate']=='2026-03-07'),isTrue);
      expect(added.skip(6).every((q)=>q.data['examDate']=='2025-03-08'),isTrue);
      expect(added.map((q)=>q.number).toList(),[30,31,32,35,39,40,13,14,33,34]);
      expect(added[5].body,contains(added[4].body));
      expect(added.fold<int>(0,(s,q)=>s+q.tables.length),1);
      expect(added[5].tables.single['rows'],[['물고기 A','60','40','20','60'],['물고기 B','0','20','40','0']]);
      expect(added.fold<int>(0,(s,q)=>s+q.underlines.length),7);
      expect(added.every((q)=>q.figures.isEmpty),isTrue);
      for (final q in added) {
        expect(q.body.contains(RegExp(r'[\uE000-\uF8FF\u2024]')), isFalse);
        expect(File(q.original).lengthSync(), greaterThan(1000));
      }
    },
  );
  testWidgets('verbal Set17 special text fits cover and opened fold', (
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
        final needle={0:'보석 결정의 판단 기준은',1:'부담하지 않는다는 의견',2:'낙관주의에 대해 비판적인 시각',3:'이 세 가설을 검증하기',4:'종 다양성을 위해서는',5:'',6:'교통사고가 현저하게 줄어들려면',7:'갑은 이 사실에 새롭게',8:'다섯 개의 물품 중 양품이',9:'다섯 개의 단어 P, Q, R, S, T'}[n]!;
        final target=n==5 ? find.byKey(ValueKey('psat-table-${q.id}-${q.tables.single["caption"]}')) : find.byWidgetPredicate((w)=>w is PsatText && w.text.contains(needle));
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
            'artifacts/psat600_20261028/verbal17/screens/q${q.number}-${size.width.toInt()}.png',
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
