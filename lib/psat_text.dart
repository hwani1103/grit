import 'package:flutter/material.dart';

// Only Korean named labels are presentation markup; inequalities stay literal.
final _namedLabel = RegExp(r'<([가-힣][가-힣A-Za-z0-9 ·ㆍ()\-]{0,59})>');
final _listLabel = RegExp(r'^([ㄱㄴㄷㄹㅁㅂㅅ]\.|\([가나다라마바사아자차카타파하]\)|[○◯])\s+');
final _sectionLabel = RegExp(
  r'^<\s*(보\s*기|조\s*건|참\s*고|상\s*황|회\s*의|정\s*보|선정방식|입지조건|보고서|방송뉴스)\s*>',
);

// Dense law parsing requires a parenthesized title. Anonymous bare titles are
// bold only when explicitly stored as a whole block, never for inline references.
final _bareArticle = RegExp(r'^제[0-9○△□◇◯〇]+조(?:의[0-9]+)?$');
final _articleTitle = RegExp(
  r'제\s*[0-9○△□◇◯〇]+조(?:의[0-9]+)?\s*\((?:[^()\n]|\([^()\n]*\))*\)',
);
final _legalLabel = RegExp(r'^([①-⑳]|[1-9][0-9]?\.|[가나다라마바사아자차카타파하]\.)\s+');

List<String>? _legalReadingBlocks(String source) {
  if (_articleTitle.matchAsPrefix(source.trimLeft()) == null) return null;
  // Stop law formatting at a separate problem section or explicit footnote.
  final section = RegExp(
    r'<\s*(?:상\s*황|보\s*기|조\s*건|참\s*고)\s*>|\n\s*\n(?=※)',
  ).firstMatch(source);
  final law = source
      .substring(0, section?.start)
      .replaceAll(RegExp(r'\s+'), ' ')
      .trim();
  final result = <String>[];
  final titles = _articleTitle.allMatches(law).toList();
  for (var i = 0; i < titles.length; i++) {
    final title = titles[i];
    result.add(title.group(0)!);
    final content = law
        .substring(
          title.end,
          i + 1 < titles.length ? titles[i + 1].start : law.length,
        )
        .trim();
    final candidates = RegExp(
      r'(?<!\S)([①-⑳]|[1-9][0-9]?\.|[가나다라마바사아자차카타파하]\.)\s+',
    ).allMatches(content);
    var start = 0, clauseStart = 0;
    var numbered = false;
    for (final marker in candidates) {
      final label = marker.group(1)!;
      final before = content.substring(clauseStart, marker.start);
      // Quoted text is not a structural list. Current sources use paired quotes.
      final prefix = content.substring(0, marker.start);
      if (['“', '‘', '「', '『'].any((open) {
        const close = {'“': '”', '‘': '’', '「': '」', '『': '』'};
        return open.allMatches(prefix).length >
            close[open]!.allMatches(prefix).length;
      })) {
        continue;
      }
      if (RegExp(r'^[①-⑳]$').hasMatch(label)) {
        clauseStart = marker.end;
        numbered = false;
      } else if (RegExp(r'^[0-9]').hasMatch(label)) {
        // Definition articles enumerate terms after this introduction without
        // saying '각 호'. Keep those numbered definitions as separate items.
        final definedTerm =
            RegExp(r'(?:뜻은|정의는) 다음과 같다\.').hasMatch(before) &&
            content.substring(marker.end).startsWith('“');
        if (!before.contains('각 호') && !definedTerm) {
          continue;
        }
        numbered = true;
      } else if (!numbered) {
        continue;
      }
      final previous = content.substring(start, marker.start).trim();
      if (previous.isNotEmpty) result.add(previous);
      start = marker.start;
    }
    final last = content.substring(start).trim();
    if (last.isNotEmpty) result.add(last);
  }
  if (section != null) {
    result.addAll(psatReadingBlocks(source.substring(section.start)));
  }
  return result;
}

/// Break only dense named-label paragraphs, never inside quotes or brackets.
/// Source text and stored question snapshots are not modified.
List<String> psatReadingBlocks(String source) {
  final legal = _legalReadingBlocks(source);
  if (legal != null) return legal;
  final result = <String>[];
  final normalized = source.replaceAllMapped(
    RegExp(r'\n(?=(?:[ㄱㄴㄷㄹㅁㅂㅅ]\.|[○◯]|\([가나다라마바사아자차카타파하]\))\s)'),
    (_) => '\n\n',
  );
  for (final paragraph in normalized.split(RegExp(r'\n\s*\n'))) {
    if (paragraph.trim().isEmpty) continue;
    final section = _sectionLabel.matchAsPrefix(paragraph);
    if (section != null) {
      result.add(section.group(0)!);
      final tail = paragraph.substring(section.end).trim();
      if (tail.isNotEmpty) result.addAll(psatReadingBlocks(tail));
      continue;
    }
    if (_namedLabel.allMatches(paragraph).length < 3 ||
        _listLabel.hasMatch(paragraph)) {
      result.add(paragraph);
      continue;
    }
    var start = 0;
    final closing = <String>[];
    const pairs = {'<': '>', '(': ')', '“': '”', '‘': '’', '「': '」', '『': '』'};
    for (var i = 0; i < paragraph.length; i++) {
      final char = paragraph[i];
      if (closing.isNotEmpty && char == closing.last) {
        closing.removeLast();
      } else if (pairs.containsKey(char)) {
        closing.add(pairs[char]!);
      }
      if (closing.isEmpty &&
          i > 0 &&
          paragraph[i - 1] == '다' &&
          char == '.' &&
          i + 1 < paragraph.length &&
          RegExp(r'\s').hasMatch(paragraph[i + 1])) {
        result.add(paragraph.substring(start, i + 1).trim());
        start = i + 1;
      }
    }
    final tail = paragraph.substring(start).trim();
    if (tail.isNotEmpty) result.add(tail);
  }
  return result;
}

