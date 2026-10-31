import 'dart:convert';
import 'dart:io';
import 'dart:ui' as ui;
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/store.dart';
import 'package:grit/psat.dart';
import 'package:grit/psat_model.dart';
import 'package:grit/psat_sets.dart';
import 'package:grit/psat_text.dart';
import 'store_test.dart' show MemoryPersistence;

PsatAttempt record(PsatQuestion q, String id) {
  final start = DateTime(2026, 10, 28, 12);
  return PsatAttempt(
    id: id,
    question: q,
    selected: q.answer,
    startedAt: start,
    completedAt: start.add(const Duration(seconds: 45)),
    seconds: 45,
  );
}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  late PsatCatalog catalog;
  setUpAll(() async {
    catalog = await loadPsatCatalog();
    for (final name in ['Roboto', 'Ahem']) {
      await (FontLoader(name)..addFont(
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

  test(
    'actual 50 revision-one snapshots survive current bank and reattempt',
    () async {
      final disk = MemoryPersistence();
      final c = AppController(disk);
      final originals = <String, Map<String, dynamic>>{};
      for (final file in ['batch01', 'data01', 'verbal02', 'situation02']) {
        for (final raw
            in jsonDecode(
                  File(
                    'artifacts/psat_explanations_20261028/before/$file.json',
                  ).readAsStringSync(),
                )
                as List) {
          final q = PsatQuestion.fromJson(
            Map<String, dynamic>.from(raw as Map),
          );
          final a = record(q, 'old-${q.id}');
          originals[a.id] = a.toJson();
          await c.savePsat(a);
        }
      }
      expect(originals.length, 50);
      for (final q in catalog.questions.values.where(
        (q) => originals.containsKey('old-${q.id}'),
      )) {
        expect(q.data['revision'], greaterThanOrEqualTo(2));
        await c.savePsat(record(q, 'new-${q.id}'));
      }
      final reopened = AppController(disk);
      await reopened.load();
      expect(reopened.psatRecords.length, 100);
      for (final a in reopened.psatRecords) {
        if (a.id.startsWith('old-')) {
          expect(a.toJson(), originals[a.id], reason: a.id);
          expect(a.question.data['revision'], 1);
        } else {
          expect(
            a.question.toJson(),
            catalog.questions[a.question.id]!.toJson(),
          );
        }
      }
      for (final set in catalog.sets) {
        expect(
          PsatProgress(reopened.psatRecords).completed(set),
          set.questionIds
              .where((id) => originals.containsKey('old-$id'))
              .length,
        );
      }
      reopened.dispose();
      c.dispose();
    },
  );

  testWidgets(
    'all published reviews stay reachable through open-cover-open transitions',
    (t) async {
      t.view.devicePixelRatio = 1;
      addTearDown(t.view.resetDevicePixelRatio);
      addTearDown(t.view.resetPhysicalSize);
      final c = AppController(MemoryPersistence());
      var reviewed = 0;
      final reviewing = _recoveryRange(catalog.questions.values);
      for (final q in reviewing) {
        t.view.physicalSize = const Size(752, 834);
        await t.pumpWidget(
          MaterialApp(
            theme: ThemeData(fontFamily: 'Roboto'),
            home: PsatReader(
              key: ValueKey(q.id),
              controller: c,
              question: q,
              review: record(q, q.id),
            ),
          ),
        );
        await t.pumpAndSettle();
        for (final size in [
          const Size(752, 834),
          const Size(360, 840),
          const Size(752, 834),
        ]) {
          t.view.physicalSize = size;
          await t.pumpAndSettle();
          t
              .state<ScrollableState>(find.byType(Scrollable).last)
              .position
              .jumpTo(0);
          await t.pumpAndSettle();
          final limit = find.byWidgetPredicate(
            (w) => w is PsatText && w.text == q.steps.last,
          );
          await t.scrollUntilVisible(
            limit,
            450,
            scrollable: find.byType(Scrollable).last,
            maxScrolls: 150,
          );
          await t.pumpAndSettle();
          expect(limit.hitTestable(), findsOneWidget, reason: q.id);
          await t.scrollUntilVisible(
            find.text('목록으로'),
            450,
            scrollable: find.byType(Scrollable).last,
            maxScrolls: 150,
          );
          await t.pumpAndSettle();
          expect(
            find.text('목록으로').hitTestable(),
            findsOneWidget,
            reason: '${q.id} $size',
          );
          expect(t.takeException(), isNull, reason: '${q.id} $size');
        }
        reviewed++;
        if (reviewed % 100 == 0) {
          debugPrint(
            'Fold transition review: $reviewed/${catalog.questions.length}',
          );
        }
      }
      expect(reviewed, reviewing.length);
      _recordRecovery('transitions', reviewing);
      expect(c.psatRecords, isEmpty);
      await t.pumpWidget(const SizedBox());
      c.dispose();
    },
  );

  testWidgets('capture new fast explanations on cover and open screens', (
    t,
  ) async {
    t.view.devicePixelRatio = 1;
    addTearDown(t.view.resetDevicePixelRatio);
    addTearDown(t.view.resetPhysicalSize);
    final c = AppController(MemoryPersistence());
    for (final size in [const Size(360, 840), const Size(752, 834)]) {
      t.view.physicalSize = size;
      for (final id in [
        '2023-07-22-l-14',
        '2023-07-22-d-19',
        'kr-mpm-2024-07-27-psat-s-06',
      ]) {
        final q = catalog.questions[id]!;
        final key = GlobalKey();
        await t.pumpWidget(
          MaterialApp(
            theme: ThemeData(fontFamily: 'Roboto'),
            home: RepaintBoundary(
              key: key,
              child: PsatReader(
                key: ValueKey('$id-$size'),
                controller: c,
                question: q,
                review: record(q, id),
              ),
            ),
          ),
        );
        await t.pumpAndSettle();
        final trigger = find.byWidgetPredicate(
          (w) => w is PsatText && w.text == q.steps.first,
        );
        await t.scrollUntilVisible(
          trigger,
          450,
          scrollable: find.byType(Scrollable).last,
          maxScrolls: 150,
        );
        await Scrollable.ensureVisible(t.element(trigger), alignment: 0.05);
        await t.pumpAndSettle();
        await t.runAsync(() async {
          final img =
              await (key.currentContext!.findRenderObject()!
                      as RenderRepaintBoundary)
                  .toImage(pixelRatio: 1.5);
          final bytes = await img.toByteData(format: ui.ImageByteFormat.png);
          final file = File(
            'artifacts/psat_explanations_20261028/screens/$id-${size.width.toInt()}.png',
          );
          file.parent.createSync(recursive: true);
          file.writeAsBytesSync(bytes!.buffer.asUint8List());
          img.dispose();
        });
        expect(t.takeException(), isNull, reason: id);
        await t.pumpWidget(const SizedBox());
      }
    }
    c.dispose();
  });
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
