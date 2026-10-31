import 'dart:io';
import 'dart:ui' as ui;
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/main.dart';
import 'package:grit/psat.dart';
import 'package:grit/psat_model.dart';
import 'package:grit/psat_sets.dart';
import 'package:grit/psat_text.dart';
import 'package:grit/store.dart';
import 'store_test.dart' show MemoryPersistence;

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  late PsatCatalog catalog;
  late List<PsatQuestion> added;
  setUpAll(() async {
    catalog = await loadPsatCatalog();
    added = catalog.questions.values
        .where(
          (q) => q.id.startsWith('kr-mpm-2024-07-27-psat-l-') && q.number <= 10,
        )
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
    '2024 official final key, source assets, source emphasis and snapshots are complete',
    () {
      // Official final PDF 4564 / language / book 사, visually checked.
      const key = [3, 4, 4, 3, 4, 2, 5, 1, 5, 2];
      expect(added.length, 10);
      expect(catalog.questions.length, greaterThanOrEqualTo(40));
      for (final q in added) {
        expect(q.answer, key[q.number - 1]);
        expect(q.data['book'], '사');
        expect(q.data['examDate'], '2024-07-27');
        expect(File(q.original).lengthSync(), greaterThan(1000));
        expect(q.reasons.length, 5);
        expect(q.steps.length, greaterThanOrEqualTo(3));
        expect(PsatQuestion.fromJson(q.toJson()).toJson(), q.toJson());
      }
      final q = added[6];
      expect(q.underlines.length, 5);
      expect(catalog.questions.values.first.underlines, isEmpty);
      for (final bad in [
        <String>['missing phrase'],
        <String>[''],
        <String>[q.underlines.first, q.underlines.first],
        <String>['기존과', q.underlines.first],
      ]) {
        expect(
          () => PsatQuestion.fromJson(q.toJson()..['underlines'] = bad),
          throwsFormatException,
        );
      }
      expect(catalog.forSubject('언어논리')[1].difficulty, '기본');
    },
  );

  testWidgets(
    'all five source underlines survive word wrapping and Fold resizing',
    (t) async {
      t.view.devicePixelRatio = 1;
      addTearDown(t.view.resetDevicePixelRatio);
      addTearDown(t.view.resetPhysicalSize);
      final c = AppController(MemoryPersistence());
      final q = added[6];
      for (final size in [
        const Size(360, 840),
        const Size(752, 834),
        const Size(320, 640),
      ]) {
        t.view.physicalSize = size;
        final boundary = GlobalKey();
        await t.pumpWidget(
          MaterialApp(
            theme: ThemeData(fontFamily: 'Roboto'),
            home: RepaintBoundary(
              key: boundary,
              child: PsatReader(
                key: ValueKey(size),
                controller: c,
                question: q,
              ),
            ),
          ),
        );
        await t.pumpAndSettle();
        final texts = t.widgetList<Text>(
          find.descendant(
            of: find.byType(PsatPassage),
            matching: find.byType(Text),
          ),
        );
        final marked = <String>[];
        void visit(InlineSpan span) {
          if (span is! TextSpan) return;
          if (span.style?.decoration == TextDecoration.underline) {
            marked.add((span.text ?? '').replaceAll('\u2060', ''));
          }
          for (final child in span.children ?? <InlineSpan>[]) {
            visit(child);
          }
        }

        for (final text in texts) {
          if (text.textSpan != null) visit(text.textSpan!);
        }
        expect(marked, q.underlines);
        expect(t.takeException(), isNull);
        await t.runAsync(() async {
          final render =
              boundary.currentContext!.findRenderObject()!
                  as RenderRepaintBoundary;
          final image = await render.toImage(pixelRatio: 1.5);
          final bytes = await image.toByteData(format: ui.ImageByteFormat.png);
          final file = File(
            'artifacts/psat600_20261028/verbal02/screens/q07-${size.width.toInt()}.png',
          );
          file.parent.createSync(recursive: true);
          file.writeAsBytesSync(bytes!.buffer.asUint8List());
          image.dispose();
        });
      }
      await t.pumpWidget(const SizedBox());
      c.dispose();
    },
  );

  testWidgets(
    'Set difficulty and progress are visible on phone and unfolded host captures',
    (t) async {
      t.view.devicePixelRatio = 1;
      addTearDown(t.view.resetDevicePixelRatio);
      addTearDown(t.view.resetPhysicalSize);
      final c = AppController(MemoryPersistence());
      for (final size in [const Size(360, 840), const Size(752, 834)]) {
        t.view.physicalSize = size;
        final boundary = GlobalKey();
        await t.pumpWidget(
          MaterialApp(
            theme: ThemeData(fontFamily: 'Roboto'),
            home: Scaffold(
              body: RepaintBoundary(
                key: boundary,
                child: ColoredBox(
                  color: paper,
                  child: PsatLibrary(controller: c, subject: '언어논리'),
                ),
              ),
            ),
          ),
        );
        for (
          var i = 0;
          i < 40 &&
              find.byType(CircularProgressIndicator).evaluate().isNotEmpty;
          i++
        ) {
          await t.runAsync(
            () => Future<void>.delayed(const Duration(milliseconds: 50)),
          );
          await t.pump();
        }
        await t.pumpAndSettle();
        expect(find.text('Set 2 (0 / 10)'), findsOneWidget);
        expect(
          find.descendant(
            of: find.byKey(const ValueKey('psat-set-psat-verbal-002')),
            matching: find.text('난도 · 기본'),
          ),
          findsOneWidget,
        );
        expect(t.takeException(), isNull);
        await t.runAsync(() async {
          final image =
              await (boundary.currentContext!.findRenderObject()!
                      as RenderRepaintBoundary)
                  .toImage(pixelRatio: 1.5);
          final bytes = await image.toByteData(format: ui.ImageByteFormat.png);
          File(
            'artifacts/psat600_20261028/verbal02/screens/sets-${size.width.toInt()}.png',
          ).writeAsBytesSync(bytes!.buffer.asUint8List());
          image.dispose();
        });
      }
      await t.pumpWidget(const SizedBox());
      c.dispose();
    },
  );
}
