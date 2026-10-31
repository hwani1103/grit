import 'dart:io';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/psat_model.dart';
import 'package:grit/psat_sets.dart';
import 'package:grit/psat_text.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  test('situation Set24 retains legal hierarchy, rate table order and paired headers', () async {
    final catalog = await loadPsatCatalog();
    final set = catalog.sets.singleWhere((s) => s.id == 'psat-situation-024');
    final qs = set.questionIds.map((id) => catalog.questions[id]!).toList();
    expect(qs.map((q) => q.number), List.generate(10, (i) => i + 2));
    for (final q in qs.take(4)) {
      final blocks = psatReadingBlocks(q.body);
      expect(blocks.where((b) => RegExp(r'^제[0-9○□△]+조\(').hasMatch(b)), isNotEmpty);
      expect(blocks.join().replaceAll(RegExp(r'\s+'), ''), q.body.replaceAll(RegExp(r'\s+'), ''));
      expect(blocks.any((b) => b.startsWith('① ')), isTrue);
    }
    expect(qs[6].data['choiceNote'], '㉠ → ㉡');
    expect(qs[7].data['choiceNote'], '甲 → 乙');
    expect(qs[7].figures.length, 1);
    expect(qs[7].data['figuresAfterBody'] == true, isFalse);
    expect(qs[7].body, startsWith('<상 황>'));
    expect(qs[7].body, contains('급여이체 계좌는 바꿀 수 없어'));
    for (final q in qs) {
      expect(PsatQuestion.fromJson(q.toJson()).toJson(), q.toJson());
      expect(File(q.original).lengthSync(), greaterThan(1000));
    }
  });
}
