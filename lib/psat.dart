import 'grit_dialog.dart';
import 'word_text.dart';
import 'dart:async';
import 'dart:math' as math;
import 'dart:ui' show DisplayFeatureType;
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'main.dart' show Surface, ink, muted, lime, paper, danger, toast;
import 'store.dart';
import 'psat_model.dart';
import 'psat_sets.dart';
import 'psat_text.dart';

String psatTime(int s) => '${s ~/ 60}분 ${s % 60}초';
const marks = ['①', '②', '③', '④', '⑤'];

class PsatLibrary extends StatefulWidget {
  final AppController controller;
  final String subject;
  const PsatLibrary({
    super.key,
    required this.controller,
    required this.subject,
  });
  @override
  State<PsatLibrary> createState() => _PsatLibraryState();
}

class _PsatLibraryState extends State<PsatLibrary> {
  late Future<PsatCatalog> catalog = loadPsatCatalog();
  bool onlyWrong = false;
  @override
  Widget build(BuildContext context) => FutureBuilder<PsatCatalog>(
    future: catalog,
    builder: (context, snap) {
      if (snap.hasError) {
        return Center(
          child: TextButton(
            onPressed: () => setState(() => catalog = loadPsatCatalog()),
            child: const WordText('문항을 읽지 못했어요 · 다시 읽기'),
          ),
        );
      }
      if (!snap.hasData) {
        return const Center(child: CircularProgressIndicator());
      }
      final allSets = snap.data!.forSubject(widget.subject);
      return ListenableBuilder(
        listenable: widget.controller,
        builder: (context, _) {
          final progress = PsatProgress(widget.controller.psatRecords);
          final visible = allSets.where(
            (set) => !onlyWrong || progress.wrong(set) > 0,
          );
          return LayoutBuilder(
            builder: (context, box) => ListView(
              padding: const EdgeInsets.all(20),
              children: [
                const WordText(
                  '읽고, 판단하고,\n근거까지.',
                  style: TextStyle(
                    fontSize: 29,
                    fontWeight: FontWeight.w800,
                    height: 1.25,
                  ),
                ),
                const SizedBox(height: 12),
                WordText(
                  '${widget.subject} · ${allSets.length}개 Set · ${allSets.length * 10}문항\n하루 15분, 풀 수 있는 만큼 풀고 해설까지 읽어보세요.',
                  style: const TextStyle(color: muted, height: 1.6),
                ),
                const SizedBox(height: 16),
                _wrongFilter(onlyWrong, (v) => setState(() => onlyWrong = v)),
                const SizedBox(height: 16),
                if (visible.isEmpty)
                  const Padding(
                    padding: EdgeInsets.all(24),
                    child: WordText('이 과목에서 다시 볼 오답이 없어요.'),
                  ),
                Wrap(
                  spacing: 12,
                  runSpacing: 12,
                  children: [
                    for (final set in visible)
                      SizedBox(
                        width: _psatCardWidth(box.maxWidth),
                        child: _setCard(context, set, progress, snap.data!),
                      ),
                  ],
                ),
                const SizedBox(height: 20),
                TextButton.icon(
                  onPressed: () => Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) =>
                          PsatHistory(controller: widget.controller),
                    ),
                  ),
                  icon: const Icon(Icons.history_rounded),
                  label: const WordText('기출 풀이 기록 전체 보기'),
                ),
              ],
            ),
          );
        },
      );
    },
  );

  Widget _setCard(
    BuildContext context,
    PsatSet set,
    PsatProgress progress,
    PsatCatalog catalog,
  ) {
    final count = progress.completed(set);
    final complete = count == 10;
    final scheme = Theme.of(context).colorScheme;
    return Card(
      key: ValueKey('psat-set-${set.id}'),
      margin: EdgeInsets.zero,
      elevation: 0,
      color: complete
          ? Color.alphaBlend(
              scheme.secondary.withValues(alpha: 0.25),
              scheme.surface,
            )
          : Colors.white,
      child: InkWell(
        borderRadius: BorderRadius.circular(12),
        onTap: () => Navigator.push(
          context,
          MaterialPageRoute(
            builder: (_) => PsatSetScreen(
              controller: widget.controller,
              catalog: catalog,
              set: set,
              onlyWrong: onlyWrong,
            ),
          ),
        ),
        child: Padding(
          padding: const EdgeInsets.all(18),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              WordText(
                '${set.title} ($count / 10)',
                style: const TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.w700,
                ),
              ),
              const SizedBox(height: 8),
              WordText(
                '난도 · ${set.difficulty}',
                style: const TextStyle(color: muted),
              ),
              const SizedBox(height: 12),
              Wrap(
                spacing: 12,
                runSpacing: 8,
                crossAxisAlignment: WrapCrossAlignment.center,
                children: [
                  if (complete)
                    const Icon(Icons.check_circle_outline, size: 20),
                  WordText(
                    complete ? '풀이 완료' : '채점한 문항 $count개',
                    style: const TextStyle(
                      color: ink,
                      fontWeight: FontWeight.w700,
                    ),
                  ),
                  if (progress.wrong(set) > 0)
                    WordText(
                      '다시 볼 오답 ${progress.wrong(set)}개',
                      style: const TextStyle(color: danger),
                    ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}

double _psatCardWidth(double width) =>
    width >= 700 ? (width - 52) / 2 : width - 40;

Widget _wrongFilter(bool selected, ValueChanged<bool> onSelected) => Align(
  alignment: Alignment.centerLeft,
  child: FilterChip(
    label: const WordText('다시 볼 오답'),
    selected: selected,
    onSelected: onSelected,
  ),
);

class PsatSetScreen extends StatefulWidget {
  final AppController controller;
  final PsatCatalog catalog;
  final PsatSet set;
  final bool onlyWrong;
  const PsatSetScreen({
    super.key,
    required this.controller,
    required this.catalog,
    required this.set,
    this.onlyWrong = false,
  });
  @override
  State<PsatSetScreen> createState() => _PsatSetScreenState();
}

class _PsatSetScreenState extends State<PsatSetScreen> {
  late bool onlyWrong = widget.onlyWrong;
  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(
      title: WordText('${widget.set.subject} · ${widget.set.title}'),
    ),
    body: SafeArea(
      child: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 1100),
          child: ListenableBuilder(
            listenable: widget.controller,
            builder: (context, _) {
              final progress = PsatProgress(widget.controller.psatRecords);
              final ids = widget.set.questionIds.where(
                (id) => !onlyWrong || progress.latest[id]?.correct == false,
              );
              return LayoutBuilder(
                builder: (context, box) => ListView(
                  padding: const EdgeInsets.all(20),
                  children: [
                    WordText(
                      '${widget.set.title} (${progress.completed(widget.set)} / 10)',
                      style: const TextStyle(
                        fontSize: 24,
                        fontWeight: FontWeight.w800,
                      ),
                    ),
                    const SizedBox(height: 12),
                    const WordText(
                      '오답도 풀이 완료에 포함돼요. 같은 문항을 다시 풀어도 완료 수는 늘어나지 않아요.',
                      style: TextStyle(color: muted, height: 1.6),
                    ),
                    const SizedBox(height: 16),
                    _wrongFilter(
                      onlyWrong,
                      (v) => setState(() => onlyWrong = v),
                    ),
                    const SizedBox(height: 16),
                    if (ids.isEmpty) const WordText('이 Set에서 다시 볼 오답이 없어요.'),
                    Wrap(
                      spacing: 12,
                      runSpacing: 12,
                      children: [
                        for (final id in ids)
                          SizedBox(
                            width: _psatCardWidth(box.maxWidth),
                            child: _PsatQuestionCard(
                              controller: widget.controller,
                              question: widget.catalog.questions[id]!,
                              attempt: progress.latest[id],
                            ),
                          ),
                      ],
                    ),
                  ],
                ),
              );
            },
          ),
        ),
      ),
    ),
  );
}

class _PsatQuestionCard extends StatelessWidget {
  final AppController controller;
  final PsatQuestion question;
  final PsatAttempt? attempt;
  const _PsatQuestionCard({
    required this.controller,
    required this.question,
    this.attempt,
  });
  @override
  Widget build(BuildContext context) {
    final q = question;
    return Card(
      key: ValueKey('psat-question-${q.id}'),
      margin: EdgeInsets.zero,
      elevation: 0,
      color: Colors.white,
      child: InkWell(
        borderRadius: BorderRadius.circular(12),
        onTap: () => Navigator.push(
          context,
          MaterialPageRoute(
            builder: (_) => PsatReader(
              controller: controller,
              question: attempt?.question ?? q,
              review: attempt,
            ),
          ),
        ),
        child: Padding(
          padding: const EdgeInsets.all(18),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              WordText(
                '${q.subject} · 원문 ${q.number}번',
                style: const TextStyle(color: muted, fontSize: 12),
              ),
              const SizedBox(height: 8),
              WordText(
                q.title,
                style: const TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.w700,
                  height: 1.4,
                ),
              ),
              const SizedBox(height: 12),
              Wrap(
                spacing: 12,
                runSpacing: 8,
                children: [
                  WordText(q.tag, style: const TextStyle(color: muted)),
                  WordText(
                    attempt == null
                        ? '미풀이'
                        : attempt!.correct
                        ? '정답 · 해설 복습'
                        : '오답 · 해설 복습',
                    style: TextStyle(
                      color: attempt?.correct == false ? danger : ink,
                      fontWeight: FontWeight.w700,
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class PsatHistory extends StatelessWidget {
  final AppController controller;
  const PsatHistory({super.key, required this.controller});
  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(title: const WordText('기출 풀이 기록')),
    body: SafeArea(
      child: ListenableBuilder(
        listenable: controller,
        builder: (context, _) => ListView(
          padding: const EdgeInsets.all(20),
          children: [
            if (controller.psatRecords.isEmpty)
              const WordText('채점한 문항이 여기에 저장돼요.'),
            for (final a in controller.psatRecords)
              Card(
                child: ListTile(
                  leading: Icon(
                    a.correct ? Icons.check_circle_outline : Icons.replay,
                    color: a.correct ? ink : danger,
                  ),
                  title: WordText(
                    '${a.question.subject} ${a.question.number}번 · ${a.question.title}',
                  ),
                  subtitle: WordText(
                    '${a.completedAt.toLocal().toString().substring(0, 16)} · ${psatTime(a.seconds)}',
                  ),
                  onTap: () => Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => PsatReader(
                        controller: controller,
                        question: a.question,
                        review: a,
                      ),
                    ),
                  ),
                ),
              ),
          ],
        ),
      ),
    ),
  );
}

class PsatReader extends StatefulWidget {
  final AppController controller;
  final PsatQuestion question;
  final PsatAttempt? review;
  const PsatReader({
    super.key,
    required this.controller,
    required this.question,
    this.review,
  });
  @override
  State<PsatReader> createState() => _PsatReaderState();
}

class _PsatReaderState extends State<PsatReader> {
  late final DateTime started = DateTime.now();
  Timer? timer;
  int? selected;
  PsatAttempt? done;
  bool saving = false;
  bool allowExit = false;
  double fontSize = 17;
  bool? sideBySide;
  final compactScroll = ScrollController();
  final passageScroll = ScrollController();
  final answerScroll = ScrollController();
  final resultKey = GlobalKey();
  PsatQuestion get q => widget.question;
  bool get hasFigures => q.figures.isNotEmpty;
  int get seconds =>
      done?.seconds ??
      DateTime.now().difference(started).inSeconds.clamp(0, 99999999);
  @override
  void initState() {
    super.initState();
    done = widget.review;
    selected = done?.selected;
    timer = Timer.periodic(const Duration(seconds: 1), (_) {
      if (mounted && done == null) setState(() {});
    });
  }

  @override
  void dispose() {
    timer?.cancel();
    compactScroll.dispose();
    passageScroll.dispose();
    answerScroll.dispose();
    super.dispose();
  }

  Future<void> submit() async {
    if (selected == null || saving || done != null) return;
    final end = DateTime.now();
    final attempt = PsatAttempt(
      id: '${end.microsecondsSinceEpoch}-${q.id}',
      question: q,
      selected: selected!,
      startedAt: started,
      completedAt: end,
      seconds: seconds,
    );
    setState(() => saving = true);
    try {
      await widget.controller.savePsat(attempt);
      if (!mounted) return;
      setState(() {
        done = attempt;
        saving = false;
      });
      timer?.cancel();
      WidgetsBinding.instance.addPostFrameCallback((_) {
        final target = resultKey.currentContext;
        if (mounted && target != null) {
          Scrollable.ensureVisible(
            target,
            duration: const Duration(milliseconds: 250),
            alignment: 0.05,
          );
        }
      });
    } catch (_) {
      if (mounted) {
        setState(() => saving = false);
        toast(context, '저장하지 못했어요. 선택은 유지됩니다. 다시 시도해 주세요.');
      }
    }
  }

  Future<void> leave() async {
    if (saving) return;
    final discard = await showGritDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const WordText('문제 풀이를 그만둘까요?'),
        content: const WordText(
          '아직 채점하지 않은 답안과 시간은 저장되지 않아요. 이전 완료 기록은 그대로 유지돼요.',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx, false),
            child: const WordText('계속 풀기'),
          ),
          TextButton(
            onPressed: () => Navigator.pop(ctx, true),
            child: const WordText('그만두기'),
          ),
        ],
      ),
    );
    if (discard == true && mounted) {
      setState(() => allowExit = true);
      Navigator.pop(context);
    }
  }

  @override
  Widget build(BuildContext context) => PopScope(
    canPop: done != null || allowExit,
    onPopInvokedWithResult: (didPop, _) {
      if (!didPop) unawaited(leave());
    },
    child: Scaffold(
      appBar: AppBar(
        title: WordText(
          '${q.subject} · ${q.number}번',
          style: const TextStyle(fontSize: 18),
        ),
        actions: [
          if (MediaQuery.sizeOf(context).width >= 720 &&
              MediaQuery.sizeOf(context).height >= 520)
            IconButton(
              key: const ValueKey('psat-layout-toggle'),
              tooltip: (sideBySide ?? !hasFigures) ? '크게 읽기' : '나란히 보기',
              icon: Icon(
                (sideBySide ?? !hasFigures)
                    ? Icons.width_full_outlined
                    : Icons.view_column_outlined,
              ),
              onPressed: () => setState(() {
                sideBySide = !(sideBySide ?? !hasFigures);
              }),
            ),
          PopupMenuButton<double>(
            tooltip: '글자 크기',
            icon: const Icon(Icons.text_fields),
            initialValue: fontSize,
            onSelected: (v) => setState(() => fontSize = v),
            itemBuilder: (_) => [
              for (final x in [17.0, 19.0, 21.0])
                PopupMenuItem(value: x, child: WordText('글자 크기 ${x.toInt()}')),
            ],
          ),
          IconButton(
            tooltip: '공식 문제 원문',
            icon: const Icon(Icons.article_outlined),
            onPressed: () => Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => _Original(q)),
            ),
          ),
        ],
      ),
      body: SafeArea(
        child: LayoutBuilder(
          builder: (context, box) {
            final wide = box.maxWidth >= 720 && box.maxHeight >= 420;
            final mq = MediaQuery.of(context);
            double gap = 12;
            double left = hasFigures
                ? box.maxWidth - gap - (box.maxWidth * 0.36).clamp(300.0, 440.0)
                : (box.maxWidth - gap) * 0.55;
            bool separatingHinge = false;
            for (final feature in mq.displayFeatures) {
              if (feature.type == DisplayFeatureType.hinge &&
                  feature.bounds.width > 0 &&
                  feature.bounds.height > feature.bounds.width &&
                  feature.bounds.left > 0) {
                final g = feature.bounds.width < 12
                    ? 12.0
                    : feature.bounds.width;
                final l = feature.bounds.center.dx - mq.padding.left - g / 2;
                if (l >= 280 && box.maxWidth - l - g >= 280) {
                  left = l;
                  gap = g;
                  separatingHinge = true;
                  break;
                }
              }
            }
            final split =
                wide && (separatingHinge || (sideBySide ?? !hasFigures));
            if (split) {
              return Row(
                key: const ValueKey('psat-reading-split'),
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  SizedBox(
                    width: left,
                    child: readingPane(
                      showPassage: true,
                      showAnswers: false,
                      controller: passageScroll,
                      padding: EdgeInsets.fromLTRB(
                        hasFigures ? 8 : 12,
                        8,
                        8,
                        32,
                      ),
                    ),
                  ),
                  SizedBox(width: gap),
                  Expanded(
                    child: readingPane(
                      showPassage: false,
                      showAnswers: true,
                      controller: answerScroll,
                      padding: const EdgeInsets.fromLTRB(8, 8, 12, 32),
                    ),
                  ),
                ],
              );
            }
            return Center(
              child: ConstrainedBox(
                constraints: BoxConstraints(maxWidth: hasFigures ? 1100 : 680),
                child: readingPane(
                  showPassage: true,
                  showAnswers: true,
                  key: const ValueKey('psat-reading-column'),
                  controller: compactScroll,
                  padding: EdgeInsets.fromLTRB(
                    hasFigures ? 8 : 12,
                    8,
                    hasFigures ? 8 : 12,
                    32,
                  ),
                ),
              ),
            );
          },
        ),
      ),
    ),
  );
  Widget prose(String text, {bool bold = false}) => PsatText(
    text,
    style: TextStyle(
      fontSize: fontSize,
      height: 1.75,
      fontWeight: bold ? FontWeight.w700 : FontWeight.w400,
    ),
  );
  int get _figuresBeforeBody =>
      (q.data['bodyAfterFigureCount'] as int?) ??
      (q.data['figuresAfterBody'] == true ? 0 : q.figures.length);

  List<Widget> passage({double figureScale = 1}) => [
    PsatText(
      '${q.data['source']} · ${q.data['book']} 책형',
      style: const TextStyle(color: muted, fontSize: 12, height: 1.5),
    ),
    const SizedBox(height: 12),
    prose(q.prompt, bold: true),
    const SizedBox(height: 18),
    if ((q.data['bodyBeforeFigures'] as String? ?? '').isNotEmpty) ...[
      Surface(
        padding: const EdgeInsets.all(12),
        child: SelectionArea(
          child: PsatPassage(
            q.data['bodyBeforeFigures'] as String,
            fontSize: fontSize,
            underlines: q.underlines,
            underlineLabelAnchors: q.data['underlineLabelAnchors'] == true,
          ),
        ),
      ),
      const SizedBox(height: 14),
    ],
    for (final figure in q.figures.take(_figuresBeforeBody)) ...[
      _figure(figure, scale: figureScale),
      const SizedBox(height: 14),
    ],
    if (q.body.isNotEmpty || q.tables.isNotEmpty)
      Surface(
        padding: const EdgeInsets.all(12),
        child: SelectionArea(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [...passageContent()],
          ),
        ),
      ),
    for (final figure in q.figures.skip(_figuresBeforeBody)) ...[
      const SizedBox(height: 14),
      _figure(figure, scale: figureScale),
    ],
  ];
  Widget _figure(Map<String, dynamic> figure, {double scale = 1}) => Column(
    crossAxisAlignment: CrossAxisAlignment.stretch,
    children: [
      Semantics(
        button: true,
        label: '${figure['caption']} 확대 보기',
        child: InkWell(
          key: ValueKey(figure['asset']),
          onTap: () => Navigator.push(
            context,
            MaterialPageRoute(builder: (_) => _FigureZoom(figure)),
          ),
          child: ColoredBox(
            color: Colors.white,
            child: AspectRatio(
              aspectRatio:
                  (figure['width'] as num) / (figure['height'] as num) / scale,
              child: Image.asset(
                figure['asset'] as String,
                fit: BoxFit.contain,
                filterQuality: FilterQuality.high,
                errorBuilder: (_, _, _) =>
                    const Center(child: WordText('자료 이미지를 읽지 못했어요.')),
              ),
            ),
          ),
        ),
      ),
      const SizedBox(height: 4),
      const Align(
        alignment: Alignment.centerRight,
        child: WordText(
          '표·그림을 누르면 확대',
          style: TextStyle(fontSize: 11, color: muted),
        ),
      ),
    ],
  );

  List<Widget> passageContent() {
    final tables = q.tables;
    final result = <Widget>[];
    // Old snapshots keep their original body-then-tables layout.
    if (tables.any((table) => table['afterParagraph'] != null)) {
      final paragraphs = q.body.split(RegExp(r'\n\s*\n'));
      for (var i = 0; i < paragraphs.length; i++) {
        result.add(
          PsatPassage(
            paragraphs[i],
            fontSize: fontSize,
            underlines: q.underlines,
            underlineLabelAnchors: q.data['underlineLabelAnchors'] == true,
          ),
        );
        for (final table in tables.where(
          (table) => table['afterParagraph'] == i,
        )) {
          result.addAll([const SizedBox(height: 8), _table(table)]);
        }
      }
    } else {
      result.add(
        PsatPassage(
          q.body,
          fontSize: fontSize,
          underlines: q.underlines,
          underlineLabelAnchors: q.data['underlineLabelAnchors'] == true,
        ),
      );
    }
    for (final table in tables.where(
      (table) => table['afterParagraph'] == null,
    )) {
      result.addAll([const SizedBox(height: 8), _table(table)]);
    }
    return result;
  }

  Widget _table(Map<String, dynamic> table) {
    final columns = List<String>.from(table['columns'] as List);
    final rows = (table['rows'] as List)
        .map((r) => List<String>.from(r as List))
        .toList();
    return Column(
      key: ValueKey('psat-table-${q.id}-${table["caption"]}'),
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        prose(table['caption'] as String, bold: true),
        const SizedBox(height: 10),
        for (final row in rows)
          Container(
            margin: const EdgeInsets.only(bottom: 8),
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: paper,
              borderRadius: BorderRadius.circular(12),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                prose('${columns[0]} ${row[0]}', bold: true),
                for (var i = 1; i < columns.length; i++)
                  prose('${columns[i]}: ${row[i]}'),
              ],
            ),
          ),
      ],
    );
  }

  double textHeight(String text, double width, TextStyle style) {
    final effective = DefaultTextStyle.of(context).style.merge(style);
    final painter = TextPainter(
      text: TextSpan(
        style: effective,
        children: psatWordSpans(
          [TextSpan(text: text)],
          style: effective,
          width: width,
          scaler: MediaQuery.textScalerOf(context),
          direction: Directionality.of(context),
        ),
      ),
      textDirection: Directionality.of(context),
      textScaler: MediaQuery.textScalerOf(context),
    )..layout(maxWidth: width);
    final h = painter.height;
    painter.dispose();
    return h;
  }

  double get compactChoiceHeight => math.max(
    64,
    MediaQuery.textScalerOf(context).scale(fontSize) * 1.4 +
        MediaQuery.textScalerOf(context).scale(12) * 1.5 +
        18,
  );
  int choiceColumns(double width) {
    double longest = 0;
    for (final choice in q.choices) {
      final painter = TextPainter(
        text: TextSpan(
          text: choice,
          style: DefaultTextStyle.of(
            context,
          ).style.merge(TextStyle(fontSize: fontSize)),
        ),
        textDirection: Directionality.of(context),
        textScaler: MediaQuery.textScalerOf(context),
      )..layout();
      longest = math.max(longest, painter.width);
      painter.dispose();
    }
    final count = ((width + 6) / math.max(58, longest + 20)).floor().clamp(
      1,
      5,
    );
    return count == 4 ? 3 : count;
  }

  Widget option(int i, {bool compact = false}) => Padding(
    padding: EdgeInsets.only(bottom: compact ? 0 : 10),
    child: Semantics(
      selected: selected == i + 1,
      button: true,
      child: OutlinedButton(
        key: ValueKey('psat-option-${i + 1}'),
        onPressed: done != null || saving
            ? null
            : () => setState(() => selected = i + 1),
        style: OutlinedButton.styleFrom(
          alignment: compact ? Alignment.center : Alignment.centerLeft,
          padding: EdgeInsets.all(compact ? 6 : 14),
          backgroundColor: selected == i + 1
              ? lime.withValues(alpha: 0.45)
              : Colors.white,
          foregroundColor: ink,
          disabledForegroundColor: ink,
          side: BorderSide(
            color: selected == i + 1 ? ink : const Color(0xFFE1E5DD),
            width: selected == i + 1 ? 2 : 1,
          ),
        ),
        child: compact
            ? Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  WordText(marks[i], style: const TextStyle(fontSize: 12)),
                  const SizedBox(height: 3),
                  WordText(
                    q.choices[i],
                    textAlign: TextAlign.center,
                    style: TextStyle(fontSize: fontSize, height: 1.4),
                  ),
                ],
              )
            : Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  WordText(marks[i], style: TextStyle(fontSize: fontSize)),
                  const SizedBox(width: 10),
                  Expanded(child: prose(q.choices[i])),
                ],
              ),
      ),
    ),
  );

  Widget readingPane({
    Key? key,
    required ScrollController controller,
    required EdgeInsets padding,
    required bool showPassage,
    required bool showAnswers,
  }) {
    if (!hasFigures) {
      return ListView(
        key: key,
        controller: controller,
        padding: padding,
        children: [
          if (showPassage) ...passage(),
          if (showPassage && showAnswers) const SizedBox(height: 18),
          if (showAnswers) ...answers(),
        ],
      );
    }
    return LayoutBuilder(
      key: key,
      builder: (context, box) {
        final width = box.maxWidth - padding.horizontal;
        // Reserve real text heights before scaling figures. Never shrink body text.
        double figureBudget = box.maxHeight * 0.65;
        if (q.body.isEmpty && q.tables.isEmpty && done == null) {
          double occupied = padding.vertical + 12 + 18 + q.figures.length * 36;
          occupied += textHeight(
            '${q.data['source']} · ${q.data['book']} 책형',
            width,
            const TextStyle(fontSize: 12, height: 1.5),
          );
          occupied += textHeight(
            q.prompt,
            width,
            TextStyle(
              fontSize: fontSize,
              height: 1.75,
              fontWeight: FontWeight.w700,
            ),
          );
          if (showAnswers && q.choices.every((c) => c.length <= 12)) {
            final rows = (5 / choiceColumns(width)).ceil();
            occupied +=
                18 + 24 + 12 + rows * compactChoiceHeight + (rows - 1) * 6;
            if (q.data['choiceNote'] is String) {
              occupied +=
                  textHeight(
                    q.data['choiceNote'] as String,
                    width,
                    TextStyle(
                      fontSize: fontSize,
                      height: 1.75,
                      fontWeight: FontWeight.w700,
                    ),
                  ) +
                  12;
            }
            occupied +=
                6 +
                54 +
                10 +
                textHeight(
                  '선택은 채점 전까지 바꿀 수 있어요. 채점한 문항만 기록에 저장됩니다.',
                  width,
                  const TextStyle(fontSize: 14, height: 1.5),
                );
          } else if (showAnswers) {
            occupied += box.maxHeight * 0.35;
          }
          figureBudget = math.max(180, box.maxHeight - occupied);
        }
        final naturalHeight = q.figures.fold<double>(
          0,
          (sum, f) => sum + width * (f['height'] as num) / (f['width'] as num),
        );
        // Keep phone figures near full width; a large screen can fit more by shrinking further.
        final figureScale = (figureBudget / naturalHeight).clamp(
          width >= 600 ? 0.50 : 0.80,
          1.0,
        );
        return SingleChildScrollView(
          controller: controller,
          padding: padding,
          child: ConstrainedBox(
            constraints: BoxConstraints(
              minHeight: math.max(0, box.maxHeight - padding.vertical),
            ),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                if (showPassage) ...passage(figureScale: figureScale),
                if (showPassage && showAnswers) const SizedBox(height: 18),
                if (showAnswers) ...answers(),
              ],
            ),
          ),
        );
      },
    );
  }

  List<Widget> answers() => [
    Row(
      children: [
        Expanded(
          child: WordText(
            done == null
                ? '풀이 중 · ${psatTime(seconds)}'
                : '풀이 시간 · ${psatTime(seconds)}',
            style: const TextStyle(color: muted),
          ),
        ),
        if (saving)
          const SizedBox(
            width: 18,
            height: 18,
            child: CircularProgressIndicator(strokeWidth: 2),
          ),
      ],
    ),
    const SizedBox(height: 12),
    if (q.data['choiceNote'] is String) ...[
      prose(q.data['choiceNote'] as String, bold: true),
      const SizedBox(height: 12),
    ],
    if (hasFigures && q.choices.every((c) => c.length <= 12))
      LayoutBuilder(
        builder: (context, box) {
          final columns = choiceColumns(box.maxWidth);
          final width = (box.maxWidth - (columns - 1) * 6) / columns;
          return Wrap(
            spacing: 6,
            runSpacing: 6,
            children: [
              for (var i = 0; i < q.choices.length; i++)
                SizedBox(
                  width: width,
                  height: compactChoiceHeight,
                  child: option(i, compact: true),
                ),
            ],
          );
        },
      )
    else
      for (var i = 0; i < q.choices.length; i++) option(i),
    if (done == null) ...[
      const SizedBox(height: 6),
      FilledButton(
        key: const ValueKey('psat-submit'),
        onPressed: selected == null || saving ? null : submit,
        child: const WordText('채점하고 해설 읽기'),
      ),
      const SizedBox(height: 10),
      const WordText(
        '선택은 채점 전까지 바꿀 수 있어요. 채점한 문항만 기록에 저장됩니다.',
        style: TextStyle(color: muted, height: 1.5),
      ),
    ],
    if (done != null) ...[
      const SizedBox(height: 16),
      Surface(
        key: resultKey,
        color: done!.correct
            ? const Color(0xFFE8EEDB)
            : const Color(0xFFF8E9E5),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            WordText(
              done!.correct ? '정답이에요.' : '근거를 다시 짚어봐요.',
              style: const TextStyle(fontWeight: FontWeight.w800, fontSize: 21),
            ),
            const SizedBox(height: 8),
            prose(
              '내 선택 ${marks[done!.selected - 1]} · 정답 ${marks[q.answer - 1]}',
            ),
          ],
        ),
      ),
      const SizedBox(height: 22),
      prose('풀이의 흐름', bold: true),
      const SizedBox(height: 12),
      for (var i = 0; i < q.steps.length; i++) ...[
        PsatListItem(
          marker: '${i + 1}.',
          text: q.steps[i],
          style: TextStyle(
            fontSize: fontSize,
            height: 1.75,
            fontWeight: FontWeight.w400,
          ),
        ),
        const SizedBox(height: 16),
      ],
      const Divider(),
      const SizedBox(height: 16),
      prose('보기별 판단', bold: true),
      const SizedBox(height: 12),
      for (var i = 0; i < q.reasons.length; i++) ...[
        prose('${marks[i]} ${i + 1 == q.answer ? '정답' : '오답'}', bold: true),
        prose(q.reasons[i]),
        const SizedBox(height: 16),
      ],
      Surface(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            prose('놓치기 쉬운 지점', bold: true),
            const SizedBox(height: 8),
            prose(q.data['pitfall'] as String),
            const SizedBox(height: 16),
            prose('다음 문제에도 쓰는 방법', bold: true),
            const SizedBox(height: 8),
            prose(q.data['transfer'] as String),
          ],
        ),
      ),
      const SizedBox(height: 18),
      ExpansionTile(
        tilePadding: EdgeInsets.zero,
        title: const WordText('출처와 편집 안내'),
        children: [
          Align(
            alignment: Alignment.centerLeft,
            child: WordText(
              q.data['editNote'] as String,
              style: const TextStyle(color: muted, height: 1.6),
            ),
          ),
          TextButton(
            onPressed: () async {
              await Clipboard.setData(
                ClipboardData(
                  text:
                      '문제: ${q.data['sourceUrl']}\n최종 정답: ${q.data['answerUrl']}',
                ),
              );
              if (mounted) toast(context, '공식 문제·최종 정답 주소를 복사했어요.');
            },
            child: const WordText('공식 출처 주소 복사'),
          ),
        ],
      ),
      const SizedBox(height: 12),
      OutlinedButton(
        onPressed: () => Navigator.pushReplacement(
          context,
          MaterialPageRoute(
            builder: (_) =>
                PsatReader(controller: widget.controller, question: q),
          ),
        ),
        child: const WordText('이 문제 다시 풀기'),
      ),
      const SizedBox(height: 10),
      FilledButton(
        onPressed: () => Navigator.pop(context),
        child: const WordText('목록으로'),
      ),
    ],
  ];
}

