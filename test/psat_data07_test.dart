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
        .singleWhere((s) => s.id == 'psat-data-007')
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
    '2025 data Set7 matches keys and preserves complete graphics in snapshots',
    () {
      const keys = [1, 2, 1, 3, 5, 5, 2, 2, 5, 4];
      expect(added.length, 10);
      expect(added.expand((q) => q.figures).length, 21);
      for (final q in added) {
        expect(q.answer, keys[added.indexOf(q)]);
        expect(q.steps.length, 5);
        expect(q.reasons.length, 5);
        expect(q.data['examDate'], '2025-07-19');
        expect(PsatQuestion.fromJson(q.toJson()).toJson(), q.toJson());
        expect(File(q.original).lengthSync(), greaterThan(1000));
        for (final f in q.figures) {
          final bytes = File(f['asset'] as String).readAsBytesSync();
          final data = ByteData.sublistView(bytes);
          expect(data.getUint32(16), f['width']);
          expect(data.getUint32(20), f['height']);
        }
      }
      expect(added[1].data['choiceNote'], '선택지의 순서: (가) → (나) → (다)');
      expect(added[6].choices[3], contains('km²'));
      expect(added[0].figures.length, 1);
      expect(added[5].figures.length, 1);
      expect(added[9].figures.length, 2);
      for (final i in [3]) {
        expect(added[i].choices, ['자료 1', '자료 2', '자료 3', '자료 4', '자료 5']);
        expect(added[i].figures.where((f) => (f['caption'] as String).startsWith('선택지 ')).map((f) => f['caption']).toList(), [
          '선택지 ①',
          '선택지 ②',
          '선택지 ③',
          '선택지 ④',
          '선택지 ⑤',
        ]);
      }
    },
  );
  testWidgets(
    'all 21 current figures fit cover and open widths and can be enlarged',
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
            if ([1, 2, 3, 4, 8, 9].contains(added.indexOf(q))) {
              await t.runAsync(() async {
                final img =
                    await (boundary.currentContext!.findRenderObject()!
                            as RenderRepaintBoundary)
                        .toImage(pixelRatio: 1.5);
                final bytes = await img.toByteData(
                  format: ui.ImageByteFormat.png,
                );
                final file = File(
                  'artifacts/psat600_20261028/data07/screens/figure-${added.indexOf(q)}-${q.figures.indexWhere((x) => x["asset"] == f["asset"])}-${size.width.toInt()}.png',
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
