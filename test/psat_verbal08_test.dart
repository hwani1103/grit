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
        .singleWhere((s) => s.id == 'psat-verbal-008')
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

  test('verbal Set8 preserves shared passage, blank, tables and diagram', () {
    const keys = [5, 4, 2, 1, 5, 4, 1, 1, 4, 5];
    expect(added.length, 10);
    for (var i = 0; i < 10; i++) {
      expect(added[i].answer, keys[i]);
      expect(
        PsatQuestion.fromJson(added[i].toJson()).toJson(),
        added[i].toJson(),
      );
    }
    expect(added[1].body.startsWith(added[0].body), isTrue);
    expect(added[1].body, contains('1/1,000,000'));
    expect(added[2].tables.single['rows'], hasLength(5));
    expect(added[7].tables.single['rows'], hasLength(3));
    expect(added[6].body, endsWith('□'));
    expect(added[4].body, contains('제3조(대항력)\n\n①'));
    expect(added[8].figures, isEmpty);
    expect(added[8].body, contains('[ab][ ][ ]'));
  });
  testWidgets(
    'Set8 shared question, law, blank and tables remain reachable on fold sizes',
    (t) async {
      t.view.devicePixelRatio = 1;
      addTearDown(t.view.resetDevicePixelRatio);
      addTearDown(t.view.resetPhysicalSize);
      final c = AppController(MemoryPersistence());
      for (final size in [const Size(360, 840), const Size(752, 834)]) {
        t.view.physicalSize = size;
        for (final n in [1, 2, 3, 4, 6, 7]) {
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
            1: '을은 100만 명',
            3: '제가 전에 비슷한 사안을',
            4: '제4조(계약의 갱신)',
            6: '□',
          }[n];
          final target = q.tables.isNotEmpty
              ? find.byKey(
                  ValueKey('psat-table-${q.id}-${q.tables.single["caption"]}'),
                )
              : find.byWidgetPredicate(
                  (w) => w is PsatText && w.text.contains(needle!),
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
            final bytes = await im.toByteData(format: ui.ImageByteFormat.png);
            final f = File(
              'artifacts/psat600_20261028/verbal08/screens/item$n-${size.width.toInt()}.png',
            );
            f.parent.createSync(recursive: true);
            f.writeAsBytesSync(bytes!.buffer.asUint8List());
            im.dispose();
          });
          expect(t.takeException(), isNull, reason: '$n $size');
          await t.pumpWidget(const SizedBox());
        }
      }
      c.dispose();
    },
  );
  testWidgets('Set8 particle diagrams decode without clipping and enlarge', (
    t,
  ) async {
    t.view.devicePixelRatio = 1;
    addTearDown(t.view.resetDevicePixelRatio);
    addTearDown(t.view.resetPhysicalSize);
    final c = AppController(MemoryPersistence());
    final q = added[8];
    for (final size in [const Size(360, 840), const Size(752, 834)]) {
      t.view.physicalSize = size;
      final boundary = GlobalKey();
      await t.pumpWidget(
        MaterialApp(
          theme: ThemeData(fontFamily: 'Roboto'),
          home: RepaintBoundary(
            key: boundary,
            child: PsatReader(
              key: ValueKey('$size'),
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
          scrollable: find.byType(Scrollable).first,
          maxScrolls: 100,
        );
        await t.pumpAndSettle();
        final ims = t.widgetList<RawImage>(
          find.descendant(of: target, matching: find.byType(RawImage)),
        );
        expect(ims, isNotEmpty);
        expect(ims.every((i) => i.image != null), isTrue);
        final r = t.getRect(target);
        expect(r.left, greaterThanOrEqualTo(0));
        expect(r.right, lessThanOrEqualTo(size.width));
        await t.runAsync(() async {
          final im =
              await (boundary.currentContext!.findRenderObject()!
                      as RenderRepaintBoundary)
                  .toImage(pixelRatio: 1.5);
          final bytes = await im.toByteData(format: ui.ImageByteFormat.png);
          final out = File(
            'artifacts/psat600_20261028/verbal08/screens/diagram${q.figures.indexWhere((x) => x["asset"] == f["asset"])}-${size.width.toInt()}.png',
          );
          out.parent.createSync(recursive: true);
          out.writeAsBytesSync(bytes!.buffer.asUint8List());
          im.dispose();
        });
        await t.tapAt(
          Offset(r.center.dx, r.top.clamp(90, size.height - 100) + 20),
        );
        await t.pumpAndSettle();
        expect(find.byType(InteractiveViewer), findsOneWidget);
        await t.pageBack();
        await t.pumpAndSettle();
        expect(t.takeException(), isNull);
      }
      await t.pumpWidget(const SizedBox());
    }
    c.dispose();
  });
}
