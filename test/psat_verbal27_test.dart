import 'dart:io';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/psat_model.dart';
import 'package:grit/psat_sets.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  test('verbal Set27 retains shared passage, hypothesis and source years', () async {
    final catalog = await loadPsatCatalog();
    final set = catalog.sets.singleWhere((s) => s.id == 'psat-verbal-027');
    final qs = set.questionIds.map((id) => catalog.questions[id]!).toList();
    expect(qs.map((q) => q.number), [36,37,38,39,40,1,2,3,4,5]);
    expect(qs[2].data['underlines'], hasLength(1));
    expect(qs[4].body, contains(qs[3].body));
    expect(qs[4].body, contains('자신의 실험 결과를 폐기하고'));
    expect(qs[3].body, contains('유의수준보다 작을 때'));
    expect(qs.last.data['source'], startsWith('2023.03.04'));
    for (final q in qs) {
      expect(PsatQuestion.fromJson(q.toJson()).toJson(), q.toJson());
      expect(File(q.original).lengthSync(), greaterThan(1000));
    }
  });
}
