import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/psat_model.dart';
import 'package:grit/psat_sets.dart';
import 'package:grit/psat_text.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  test(
    'verbal Set21 registered source items retain semantic typography',
    () async {
      final catalog = await loadPsatCatalog();
      final set = catalog.sets.singleWhere((s) => s.id == 'psat-verbal-021');
      final qs = set.questionIds.map((id) => catalog.questions[id]!).toList();
      expect(qs.map((q) => q.number), [12, 15, 16, 17, 18, 19, 20, 21, 22, 23]);
      for (final q in qs) {
        expect(q.steps.length, 5);
        expect(q.reasons.length, 5);
        expect(PsatQuestion.fromJson(q.toJson()).toJson(), q.toJson());
        expect(File(q.original).lengthSync(), greaterThan(1000));
        for (final u in q.underlines) {
          expect(q.body.split(u).length - 1, 1);
          expect(
            psatInlineSpans(q.body, q.underlines).any(
              (s) =>
                  s.style?.decoration == TextDecoration.underline &&
                  (s.text ?? '').contains(u),
            ),
            isTrue,
          );
        }
      }
      expect(qs[0].body.split('aⁿ＋bⁿ＝cⁿ').length - 1, 2);
      expect(qs[0].body, contains('[빈칸]'));
      expect(qs[2].body, contains('SnO₂'));
      expect(qs[2].underlines.length, 2);
      expect(qs[3].underlines.length, 1);
      expect(qs[5].body, qs[6].body);
      expect(qs[5].body.split('[빈칸]').length - 1, 2);
      expect(qs[5].body, contains('[kɔ́ːfi]'));
      expect(qs[6].choices[2], contains('[píːtsə]'));
    },
  );
}
