import 'dart:io';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/psat_model.dart';
import 'package:grit/psat_sets.dart';
import 'package:grit/psat_text.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  test(
    'situation Set22 keeps legal hierarchy, blank labels and source fraction',
    () async {
      final catalog = await loadPsatCatalog();
      final set = catalog.sets.singleWhere((s) => s.id == 'psat-situation-022');
      final qs = set.questionIds.map((id) => catalog.questions[id]!).toList();
      expect(qs.map((q) => q.number), List.generate(10, (i) => i + 22));
      for (final q in qs) {
        expect(PsatQuestion.fromJson(q.toJson()).toJson(), q.toJson());
        expect(File(q.original).lengthSync(), greaterThan(1000));
      }
      final blocks = psatReadingBlocks(qs[0].body);
      expect(blocks.where((b) => b.startsWith('제00조')).length, 4);
      expect(blocks.any((b) => b.startsWith('8. 화폐')), isTrue);
      expect(qs[2].body, contains('「산림보호법」'));
      expect(qs[2].body, contains('\n\n<상 황>'));
      expect(qs[3].body, startsWith('제00조\n\n①'));
      expect(qs[5].data['choiceNote'], '(가) → (나)');
      expect(qs[5].body.split('[빈칸]').length - 1, 2);
      expect(qs[6].body, contains('2/3가 휩쓸려 사라졌다'));
      expect(qs[6].figures, isEmpty);
      expect(qs[7].body.split('[빈칸]').length - 1, 1);
    },
  );
}
