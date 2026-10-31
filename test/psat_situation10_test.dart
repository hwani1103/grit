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
        .singleWhere((s) => s.id == 'psat-situation-010')
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
    'situation Set10 preserves blank, Greek symbols, choice columns and underlines',
    () {
      const keys = [4, 3, 4, 5, 5, 2, 5, 1, 2, 2];
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
      expect(added[4].figures.length, 1);
      expect(added[5].body, contains('㉠ □'));
      expect(added[7].body, added[8].body.split('\n\n<상황>').first);
      expect(added[9].data['choiceNote'], '㉠ → ㉡');
      expect(added[9].choices[1], '10020 · 10033');
      expect(added[1].body.split('제00조\n\n①').length - 1, 2);
      for (final q in added) {
        expect(q.body.contains(RegExp(r'[\uE000-\uF8FF\u2024]')), isFalse);
        expect(File(q.original).lengthSync(), greaterThan(1000));
      }
    },
  );
  testWidgets('situation Set10 special text fits cover and opened fold', (
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
        if (n == 4) {
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
          0: '처리결과의 통지',
          1: '○○부 장관이나 시·도지사는',
          2: '재적위원 3분의 2 이상의 출석',
          3: '2019년 수강인원이 20명',
          4: '작성한 후 뒤늦게',
          5: '㉠ □',
          6: '받은 메시지와 날씨가 3일',
          7: '관계지방자치단체 위원 수 ＝',
          8: '甲도가 관할하는',
          9: '행정구역분류코드는 다섯 자리',
        }[n]!;
        final target = find.byWidgetPredicate(
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
            'artifacts/psat600_20261028/situation10/screens/q${q.number}-${size.width.toInt()}.png',
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
