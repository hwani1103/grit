import 'dart:io';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/psat_model.dart';
import 'package:grit/psat_sets.dart';
void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  test('situation Set29 preserves source tables conditions common text and nested law', () async {
    final catalog = await loadPsatCatalog();
    final set = catalog.sets.singleWhere((s) => s.id == 'psat-situation-029');
    final qs = set.questionIds.map((id) => catalog.questions[id]!).toList();
    expect(qs.map((q) => q.number), [12,13,14,15,16,17,18,20,21,22]);
    expect(qs.expand((q) => q.figures).length, 5);
    expect(qs[7].body, contains('1911년에는'));
    expect(qs[7].body, contains('ㄱ. A가'));
    expect(qs.last.body, contains('가. 국립'));
    for (final q in qs) {
      expect(PsatQuestion.fromJson(q.toJson()).toJson(), q.toJson());
      expect(File(q.original).lengthSync(), greaterThan(1000));
      for (final f in q.figures) { expect(File(f['asset'] as String).lengthSync(), greaterThan(1000)); }
    }
  });
}
