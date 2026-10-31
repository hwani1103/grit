import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/psat_sets.dart';
import 'package:grit/psat_text.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  test(
    '2024 common passage underlines exclude the four circled source labels',
    () async {
      final catalog = await loadPsatCatalog();
      // Verified against the four marked spans on the official 2024 page10.
      const expected = [
        '만약 우리가 p를 믿는다는 것이 인식적으로 정당화된다면 그것을 믿어야 하고, 만약 우리가 p를 믿는다는 것이 인식적으로 정당화되지 않는다면 그것을 믿어야 하는 것은 아니다',
        '우리가 p를 믿는다는 것은 자유롭게 선택할 수 있는 것이 아니다',
        '만약 우리가 p를 믿는다는 것이 자유롭게 선택할 수 있는 것이 아니라면, 우리에게 p를 믿어야 할 인식적 의무는 없다',
        '우리가 p를 믿는다는 것은 인식적으로 정당화되지 않는다',
      ];
      for (final id in [
        'kr-mpm-2024-07-27-psat-l-19',
        'kr-mpm-2024-07-27-psat-l-20',
      ]) {
        final q = catalog.questions[id]!;
        final spans = psatInlineSpans(
          q.body,
          q.underlines,
          underlineLabelAnchors: q.data['underlineLabelAnchors'] == true,
        );
        expect(
          spans
              .where((s) => s.style?.decoration == TextDecoration.underline)
              .map((s) => s.text)
              .toList(),
          expected,
          reason: id,
        );
        expect(
          TextSpan(children: spans).toPlainText(),
          q.body.replaceAll('<보기>', '보기'),
        );
        expect(q.body.split(expected.last).length, greaterThan(2));
      }
    },
  );
  test(
    'pre-review common passage snapshots retain their original bytes and display setting',
    () {
      final baseline =
          jsonDecode(
                File(
                  'artifacts/psat_remaining605_20261030/batch04/revealed-current.json',
                ).readAsStringSync(),
              )
              as List;
      for (final row in baseline) {
        final q = row['question'] as Map<String, dynamic>;
        if (![
          'kr-mpm-2024-07-27-psat-l-19',
          'kr-mpm-2024-07-27-psat-l-20',
        ].contains(q['id'])) {
          continue;
        }
        expect(q.containsKey('underlineLabelAnchors'), isFalse);
        expect((q['underlines'] as List).last, startsWith('㉣'));
      }
    },
  );
}
