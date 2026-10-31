import 'dart:io';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/psat_model.dart';
import 'package:grit/psat_sets.dart';
void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  test('data Set28 preserves graph choices report order and held source exclusion', () async {
    final catalog = await loadPsatCatalog();
    final set = catalog.sets.singleWhere((s) => s.id == 'psat-data-028');
    final qs = set.questionIds.map((id) => catalog.questions[id]!).toList();
    expect(qs.map((q) => q.number), [6,7,8,9,10,11,12,13,15,16]);
    expect(qs[5].figures.length, 7);
    expect(qs[7].figures.length, 5);
    expect(qs[7].data['figuresAfterBody'], true);
    expect(qs[7].body, contains('4년 이상'));
    expect(qs[8].body, contains('A B C D E'));
    for (final q in qs) {
      expect(PsatQuestion.fromJson(q.toJson()).toJson(), q.toJson());
      expect(File(q.original).lengthSync(), greaterThan(1000));
      for (final f in q.figures) {expect(File(f['asset'] as String).lengthSync(), greaterThan(1000));}
    }
  });
}
