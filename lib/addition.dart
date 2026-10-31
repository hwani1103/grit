import 'word_text.dart';
import 'dart:math';
import 'package:flutter/material.dart';
import 'main.dart';
import 'model.dart';

/// A complete table and numeric pad, without nested scrolling or a system IME.
class AdditionExercise extends StatefulWidget {
  final Problem problem;
  final int index;
  final PracticeSession session;
  final void Function(String, String) onAnswer;
  final void Function(String, String) onMemo;
  final VoidCallback? previous;
  final VoidCallback next;
  final bool last;
  final bool busy;
  const AdditionExercise({
    super.key,
    required this.problem,
    required this.index,
    required this.session,
    required this.onAnswer,
    required this.onMemo,
    this.previous,
    required this.next,
    required this.last,
    required this.busy,
  });
  @override
  State<AdditionExercise> createState() => _AdditionExerciseState();
}

class _AdditionExerciseState extends State<AdditionExercise> {
  late int selected;
  bool replace = true;
  String? selectedMemo;
  static const memoSurface = Color(0xFFEAF1F8);
  static const memoInk = Color(0xFF365D81);
  Problem get p => widget.problem;
  String get answer => selectedMemo != null
      ? widget.session.memos[selectedMemo] ?? ''
      : widget.session.answers[p.answerKey(widget.index, selected)] ?? '';
  @override
  void initState() {
    super.initState();
    selected = p.hidden.firstWhere(
      (cell) => !widget.session.hasAnswer(p.answerKey(widget.index, cell)),
      orElse: () => p.hidden.first,
    );
  }

  void choose(int cell) => setState(() {
    selected = cell;
    selectedMemo = null;
    replace = true;
  });
  void input(String value) {
    var text = answer;
    if (value == 'back') {
      if (text.isNotEmpty) text = text.substring(0, text.length - 1);
      replace = false;
    } else if (value == 'clear') {
      text = '';
      replace = true;
    } else if (value == 'sign') {
      text = text.startsWith('-') ? text.substring(1) : '-$text';
      replace = false;
    } else {
      text = replace ? value : text + value;
      if (text.replaceAll('-', '').length > 6) return;
      replace = false;
    }
    if (selectedMemo != null) {
      widget.onMemo(selectedMemo!, text);
    } else {
      widget.onAnswer(p.answerKey(widget.index, selected), text);
    }
    setState(() {});
  }

