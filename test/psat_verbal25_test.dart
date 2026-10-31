import 'dart:io';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/psat_model.dart';
import 'package:grit/psat_sets.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  test('verbal Set25 retains shared passage, underlines and source book marks', () async {
    final catalog = await loadPsatCatalog();
    final set = catalog.sets.singleWhere((s) => s.id == 'psat-verbal-025');
    final qs = set.questionIds.map((id) => catalog.questions[id]!).toList();
    expect(qs.map((q) => q.number), List.generate(10, (i) => i + 16));
    expect(qs.first.data['underlines'], hasLength(6));
    expect(qs[4].body.startsWith(qs[3].body), isTrue);
    expect(qs[3].body, contains('총괄 관리자만이'));
    expect(qs[4].body, contains('ㄷ. 우리 사회의 조직 체계에서'));
    expect(qs[6].body, contains('『경국대전』'));
    expect(qs[6].choices.last, contains('『경국대전』'));
    for (final q in qs) {
      expect(PsatQuestion.fromJson(q.toJson()).toJson(), q.toJson());
      expect(File(q.original).lengthSync(), greaterThan(1000));
      expect(RegExp(r'[\uE000-\uF8FF\uFFFD\u2060]').hasMatch(q.body), isFalse);
    }
  });
}
