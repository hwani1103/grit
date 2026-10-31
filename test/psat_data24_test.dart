import 'dart:io';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/psat_model.dart';
import 'package:grit/psat_sets.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  test(
    'data Set24 keeps graphs, report underlines and exact stopping rules',
    () async {
      final catalog = await loadPsatCatalog();
      final set = catalog.sets.singleWhere((s) => s.id == 'psat-data-024');
      final qs = set.questionIds.map((id) => catalog.questions[id]!).toList();
      expect(qs.map((q) => q.number), List.generate(10, (i) => i + 3));
      expect(qs.map((q) => q.figures.length), [5, 1, 2, 2, 7, 5, 1, 1, 3, 1]);
      expect(qs.first.data['figuresAfterBody'], isTrue);
      expect(qs.first.body, contains('2022년 이후 중소도시'));
      expect(qs[8].data['underlines'], hasLength(5));
      for (final s in qs[8].data['underlines'] as List) {
        expect(qs[8].body.split(s as String), hasLength(2));
      }
      expect(qs[2].data['steps'][2], contains('①과 ⑤'));
      expect(qs[6].data['steps'][2], contains('①과 ④'));
      for (final q in qs) {
        expect(PsatQuestion.fromJson(q.toJson()).toJson(), q.toJson());
        expect(File(q.original).lengthSync(), greaterThan(1000));
      }
    },
  );
}
