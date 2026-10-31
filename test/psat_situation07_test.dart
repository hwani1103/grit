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
        .singleWhere((s) => s.id == 'psat-situation-007')
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
  test('situation Set7 preserves six tables, laws and paired choices', () {
    expect(added.length, 10);
    const keys = [5, 4, 3, 3, 4, 2, 1, 1, 2, 3];
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
    expect(added.fold<int>(0, (n, q) => n + q.tables.length), 6);
    expect(added[4].tables.single['rows'], [
      ['건강생활실천율(%)', '35', '30', '25', '30', '30'],
    ]);
    expect(added[5].tables.single['rows'].length, 3);
    expect(added[6].data['choiceNote'], contains('甲의 근무처·직위 → 丙의 근무처·직위'));
    expect(added[6].choices.every((c) => c.split(' / ').length == 2), isTrue);
    expect(added[7].tables.single['afterParagraph'], 5);
    expect(added[7].body, contains('붙박이장이 있는 경우 2.5억 원 이하)'));
    expect(added[8].tables.map((t) => t['afterParagraph']).toList(), [2, 3]);
    expect(added[9].tables.single['afterParagraph'], 10);
  });
  testWidgets('situation Set7 source features fit cover and open screens', (
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
        (1, -1),
        (2, -1),
        (4, 0),
        (5, 0),
        (7, 0),
        (8, 0),
        (8, 1),
        (9, 0),
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
            'artifacts/psat600_20261028/situation07/screens/q$n-t${sample.$2}-${size.width.toInt()}.png',
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
