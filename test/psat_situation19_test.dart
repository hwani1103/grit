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
        .singleWhere((s) => s.id == 'psat-situation-019')
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
  test('situation Set19 source keys, common passages, native tables and snapshot retention', () {
    expect(added.length,10);
    expect(added.map((q)=>q.number).toList(),[11,12,19,20,31,32,36,39,40,1]);
    expect(added.map((q)=>q.answer).toList(),[2,4,2,1,2,3,3,5,4,5]);
    for(final q in added) {
      expect(q.steps.length,5);expect(q.reasons.length,5);
      expect(PsatQuestion.fromJson(q.toJson()).toJson(),q.toJson());
      expect(File(q.original).lengthSync(),greaterThan(1000));
      expect(q.body.contains(RegExp(r'[\uE000-\uF8FF]')),isFalse);
    }
    expect(added[1].tables.single['rows'].length,3);
    expect(added[6].tables.single['rows'].length,5);
    expect(added[2].body,contains('μg/m^3'));
    expect(added[3].body,contains('(가) [빈칸]'));
    expect(added[7].body,startsWith('미국 복권의 역사'));
    expect(added[8].body,startsWith('미국 복권의 역사'));
    expect(added[6].steps[4],contains('④를 건수 차 때문에'));
  });
  testWidgets('situation Set19 special text fits cover and opened fold', (
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
        final needle=n==9?'국토교통부장관은 자동차정책기본계획':q.body.split('\n\n').first;
        final target=[1,6].contains(n)
          ? find.byKey(ValueKey('psat-table-${q.id}-${q.tables.last["caption"]}'))
          : find.byWidgetPredicate((w)=>w is PsatText && w.text.contains(needle));
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
            'artifacts/psat600_20261028/situation19/screens/q${q.number}-${size.width.toInt()}.png',
          );
          f.parent.createSync(recursive: true);
          f.writeAsBytesSync(b!.buffer.asUint8List());
          im.dispose();
        });
        expect(t.takeException(), isNull, reason: '$n $size');
        await t.pumpWidget(const SizedBox());
      }
    }
    c.dispose();
  });
}
