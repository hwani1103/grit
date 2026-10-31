import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/psat.dart';
import 'package:grit/psat_sets.dart';
import 'package:grit/psat_text.dart';
import 'package:grit/store.dart';
import 'store_test.dart' show MemoryPersistence;

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  testWidgets('native report remains between source table and option tables', (
    t,
  ) async {
      final catalog = (await t.runAsync(loadPsatCatalog))!;
    final q = catalog.questions['kr-mpm-2026-07-18-psat-d-07']!;
    for (final item in catalog.questions.values) {
      final count = item.data['bodyAfterFigureCount'];
      if (count != null) {
        expect(count, isA<int>(), reason: item.id);
        expect(
          count,
          inInclusiveRange(0, item.figures.length),
          reason: item.id,
        );
      }
    }
    t.view.devicePixelRatio = 1;
    t.view.physicalSize = const Size(390, 844);
    addTearDown(t.view.resetDevicePixelRatio);
    addTearDown(t.view.resetPhysicalSize);
    await t.pumpWidget(
      MaterialApp(
        home: PsatReader(
          controller: AppController(MemoryPersistence()),
          question: q,
        ),
      ),
    );
    await t.pumpAndSettle();
    final report = find.byWidgetPredicate(
      (w) => w is PsatText && w.text.startsWith('‘갑’국 영유아'),
    );
    expect(report, findsOneWidget);
    final original = find.byKey(ValueKey(q.figures[0]['asset']));
    final firstChoice = find.byKey(ValueKey(q.figures[1]['asset']));
    expect(t.getBottomLeft(original).dy, lessThan(t.getTopLeft(report).dy));
    expect(t.getBottomLeft(report).dy, lessThan(t.getTopLeft(firstChoice).dy));
    var previousY = t.getTopLeft(firstChoice).dy;
    for (final figure in q.figures.skip(2)) {
      final nextY = t.getTopLeft(find.byKey(ValueKey(figure['asset']))).dy;
      expect(nextY, greaterThan(previousY));
      previousY = nextY;
    }
    expect(t.takeException(), isNull);
  });
}
