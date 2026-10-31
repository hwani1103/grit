import 'dart:io';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/psat_model.dart';
import 'package:grit/psat_sets.dart';
void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  test('verbal Set30 preserves blanks underlines and experimental units', () async {
    final catalog = await loadPsatCatalog();
    final set = catalog.sets.singleWhere((s) => s.id == 'psat-verbal-030');
    final qs = set.questionIds.map((id) => catalog.questions[id]!).toList();
    expect(qs.map((q) => q.number), [26,27,28,29,30,31,32,33,34,35]);
    expect('[빈칸]'.allMatches(qs[1].body).length, 2);
    expect(qs[1].choices.every((s) => s.contains('\n(나):')), isTrue);
    expect(qs[2].body, contains('“[빈칸]”'));
    expect(qs[5].data['underlines'], hasLength(1));
    expect(qs[6].data['underlines'], hasLength(1));
    expect(qs.last.body, contains('μM'));
    for (final q in qs) {
      expect(PsatQuestion.fromJson(q.toJson()).toJson(), q.toJson());
      expect(File(q.original).lengthSync(), greaterThan(1000));
    }
  });
}
