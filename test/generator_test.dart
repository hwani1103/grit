import 'dart:convert';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/model.dart';

void main() {
  test(
    '500 seeds per set satisfy counts, exact comparison and difficulty rules',
    () {
      final bins = [0, 0, 0, 0];
      for (var seed = 0; seed < 500; seed++) {
        for (final kind in SetKind.values) {
          final problems = Generator(seed).generate(kind);
          expect(problems.length, switch (kind) {
            SetKind.addition => 5,
            SetKind.multiplication => 18,
            SetKind.division => 15,
          });
          final signatures = <String>{};
          for (var i = 0; i < problems.length; i++) {
            final p = problems[i];
            if (p.type == ProblemType.table) {
              final spec = Generator.tableSpecs[i];
              expect(p.hidden.length, spec[2]);
              expect(Generator.solveRounds(p), inInclusiveRange(2, 4));
              for (var r = 0; r < spec[0]; r++) {
                for (var c = 0; c < spec[1]; c++) {
                  expect(p.values[r][c], inInclusiveRange(spec[3], spec[4]));
                }
                expect(
                  p.values[r].take(spec[1]).fold(0, (a, b) => a + b),
                  p.values[r].last,
                );
              }
              for (var c = 0; c <= spec[1]; c++) {
                expect(
                  p.values.take(spec[0]).fold(0, (a, r) => a + r[c]),
                  p.values.last[c],
                );
              }
            } else if (p.type == ProblemType.product) {
              final a = p.values[0], b = p.values[1];
              expect((a[0] - b[0]) * (a[1] - b[1]), lessThan(0));
              expect(
                Generator.gap(a[0] * a[1], b[0] * b[1]),
                inInclusiveRange(.10, .25),
              );
              expect(p.relation, a[0] * a[1] > b[0] * b[1] ? '>' : '<');
            } else if (p.type == ProblemType.fraction) {
              for (final pair in p.values) {
                for (final n in pair) {
                  expect(n, inInclusiveRange(10, 349));
                }
              }
              final a = p.values[0], b = p.values[1];
              final gap = Generator.gap(a[0] * b[1], b[0] * a[1]);
              expect(gap, greaterThan(0));
              expect(gap, lessThan(.14));
              bins[gap < .01
                  ? 0
                  : gap < .05
                  ? 1
                  : gap < .10
                  ? 2
                  : 3]++;
              expect(p.relation, a[0] * b[1] > b[0] * a[1] ? '>' : '<');
            } else {
              final sorted = p.ordered.map((n) => p.values[n]).toList();
              for (final pair in sorted) {
                expect(pair[0] / pair[1], inInclusiveRange(.35, 2));
                for (final n in pair) {
                  expect(n, inInclusiveRange(10, i < 3 ? 349 : 999));
                }
              }
              expect(
                Generator.gap(
                  sorted.first[0] * sorted.last[1],
                  sorted.last[0] * sorted.first[1],
                ),
                inInclusiveRange(.17, .28),
              );
              for (var j = 1; j < 4; j++) {
                final a = sorted[j - 1], b = sorted[j];
                expect(a[0] * b[1], greaterThan(b[0] * a[1]));
                expect(
                  Generator.gap(a[0] * b[1], b[0] * a[1]),
                  inInclusiveRange(.035, .14),
                );
              }
            }
            final parts = p.values.map((r) => r.join('/')).toList()..sort();
            expect(
              signatures.add(
                p.type.name + parts.join('|') + p.hidden.join(','),
              ),
              isTrue,
            );
          }
          final session = PracticeSession(
            id: '$seed-${kind.name}',
            kind: kind,
            seed: seed,
            problems: problems,
            startedAt: DateTime(2026, 10, 26),
          );
          expect(
            session.total,
            kind == SetKind.addition
                ? 40
                : kind == SetKind.multiplication
                ? 18
                : 15,
          );
          session.answers.addAll(session.expected);
          expect(session.correct, session.total);
          expect(session.answered, session.total);
          final restored = PracticeSession.fromJson(
            jsonDecode(jsonEncode(session.toJson())),
          );
          expect(restored.correct, session.total);
          expect(
            jsonEncode(
              Generator(seed).generate(kind).map((p) => p.toJson()).toList(),
            ),
            jsonEncode(problems.map((p) => p.toJson()).toList()),
          );
        }
      }
      final total = bins.fold(0, (a, b) => a + b);
      for (var i = 0; i < 4; i++) {
        expect(bins[i] / total, closeTo([.12, .32, .30, .26][i], .025));
      }
    },
  );
  test('unanswered, negative numbers, partial order and elapsed time', () {
    final session = PracticeSession(
      id: 'one',
      kind: SetKind.addition,
      seed: 1,
      problems: Generator(1).generate(SetKind.addition),
      startedAt: DateTime(2026, 10, 26, 23, 59, 30),
    );
    expect(session.answered, 0);
    expect(session.correct, 0);
    session.answers[session.expected.keys.first] = '-';
    expect(session.answered, 0);
    session.answers.addAll(session.expected);
    final key = session.expected.keys.first;
    session.answers[key] = '00${session.expected[key]!}';
    // Leading zeros count as a numeric answer, not a text mismatch.
    if (!session.expected[key]!.startsWith('-')) expect(session.correct, 40);
    expect(session.elapsedAt(DateTime(2026, 10, 27, 0, 1)), 90);
    expect(session.elapsedAt(DateTime(2026, 10, 25)), 0);
    final order = PracticeSession(
      id: 'two',
      kind: SetKind.division,
      seed: 2,
      problems: Generator(2).generate(SetKind.division),
      startedAt: DateTime(2026),
    );
    order.answers['0'] = '0,1,2';
    expect(order.answered, 0);
    expect(order.correct, 0);
  });
}
