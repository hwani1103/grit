import 'dart:io';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/psat_model.dart';
import 'package:grit/psat_sets.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  test(
    'situation Set23 keeps original tables, shared passage and law scope',
    () async {
      final catalog = await loadPsatCatalog();
      final set = catalog.sets.singleWhere((s) => s.id == 'psat-situation-023');
      final qs = set.questionIds.map((id) => catalog.questions[id]!).toList();
      expect(qs.map((q) => q.number), [32, 33, 34, 35, 36, 37, 38, 39, 40, 1]);
      for (final i in [3, 4, 5, 6]) {
        expect(qs[i].figures.length, 1);
        expect(qs[i].data['figuresAfterBody'], [3, 6].contains(i));
      }
      expect(qs[3].body, contains('25명 미만'));
      expect(qs[6].body, contains('심사위원 3인'));
      expect(
        qs[7].body.split('<보 기>').first.trim(),
        qs[8].body.split('<상 황>').first.trim(),
      );
      expect(qs.last.body, contains('이하 이 조에서 같다'));
      expect(qs.last.body, contains('제00조(공공데이터의 제공 운영실태 평가)\n\n①'));
      for (final q in qs) {
        expect(PsatQuestion.fromJson(q.toJson()).toJson(), q.toJson());
        expect(File(q.original).lengthSync(), greaterThan(1000));
      }
    },
  );
}
