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

// Each new ten-question Set must expose the complete explanation at all four
// supported host sizes before it is counted as verified.
void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  const setId = String.fromEnvironment('GRIT_REVIEW_SET', defaultValue: 'psat-verbal-016');
  late List<PsatQuestion> questions;
  setUpAll(() async {
    final catalog = await loadPsatCatalog();
    questions = catalog.sets.singleWhere((s) => s.id == setId).questionIds
        .map((id) => catalog.questions[id]!).toList();
    expect(questions.length, 10);
    for (final name in ['Roboto', 'Ahem']) {
      await (FontLoader(name)..addFont(Future.value(ByteData.sublistView(
        File('C:/Windows/Fonts/malgun.ttf').readAsBytesSync(),
      )))).load();
    }
    await (FontLoader('MaterialIcons')..addFont(Future.value(ByteData.sublistView(
      File('C:/tools/flutter/bin/cache/artifacts/material_fonts/MaterialIcons-Regular.otf').readAsBytesSync(),
    )))).load();
  });
  for (final spec in [
    (const Size(320, 640), 1.4),
    (const Size(390, 844), 1.0),
    (const Size(752, 834), 1.0),
    (const Size(840, 360), 1.0),
  ]) {
    testWidgets('$setId complete explanations reachable at $spec', (t) async {
      t.view.devicePixelRatio = 1;
      t.view.physicalSize = spec.$1;
      addTearDown(t.view.resetDevicePixelRatio);
      addTearDown(t.view.resetPhysicalSize);
      final controller = AppController(MemoryPersistence());
      for (final q in questions) {
        final boundary = GlobalKey();
        final start = DateTime(2026, 10, 29);
        final review = PsatAttempt(id: 'review-${q.id}', question: q,
          selected: q.answer, startedAt: start,
          completedAt: start.add(const Duration(seconds: 30)), seconds: 30);
        await t.pumpWidget(MaterialApp(
          theme: ThemeData(fontFamily: 'Roboto'),
          builder: (context, child) => MediaQuery(
            data: MediaQuery.of(context).copyWith(textScaler: TextScaler.linear(spec.$2)),
            child: child!,
          ),
          home: RepaintBoundary(key: boundary, child: PsatReader(
            key: ValueKey(q.id), controller: controller, question: q, review: review)),
        ));
        await t.pumpAndSettle();
        final end = find.text('목록으로');
        await t.scrollUntilVisible(end, 450,
          scrollable: find.byType(Scrollable).last, maxScrolls: 150);
        await t.pumpAndSettle();
        expect(end.hitTestable(), findsOneWidget, reason: q.id);
        expect(t.takeException(), isNull, reason: q.id);
        if ((questions.indexOf(q) == 0 || questions.indexOf(q) == 9) && spec.$2 == 1.0) {
          await t.runAsync(() async {
            final im = await (boundary.currentContext!.findRenderObject()! as RenderRepaintBoundary).toImage(pixelRatio: 1.5);
            final bytes = await im.toByteData(format: ui.ImageByteFormat.png);
            final out = File('artifacts/psat600_20261028/batch-review/$setId/${q.id}-${spec.$1.width.toInt()}.png');
            out.parent.createSync(recursive: true);
            out.writeAsBytesSync(bytes!.buffer.asUint8List());
            im.dispose();
          });
        }
        await t.pumpWidget(const SizedBox());
      }
      controller.dispose();
    });
  }
}
