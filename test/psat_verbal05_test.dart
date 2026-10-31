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
        .singleWhere((s) => s.id == 'psat-verbal-005')
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
    'verbal Set5 preserves mixed years, shared source, underlines and two tables',
    () {
      expect(added.length, 10);
      const keys = [2, 1, 3, 3, 4, 1, 3, 1, 5, 2];
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
      expect(added[6].body, contains('공리주의에 따르면'));
      expect(added[6].body, contains('현세대도 미래세대가 겪는 고통에 대해'));
      expect(added[5].tables.single['afterParagraph'], 1);
      expect(added[5].body.split('\n\n')[2], startsWith('다만 장애인'));
      expect(added[7].tables.single['rows'], [
        ['A', '㉠', '㉡', '㉢', '㉣'],
        ['B', '㉤', '㉥', '㉦', '㉧'],
      ]);
      expect(added[7].tables.single['afterParagraph'], 3);
      expect(added[8].body, contains('갑: 예, 그러면 □.'));
      expect(added[9].body, contains('제4조(지원대상)\n\n①'));
    },
  );
  testWidgets('verbal Set5 source features fit cover and open screens', (
    t,
  ) async {
    t.view.devicePixelRatio = 1;
    addTearDown(t.view.resetDevicePixelRatio);
    addTearDown(t.view.resetPhysicalSize);
    final c = AppController(MemoryPersistence());
    for (final size in [const Size(360, 840), const Size(752, 834)]) {
      t.view.physicalSize = size;
      for (final n in [4, 5, 6, 7, 8, 9]) {
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
        if (n == 5 || n == 7) {
          final target = find.byKey(
            ValueKey('psat-table-${q.id}-${q.tables.single["caption"]}'),
          );
          await t.scrollUntilVisible(
            target,
            350,
            scrollable: find.byType(Scrollable).first,
            maxScrolls: 100,
          );
        } else {
          final needle = {
            4: '㉠오늘 회의',
            6: '㉠이는 수용',
            8: '갑: 예, 그러면',
            9: '교복 구입비 지원 대상은 B시에',
          }[n]!;
          final target = find.byWidgetPredicate(
            (w) => w is PsatText && w.text.contains(needle),
          );
          await t.scrollUntilVisible(
            target,
            350,
            scrollable: find.byType(Scrollable).first,
            maxScrolls: 100,
          );
        }
        await t.pumpAndSettle();
        if (n == 9) {
          await t.drag(find.byType(Scrollable).first, const Offset(0, 150));
          await t.pumpAndSettle();
        }
        await t.runAsync(() async {
          final img =
              await (boundary.currentContext!.findRenderObject()!
                      as RenderRepaintBoundary)
                  .toImage(pixelRatio: 1.5);
          final bytes = await img.toByteData(format: ui.ImageByteFormat.png);
          final file = File(
            'artifacts/psat600_20261028/verbal05/screens/q$n-${size.width.toInt()}.png',
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
}
