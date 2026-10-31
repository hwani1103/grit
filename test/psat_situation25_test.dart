import 'dart:io';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/psat_model.dart';
import 'package:grit/psat_sets.dart';
import 'package:grit/psat_text.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  test('situation Set25 retains source figures, shared passage, pair headers and legal blocks', () async {
    final catalog = await loadPsatCatalog();
    final set = catalog.sets.singleWhere((s) => s.id == 'psat-situation-025');
    final qs = set.questionIds.map((id) => catalog.questions[id]!).toList();
    expect(qs.map((q) => q.number), List.generate(10, (i) => i + 12));
    expect(qs.fold<int>(0, (n, q) => n + q.figures.length), 9);
    expect(qs[1].data['figuresAfterBody'] == true, isFalse);
    for (final i in [0, 4, 5, 6]) {
      expect(qs[i].data['figuresAfterBody'], isTrue);
    }
    expect(qs[2].data['choiceNote'], '최솟값 → 최댓값');
    expect(qs[8].data['choiceNote'], '직접효과 → 비율승수');
    for (final i in [7, 8]) {
      expect(qs[i].body, startsWith('□□연구소에서'));
      expect(qs[i].body, contains('관광객의 최초 관광지출로 나눈 값이다.'));
    }
    final blocks = psatReadingBlocks(qs[9].body);
    expect(blocks, contains('제◇◇조(벌칙)'));
    expect(blocks.where((b) => RegExp(r'^제[○□△◇]+조\(').hasMatch(b)).length, 4);
    expect(blocks.where((b) => RegExp(r'^[123]\. “').hasMatch(b)).length, 3);
    expect(blocks, contains('이 법에서 사용하는 용어의 뜻은 다음과 같다.'));
    expect(blocks.join().replaceAll(RegExp(r'\s+'), ''), qs[9].body.replaceAll(RegExp(r'\s+'), ''));
    for (final q in qs) {
      expect(PsatQuestion.fromJson(q.toJson()).toJson(), q.toJson());
      expect(File(q.original).lengthSync(), greaterThan(1000));
    }
  });
}
