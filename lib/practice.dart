import 'addition.dart';
import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'main.dart';
import 'model.dart';
import 'store.dart';

class PracticeScreen extends StatefulWidget {
  final AppController controller;
  final PracticeSession session;
  const PracticeScreen({
    super.key,
    required this.controller,
    required this.session,
  });
  @override
  State<PracticeScreen> createState() => _PracticeScreenState();
}

class _PracticeScreenState extends State<PracticeScreen> {
  late int index;
  late final ValueNotifier<int> elapsed;
  Timer? ticker;
  Timer? advance;
  bool busy = false;
  bool leaving = false;
  bool allowPop = false;
  bool submitting = false;
  DateTime? stoppedAt;
  final scroll = ScrollController();
  GlobalKey<_TableExerciseState> tableKey = GlobalKey<_TableExerciseState>();
  AppController get c => widget.controller;
  PracticeSession get s => widget.session;
  @override
  void initState() {
    super.initState();
    index = s.page;
    elapsed = ValueNotifier(s.elapsedAt(DateTime.now()));
    ticker = Timer.periodic(const Duration(seconds: 1), (_) {
      if (stoppedAt == null) elapsed.value = s.elapsedAt(DateTime.now());
    });
    c.addListener(changed);
  }

  void changed() {
    if (mounted) setState(() {});
  }

  @override
  void dispose() {
    advance?.cancel();
    ticker?.cancel();
    elapsed.dispose();
    scroll.dispose();
    c.removeListener(changed);
    super.dispose();
  }

  void go(int value) {
    advance?.cancel();
    FocusManager.instance.primaryFocus?.unfocus();
    setState(() {
      index = value.clamp(0, s.problems.length - 1);
      tableKey = GlobalKey<_TableExerciseState>();
    });
    c.page(index);
    if (scroll.hasClients) scroll.jumpTo(0);
  }

  void selected(String answer) {
    advance?.cancel();
    c.answer('$index', answer);
    final p = s.problems[index];
    final complete =
        p.type != ProblemType.order || answer.split(',').length == 4;
    if (complete && index < s.problems.length - 1) {
      advance = Timer(const Duration(milliseconds: 420), () {
        if (mounted && !busy) go(index + 1);
      });
    }
  }

