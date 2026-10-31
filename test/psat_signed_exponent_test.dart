import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/psat_text.dart';

void main() {
  test(
    'inverse units retain the negative sign inside their displayed exponent',
    () {
      const source = '1,590cm⁻¹; x⁻¹²; y⁺²; 2⁵⁶; 10⁰';
      final plain = TextSpan(
        children: psatInlineSpans(source, const []),
      ).toPlainText();
      expect(plain, '1,590cm^(-1); x^(-12); y^(+2); 2^56; 10^0');
    },
  );
  test('emphasis around an inverse unit survives display conversion', () {
    final spans = psatInlineSpans('파수 300cm⁻¹ 이하', const ['300cm⁻¹']);
    final marked = spans
        .where((s) => s.style?.decoration == TextDecoration.underline)
        .single;
    expect(marked.text, '300cm^(-1)');
    expect(TextSpan(children: spans).toPlainText(), '파수 300cm^(-1) 이하');
  });
}
