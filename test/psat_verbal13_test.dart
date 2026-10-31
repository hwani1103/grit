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
        .singleWhere((s) => s.id == 'psat-verbal-013')
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
    'verbal Set13 preserves mixed exam dates, electoral table, underlines and book titles',
    () {
      const keys = [3, 2, 5, 4, 4, 5, 1, 3, 4, 5];
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
        ['(가)', '㉠', '㉡', '㉢'],
        ['(나)', '㉣', '㉤', '㉥'],
      ]);
      expect(
        added.take(3).every((q) => q.data['examDate'] == '2025-11-15'),
        isTrue,
      );
      expect(
        added.skip(3).every((q) => q.data['examDate'] == '2026-07-18'),
        isTrue,
      );
      expect(added[6].underlines, ['㉠ ‘전이’']);
      expect(added[7].underlines.length, 5);
      expect(added[8].body, contains('『묵재일기』'));
      expect(added[8].body, contains('(가)'));
      expect(added[8].body, contains('(나)'));
      expect(added[9].underlines, ['자료 조사']);
      expect(added[2].body, contains('제00조(조합장의 선임)\n\n①'));
      for (final q in added) {
        expect(q.body.contains(RegExp(r'[\uE000-\uF8FF\u2024]')), isFalse);
        expect(File(q.original).lengthSync(), greaterThan(1000));
      }
    },
  );
  testWidgets('verbal Set13 special text fits cover and opened fold', (
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
          1: '군인이 근무지역 내',
          2: '제00조(조합장의 선임)',
          3: '이후 고려 숙종은',
          4: '이런 설명 구조에서',
          5: '이러한 우분투',
          6: '‘전이’',
          7: '실제 경험을 있는 그대로 저장하기 위해',
          8: '18세기에',
          9: '자료 조사',
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
            'artifacts/psat600_20261028/verbal13/screens/q${q.number}-${size.width.toInt()}.png',
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
