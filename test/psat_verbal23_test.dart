import 'dart:io';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/psat_model.dart';
import 'package:grit/psat_sets.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  test(
    'verbal Set23 retains shared passage, scientific symbols and experiment legend',
    () async {
      final catalog = await loadPsatCatalog();
      final set = catalog.sets.singleWhere((s) => s.id == 'psat-verbal-023');
      final qs = set.questionIds.map((id) => catalog.questions[id]!).toList();
      expect(qs.map((q) => q.number), [36, 37, 38, 39, 40, 1, 2, 3, 4, 5]);
      expect(qs.first.body, contains('cm⁻¹'));
      for (final symbol in ['α', 'β', 'γ']) {
        expect(qs.first.body, contains(symbol));
      }
      expect(qs[1].figures.length, 1);
      expect(qs[1].data['figuresAfterBody'], isTrue);
      expect(qs[1].body, contains('P 억제제는 뇌에서 ROS의 생성을 저해한다.'));
      expect(qs[4].body.split('<보 기>').first.trim(), qs[3].body);
      expect(qs[5].body, contains('『경국대전』'));
      expect(qs[6].body, contains('『삼우당실기』'));
      expect(qs[6].body, contains('『고려사』'));
      for (final q in qs) {
        expect(PsatQuestion.fromJson(q.toJson()).toJson(), q.toJson());
        expect(File(q.original).lengthSync(), greaterThan(1000));
        expect(
          RegExp(r'[\uE000-\uF8FF\uFFFD\u2060]').hasMatch(q.body),
          isFalse,
        );
      }
    },
  );
}
