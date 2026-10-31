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
    final c = await loadPsatCatalog();
    added = c.sets
        .singleWhere((s) => s.id == 'psat-verbal-019')
        .questionIds
        .map((id) => c.questions[id]!)
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
    'verbal Set19 preserves two original emphases, alpha, blank and book title',
    () {
      expect(added.length, 10);
      expect(added.map((q) => q.answer).toList(), [
        5,
        5,
        4,
        5,
        4,
        1,
        2,
        2,
        1,
        4,
      ]);
      expect(added.map((q) => q.number).toList(), [
        11,
        12,
        21,
        22,
        23,
        24,
        36,
        37,
        38,
        1,
      ]);
      for (final q in added) {
        expect(q.steps.length, 5);
        expect(q.reasons.length, 5);
        expect(PsatQuestion.fromJson(q.toJson()).toJson(), q.toJson());
        expect(File(q.original).lengthSync(), greaterThan(1000));
      }
      expect(added[1].body, contains('[빈칸]'));
      expect(added[7].body, contains('α 경로'));
      expect(added[7].choices.every((c) => !c.contains('\ue09d')), isTrue);
      expect(added[9].body, contains('『경국대전』'));
      for (final n in [6, 8]) {
        expect(added[n].body, isNotEmpty);
        expect(added[n].figures, isEmpty);
        expect(added[n].underlines.length, 1);
      }
    },
  );
  testWidgets('verbal Set19 special text fits cover and opened fold', (
    t,
  ) async {
    t.view.devicePixelRatio = 1;
    addTearDown(t.view.resetDevicePixelRatio);
    addTearDown(t.view.resetPhysicalSize);
    final c = AppController(MemoryPersistence());
    for (final size in [const Size(360, 840), const Size(752, 834)]) {
      t.view.physicalSize = size;
      for (final n in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]) {
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
        if (q.figures.isNotEmpty) {
          await t.runAsync(() async {
            for (final f in q.figures) {
              await precacheImage(
                AssetImage(f['asset'] as String),
                t.element(find.byType(PsatReader)),
              );
            }
          });
          await t.pumpAndSettle();
        }
        final needle = {
          0: '토양에 영양분이 충분한',
          1: '그런데 [빈칸]',
          2: '이 외에도 서운관',
          3: '법원의 허가를 받아야만 성명을',
          4: '합의된 계획에 따라',
          5: '지역 공동체가 빈곤층을 부양할',
          6: '연구자들은 이 이론이',
          7: 'α 경로를 통한 자극과',
          8: '기름방울은 중력에 의해',
          9: '『경국대전』',
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
        await t.pumpAndSettle();
        expect(target, findsOneWidget);
        final r = t.getRect(target);
        expect(r.left, greaterThanOrEqualTo(0));
        expect(r.right, lessThanOrEqualTo(size.width));
        await t.runAsync(() async {
          final im =
              await (boundary.currentContext!.findRenderObject()!
                      as RenderRepaintBoundary)
                  .toImage(pixelRatio: 1.5);
          final b = await im.toByteData(format: ui.ImageByteFormat.png);
          final f = File(
            'artifacts/psat600_20261028/verbal19/screens/q${q.number}-${size.width.toInt()}.png',
          );
          f.parent.createSync(recursive: true);
          f.writeAsBytesSync(b!.buffer.asUint8List());
          im.dispose();
        });
        if (q.figures.isNotEmpty) {
          final images = t.widgetList<RawImage>(
            find.descendant(of: target, matching: find.byType(RawImage)),
          );
          expect(images, isNotEmpty);
          expect(images.every((im) => im.image != null), isTrue);
          await t.tapAt(
            Offset(r.center.dx, r.top.clamp(90, size.height - 100) + 20),
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
