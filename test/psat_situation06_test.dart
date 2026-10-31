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
        .singleWhere((s) => s.id == 'psat-situation-006')
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
  test('situation Set6 preserves shared source and four tables', () {
    expect(added.length, 10);
    const keys = [1, 1, 2, 2, 5, 1, 2, 5, 3, 4];
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
    expect(added[6].tables.single['rows'], [
      ['문항 개수', '2', '0', '3', '5', '5'],
    ]);
    expect(added[6].data['choiceNote'], contains('16번 → 17번'));
    expect(added[7].tables.single['afterParagraph'], 4);
    for (final i in [8, 9]) {
      expect(added[i].body, contains('소득에 관계없이'));
      expect(added[i].body, contains('본인부담금이 발생하지 않는다.'));
    }
    expect(added[9].tables.map((t) => t['afterParagraph']).toList(), [5, 6]);
    expect(added[9].tables[0]['rows'].length, 7);
    expect(added[9].tables[1]['rows'].length, 3);
  });
  testWidgets('situation Set6 source features fit cover and open screens', (
    t,
  ) async {
    t.view.devicePixelRatio = 1;
    addTearDown(t.view.resetDevicePixelRatio);
    addTearDown(t.view.resetPhysicalSize);
    final c = AppController(MemoryPersistence());
    for (final size in [const Size(360, 840), const Size(752, 834)]) {
      t.view.physicalSize = size;
      for (final sample in [
        (0, -1),
        (3, -1),
        (5, -1),
        (6, 0),
        (7, 0),
        (9, 0),
        (9, 1),
      ]) {
        final n = sample.$1;
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
        if (sample.$2 >= 0) {
          final table = q.tables[sample.$2];
          final target = find.byKey(
            ValueKey('psat-table-${q.id}-${table["caption"]}'),
          );
          await t.scrollUntilVisible(
            target,
            350,
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
            'artifacts/psat600_20261028/situation06/screens/q$n-t${sample.$2}-${size.width.toInt()}.png',
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
