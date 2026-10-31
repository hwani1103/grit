import 'dart:io';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/psat_model.dart';
import 'package:grit/psat_sets.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  test('data Set27 retains bounds notes and source report graphics', () async {
    final catalog = await loadPsatCatalog();
    final set = catalog.sets.singleWhere((s) => s.id == 'psat-data-027');
    final qs = set.questionIds.map((id) => catalog.questions[id]!).toList();
    expect(qs.map((q) => q.number), [35, 37, 38, 39, 40, 1, 2, 3, 4, 5]);
    expect(qs.map((q) => q.figures.length), [1, 1, 2, 2, 1, 2, 2, 7, 1, 1]);
    expect((qs[6].data['underlines'] as List).length, 4);
    expect(qs[7].body, isEmpty);
    expect(
      catalog.questions.containsKey('kr-mpm-2024-03-02-psat-d-36'),
      isFalse,
    );
    for (final q in qs) {
      expect(PsatQuestion.fromJson(q.toJson()).toJson(), q.toJson());
      expect(File(q.original).lengthSync(), greaterThan(1000));
    }
  });
}
