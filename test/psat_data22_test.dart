import 'dart:io';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/psat_model.dart';
import 'package:grit/psat_sets.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  test(
    'data Set22 retains cross-column graphs and both common-table copies',
    () async {
      final catalog = await loadPsatCatalog();
      final set = catalog.sets.singleWhere((s) => s.id == 'psat-data-022');
      final qs = set.questionIds.map((id) => catalog.questions[id]!).toList();
      expect(qs.map((q) => q.number), List.generate(10, (i) => i + 21));
      expect(qs.map((q) => q.figures.length), [2, 1, 1, 1, 1, 1, 5, 6, 3, 7]);
      for (final q in qs) {
        expect(PsatQuestion.fromJson(q.toJson()).toJson(), q.toJson());
        expect(File(q.original).lengthSync(), greaterThan(1000));
      }
      for (var i = 0; i < 3; i++) {
        expect(
          File(qs[8].figures[i]['asset'] as String).readAsBytesSync(),
          File(qs[9].figures[i]['asset'] as String).readAsBytesSync(),
        );
      }
      for (final pair in [(6, 1), (7, 2), (9, 3)]) {
        expect(
          qs[pair.$1].figures
              .skip(pair.$2)
              .map((f) => (f['caption'] as String)[0]),
          ['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ'],
        );
      }
      expect(qs.last.choices, ['ㄱ, ㄴ', 'ㄱ, ㄷ', 'ㄴ, ㄷ', 'ㄴ, ㄹ', 'ㄷ, ㄹ']);
    },
  );
}
