import 'dart:convert';
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
  const manifestPath = String.fromEnvironment(
    'PSAT_AUDIT_MANIFEST',
    defaultValue: 'artifacts/psat_quality_audit_20261029/sample15.json',
  );
  const outputPath = String.fromEnvironment(
    'PSAT_AUDIT_OUTPUT',
    defaultValue: 'artifacts/psat_quality_audit_20261029/screens',
  );
  const expectedQuestionCount = int.fromEnvironment(
    'PSAT_AUDIT_COUNT',
    defaultValue: 15,
  );
  late List<PsatQuestion> questions;
  setUpAll(() async {
    final manifest =
        jsonDecode(File(manifestPath).readAsStringSync())
            as Map<String, dynamic>;
    final catalog = await loadPsatCatalog();
    questions = (manifest['sample'] as List)
        .map((x) => catalog.questions[x['id']]!)
        .toList();
    expect(questions.length, expectedQuestionCount);
    for (final name in ['AuditKorean', 'Ahem']) {
      await (FontLoader(name)..addFont(
            Future.value(
              ByteData.sublistView(
                File('C:/Windows/Fonts/malgun.ttf').readAsBytesSync(),
              ),
            ),
          ))
          .load();
    }
    await (FontLoader('Roboto')..addFont(
          Future.value(
            ByteData.sublistView(
              File(
                'C:/tools/flutter/engine/src/flutter/txt/third_party/fonts/Roboto-Regular.ttf',
              ).readAsBytesSync(),
            ),
          ),
        ))
        .load();
    await (FontLoader('AuditSymbols')..addFont(
          Future.value(
            ByteData.sublistView(
              File('C:/Windows/Fonts/segoeui.ttf').readAsBytesSync(),
            ),
          ),
        ))
        .load();
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
  Future<void> capture(WidgetTester t, GlobalKey key, String name) async {
    await t.runAsync(() async {
      final im =
          await (key.currentContext!.findRenderObject()!
                  as RenderRepaintBoundary)
              .toImage(pixelRatio: 1);
      final bytes = await im.toByteData(format: ui.ImageByteFormat.png);
      final file = File('$outputPath/$name.png');
      file.parent.createSync(recursive: true);
      file.writeAsBytesSync(bytes!.buffer.asUint8List());
      im.dispose();
    });
  }

  for (final spec in [
    (const Size(320, 640), 1.4),
    (const Size(390, 844), 1.0),
    (const Size(752, 834), 1.0),
    (const Size(840, 360), 1.0),
  ]) {
    testWidgets('frozen audit sample full review remains readable at $spec', (
      t,
    ) async {
      t.view.devicePixelRatio = 1;
      t.view.physicalSize = spec.$1;
      addTearDown(t.view.resetDevicePixelRatio);
      addTearDown(t.view.resetPhysicalSize);
      final c = AppController(MemoryPersistence());
      for (final q in questions) {
        final key = GlobalKey();
        final start = DateTime(2026, 10, 29);
        final attempt = PsatAttempt(
          id: 'audit-${q.id}',
          question: q,
          selected: q.answer,
          startedAt: start,
          completedAt: start.add(const Duration(seconds: 30)),
          seconds: 30,
        );
        await t.pumpWidget(
          MaterialApp(
            theme: ThemeData(
              fontFamily: 'Roboto',
              fontFamilyFallback: const ['AuditKorean', 'AuditSymbols'],
            ),
            builder: (context, child) => MediaQuery(
              data: MediaQuery.of(
                context,
              ).copyWith(textScaler: TextScaler.linear(spec.$2)),
              child: child!,
            ),
            home: RepaintBoundary(
              key: key,
              child: PsatReader(
                key: ValueKey('${q.id}-$spec'),
                controller: c,
                question: q,
                review: attempt,
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
        if (spec.$1.width == 390 || spec.$1.width == 752) {
          await capture(t, key, '${q.id}-${spec.$1.width.toInt()}-start');
        }
        final end = find.text('목록으로');
        final scroll = find.byType(Scrollable).last;
        var page = 0;
        while (end.hitTestable().evaluate().isEmpty && page < 100) {
          await t.drag(scroll, Offset(0, -spec.$1.height * .65));
          await t.pumpAndSettle();
          page++;
          if (spec.$1.width == 390) {
            await capture(
              t,
              key,
              '${q.id}-390-page-${page.toString().padLeft(2, '0')}',
            );
          }
          expect(t.takeException(), isNull, reason: '${q.id} page$page');
        }
        expect(end.hitTestable(), findsOneWidget, reason: q.id);
        expect(t.takeException(), isNull, reason: q.id);
        if (spec.$1.width == 752) {
          await capture(t, key, '${q.id}-752-end');
        }
        await t.pumpWidget(const SizedBox());
      }
      c.dispose();
    });
  }
  testWidgets('audit data figures keep width and zoom access', (t) async {
    var zoomed = 0;
    var figuresChecked = 0;
    t.view.devicePixelRatio = 1;
    t.view.physicalSize = const Size(390, 844);
    addTearDown(t.view.resetDevicePixelRatio);
    addTearDown(t.view.resetPhysicalSize);
    final c = AppController(MemoryPersistence());
    for (final q in questions.where((q) => q.figures.isNotEmpty)) {
      final key = GlobalKey();
      await t.pumpWidget(
        RepaintBoundary(
          key: key,
          child: MaterialApp(
            theme: ThemeData(
              fontFamily: 'Roboto',
              fontFamilyFallback: const ['AuditKorean', 'AuditSymbols'],
            ),
            home: PsatReader(key: ValueKey(q.id), controller: c, question: q),
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
        final figureIndex = q.figures.indexWhere(
          (x) => x['asset'] == f['asset'],
        );
        expect(figureIndex, greaterThanOrEqualTo(0));
        final target = find.byKey(ValueKey(f['asset']));
        await t.scrollUntilVisible(
          target,
          350,
          scrollable: find.byType(Scrollable).last,
          maxScrolls: 100,
        );
        await t.pumpAndSettle();
        final rect = t.getRect(target);
        expect(rect.left, greaterThanOrEqualTo(0));
        expect(rect.right, lessThanOrEqualTo(390));
        final raw = t.widgetList<RawImage>(
          find.descendant(of: target, matching: find.byType(RawImage)),
        );
        expect(raw, isNotEmpty);
        expect(raw.every((i) => i.image != null), isTrue);
        await capture(t, key, '${q.id}-figure-$figureIndex');
        await t.tapAt(Offset(rect.center.dx, rect.top.clamp(90, 744) + 20));
        await t.pumpAndSettle();
        expect(
          find.byType(InteractiveViewer),
          findsOneWidget,
          reason: f['asset'] as String,
        );
        if (figureIndex == 0) {
          final center = t.getCenter(find.byType(InteractiveViewer));
          final left = await t.startGesture(
            center - const Offset(35, 0),
            pointer: 1,
          );
          final right = await t.startGesture(
            center + const Offset(35, 0),
            pointer: 2,
          );
          await t.pump();
          await left.moveTo(center - const Offset(100, 0));
          await right.moveTo(center + const Offset(100, 0));
          await t.pump();
          await left.up();
          await right.up();
          await t.pumpAndSettle();
          final transforms = t.widgetList<Transform>(
            find.descendant(
              of: find.byType(InteractiveViewer),
              matching: find.byType(Transform),
            ),
          );
          expect(
            transforms.any((w) => w.transform.getMaxScaleOnAxis() > 1.5),
            isTrue,
            reason: q.id,
          );
          await capture(t, key, '${q.id}-pinch-zoom');
          zoomed++;
        }
        await t.pageBack();
        await t.pumpAndSettle();
        expect(t.takeException(), isNull);
        figuresChecked++;
      }
      await t.pumpWidget(const SizedBox());
    }
    c.dispose();
    expect(zoomed, questions.where((q) => q.figures.isNotEmpty).length);
    expect(
      figuresChecked,
      questions.fold<int>(0, (sum, q) => sum + q.figures.length),
    );
  });
  testWidgets('audit original source pages decode and support pinch zoom', (
    t,
  ) async {
    t.view.devicePixelRatio = 1;
    t.view.physicalSize = const Size(390, 844);
    addTearDown(t.view.resetDevicePixelRatio);
    addTearDown(t.view.resetPhysicalSize);
    final c = AppController(MemoryPersistence());
    for (final q in questions) {
      final key = GlobalKey();
      await t.pumpWidget(
        RepaintBoundary(
          key: key,
          child: MaterialApp(
            theme: ThemeData(
              fontFamily: 'Roboto',
              fontFamilyFallback: const ['AuditKorean', 'AuditSymbols'],
            ),
            home: PsatReader(key: ValueKey(q.id), controller: c, question: q),
          ),
        ),
      );
      await t.pumpAndSettle();
      await t.runAsync(
        () => precacheImage(
          AssetImage(q.original),
          t.element(find.byType(PsatReader)),
        ),
      );
      await t.tap(find.byTooltip('공식 문제 원문'));
      await t.pumpAndSettle();
      final viewer = find.byType(InteractiveViewer);
      expect(viewer, findsOneWidget, reason: q.id);
      final raw = t.widgetList<RawImage>(
        find.descendant(of: viewer, matching: find.byType(RawImage)),
      );
      expect(raw.single.image, isNotNull, reason: q.original);
      await capture(t, key, '${q.id}-original-page');
      final center = t.getCenter(viewer);
      final left = await t.startGesture(
        center - const Offset(35, 0),
        pointer: 1,
      );
      final right = await t.startGesture(
        center + const Offset(35, 0),
        pointer: 2,
      );
      await t.pump();
      await left.moveTo(center - const Offset(100, 0));
      await right.moveTo(center + const Offset(100, 0));
      await t.pump();
      await left.up();
      await right.up();
      await t.pumpAndSettle();
      final transforms = t.widgetList<Transform>(
        find.descendant(of: viewer, matching: find.byType(Transform)),
      );
      expect(
        transforms.any((w) => w.transform.getMaxScaleOnAxis() > 1.5),
        isTrue,
        reason: q.id,
      );
      expect(t.takeException(), isNull, reason: q.id);
      await t.pumpWidget(const SizedBox());
    }
    c.dispose();
  });
}
