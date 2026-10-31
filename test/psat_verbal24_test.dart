import 'dart:io';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/psat_model.dart';
import 'package:grit/psat_sets.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  test('verbal Set24 retains original underlines, blank and subscript in snapshots', () async {
    final catalog = await loadPsatCatalog();
    final set = catalog.sets.singleWhere((s) => s.id == 'psat-verbal-024');
    final qs = set.questionIds.map((id) => catalog.questions[id]!).toList();
    expect(qs.map((q) => q.number), List.generate(10, (i) => i + 6));
    expect((qs[2].data['underlines'] as List).length, 5);
    expect((qs[9].data['underlines'] as List).length, 2);
    expect(qs[6].body, contains('산소(O₂)'));
    expect(qs[6].body, contains('“[빈칸]?”'));
    for (final q in qs) {
      expect(PsatQuestion.fromJson(q.toJson()).toJson(), q.toJson());
      expect(File(q.original).lengthSync(), greaterThan(1000));
      expect(RegExp(r'[\uE000-\uF8FF\uFFFD\u2060]').hasMatch(q.body), isFalse);
    }
  });
}
