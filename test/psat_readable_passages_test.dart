import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/psat_sets.dart';
import 'package:grit/psat_text.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  test(
    'source labels scope repeated underlines without marking later mentions',
    () async {
      final catalog = await loadPsatCatalog();
      for (final entry in {
        'kr-mpm-2026-03-07-psat-l-36': '다중 타격 이론',
        'kr-mpm-2026-03-07-psat-l-38': '기본 전하량이 존재한다는 주장',
      }.entries) {
        final q = catalog.questions[entry.key]!;
        final spans = psatInlineSpans(
          q.body,
          q.underlines,
          underlineLabelAnchors: true,
        );
        expect(TextSpan(children: spans).toPlainText(), q.body.replaceAll('<보기>', '보기'));
        final marked = spans
            .where((s) => s.style?.decoration == TextDecoration.underline)
            .map((s) => s.text)
            .toList();
        expect(marked, [entry.value]);
        expect(q.body.split(entry.value).length, greaterThan(2));
      }
    },
  );
  test(
    'long language passages reflow and diagram references remain available',
    () async {
      final catalog = await loadPsatCatalog();
      for (final id in [
        'kr-mpm-2021-07-10-psat-l-04',
        'kr-mpm-2021-07-10-psat-l-17',
        'kr-mpm-2025-11-15-psat-l-12',
        'kr-mpm-2026-03-07-psat-l-36',
        'kr-mpm-2026-03-07-psat-l-38',
      ]) {
        expect(catalog.questions[id]!.body.length, greaterThan(400));
      }
      final particle = catalog.questions['kr-mpm-2021-07-10-psat-l-04']!;
      expect(particle.body, contains('[ab][ ][ ], [a][b][ ], [a][ ][b]'));
      expect(
        particle.body,
        contains(
          '[aa][ ][ ], [ ][aa][ ], [ ][ ][aa], [a][a][ ], [a][ ][a], [ ][a][a]',
        ),
      );
      final hiring = catalog.questions['kr-mpm-2021-07-10-psat-l-17']!;
      expect(hiring.figures.single['asset'], contains('2021-l17-2-poppler'));
      expect(hiring.data['figuresAfterBody'], true);
    },
  );
}
