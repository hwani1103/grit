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
  late PsatCatalog catalog;
  late List<PsatQuestion> added;
  setUpAll(() async {
    catalog = await loadPsatCatalog();
    added = catalog.questions.values
        .where(
          (q) => q.id.startsWith('kr-mpm-2024-07-27-psat-s-') && q.number <= 10,
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
  test(
    '2024 situation official key and complete shared passage survive snapshots',
    () {
      // Official final notice 4564, PDF page 2, subject 상황판단, book 사.
      const answers = [5, 5, 2, 4, 1, 2, 4, 4, 2, 3];
      expect(added.length, 10);
      for (final q in added) {
        expect(q.answer, answers[q.number - 1]);
        expect(q.data['book'], '사');
        expect(q.steps.length, greaterThanOrEqualTo(3));
        expect(q.reasons.length, 5);
        expect(File(q.original).lengthSync(), greaterThan(1000));
        expect(PsatQuestion.fromJson(q.toJson()).toJson(), q.toJson());
      }
      expect(
        added[8].body.split('\n\n<보기>').first,
        added[9].body.split('\n\n<상황>').first,
      );
      expect(added[9].body, contains('2⁵⁶개의 키'));
      expect(
        TextSpan(
          children: psatInlineSpans('2⁸=256, 2⁵⁶, 2¹⁰⁰', const []),
        ).toPlainText(),
        '2^8=256, 2^56, 2^100',
      );
      expect(
        TextSpan(children: psatInlineSpans('2⁵⁶', const ['2⁵⁶'])).toPlainText(),
        '2^56',
      );
      expect(
        psatInlineSpans('2⁵⁶', const ['2⁵⁶']).single.style?.decoration,
        TextDecoration.underline,
      );

      expect(added[9].body, contains('2⁸, 즉 256개'));
      expect(added[9].body, contains('2¹⁰⁰개'));
      expect(added[5].tables.single['rows'], [
        ['甲', '□5701'],
        ['乙', '84□98'],
        ['丙', '83□□4'],
        ['丁', '□6715'],
      ]);
      expect(
        catalog.sets
            .singleWhere((s) => s.id == 'psat-situation-002')
            .questionIds,
        added.map((q) => q.id).toList(),
      );
      for (final bad in [-1, 3, 0.5, '1']) {
        final data = added[7].toJson();
        data['tables'][0]['afterParagraph'] = bad;
        expect(() => PsatQuestion.fromJson(data), throwsFormatException);
      }
      // Older saved questions need no insertion metadata and retain the same JSON.
      final legacy = catalog.questions.values.firstWhere(
        (q) => q.id == '2023-07-22-s-08',
      );
      expect(PsatQuestion.fromJson(legacy.toJson()).toJson(), legacy.toJson());
    },
  );

  Future<void> capture(WidgetTester t, GlobalKey boundary, String label) async {
    await t.runAsync(() async {
      final image =
          await (boundary.currentContext!.findRenderObject()!
                  as RenderRepaintBoundary)
              .toImage(pixelRatio: 1.5);
      final bytes = await image.toByteData(format: ui.ImageByteFormat.png);
      final file = File(
        'artifacts/psat600_20261028/situation02_2024/screens/$label.png',
      );
      file.parent.createSync(recursive: true);
      file.writeAsBytesSync(bytes!.buffer.asUint8List());
      image.dispose();
    });
  }

  Finder proseWith(String part) =>
      find.byWidgetPredicate((w) => w is PsatText && w.text.contains(part));
  testWidgets(
    'table source order, anonymous articles and exponents remain readable after resizing',
    (t) async {
      t.view.devicePixelRatio = 1;
      addTearDown(t.view.resetDevicePixelRatio);
      addTearDown(t.view.resetPhysicalSize);
      final c = AppController(MemoryPersistence());
      for (final size in [
        const Size(360, 840),
        const Size(752, 834),
        const Size(320, 640),
      ]) {
        t.view.physicalSize = size;
        for (final n in [1, 6, 7, 8, 10]) {
          final q = added[n - 1];
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
          expect(t.takeException(), isNull);
          if (n == 1) {
            final articles = t
                .widgetList<PsatText>(proseWith('제00조'))
                .where((w) => w.text == '제00조')
                .toList();
            expect(articles.length, 3);
            expect(
              articles.every((w) => w.style.fontWeight == FontWeight.w700),
              isTrue,
            );
            final citations = t
                .widgetList<PsatText>(proseWith('제1항'))
                .where((w) => w.text != '제00조');
            expect(
              citations.every((w) => w.style.fontWeight != FontWeight.w700),
              isTrue,
            );
          }
          if (n == 7) {
            final table = find.byKey(ValueKey('psat-table-${q.id}-공의 색·무게·개수'));
            expect(
              t.getTopLeft(proseWith('각 상자에는 100g')).dy,
              greaterThanOrEqualTo(t.getBottomLeft(table).dy),
            );
            expect(
              t.getTopLeft(table).dy,
              greaterThan(t.getTopLeft(proseWith('甲은 아래')).dy),
            );
          }
          if (n == 8) {
            final table1 = find.byKey(ValueKey('psat-table-${q.id}-작품별 현황'));
            final table2 = find.byKey(ValueKey('psat-table-${q.id}-점수 가감 기준'));
            expect(
              t.getTopLeft(proseWith('최종점수는 작품별')).dy,
              greaterThanOrEqualTo(t.getBottomLeft(table1).dy),
            );
            expect(
              t.getTopLeft(proseWith('최종점수가 75점')).dy,
              greaterThanOrEqualTo(t.getBottomLeft(table2).dy),
            );
          }
          await capture(
            t,
            boundary,
            'q${n.toString().padLeft(2, '0')}-${size.width.toInt()}',
          );
          if (n == 10) {
            await t.ensureVisible(proseWith('2⁵⁶개의 키').first);
            await t.pumpAndSettle();
            expect(t.takeException(), isNull);
            await capture(t, boundary, 'q10-exponent-${size.width.toInt()}');
          }
          if (n == 8) {
            await t.ensureVisible(
              find.byKey(ValueKey('psat-table-${q.id}-점수 가감 기준')),
            );
            await t.pumpAndSettle();
            expect(t.takeException(), isNull);
            await capture(t, boundary, 'q08-criteria-${size.width.toInt()}');
          }
        }
      }
      await t.pumpWidget(const SizedBox());
      c.dispose();
    },
  );
}
