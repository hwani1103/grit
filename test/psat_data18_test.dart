import 'dart:io';
import 'dart:ui' as ui;
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/psat.dart';
import 'package:grit/psat_model.dart';
import 'package:grit/psat_sets.dart';
import 'package:grit/store.dart';
import 'store_test.dart' show MemoryPersistence;

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  late List<PsatQuestion> added;
  setUpAll(() async {
    final catalog = await loadPsatCatalog();
    added = catalog.sets
        .singleWhere((s) => s.id == 'psat-data-018')
        .questionIds
        .map((id) => catalog.questions[id]!)
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
    'data Set18 official keys, full graphics and exact rounding boundaries',
    () {
      expect(added.length, 10);
      expect(
        added.map((q) => q.number).toList(),
        List.generate(10, (i) => i + 21),
      );
      expect(added.map((q) => q.answer).toList(), [
        4,
        4,
        3,
        1,
        4,
        2,
        1,
        2,
        4,
        3,
      ]);
      expect(added.map((q) => q.figures.length).toList(), [
        1,
        1,
        4,
        2,
        1,
        1,
        1,
        2,
        3,
        2,
      ]);
      for (final q in added) {
        expect(q.steps.length, 5);
        expect(q.reasons.length, 5);
        expect(PsatQuestion.fromJson(q.toJson()).toJson(), q.toJson());
      }
      expect(added[4].steps[2], contains('미국 1위·독일 9위의 2개'));
      expect(added[5].steps[4], contains('총점 1,600·방송 100'));
      expect(added[8].steps[4], contains('71·92·10·108·14·12'));
      expect(added[9].steps[1], contains('24.5≤'));
      expect(added[1].choices, ['밑줄 ①', '밑줄 ②', '밑줄 ③', '밑줄 ④', '밑줄 ⑤']);
      expect(added[8].data['choiceNote'], 'A → B');
    },
  );
  testWidgets(
    'all 18 current figures fit cover and open widths and can be enlarged',
    (t) async {
      t.view.devicePixelRatio = 1;
      addTearDown(t.view.resetDevicePixelRatio);
      addTearDown(t.view.resetPhysicalSize);
      final c = AppController(MemoryPersistence());
      for (final size in [const Size(360, 840), const Size(752, 834)]) {
        t.view.physicalSize = size;
        for (final q in added) {
          final boundary = GlobalKey();
          await t.pumpWidget(
            MaterialApp(
              theme: ThemeData(fontFamily: 'Roboto'),
              home: RepaintBoundary(
                key: boundary,
                child: PsatReader(
                  key: ValueKey('${q.id}-$size'),
                  controller: c,
                  question: q,
                ),
              ),
            ),
          );
          await t.pumpAndSettle();
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
            final target = find.byKey(ValueKey(f['asset']));
            await t.scrollUntilVisible(
              target,
              350,
              scrollable: find.byType(Scrollable).last,
              maxScrolls: 100,
            );
            await t.pumpAndSettle();
            final rawImages = t.widgetList<RawImage>(
              find.descendant(of: target, matching: find.byType(RawImage)),
            );
            expect(rawImages, isNotEmpty, reason: f['asset'] as String);
            expect(
              rawImages.every((im) => im.image != null),
              isTrue,
              reason: f['asset'] as String,
            );
            final rect = t.getRect(target);
            expect(rect.left, greaterThanOrEqualTo(0));
            expect(rect.right, lessThanOrEqualTo(size.width));
            if ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9].contains(added.indexOf(q))) {
              await t.runAsync(() async {
                final img =
                    await (boundary.currentContext!.findRenderObject()!
                            as RenderRepaintBoundary)
                        .toImage(pixelRatio: 1.5);
                final bytes = await img.toByteData(
                  format: ui.ImageByteFormat.png,
                );
                final file = File(
                  'artifacts/psat600_20261028/data18/screens/figure-${added.indexOf(q)}-${q.figures.indexWhere((x) => x["asset"] == f["asset"])}-${size.width.toInt()}.png',
                );
                file.parent.createSync(recursive: true);
                file.writeAsBytesSync(bytes!.buffer.asUint8List());
                img.dispose();
              });
            }
            await t.tapAt(
              Offset(
                rect.center.dx,
                rect.top.clamp(90, size.height - 100) + 20,
              ),
            );
            await t.pumpAndSettle();
            expect(
              find.byType(InteractiveViewer),
              findsOneWidget,
              reason: '${q.id} ${f['asset']}',
            );
            await t.pageBack();
            await t.pumpAndSettle();
            expect(t.takeException(), isNull, reason: q.id);
          }
          await t.pumpWidget(const SizedBox());
        }
      }
      c.dispose();
    },
  );
}
