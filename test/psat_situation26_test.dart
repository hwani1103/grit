import 'dart:io';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/psat_model.dart';
import 'package:grit/psat_sets.dart';
import 'package:grit/psat_text.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  test(
    'situation Set26 keeps legal hierarchy, formulas and original figures',
    () async {
      final catalog = await loadPsatCatalog();
      final set = catalog.sets.singleWhere((s) => s.id == 'psat-situation-026');
      final qs = set.questionIds.map((id) => catalog.questions[id]!).toList();
      expect(qs.map((q) => q.number), List.generate(10, (i) => i + 22));
      expect(qs.fold<int>(0, (n, q) => n + q.figures.length), 4);
      expect(qs[5].body, contains('탄소중립포인트'));
      expect(qs[5].tables, isNotEmpty);
      expect(qs[5].figures, isEmpty);
      expect(qs[3].data['bodyBeforeFigures'], contains('제○○조(어장청소 등)'));
      expect(qs[3].body, startsWith('③'));
      final legal = psatReadingBlocks(qs.first.body);
      expect(legal.where((x) => x.startsWith('제△△조(참전명예수당)')), hasLength(1));
      for (final q in qs) {
        expect(PsatQuestion.fromJson(q.toJson()).toJson(), q.toJson());
        expect(File(q.original).lengthSync(), greaterThan(1000));
        for (final f in q.figures) {
          expect(File(f['asset'] as String).lengthSync(), greaterThan(1000));
        }
      }
    },
  );
}
