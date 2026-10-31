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
        .singleWhere((s) => s.id == 'psat-situation-005')
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
    'situation Set5 preserves sources, law blocks, shared passage and costs',
    () {
      expect(added.length, 10);
      const keys = [2, 5, 4, 5, 1, 5, 2, 4, 3, 5];
      for (var i = 0; i < added.length; i++) {
        final q = added[i];
        expect(q.answer, keys[i]);
        expect(q.steps.length, 5);
        expect(q.reasons.length, 5);
        expect(PsatQuestion.fromJson(q.toJson()).toJson(), q.toJson());
      }
      for (final i in [0, 1, 9]) {
        final blocks = psatReadingBlocks(added[i].body);
        expect(blocks.any((b) => RegExp(r'^제.+조\(.+\)$').hasMatch(b)), isTrue);
        expect(blocks.any((b) => b.startsWith('② ')), isTrue);
      }
      expect(added[3].tables.single['rows'], hasLength(5));
      expect(added[3].tables.single['afterParagraph'], 4);
      for (final i in [4, 5]) {
        expect(added[i].body, contains('천연향료는 다양한 방법'));
        expect(added[i].body, contains('부향률이 20～30%'));
      }
      expect(added[5].steps.join(), contains('乙의 종류를 확정할 필요는 없다'));
      expect(added[8].body, contains('㉠ 사이였다.'));
    },
  );
  testWidgets('situation Set5 law table shared text and puzzles fit two widths', (
    t,
  ) async {
    t.view.devicePixelRatio = 1;
    addTearDown(t.view.resetDevicePixelRatio);
    addTearDown(t.view.resetPhysicalSize);
    final c = AppController(MemoryPersistence());
    for (final size in [const Size(360, 840), const Size(752, 834)]) {
      t.view.physicalSize = size;
      for (final n in [0, 3, 5, 6, 8, 9]) {
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
        if (n == 3) {
          await t.scrollUntilVisible(
            find.byKey(
              ValueKey('psat-table-${q.id}-${q.tables.single["caption"]}'),
            ),
            350,
            scrollable: find.byType(Scrollable).first,
            maxScrolls: 100,
          );
        } else {
          final needle = {
            0: '제00조(천문역법)',
            5: '<대화>',
            6: '엘리베이터 안에는',
            8: '시계수리공 甲은',
            9: '제△△조(복지 급여 등)',
          }[n]!;
          final target = find.byWidgetPredicate(
            (w) =>
                w is PsatText &&
                ([0, 5, 9].contains(n)
                    ? w.text == needle
                    : w.text.contains(needle)),
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
            'artifacts/psat600_20261028/situation05/screens/q$n-${size.width.toInt()}.png',
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
