import 'dart:io';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/psat_model.dart';
import 'package:grit/psat_sets.dart';
void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  test('situation Set28 preserves legal titles fraction and calendar snapshot', () async {
    final catalog = await loadPsatCatalog();
    final set = catalog.sets.singleWhere((s) => s.id == 'psat-situation-028');
    final qs = set.questionIds.map((id) => catalog.questions[id]!).toList();
    expect(qs.map((q) => q.number), [2,3,4,5,6,7,8,9,10,11]);
    expect(qs.first.body, contains('제00조(소하천의 점용 등)'));
    expect(qs[5].body, contains('1/2박스'));
    expect(qs[3].body, contains('2023. 1. 30.'));
    expect(qs[3].body, isNot(contains('2023.\n\n1.')));
    expect(qs.last.data['figuresAfterBody'], true);
    expect(qs.last.figures.length, 1);
    for (final q in qs) {
      expect(PsatQuestion.fromJson(q.toJson()).toJson(), q.toJson());
      expect(File(q.original).lengthSync(), greaterThan(1000));
    }
  });
}
