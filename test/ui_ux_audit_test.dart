import 'dart:convert';
import 'dart:io';
import 'dart:ui' as ui;
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/guide.dart';
import 'package:grit/guide_content.dart';
import 'package:grit/main.dart';
import 'package:grit/model.dart';
import 'package:grit/practice.dart';
import 'package:grit/psat.dart';
import 'package:grit/psat_sets.dart';
import 'package:grit/store.dart';
import 'package:grit/word_text.dart';
import 'store_test.dart' show MemoryPersistence;

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  final out = Directory('artifacts/ui_ux_audit_20261031')
    ..createSync(recursive: true);
  setUpAll(() async {
    for (final family in ['Roboto', 'Ahem']) {
      await (FontLoader(family)..addFont(
            Future.value(
              ByteData.sublistView(
                File('C:/Windows/Fonts/malgun.ttf').readAsBytesSync(),
              ),
            ),
          ))
          .load();
    }
    await (FontLoader('MaterialIcons')..addFont(
          Future.value(
            ByteData.sublistView(
              File(
                'C:/tools/flutter/bin/cache/artifacts/material_fonts/MaterialIcons-Regular.otf',
              ).readAsBytesSync(),
            ),
          ),
        ))
        .load();
  });

  for (final kind in [SetKind.multiplication, SetKind.division]) {
    testWidgets(
      '${kind.name} is generated once and advances after 100ms with immediate selection',
      (t) async {
        t.view.devicePixelRatio = 1;
        t.view.physicalSize = const Size(390, 844);
        addTearDown(t.view.resetDevicePixelRatio);
        addTearDown(t.view.resetPhysicalSize);
        final c = AppController(MemoryPersistence());
        final session = await c.start(kind);
        final originalProblems = session.problems;
        final before = jsonEncode(
          originalProblems.map((p) => p.toJson()).toList(),
        );
        expect(
          originalProblems.length,
          kind == SetKind.multiplication ? 18 : 15,
        );
        await t.pumpWidget(
          MaterialApp(
            theme: ThemeData(fontFamily: 'Roboto'),
            home: PracticeScreen(controller: c, session: session),
          ),
        );
        await t.pumpAndSettle();
        if (kind == SetKind.division) {
          final order = session.problems.first.ordered;
          for (final i in order.take(3)) {
            await t.tap(find.text(String.fromCharCode(65 + i)).first);
            await t.pump();
            expect(session.page, 0);
          }
          await t.tap(find.text(String.fromCharCode(65 + order.last)).first);
        } else {
          await t.tap(find.text('왼쪽이 큼'));
        }
        await t.pump();
        expect(session.hasAnswer('0'), isTrue);
        expect(session.page, 0);
        await t.pump(const Duration(milliseconds: 99));
        expect(session.page, 0);
        await t.pump(const Duration(milliseconds: 1));
        expect(session.page, 1);
        expect(identical(session.problems, originalProblems), isTrue);
        expect(
          jsonEncode(session.problems.map((p) => p.toJson()).toList()),
          before,
        );
        expect(t.takeException(), isNull);
        await t.pumpWidget(const SizedBox());
        c.dispose();
      },
    );
  }

  testWidgets(
    'all text call-site literals fit at narrow widths and larger text',
    (t) async {
      final inventory =
          jsonDecode(
                File(
                  'test/fixtures/ui_text_inventory_20261031.json',
                ).readAsStringSync(),
              )
              as List;
      var checks = 0;
      final labels = <Map<String, dynamic>>[];
      for (final value in inventory) {
        final item = Map<String, dynamic>.from(value as Map);
        for (final text in item['literals'] as List) {
          if ((text as String).trim().isNotEmpty) {
            labels.add({...item, 'text': text});
          }
        }
      }
      for (var c = 0; c < guideChapters.length; c++) {
        final chapter = guideChapters[c];
        final texts = [
          chapter.title,
          chapter.subtitle,
          chapter.intro,
          chapter.route,
          for (final tip in chapter.tips) ...[
            tip.title,
            tip.level,
            tip.when,
            tip.steps,
            tip.why,
            tip.benefit,
            tip.caution,
            tip.next,
          ],
          for (final quiz in chapter.quizzes) ...[quiz.question, quiz.answer],
        ];
        for (final text in texts) {
          labels.add({
            'file': 'lib/guide_content.dart',
            'line': 'chapter ${c + 1}',
            'text': text,
            'style': {'fontSize': 16, 'height': 1.8},
            'guide': true,
          });
        }
      }
      final checked = <Map<String, Object?>>[];
      for (final item in labels) {
        final style = Map<String, dynamic>.from(item['style'] as Map);
        final text = item['text'] as String;
        for (final width
            in (item['guide'] == true
                ? [280.0, 350.0, 712.0]
                : [64.0, 130.0, 280.0, 350.0, 712.0])) {
          for (final scale in [1.0, 1.4, 2.0]) {
            await t.pumpWidget(
              MaterialApp(
                home: MediaQuery(
                  data: MediaQueryData(textScaler: TextScaler.linear(scale)),
                  child: OverflowBox(
                    minWidth: 0,
                    maxWidth: width,
                    minHeight: 0,
                    maxHeight: double.infinity,
                    alignment: Alignment.topCenter,
                    child: SizedBox(
                      width: width,
                      child: WordText(
                        text,
                        style: TextStyle(
                          fontFamily: 'Roboto',
                          fontSize:
                              (style['fontSize'] as num?)?.toDouble() ?? 14,
                          height: (style['height'] as num?)?.toDouble(),
                          letterSpacing: (style['letterSpacing'] as num?)
                              ?.toDouble(),
                          fontWeight:
                              FontWeight.values[((style['weight'] as int? ??
                                          400) ~/
                                      100) -
                                  1],
                        ),
                      ),
                    ),
                  ),
                ),
              ),
            );
            await t.pump();
            final paragraph = t.renderObject<RenderParagraph>(
              find.descendant(
                of: find.byType(WordText),
                matching: find.byWidgetPredicate(
                  (w) => w.runtimeType.toString() == '_WordParagraphWidget',
                ),
              ),
            );
            expect(
              paragraph.didExceedMaxLines,
              isFalse,
              reason: '${item['file']}:${item['line']} $width/$scale',
            );
            expect(paragraph.text.toPlainText().replaceAll('\u2060', ''), text);
            expect(
              t.takeException(),
              isNull,
              reason: '${item['file']}:${item['line']} $width/$scale',
            );
            checks++;
          }
        }
        checked.add({'file': item['file'], 'line': item['line'], 'text': text});
      }
      File('${out.path}/text-matrix.json').writeAsStringSync(
        const JsonEncoder.withIndent('  ').convert({
          'status': 'PASS',
          'callSites': inventory.length,
          'literalAlternatives': labels.length,
          'checks': checks,
          'widths': [64, 130, 280, 350, 712],
          'scales': [1, 1.4, 2],
          'labels': checked,
        }),
      );
      await t.pumpWidget(const SizedBox());
    },
  );

  testWidgets(
    'screen families: layouts, reachable controls and host captures',
    (t) async {
      t.view.devicePixelRatio = 1;
      addTearDown(t.view.resetDevicePixelRatio);
      addTearDown(t.view.resetPhysicalSize);
      late PsatCatalog catalog;
      await t.runAsync(() async {
        catalog = await loadPsatCatalog();
      });
      final captures = <String>[];
      for (final size in [
        const Size(320, 640),
        const Size(390, 844),
        const Size(844, 390),
        const Size(752, 834),
      ]) {
        t.view.physicalSize = size;
        final c = AppController(MemoryPersistence());
        final session = PracticeSession(
          id: 'audit',
          kind: SetKind.multiplication,
          seed: 73,
          problems: Generator(73).generate(SetKind.multiplication),
          startedAt: DateTime(2026, 10, 31),
          completedAt: DateTime(2026, 10, 31, 0, 2),
          elapsedSeconds: 120,
        );
        session.answers.addAll(session.expected);
        c.records = [session];
        Future<void> screen(
          String name,
          Widget child, {
          bool app = false,
          String? tapText,
          String? tapTooltip,
          String? tapKey,
        }) async {
          final key = GlobalKey();
          await t.pumpWidget(
            RepaintBoundary(
              key: key,
              child: app
                  ? child
                  : MaterialApp(
                      debugShowCheckedModeBanner: false,
                      theme: ThemeData(
                        fontFamily: 'Roboto',
                        colorScheme: ColorScheme.fromSeed(seedColor: ink),
                      ),
                      home: child,
                    ),
            ),
          );
          for (
            var i = 0;
            i < 100 &&
                find.byType(CircularProgressIndicator).evaluate().isNotEmpty;
            i++
          ) {
            await t.runAsync(
              () => Future<void>.delayed(const Duration(milliseconds: 20)),
            );
            await t.pump();
          }
          await t.pumpAndSettle();
          if (tapText != null) {
            await t.tap(find.text(tapText));
            await t.pumpAndSettle();
          }
          if (tapTooltip != null) {
            await t.tap(find.byTooltip(tapTooltip));
            await t.pumpAndSettle();
          }
          if (tapKey != null) {
            await t.tap(find.byKey(ValueKey(tapKey)));
            await t.pumpAndSettle();
          }
          // Asset decoding runs outside the fake test clock. Wait for actual
          // image frames so a pending decoder cannot look like a blank figure.
          await t.runAsync(() async {
            for (final element in find.byType(Image).evaluate()) {
              await precacheImage((element.widget as Image).image, element);
            }
          });
          await t.pumpAndSettle();
          for (final element in find.byType(RawImage).evaluate()) {
            expect(
              (element.widget as RawImage).image,
              isNotNull,
              reason: '$name $size',
            );
          }
          expect(t.takeException(), isNull, reason: '$name $size');
          await t.runAsync(() async {
            final boundary =
                key.currentContext!.findRenderObject()!
                    as RenderRepaintBoundary;
            final image = await boundary.toImage();
            final bytes = await image.toByteData(
              format: ui.ImageByteFormat.png,
            );
            final file =
                '$name-${size.width.toInt()}x${size.height.toInt()}.png';
            File(
              '${out.path}/$file',
            ).writeAsBytesSync(bytes!.buffer.asUint8List());
            image.dispose();
            captures.add(file);
          });
        }

        await screen('home', GritApp(controller: c), app: true);
        for (final kind in SetKind.values) {
          final button = find.byKey(ValueKey('vitamin-history-${kind.name}'));
          expect(button.hitTestable(), findsOneWidget);
          expect(t.getSize(button).shortestSide, greaterThanOrEqualTo(48));
        }
        await screen(
          'global-history',
          GritApp(controller: c),
          app: true,
          tapText: '나의 기록',
        );
        await screen(
          'settings',
          GritApp(controller: c),
          app: true,
          tapTooltip: '설정 및 기록 관리',
        );
        await screen(
          'prepare',
          GritApp(controller: c),
          app: true,
          tapKey: 'vitamin-start-multiplication',
        );
        await screen(
          'vitamin-history',
          Scaffold(
            body: VitaminHistoryDialog(
              kind: SetKind.multiplication,
              records: c.records,
            ),
          ),
        );
        await screen('vitamin-result', ResultScreen(session: session));
        for (final kind in SetKind.values) {
          final active = PracticeSession(
            id: 'active-${kind.name}',
            kind: kind,
            seed: 73,
            problems: Generator(73).generate(kind),
            startedAt: DateTime.now(),
          );
          c.active = active;
          await screen(
            'practice-${kind.name}',
            PracticeScreen(controller: c, session: active),
          );
          if (kind != SetKind.addition) {
            active.page = kind == SetKind.multiplication ? 8 : 5;
            await screen(
              'fraction-${kind.name}',
              PracticeScreen(
                key: ValueKey(active.page),
                controller: c,
                session: active,
              ),
            );
          }
          c.active = null;
        }
        await screen('guide', const GuideScreen());
        await screen(
          'guide-chapter',
          const GuideChapterScreen(chapterIndex: 0),
        );
        for (final subject in ['자료해석', '언어논리', '상황판단']) {
          await screen(
            'library-$subject',
            Scaffold(
              body: PsatLibrary(controller: c, subject: subject),
            ),
          );
          final set = catalog.forSubject(subject).first;
          await screen(
            'set-$subject',
            PsatSetScreen(controller: c, catalog: catalog, set: set),
          );
          await screen(
            'reader-$subject',
            PsatReader(
              controller: c,
              question: catalog.questions[set.questionIds.first]!,
            ),
          );
        }
        await screen('psat-history', PsatHistory(controller: c));
        await t.pumpWidget(const SizedBox());
        c.dispose();
      }
      File('${out.path}/screen-matrix.json').writeAsStringSync(
        const JsonEncoder.withIndent(
          '  ',
        ).convert({'status': 'PASS', 'captures': captures}),
      );
    },
  );
}
