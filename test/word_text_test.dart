import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/word_text.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  setUpAll(() async {
    final font = FontLoader('WordTest')
      ..addFont(
        Future.value(
          ByteData.sublistView(
            File('C:/Windows/Fonts/malgun.ttf').readAsBytesSync(),
          ),
        ),
      );
    await font.load();
  });
  RenderParagraph paragraph(RenderObject root) {
    RenderParagraph? found;
    void visit(RenderObject value) {
      if (value is RenderParagraph) found = value;
      value.visitChildren(visit);
    }

    visit(root);
    return found!;
  }

  testWidgets(
    'UI words use actual width and resize safely including intrinsic dialogs',
    (t) async {
      for (final width in [130.0, 64.0, 130.0]) {
        await t.pumpWidget(
          MaterialApp(
            home: Center(
              child: SizedBox(
                width: width,
                child: const WordText(
                  '오늘 자료해석은 연습합니다.',
                  style: TextStyle(fontFamily: 'WordTest', fontSize: 19),
                ),
              ),
            ),
          ),
        );
        await t.pump();
        final render = paragraph(t.renderObject(find.byType(WordText)));
        final text = render.text.toPlainText();
        expect(text.replaceAll('\u2060', ''), '오늘 자료해석은 연습합니다.');
        final start = text.indexOf('자');
        final end = text.indexOf(' ', start);
        final rects = render.getBoxesForSelection(
          TextSelection(baseOffset: start, extentOffset: end),
        );
        if (width == 130) {
          expect(rects.length, 1);
          expect(rects.single.top, greaterThan(0));
        } else {
          expect(rects.length, greaterThan(1));
        }
        expect(t.takeException(), isNull);
      }
      await t.pumpWidget(
        const MaterialApp(
          home: Center(
            child: IntrinsicWidth(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  WordText('자료해석은 단어 단위로 읽습니다.'),
                  WordSelectableText('풀이 안내서에서도 같은 규칙을 씁니다.'),
                ],
              ),
            ),
          ),
        ),
      );
      await t.pumpAndSettle();
      expect(t.takeException(), isNull);
    },
  );
}
