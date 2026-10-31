import 'dart:io';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/psat_model.dart';
import 'package:grit/psat_sets.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  test('verbal Set26 preserves choice order, corrections, logical conditions', () async {
    final catalog = await loadPsatCatalog();
    final set = catalog.sets.singleWhere((s) => s.id == 'psat-verbal-026');
    final qs = set.questionIds.map((id) => catalog.questions[id]!).toList();
    expect(qs.map((q) => q.number), List.generate(10, (i) => i + 26));
    expect(qs.first.data['choiceNote'], '선택지의 순서: (가) → (나) → (다)');
    expect(qs[1].data['underlines'], hasLength(5));
    expect(qs[6].data['underlines'], hasLength(3));
    expect(qs[4].body, contains('「생명윤리 및 안전에 관한 법률」'));
    expect(qs[7].body, contains('총무과에는 한 명만'));
    expect(qs[8].body, contains('세 명의 예측은 옳고'));
    for (final q in qs) {
      expect(PsatQuestion.fromJson(q.toJson()).toJson(), q.toJson());
      expect(File(q.original).lengthSync(), greaterThan(1000));
      expect(RegExp(r'[\uE000-\uF8FF\uFFFD\u2060]').hasMatch(q.body), isFalse);
    }
  });
}
