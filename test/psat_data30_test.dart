import 'dart:io';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/psat_model.dart';
import 'package:grit/psat_sets.dart';
void main() {
 TestWidgetsFlutterBinding.ensureInitialized();
 test('data Set30 retains common deviations, labeled extrema and complete graph choices', () async {
  final catalog = await loadPsatCatalog();
  final set = catalog.sets.singleWhere((s) => s.id == 'psat-data-030');
  final qs = set.questionIds.map((id) => catalog.questions[id]!).toList();
  expect(qs.map((q) => q.number), [27,28,29,30,31,32,33,34,35,36]);
  expect(qs.expand((q) => q.figures).length, 23);
  expect(qs[3].figures.length, 5);
  expect(qs[9].figures.length, 8);
  expect(qs[4].choices.first, '최솟값: －4\n최댓값: 3');
  for (final q in qs) {
   expect(PsatQuestion.fromJson(q.toJson()).toJson(), q.toJson());
   expect(File(q.original).lengthSync(), greaterThan(1000));
   for (final f in q.figures) {expect(File(f['asset'] as String).lengthSync(), greaterThan(1000));}
  }
 });
}
