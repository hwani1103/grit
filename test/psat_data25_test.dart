import 'dart:io';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/psat_model.dart';
import 'package:grit/psat_sets.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  test(
    'data Set25 retains map legends, common report and paired headers',
    () async {
      final catalog = await loadPsatCatalog();
      final set = catalog.sets.singleWhere((s) => s.id == 'psat-data-025');
      final qs = set.questionIds.map((id) => catalog.questions[id]!).toList();
      expect(qs.map((q) => q.number), List.generate(10, (i) => i + 14));
      expect(qs.map((q) => q.figures.length), [2, 3, 2, 1, 1, 1, 1, 1, 2, 6]);
      for (final i in [3, 7]) {
        expect(qs[i].data['choiceNote'], 'A → B → C');
      }
      expect(qs[8].data['choiceNote'], 'B → C');
      expect(qs[8].body, startsWith('<보고서>'));
      expect(qs[8].body, contains('다음으로 ‘갑’시에 거주하는 양육자의'));
      expect(qs[9].body, qs[8].body);
      expect(
        catalog.questions.containsKey('kr-mpm-2024-03-02-psat-d-13'),
        isFalse,
      );
      for (final q in qs) {
        expect(PsatQuestion.fromJson(q.toJson()).toJson(), q.toJson());
        expect(File(q.original).lengthSync(), greaterThan(1000));
      }
    },
  );
}
