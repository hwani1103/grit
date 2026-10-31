import 'dart:convert';
import 'package:grit/main.dart';
import 'package:grit/model.dart';
import 'package:grit/practice.dart';
import 'ui_test.dart' show sample;
import 'dart:io';
import 'dart:ui' as ui;
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/grit_dialog.dart';
import 'package:grit/psat.dart';
import 'package:grit/psat_model.dart';
import 'package:grit/store.dart';
import 'package:grit/word_text.dart';
import 'store_test.dart' show MemoryPersistence;

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  late List<PsatQuestion> bank;
  setUpAll(() async {
    bank = await loadPsatBank();
    for (final family in ['Roboto', 'Ahem']) {
      final loader = FontLoader(family)
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
  Rect surface(WidgetTester t) => t.getRect(
    find
        .descendant(
          of: find.byType(AlertDialog),
          matching: find.byWidgetPredicate(
            (w) => w is Material && w.type == MaterialType.card,
          ),
        )
        .last,
  );
  const inner = Size(752, 834);
  const cover = Size(360, 840);
  List<ui.DisplayFeature> features(Size size, ui.DisplayFeatureState state) =>
      size == cover
      ? []
      : [
          ui.DisplayFeature(
            bounds: Rect.fromLTWH(size.width / 2, 0, 0, size.height),
            type: ui.DisplayFeatureType.fold,
            state: state,
          ),
        ];

  testWidgets(
    'all published leave dialogs stay centered through flat half-open cover and return',
    (t) async {
      t.view.devicePixelRatio = 1;
      addTearDown(t.view.resetDevicePixelRatio);
      addTearDown(t.view.resetPhysicalSize);
      final c = AppController(MemoryPersistence());
      final reviewing = _recoveryRange(bank);
      for (final q in reviewing) {
        final nav = GlobalKey<NavigatorState>();
        final media = ValueNotifier<MediaQueryData>(
          const MediaQueryData(size: inner),
        );
        t.view.physicalSize = inner;
        await t.pumpWidget(
          MaterialApp(
            navigatorKey: nav,
            builder: (context, child) => ValueListenableBuilder<MediaQueryData>(
              valueListenable: media,
              builder: (context, value, _) =>
                  MediaQuery(data: value, child: child!),
            ),
            home: const Scaffold(body: Text('list')),
          ),
        );
        nav.currentState!.push(
          MaterialPageRoute(
            builder: (_) => PsatReader(controller: c, question: q),
          ),
        );
        await t.pumpAndSettle();
        nav.currentState!.maybePop();
        await t.pumpAndSettle();
        for (final spec in [
          (inner, ui.DisplayFeatureState.postureFlat),
          (inner, ui.DisplayFeatureState.postureHalfOpened),
          (cover, ui.DisplayFeatureState.unknown),
          (inner, ui.DisplayFeatureState.postureHalfOpened),
          (inner, ui.DisplayFeatureState.postureFlat),
        ]) {
          t.view.physicalSize = spec.$1;
          media.value = MediaQueryData(
            size: spec.$1,
            padding: const EdgeInsets.only(top: 38, bottom: 48),
            displayFeatures: features(spec.$1, spec.$2),
          );
          await t.pumpAndSettle();
          expect(
            surface(t).center.dx,
            closeTo(spec.$1.width / 2, .5),
            reason: '${q.id} $spec',
          );
          expect(
            surface(t).center.dy,
            closeTo((38 + spec.$1.height - 48) / 2, .5),
          );
          expect(find.text('계속 풀기').hitTestable(), findsOneWidget);
          expect(find.text('그만두기').hitTestable(), findsOneWidget);
          expect(t.takeException(), isNull, reason: q.id);
        }
        await t.tap(find.text('계속 풀기'));
        await t.pumpAndSettle();
        expect(find.byType(PsatReader), findsOneWidget);
        expect(c.psatRecords, isEmpty);
        nav.currentState!.maybePop();
        await t.pumpAndSettle();
        await t.tap(find.text('그만두기'));
        await t.pumpAndSettle();
        expect(find.byType(PsatReader), findsNothing);
        expect(c.psatRecords, isEmpty);
        await t.pumpWidget(const SizedBox());
        media.dispose();
      }
      _recordRecovery('dialogs', reviewing);
      c.dispose();
    },
  );

  testWidgets(
    'real hinge remains avoided and common dialog can dismiss via barrier',
    (t) async {
      t.view.devicePixelRatio = 1;
      t.view.physicalSize = inner;
      addTearDown(t.view.resetDevicePixelRatio);
      addTearDown(t.view.resetPhysicalSize);
      final nav = GlobalKey<NavigatorState>();
      await t.pumpWidget(
        MaterialApp(
          navigatorKey: nav,
          builder: (context, child) => MediaQuery(
            data: const MediaQueryData(
              size: inner,
              displayFeatures: [
                ui.DisplayFeature(
                  bounds: Rect.fromLTWH(370, 0, 12, 834),
                  type: ui.DisplayFeatureType.hinge,
                  state: ui.DisplayFeatureState.postureHalfOpened,
                ),
              ],
            ),
            child: child!,
          ),
          home: Builder(
            builder: (context) => Scaffold(
              body: TextButton(
                onPressed: () => showGritDialog<void>(
                  context: context,
                  builder: (_) => const AlertDialog(
                    title: WordText('확인'),
                    content: WordText('내용을 확인해 주세요.'),
                  ),
                ),
                child: const Text('open'),
              ),
            ),
          ),
        ),
      );
      await t.tap(find.text('open'));
      await t.pumpAndSettle();
      expect(surface(t).right, lessThanOrEqualTo(370));
      await t.tapAt(const Offset(730, 100));
      await t.pumpAndSettle();
      expect(find.byType(AlertDialog), findsNothing);
      expect(t.takeException(), isNull);
    },
  );
  testWidgets(
    'vitamin exit submit and history reset stay centered without changing records on cancel',
    (t) async {
      t.view.devicePixelRatio = 1;
      t.view.physicalSize = inner;
      addTearDown(t.view.resetDevicePixelRatio);
      addTearDown(t.view.resetPhysicalSize);
      final c = AppController(MemoryPersistence());
      final session = sample(SetKind.addition)..memos['0:r:0'] = '456';
      c.active = session;
      c.records.add(
        sample(SetKind.multiplication)
          ..completedAt = DateTime.now()
          ..elapsedSeconds = 90,
      );
      final nav = GlobalKey<NavigatorState>();
      final media = ValueNotifier(
        MediaQueryData(
          size: inner,
          displayFeatures: features(
            inner,
            ui.DisplayFeatureState.postureHalfOpened,
          ),
        ),
      );
      await t.pumpWidget(
        MaterialApp(
          navigatorKey: nav,
          builder: (context, child) => ValueListenableBuilder<MediaQueryData>(
            valueListenable: media,
            builder: (_, value, _) => MediaQuery(data: value, child: child!),
          ),
          home: HomeScreen(controller: c),
        ),
      );
      await t.pumpAndSettle();
      nav.currentState!.push(
        MaterialPageRoute(
          builder: (_) => PracticeScreen(controller: c, session: session),
        ),
      );
      await t.pumpAndSettle();
      Future<void> check() async {
        for (final spec in [
          (inner, ui.DisplayFeatureState.postureHalfOpened),
          (inner, ui.DisplayFeatureState.postureFlat),
          (cover, ui.DisplayFeatureState.unknown),
          (inner, ui.DisplayFeatureState.postureHalfOpened),
        ]) {
          t.view.physicalSize = spec.$1;
          media.value = MediaQueryData(
            size: spec.$1,
            displayFeatures: features(spec.$1, spec.$2),
          );
          await t.pumpAndSettle();
          expect(surface(t).center.dx, closeTo(spec.$1.width / 2, .5));
          expect(t.takeException(), isNull);
        }
      }

      await t.tap(find.byTooltip('연습 나가기'));
      await t.pumpAndSettle();
      await check();
      await t.tap(find.text('계속 풀기'));
      await t.pumpAndSettle();
      expect(c.active, same(session));
      expect(session.memos['0:r:0'], '456');
      await t.tap(find.text('완료'));
      await t.pumpAndSettle();
      await check();
      await t.tap(find.text('마저 풀기'));
      await t.pumpAndSettle();
      expect(c.active, same(session));
      expect(c.records.length, 1);
      // Remove only the test route without activating the discard operation.
      nav.currentState!.pop();
      await t.pumpAndSettle();
      await t.tap(find.byTooltip('설정 및 기록 관리'));
      await t.pumpAndSettle();
      await t.tap(find.text('기록 초기화'));
      await t.pumpAndSettle();
      await check();
      await t.tap(find.text('취소'));
      await t.pumpAndSettle();
      expect(c.records.length, 1);
      expect(c.active, same(session));
      expect(session.memos['0:r:0'], '456');
      await t.pumpWidget(const SizedBox());
      media.dispose();
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
