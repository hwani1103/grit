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
        .singleWhere((s) => s.id == 'psat-verbal-014')
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
    'verbal Set14 preserves eligibility table, underlines, book titles and ordered blanks',
    () {
      const keys = [5, 3, 5, 1, 2, 2, 3, 3, 5, 1];
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
      expect(added[0].tables.single['rows'], [
        ['준비형', '19세 이상 34세 미만', '미취업'],
        ['성장형', '19세 이상 34세 미만', '취업'],
        ['전환형', '34세 이상 49세 이하', '상관 없음'],
      ]);
      expect(added.every((q) => q.data['examDate'] == '2026-07-18'), isTrue);
      expect(added[1].body, contains('『종의 기원』'));
      expect(added[4].data['choiceNote'], '(가) → (나)');
      expect(added[6].underlines, ['두 개의 전제']);
      expect(added[8].underlines, ['한 사람']);
      expect(added[9].data['choiceNote'], '(가) → (나) → (다)');
      for (final q in added) {
        expect(q.body.contains(RegExp(r'[\uE000-\uF8FF\u2024]')), isFalse);
        expect(File(q.original).lengthSync(), greaterThan(1000));
      }
    },
  );
  testWidgets('verbal Set14 special text fits cover and opened fold', (
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
        final needle = {
          0: '',
          1: '『종의 기원』',
          2: '홍색비황세균과 녹색비황세균은',
          3: '이에 대해',
          4: '밴드갭 에너지는',
          5: '인디카에도',
          6: '전제 2:',
          7: '마라톤부 회원은',
          8: '한 사람',
          9: '실험 C:',
        }[n]!;
        final target = n == 0
            ? find.byKey(
                ValueKey('psat-table-${q.id}-${q.tables.single["caption"]}'),
              )
            : find.byWidgetPredicate(
                (w) => w is PsatText && w.text.contains(needle),
              );
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
            'artifacts/psat600_20261028/verbal14/screens/q${q.number}-${size.width.toInt()}.png',
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