  Future<void> leave() async {
    if (busy || leaving || submitting) return;
    leaving = true;
    advance?.cancel();
    final discard = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('이번 연습을 그만둘까요?'),
        content: const Text(
          '나가면 이번 문제와 답안·메모가 사라지고 완료 기록에는 남지 않습니다. 기존 완료 기록은 유지됩니다.\n\n이 안내를 보는 동안에도 시간은 흐릅니다.',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('계속 풀기'),
          ),
          TextButton(
            key: const ValueKey('confirm-discard'),
            onPressed: () => Navigator.pop(context, true),
            child: const Text('나가기'),
          ),
        ],
      ),
    );
    if (!mounted) return;
    if (discard == true) {
      await c.abandon();
      if (!mounted) return;
      setState(() => allowPop = true);
      WidgetsBinding.instance.addPostFrameCallback((_) {
        if (mounted) Navigator.pop(context);
      });
    } else {
      leaving = false;
    }
  }

  Future<void> finish() async {
    if (busy || submitting || leaving) return;
    submitting = true;
    advance?.cancel();
    FocusManager.instance.primaryFocus?.unfocus();
    if (s.answered < s.total) {
      final submit = await showDialog<bool>(
        context: context,
        builder: (context) => AlertDialog(
          title: Text('아직 ${s.total - s.answered}개가 남아 있어요'),
          content: const Text('지금 완료하면 미응답은 오답으로 기록됩니다.'),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context, false),
              child: const Text('마저 풀기'),
            ),
            TextButton(
              onPressed: () => Navigator.pop(context, true),
              child: const Text('제출하고 채점'),
            ),
          ],
        ),
      );
      if (submit != true) {
        submitting = false;
        if (mounted) jumpUnanswered();
        return;
      }
    }
    if (!mounted) return;
    stoppedAt = DateTime.now();
    elapsed.value = s.elapsedAt(stoppedAt!);
    setState(() => busy = true);
    try {
      final result = await c.complete(stoppedAt!);
      if (mounted) {
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (_) => ResultScreen(session: result)),
        );
      }
    } catch (_) {
      stoppedAt = null;
      submitting = false;
      if (mounted) {
        setState(() => busy = false);
        toast(context, '결과를 저장하지 못했어요. 답안은 유지됩니다. 다시 완료를 눌러 주세요.');
      }
    }
  }

  void jumpUnanswered() {
    for (var i = 0; i < s.problems.length; i++) {
      if (s.problems[i].expected(i).keys.any((k) => !s.hasAnswer(k))) {
        go(i);
        break;
      }
    }
  }

  Future<void> overview() async {
    advance?.cancel();
    final target = await showModalBottomSheet<int>(
      context: context,
      showDragHandle: true,
      backgroundColor: paper,
      isScrollControlled: true,
      builder: (context) => SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.fromLTRB(24, 8, 24, 24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                '문제 한눈에 보기',
                style: TextStyle(fontSize: 22, fontWeight: FontWeight.w800),
              ),
              const SizedBox(height: 8),
              const Text(
                '초록색은 응답 완료 · 정답 여부는 제출 후 확인',
                style: TextStyle(color: muted, fontSize: 12),
              ),
              const SizedBox(height: 20),
              Wrap(
                spacing: 10,
                runSpacing: 10,
                children: List.generate(s.problems.length, (i) {
                  final done = s.problems[i]
                      .expected(i)
                      .keys
                      .every(s.hasAnswer);
                  return SizedBox(
                    width: 58,
                    height: 54,
                    child: OutlinedButton(
                      style: OutlinedButton.styleFrom(
                        padding: EdgeInsets.zero,
                        backgroundColor: done ? lime : Colors.white,
                        side: BorderSide(
                          color: i == index ? ink : line,
                          width: i == index ? 2 : 1,
                        ),
                      ),
                      onPressed: () => Navigator.pop(context, i),
                      child: Text('${i + 1}'),
                    ),
                  );
                }),
              ),
            ],
          ),
        ),
      ),
    );
    if (target != null && mounted) go(target);
  }

  Widget additionBody() => SafeArea(
    top: false,
    child: Center(
      child: ConstrainedBox(
        constraints: const BoxConstraints(maxWidth: 1000),
        child: Padding(
          padding: const EdgeInsets.fromLTRB(12, 0, 12, 10),
          child: Column(
            children: [
              SizedBox(
                height: 38,
                child: Row(
                  children: [
                    InkWell(
                      onTap: busy ? null : overview,
                      child: Padding(
                        padding: const EdgeInsets.symmetric(
                          horizontal: 4,
                          vertical: 6,
                        ),
                        child: Row(
                          children: [
                            Text(
                              '표 ${index + 1} / 5',
                              style: const TextStyle(
                                fontWeight: FontWeight.w800,
                                fontSize: 14,
                              ),
                            ),
                            const Icon(Icons.expand_more_rounded, size: 20),
                          ],
                        ),
                      ),
                    ),
                    const SizedBox(width: 10),
                    Text(
                      '${s.answered}/40 응답',
                      style: const TextStyle(fontSize: 11, color: muted),
                    ),
                    const Spacer(),
                    const Icon(Icons.timer_outlined, size: 15, color: muted),
                    const SizedBox(width: 5),
                    ValueListenableBuilder<int>(
                      valueListenable: elapsed,
                      builder: (_, value, _) => Text(
                        clockLabel(value),
                        style: numeric.copyWith(
                          fontWeight: FontWeight.w700,
                          fontSize: 15,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              ClipRRect(
                borderRadius: BorderRadius.circular(4),
                child: LinearProgressIndicator(
                  value: s.answered / s.total,
                  minHeight: 3,
                  color: ink,
                  backgroundColor: line,
                ),
              ),
              const SizedBox(height: 8),
              if (c.error != null)
                Text(
                  c.error!,
                  style: const TextStyle(color: danger, fontSize: 11),
                ),
              Expanded(
                child: AdditionExercise(
                  key: ValueKey(index),
                  problem: s.problems[index],
                  index: index,
                  session: s,
                  onAnswer: c.answer,
                  onMemo: c.memo,
                  previous: index == 0 ? null : () => go(index - 1),
                  next: index == 4 ? finish : () => go(index + 1),
                  last: index == 4,
                  busy: busy,
                ),
              ),
            ],
          ),
        ),
      ),
    ),
  );
  Widget problemMap() => Surface(
    key: const ValueKey('practice-problem-map'),
    padding: const EdgeInsets.all(12),
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      mainAxisSize: MainAxisSize.min,
      children: [
        const Eyebrow('이번 연습'),
        const SizedBox(height: 12),
        ValueListenableBuilder<int>(
          valueListenable: elapsed,
          builder: (_, value, _) => Text(
            clockLabel(value),
            style: numeric.copyWith(fontSize: 26, fontWeight: FontWeight.w800),
          ),
        ),
        const SizedBox(height: 6),
        Text(
          '${s.answered}/${s.total} 응답',
          style: const TextStyle(color: muted, fontSize: 12),
        ),
        const SizedBox(height: 20),
        Wrap(
          spacing: 6,
          runSpacing: 6,
          children: List.generate(s.problems.length, (i) {
            final done = s.problems[i].expected(i).keys.every(s.hasAnswer);
            return SizedBox(
              width: 40,
              height: 44,
              child: OutlinedButton(
                key: ValueKey('problem-jump-$i'),
                onPressed: busy ? null : () => go(i),
                style: OutlinedButton.styleFrom(
                  padding: EdgeInsets.zero,
                  backgroundColor: i == index
                      ? ink
                      : done
                      ? lime
                      : Colors.white,
                  foregroundColor: i == index ? Colors.white : ink,
                  side: BorderSide(color: i == index ? ink : line),
                ),
                child: Text('${i + 1}'),
              ),
            );
          }),
        ),
        const SizedBox(height: 14),
        const Text('초록색 · 응답 완료', style: TextStyle(fontSize: 11, color: muted)),
      ],
    ),
  );

  Widget comparisonBody(Problem p) => SafeArea(
    top: false,
    child: LayoutBuilder(
      builder: (context, box) {
        final wide = box.maxWidth >= 700 && box.maxHeight >= 500;
        final compact = box.maxWidth < 380 || box.maxHeight < 740;
        Widget exercise = p.type == ProblemType.order
            ? OrderingExercise(
                problem: p,
                answer: s.answers['$index'] ?? '',
                onChanged: selected,
              )
            : ComparisonExercise(
                problem: p,
                answer: s.answers['$index'],
                onChanged: selected,
              );
        Widget workspace = Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Row(
              children: [
                TextButton(
                  onPressed: busy ? null : overview,
                  child: Text('${index + 1} / ${s.problems.length}'),
                ),
                const Spacer(),
                if (!wide)
                  ValueListenableBuilder<int>(
                    valueListenable: elapsed,
                    builder: (_, value, _) => Text(
                      clockLabel(value),
                      style: numeric.copyWith(
                        fontSize: 16,
                        fontWeight: FontWeight.w700,
                      ),
                    ),
                  ),
              ],
            ),
            LinearProgressIndicator(
              value: s.answered / s.total,
              minHeight: 3,
              color: ink,
              backgroundColor: line,
            ),
            if (c.error != null)
              Text(
                c.error!,
                style: const TextStyle(color: danger, fontSize: 12),
              ),
            Expanded(
              child: LayoutBuilder(
                builder: (context, area) => SingleChildScrollView(
                  controller: scroll,
                  child: ConstrainedBox(
                    constraints: BoxConstraints(minHeight: area.maxHeight),
                    child: Padding(
                      padding: EdgeInsets.symmetric(
                        vertical: compact ? 10 : 20,
                      ),
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        crossAxisAlignment: CrossAxisAlignment.stretch,
                        children: [
                          Text(
                            p.type == ProblemType.order
                                ? '큰 것부터 차례로 탭하세요.'
                                : '어느 쪽이 더 클까요?',
                            style: TextStyle(
                              fontSize: compact ? 21 : 23,
                              fontWeight: FontWeight.w800,
                              letterSpacing: -.7,
                            ),
                          ),
                          const SizedBox(height: 6),
                          Text(
                            p.type == ProblemType.order
                                ? '선택한 카드를 다시 누르면 취소됩니다.'
                                : '답을 선택하면 다음 문제로 넘어갑니다.',
                            style: const TextStyle(fontSize: 12, color: muted),
                          ),
                          SizedBox(height: compact ? 16 : 24),
                          IgnorePointer(ignoring: busy, child: exercise),
                        ],
                      ),
                    ),
                  ),
                ),
              ),
            ),
            const SizedBox(height: 8),
            Row(
              children: [
                OutlinedButton(
                  onPressed: index == 0 || busy ? null : () => go(index - 1),
                  child: const Icon(Icons.arrow_back_rounded),
                ),
                const SizedBox(width: 10),
                Expanded(
                  child: index == s.problems.length - 1
                      ? FilledButton(
                          onPressed: busy ? null : finish,
                          child: const Text('완료하고 채점하기'),
                        )
                      : OutlinedButton(
                          onPressed: busy ? null : () => go(index + 1),
                          child: const Text('다음 문제'),
                        ),
                ),
                if (!wide)
                  IconButton(
                    tooltip: '전체 문제 보기',
                    onPressed: busy ? null : overview,
                    icon: const Icon(Icons.apps_rounded),
                  ),
              ],
            ),
          ],
        );
        return Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 1100),
            child: Padding(
              padding: EdgeInsets.fromLTRB(
                compact ? 12 : 20,
                0,
                compact ? 12 : 20,
                12,
              ),
              child: wide
                  ? Row(
                      key: const ValueKey('practice-wide'),
                      crossAxisAlignment: CrossAxisAlignment.center,
                      children: [
                        Expanded(child: workspace),
                        const SizedBox(width: 24),
                        SizedBox(width: 166, child: problemMap()),
                      ],
                    )
                  : workspace,
            ),
          ),
        );
      },
    ),
  );

  @override
  Widget build(BuildContext context) {
    final p = s.problems[index];
    final isTable = p.type == ProblemType.table;
    return PopScope(
      canPop: allowPop,
      onPopInvokedWithResult: (didPop, result) {
        if (!didPop) unawaited(leave());
      },
      child: Scaffold(
        appBar: AppBar(
          leading: IconButton(
            tooltip: '연습 나가기',
            onPressed: busy ? null : leave,
            icon: const Icon(Icons.arrow_back_rounded),
          ),
          title: Text(
            s.kind.title,
            style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w800),
          ),
          actions: [
            TextButton(
              onPressed: busy ? null : finish,
              child: busy
                  ? const SizedBox(
                      width: 18,
                      height: 18,
                      child: CircularProgressIndicator(strokeWidth: 2),
                    )
                  : const Text(
                      '완료',
                      style: TextStyle(fontWeight: FontWeight.w800),
                    ),
            ),
            const SizedBox(width: 8),
          ],
        ),
        body: isTable ? additionBody() : comparisonBody(p),
      ),
    );
  }
}

