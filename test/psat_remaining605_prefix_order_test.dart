import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/psat.dart';
import 'package:grit/psat_sets.dart';
import 'package:grit/psat_text.dart';
import 'package:grit/store.dart';
import 'store_test.dart' show MemoryPersistence;

void main() {
  testWidgets('source prose brackets the original figure in reading order', (t) async {
    final catalog = (await t.runAsync(loadPsatCatalog))!;
    expect(catalog.questions.values.where((q) => q.data.containsKey('bodyBeforeFigures')).map((q) => q.id).toSet(), {
      'kr-mpm-2024-03-02-psat-s-13',
      'kr-mpm-2024-03-02-psat-s-25',
      'kr-mpm-2024-03-02-psat-s-37',
      'kr-mpm-2024-03-02-psat-d-39',
      'kr-mpm-2023-03-04-psat-s-18',
      'kr-mpm-2023-03-04-psat-s-30',
    });
    t.view.devicePixelRatio = 1;
    t.view.physicalSize = const Size(390, 844);
    addTearDown(t.view.resetDevicePixelRatio);
    addTearDown(t.view.resetPhysicalSize);
    for (final id in ['kr-mpm-2024-03-02-psat-s-13', 'kr-mpm-2024-03-02-psat-s-25', 'kr-mpm-2024-03-02-psat-s-37', 'kr-mpm-2023-03-04-psat-s-18', 'kr-mpm-2023-03-04-psat-s-30']) {
      final q = catalog.questions[id]!;
      final n = q.number;
      await t.pumpWidget(MaterialApp(home: PsatReader(controller: AppController(MemoryPersistence()), question: q)));
      await t.pumpAndSettle();
      final prefix = find.byWidgetPredicate((w) => w is PsatPassage && w.text == q.data['bodyBeforeFigures']);
      final body = find.byWidgetPredicate((w) => w is PsatPassage && w.text == q.body);
      final figure = find.byKey(ValueKey(q.figures.first['asset']));
      expect(prefix, findsOneWidget);
      expect(body, findsOneWidget);
      expect(t.getBottomLeft(prefix).dy, lessThan(t.getTopLeft(figure).dy));
      expect(t.getBottomLeft(figure).dy, lessThan(t.getTopLeft(body).dy));
      if (n == 37) {
        final secondFigure = find.byKey(ValueKey(q.figures.last['asset']));
        expect(t.getBottomLeft(body).dy, lessThan(t.getTopLeft(secondFigure).dy));
      }
      expect(t.takeException(), isNull);
      await t.pumpWidget(const SizedBox.shrink());
    }
    final q = catalog.questions['kr-mpm-2024-03-02-psat-d-39']!;
    await t.pumpWidget(MaterialApp(home: PsatReader(controller: AppController(MemoryPersistence()), question: q)));
    await t.pumpAndSettle();
    final prefix = find.byWidgetPredicate((w) => w is PsatPassage && w.text == q.data['bodyBeforeFigures']);
    final firstFigure = find.byKey(ValueKey(q.figures.first['asset']));
    final lastFigure = find.byKey(ValueKey(q.figures.last['asset']));
    expect(prefix, findsOneWidget);
    expect(t.getBottomLeft(prefix).dy, lessThan(t.getTopLeft(firstFigure).dy));
    expect(t.getBottomLeft(firstFigure).dy, lessThan(t.getTopLeft(lastFigure).dy));
    expect(q.body, isEmpty);
    expect(t.takeException(), isNull);
  });
}
