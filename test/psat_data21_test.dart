import 'dart:io';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/psat_model.dart';
import 'package:grit/psat_sets.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  test('data Set21 retains shared tables and all five graph choices', () async {
    final catalog = await loadPsatCatalog();
    final set = catalog.sets.singleWhere((s) => s.id == 'psat-data-021');
    final qs = set.questionIds.map((id) => catalog.questions[id]!).toList();
    expect(qs.map((q) => q.number), List.generate(10, (i) => i + 11));
    expect(qs.map((q) => q.figures.length), [1, 2, 2, 7, 2, 1, 3, 1, 1, 1]);
    for (final q in qs) {
      expect(PsatQuestion.fromJson(q.toJson()).toJson(), q.toJson());
      expect(File(q.original).lengthSync(), greaterThan(1000));
    }
    for (var i = 0; i < 2; i++) {
      expect(
        File(qs[2].figures[i]['asset'] as String).readAsBytesSync(),
        File(qs[3].figures[i]['asset'] as String).readAsBytesSync(),
      );
    }
    expect(qs[3].choices, ['자료 1', '자료 2', '자료 3', '자료 4', '자료 5']);
    expect(qs[3].figures.skip(2).map((f) => (f['caption'] as String)[0]), [
      '①',
      '②',
      '③',
      '④',
      '⑤',
    ]);
    expect(qs.last.choices, ['ㄱ', 'ㄴ', 'ㄱ, ㄷ', 'ㄴ, ㄷ', 'ㄱ, ㄴ, ㄷ']);
  });
}
