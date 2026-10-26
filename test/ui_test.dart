import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/main.dart';
import 'package:grit/model.dart';
import 'package:grit/store.dart';
import 'package:grit/practice.dart'
    show ReviewCard, ComparisonExercise, PracticeScreen;
import 'store_test.dart' show MemoryPersistence;

PracticeSession sample(SetKind kind, {int page = 0}) => PracticeSession(
  id: 'sample-${kind.name}',
  kind: kind,
  seed: 73,
  problems: Generator(73).generate(kind),
  startedAt: DateTime.now().subtract(const Duration(seconds: 83)),
  page: page,
);

Future<void> enterActive(WidgetTester tester, AppController c) async {
  final context = tester.element(find.byType(HomeScreen));
  Navigator.of(context).push(
    MaterialPageRoute(
      builder: (_) => PracticeScreen(controller: c, session: c.active!),
    ),
  );
  await tester.pumpAndSettle();
}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  setUpAll(() async {
    final iconLoader = FontLoader('MaterialIcons')
      ..addFont(
        Future.value(
          ByteData.sublistView(
            File(
              'C:/tools/flutter/bin/cache/artifacts/material_fonts/MaterialIcons-Regular.otf',
            ).readAsBytesSync(),
          ),
        ),
      );
    await iconLoader.load();
    final font = File('C:/Windows/Fonts/malgun.ttf');
    if (font.existsSync()) {
      final loader = FontLoader('Roboto')
        ..addFont(Future.value(ByteData.sublistView(font.readAsBytesSync())));
      await loader.load();
      // Text without an explicit family uses Ahem in the host test binding.
      final fallback = FontLoader('Ahem')
        ..addFont(Future.value(ByteData.sublistView(font.readAsBytesSync())));
      await fallback.load();
    }
  });
  void size(WidgetTester tester, Size value) {
    tester.view.devicePixelRatio = 1;
    tester.view.physicalSize = value;
    addTearDown(tester.view.resetDevicePixelRatio);
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetViewInsets);
  }

  Future<void> close(WidgetTester tester, AppController c) async {
    await tester.pumpWidget(const SizedBox());
    c.dispose();
    await tester.pump();
  }

  for (final viewport in [
    const Size(320, 640),
    const Size(390, 844),
    const Size(844, 390),
    const Size(720, 840),
  ]) {
    testWidgets(
      'home fits without scrolling with or without active work at $viewport',
      (tester) async {
        size(tester, viewport);
        for (final active in [false, true]) {
          final c = AppController(MemoryPersistence());
          if (active) c.active = sample(SetKind.addition);
          await tester.pumpWidget(GritApp(controller: c));
          await tester.pumpAndSettle();
          expect(find.byType(Scrollable), findsNothing);
          expect(find.textContaining('매번 새로운 문제'), findsNothing);
          for (final kind in SetKind.values) {
            expect(find.text(kind.title).last.hitTestable(), findsOneWidget);
          }
          expect(find.text('이어서 풀기'), findsNothing);
          expect(tester.takeException(), isNull);
          await close(tester, c);
        }
      },
    );
  }
  testWidgets('phone home, creation, tap comparison, completion and review', (
    tester,
  ) async {
    size(tester, const Size(390, 844));
    final c = AppController(MemoryPersistence());
    final key = GlobalKey();
    await tester.pumpWidget(
      RepaintBoundary(
        key: key,
        child: GritApp(controller: c),
      ),
    );
    await tester.pumpAndSettle();
    // Home screenshot already rendered; separate from interaction assertions.

    await tester.ensureVisible(find.text('곱셈'));

    await tester.tap(find.text('곱셈'));

    await tester.pumpAndSettle();

    await tester.tap(find.text('시작'));

    await tester.pumpAndSettle();

    expect(c.active!.kind, SetKind.multiplication);

    final correct = c.active!.problems[0].relation;
    await tester.ensureVisible(find.text(correct == '>' ? '왼쪽이 큼' : '오른쪽이 큼'));
    await tester.tap(find.text(correct == '>' ? '왼쪽이 큼' : '오른쪽이 큼'));
    await tester.pump(const Duration(milliseconds: 500));
    expect(c.active!.correct, 1);
    expect(c.active!.page, 1);
    await tester.tap(find.text('완료'));
    await tester.pumpAndSettle();
    await tester.tap(find.text('제출하고 채점'));
    await tester.pumpAndSettle();
    expect(c.records.length, 1);
    expect(c.records.single.correct, 1);
    expect(c.active, isNull);

    expect(tester.takeException(), isNull);
    await close(tester, c);
  });
  for (final viewport in [
    const Size(320, 640),
    const Size(390, 844),
    const Size(844, 390),
    const Size(673, 841),
    const Size(720, 840),
    const Size(900, 700),
    const Size(1024, 800),
  ]) {
    testWidgets('whole table and keypad without scrolling at $viewport', (
      tester,
    ) async {
      size(tester, viewport);
      final c = AppController(MemoryPersistence())
        ..active = sample(SetKind.addition, page: 4);
      final key = GlobalKey();
      await tester.pumpWidget(
        RepaintBoundary(
          key: key,
          child: GritApp(controller: c),
        ),
      );
      await tester.pumpAndSettle();
      await tester.pumpAndSettle();
      await tester.pumpAndSettle();
      await enterActive(tester, c);
      await tester.pumpAndSettle();

      expect(tester.takeException(), isNull);
      expect(find.byType(TextField), findsNothing);
      expect(find.byType(Scrollable), findsNothing);
      final problem = c.active!.problems[4];
      expect(find.text('구분'), findsNothing);
      for (var r = 0; r < problem.values.length; r++) {
        expect(find.byKey(ValueKey('memo-r-$r')).hitTestable(), findsOneWidget);
      }
      for (var col = 0; col < problem.width; col++) {
        expect(
          find.byKey(ValueKey('memo-c-$col')).hitTestable(),
          findsOneWidget,
        );
      }
      for (final cell in problem.hidden) {
        expect(
          find.byKey(ValueKey('answer-$cell')).hitTestable(),
          findsOneWidget,
        );
      }
      Future<void> press(String key) async {
        await tester.tap(find.byKey(ValueKey('pad-$key')));
        await tester.pump();
      }

      await tester.tap(find.byKey(ValueKey('answer-${problem.hidden.first}')));
      await press('sign');
      await press('1');
      await press('2');
      final answerKey = problem.answerKey(4, problem.hidden.first);
      expect(c.active!.answers[answerKey], '-12');
      await press('back');
      expect(c.active!.answers[answerKey], '-1');
      expect(find.textContaining(RegExp(r'\d+행 ·')), findsOneWidget);
      await tester.tap(find.byKey(const ValueKey('memo-r-0')));
      await press('4');
      await press('5');
      await press('6');
      expect(c.active!.memos['4:r:0'], '456');
      expect(c.active!.answered, 1);
      expect(c.active!.answers[answerKey], '-1');
      expect(find.text('가로 1 · 계산 메모'), findsOneWidget);
      await tester.tap(find.byKey(const ValueKey('memo-c-0')));
      await press('sign');
      await press('3');
      expect(c.active!.memos['4:c:0'], '-3');
      await press('clear');
      expect(c.active!.memos.containsKey('4:c:0'), isFalse);
      await tester.tap(find.byKey(ValueKey('answer-${problem.hidden.first}')));
      await press('sign');
      await press('sign');
      await press('2');
      await tester.tap(find.text('이전 표'));
      await tester.pumpAndSettle();
      expect(c.active!.page, 3);
      expect(c.active!.memos['4:r:0'], '456');
      await tester.tap(find.text('다음 표'));
      await tester.pumpAndSettle();
      expect(c.active!.answers[answerKey], '-12');
      expect(find.byType(Scrollable), findsNothing);
      if (const bool.fromEnvironment('GRIT_CAPTURE') &&
          (viewport.width == 390 || viewport.width == 720)) {
        await expectLater(
          find.byKey(key),
          matchesGoldenFile(
            '../test_output/memo-${viewport.width.toInt()}.png',
          ),
        );
      }
      expect(tester.takeException(), isNull);
      await close(tester, c);
    });
  }
  testWidgets(
    'history reset confirms, updates both tabs and preserves active work; no backup UI',
    (tester) async {
      size(tester, const Size(390, 844));
      final finished = sample(SetKind.multiplication)
        ..completedAt = DateTime.now()
        ..elapsedSeconds = 90;
      final c = AppController(MemoryPersistence())
        ..records = [finished]
        ..active = sample(SetKind.addition);
      final active = c.active!;
      active.memos['0:r:0'] = '456';
      await tester.pumpWidget(GritApp(controller: c));
      await tester.pumpAndSettle();
      Future<void> openReset() async {
        await tester.tap(find.byTooltip('설정 및 기록 관리'));
        await tester.pumpAndSettle();
        expect(find.textContaining('백업'), findsNothing);
        await tester.tap(find.text('기록 초기화'));
        await tester.pumpAndSettle();
      }

      await openReset();
      await tester.tap(find.text('취소'));
      await tester.pumpAndSettle();
      expect(c.records.length, 1);
      await tester.tap(find.text('나의 기록'));
      await tester.pumpAndSettle();
      await openReset();
      await tester.tap(find.byKey(const ValueKey('confirm-reset-history')));
      await tester.pumpAndSettle();
      expect(c.records, isEmpty);
      expect(find.text('첫 번째 기록을 기다리고 있어요.'), findsOneWidget);
      await tester.tap(find.text('연습'));
      await tester.pumpAndSettle();
      expect(find.text('0'), findsNWidgets(3));
      expect(c.active, same(active));
      expect(c.active!.memos['0:r:0'], '456');
      expect(tester.takeException(), isNull);
      await close(tester, c);
    },
  );
  testWidgets(
    'comparison operands stay left and right at phone and unfolded widths',
    (tester) async {
      size(tester, const Size(320, 640));
      for (final viewport in [
        const Size(320, 640),
        const Size(390, 844),
        const Size(720, 840),
      ]) {
        tester.view.physicalSize = viewport;
        for (final problem in [
          Generator(12).product(),
          Generator(13).fraction(),
        ]) {
          await tester.pumpWidget(
            MaterialApp(
              home: Scaffold(
                body: Padding(
                  padding: const EdgeInsets.all(16),
                  child: ComparisonExercise(
                    problem: problem,
                    onChanged: (_) {},
                  ),
                ),
              ),
            ),
          );
          await tester.pumpAndSettle();
          final left = tester.getCenter(
            find.byKey(const ValueKey('comparison-operand-0')),
          );
          final right = tester.getCenter(
            find.byKey(const ValueKey('comparison-operand-1')),
          );
          expect(left.dx, lessThan(right.dx));
          expect(left.dy, closeTo(right.dy, .1));
          expect(tester.takeException(), isNull);
        }
      }
      await tester.pumpWidget(const SizedBox());
    },
  );
  testWidgets('review displays saved memo distinctly from answer and grade', (
    tester,
  ) async {
    size(tester, const Size(720, 840));
    final session = sample(SetKind.addition);
    session.memos['0:r:0'] = '456789';
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: ReviewCard(
            problem: session.problems[0],
            index: 0,
            session: session,
          ),
        ),
      ),
    );
    await tester.pumpAndSettle();
    final memoText = tester.widget<Text>(find.text('456789'));
    expect(memoText.style!.color, const Color(0xFF365D81));
    expect(find.text('0/7'), findsOneWidget);
    expect(find.text('구분'), findsNothing);
    expect(tester.takeException(), isNull);
    await tester.pumpWidget(const SizedBox());
  });
  testWidgets('folding preserves selected cell, answers, page and start time', (
    tester,
  ) async {
    size(tester, const Size(390, 844));
    final c = AppController(MemoryPersistence())
      ..active = sample(SetKind.addition, page: 4);
    await tester.pumpWidget(GritApp(controller: c));
    await tester.pumpAndSettle();
    await enterActive(tester, c);
    await tester.pumpAndSettle();
    final session = c.active!;
    final startedAt = session.startedAt;
    final problem = session.problems[4];
    final selected = problem.hidden.last;
    final answerKey = problem.answerKey(4, selected);
    await tester.tap(find.byKey(ValueKey('answer-$selected')));
    await tester.tap(find.byKey(const ValueKey('pad-1')));
    await tester.pump();
    expect(find.byKey(const ValueKey('addition-stacked')), findsOneWidget);
    for (final viewport in [
      const Size(720, 840),
      const Size(900, 700),
      const Size(390, 844),
    ]) {
      tester.view.physicalSize = viewport;
      await tester.pumpAndSettle();
      final wide = viewport.width > 600;
      expect(
        find.byKey(ValueKey(wide ? 'addition-wide' : 'addition-stacked')),
        findsOneWidget,
      );
      expect(find.byType(Scrollable), findsNothing);
      for (final cell in problem.hidden) {
        expect(
          find.byKey(ValueKey('answer-$cell')).hitTestable(),
          findsOneWidget,
        );
      }
      await tester.tap(find.byKey(const ValueKey('pad-2')));
      await tester.pump();
      expect(c.active, same(session));
      expect(session.page, 4);
      expect(session.startedAt, startedAt);
      expect(tester.takeException(), isNull);
    }
    expect(session.answers[answerKey], '1222');
    expect(session.answers.length, 1);
    await tester.tap(find.byKey(const ValueKey('memo-r-2')));
    await tester.tap(find.byKey(const ValueKey('pad-4')));
    await tester.pump();
    tester.view.physicalSize = const Size(720, 840);
    await tester.pumpAndSettle();
    await tester.tap(find.byKey(const ValueKey('pad-5')));
    await tester.pump();
    expect(session.memos['4:r:2'], '45');
    expect(session.answers[answerKey], '1222');
    expect(tester.takeException(), isNull);
    await close(tester, c);
  });
  testWidgets(
    'fraction order can be corrected and auto advances only with four choices',
    (tester) async {
      size(tester, const Size(390, 844));
      final c = AppController(MemoryPersistence())
        ..active = sample(SetKind.division);
      final key = GlobalKey();
      await tester.pumpWidget(
        RepaintBoundary(
          key: key,
          child: GritApp(controller: c),
        ),
      );
      await tester.pumpAndSettle();
      await tester.pumpAndSettle();
      await tester.pumpAndSettle();
      await enterActive(tester, c);
      await tester.pumpAndSettle();

      final order = c.active!.problems[0].ordered;
      for (var i = 0; i < 4; i++) {
        final slot = find.byKey(ValueKey('order-slot-$i'));
        expect(
          find.descendant(of: slot, matching: find.text('·')),
          findsOneWidget,
        );
      }
      for (final i in order.take(3)) {
        await tester.tap(find.text(String.fromCharCode(65 + i)).first);
        await tester.pump();
      }
      expect(c.active!.answered, 0);
      for (var i = 0; i < 3; i++) {
        final slot = find.byKey(ValueKey('order-slot-$i'));
        expect(
          find.descendant(
            of: slot,
            matching: find.text(String.fromCharCode(65 + order[i])),
          ),
          findsOneWidget,
        );
      }
      await tester.tap(find.text(String.fromCharCode(65 + order[1])).first);
      await tester.pump();
      expect(c.active!.answers['0']!.split(',').length, 2);
      await tester.ensureVisible(find.text('순서 다시 선택'));
      await tester.tap(find.text('순서 다시 선택'));
      await tester.pump();
      for (final i in order) {
        await tester.ensureVisible(
          find.text(String.fromCharCode(65 + i)).first,
        );
        await tester.tap(find.text(String.fromCharCode(65 + i)).first);
        await tester.pump();
      }
      expect(c.active!.correct, 1);
      await tester.pump(const Duration(milliseconds: 500));
      expect(c.active!.page, 1);
      expect(tester.takeException(), isNull);
      await close(tester, c);
    },
  );
  testWidgets('history and narrow screen fraction layout', (tester) async {
    size(tester, const Size(320, 640));
    final c = AppController(MemoryPersistence())
      ..active = sample(SetKind.division, page: 5);
    final key = GlobalKey();
    await tester.pumpWidget(
      RepaintBoundary(
        key: key,
        child: GritApp(controller: c),
      ),
    );
    await tester.pumpAndSettle();
    await tester.pumpAndSettle();
    await tester.pumpAndSettle();
    await enterActive(tester, c);
    await tester.pumpAndSettle();

    expect(tester.takeException(), isNull);
    await close(tester, c);
  });
  testWidgets('large system text does not overflow home or comparison', (
    tester,
  ) async {
    size(tester, const Size(360, 800));
    tester.platformDispatcher.textScaleFactorTestValue = 1.4;
    addTearDown(tester.platformDispatcher.clearTextScaleFactorTestValue);
    final c = AppController(MemoryPersistence());
    await tester.pumpWidget(GritApp(controller: c));
    await tester.pumpAndSettle();
    expect(tester.takeException(), isNull);

    await tester.ensureVisible(find.text('곱셈'));

    await tester.tap(find.text('곱셈'));

    await tester.pumpAndSettle();
    await tester.ensureVisible(find.text('시작'));

    await tester.tap(find.text('시작'));

    await tester.pumpAndSettle();
    expect(tester.takeException(), isNull);
    await close(tester, c);
  });
  testWidgets(
    'back confirms discard, cancellation and background keep time running',
    (tester) async {
      size(tester, const Size(390, 844));
      final disk = MemoryPersistence();
      final c = AppController(disk)..active = sample(SetKind.addition);
      final session = c.active!;
      session.memos['0:r:0'] = '456';
      await tester.pumpWidget(GritApp(controller: c));
      await enterActive(tester, c);
      await tester.tap(find.byTooltip('연습 나가기'));
      await tester.pumpAndSettle();
      expect(find.text('이번 연습을 그만둘까요?'), findsOneWidget);
      // Repeated back requests never stack duplicate exit dialogs.
      await tester.pump(const Duration(seconds: 3));
      await tester.tap(find.text('계속 풀기'));
      await tester.pumpAndSettle();
      expect(c.active, same(session));
      expect(session.memos['0:r:0'], '456');
      tester.binding.handleAppLifecycleStateChanged(AppLifecycleState.paused);
      await tester.pump();
      tester.binding.handleAppLifecycleStateChanged(AppLifecycleState.resumed);
      await tester.pump();
      expect(c.active, same(session));
      expect(
        session.elapsedAt(session.startedAt.add(const Duration(minutes: 7))),
        420,
      );
      await tester.binding.handlePopRoute();
      await tester.pumpAndSettle();
      expect(find.text('이번 연습을 그만둘까요?'), findsOneWidget);
      await tester.tap(find.byKey(const ValueKey('confirm-discard')));
      await tester.pumpAndSettle();
      expect(find.byType(PracticeScreen), findsNothing);
      expect(find.text('이어서 풀기'), findsNothing);
      expect(c.active, isNull);
      expect(c.records, isEmpty);
      final reopened = AppController(disk);
      await reopened.load();
      expect(reopened.active, isNull);
      reopened.dispose();
      expect(tester.takeException(), isNull);
      await close(tester, c);
    },
  );
}
