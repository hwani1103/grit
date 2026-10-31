import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/guide.dart';
import 'package:grit/guide_content.dart';
import 'package:grit/main.dart';
import 'package:grit/store.dart';
import 'store_test.dart' show MemoryPersistence;

void main() {
  testWidgets(
    'vitamin opens offline guide, search finds method, reader changes lesson',
    (tester) async {
      final c = AppController(MemoryPersistence());
      await tester.pumpWidget(GritApp(controller: c));
      await tester.pumpAndSettle();
      await tester.tap(find.text('풀이 안내서'));
      await tester.pumpAndSettle();
      await tester.enterText(find.byKey(const ValueKey('guide-search')), '용병법');
      await tester.pumpAndSettle();
      final method = find.text('F · 용병법: 추가된 덩어리가 비율을 끌어간다');
      await tester.scrollUntilVisible(
        method,
        300,
        scrollable: find
            .descendant(
              of: find.byType(ListView).first,
              matching: find.byType(Scrollable),
            )
            .first,
      );
      await tester.tap(method);
      await tester.pumpAndSettle();
      expect(find.text('1. 언제 쓰나요?'), findsOneWidget);
      await tester.scrollUntilVisible(
        find.text('6. 막히면 다음 방법'),
        350,
        scrollable: find
            .descendant(
              of: find.byType(ListView).first,
              matching: find.byType(Scrollable),
            )
            .first,
      );
      expect(find.text('6. 막히면 다음 방법'), findsOneWidget);
      await tester.scrollUntilVisible(
        find.text('다음 풀이'),
        250,
        scrollable: find
            .descendant(
              of: find.byType(ListView).first,
              matching: find.byType(Scrollable),
            )
            .first,
      );
      await tester.drag(find.byType(ListView).first, const Offset(0, -180));
      await tester.pumpAndSettle();
      await tester.tap(find.text('다음 풀이'));
      await tester.pumpAndSettle();
      expect(find.text('G · 역수: 뒤집으면 크기도 뒤집힌다'), findsOneWidget);
      expect(tester.takeException(), isNull);
      await tester.pumpWidget(const SizedBox());
      c.dispose();
    },
  );
  testWidgets(
    'all lessons readable at narrow width with large text; quiz reveals explanation',
    (tester) async {
      tester.view.devicePixelRatio = 1;
      tester.view.physicalSize = const Size(320, 640);
      tester.platformDispatcher.textScaleFactorTestValue = 1.4;
      addTearDown(tester.view.resetDevicePixelRatio);
      addTearDown(tester.view.resetPhysicalSize);
      addTearDown(tester.platformDispatcher.clearTextScaleFactorTestValue);
      for (var c = 0; c < guideChapters.length; c++) {
        for (var t = 0; t < guideChapters[c].tips.length; t++) {
          await tester.pumpWidget(
            MaterialApp(
              home: GuideTipScreen(
                key: ValueKey('$c-$t'),
                chapterIndex: c,
                initialTip: t,
              ),
            ),
          );
          await tester.pumpAndSettle();
          expect(find.text(guideChapters[c].tips[t].title), findsOneWidget);
          await tester.scrollUntilVisible(
            find.text('6. 막히면 다음 방법'),
            400,
            maxScrolls: 100,
            scrollable: find
                .descendant(
                  of: find.byType(ListView).first,
                  matching: find.byType(Scrollable),
                )
                .first,
          );
          await tester.scrollUntilVisible(
            find.text('참고 자료와 작성 기준'),
            300,
            maxScrolls: 30,
            scrollable: find
                .descendant(
                  of: find.byType(ListView).first,
                  matching: find.byType(Scrollable),
                )
                .first,
          );
          expect(tester.takeException(), isNull, reason: '$c-$t');
        }
      }
      await tester.pumpWidget(
        const MaterialApp(home: GuideChapterScreen(chapterIndex: 1)),
      );
      await tester.pumpAndSettle();
      final quiz = guideChapters[1].quizzes[0];
      await tester.scrollUntilVisible(
        find.text('Q1. ${quiz.question}'),
        400,
        maxScrolls: 60,
        scrollable: find
            .descendant(
              of: find.byType(ListView).first,
              matching: find.byType(Scrollable),
            )
            .first,
      );
      expect(find.text(quiz.answer), findsNothing);
      await tester.tap(find.text('Q1. ${quiz.question}'));
      await tester.pumpAndSettle();
      expect(find.text(quiz.answer), findsOneWidget);
      expect(tester.takeException(), isNull);
      await tester.pumpWidget(const SizedBox());
    },
  );
  test(
    'guide identities and close comparison examples verified independently',
    () {
      // Difference-fraction, complement, reciprocal and relative-odds transformations.
      for (var a = 1; a < 50; a += 3) {
        for (var b = 1; b < 55; b += 4) {
          for (var h = 1; h < 12; h += 2) {
            for (var k = 1; k < 14; k += 3) {
              final before = a / b;
              final after = (a + h) / (b + k);
              expect(
                (after - before).abs() < 1e-12 ? 0 : (after - before).sign,
                (h * b - a * k).sign,
              );
              expect(
                (a * (b + k) - (a + h) * b).sign,
                ((b + k) / (a + h) - b / a).abs() < 1e-12
                    ? 0
                    : ((b + k) / (a + h) - b / a).sign,
              );
            }
          }
        }
      }
      expect(9832 * 338, 3323216);
      expect(9600 * 345, 3312000);
      expect(95 * 227 - 103 * 209, 38);
      expect(91 * 221 - 99 * 203, 14);
      expect(49 * 126 - 39 * 156, 90);
      expect(72 * 115 - 81 * 100, 180);
      expect(72 * 34 - 81 * 28, 180);
      expect(guideChapters.fold(0, (n, c) => n + c.tips.length), 31);
      expect(guideChapters.fold(0, (n, c) => n + c.quizzes.length), 13);
    },
  );
}
