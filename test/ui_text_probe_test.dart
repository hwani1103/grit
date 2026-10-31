import 'dart:convert';
import 'dart:io';
import 'dart:ui' as ui;
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/psat_text.dart';
import 'package:grit/word_text.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  testWidgets('diagnose punctuation and word layout without changing source', (
    t,
  ) async {
    for (final family in ['Roboto', 'Ahem']) {
      await (FontLoader(family)..addFont(
            Future.value(
              ByteData.sublistView(
                File('C:/Windows/Fonts/malgun.ttf').readAsBytesSync(),
              ),
            ),
          ))
          .load();
    }
    final out = Directory('artifacts/ui_ux_audit_20261031')
      ..createSync(recursive: true);
    final data = <Map<String, Object?>>[];
    for (final source in [
      '어느 쪽이 더 클까요?',
      '큰 것부터 차례로 탭하세요.',
      '오늘도, 한 걸음.',
      'GRIT.',
    ]) {
      for (final spacing in [0.0, -.7, -1.2]) {
        for (final joined in [false, true]) {
          const width = 350.0;
          final style = TextStyle(
            fontFamily: 'Roboto',
            fontSize: 23,
            fontWeight: FontWeight.w800,
            letterSpacing: spacing,
          );
          final span = TextSpan(
            style: style,
            children: joined
                ? psatWordSpans(
                    [TextSpan(text: source)],
                    style: style,
                    width: width,
                    scaler: TextScaler.noScaling,
                    direction: TextDirection.ltr,
                  )
                : [TextSpan(text: source)],
          );
          final painter = TextPainter(
            text: span,
            textDirection: TextDirection.ltr,
          )..layout(maxWidth: width);
          final display = span.toPlainText();
          final end = painter.getBoxesForSelection(
            TextSelection(
              baseOffset: display.length - 1,
              extentOffset: display.length,
            ),
          );
          data.add({
            'source': source,
            'spacing': spacing,
            'joined': joined,
            'width': painter.width,
            'lines': painter.computeLineMetrics().length,
            'lastBox': end
                .map((b) => [b.left, b.top, b.right, b.bottom])
                .toList(),
          });
          painter.dispose();
        }
      }
    }
    final key = GlobalKey();
    await t.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: Center(
            child: RepaintBoundary(
              key: key,
              child: ColoredBox(
                color: Colors.white,
                child: SizedBox(
                  width: 350,
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      for (final spacing in [0.0, -.7, -1.2]) ...[
                        WordText(
                          '어느 쪽이 더 클까요?',
                          style: TextStyle(
                            fontSize: 23,
                            fontWeight: FontWeight.w800,
                            letterSpacing: spacing,
                          ),
                        ),
                        Text(
                          '어느 쪽이 더 클까요?',
                          style: TextStyle(
                            fontSize: 23,
                            fontWeight: FontWeight.w800,
                            letterSpacing: spacing,
                          ),
                        ),
                        const SizedBox(height: 12),
                      ],
                    ],
                  ),
                ),
              ),
            ),
          ),
        ),
      ),
    );
    await t.pumpAndSettle();
    final boundary =
        key.currentContext!.findRenderObject()! as RenderRepaintBoundary;
    await t.runAsync(() async {
      final img = await boundary.toImage(pixelRatio: 3);
      final png = await img.toByteData(format: ui.ImageByteFormat.png);
      File(
        '${out.path}/punctuation-probe.png',
      ).writeAsBytesSync(png!.buffer.asUint8List());
      img.dispose();
    });
    File(
      '${out.path}/punctuation-probe.json',
    ).writeAsStringSync(const JsonEncoder.withIndent('  ').convert(data));
    await t.pumpWidget(const SizedBox());
    expect(t.takeException(), isNull);
  });
}