class _Original extends StatelessWidget {
  final PsatQuestion q;
  const _Original(this.q);
  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(title: WordText('공식 원문 · ${q.number}번')),
    body: SafeArea(
      child: Column(
        children: [
          const Padding(
            padding: EdgeInsets.all(12),
            child: WordText('두 손가락으로 확대하고, 확대한 화면을 움직여 읽으세요.'),
          ),
          Expanded(
            child: InteractiveViewer(
              minScale: 1,
              maxScale: 6,
              child: Center(
                child: Image.asset(
                  q.original,
                  fit: BoxFit.contain,
                  errorBuilder: (_, _, _) => const WordText('원문 이미지를 읽지 못했어요.'),
                ),
              ),
            ),
          ),
        ],
      ),
    ),
  );
}

class _FigureZoom extends StatelessWidget {
  final Map<String, dynamic> figure;
  const _FigureZoom(this.figure);
  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(title: const WordText('자료 확대')),
    body: SafeArea(
      child: Column(
        children: [
          const Padding(
            padding: EdgeInsets.all(8),
            child: WordText('두 손가락으로 확대하고 움직여 읽으세요.'),
          ),
          Expanded(
            child: InteractiveViewer(
              minScale: 1,
              maxScale: 8,
              child: Center(
                child: Image.asset(
                  figure['asset'] as String,
                  fit: BoxFit.contain,
                  filterQuality: FilterQuality.high,
                ),
              ),
            ),
          ),
        ],
      ),
    ),
  );
}