// Some Korean fonts omit superscript digits. Use unambiguous ASCII exponent
// notation for display, keeping the exact source glyphs in question snapshots.
String _displayExponents(String source) =>
    source.replaceAllMapped(RegExp(r'[⁺⁻]?[⁰¹²³⁴⁵⁶⁷⁸⁹]+'), (match) {
      final value = match.group(0)!;
      final sign = value.startsWith('⁻')
          ? '-'
          : value.startsWith('⁺')
          ? '+'
          : '';
      final digits = (sign.isEmpty ? value : value.substring(1))
          .split('')
          .map((c) => '⁰¹²³⁴⁵⁶⁷⁸⁹'.indexOf(c))
          .join();
      return sign.isEmpty ? '^$digits' : '^($sign$digits)';
    });

/// Preserve source emphasis while keeping display-only word joining separate.
List<TextSpan> psatInlineSpans(
  String text,
  List<String> underlines, {
  bool underlineLabelAnchors = false,
}) {
  final ranges = <(int, int)>[];
  for (final phrase in underlines) {
    if (phrase.isEmpty) continue;
    for (final match in RegExp(RegExp.escape(phrase)).allMatches(text)) {
      // A circled source label scopes a repeated phrase to its marked occurrence.
      // The label itself sits before the underline in the official passage.
      final labelLength =
          underlineLabelAnchors && RegExp(r'^[㉠-㉻]').hasMatch(phrase) ? 1 : 0;
      // A quoted label anchor identifies one occurrence while the source stroke
      // covers only the word inside the quotes (for example ㉠‘전이’).
      final quoteStart =
          phrase.length - phrase.substring(labelLength).trimLeft().length;
      final quotedAnchor =
          labelLength == 1 &&
          phrase.length > quoteStart + 2 &&
          ((phrase[quoteStart] == '‘' && phrase.endsWith('’')) ||
              (phrase[quoteStart] == '“' && phrase.endsWith('”')));
      ranges.add((
        match.start + (quotedAnchor ? quoteStart + 1 : labelLength),
        match.end - (quotedAnchor ? 1 : 0),
      ));
    }
  }
  final spans = <TextSpan>[];
  void add(int start, int end, [TextStyle? style]) {
    if (start >= end) return;
    final boundaries = <int>{start, end};
    for (final range in ranges) {
      if (range.$1 > start && range.$1 < end) boundaries.add(range.$1);
      if (range.$2 > start && range.$2 < end) boundaries.add(range.$2);
    }
    final cuts = boundaries.toList()..sort();
    for (var i = 0; i + 1 < cuts.length; i++) {
      final a = cuts[i], b = cuts[i + 1];
      final marked = ranges.any((r) => a >= r.$1 && b <= r.$2);
      spans.add(
        TextSpan(
          text: _displayExponents(text.substring(a, b)),
          style: marked
              ? (style ?? const TextStyle()).copyWith(
                  decoration: TextDecoration.underline,
                )
              : style,
        ),
      );
    }
  }

  var offset = 0;
  for (final match in _namedLabel.allMatches(text)) {
    add(offset, match.start);
    add(
      match.start + 1,
      match.end - 1,
      const TextStyle(fontWeight: FontWeight.w700),
    );
    offset = match.end;
  }
  add(offset, text.length);
  return spans;
}

class PsatText extends StatelessWidget {
  final String text;
  final TextStyle style;
  final List<String> underlines;
  final bool underlineLabelAnchors;
  const PsatText(
    this.text, {
    super.key,
    required this.style,
    this.underlines = const [],
    this.underlineLabelAnchors = false,
  });

  @override
  Widget build(BuildContext context) {
    final spans = psatInlineSpans(
      text,
      underlines,
      underlineLabelAnchors: underlineLabelAnchors,
    );
    return LayoutBuilder(
      builder: (context, constraints) {
        final effectiveStyle = DefaultTextStyle.of(context).style.merge(style);
        final display = TextSpan(children: spans).toPlainText();
        final wrapped = psatWordSpans(
          spans,
          style: effectiveStyle,
          width: constraints.maxWidth,
          scaler: MediaQuery.textScalerOf(context),
          direction: Directionality.of(context),
        );
        return Text.rich(
          TextSpan(children: wrapped),
          style: style,
          semanticsLabel: display,
        );
      },
    );
  }
}

