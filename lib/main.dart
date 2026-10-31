import 'grit_dialog.dart';
import 'word_text.dart';
import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'model.dart';
import 'store.dart';
import 'practice.dart';
import 'guide.dart';
import 'psat.dart';

const ink = Color(0xFF203B33);
const muted = Color(0xFF69776E);
const paper = Color(0xFFF6F5F0);
const lime = Color(0xFFD6EF88);
const line = Color(0xFFE1E5DD);
const danger = Color(0xFFB44937);
const numeric = TextStyle(fontFeatures: [FontFeature.tabularFigures()]);

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final controller = AppController(DevicePersistence());
  await controller.load();
  runApp(GritApp(controller: controller));
}

class VitaminHistoryDialog extends StatelessWidget {
  final SetKind kind;
  final List<PracticeSession> records;
  const VitaminHistoryDialog({
    super.key,
    required this.kind,
    required this.records,
  });

  @override
  Widget build(BuildContext context) {
    final sessions =
        records.where((r) => r.kind == kind && r.completedAt != null).toList()
          ..sort((a, b) {
            final byStart = a.startedAt.compareTo(b.startedAt);
            return byStart != 0 ? byStart : a.id.compareTo(b.id);
          });
    Widget cells(
      String round,
      String accuracy,
      String minutes, {
      bool header = false,
    }) => Row(
      children: [
        for (final value in [round, accuracy, minutes])
          Expanded(
            child: WordText(
              value,
              textAlign: TextAlign.center,
              style: numeric.copyWith(
                fontSize: header ? 12 : 15,
                fontWeight: header ? FontWeight.w500 : FontWeight.w700,
                color: header ? muted : ink,
              ),
            ),
          ),
      ],
    );
    return Dialog(
      key: const ValueKey('vitamin-history-dialog'),
      insetPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 20),
      child: SizedBox(
        width: 480,
        height: MediaQuery.sizeOf(context).height * .72,
        child: Padding(
          padding: const EdgeInsets.fromLTRB(16, 8, 16, 16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Row(
                children: [
                  Expanded(
                    child: WordText(
                      '${kind.title} 기록',
                      style: const TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.w800,
                      ),
                    ),
                  ),
                  IconButton(
                    tooltip: '기록 닫기',
                    onPressed: () => Navigator.pop(context),
                    icon: const Icon(Icons.close_rounded),
                  ),
                ],
              ),
              const WordText(
                '완료한 세트 기준 · 최근 회차부터',
                style: TextStyle(fontSize: 12, color: muted),
              ),
              const SizedBox(height: 16),
              cells('회차', '정답률', '소요시간(분)', header: true),
              const Divider(height: 24),
              Expanded(
                child: sessions.isEmpty
                    ? const Center(child: WordText('아직 완료한 연습이 없어요.'))
                    : Scrollbar(
                        child: ListView.separated(
                          key: ValueKey('vitamin-history-list-${kind.name}'),
                          padding: const EdgeInsets.only(bottom: 8),
                          itemCount: sessions.length,
                          separatorBuilder: (_, _) => const Divider(height: 1),
                          itemBuilder: (_, index) {
                            final round = sessions.length - index;
                            final session = sessions[round - 1];
                            return Padding(
                              key: ValueKey('vitamin-record-${session.id}'),
                              padding: const EdgeInsets.symmetric(vertical: 16),
                              child: cells(
                                '$round회차',
                                '${(session.correct / session.total * 100).toStringAsFixed(1)}%',
                                (session.elapsedSeconds! / 60).toStringAsFixed(
                                  2,
                                ),
                              ),
                            );
                          },
                        ),
                      ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class GritApp extends StatefulWidget {
  final AppController controller;
  const GritApp({super.key, required this.controller});
  @override
  State<GritApp> createState() => _GritAppState();
}

class _GritAppState extends State<GritApp> with WidgetsBindingObserver {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    super.dispose();
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (state != AppLifecycleState.resumed && !widget.controller.loadFailed) {
      unawaited(widget.controller.flush().catchError((Object e) {}));
    }
  }

  @override
  Widget build(BuildContext context) => MaterialApp(
    title: 'GRIT',
    debugShowCheckedModeBanner: false,
    theme: ThemeData(
      useMaterial3: true,
      scaffoldBackgroundColor: paper,
      colorScheme:
          ColorScheme.fromSeed(
            seedColor: ink,
            brightness: Brightness.light,
          ).copyWith(
            primary: ink,
            onPrimary: Colors.white,
            secondary: lime,
            surface: paper,
            onSurface: ink,
            error: danger,
          ),
      textTheme: ThemeData.light().textTheme.apply(
        bodyColor: ink,
        displayColor: ink,
      ),
      appBarTheme: const AppBarTheme(
        backgroundColor: paper,
        foregroundColor: ink,
        elevation: 0,
        scrolledUnderElevation: 0,
        centerTitle: false,
        systemOverlayStyle: SystemUiOverlayStyle(
          statusBarColor: Colors.transparent,
          statusBarIconBrightness: Brightness.dark,
          systemNavigationBarColor: paper,
          systemNavigationBarIconBrightness: Brightness.dark,
        ),
      ),
      filledButtonTheme: FilledButtonThemeData(
        style: FilledButton.styleFrom(
          minimumSize: const Size(48, 54),
          textStyle: const TextStyle(fontSize: 16, fontWeight: FontWeight.w700),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(16),
          ),
        ),
      ),
      outlinedButtonTheme: OutlinedButtonThemeData(
        style: OutlinedButton.styleFrom(
          minimumSize: const Size(48, 50),
          side: const BorderSide(color: line),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(16),
          ),
        ),
      ),
      dividerTheme: const DividerThemeData(color: line, space: 1),
      snackBarTheme: SnackBarThemeData(
        behavior: SnackBarBehavior.floating,
        backgroundColor: ink,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
      ),
      navigationBarTheme: NavigationBarThemeData(
        backgroundColor: Colors.white,
        indicatorColor: lime,
        labelTextStyle: WidgetStateProperty.all(
          const TextStyle(fontSize: 12, fontWeight: FontWeight.w700),
        ),
      ),
    ),
    home: HomeScreen(controller: widget.controller),
  );
}

class Surface extends StatelessWidget {
  final Widget child;
  final Color color;
  final EdgeInsets padding;
  const Surface({
    super.key,
    required this.child,
    this.color = Colors.white,
    this.padding = const EdgeInsets.all(20),
  });
  @override
  Widget build(BuildContext context) => Container(
    padding: padding,
    decoration: BoxDecoration(
      color: color,
      borderRadius: BorderRadius.circular(24),
      border: Border.all(color: color == Colors.white ? line : color),
    ),
    child: child,
  );
}

class Eyebrow extends StatelessWidget {
  final String text;
  const Eyebrow(this.text, {super.key});
  @override
  Widget build(BuildContext context) => WordText(
    text,
    style: const TextStyle(
      fontSize: 11,
      letterSpacing: 1.7,
      fontWeight: FontWeight.w800,
      color: muted,
    ),
  );
}

void toast(BuildContext context, String message) => ScaffoldMessenger.of(
  context,
).showSnackBar(SnackBar(content: WordText(message)));

class HomeScreen extends StatefulWidget {
  final AppController controller;
  const HomeScreen({super.key, required this.controller});
  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int tab = 0;
  SetKind? filter;
  bool busy = false;
  AppController get c => widget.controller;
  @override
  Widget build(BuildContext context) => ListenableBuilder(
    listenable: c,
    builder: (context, _) => Scaffold(
      appBar: AppBar(
        title: const WordText(
          'GRIT.',
          style: TextStyle(
            fontSize: 28,
            fontWeight: FontWeight.w900,
            letterSpacing: -1.2,
          ),
        ),
        actions: [
          IconButton(
            tooltip: '설정 및 기록 관리',
            onPressed: settings,
            icon: const Icon(Icons.tune_rounded),
          ),
          const SizedBox(width: 12),
        ],
      ),
      body: SafeArea(
        top: false,
        child: Center(
          child: ConstrainedBox(
            constraints: BoxConstraints(maxWidth: tab == 4 ? 720 : 1100),
            child: c.loadFailed
                ? loadError()
                : tab == 0
                ? training()
                : tab >= 1 && tab <= 3
                ? PsatLibrary(
                    key: ValueKey(tab),
                    controller: c,
                    subject: ['자료해석', '언어논리', '상황판단'][tab - 1],
                  )
                : history(),
          ),
        ),
      ),
      bottomNavigationBar: NavigationBar(
        selectedIndex: tab,
        onDestinationSelected: (value) => setState(() => tab = value),
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.grid_view_rounded),
            label: '비타민',
          ),
          NavigationDestination(
            icon: Icon(Icons.bar_chart_rounded),
            label: '자료해석',
          ),
          NavigationDestination(
            icon: Icon(Icons.menu_book_rounded),
            label: '언어논리',
          ),
          NavigationDestination(
            icon: Icon(Icons.account_tree_outlined),
            label: '상황판단',
          ),
          NavigationDestination(
            icon: Icon(Icons.history_rounded),
            label: '나의 기록',
          ),
        ],
      ),
    ),
  );
  Widget loadError() => Padding(
    padding: const EdgeInsets.all(24),
    child: Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        const Icon(Icons.folder_off_outlined, size: 48),
        const SizedBox(height: 20),
        WordText(c.error!, textAlign: TextAlign.center),
        const SizedBox(height: 20),
        FilledButton(onPressed: c.load, child: const WordText('다시 읽기')),
      ],
    ),
  );
  Widget training() => LayoutBuilder(
    builder: (context, box) {
      final count = c.records.length;
      final seconds = c.records.fold(0, (s, r) => s + r.elapsedSeconds!);
      final wide =
          box.maxWidth >= 700 || (box.maxWidth >= 600 && box.maxHeight < 520);
      final compact = box.maxHeight < 620;
      final spacing = compact ? 8.0 : 12.0;
      Widget header() => SizedBox(
        height: compact ? 54 : 86,
        child: Row(
          children: [
            Expanded(
              child: FittedBox(
                fit: BoxFit.scaleDown,
                alignment: Alignment.centerLeft,
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    if (!compact)
                      WordText(
                        dateLabel(DateTime.now()),
                        style: const TextStyle(fontSize: 11, color: muted),
                      ),
                    WordText(
                      '오늘도, 한 걸음.',
                      style: TextStyle(
                        fontSize: compact ? 24 : 31,
                        height: 1.2,
                        fontWeight: FontWeight.w800,
                        letterSpacing: 0,
                      ),
                    ),
                    const SizedBox(height: 4),
                    const FittedBox(
                      fit: BoxFit.scaleDown,
                      child: WordText(
                        '작은 연습이 쌓여, 결국 실력이 됩니다.',
                        style: TextStyle(color: muted, fontSize: 12),
                      ),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(width: 8),
            SizedBox(
              width: 76,
              child: TextButton(
                key: const ValueKey('vitamin-guide'),
                style: TextButton.styleFrom(
                  padding: const EdgeInsets.all(4),
                  minimumSize: const Size(72, 48),
                ),
                onPressed: () => Navigator.push(
                  context,
                  MaterialPageRoute(builder: (_) => const GuideScreen()),
                ),
                child: const Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(Icons.menu_book_rounded, size: 20),
                    SizedBox(height: 4),
                    WordText(
                      '풀이 안내서',
                      maxLines: 1,
                      style: TextStyle(fontSize: 11),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      );
      Widget stats() => SizedBox(
        height: compact ? 88 : 112,
        child: Surface(
          color: ink,
          padding: EdgeInsets.all(compact ? 12 : 14),
          child: Column(
            children: [
              if (!compact) ...[
                const Align(
                  alignment: Alignment.centerLeft,
                  child: WordText(
                    '꾸준함의 기록',
                    style: TextStyle(color: Color(0xFFBECDBF), fontSize: 12),
                  ),
                ),
                const SizedBox(height: 8),
              ],
              Expanded(
                child: Row(
                  children: [
                    stat('$count', '완료한 세트'),
                    stat('${seconds ~/ 60}', '누적 연습 · 분'),
                  ],
                ),
              ),
            ],
          ),
        ),
      );
      Widget errorNotice() => SizedBox(
        height: 38,
        child: Row(
          children: [
            const Icon(Icons.error_outline, color: danger, size: 18),
            const SizedBox(width: 6),
            const Expanded(
              child: WordText(
                '저장하지 못했어요.',
                style: TextStyle(color: danger, fontSize: 12),
              ),
            ),
            TextButton(
              onPressed: () async {
                try {
                  await c.flush();
                } catch (_) {}
              },
              child: const WordText('다시 시도'),
            ),
          ],
        ),
      );
      Widget choices() => Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxHeight: 324),
          child: Column(
            children: [
              for (final kind in SetKind.values) ...[
                if (kind != SetKind.addition) SizedBox(height: spacing),
                Expanded(child: kindCard(kind, compact: compact)),
              ],
            ],
          ),
        ),
      );
      return Padding(
        key: const ValueKey('training-no-scroll'),
        padding: EdgeInsets.fromLTRB(
          box.maxWidth < 360 ? 12 : 20,
          8,
          box.maxWidth < 360 ? 12 : 20,
          12,
        ),
        child: wide
            ? Row(
                key: const ValueKey('training-wide'),
                children: [
                  Expanded(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        header(),
                        SizedBox(height: spacing),
                        stats(),
                        if (c.error != null) errorNotice(),
                      ],
                    ),
                  ),
                  const SizedBox(width: 16),
                  Expanded(child: choices()),
                ],
              )
            : Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  header(),
                  SizedBox(height: spacing),
                  stats(),
                  if (c.error != null) errorNotice(),
                  SizedBox(height: spacing),
                  Expanded(child: choices()),
                ],
              ),
      );
    },
  );

  Widget stat(String value, String label) => Expanded(
    child: FittedBox(
      fit: BoxFit.scaleDown,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          WordText(
            value,
            style: numeric.copyWith(
              color: lime,
              fontSize: 27,
              fontWeight: FontWeight.w800,
            ),
          ),
          const SizedBox(height: 3),
          WordText(
            label,
            style: const TextStyle(color: Colors.white, fontSize: 11),
          ),
        ],
      ),
    ),
  );
  Widget kindCard(SetKind kind, {bool compact = false}) {
    final (symbol, color) = switch (kind) {
      SetKind.addition => ('+ -', const Color(0xFFE8EEDB)),
      SetKind.multiplication => ('×', const Color(0xFFF4E6D4)),
      SetKind.division => ('÷', const Color(0xFFE3E9F5)),
    };
    return Material(
      color: Colors.white,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(22),
        side: const BorderSide(color: line),
      ),
      clipBehavior: Clip.antiAlias,
      child: Padding(
        padding: compact
            ? const EdgeInsets.symmetric(horizontal: 10, vertical: 6)
            : const EdgeInsets.all(14),
        child: Row(
          children: [
            Container(
              width: compact ? 38 : 50,
              height: compact ? 38 : 50,
              alignment: Alignment.center,
              decoration: BoxDecoration(
                color: color,
                borderRadius: BorderRadius.circular(14),
              ),
              child: WordText(
                symbol,
                style: TextStyle(
                  fontSize: compact ? 23 : 28,
                  fontWeight: FontWeight.w700,
                ),
              ),
            ),
            SizedBox(width: compact ? 10 : 14),
            Expanded(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  FittedBox(
                    fit: BoxFit.scaleDown,
                    child: WordText(
                      kind.title,
                      style: TextStyle(
                        fontSize: compact ? 17 : 20,
                        fontWeight: FontWeight.w800,
                      ),
                    ),
                  ),
                  const SizedBox(height: 3),
                  FittedBox(
                    fit: BoxFit.scaleDown,
                    child: WordText(
                      kind.quantity,
                      style: const TextStyle(color: muted, fontSize: 11),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(width: 4),
            OutlinedButton(
              key: ValueKey('vitamin-history-${kind.name}'),
              style: OutlinedButton.styleFrom(
                minimumSize: const Size(48, 48),
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                backgroundColor: paper,
                side: const BorderSide(color: line),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
              onPressed: () => showGritDialog<void>(
                context: context,
                builder: (_) =>
                    VitaminHistoryDialog(kind: kind, records: c.records),
              ),
              child: const Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Icon(Icons.history_rounded, size: 17),
                  SizedBox(height: 2),
                  WordText('기록', style: TextStyle(fontSize: 11)),
                ],
              ),
            ),
            const SizedBox(width: 4),
            IconButton.filledTonal(
              key: ValueKey('vitamin-start-${kind.name}'),
              tooltip: '${kind.title} 시작',
              constraints: const BoxConstraints(minWidth: 48, minHeight: 48),
              iconSize: 30,
              style: IconButton.styleFrom(backgroundColor: lime),
              onPressed: c.active == null && !busy ? () => prepare(kind) : null,
              icon: const Icon(Icons.arrow_forward_rounded),
            ),
          ],
        ),
      ),
    );
  }

  Future<void> prepare(SetKind kind) async {
    final start = await showModalBottomSheet<bool>(
      context: context,
      isScrollControlled: true,
      showDragHandle: true,
      backgroundColor: paper,
      builder: (context) => SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.fromLTRB(24, 4, 24, 28),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Eyebrow('READY WHEN YOU ARE'),
              const SizedBox(height: 12),
              WordText(
                kind.title,
                style: const TextStyle(
                  fontSize: 30,
                  fontWeight: FontWeight.w800,
                ),
              ),
              const SizedBox(height: 8),
              WordText(kind.subtitle, style: const TextStyle(color: muted)),
              const SizedBox(height: 24),
              Surface(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    WordText(
                      kind.quantity,
                      style: const TextStyle(fontWeight: FontWeight.w700),
                    ),
                    const SizedBox(height: 12),
                    WordText(
                      kind == SetKind.addition
                          ? '빈칸을 눌러 숫자를 입력하세요. − 버튼으로 음수 부호를 바꿀 수 있어요. 지우기 버튼을 길게 누르면 선택한 칸을 모두 지웁니다.'
                          : '대소비교는 버튼으로, 분수 정렬은 큰 것부터 차례로 탭하세요.',
                    ),
                    const SizedBox(height: 12),
                    const WordText(
                      '시작과 함께 새 문제와 타이머가 열립니다.\n다른 앱을 보거나 화면을 끄면 타이머가 멈추고, 돌아오면 다시 흐릅니다.\n연습 화면을 나가거나 앱이 종료되면 진행 내용은 사라집니다.',
                      style: TextStyle(color: muted, fontSize: 13, height: 1.6),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 24),
              SizedBox(
                width: double.infinity,
                child: FilledButton.icon(
                  onPressed: () => Navigator.pop(context, true),
                  icon: const Icon(Icons.play_arrow_rounded),
                  label: const WordText('시작'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
    if (start != true || !mounted) return;
    setState(() => busy = true);
    try {
      final session = await c.start(kind);
      if (mounted) await openSession(session);
    } catch (_) {
      if (mounted) toast(context, '연습을 시작하지 못했어요. 저장 공간을 확인해 주세요.');
    } finally {
      if (mounted) setState(() => busy = false);
    }
  }

  Future<void> openSession(PracticeSession session) => Navigator.push(
    context,
    MaterialPageRoute(
      builder: (_) => PracticeScreen(controller: c, session: session),
    ),
  );
  Widget history() {
    final records = c.records
        .where((r) => filter == null || r.kind == filter)
        .toList();
    return ListView(
      padding: const EdgeInsets.fromLTRB(20, 16, 20, 28),
      children: [
        OutlinedButton.icon(
          onPressed: () => Navigator.push(
            context,
            MaterialPageRoute(builder: (_) => PsatHistory(controller: c)),
          ),
          icon: const Icon(Icons.menu_book_outlined),
          label: WordText('PSAT 기출 기록 (${c.psatRecords.length})'),
        ),
        const SizedBox(height: 20),
        const Eyebrow('YOUR PROGRESS'),
        const SizedBox(height: 12),
        const WordText(
          '쌓이는 노력.',
          style: TextStyle(
            fontSize: 31,
            fontWeight: FontWeight.w800,
            letterSpacing: 0,
          ),
        ),
        const SizedBox(height: 8),
        const WordText(
          '시간보다 중요한 건, 다시 시작한 당신.',
          style: TextStyle(color: muted, fontSize: 14),
        ),
        const SizedBox(height: 20),
        Wrap(
          spacing: 6,
          runSpacing: 4,
          children: [
            ChoiceChip(
              label: const WordText('전체'),
              selected: filter == null,
              onSelected: (_) => setState(() => filter = null),
            ),
            for (final kind in SetKind.values)
              ChoiceChip(
                label: WordText(kind.title),
                selected: filter == kind,
                onSelected: (_) => setState(() => filter = kind),
              ),
          ],
        ),
        const SizedBox(height: 20),
        if (records.isEmpty)
          const Padding(
            padding: EdgeInsets.symmetric(vertical: 70),
            child: Column(
              children: [
                Icon(Icons.auto_stories_outlined, size: 44, color: muted),
                SizedBox(height: 20),
                WordText(
                  '첫 번째 기록을 기다리고 있어요.',
                  style: TextStyle(fontWeight: FontWeight.w700),
                ),
                SizedBox(height: 8),
                WordText(
                  '연습을 완료하면 이곳에 차곡차곡 쌓여요.',
                  style: TextStyle(color: muted, fontSize: 13),
                ),
              ],
            ),
          ),
        for (var i = 0; i < records.length; i++) ...[
          if (i == 0 ||
              dateLabel(records[i].startedAt) !=
                  dateLabel(records[i - 1].startedAt))
            Padding(
              padding: const EdgeInsets.only(bottom: 10, top: 12),
              child: Eyebrow(dateLabel(records[i].startedAt)),
            ),
          recordCard(records[i]),
          const SizedBox(height: 10),
        ],
      ],
    );
  }

  Widget recordCard(PracticeSession r) => Material(
    color: Colors.white,
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(20),
      side: const BorderSide(color: line),
    ),
    clipBehavior: Clip.antiAlias,
    child: InkWell(
      onTap: () => Navigator.push(
        context,
        MaterialPageRoute(builder: (_) => ResultScreen(session: r)),
      ),
      child: Padding(
        padding: const EdgeInsets.all(18),
        child: Row(
          children: [
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  WordText(
                    r.kind.title,
                    style: const TextStyle(
                      fontWeight: FontWeight.w800,
                      fontSize: 17,
                    ),
                  ),
                  const SizedBox(height: 6),
                  WordText(
                    '${'${r.startedAt.hour}'.padLeft(2, '0')}:${'${r.startedAt.minute}'.padLeft(2, '0')}  ·  ${durationLabel(r.elapsedSeconds!)}',
                    style: const TextStyle(color: muted, fontSize: 13),
                  ),
                ],
              ),
            ),
            WordText(
              '${r.correct}',
              style: numeric.copyWith(
                fontSize: 26,
                fontWeight: FontWeight.w800,
              ),
            ),
            WordText('/${r.total}', style: const TextStyle(color: muted)),
            const SizedBox(width: 10),
            const Icon(Icons.chevron_right_rounded, color: muted),
          ],
        ),
      ),
    ),
  );
  Future<void> resetHistory() async {
    if (busy) return;
    final confirmed = await showGritDialog<bool>(
      context: context,
      builder: (dialogContext) => AlertDialog(
        title: const WordText('기록을 모두 초기화할까요?'),
        content: const WordText(
          '비타민의 누적 통계·완료 기록과 PSAT 세 과목의 모든 풀이 기록이 삭제됩니다. 되돌릴 수 없습니다.',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(dialogContext, false),
            child: const WordText('취소'),
          ),
          TextButton(
            key: const ValueKey('confirm-reset-history'),
            onPressed: () => Navigator.pop(dialogContext, true),
            child: const WordText('모두 초기화', style: TextStyle(color: danger)),
          ),
        ],
      ),
    );
    if (confirmed != true || !mounted) return;
    setState(() => busy = true);
    try {
      await c.resetHistory();
      if (mounted) toast(context, '연습 기록을 초기화했어요.');
    } catch (_) {
      if (mounted) toast(context, '초기화하지 못했어요. 기존 기록은 유지됩니다.');
    } finally {
      if (mounted) setState(() => busy = false);
    }
  }

  Future<void> settings() async {
    await showModalBottomSheet<void>(
      context: context,
      showDragHandle: true,
      isScrollControlled: true,
      backgroundColor: paper,
      builder: (sheetContext) => SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.fromLTRB(24, 8, 24, 28),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const WordText(
                '당신의 연습, 당신의 기록.',
                style: TextStyle(fontWeight: FontWeight.w800, fontSize: 22),
              ),
              const SizedBox(height: 12),
              const WordText(
                '연습 기록은 이 기기에 자동 저장됩니다. 앱을 삭제하면 기록도 삭제됩니다.',
                style: TextStyle(color: muted, height: 1.6),
              ),
              const SizedBox(height: 22),
              ListTile(
                contentPadding: EdgeInsets.zero,
                leading: const Icon(
                  Icons.delete_outline_rounded,
                  color: danger,
                ),
                title: const WordText(
                  '기록 초기화',
                  style: TextStyle(color: danger),
                ),
                subtitle: const WordText('비타민과 PSAT 기출 풀이 기록을 모두 삭제'),
                enabled:
                    !busy &&
                    !c.loadFailed &&
                    (c.records.isNotEmpty || c.psatRecords.isNotEmpty),
                onTap: () {
                  Navigator.pop(sheetContext);
                  resetHistory();
                },
              ),
              const SizedBox(height: 22),
              const Divider(),
              const SizedBox(height: 20),
              const WordText(
                'GRIT',
                style: TextStyle(fontWeight: FontWeight.w800),
              ),
              const SizedBox(height: 6),
              const WordText(
                '매일 조금씩, 기어이 해낸다.',
                style: TextStyle(color: muted, fontSize: 12),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
