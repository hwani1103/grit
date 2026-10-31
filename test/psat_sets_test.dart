import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/main.dart';
import 'package:grit/psat.dart';
import 'package:grit/psat_model.dart';
import 'package:grit/psat_sets.dart';
import 'package:grit/store.dart';
import 'store_test.dart' show MemoryPersistence;

class DelayedPersistence extends MemoryPersistence {
  Completer<void>? pending;
  @override
  Future<void> write(String data) async {
    if (pending != null) await pending!.future;
    return super.write(data);
  }
}

PsatAttempt saved(PsatQuestion q, int serial, {bool correct = true}) {
  final start = DateTime(2026, 10, 28, 9).add(Duration(minutes: serial));
  return PsatAttempt(
    id: 'attempt-$serial',
    question: q,
    selected: correct ? q.answer : q.answer % 5 + 1,
    startedAt: start,
    completedAt: start.add(const Duration(seconds: 30)),
    seconds: 30,
  );
}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  late PsatCatalog catalog;
  late Map<String, dynamic> manifest;
  setUpAll(() async {
    catalog = await loadPsatCatalog();
    manifest =
        jsonDecode(await rootBundle.loadString('assets/psat/sets.json'))
            as Map<String, dynamic>;
    for (final name in ['Roboto', 'Ahem']) {
      final font = FontLoader(name)
        ..addFont(
          Future.value(
            ByteData.sublistView(
              File('C:/Windows/Fonts/malgun.ttf').readAsBytesSync(),
            ),
          ),
        );
      await font.load();
    }
  });
  Map<String, dynamic> copyManifest() =>
      jsonDecode(jsonEncode(manifest)) as Map<String, dynamic>;

  test(
    'all published questions have one fixed ten-question Set; bank order cannot change membership',
    () {
      expect(catalog.sets.length, catalog.questions.length ~/ 10);
      final original = catalog.sets.expand((s) => s.questionIds).toList();
      expect(original.toSet(), catalog.questions.keys.toSet());
      expect(original.length, greaterThanOrEqualTo(40));
      final reordered = PsatCatalog(
        catalog.questions.values.toList().reversed.toList(),
        manifest,
      );
      for (var i = 0; i < catalog.sets.length; i++) {
        expect(reordered.sets[i].id, catalog.sets[i].id);
        expect(reordered.sets[i].questionIds, catalog.sets[i].questionIds);
      }
      expect(catalog.forSubject('자료해석').first.id, 'psat-data-002');
      expect(catalog.forSubject('언어논리').first.id, 'psat-verbal-002');
      expect(catalog.forSubject('상황판단').first.id, 'psat-situation-002');
    },
  );

  test(
    'reject incomplete, repeated, missing, cross-subject and unassigned question membership',
    () {
      final invalid = <Map<String, dynamic>>[];
      var m = copyManifest();
      (m['sets'][0]['questionIds'] as List).removeLast();
      invalid.add(m);
      m = copyManifest();
      m['sets'][0]['questionIds'][1] = m['sets'][0]['questionIds'][0];
      invalid.add(m);
      m = copyManifest();
      m['sets'][0]['questionIds'][0] = 'missing';
      invalid.add(m);
      m = copyManifest();
      m['sets'][0]['questionIds'][0] = m['sets'][1]['questionIds'][0];
      invalid.add(m);
      m = copyManifest();
      (m['sets'] as List).removeLast();
      invalid.add(m);
      m = copyManifest();
      m['sets'][1]['id'] = m['sets'][0]['id'];
      invalid.add(m);
      m = copyManifest();
      m['schemaVersion'] = 2;
      invalid.add(m);
      for (final value in invalid) {
        expect(
          () => PsatCatalog(catalog.questions.values.toList(), value),
          throwsFormatException,
        );
      }
    },
  );

  test(
    'pending and failed writes do not count; wrong answers, retries, reload and old snapshots do',
    () async {
      final disk = DelayedPersistence();
      final c = AppController(disk);
      final set = catalog.sets.first;
      final q = catalog.questions[set.questionIds.first]!;
      disk.pending = Completer<void>();
      final pendingSave = c.savePsat(saved(q, 1, correct: false));
      expect(PsatProgress(c.psatRecords).completed(set), 0);
      disk.pending!.complete();
      await pendingSave;
      disk.pending = null;
      expect(PsatProgress(c.psatRecords).completed(set), 1);
      expect(PsatProgress(c.psatRecords).wrong(set), 1);
      final originalSnapshot = c.psatRecords.single.question.toJson();
      disk.fail = true;
      await expectLater(
        c.savePsat(saved(catalog.questions[set.questionIds[1]]!, 2)),
        throwsStateError,
      );
      expect(PsatProgress(c.psatRecords).completed(set), 1);
      disk.fail = false;
      for (var n = 3; n <= 12; n++) {
        await c.savePsat(saved(q, n));
      }
      expect(PsatProgress(c.psatRecords).completed(set), 1);
      expect(PsatProgress(c.psatRecords).wrong(set), 0);
      // The latest result is based on timestamp, even for an unordered input.
      expect(PsatProgress(c.psatRecords.reversed).wrong(set), 0);
      for (var i = 1; i < set.questionIds.length; i++) {
        await c.savePsat(
          saved(catalog.questions[set.questionIds[i]]!, i + 20, correct: false),
        );
      }
      expect(PsatProgress(c.psatRecords).completed(set), 10);
      expect(PsatProgress(c.psatRecords).wrong(set), 9);
      final reopened = AppController(disk);
      await reopened.load();
      expect(PsatProgress(reopened.psatRecords).completed(set), 10);
      expect(PsatProgress(reopened.psatRecords).wrong(set), 9);
      expect(reopened.psatRecords.last.question.toJson(), originalSnapshot);
      // A future bank revision with the same ID must not replace saved snapshots.
      final changed = q.toJson()
        ..['body'] = '수정된 현재 은행 본문'
        ..['revision'] = 2;
      final nextBank = catalog.questions.values
          .map((x) => x.id == q.id ? PsatQuestion.fromJson(changed) : x)
          .toList();
      final next = PsatCatalog(nextBank, manifest);
      expect(PsatProgress(reopened.psatRecords).completed(next.sets.first), 10);
      expect(reopened.psatRecords.last.question.toJson(), originalSnapshot);
      c.dispose();
      reopened.dispose();
    },
  );

  Future<void> loadLibrary(WidgetTester t) async {
    await t.runAsync(() async {
      await loadPsatCatalog();
    });
    await t.pumpAndSettle();
  }

  testWidgets(
    'Set card updates from committed records and keeps completion independent of wrong filter',
    (t) async {
      final c = AppController(MemoryPersistence());
      final set = catalog.forSubject('자료해석').first;
      await t.pumpWidget(GritApp(controller: c));
      await t.tap(find.text('자료해석'));
      await t.pump();
      await loadLibrary(t);
      expect(find.text('Set 1 (0 / 10)'), findsOneWidget);
      final card = find.byKey(ValueKey('psat-set-${set.id}'));
      final initialColor = t.widget<Card>(card).color;
      for (var i = 0; i < 10; i++) {
        await c.savePsat(
          saved(catalog.questions[set.questionIds[i]]!, i, correct: false),
        );
      }
      await t.pumpAndSettle();
      expect(find.text('Set 1 (10 / 10)'), findsOneWidget);
      expect(find.text('풀이 완료'), findsOneWidget);
      expect(t.widget<Card>(card).color, isNot(initialColor));
      await t.tap(find.text('다시 볼 오답'));
      await t.pumpAndSettle();
      expect(find.text('Set 1 (10 / 10)'), findsOneWidget);
      await t.tap(card);
      await t.pumpAndSettle();
      expect(find.byType(PsatSetScreen), findsOneWidget);
      expect(find.text('Set 1 (10 / 10)'), findsOneWidget);
      expect(t.widget<FilterChip>(find.byType(FilterChip)).selected, isTrue);
      final q = catalog.questions[set.questionIds.first]!;
      await c.savePsat(saved(q, 100));
      await t.pumpAndSettle();
      expect(find.byKey(ValueKey('psat-question-${q.id}')), findsNothing);
      expect(find.text('Set 1 (10 / 10)'), findsOneWidget);
      await t.tap(find.text('다시 볼 오답'));
      await t.pumpAndSettle();
      await t.tap(find.byKey(ValueKey('psat-question-${q.id}')));
      await t.pumpAndSettle();
      final reader = t.widget<PsatReader>(find.byType(PsatReader));
      expect(reader.review?.id, 'attempt-100');
      expect(reader.question.toJson(), c.psatRecords.first.question.toJson());
      await t.pumpWidget(const SizedBox());
      c.dispose();
    },
  );

  testWidgets(
    'Set browsing and progress survive fold and large type; all ten cards remain reachable',
    (t) async {
      t.view.devicePixelRatio = 1;
      addTearDown(t.view.resetDevicePixelRatio);
      addTearDown(t.view.resetPhysicalSize);
      final c = AppController(MemoryPersistence());
      final set = catalog.forSubject('언어논리').first;
      await c.savePsat(
        saved(catalog.questions[set.questionIds.first]!, 1, correct: false),
      );
      t.view.physicalSize = const Size(360, 840);
      await t.pumpWidget(
        MaterialApp(
          theme: ThemeData(fontFamily: 'Roboto'),
          builder: (context, child) => MediaQuery(
            data: MediaQuery.of(
              context,
            ).copyWith(textScaler: TextScaler.linear(1.4)),
            child: child!,
          ),
          home: PsatSetScreen(controller: c, catalog: catalog, set: set),
        ),
      );
      for (final size in [
        const Size(360, 840),
        const Size(752, 834),
        const Size(320, 640),
        const Size(840, 360),
        const Size(360, 840),
      ]) {
        t.view.physicalSize = size;
        await t.pumpAndSettle();
        final scroll = find.byType(Scrollable).first;
        await t.scrollUntilVisible(
          find.text('Set 1 (1 / 10)'),
          -400,
          scrollable: scroll,
          maxScrolls: 80,
        );
        for (final id in set.questionIds) {
          final card = find.byKey(ValueKey('psat-question-$id'));
          await t.scrollUntilVisible(
            card,
            350,
            scrollable: scroll,
            maxScrolls: 80,
          );
          await t.pumpAndSettle();
          expect(card.hitTestable(), findsOneWidget, reason: '$size / $id');
          expect(t.takeException(), isNull, reason: '$size / $id');
        }
        expect(PsatProgress(c.psatRecords).completed(set), 1);
      }
      await t.pumpWidget(const SizedBox());
      c.dispose();
    },
  );
}
