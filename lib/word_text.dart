import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'psat_text.dart' show psatWordSpans;

/// Plain UI text. Source strings and accessibility labels are never rewritten.
class WordText extends Text {
  const WordText(
    super.data, {
    super.key,
    super.style,
    super.textAlign,
    super.maxLines,
    super.overflow,
    super.softWrap,
    super.semanticsLabel,
  });
  @override
  Widget build(BuildContext context) {
    final defaults = DefaultTextStyle.of(context);
    var effective = defaults.style.merge(style);
    if (MediaQuery.boldTextOf(context)) {
      effective = effective.merge(const TextStyle(fontWeight: FontWeight.bold));
    }
    return Semantics(
      label: semanticsLabel ?? data,
      excludeSemantics: true,
      child: _WordParagraphWidget(
        source: TextSpan(text: data, style: effective),
        alignment: textAlign ?? defaults.textAlign ?? TextAlign.start,
        direction: Directionality.of(context),
        scaler: MediaQuery.textScalerOf(context),
        wrapping: softWrap ?? defaults.softWrap,
        clipping: overflow ?? defaults.overflow,
        lines: maxLines ?? defaults.maxLines,
        registrar: SelectionContainer.maybeOf(context),
        selection: DefaultSelectionStyle.of(context).selectionColor,
      ),
    );
  }
}

class WordSelectableText extends StatelessWidget {
  final String data;
  final TextStyle? style;
  const WordSelectableText(this.data, {super.key, this.style});
  @override
  Widget build(BuildContext context) =>
      SelectionArea(child: WordText(data, style: style));
}

class _WordParagraphWidget extends LeafRenderObjectWidget {
  final TextSpan source;
  final TextAlign alignment;
  final TextDirection direction;
  final TextScaler scaler;
  final bool wrapping;
  final TextOverflow clipping;
  final int? lines;
  final SelectionRegistrar? registrar;
  final Color? selection;
  const _WordParagraphWidget({
    required this.source,
    required this.alignment,
    required this.direction,
    required this.scaler,
    required this.wrapping,
    required this.clipping,
    required this.lines,
    this.registrar,
    this.selection,
  });
  @override
  _WordParagraph createRenderObject(BuildContext context) => _WordParagraph(
    source,
    textAlign: alignment,
    textDirection: direction,
    textScaler: scaler,
    softWrap: wrapping,
    overflow: clipping,
    maxLines: lines,
    registrar: registrar,
    selectionColor: selection,
  );
  @override
  void updateRenderObject(BuildContext context, _WordParagraph renderObject) {
    renderObject
      ..source = source
      ..textAlign = alignment
      ..textDirection = direction
      ..textScaler = scaler
      ..softWrap = wrapping
      ..overflow = clipping
      ..maxLines = lines
      ..registrar = registrar
      ..selectionColor = selection;
  }
}

/// Measure at the actual render width, including intrinsic-size dialog/button layouts.
class _WordParagraph extends RenderParagraph {
  TextSpan _source;
  // Intrinsic sizing, dry layout and normal layout often ask for the same
  // wrapping. Keep a small per-paragraph cache instead of shaping every word
  // again on each answer tap or parent rebuild.
  final _wrapped = <(TextSpan, double, TextScaler, TextDirection), TextSpan>{};
  _WordParagraph(
    super.text, {
    super.textAlign,
    required super.textDirection,
    super.textScaler,
    super.softWrap,
    super.overflow,
    super.maxLines,
    super.registrar,
    super.selectionColor,
  }) : _source = text as TextSpan;
  set source(TextSpan value) {
    if (_source == value) return;
    _source = value;
    _wrapped.clear();
    markNeedsLayout();
    markNeedsSemanticsUpdate();
  }

  TextSpan wrapped(double width) {
    final key = (_source, width, textScaler, textDirection);
    final cached = _wrapped[key];
    if (cached != null) return cached;
    final result = TextSpan(
      style: _source.style,
      children: psatWordSpans(
        [TextSpan(text: _source.text)],
        style: _source.style!,
        width: width,
        scaler: textScaler,
        direction: textDirection,
      ),
    );
    if (_wrapped.length >= 4) _wrapped.clear();
    _wrapped[key] = result;
    return result;
  }

  TextPainter measure(double width) =>
      TextPainter(
        text: wrapped(width.isFinite ? width : double.maxFinite),
        textAlign: textAlign,
        textDirection: textDirection,
        textScaler: textScaler,
        maxLines: maxLines,
        ellipsis: overflow == TextOverflow.ellipsis ? '…' : null,
      )..layout(
        maxWidth: softWrap || overflow == TextOverflow.ellipsis
            ? width
            : double.infinity,
      );
  @override
  void performLayout() {
    invokeLayoutCallback<BoxConstraints>((box) {
      super.text = wrapped(box.maxWidth);
    });
    super.performLayout();
  }

  @override
  Size computeDryLayout(BoxConstraints constraints) {
    final painter = measure(constraints.maxWidth);
    final result = constraints.constrain(painter.size);
    painter.dispose();
    return result;
  }

  double intrinsic(double width, {bool minimum = false, bool height = false}) {
    final painter = measure(width);
    final result = height
        ? painter.height
        : minimum
        ? painter.minIntrinsicWidth
        : painter.maxIntrinsicWidth;
    painter.dispose();
    return result;
  }

  @override
  double computeMinIntrinsicWidth(double height) =>
      intrinsic(double.infinity, minimum: true);
  @override
  double computeMaxIntrinsicWidth(double height) => intrinsic(double.infinity);
  @override
  double computeMinIntrinsicHeight(double width) =>
      intrinsic(width, height: true);
  @override
  double computeMaxIntrinsicHeight(double width) =>
      intrinsic(width, height: true);
}

// Shared word layout verified for intrinsic and bounded containers.
