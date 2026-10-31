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
        .singleWhere((s) => s.id == 'psat-data-017')
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
    'mixed-date data Set17 matches keys and preserves complete graphics in snapshots',
    () {
      const keys = [2, 3, 5, 1, 2, 5, 1, 5, 1, 3];
      expect(added.length, 10);
      expect(
        added.map((q) => q.number).toList(),
        List.generate(10, (i) => i + 11),
      );
      expect(added.last.steps[3], contains('1970'));
      expect(added[4].figures.last['caption'], startsWith('⑤'));
      expect(added.map((q) => q.answer).toList(), keys);
      for (final q in added) {
        expect(q.steps.length, 5);
        expect(q.reasons.length, 5);
        expect(PsatQuestion.fromJson(q.toJson()).toJson(), q.toJson());
      }
      expect(
        added.expand((q) => q.figures).map((f) => f['asset']).toSet().length,
        19,
      );
      expect(added.map((q) => q.figures.length).toList(), [
        2,
        1,
        1,
        1,
        6,
        1,
        1,
        1,
        2,
        3,
      ]);
      expect(added.every((q) => q.data['examDate'] == '2026-03-07'), isTrue);
      expect(added[2].data['choiceNote'], 'A → B → C');
      for (final i in [4]) {
        expect(added[i].choices, ['자료 1', '자료 2', '자료 3', '자료 4', '자료 5']);
      }
    },
  );
  testWidgets(
    'all 19 current figures fit cover and open widths and can be enlarged',
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
                  'artifacts/psat600_20261028/data17/screens/figure-${added.indexOf(q)}-${q.figures.indexWhere((x) => x["asset"] == f["asset"])}-${size.width.toInt()}.png',
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
