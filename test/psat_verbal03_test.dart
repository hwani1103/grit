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
    added = catalog.questions.values
        .where(
          (q) =>
              q.id.startsWith('kr-mpm-2024-07-27-psat-l-') &&
              q.number >= 11 &&
              q.number <= 20,
        )
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
  test('verbal Set3 preserves shared source, underlines, blank and table', () {
    expect(added.length, 10);
    const keys = [2, 3, 2, 4, 1, 2, 5, 5, 3, 3];
    for (final q in added) {
      expect(q.answer, keys[q.number - 11]);
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
    expect(added[3].body, contains('조금 전 확인된 바로, □.'));
    expect(added[7].tables.single['rows'], [
      ['I', '○', '○', '×', '×'],
      ['II', '×', '○', '×', '○'],
    ]);
    final common = added[8].body.split('\n\n<보기>')[0];
    expect(common, added[9].body.split('\n\n<보기>')[0]);
    expect(common, contains('철학자 B는'));
    expect(common, contains('말할 수 있다.'));
  });
  testWidgets('verbal Set3 source features fit cover and open screens', (
    t,
  ) async {
    t.view.devicePixelRatio = 1;
    addTearDown(t.view.resetDevicePixelRatio);
    addTearDown(t.view.resetPhysicalSize);
    final c = AppController(MemoryPersistence());
    for (final size in [const Size(360, 840), const Size(752, 834)]) {
      t.view.physicalSize = size;
      for (final n in [11, 14, 18, 19]) {
        final q = added.firstWhere((q) => q.number == n);
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
        if (n == 14) {
          final target = find.byWidgetPredicate(
            (w) => w is PsatText && w.text.contains('조금 전 확인된 바로, □.'),
          );
          await t.scrollUntilVisible(
            target,
            400,
            scrollable: find.byType(Scrollable).first,
            maxScrolls: 100,
          );
        }
        if (n == 18) {
          final target = find.byKey(
            ValueKey('psat-table-${q.id}-${q.tables.single["caption"]}'),
          );
          await t.scrollUntilVisible(
            target,
            400,
            scrollable: find.byType(Scrollable).first,
            maxScrolls: 100,
          );
        }
        if (n == 19) {
          final target = find.byWidgetPredicate(
            (w) => w is PsatText && w.text.startsWith('의무론 논제'),
          );
          await t.scrollUntilVisible(
            target,
            400,
            scrollable: find.byType(Scrollable).first,
            maxScrolls: 100,
          );
        }
        await t.pumpAndSettle();
        await t.runAsync(() async {
          final img =
              await (boundary.currentContext!.findRenderObject()!
                      as RenderRepaintBoundary)
                  .toImage(pixelRatio: 1.5);
          final bytes = await img.toByteData(format: ui.ImageByteFormat.png);
          final file = File(
            'artifacts/psat600_20261028/verbal03_2024/screens/q$n-${size.width.toInt()}.png',
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