  @override
  Widget build(BuildContext context) => LayoutBuilder(
    builder: (context, constraints) {
      final width = constraints.maxWidth;
      final height = constraints.maxHeight;
      // A square unfolded window also has room for two usable panels.
      // Bound the keypad width so the remaining space stays available to the table.
      const gap = 20.0;
      final sideBySide =
          width >= 640 || (width >= 560 && width > height * 1.25);
      if (sideBySide) {
        final padWidth = (width * .34).clamp(232.0, 300.0);
        final navHeight = height < 360 ? 44.0 : 50.0;
        final showPreview = height >= 480;
        final inputHeight = min(
          height,
          320.0 + navHeight + 12 + (showPreview ? 76 : 0),
        );
        final tableWidth = width - padWidth - gap;
        final tableHeight = min(
          height,
          (p.values.length + 1) * (tableWidth >= 420 ? 64.0 : 56.0) + 32,
        );
        return Row(
          key: const ValueKey('addition-wide'),
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Expanded(
              child: SizedBox(
                height: tableHeight,
                child: Column(
                  children: [
                    selectionLabel(26),
                    const SizedBox(height: 6),
                    Expanded(child: grid(tableHeight - 32)),
                  ],
                ),
              ),
            ),
            const SizedBox(width: gap),
            SizedBox(
              width: padWidth,
              height: inputHeight,
              child: Column(
                children: [
                  if (showPreview) ...[
                    Surface(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 14,
                        vertical: 8,
                      ),
                      color: selectedMemo == null ? Colors.white : memoSurface,
                      child: Row(
                        children: [
                          WordText(
                            selectedMemo == null ? '선택한 답안' : '계산 메모',
                            style: const TextStyle(fontSize: 11, color: muted),
                          ),
                          const Spacer(),
                          WordText(
                            answer.isEmpty ? '—' : answer,
                            key: const ValueKey('wide-input-preview'),
                            style: numeric.copyWith(
                              fontSize: 23,
                              fontWeight: FontWeight.w700,
                            ),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 12),
                  ],
                  Expanded(child: keypad()),
                  const SizedBox(height: 12),
                  navigation(navHeight),
                ],
              ),
            ),
          ],
        );
      }
      final navHeight = height < 520 ? 44.0 : 48.0;
      final padHeight = height < 520 ? 200.0 : 236.0;
      const labelHeight = 26.0;
      final gridHeight = max(
        0.0,
        height - padHeight - navHeight - labelHeight - 24,
      );
      return Column(
        key: const ValueKey('addition-stacked'),
        children: [
          Expanded(child: grid(gridHeight)),
          const SizedBox(height: 6),
          Center(
            child: ConstrainedBox(
              constraints: const BoxConstraints(maxWidth: 480),
              child: Column(
                children: [
                  selectionLabel(labelHeight),
                  const SizedBox(height: 6),
                  SizedBox(height: padHeight, child: keypad()),
                  const SizedBox(height: 12),
                  navigation(navHeight),
                ],
              ),
            ),
          ),
        ],
      );
    },
  );
  Widget selectionLabel(double height) {
    final row = selected ~/ p.width, col = selected % p.width;
    final rowName = row == p.values.length - 1 ? '합계 행' : '${row + 1}행';
    final colName = col == p.width - 1 ? '합계 열' : '${col + 1}열';
    final memoParts = selectedMemo?.split(':');
    final caption = memoParts == null
        ? '$rowName · $colName 답안'
        : '${memoParts[1] == 'r' ? '가로' : '세로'} ${int.parse(memoParts[2]) + 1} · 계산 메모';
    return SizedBox(
      height: height,
      child: Row(
        children: [
          const Icon(Icons.edit_outlined, size: 14, color: muted),
          const SizedBox(width: 6),
          Expanded(
            child: FittedBox(
              fit: BoxFit.scaleDown,
              alignment: Alignment.centerLeft,
              child: WordText(
                caption,
                style: const TextStyle(
                  fontSize: 12,
                  fontWeight: FontWeight.w700,
                ),
              ),
            ),
          ),
          const SizedBox(width: 8),
          const WordText(
            '파란 칸은 메모',
            style: TextStyle(fontSize: 10, color: muted),
          ),
        ],
      ),
    );
  }

  Widget grid(double height) => LayoutBuilder(
    builder: (context, constraints) {
      final rows = p.values.length, cols = p.width;
      final rowLimit = constraints.maxWidth >= 420 ? 64.0 : 56.0;
      final actualHeight = min(
        min(height, constraints.maxHeight),
        (rows + 1) * rowLimit,
      );
      final cellHeight = actualHeight / (rows + 1);
      // Removing the name row/column makes room for one memo row/column.
      final valueWidth = constraints.maxWidth / (cols + 1);
      final font = (valueWidth * .42).clamp(13.0, 21.0);
      return Align(
        alignment: Alignment.center,
        child: SizedBox(
          height: actualHeight,
          child: Column(
            children: [
              for (var row = 0; row < rows; row++)
                Row(
                  children: [
                    for (var col = 0; col < cols; col++)
                      valueTile(row, col, valueWidth, cellHeight, font),
                    memoTile('r', row, valueWidth, cellHeight, font),
                  ],
                ),
              Row(
                children: [
                  for (var col = 0; col < cols; col++)
                    memoTile('c', col, valueWidth, cellHeight, font),
                  SizedBox(
                    width: valueWidth,
                    height: cellHeight,
                    child: const Center(
                      child: FittedBox(
                        fit: BoxFit.scaleDown,
                        child: WordText(
                          '메모',
                          style: TextStyle(fontSize: 10, color: memoInk),
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      );
    },
  );

  Widget memoTile(
    String axis,
    int number,
    double width,
    double height,
    double font,
  ) {
    final id = '${widget.index}:$axis:$number';
    final value = widget.session.memos[id] ?? '';
    final focused = selectedMemo == id;
    return Semantics(
      label:
          '${axis == 'r' ? '가로' : '세로'} ${number + 1} 계산 메모 ${value.isEmpty ? '비어 있음' : value}',
      selected: focused,
      button: true,
      child: GestureDetector(
        key: ValueKey('memo-$axis-$number'),
        behavior: HitTestBehavior.opaque,
        onTap: widget.busy
            ? null
            : () => setState(() {
                selectedMemo = id;
                replace = true;
              }),
        child: Container(
          width: width,
          height: height,
          padding: const EdgeInsets.all(3),
          decoration: BoxDecoration(
            color: focused ? const Color(0xFFCCE0F1) : memoSurface,
            border: Border.all(
              color: focused ? memoInk : const Color(0xFFBCCEDC),
              width: focused ? 2 : .5,
            ),
          ),
          alignment: Alignment.center,
          child: value.isEmpty
              ? const Icon(Icons.edit_outlined, size: 13, color: memoInk)
              : FittedBox(
                  fit: BoxFit.scaleDown,
                  child: WordText(
                    value,
                    style: numeric.copyWith(fontSize: font, color: memoInk),
                  ),
                ),
        ),
      ),
    );
  }

  Widget valueTile(int row, int col, double width, double height, double font) {
    final position = row * p.width + col;
    final hidden = p.hidden.contains(position);
    final focused = selectedMemo == null && position == selected;
    final memoParts = selectedMemo?.split(':');
    final aligned = memoParts == null
        ? row == selected ~/ p.width || col == selected % p.width
        : memoParts[1] == 'r'
        ? row == int.parse(memoParts[2])
        : col == int.parse(memoParts[2]);
    final totalRow = row == p.values.length - 1;
    final totalCol = col == p.width - 1;
    final value = hidden
        ? widget.session.answers[p.answerKey(widget.index, position)] ?? ''
        : '${p.values[row][col]}';
    final child = Container(
      width: width,
      height: height,
      alignment: Alignment.center,
      padding: const EdgeInsets.symmetric(horizontal: 3),
      decoration: BoxDecoration(
        color: focused
            ? lime
            : hidden
            ? Colors.white
            : aligned
            ? const Color(0xFFE9EEE3)
            : const Color(0xFFF0F2EB),
        border: focused
            ? Border.all(color: ink, width: 2)
            : Border(
                top: BorderSide(
                  color: totalRow ? ink : line,
                  width: totalRow ? 1.5 : .5,
                ),
                left: BorderSide(
                  color: totalCol ? ink : line,
                  width: totalCol ? 1.5 : .5,
                ),
                right: const BorderSide(color: line, width: .5),
                bottom: const BorderSide(color: line, width: .5),
              ),
      ),
      child: FittedBox(
        fit: BoxFit.scaleDown,
        child: WordText(
          value.isEmpty ? '·' : value,
          style: numeric.copyWith(
            fontSize: font,
            fontWeight: hidden || totalRow || totalCol
                ? FontWeight.w800
                : FontWeight.w500,
          ),
        ),
      ),
    );
    if (!hidden) return child;
    return Semantics(
      label:
          '${row + 1}행 ${col + 1}열 ${totalRow || totalCol ? '합계 ' : ''}답칸 ${value.isEmpty ? '비어 있음' : value}',
      selected: focused,
      button: true,
      child: GestureDetector(
        key: ValueKey('answer-$position'),
        behavior: HitTestBehavior.opaque,
        onTap: widget.busy ? null : () => choose(position),
        child: child,
      ),
    );
  }

  Widget keypad() => Column(
    children: [
      for (var row = 0; row < 4; row++) ...[
        if (row > 0) const SizedBox(height: 8),
        Expanded(
          child: Row(
            children: [
              for (var col = 0; col < 3; col++) ...[
                if (col > 0) const SizedBox(width: 8),
                Expanded(
                  child: row < 3
                      ? key('${row * 3 + col + 1}', '${row * 3 + col + 1}')
                      : switch (col) {
                          0 => key('sign', '-'),
                          1 => key('0', '0'),
                          _ => Tooltip(
                            message: '한 자리 지우기 · 길게 누르면 모두 지우기',
                            child: key(
                              'back',
                              '⌫',
                              icon: Icons.backspace_outlined,
                              onLongPress: () => input('clear'),
                            ),
                          ),
                        },
                ),
              ],
            ],
          ),
        ),
      ],
    ],
  );
  Widget key(
    String id,
    String label, {
    VoidCallback? onLongPress,
    IconData? icon,
  }) => Semantics(
    button: true,
    label: id == 'back'
        ? '한 자리 지우기, 길게 누르면 모두 지우기'
        : id == 'sign'
        ? '음수 부호 전환'
        : label,
    child: Material(
      color: Colors.white,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(13),
        side: const BorderSide(color: line),
      ),
      clipBehavior: Clip.antiAlias,
      child: InkWell(
        key: ValueKey('pad-$id'),
        onTap: widget.busy ? null : () => input(id),
        onLongPress: widget.busy ? null : onLongPress,
        child: Center(
          child: icon != null
              ? Icon(icon, size: 24)
              : WordText(
                  label,
                  style: TextStyle(fontSize: 25, fontWeight: FontWeight.w700),
                ),
        ),
      ),
    ),
  );
  Widget navigation(double height) => SizedBox(
    height: height,
    child: Row(
      children: [
        SizedBox(
          width: 76,
          height: height,
          child: OutlinedButton(
            style: OutlinedButton.styleFrom(
              padding: EdgeInsets.zero,
              minimumSize: Size.zero,
            ),
            onPressed: widget.busy ? null : widget.previous,
            child: const WordText('이전 표', style: TextStyle(fontSize: 12)),
          ),
        ),
        const SizedBox(width: 10),
        Expanded(
          child: SizedBox(
            height: height,
            child: FilledButton(
              style: FilledButton.styleFrom(minimumSize: Size.zero),
              onPressed: widget.busy ? null : widget.next,
              child: FittedBox(
                fit: BoxFit.scaleDown,
                child: WordText(widget.last ? '완료하고 채점' : '다음 표'),
              ),
            ),
          ),
        ),
      ],
    ),
  );
}