class FractionView extends StatelessWidget {
  final List<int> pair;
  final double size;
  final Color color;
  const FractionView(this.pair, {super.key, this.size = 32, this.color = ink});
  @override
  Widget build(BuildContext context) => Semantics(
    label: '${pair[1]}분의 ${pair[0]}',
    excludeSemantics: true,
    child: IntrinsicWidth(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 12),
            child: Text(
              '${pair[0]}',
              style: numeric.copyWith(
                fontSize: size,
                fontWeight: FontWeight.w700,
                color: color,
              ),
            ),
          ),
          Container(
            height: 2,
            margin: const EdgeInsets.symmetric(vertical: 4),
            color: color,
          ),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 12),
            child: Text(
              '${pair[1]}',
              style: numeric.copyWith(
                fontSize: size,
                fontWeight: FontWeight.w700,
                color: color,
              ),
            ),
          ),
        ],
      ),
    ),
  );
}

class ComparisonExercise extends StatelessWidget {
  final Problem problem;
  final String? answer;
  final ValueChanged<String> onChanged;
  const ComparisonExercise({
    super.key,
    required this.problem,
    this.answer,
    required this.onChanged,
  });
  Widget operand(int i) => Surface(
    key: ValueKey('comparison-operand-$i'),
    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 18),
    child: Column(
      children: [
        Text(
          i == 0 ? '왼쪽' : '오른쪽',
          style: const TextStyle(
            fontSize: 12,
            color: muted,
            fontWeight: FontWeight.w700,
          ),
        ),
        const SizedBox(height: 14),
        if (problem.type == ProblemType.product)
          FittedBox(
            fit: BoxFit.scaleDown,
            child: Text(
              '${problem.values[i][0]} × ${(problem.values[i][1] / 10).toStringAsFixed(1)}',
              maxLines: 1,
              softWrap: false,
              style: numeric.copyWith(
                fontSize: 28,
                fontWeight: FontWeight.w800,
              ),
            ),
          )
        else
          FittedBox(
            fit: BoxFit.scaleDown,
            child: FractionView(problem.values[i], size: 37),
          ),
        const SizedBox(height: 6),
      ],
    ),
  );
  @override
  Widget build(BuildContext context) => Column(
    children: [
      Row(
        children: [
          Expanded(child: operand(0)),
          const Padding(
            padding: EdgeInsets.symmetric(horizontal: 8),
            child: Text(
              'VS',
              style: TextStyle(
                color: muted,
                fontSize: 10,
                fontWeight: FontWeight.w800,
              ),
            ),
          ),
          Expanded(child: operand(1)),
        ],
      ),
      const SizedBox(height: 28),
      Row(
        children: [
          comparisonButton('>', '왼쪽이 큼'),
          const SizedBox(width: 12),
          comparisonButton('<', '오른쪽이 큼'),
        ],
      ),
      const SizedBox(height: 12),
      const Text(
        '이전 문제로 돌아가 답을 수정할 수 있어요.',
        style: TextStyle(color: muted, fontSize: 11),
      ),
    ],
  );
  Widget comparisonButton(String sign, String label) => Expanded(
    child: Semantics(
      label: label,
      button: true,
      selected: answer == sign,
      child: Material(
        color: answer == sign ? ink : lime,
        borderRadius: BorderRadius.circular(20),
        clipBehavior: Clip.antiAlias,
        child: InkWell(
          onTap: () => onChanged(sign),
          child: Padding(
            padding: const EdgeInsets.symmetric(vertical: 16),
            child: Column(
              children: [
                Text(
                  sign,
                  style: TextStyle(
                    fontSize: 34,
                    height: 1.1,
                    fontWeight: FontWeight.w700,
                    color: answer == sign ? Colors.white : ink,
                  ),
                ),
                const SizedBox(height: 5),
                Text(
                  label,
                  style: TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.w800,
                    color: answer == sign ? Colors.white : ink,
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    ),
  );
}

class OrderingExercise extends StatelessWidget {
  final Problem problem;
  final String answer;
  final ValueChanged<String> onChanged;
  const OrderingExercise({
    super.key,
    required this.problem,
    required this.answer,
    required this.onChanged,
  });
  @override
  Widget build(BuildContext context) {
    final selected = answer.isEmpty
        ? <int>[]
        : answer.split(',').map(int.parse).toList();
    return Column(
      children: [
        for (var row = 0; row < 2; row++) ...[
          Row(
            children: [
              for (var col = 0; col < 2; col++) ...[
                if (col == 1) const SizedBox(width: 12),
                Expanded(child: card(row * 2 + col, selected)),
              ],
            ],
          ),
          const SizedBox(height: 12),
        ],
        const SizedBox(height: 12),
        Surface(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Eyebrow('YOUR ORDER  /  큰 값 → 작은 값'),
              const SizedBox(height: 16),
              Row(
                children: List.generate(
                  4,
                  (i) => Expanded(
                    child: Padding(
                      padding: EdgeInsets.only(right: i == 3 ? 0 : 6),
                      child: Container(
                        key: ValueKey('order-slot-$i'),
                        height: 52,
                        alignment: Alignment.center,
                        decoration: BoxDecoration(
                          color: i < selected.length ? lime : paper,
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: Text(
                          i < selected.length
                              ? String.fromCharCode(65 + selected[i])
                              : '·',
                          style: TextStyle(
                            fontSize: 22,
                            fontWeight: FontWeight.w800,
                            color: i < selected.length ? ink : muted,
                          ),
                        ),
                      ),
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
        TextButton.icon(
          onPressed: selected.isEmpty ? null : () => onChanged(''),
          icon: const Icon(Icons.restart_alt_rounded, size: 18),
          label: const Text('순서 다시 선택'),
        ),
      ],
    );
  }

  Widget card(int i, List<int> selected) {
    final rank = selected.indexOf(i);
    return Semantics(
      label: '${String.fromCharCode(65 + i)} 분수 선택',
      button: true,
      selected: rank >= 0,
      child: Material(
        color: rank >= 0 ? const Color(0xFFEAF2D6) : Colors.white,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(22),
          side: BorderSide(
            color: rank >= 0 ? ink : line,
            width: rank >= 0 ? 2 : 1,
          ),
        ),
        clipBehavior: Clip.antiAlias,
        child: InkWell(
          onTap: () {
            final next = [...selected];
            if (rank >= 0) {
              next.remove(i);
            } else {
              next.add(i);
            }
            onChanged(next.join(','));
          },
          child: Padding(
            padding: const EdgeInsets.all(14),
            child: Column(
              children: [
                Row(
                  children: [
                    Text(
                      String.fromCharCode(65 + i),
                      style: const TextStyle(
                        fontWeight: FontWeight.w800,
                        color: muted,
                        fontSize: 12,
                      ),
                    ),
                    const Spacer(),
                    Text(
                      rank >= 0 ? '선택됨' : ' ',
                      style: const TextStyle(
                        fontWeight: FontWeight.w700,
                        fontSize: 12,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 8),
                FractionView(problem.values[i], size: 29),
                const SizedBox(height: 6),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

List<String> columnNames(int index) => switch (index) {
  0 => ['언어', '자료', '상황'],
  1 => ['2023', '2024', '2025', '2026'],
  2 => ['2024', '2025', '2026'],
  3 => ['2023', '2024', '2025', '2026'],
  _ => ['A도', 'B도', 'C도', 'D도', 'E도', 'F도'],
};
List<String> rowNames(int index) => switch (index) {
  0 => ['A', 'B', 'C'],
  1 => ['초졸↓', '중졸', '고졸', '대졸↑'],
  2 => ['기업 A', '기업 B', '기업 C'],
  3 => ['한', '미', '일', '중'],
  _ => ['0–10', '11–20', '21–30', '31–40', '40↑'],
};

class TableExercise extends StatefulWidget {
  final Problem problem;
  final int index;
  final PracticeSession session;
  final void Function(String, String) onAnswer;
  const TableExercise({
    super.key,
    required this.problem,
    required this.index,
    required this.session,
    required this.onAnswer,
  });
  @override
  State<TableExercise> createState() => _TableExerciseState();
}

class _TableExerciseState extends State<TableExercise> {
  final controllers = <int, TextEditingController>{};
  final nodes = <int, FocusNode>{};
  final keys = <int, GlobalKey>{};
  final horizontal = ScrollController();
  int? selected;
  Problem get p => widget.problem;
  @override
  void initState() {
    super.initState();
    for (final cell in p.hidden) {
      controllers[cell] = TextEditingController(
        text: widget.session.answers[p.answerKey(widget.index, cell)] ?? '',
      );
      keys[cell] = GlobalKey();
      nodes[cell] = FocusNode()
        ..addListener(() {
          if (nodes[cell]!.hasFocus && mounted) setState(() => selected = cell);
        });
    }
  }

  @override
  void dispose() {
    for (final c in controllers.values) {
      c.dispose();
    }
    for (final n in nodes.values) {
      n.dispose();
    }
    horizontal.dispose();
    super.dispose();
  }

  void focus(int cell) {
    setState(() => selected = cell);
    nodes[cell]!.requestFocus();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      final context = keys[cell]?.currentContext;
      if (context != null) {
        Scrollable.ensureVisible(
          context,
          alignment: .5,
          duration: MediaQuery.disableAnimationsOf(context)
              ? Duration.zero
              : const Duration(milliseconds: 180),
        );
      }
    });
  }

  void move(int direction) {
    final i = selected == null ? -1 : p.hidden.indexOf(selected!);
    focus(p.hidden[(i + direction).clamp(0, p.hidden.length - 1)]);
  }

  void negate() {
    if (selected == null) {
      focus(p.hidden.first);
    }
    final cell = selected!;
    final old = controllers[cell]!.text;
    final text = old.startsWith('-') ? old.substring(1) : '-$old';
    controllers[cell]!.value = TextEditingValue(
      text: text,
      selection: TextSelection.collapsed(offset: text.length),
    );
    widget.onAnswer(p.answerKey(widget.index, cell), text);
    nodes[cell]!.requestFocus();
  }

  Widget label(String value, double width, {bool header = false}) => Container(
    width: width,
    height: 52,
    alignment: Alignment.center,
    decoration: BoxDecoration(
      color: header ? const Color(0xFFE9EEE3) : const Color(0xFFF0F2EB),
      border: Border.all(color: line, width: .5),
    ),
    padding: const EdgeInsets.symmetric(horizontal: 2),
    child: Text(
      value,
      textAlign: TextAlign.center,
      style: const TextStyle(fontSize: 11, fontWeight: FontWeight.w800),
    ),
  );
  Widget cell(int r, int col, double width) {
    final position = r * p.width + col;
    final hidden = p.hidden.contains(position);
    final active = selected == position;
    final aligned =
        selected != null &&
        (selected! ~/ p.width == r || selected! % p.width == col);
    final color = active
        ? const Color(0xFFF1F9D9)
        : hidden
        ? Colors.white
        : aligned
        ? const Color(0xFFE8EDDF)
        : const Color(0xFFF0F2EB);
    return Container(
      key: keys[position],
      width: width,
      height: 52,
      decoration: BoxDecoration(
        color: color,
        border: Border.all(color: active ? ink : line, width: active ? 2 : .5),
      ),
      child: hidden
          ? Semantics(
              label:
                  '${rowNames(widget.index).elementAtOrNull(r) ?? '합계'} ${columnNames(widget.index).elementAtOrNull(col) ?? '합계'} 빈칸',
              child: TextField(
                controller: controllers[position],
                focusNode: nodes[position],
                textAlign: TextAlign.center,
                style: numeric.copyWith(
                  fontSize: 17,
                  fontWeight: FontWeight.w800,
                ),
                keyboardType: const TextInputType.numberWithOptions(
                  signed: true,
                ),
                textInputAction: TextInputAction.next,
                inputFormatters: [
                  TextInputFormatter.withFunction(
                    (old, value) => RegExp(r'^-?\d{0,6}$').hasMatch(value.text)
                        ? value
                        : old,
                  ),
                ],
                decoration: const InputDecoration(
                  border: InputBorder.none,
                  enabledBorder: InputBorder.none,
                  focusedBorder: InputBorder.none,
                  hintText: '·',
                  contentPadding: EdgeInsets.symmetric(vertical: 14),
                  isDense: true,
                ),
                onTap: () => focus(position),
                onChanged: (value) =>
                    widget.onAnswer(p.answerKey(widget.index, position), value),
                onSubmitted: (_) => move(1),
              ),
            )
          : Center(
              child: Text(
                '${p.values[r][col]}',
                style: numeric.copyWith(
                  fontSize: 16,
                  fontWeight: FontWeight.w600,
                ),
              ),
            ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final rows = p.values.length - 1, cols = p.width - 1;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        LayoutBuilder(
          builder: (context, box) {
            const rowWidth = 46.0, sumWidth = 64.0;
            final usable = box.maxWidth - rowWidth - sumWidth;
            final width = (usable / cols).clamp(60.0, 120.0);
            final scrolling = width * cols > usable + .1;
            return Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                if (scrolling)
                  const Padding(
                    padding: EdgeInsets.only(bottom: 10),
                    child: Row(
                      children: [
                        Icon(Icons.swipe_rounded, size: 16, color: muted),
                        SizedBox(width: 6),
                        Expanded(
                          child: Text(
                            '가운데 열을 좌우로 밀어 보세요. 합계는 고정됩니다.',
                            style: TextStyle(color: muted, fontSize: 11),
                          ),
                        ),
                      ],
                    ),
                  ),
                ClipRRect(
                  borderRadius: BorderRadius.circular(14),
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Column(
                        children: [
                          label('구분', rowWidth, header: true),
                          for (var r = 0; r <= rows; r++)
                            label(
                              r == rows ? '합계' : rowNames(widget.index)[r],
                              rowWidth,
                            ),
                        ],
                      ),
                      Expanded(
                        child: Scrollbar(
                          controller: horizontal,
                          thumbVisibility: scrolling,
                          child: SingleChildScrollView(
                            controller: horizontal,
                            scrollDirection: Axis.horizontal,
                            child: Column(
                              children: [
                                Row(
                                  children: [
                                    for (var col = 0; col < cols; col++)
                                      label(
                                        columnNames(widget.index)[col],
                                        width,
                                        header: true,
                                      ),
                                  ],
                                ),
                                for (var r = 0; r <= rows; r++)
                                  Row(
                                    children: [
                                      for (var col = 0; col < cols; col++)
                                        cell(r, col, width),
                                    ],
                                  ),
                              ],
                            ),
                          ),
                        ),
                      ),
                      Column(
                        children: [
                          label('합계', sumWidth, header: true),
                          for (var r = 0; r <= rows; r++)
                            cell(r, cols, sumWidth),
                        ],
                      ),
                    ],
                  ),
                ),
              ],
            );
          },
        ),
        const SizedBox(height: 14),
        Wrap(
          spacing: 8,
          runSpacing: 4,
          crossAxisAlignment: WrapCrossAlignment.center,
          children: [
            OutlinedButton(
              onPressed: negate,
              child: const Text(
                '− / +',
                style: TextStyle(fontSize: 17, fontWeight: FontWeight.w700),
              ),
            ),
            OutlinedButton(
              onPressed: () => move(-1),
              child: const Icon(Icons.chevron_left_rounded),
            ),
            OutlinedButton(
              onPressed: () => move(1),
              child: const Text('다음 빈칸'),
            ),
          ],
        ),
        const SizedBox(height: 10),
        const Text(
          '흰 칸은 답칸 · 회색 칸은 주어진 값 · 연습용 데이터',
          style: TextStyle(fontSize: 11, color: muted),
        ),
      ],
    );
  }
}

class ResultScreen extends StatelessWidget {
  final PracticeSession session;
  const ResultScreen({super.key, required this.session});
  @override
  Widget build(BuildContext context) {
    final correct = session.correct, total = session.total;
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          '연습 기록',
          style: TextStyle(fontWeight: FontWeight.w800, fontSize: 18),
        ),
      ),
      body: SafeArea(
        top: false,
        child: Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 720),
            child: ListView(
              padding: const EdgeInsets.fromLTRB(20, 16, 20, 28),
              children: [
                const Eyebrow('ONE STEP FORWARD'),
                const SizedBox(height: 12),
                Text(
                  correct == total ? '빈틈없이 해냈어요.' : '오늘의 노력이 쌓였어요.',
                  style: const TextStyle(
                    fontSize: 28,
                    fontWeight: FontWeight.w800,
                    letterSpacing: -.8,
                  ),
                ),
                const SizedBox(height: 10),
                Text(
                  '${dateLabel(session.startedAt)}  ·  ${session.kind.title}',
                  style: const TextStyle(color: muted),
                ),
                const SizedBox(height: 24),
                Surface(
                  color: ink,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        '정답',
                        style: TextStyle(
                          color: Color(0xFFBECDBF),
                          fontSize: 12,
                        ),
                      ),
                      const SizedBox(height: 8),
                      Row(
                        crossAxisAlignment: CrossAxisAlignment.baseline,
                        textBaseline: TextBaseline.alphabetic,
                        children: [
                          Text(
                            '$correct',
                            style: numeric.copyWith(
                              fontSize: 64,
                              height: 1.15,
                              fontWeight: FontWeight.w800,
                              color: lime,
                            ),
                          ),
                          Text(
                            ' / $total',
                            style: const TextStyle(
                              fontSize: 23,
                              color: Colors.white,
                            ),
                          ),
                          const Spacer(),
                          Text(
                            '${(correct / total * 100).round()}%',
                            style: numeric.copyWith(
                              fontSize: 25,
                              color: Colors.white,
                              fontWeight: FontWeight.w700,
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 22),
                      const Divider(color: Color(0xFF51675D)),
                      const SizedBox(height: 18),
                      Row(
                        children: [
                          const Icon(
                            Icons.timer_outlined,
                            color: Colors.white,
                            size: 20,
                          ),
                          const SizedBox(width: 8),
                          Expanded(
                            child: Text(
                              durationLabel(session.elapsedSeconds!),
                              style: numeric.copyWith(
                                color: Colors.white,
                                fontWeight: FontWeight.w700,
                                fontSize: 18,
                              ),
                            ),
                          ),
                          Text(
                            '미응답 ${total - session.answered}개',
                            style: const TextStyle(
                              color: Color(0xFFBECDBF),
                              fontSize: 12,
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 12),
                const Text(
                  '실제 경과시간 기준 · 오답 벌점 없음 · 기록 저장 완료',
                  textAlign: TextAlign.center,
                  style: TextStyle(fontSize: 11, color: muted),
                ),
                const SizedBox(height: 28),
                const Eyebrow('REVIEW YOUR ANSWERS'),
                const SizedBox(height: 12),
                for (var i = 0; i < session.problems.length; i++) ...[
                  ReviewCard(
                    problem: session.problems[i],
                    index: i,
                    session: session,
                  ),
                  const SizedBox(height: 12),
                ],
                const SizedBox(height: 10),
                FilledButton(
                  onPressed: () => Navigator.pop(context),
                  child: const Text('돌아가기'),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class ReviewCard extends StatelessWidget {
  final Problem problem;
  final int index;
  final PracticeSession session;
  const ReviewCard({
    super.key,
    required this.problem,
    required this.index,
    required this.session,
  });
  String formatOperand(List<int> pair) => problem.type == ProblemType.product
      ? '${pair[0]} × ${(pair[1] / 10).toStringAsFixed(1)}'
      : '${pair[0]}/${pair[1]}';
  @override
  Widget build(BuildContext context) {
    final expected = problem.expected(index);
    final correct = expected.entries
        .where((e) => session.matches(e.key, e.value))
        .length;
    final all = correct == expected.length;
    return Surface(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Text(
                '${index + 1}'.padLeft(2, '0'),
                style: const TextStyle(
                  fontWeight: FontWeight.w800,
                  color: muted,
                ),
              ),
              const SizedBox(width: 10),
              Expanded(
                child: Text(
                  problem.type == ProblemType.table
                      ? '표 ${index + 1}'
                      : problem.type == ProblemType.order
                      ? '분수 정렬'
                      : '대소비교',
                  style: const TextStyle(fontWeight: FontWeight.w800),
                ),
              ),
              Icon(
                all ? Icons.check_circle_rounded : Icons.cancel_rounded,
                color: all ? ink : danger,
                size: 19,
              ),
              const SizedBox(width: 6),
              Text(
                '$correct/${expected.length}',
                style: TextStyle(
                  color: all ? ink : danger,
                  fontWeight: FontWeight.w700,
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),
          if (problem.type == ProblemType.table) ...[
            SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Column(
                children: [
                  for (var r = 0; r < problem.values.length; r++)
                    Row(
                      children: [
                        for (var col = 0; col < problem.width; col++)
                          reviewValue(r, col),
                        reviewCell(
                          session.memos['$index:r:$r'] ?? '·',
                          memo: true,
                        ),
                      ],
                    ),
                  Row(
                    children: [
                      for (var col = 0; col < problem.width; col++)
                        reviewCell(
                          session.memos['$index:c:$col'] ?? '·',
                          memo: true,
                        ),
                      reviewCell('메모', memo: true),
                    ],
                  ),
                ],
              ),
            ),
            const SizedBox(height: 10),
            const Text(
              '틀린 칸: 내 답 → 정답 · 파란 칸: 계산 메모\n좌우로 밀어 전체 표 확인',
              style: TextStyle(fontSize: 10, color: muted),
            ),
          ] else if (problem.type == ProblemType.order) ...[
            Wrap(
              spacing: 14,
              runSpacing: 8,
              children: List.generate(
                4,
                (i) => Text(
                  '${String.fromCharCode(65 + i)}  ${formatOperand(problem.values[i])}',
                  style: const TextStyle(fontWeight: FontWeight.w600),
                ),
              ),
            ),
            const SizedBox(height: 12),
            Text(
              '내 순서   ${orderAnswer(session.answers['$index'])}',
              style: TextStyle(color: all ? ink : danger),
            ),
            const SizedBox(height: 5),
            Text(
              '정답 순서   ${problem.ordered.map((i) => String.fromCharCode(65 + i)).join(' > ')}',
              style: const TextStyle(fontWeight: FontWeight.w700),
            ),
          ] else ...[
            Text(
              '${formatOperand(problem.values[0])}  ${problem.relation}  ${formatOperand(problem.values[1])}',
              style: numeric.copyWith(
                fontSize: 17,
                fontWeight: FontWeight.w700,
              ),
            ),
            const SizedBox(height: 10),
            Text(
              '내 답  ${session.answers['$index'] ?? '미응답'}    ·    정답  ${problem.relation}',
              style: TextStyle(color: all ? muted : danger, fontSize: 13),
            ),
          ],
        ],
      ),
    );
  }

  String orderAnswer(String? answer) => answer == null || answer.isEmpty
      ? '미응답'
      : answer
            .split(',')
            .map((i) => String.fromCharCode(65 + int.parse(i)))
            .join(' > ');
  Widget reviewCell(
    String value, {
    bool header = false,
    bool wrong = false,
    bool memo = false,
    bool totalRow = false,
    bool totalCol = false,
  }) => Container(
    width: 64,
    height: 54,
    alignment: Alignment.center,
    padding: const EdgeInsets.symmetric(horizontal: 3),
    decoration: BoxDecoration(
      color: memo
          ? const Color(0xFFEAF1F8)
          : wrong
          ? const Color(0xFFFFEEE8)
          : header
          ? const Color(0xFFEFF2EA)
          : Colors.white,
      border: Border(
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
    child: Text(
      value,
      textAlign: TextAlign.center,
      style: TextStyle(
        fontSize: header ? 10 : 13,
        fontWeight: FontWeight.w600,
        color: memo
            ? const Color(0xFF365D81)
            : wrong
            ? danger
            : ink,
      ),
    ),
  );
  Widget reviewValue(int row, int col) {
    final cell = row * problem.width + col,
        key = problem.answerKey(index, row * problem.width + col);
    final value = '${problem.values[row][col]}';
    final wrong = problem.hidden.contains(cell) && !session.matches(key, value);
    final input = session.answers[key];
    return reviewCell(
      wrong
          ? '${(input == null || input.trim().isEmpty) ? '미응답' : input}\n→ $value'
          : value,
      wrong: wrong,
      totalRow: row == problem.values.length - 1,
      totalCol: col == problem.width - 1,
    );
  }
}
