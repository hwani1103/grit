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
        .singleWhere((s) => s.id == 'psat-verbal-010')
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
    'verbal Set10 preserves blank, Greek symbols, choice columns and underlines',
    () {
      const keys = [5, 3, 3, 3, 1, 2, 5, 4, 3, 4];
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
      expect(added[1].figures.length, 1);
      expect(added[1].body, contains('공공 기관 통합 채용'));
      expect(added[2].tables.single['rows'], [
        ['A', '㉠', '㉡', '㉢'],
        ['B', '㉣', '㉤', '㉥'],
      ]);
      expect(
        added[4].body.replaceAll(' %', '%'),
        added[5].body.split('\n\n<보기>').first.replaceAll(' %', '%'),
      );
      expect(added[4].data['choiceNote'], '(가) → (나) → (다) → (라)');
      expect(added[6].body, endsWith('□'));
      expect(added[7].body, contains('제9조(충전시설 설치대상)\n\n①'));
      expect(added[8].body, contains('제8조(위원장 및 위원)\n\n①'));
      expect(added[9].data['examDate'], '2025-11-15');
      for (final q in added) {
        expect(q.body.contains(RegExp(r'[\uE000-\uF8FF\u2024]')), isFalse);
        expect(File(q.original).lengthSync(), greaterThan(1000));
      }
    },
  );
  testWidgets('verbal Set10 special text fits cover and opened fold', (
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
        if (n == 1) {
          await t.runAsync(() async {
            for (final f in q.figures) {
              await precacheImage(
                AssetImage(f['asset'] as String),
                t.element(find.byType(PsatReader)),
              );
            }
          });
          await t.pumpAndSettle();
          for (final f in q.figures) {
            final im = find.byKey(ValueKey(f['asset']));
            await t.scrollUntilVisible(
              im,
              350,
              scrollable: find.byType(Scrollable).first,
              maxScrolls: 100,
            );
            await t.pumpAndSettle();
            expect(
              t
                  .widgetList<RawImage>(
                    find.descendant(of: im, matching: find.byType(RawImage)),
                  )
                  .every((i) => i.image != null),
              isTrue,
            );
            final rect = t.getRect(im);
            expect(rect.left, greaterThanOrEqualTo(0));
            expect(rect.right, lessThanOrEqualTo(size.width));
            await t.tapAt(
              Offset(
                rect.center.dx,
                rect.top.clamp(90, size.height - 100) + 20,
              ),
            );
            await t.pumpAndSettle();
            expect(find.byType(InteractiveViewer), findsOneWidget);
            await t.pageBack();
            await t.pumpAndSettle();
          }
        }
        final needle = {
          0: '㉠ 오늘 회의에서',
          1: '',
          2: '입안 지원 신청 조례안별 분류',
          3: '㉠ 필요한 자료',
          4: '㉡ B의 주장',
          5: 'X가 특정 범죄자의',
          6: '말씀하신 것을 바탕으로',
          7: '제9조(충전시설 설치대상)',
          8: '제8조(위원장 및 위원)',
          9: '승정원은 임금이 기거하는',
        }[n]!;
        final target = n == 1
            ? find.byKey(ValueKey(q.figures.last['asset']))
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
            'artifacts/psat600_20261028/verbal10/screens/q${q.number}-${size.width.toInt()}.png',
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
