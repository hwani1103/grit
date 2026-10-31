import 'dart:io';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/psat_model.dart';
import 'package:grit/psat_sets.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  test(
    'situation Set21 source bodies, law hierarchy and choice columns survive loading',
    () async {
      final catalog = await loadPsatCatalog();
      final set = catalog.sets.singleWhere((s) => s.id == 'psat-situation-021');
      final qs = set.questionIds.map((id) => catalog.questions[id]!).toList();
      expect(qs.map((q) => q.number), List.generate(10, (i) => i + 12));
      for (final q in qs) {
        expect(q.steps.length, 5);
        expect(q.reasons.length, 5);
        expect(PsatQuestion.fromJson(q.toJson()).toJson(), q.toJson());
        expect(File(q.original).lengthSync(), greaterThan(1000));
        if ([12, 16, 17, 18].contains(q.number)) {
          expect(q.body, isNotEmpty);
          if ([12, 16].contains(q.number)) {
            expect(q.figures.length, 1);
            expect(
              File(q.figures.single['asset'] as String).lengthSync(),
              greaterThan(10000),
            );
          } else {
            expect(q.figures, isEmpty);
            expect(q.tables, isNotEmpty);
          }
        }
      }
      expect(qs[2].data['choiceNote'], '작년 → 올해');
      expect(qs[8].data['choiceNote'], '(가) → (나)');
      expect(qs[8].body.split('[빈칸]').length - 1, 2);
      expect(qs[9].body, startsWith('제00조(수출입규제폐기물의 수출허가)\n\n①'));
      expect(qs[9].body, contains('\n\n1.'));
      expect(qs[9].body, contains('\n\n⑤'));
      expect(qs[7].body, contains('30MW'));
      expect(qs[8].body, contains('250kW'));
    },
  );
}
