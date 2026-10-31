import 'dart:io';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/psat_model.dart';
import 'package:grit/psat_sets.dart';
void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  test('verbal Set29 retains shared passage blanks and staged assignment distinction', () async {
    final catalog = await loadPsatCatalog();
    final set = catalog.sets.singleWhere((s) => s.id == 'psat-verbal-029');
    final qs = set.questionIds.map((id) => catalog.questions[id]!).toList();
    expect(qs.map((q) => q.number), [16,17,18,19,20,21,22,23,24,25]);
    expect(qs[3].body, qs[4].body);
    expect('[빈칸]'.allMatches(qs[3].body).length, 3);
    expect(qs[3].choices.every((s) => s.contains('\n(나):') && s.contains('\n(다):')), isTrue);
    expect(qs.first.body, contains('\n\n<추가 원칙>'));
    for (final q in qs) {
      expect(PsatQuestion.fromJson(q.toJson()).toJson(), q.toJson());
      expect(File(q.original).lengthSync(), greaterThan(1000));
    }
  });
}
