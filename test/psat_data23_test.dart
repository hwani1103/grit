import 'dart:io';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/psat_model.dart';
import 'package:grit/psat_sets.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  test(
    'data Set23 keeps source graphics and excludes held candidates',
    () async {
      final catalog = await loadPsatCatalog();
      final set = catalog.sets.singleWhere((s) => s.id == 'psat-data-023');
      final qs = set.questionIds.map((id) => catalog.questions[id]!).toList();
      expect(qs.map((q) => q.number), [32, 33, 35, 36, 37, 38, 39, 40, 1, 2]);
      expect(qs.map((q) => q.figures.length), [2, 2, 2, 3, 2, 1, 1, 2, 4, 2]);
      expect(qs.first.data['choiceNote'], 'A → B');
      expect(qs.last.data['choiceNote'], 'A → B → C → D');
      expect(qs[4].body, contains('1개 유형의 부동산만을 보유한'));
      expect(qs[7].body, contains('지급대상 4인 이상 세대'));
      expect(
        catalog.questions.containsKey('kr-mpm-2025-03-08-psat-d-31'),
        isFalse,
      );
      expect(
        catalog.questions.containsKey('kr-mpm-2025-03-08-psat-d-34'),
        isFalse,
      );
      for (final q in qs) {
        expect(PsatQuestion.fromJson(q.toJson()).toJson(), q.toJson());
        expect(File(q.original).lengthSync(), greaterThan(1000));
      }
    },
  );
}
