import 'dart:io';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/psat_model.dart';
import 'package:grit/psat_sets.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  test('data Set26 preserves shared figures and report underlines', () async {
    final catalog = await loadPsatCatalog();
    final set = catalog.sets.singleWhere((s) => s.id == 'psat-data-026');
    final qs = set.questionIds.map((id) => catalog.questions[id]!).toList();
    expect(qs.map((q) => q.number), [24, 25, 26, 27, 29, 30, 31, 32, 33, 34]);
    expect(qs.map((q) => q.figures.length), [4, 1, 5, 2, 6, 1, 1, 3, 2, 1]);
    expect(qs.first.data['figuresAfterBody'], isTrue);
    expect(qs.first.body, startsWith('<보고서>'));
    expect(qs[4].body, isEmpty);
    expect((qs[8].data['underlines'] as List).length, 4);
    expect(
      catalog.questions.containsKey('kr-mpm-2024-03-02-psat-d-28'),
      isFalse,
    );
    for (final q in qs) {
      expect(PsatQuestion.fromJson(q.toJson()).toJson(), q.toJson());
      expect(File(q.original).lengthSync(), greaterThan(1000));
    }
  });
}
