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
        .singleWhere((s) => s.id == 'psat-verbal-006')
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
    'verbal Set6 preserves 2025 source, six underlines and process diagram',
    () {
      expect(added.length, 10);
      const keys = [1, 1, 3, 5, 2, 3, 4, 2, 3, 4];
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
      expect(added[6].underlines.length, 5);
      expect(added[8].underlines, ['필요한 자료']);
      expect(added[7].body, contains('(가) 사실을'));
      expect(added[7].body, contains('(나) 는 점을'));
      expect(added[9].figures.length, 1);
      expect(added[9].data['figuresAfterBody'], isTrue);
      expect(
        added.take(9).every((q) => q.data['figuresAfterBody'] != true),
        isTrue,
      );
      expect(added[3].body, contains('「모나리자」'));
      expect(added[5].body, contains('「외자도입촉진법」'));
    },
  );
  testWidgets('verbal Set6 source features fit cover and open screens', (
    t,
  ) async {
    t.view.devicePixelRatio = 1;
    addTearDown(t.view.resetDevicePixelRatio);
    addTearDown(t.view.resetPhysicalSize);
    final c = AppController(MemoryPersistence());
    for (final size in [const Size(360, 840), const Size(752, 834)]) {
      t.view.physicalSize = size;
      for (final n in [3, 5, 6, 7, 8, 9]) {
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
        if (n == 9) {
          final f = q.figures.single;
          await t.runAsync(() async {
            await precacheImage(
              AssetImage(f['asset'] as String),
              t.element(find.byType(PsatReader)),
            );
          });
          await t.pumpAndSettle();
          final target = find.byKey(ValueKey(f['asset']));
          await t.scrollUntilVisible(
            target,
            350,
            scrollable: find.byType(Scrollable).first,
            maxScrolls: 100,
          );
          await t.pumpAndSettle();
          final ims = t.widgetList<RawImage>(
            find.descendant(of: target, matching: find.byType(RawImage)),
          );
          expect(ims, isNotEmpty);
          expect(ims.every((im) => im.image != null), isTrue);
          final rect = t.getRect(target);
          final tail = find.byWidgetPredicate(
            (w) =>
                w is PsatText && w.text.contains('디지털 지우개 서비스의 진행 과정은 다음과 같다.'),
          );
          expect(t.getRect(tail).bottom, lessThanOrEqualTo(rect.top));
          expect(rect.left, greaterThanOrEqualTo(0));
          expect(rect.right, lessThanOrEqualTo(size.width));
        } else {
          final needle = {
            3: '「모나리자」',
            5: '1960년에',
            6: '㉣뒤의 해석',
            7: '저축률이 높았다. 사람들이 (나)',
            8: '㉠필요한 자료',
          }[n]!;
          if (n != 3) {
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
        }
        await t.runAsync(() async {
          final img =
              await (boundary.currentContext!.findRenderObject()!
                      as RenderRepaintBoundary)
                  .toImage(pixelRatio: 1.5);
          final bytes = await img.toByteData(format: ui.ImageByteFormat.png);
          final file = File(
            'artifacts/psat600_20261028/verbal06/screens/q$n-${size.width.toInt()}.png',
          );
          file.parent.createSync(recursive: true);
          file.writeAsBytesSync(bytes!.buffer.asUint8List());
          img.dispose();
        });
        if (n == 9) {
          final target = find.byKey(ValueKey(q.figures.single['asset']));
          final rect = t.getRect(target);
          await t.tapAt(
            Offset(rect.center.dx, rect.top.clamp(90, size.height - 100) + 20),
          );
          await t.pumpAndSettle();
          expect(find.byType(InteractiveViewer), findsOneWidget);
          await t.pageBack();
          await t.pumpAndSettle();
        }
        expect(t.takeException(), isNull, reason: '$n $size');
        await t.pumpWidget(const SizedBox());
      }
    }
    c.dispose();
  });
}
