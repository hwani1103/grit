import 'dart:io';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/psat_model.dart';
import 'package:grit/psat_sets.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  test(
    'situation Set27 retains windows, evaluation notes and legal exceptions',
    () async {
      final catalog = await loadPsatCatalog();
      final set = catalog.sets.singleWhere((s) => s.id == 'psat-situation-027');
      final qs = set.questionIds.map((id) => catalog.questions[id]!).toList();
      expect(qs.map((q) => q.number), [32, 33, 34, 35, 36, 37, 38, 39, 40, 1]);
      expect(qs.map((q) => q.figures.length), [0, 0, 0, 0, 1, 2, 1, 0, 0, 0]);
      expect(qs[5].data['bodyBeforeFigures'], contains('전기차충전기 설치업체'));
      expect(qs[5].data['bodyAfterFigureCount'], 1);
      expect(qs[5].body, contains('2.5점의 가점'));
      expect(qs[6].data['figuresAfterBody'], isTrue);
      expect(qs[8].body, contains(qs[7].body));
      expect(qs[4].body, contains('직전 10개 경기 전적'));
      expect(qs.last.body, contains('다만 제1호에 해당하는 경우에는'));
      expect(qs.last.body, contains('다만 제5항 제3호에 따라'));
      for (final q in qs) {
        expect(PsatQuestion.fromJson(q.toJson()).toJson(), q.toJson());
        expect(File(q.original).lengthSync(), greaterThan(1000));
      }
    },
  );
}
