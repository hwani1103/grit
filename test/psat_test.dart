import 'dart:convert';
import 'dart:io';
import 'dart:ui' as ui;
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/main.dart';
import 'package:grit/model.dart';
import 'package:grit/store.dart';
import 'package:grit/psat.dart';
import 'package:grit/psat_model.dart';
import 'package:grit/psat_sets.dart';
import 'package:grit/psat_text.dart';
import 'store_test.dart' show MemoryPersistence;

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  late List<PsatQuestion> bank;
  setUpAll(() async {
    bank = (await loadPsatCatalog()).questions.values.toList();
    final icons = FontLoader('MaterialIcons')
      ..addFont(
        Future.value(
          ByteData.sublistView(
            File(
              'C:/tools/flutter/bin/cache/artifacts/material_fonts/MaterialIcons-Regular.otf',
            ).readAsBytesSync(),
          ),
        ),
      );
    await icons.load();
    for (final name in ['Roboto', 'Ahem']) {
      final loader = FontLoader(name)
        ..addFont(
          Future.value(
            ByteData.sublistView(
              File('C:/Windows/Fonts/malgun.ttf').readAsBytesSync(),
            ),
          ),
        );
      await loader.load();
    }
  });
  test('question prompts exclude preceding tables and numbered choices', () {
    for (final q in bank) {
      expect(RegExp(r'^\s*\d').hasMatch(q.prompt), isFalse, reason: q.id);
      expect(q.prompt.contains('①'), isFalse, reason: q.id);
    }
    for (final id in [
      'kr-mpm-2026-07-18-psat-d-08',
      'kr-mpm-2026-03-07-psat-d-03',
      'kr-mpm-2025-03-08-psat-d-02',
    ]) {
      final q = bank.firstWhere((q) => q.id == id);
      expect(q.prompt.startsWith('다음'), isTrue, reason: id);
      expect(q.prompt.length, lessThan(180), reason: id);
    }
  });
  test('reading blocks preserve conditions and quoted sentences', () {
    final q = bank.firstWhere((q) => q.id.endsWith('l-14'));
    final blocks = psatReadingBlocks(q.body);
    expect(blocks.length, 8);
    expect(
      blocks.join(' ').replaceAll(RegExp(r'\s+'), ' '),
      q.body.replaceAll(RegExp(r'\s+'), ' '),
    );
    const quoted = '<가> <나> <다>의 설명은 “참이다. 거짓이다.”이다. 다음 조건이다.';
    expect(psatReadingBlocks(quoted), [
      '<가> <나> <다>의 설명은 “참이다. 거짓이다.”이다.',
      '다음 조건이다.',
    ]);
    expect(psatReadingBlocks('A < B, C > D. 1.5 < 2.0'), [
      'A < B, C > D. 1.5 < 2.0',
    ]);
  });
  testWidgets(
    'Korean word moves intact; oversized token wraps; comparison signs remain',
    (t) async {
      for (final scale in [1.0, 1.4]) {
        await t.pumpWidget(
          MaterialApp(
            home: Center(
              child: SizedBox(
                width: 110,
                child: MediaQuery(
                  data: MediaQueryData(textScaler: TextScaler.linear(scale)),
                  child: const PsatText(
                    '조건은 반복되는 조건이다.',
                    key: ValueKey('words'),
                    style: TextStyle(fontFamily: 'Roboto', fontSize: 19),
                  ),
                ),
              ),
            ),
          ),
        );
        await t.pump();
        final finder = find.descendant(
          of: find.byKey(const ValueKey('words')),
          matching: find.byType(RichText),
        );
        final paragraph = t.renderObject<RenderParagraph>(finder);
        final text = paragraph.text.toPlainText();
        final start = text.indexOf('반');
        final end = text.indexOf(' ', start);
        final boxes = paragraph.getBoxesForSelection(
          TextSelection(baseOffset: start, extentOffset: end),
        );
        expect(boxes.length, 1);
        expect(boxes.single.top, greaterThan(0));
        expect(boxes.single.right, lessThanOrEqualTo(110.5));
        expect(text.replaceAll('\u2060', ''), '조건은 반복되는 조건이다.');
      }
      await t.pumpWidget(
        const MaterialApp(
          home: Center(
            child: SizedBox(
              width: 80,
              child: PsatText(
                '아주길어서화면너비를넘어가는하나의어절 A < B',
                key: ValueKey('long'),
                style: TextStyle(fontFamily: 'Roboto', fontSize: 19),
              ),
            ),
          ),
        ),
      );
      await t.pump();
      final paragraph = t.renderObject<RenderParagraph>(
        find.descendant(
          of: find.byKey(const ValueKey('long')),
          matching: find.byType(RichText),
        ),
      );
      final text = paragraph.text.toPlainText();
      expect(text, contains('A < B'));
      expect(text, isNot(contains('\u2060')));
      final boxes = paragraph.getBoxesForSelection(
        TextSelection(baseOffset: 0, extentOffset: text.length),
      );
      expect(boxes.length, greaterThan(1));
      // A selected trailing space may extend past the line; visible glyphs must not.
      for (var i = 0; i < text.length; i++) {
        if (text[i].trim().isEmpty) continue;
        final glyph = paragraph.getBoxesForSelection(
          TextSelection(baseOffset: i, extentOffset: i + 1),
        );
        expect(
          glyph.every((box) => box.right <= 80.5),
          isTrue,
          reason: '${text[i]}: $glyph',
        );
      }
      expect(t.takeException(), isNull);
    },
  );
  test(
    'law hierarchy preserves all text and separates titles, clauses and items',
    () {
      String clean(String s) => s.replaceAll(RegExp(r'\s+'), '');
      for (final n in [2, 4, 11, 12]) {
        final q = bank.firstWhere((q) => q.subject == '상황판단' && q.number == n);
        final blocks = psatReadingBlocks(q.body);
        expect(clean(blocks.join()), clean(q.body), reason: q.id);
        expect(blocks.any((b) => b.startsWith('① ')), isTrue);
        expect(blocks.any((b) => b.startsWith('② ')), isTrue);
        for (final b in blocks.where(
          (b) => b.startsWith('제') && b.contains('('),
        )) {
          if (b.contains('①')) fail('Article title contains clause: $b');
        }
      }
      final q2 = bank.firstWhere((q) => q.id.endsWith('s-02'));
      final b2 = psatReadingBlocks(q2.body);
      expect(b2.where((b) => b.startsWith('제00조')).length, 3);
      expect(b2.where((b) => b.startsWith('① ')).length, 2);
      expect(b2.where((b) => b.startsWith('1. ')).length, 1);
      expect(b2.where((b) => b.startsWith('2. ')).length, 1);
      final q12 = bank.firstWhere((q) => q.id.endsWith('s-12'));
      expect(
        psatReadingBlocks(q12.body).where((b) => b.startsWith('가. ')).length,
        2,
      );
      const sample = '제10조(제목) ① “② 인용한 번호”는 그대로 둔다. ② 제10조 제1항을 참조한다.';
      expect(psatReadingBlocks(sample), [
        '제10조(제목)',
        '① “② 인용한 번호”는 그대로 둔다.',
        '② 제10조 제1항을 참조한다.',
      ]);
      const definitions =
          '제1조(정의) 용어의 뜻은 다음과 같다. '
          '1. “항목”이란 “2. 인용 번호”를 포함한다. '
          '2. “기간”이란 2024. 1. 1.부터의 기간이다. '
          '제2조(절차) ① 신청한다.';
      expect(psatReadingBlocks(definitions), [
        '제1조(정의)',
        '용어의 뜻은 다음과 같다.',
        '1. “항목”이란 “2. 인용 번호”를 포함한다.',
        '2. “기간”이란 2024. 1. 1.부터의 기간이다.',
        '제2조(절차)',
        '① 신청한다.',
      ]);
      expect(
        psatReadingBlocks(definitions.replaceFirst('뜻은', '정의는')),
        psatReadingBlocks(
          definitions,
        ).map((block) => block.replaceFirst('뜻은', '정의는')).toList(),
      );
      final astronomy = bank.firstWhere(
        (q) => q.id == 'kr-mpm-2023-07-22-psat-s-01',
      );
      final astronomyBlocks = psatReadingBlocks(astronomy.body);
      for (var number = 1; number <= 6; number++) {
        expect(
          astronomyBlocks.where((block) => block.startsWith('$number. ')),
          hasLength(1),
        );
      }
      expect(psatReadingBlocks('<회의>\n\n(가) 내용\n\n(나) 내용'), [
        '<회의>',
        '(가) 내용',
        '(나) 내용',
      ]);
    },
  );
  PsatAttempt attempt(PsatQuestion q, {int? selected}) {
    final start = DateTime(2026, 10, 28, 10);
    return PsatAttempt(
      id: 'review-${q.id}',
      question: q,
      selected: selected ?? q.answer,
      startedAt: start,
      completedAt: start.add(const Duration(seconds: 93)),
      seconds: 93,
    );
  }

  test('official final answers, both subjects and original assets', () {
    final officialL = {
      3: 2,
      4: 3,
      8: 2,
      9: 4,
      10: 4,
      11: 1,
      12: 4,
      14: 3,
      15: 5,
      16: 5,
    };
    final officialS = {
      2: 1,
      4: 3,
      6: 1,
      8: 4,
      11: 4,
      12: 5,
      13: 2,
      14: 4,
      15: 1,
      16: 1,
    };
    final originalBank = bank
        .where((q) => q.id.startsWith('2023-07-22-'))
        .toList();
    expect(originalBank.where((q) => q.subject == '언어논리').length, 10);
    expect(originalBank.where((q) => q.subject == '상황판단').length, 10);
    expect(originalBank.where((q) => q.subject == '자료해석').length, 10);
    const officialD = {
      2: 3,
      3: 2,
      4: 3,
      6: 4,
      9: 2,
      11: 3,
      12: 4,
      14: 3,
      17: 4,
      19: 2,
    };
    expect(originalBank.map((q) => q.id).toSet().length, 30);
    for (final q in originalBank) {
      expect(
        q.answer,
        (q.subject == '언어논리'
            ? officialL
            : q.subject == '상황판단'
            ? officialS
            : officialD)[q.number],
      );
      expect(File(q.original).lengthSync(), greaterThan(1000));
      expect(q.reasons.length, 5);
      for (final figure in q.figures) {
        expect(File(figure['asset'] as String).lengthSync(), greaterThan(1000));
      }
      expect(q.steps.length, greaterThanOrEqualTo(3));
      for (final table in q.tables) {
        for (final row in table['rows'] as List) {
          expect((row as List).length, (table['columns'] as List).length);
        }
      }
    }
  });
  test(
    'legacy arithmetic records and PSAT snapshot survive reload and reset failure',
    () async {
      final disk = MemoryPersistence();
      final c = AppController(disk);
      await c.start(SetKind.addition);
      c.memo('0:r:0', '123');
      await c.complete(DateTime.now());
      final legacy = c.records.single.toJson();
      final raw = jsonDecode(disk.value!) as Map;
      raw.remove('psatRecords');
      disk.value = jsonEncode(raw);
      final migrated = AppController(disk);
      await migrated.load();
      expect(migrated.psatRecords, isEmpty);
      await migrated.savePsat(attempt(bank.first, selected: 1));
      expect(migrated.records.single.toJson(), legacy);
      final reopened = AppController(disk);
      await reopened.load();
      expect(reopened.records.single.toJson(), legacy);
      expect(
        reopened.psatRecords.single.question.toJson(),
        bank.first.toJson(),
      );
      expect(reopened.psatRecords.single.correct, isFalse);
      disk.fail = true;
      await expectLater(reopened.savePsat(attempt(bank[1])), throwsStateError);
      expect(reopened.psatRecords.length, 1);
      await expectLater(reopened.resetHistory(), throwsStateError);
      expect(reopened.records.length, 1);
      expect(reopened.psatRecords.length, 1);
      disk.fail = false;
      await reopened.resetHistory();
      final cleared = AppController(disk);
      await cleared.load();
      expect(cleared.records, isEmpty);
      expect(cleared.psatRecords, isEmpty);
      c.dispose();
      migrated.dispose();
      reopened.dispose();
      cleared.dispose();
    },
  );
  test('corrupt PSAT record blocks writes and preserves raw storage', () async {
    final disk = MemoryPersistence()
      ..value = jsonEncode({
        'app': 'GRIT',
        'format': 1,
        'records': [],
        'psatRecords': [
          {'id': 'broken'},
        ],
      });
    final raw = disk.value;
    final c = AppController(disk);
    await c.load();
    expect(c.loadFailed, isTrue);
    await c.flush();
    expect(disk.value, raw);
    await expectLater(c.savePsat(attempt(bank.first)), throwsStateError);
    expect(disk.value, raw);
    c.dispose();
  });
  Finder scroller() => find.byType(Scrollable).last;
  Future<void> reveal(WidgetTester t, Finder target) async {
    await t.scrollUntilVisible(
      target,
      450,
      scrollable: scroller(),
      maxScrolls: 150,
    );
    await t.pump();
  }

  for (final spec in [
    (const Size(320, 640), 1.4),
    (const Size(390, 844), 1.0),
    (const Size(752, 834), 1.0),
    (const Size(840, 360), 1.0),
  ]) {
    testWidgets(
      'all published complete explanations remain reachable at $spec',
      (t) async {
        t.view.devicePixelRatio = 1;
        t.view.physicalSize = spec.$1;
        addTearDown(t.view.resetDevicePixelRatio);
        addTearDown(t.view.resetPhysicalSize);
        final c = AppController(MemoryPersistence());
        var reviewed = 0;
        final reviewing = _recoveryRange(bank);
        for (final q in reviewing) {
          await t.pumpWidget(
            MaterialApp(
              theme: ThemeData(fontFamily: 'Roboto'),
              builder: (context, child) => MediaQuery(
                data: MediaQuery.of(
                  context,
                ).copyWith(textScaler: TextScaler.linear(spec.$2)),
                child: child!,
              ),
              home: PsatReader(
                key: ValueKey(q.id),
                controller: c,
                question: q,
                review: attempt(q),
              ),
            ),
          );
          await t.pump();
          await reveal(t, find.text('목록으로'));
          expect(find.text('목록으로').hitTestable(), findsOneWidget, reason: q.id);
          expect(t.takeException(), isNull, reason: q.id);
          reviewed++;
          if (reviewed % 100 == 0) {
            debugPrint('Full review $spec: $reviewed/${bank.length}');
          }
        }
        expect(reviewed, reviewing.length);
        _recordRecovery('explanations-${spec.$1.width.toInt()}', reviewing);
        await t.pumpWidget(const SizedBox());
        c.dispose();
      },
    );
  }
  testWidgets(
    'answer and elapsed time survive fold; no feedback before submit; save failure retries once',
    (t) async {
      t.view.devicePixelRatio = 1;
      t.view.physicalSize = const Size(360, 840);
      addTearDown(t.view.resetDevicePixelRatio);
      addTearDown(t.view.resetPhysicalSize);
      final disk = MemoryPersistence();
      final c = AppController(disk);
      final q = bank.last;
      await t.pumpWidget(
        MaterialApp(
          home: PsatReader(controller: c, question: q),
        ),
      );
      await t.pump();
      final option = find.byKey(ValueKey('psat-option-${q.answer}'));
      await reveal(t, option);
      await t.tap(option);
      await t.pump(const Duration(seconds: 3));
      expect(c.psatRecords, isEmpty);
      expect(find.text('풀이의 흐름'), findsNothing);
      t.view.physicalSize = const Size(752, 834);
      await t.pump();
      await reveal(t, find.byKey(const ValueKey('psat-submit')));
      expect(
        t
            .widget<FilledButton>(find.byKey(const ValueKey('psat-submit')))
            .onPressed,
        isNotNull,
      );
      disk.fail = true;
      await t.tap(find.byKey(const ValueKey('psat-submit')));
      await t.pumpAndSettle();
      expect(c.psatRecords, isEmpty);
      expect(find.text('풀이의 흐름'), findsNothing);
      disk.fail = false;
      await t.tap(find.byKey(const ValueKey('psat-submit')));
      await t.pumpAndSettle();
      expect(c.psatRecords.length, 1);
      expect(c.psatRecords.single.correct, isTrue);
      t.view.physicalSize = const Size(360, 840);
      await t.pump();
      await reveal(t, find.text('목록으로'));
      expect(c.psatRecords.length, 1);
      expect(t.takeException(), isNull);
      await t.pumpWidget(const SizedBox());
      c.dispose();
    },
  );
  testWidgets(
    'home navigation, PSAT-only history reset affordance and Set loading',
    (t) async {
      final c = AppController(MemoryPersistence());
      await c.savePsat(attempt(bank.first));
      late PsatCatalog navigationCatalog;
      await t.runAsync(() async {
        navigationCatalog = await loadPsatCatalog();
      });
      await t.pumpWidget(GritApp(controller: c));
      await t.pumpAndSettle(
        const Duration(milliseconds: 100),
        EnginePhase.sendSemanticsUpdate,
        const Duration(seconds: 10),
      );
      for (final subject in ['언어논리', '상황판단', '자료해석']) {
        await t.tap(find.text(subject));
        await t.pump();
        // Asset decoding can use a real isolate, outside the widget fake clock.
        for (
          var wait = 0;
          wait < 40 &&
              find.byType(CircularProgressIndicator).evaluate().isNotEmpty;
          wait++
        ) {
          await t.runAsync(
            () => Future<void>.delayed(const Duration(milliseconds: 50)),
          );
          await t.pump();
        }
        await t.pumpAndSettle(
          const Duration(milliseconds: 100),
          EnginePhase.sendSemanticsUpdate,
          const Duration(seconds: 10),
        );
        final title = 'Set 1 (0 / 10)';
        expect(find.text(title), findsOneWidget);
        await t.tap(find.text(title));
        await t.pumpAndSettle(
          const Duration(milliseconds: 100),
          EnginePhase.sendSemanticsUpdate,
          const Duration(seconds: 10),
        );
        expect(
          find.text(
            navigationCatalog
                .questions[navigationCatalog
                    .forSubject(subject)
                    .first
                    .questionIds
                    .first]!
                .title,
          ),
          findsOneWidget,
        );
        expect(find.text('$subject · Set 1'), findsOneWidget);
        await t.pageBack();
        await t.pumpAndSettle(
          const Duration(milliseconds: 100),
          EnginePhase.sendSemanticsUpdate,
          const Duration(seconds: 10),
        );
      }
      expect(find.byType(ChoiceChip), findsNothing);
      expect(find.text('비타민'), findsOneWidget);
      await t.tap(find.byTooltip('설정 및 기록 관리'));
      await t.pumpAndSettle(
        const Duration(milliseconds: 100),
        EnginePhase.sendSemanticsUpdate,
        const Duration(seconds: 10),
      );
      final tile = find.ancestor(
        of: find.text('기록 초기화'),
        matching: find.byType(ListTile),
      );
      expect(t.widget<ListTile>(tile).enabled, isTrue);
      await t.pumpWidget(const SizedBox());
      c.dispose();
    },
  );
  testWidgets('phone and unfolding screenshots with hinge and original viewer', (
    t,
  ) async {
    final c = AppController(MemoryPersistence());
    t.view.devicePixelRatio = 1;
    addTearDown(t.view.resetDevicePixelRatio);
    addTearDown(t.view.resetPhysicalSize);
    for (final size in [const Size(360, 840), const Size(752, 834)]) {
      t.view.physicalSize = size;
      final boundary = GlobalKey();
      final q = bank.firstWhere((q) => q.id.endsWith('l-14'));
      await t.pumpWidget(
        MaterialApp(
          theme: ThemeData(fontFamily: 'Roboto'),
          home: MediaQuery(
            data: MediaQueryData(
              size: size,
              displayFeatures: size.width > 700
                  ? [
                      const ui.DisplayFeature(
                        bounds: Rect.fromLTWH(370, 0, 12, 834),
                        type: ui.DisplayFeatureType.hinge,
                        state: ui.DisplayFeatureState.postureFlat,
                      ),
                    ]
                  : [],
            ),
            child: RepaintBoundary(
              key: boundary,
              child: PsatReader(
                key: ValueKey(size),
                controller: c,
                question: q,
              ),
            ),
          ),
        ),
      );
      await t.pumpAndSettle();
      expect(t.takeException(), isNull);
      await t.runAsync(() async {
        final render =
            boundary.currentContext!.findRenderObject()!
                as RenderRepaintBoundary;
        final image = await render.toImage(pixelRatio: 1.5);
        final bytes = await image.toByteData(format: ui.ImageByteFormat.png);
        final file = File(
          'artifacts/psat_readability_20261028/reader-${size.width.toInt()}.png',
        );
        file.parent.createSync(recursive: true);
        file.writeAsBytesSync(bytes!.buffer.asUint8List());
        image.dispose();
      });
      await t.tap(find.byTooltip('공식 문제 원문'));
      await t.pumpAndSettle();
      expect(find.byType(InteractiveViewer), findsOneWidget);
      expect(t.takeException(), isNull);
      await t.pumpWidget(const SizedBox());
      await t.pump();
    }
    await t.pumpWidget(const SizedBox());
    c.dispose();
  });
  testWidgets('law markers align and data figures fit narrow screen and expand', (
    t,
  ) async {
    final c = AppController(MemoryPersistence());
    t.view.devicePixelRatio = 1;
    addTearDown(t.view.resetDevicePixelRatio);
    addTearDown(t.view.resetPhysicalSize);
    for (final size in [const Size(360, 800), const Size(752, 834)]) {
      t.view.physicalSize = size;
      for (final id in [
        '2023-07-22-s-02',
        '2023-07-22-s-12',
        '2023-07-22-d-09',
        '2023-07-22-d-12',
        '2023-07-22-d-14',
      ]) {
        final q = bank.firstWhere((q) => q.id == id);
        final boundary = GlobalKey();
        await t.pumpWidget(
          MaterialApp(
            theme: ThemeData(fontFamily: 'Roboto'),
            home: RepaintBoundary(
              key: boundary,
              child: PsatReader(
                key: ValueKey('$id-$size'),
                controller: c,
                question: q,
              ),
            ),
          ),
        );
        await t.pumpAndSettle();
        if (id.endsWith('s-02')) {
          final markerFinder = find.descendant(
            of: find.byType(PsatPassage),
            matching: find.text('①'),
          );
          final markers = t.widgetList<Text>(markerFinder);
          expect(markers, isNotEmpty);
          expect(
            markers.every((m) => m.style!.fontWeight == FontWeight.w400),
            isTrue,
          );
          final heading = find.byWidgetPredicate(
            (w) => w is PsatText && w.text == '제00조(법 적용의 기준)',
          );
          expect(
            t.getBottomLeft(heading).dy,
            lessThan(t.getTopLeft(markerFinder.first).dy),
          );
        }
        if (q.figures.isNotEmpty) {
          final target = find.byKey(ValueKey(q.figures.first['asset']));
          await t.ensureVisible(target);
          await t.pumpAndSettle();
          final rect = t.getRect(target);
          expect(rect.left, greaterThanOrEqualTo(0));
          expect(rect.right, lessThanOrEqualTo(size.width));
          if (size.width == 360) expect(rect.width, closeTo(344, 0.1));
          if (size.width == 752) expect(rect.width, closeTo(736, 0.1));
        }
        await t.runAsync(() async {
          final render =
              boundary.currentContext!.findRenderObject()!
                  as RenderRepaintBoundary;
          final img = await render.toImage(pixelRatio: 1.5);
          final bytes = await img.toByteData(format: ui.ImageByteFormat.png);
          final file = File(
            'artifacts/psat_data10_20261028/screens/$id-${size.width.toInt()}.png',
          );
          file.parent.createSync(recursive: true);
          file.writeAsBytesSync(bytes!.buffer.asUint8List());
          img.dispose();
        });
        if (q.figures.isNotEmpty) {
          await t.tap(find.byKey(ValueKey(q.figures.first['asset'])));
          await t.pumpAndSettle();
          expect(find.byType(InteractiveViewer), findsOneWidget);
          expect(find.text('자료 확대'), findsOneWidget);
        }
        expect(t.takeException(), isNull, reason: id);
        await t.pumpWidget(const SizedBox());
        await t.pump();
      }
    }
    c.dispose();
  });
  testWidgets('data reading mode and answer survive folding and unfolding', (
    t,
  ) async {
    final c = AppController(MemoryPersistence());
    t.view.devicePixelRatio = 1;
    t.view.physicalSize = const Size(752, 834.67);
    addTearDown(t.view.resetDevicePixelRatio);
    addTearDown(t.view.resetPhysicalSize);
    final q = bank.firstWhere((q) => q.id.endsWith('d-02'));
    await t.pumpWidget(
      MaterialApp(
        home: PsatReader(controller: c, question: q),
      ),
    );
    await t.pumpAndSettle();
    expect(find.byKey(const ValueKey('psat-reading-column')), findsOneWidget);
    await t.tap(find.byTooltip('나란히 보기'));
    await t.pumpAndSettle();
    expect(find.byKey(const ValueKey('psat-reading-split')), findsOneWidget);
    final image = find.byKey(ValueKey(q.figures.first['asset']));
    expect(t.getSize(image).width, closeTo(424, 0.1));
    await t.tap(find.byKey(const ValueKey('psat-option-3')));
    await t.pump();
    t.view.physicalSize = const Size(360, 840);
    await t.pumpAndSettle();
    expect(find.byKey(const ValueKey('psat-reading-column')), findsOneWidget);
    expect(find.byKey(const ValueKey('psat-layout-toggle')), findsNothing);
    await reveal(t, find.byKey(const ValueKey('psat-submit')));
    expect(
      t
          .widget<FilledButton>(find.byKey(const ValueKey('psat-submit')))
          .onPressed,
      isNotNull,
    );
    t.view.physicalSize = const Size(752, 834.67);
    await t.pumpAndSettle();
    expect(find.byKey(const ValueKey('psat-reading-split')), findsOneWidget);
    await t.tap(find.byKey(const ValueKey('psat-submit')));
    await t.pumpAndSettle();
    expect(c.psatRecords.single.selected, 3);
    expect(c.psatRecords.single.correct, isTrue);
    await t.tap(find.byTooltip('크게 읽기'));
    await t.pumpAndSettle();
    await reveal(t, find.text('목록으로'));
    expect(c.psatRecords.length, 1);
    expect(t.takeException(), isNull);
    await t.pumpWidget(const SizedBox());
    c.dispose();
  });
  testWidgets(
    'short data question fits the available Fold screen without scrolling',
    (t) async {
      final c = AppController(MemoryPersistence());
      t.view.devicePixelRatio = 1;
      addTearDown(t.view.resetDevicePixelRatio);
      addTearDown(t.view.resetPhysicalSize);
      for (final spec in [
        (const Size(752, 834.67), 'd-03'),
        (const Size(360, 840), 'd-02'),
      ]) {
        t.view.physicalSize = spec.$1;
        final q = bank.firstWhere((q) => q.id.endsWith(spec.$2));
        await t.pumpWidget(
          MaterialApp(
            home: MediaQuery(
              data: MediaQueryData(
                size: spec.$1,
                padding: const EdgeInsets.only(top: 38, bottom: 48),
              ),
              child: PsatReader(
                key: ValueKey(spec),
                controller: c,
                question: q,
              ),
            ),
          ),
        );
        await t.pumpAndSettle();
        final state = t.state<ScrollableState>(find.byType(Scrollable));
        expect(
          state.position.maxScrollExtent,
          lessThanOrEqualTo(1),
          reason: spec.toString(),
        );
        expect(
          find.byKey(const ValueKey('psat-submit')).hitTestable(),
          findsOneWidget,
        );
        expect(t.takeException(), isNull);
        await t.pumpWidget(const SizedBox());
      }
      c.dispose();
    },
  );
}

// Optional ranges bound host-test memory; the default still visits every question.
List<PsatQuestion> _recoveryRange(Iterable<PsatQuestion> source) {
  const start = int.fromEnvironment('PSAT_RECOVERY_START', defaultValue: 0);
  const count = int.fromEnvironment('PSAT_RECOVERY_COUNT', defaultValue: 0);
  final all = source.toList();
  expect(start, inInclusiveRange(0, all.length - 1));
  expect(count, greaterThanOrEqualTo(0));
  final end = count == 0
      ? all.length
      : (start + count).clamp(0, all.length).toInt();
  final selected = all.sublist(start, end);
  expect(selected, isNotEmpty);
  return selected;
}

void _recordRecovery(String kind, List<PsatQuestion> questions) {
  const output = String.fromEnvironment('PSAT_RECOVERY_OUTPUT');
  if (output.isEmpty) {
    return;
  }
  const start = int.fromEnvironment('PSAT_RECOVERY_START', defaultValue: 0);
  final file = File('$output/$kind-$start.json');
  file.parent.createSync(recursive: true);
  file.writeAsStringSync(
    jsonEncode({
      'status': 'PASS',
      'kind': kind,
      'start': start,
      'questionIds': questions.map((q) => q.id).toList(),
    }),
  );
}
