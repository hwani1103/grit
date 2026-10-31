import 'dart:io';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/psat_model.dart';
import 'package:grit/psat_sets.dart';
void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  test('data Set29 retains shared mask source graphs and full rate figures', () async {
    final catalog = await loadPsatCatalog();
    final set = catalog.sets.singleWhere((s) => s.id == 'psat-data-029');
    final qs = set.questionIds.map((id) => catalog.questions[id]!).toList();
    expect(qs.map((q) => q.number), [17,18,19,20,21,22,23,24,25,26]);
    expect(qs.expand((q) => q.figures).length, 27);
    expect(qs[2].figures.length, 8);
    expect(qs[8].figures.length, 5);
    expect(qs[7].steps.join(' '), contains('366'));
    expect(qs[1].prompt, contains('6～11월'));
    for (final q in qs) {
      expect(PsatQuestion.fromJson(q.toJson()).toJson(), q.toJson());
      expect(File(q.original).lengthSync(), greaterThan(1000));
      for (final f in q.figures) { expect(File(f['asset'] as String).lengthSync(), greaterThan(1000)); }
    }
  });
}
