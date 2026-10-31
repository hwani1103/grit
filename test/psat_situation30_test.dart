import 'dart:io';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/psat_model.dart';
import 'package:grit/psat_sets.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  test(
    'situation Set30 keeps legal dates formula and linked table conditions',
    () async {
      final catalog = await loadPsatCatalog();
      final set = catalog.sets.singleWhere((s) => s.id == 'psat-situation-030');
      final qs = set.questionIds.map((id) => catalog.questions[id]!).toList();
      expect(qs.map((q) => q.number), [23, 24, 25, 26, 27, 28, 29, 30, 31, 32]);
      expect(qs[1].choices[1], contains('2023. 3. 2.'));
      expect(qs[3].body, contains('○○약국'));
      expect(qs[3].data['figuresAfterBody'], isTrue);
      expect(qs[6].figures, hasLength(1));
      expect(qs[6].choices[2], '최댓값: 108\n최솟값: 45');
      expect(qs[7].data['bodyBeforeFigures'], contains('일 지수'));
      expect(qs[7].data['bodyAfterFigureCount'], 1);
      expect(qs[7].body, contains('3이 작았다'));
      expect(qs[7].figures, hasLength(1));
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