class PsatPassage extends StatelessWidget {
  final String text;
  final double fontSize;
  final List<String> underlines;
  final bool underlineLabelAnchors;
  const PsatPassage(
    this.text, {
    super.key,
    required this.fontSize,
    this.underlines = const [],
    this.underlineLabelAnchors = false,
  });

  @override
  Widget build(BuildContext context) {
    final style = TextStyle(
      fontSize: fontSize,
      height: 1.75,
      fontWeight: FontWeight.w400,
    );
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        for (final block in psatReadingBlocks(text))
          Padding(
            padding: const EdgeInsets.only(bottom: 14),
            child: _block(block, style),
          ),
      ],
    );
  }

  Widget _block(String block, TextStyle style) {
    final article = _articleTitle.matchAsPrefix(block);
    if ((article != null && article.end == block.length) ||
        _bareArticle.hasMatch(block)) {
      return PsatText(
        block,
        style: style.copyWith(fontWeight: FontWeight.w700),
        underlines: underlines,
        underlineLabelAnchors: underlineLabelAnchors,
      );
    }
    final legal = _legalLabel.firstMatch(block);
    if (legal != null) {
      final marker = legal.group(1)!;
      final indent = RegExp(r'^[0-9]').hasMatch(marker)
          ? 12.0
          : RegExp(r'^[가-하]').hasMatch(marker)
          ? 24.0
          : 0.0;
      return PsatListItem(
        marker: marker,
        text: block.substring(legal.end),
        style: style,
        indent: indent,
        underlines: underlines,
        underlineLabelAnchors: underlineLabelAnchors,
      );
    }
    final section = _sectionLabel.firstMatch(block.trim());
    if (section != null) {
      return Padding(
        padding: const EdgeInsets.only(top: 8),
        child: Text(
          section.group(1)!.replaceAll(RegExp(r'\s'), ''),
          style: style.copyWith(fontWeight: FontWeight.w700),
        ),
      );
    }
    final label = _listLabel.firstMatch(block);
    if (label != null) {
      return PsatListItem(
        marker: label.group(1)!,
        text: block.substring(label.end),
        style: style,
        underlines: underlines,
        underlineLabelAnchors: underlineLabelAnchors,
      );
    }
    return PsatText(
      block,
      style: style,
      underlines: underlines,
      underlineLabelAnchors: underlineLabelAnchors,
    );
  }
}

/// Shared hanging indent for clauses, options, conditions and explanation steps.
class PsatListItem extends StatelessWidget {
  final String marker, text;
  final TextStyle style;
  final double indent;
  final List<String> underlines;
  final bool underlineLabelAnchors;
  const PsatListItem({
    super.key,
    required this.marker,
    required this.text,
    required this.style,
    this.indent = 0,
    this.underlines = const [],
    this.underlineLabelAnchors = false,
  });
  @override
  Widget build(BuildContext context) => Padding(
    padding: EdgeInsets.only(left: indent),
    child: Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(marker, style: style.copyWith(fontWeight: FontWeight.w400)),
        const SizedBox(width: 10),
        Expanded(
          child: PsatText(
            text,
            style: style,
            underlines: underlines,
            underlineLabelAnchors: underlineLabelAnchors,
          ),
        ),
      ],
    ),
  );
}

/// Keep whitespace-delimited Korean words together at the measured font size.
/// An overlong word keeps Flutter's normal character wrapping to avoid clipping.
List<TextSpan> psatWordSpans(
  List<TextSpan> spans, {
  required TextStyle style,
  required double width,
  required TextScaler scaler,
  required TextDirection direction,
}) {
  if (!width.isFinite || width <= 0) return spans;
  final source = spans.map((s) => s.text ?? '').join();
  final joins = <int>{};
  for (final word in RegExp(r'[^\s]+').allMatches(source)) {
    final token = word.group(0)!;
    if (!RegExp(r'[가-힣]').hasMatch(token)) continue;
    var offset = 0;
    final pieces = <TextSpan>[];
    for (final span in spans) {
      final text = span.text ?? '';
      final start = word.start > offset ? word.start - offset : 0;
      final end = word.end < offset + text.length
          ? word.end - offset
          : text.length;
      if (start < end) {
        pieces.add(
          TextSpan(text: text.substring(start, end), style: span.style),
        );
      }
      offset += text.length;
    }
    final painter = TextPainter(
      text: TextSpan(style: style, children: pieces),
      textDirection: direction,
      textScaler: scaler,
    )..layout();
    final fits = painter.width <= width;
    painter.dispose();
    if (!fits) continue;
    var position = word.start;
    for (final character in token.characters) {
      if (position > word.start) joins.add(position);
      position += character.length;
    }
  }
  var offset = 0;
  return [
    for (final span in spans)
      (() {
        final buffer = StringBuffer();
        for (final character in (span.text ?? '').characters) {
          if (joins.contains(offset)) buffer.write('\u2060');
          buffer.write(character);
          offset += character.length;
        }
        return TextSpan(text: buffer.toString(), style: span.style);
      })(),
  ];
}
