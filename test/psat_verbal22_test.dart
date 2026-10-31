import 'dart:io';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/psat_model.dart';
import 'package:grit/psat_sets.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  test('verbal Set22 preserves blanks, choice pairs and marked term', () async {
    final catalog = await loadPsatCatalog();
    final set = catalog.sets.singleWhere((s) => s.id == 'psat-verbal-022');
    final qs = set.questionIds.map((id) => catalog.questions[id]!).toList();
    expect(qs.map((q) => q.number), [24, 25, 26, 27, 28, 29, 30, 31, 32, 35]);
    for (final q in qs) {
      expect(PsatQuestion.fromJson(q.toJson()).toJson(), q.toJson());
      expect(File(q.original).lengthSync(), greaterThan(1000));
    }
    expect(qs[2].body.split('[빈칸]').length - 1, 1);
    expect(qs[3].body.split('[빈칸]').length - 1, 2);
    expect(qs[4].body.split('[빈칸]').length - 1, 3);
    expect(qs[3].choices.every((c) => c.contains('\n(나):')), isTrue);
    expect(qs[4].data['choiceNote'], '(가) → (나) → (다)');
    expect(qs[6].data['underlines'], ['㉠‘이익조정’']);
    expect(qs[8].body, contains('\n\nA:'));
    expect(qs[8].body, contains('\n\nB:'));
    expect(qs[9].body, contains('\n\n갑:'));
  });
}
