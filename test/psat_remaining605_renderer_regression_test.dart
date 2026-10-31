import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/psat_sets.dart';
import 'package:grit/psat_text.dart' as current;
import '../artifacts/psat_remaining605_20261030/batch25/psat_text-before.dart'
    as baseline;

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  test('quoted anchor fix preserves all other catalog body spans', () async {
    final catalog = await loadPsatCatalog();
    expect(catalog.questions.length, 900);
    for (final q in catalog.questions.values) {
      final flag = q.data['underlineLabelAnchors'] == true;
      final now = current.psatInlineSpans(
        q.body,
        q.underlines,
        underlineLabelAnchors: flag,
      );
      final before = baseline.psatInlineSpans(
        q.body,
        q.underlines,
        underlineLabelAnchors: flag,
      );
      expect(
        TextSpan(children: now).toPlainText(),
        TextSpan(children: before).toPlainText(),
        reason: q.id,
      );
      if (const {
        'kr-mpm-2026-07-18-psat-l-06',
        'kr-mpm-2025-03-08-psat-l-30',
      }.contains(q.id)) {
        expect(
          now
              .where((s) => s.style?.decoration == TextDecoration.underline)
              .map((s) => s.text)
              .toList(),
          [q.id == 'kr-mpm-2026-07-18-psat-l-06' ? '전이' : '이익조정'],
        );
      } else {
        expect(now, before, reason: q.id);
      }
    }
  });
}
