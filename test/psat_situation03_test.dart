import 'dart:io';
import 'dart:ui' as ui;
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/psat.dart';
import 'package:grit/psat_model.dart';
import 'package:grit/psat_sets.dart';
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
              q.id.startsWith('kr-mpm-2024-07-27-psat-s-') &&
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
  test('situation Set3 preserves keys, all tables and source order', () {
    expect(added.length, 10);
    const keys = [1, 4, 3, 3, 5, 5, 2, 1, 3, 4];
    for (final q in added) {
      expect(q.answer, keys[q.number - 11]);
      expect(q.steps.length, 5);
      expect(q.reasons.length, 5);
      expect(PsatQuestion.fromJson(q.toJson()).toJson(), q.toJson());
      expect(File(q.original).lengthSync(), greaterThan(1000));
    }
    expect(added.first.body.split('제00조').length - 1, 3);
    expect(added[1].tables.single['rows'], [
      ['A', '보도자료', '2', '상'],
      ['B', '보도자료', '34', '중'],
      ['C', '보도자료', '5', '하'],
      ['D', '설명자료', '3', '상'],
    ]);
    expect(added[4].tables.single['rows'], [
      ['X', '1'],
      ['Y', '2'],
      ['Z', '4'],
      ['W', '3'],
    ]);
    expect(added[6].tables.single['afterParagraph'], 0);
    expect(added[6].tables.single['rows'].length, 10);
    expect(added[6].body.split('\n\n')[1], startsWith('만약 어떤 순위'));
    expect(added[9].tables.single['rows'].last, [
      'D',
      '33',
      '교육',
      '0.8',
      '5.0',
    ]);
  });
  testWidgets('situation Set3 law and four tables fit cover and open screens', (
    t,
  ) async {
    t.view.devicePixelRatio = 1;
    addTearDown(t.view.resetDevicePixelRatio);
    addTearDown(t.view.resetPhysicalSize);
    final c = AppController(MemoryPersistence());
    for (final size in [const Size(360, 840), const Size(752, 834)]) {
      t.view.physicalSize = size;
      for (final n in [11, 12, 15, 17, 20]) {
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
        if (q.tables.isNotEmpty) {
          final target = find.byKey(
            ValueKey('psat-table-${q.id}-${q.tables.single["caption"]}'),
          );
          await t.scrollUntilVisible(
            target,
            350,
            scrollable: find.byType(Scrollable).first,
            maxScrolls: 100,
          );
          expect(target, findsOneWidget);
        }
        await t.pumpAndSettle();
        await t.runAsync(() async {
          final img =
              await (boundary.currentContext!.findRenderObject()!
                      as RenderRepaintBoundary)
                  .toImage(pixelRatio: 1.5);
          final bytes = await img.toByteData(format: ui.ImageByteFormat.png);
          final file = File(
            'artifacts/psat600_20261028/situation03_2024/screens/q$n-${size.width.toInt()}.png',
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
