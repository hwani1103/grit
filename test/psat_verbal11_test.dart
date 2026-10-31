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
        .singleWhere((s) => s.id == 'psat-verbal-011')
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
    'verbal Set11 preserves blank, admission table, coordinate symbols and underlines',
    () {
      const keys = [2, 1, 4, 5, 4, 4, 3, 3, 2, 1];
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
      expect(added[4].body, contains('“□.”'));
      expect(added[5].underlines.length, 5);
      expect(added[7].tables.single['rows'], [
        ['과학고', '전기', '2', 'A시'],
        ['영재고', '전기', '1', '전국'],
        ['특성화고', '전기', '30', 'A시'],
        ['예술고', '후기', '5', '전국'],
        ['일반고', '후기', '30', 'A시'],
      ]);
      expect(added[7].body, contains('「영재교육진흥법」'));
      expect(added[9].figures, isEmpty);
      expect(added[9].body, contains('t₁부터 t₂까지'));
      expect(added[9].choices[1], contains('t3부터'));
      expect(added.every((q) => q.data['examDate'] == '2025-11-15'), isTrue);
      for (final q in added) {
        expect(q.body.contains(RegExp(r'[\uE000-\uF8FF\u2024]')), isFalse);
        expect(File(q.original).lengthSync(), greaterThan(1000));
      }
    },
  );
  testWidgets('verbal Set11 special text fits cover and opened fold', (
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
        if (n == 9) {
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
          0: '이성계는 왕명을',
          1: '오랫동안 AI는',
          2: '그런데 사물을',
          3: '1990년 개정 이전의',
          4: '“□.”',
          5: '권리라는 점에서 자율적',
          6: '자료 조사',
          7: '고등학교 입학전형 기본계획',
          8: '인공적으로 음의',
          9: '항구의 기온이',
        }[n]!;
        final target = n == 7
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
            'artifacts/psat600_20261028/verbal11/screens/q${q.number}-${size.width.toInt()}.png',
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
