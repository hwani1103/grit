import 'dart:io';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/psat_model.dart';
import 'package:grit/psat_sets.dart';
void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  test('verbal Set28 retains pi correction underlines and logical blank', () async {
    final catalog = await loadPsatCatalog();
    final set = catalog.sets.singleWhere((s) => s.id == 'psat-verbal-028');
    final qs = set.questionIds.map((id) => catalog.questions[id]!).toList();
    expect(qs.map((q) => q.number), [6,7,8,9,10,11,12,13,14,15]);
    expect(qs[1].body, contains('π/4'));
    expect((qs[4].data['underlines'] as List).length, 5);
    expect((qs[5].data['underlines'] as List).length, 1);
    expect(qs.last.body, contains('[빈칸]'));
    for (final q in qs) {
      expect(PsatQuestion.fromJson(q.toJson()).toJson(), q.toJson());
      expect(File(q.original).lengthSync(), greaterThan(1000));
    }
  });
}
