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
        .singleWhere((s) => s.id == 'psat-situation-018')
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
  test('situation Set18 legal procedure, exact dates, original keys and flower table', () {
    const keys=[3,4,2,5,1,1,3,3,2,1];
    expect(added.length,10);
    for(var i=0;i<10;i++) {
      final q=added[i];expect(q.answer,keys[i]);
      expect(q.number,i+1);expect(q.steps.length,5);expect(q.reasons.length,5);
      expect(PsatQuestion.fromJson(q.toJson()).toJson(),q.toJson());
      expect(File(q.original).lengthSync(),greaterThan(1000));
      expect(q.body.contains(RegExp(r'[\uE000-\uF8FF\u2024]')),isFalse);
    }
    expect(added[2].body,contains('「민법」'));
    expect(added[2].body,contains('청문을 하여야 한다'));
    expect(added[8].data['choiceNote'],'甲 → 丙');
    final table=added[9].tables.single;
    expect(table['rows'].length,5);
    expect(table['rows'][1],['백합','하양','3일','6,000원','5/10 ～ 5/20 수급 어려움으로 50% 가격 인상']);
    final paragraphs=added[9].body.split('\n\n');
    expect(paragraphs[table['afterParagraph']],startsWith('다음은 꽃집'));
    expect(added[9].steps.join(' '),contains('6/3'));
  });
  testWidgets('situation Set18 special text fits cover and opened fold', (
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
        final needle={0:'제□□조(기후변화 시나리오',1:'제00조(지하부분에 대한 보상 등)',2:'제△△조(마을기업의 지정취소)',3:'제00조(말소등록)',4:'제00조(고액',5:'회계처리는 대금 지불 방식',6:'A부처는 총',7:'부서 직원 120명',8:'A달리기 동호회 회원',9:''}[n]!;
        final target=n==9
          ? find.byKey(ValueKey('psat-table-${q.id}-${q.tables.last["caption"]}'))
          : find.byWidgetPredicate((w)=>w is PsatText && w.text.contains(needle));
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
            'artifacts/psat600_20261028/situation18/screens/q${q.number}-${size.width.toInt()}.png',
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
