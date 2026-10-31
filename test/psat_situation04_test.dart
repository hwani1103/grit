import 'dart:io';
import 'dart:ui' as ui;
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/psat.dart';
import 'package:grit/psat_model.dart';
import 'package:grit/psat_sets.dart';
import 'package:grit/psat_text.dart';
import 'package:grit/store.dart';
import 'store_test.dart' show MemoryPersistence;

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  late List<PsatQuestion> added;
  setUpAll(() async {
    final catalog = await loadPsatCatalog();
    added = catalog.sets
        .singleWhere((s) => s.id == 'psat-situation-004')
        .questionIds
        .map((id) => catalog.questions[id]!)
        .toList();
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
    'situation Set4 preserves mixed years, nine native tables and prose and keys',
    () {
      expect(added.length, 10);
      const keys = [2, 4, 3, 3, 2, 3, 4, 2, 5, 1];
      for (final q in added) {
        expect(q.answer, keys[added.indexOf(q)]);
        expect(q.steps.length, 5);
        expect(q.reasons.length, 5);
        expect(PsatQuestion.fromJson(q.toJson()).toJson(), q.toJson());
        for (final u in q.underlines) {
          expect(q.body.split(u).length - 1, 1);
          final spans = psatInlineSpans(q.body, q.underlines);
          expect(
            spans.any(
              (s) =>
                  s.style?.decoration == TextDecoration.underline &&
                  (s.text ?? '').contains(u),
            ),
            isTrue,
          );
        }
      }
      expect(added.expand((q) => q.tables).length, 9);
      expect(added.expand((q) => q.figures).length, 0);
      expect(added[4].steps.join(' '), contains('24일'));
      expect(added[4].steps.join(' '), isNot(contains('30일')));
      expect(added[2].tables.single['rows'], [
        ['甲', '08:55', '20:00', '－', '10:30', '13:30'],
        ['乙', '08:00', '19:55', '－', '－', '－'],
        ['丙', '09:00', '21:30', '개인용무시간 (19:00～19:30)', '13:00', '14:30'],
        ['丁', '08:30', '23:30', '재택근무', '－', '－'],
        ['戊', '07:00', '21:30', '－', '－', '－'],
      ]);
      expect(added[9].tables.length, 3);
    },
  );
  testWidgets('situation Set4 source features fit cover and open screens', (
    t,
  ) async {
    t.view.devicePixelRatio = 1;
    addTearDown(t.view.resetDevicePixelRatio);
    addTearDown(t.view.resetPhysicalSize);
    final c = AppController(MemoryPersistence());
    for (final size in [const Size(360, 840), const Size(752, 834)]) {
      t.view.physicalSize = size;
      for (final n in [0, 1, 2, 5, 9]) {
        final q = added[n];
        final boundary = GlobalKey();
        await t.pumpWidget(
          MaterialApp(
            theme: ThemeData(fontFamily: 'Roboto'),
            home: RepaintBoundary(
              key: boundary,
              child: PsatReader(
                key: ValueKey('$n-$size'),
                controller: c,
                question: q,
              ),
            ),
          ),
        );
        await t.pumpAndSettle();
        for (final table in q.tables) {
          final target = find.byKey(
            ValueKey('psat-table-${q.id}-${table["caption"]}'),
          );
          await t.scrollUntilVisible(
            target,
            400,
            scrollable: find.byType(Scrollable).first,
            maxScrolls: 100,
          );
          expect(t.getRect(target).right, lessThanOrEqualTo(size.width));
        }
        await t.pumpAndSettle();
        await t.runAsync(() async {
          final img =
              await (boundary.currentContext!.findRenderObject()!
                      as RenderRepaintBoundary)
                  .toImage(pixelRatio: 1.5);
          final bytes = await img.toByteData(format: ui.ImageByteFormat.png);
          final file = File(
            'artifacts/psat600_20261028/situation04/screens/q$n-${size.width.toInt()}.png',
          );
          file.parent.createSync(recursive: true);
          file.writeAsBytesSync(bytes!.buffer.asUint8List());
          img.dispose();
        });
        expect(t.takeException(), isNull, reason: '$n $size');
        await t.pumpWidget(const SizedBox());
      }
    }
    c.dispose();
  });
  testWidgets('all nine native situation tables fit cover and open widths', (
    t,
  ) async {
    t.view.devicePixelRatio = 1;
    addTearDown(t.view.resetDevicePixelRatio);
    addTearDown(t.view.resetPhysicalSize);
    final c = AppController(MemoryPersistence());
    var checked = 0;
    for (final size in [const Size(360, 840), const Size(752, 834)]) {
      t.view.physicalSize = size;
      for (final q in added.where((q) => q.tables.isNotEmpty)) {
        await t.pumpWidget(
          MaterialApp(
            theme: ThemeData(fontFamily: 'Roboto'),
            home: PsatReader(
              key: ValueKey('${q.id}-$size'),
              controller: c,
              question: q,
            ),
          ),
        );
        await t.pumpAndSettle();
        for (final table in q.tables) {
          final target = find.byKey(
            ValueKey('psat-table-${q.id}-${table["caption"]}'),
          );
          await t.scrollUntilVisible(
            target,
            350,
            scrollable: find.byType(Scrollable).first,
            maxScrolls: 100,
          );
          await t.pumpAndSettle();
          expect(target, findsOneWidget);
          final rect = t.getRect(target);
          expect(rect.left, greaterThanOrEqualTo(0));
          expect(rect.right, lessThanOrEqualTo(size.width));
          expect(t.takeException(), isNull, reason: q.id);
          checked++;
        }
        await t.pumpWidget(const SizedBox());
      }
    }
    expect(checked, 18);
    c.dispose();
  });
}
