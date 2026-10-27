import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'model.dart';
import 'store.dart';
import 'practice.dart';
import 'guide.dart';

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
  Widget build(BuildContext context) => Text(
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
).showSnackBar(SnackBar(content: Text(message)));

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
        title: const Text(
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
            constraints: BoxConstraints(maxWidth: tab == 0 ? 1100 : 720),
            child: c.loadFailed
                ? loadError()
                : tab == 0
                ? training()
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
            label: '연습',
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
        Text(c.error!, textAlign: TextAlign.center),
        const SizedBox(height: 20),
        FilledButton(onPressed: c.load, child: const Text('다시 읽기')),
      ],
    ),
  );
  Widget training() => LayoutBuilder(
    builder: (context, box) {
      final count = c.records.length;
      final correct = c.records.fold(0, (s, r) => s + r.correct);
      final seconds = c.records.fold(0, (s, r) => s + r.elapsedSeconds!);
      final wide =
          box.maxWidth >= 700 || (box.maxWidth >= 600 && box.maxHeight < 520);
      final compact = box.maxHeight < 620;
      final spacing = compact ? 8.0 : 12.0;
      Widget header() => SizedBox(
        height: compact ? 54 : 86,
        child: FittedBox(
          fit: BoxFit.scaleDown,
          alignment: Alignment.centerLeft,
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              if (!compact)
                Text(
                  dateLabel(DateTime.now()),
                  style: const TextStyle(fontSize: 11, color: muted),
                ),
              Text(
                '오늘도, 한 걸음.',
                style: TextStyle(
                  fontSize: compact ? 24 : 31,
                  height: 1.2,
                  fontWeight: FontWeight.w800,
                  letterSpacing: -1,
                ),
              ),
              const SizedBox(height: 4),
              const FittedBox(
                fit: BoxFit.scaleDown,
                child: Text(
                  '작은 연습이 쌓여, 결국 실력이 됩니다.',
                  style: TextStyle(color: muted, fontSize: 12),
                ),
              ),
            ],
          ),
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
                  child: Text(
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
                    stat('$correct', '맞힌 문제'),
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
              child: Text(
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
              child: const Text('다시 시도'),
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
          Text(
            value,
            style: numeric.copyWith(
              color: lime,
              fontSize: 27,
              fontWeight: FontWeight.w800,
            ),
          ),
          const SizedBox(height: 3),
          Text(
            label,
            style: const TextStyle(color: Colors.white, fontSize: 11),
          ),
        ],
      ),
    ),
  );
  Widget kindCard(SetKind kind, {bool compact = false}) {
    final (symbol, color) = switch (kind) {
      SetKind.addition => ('+ −', const Color(0xFFE8EEDB)),
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
      child: InkWell(
        onTap: c.active == null && !busy ? () => prepare(kind) : null,
        child: Padding(
          padding: EdgeInsets.all(compact ? 10 : 14),
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
                child: Text(
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
                      child: Text(
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
                      child: Text(
                        kind.quantity,
                        style: const TextStyle(color: muted, fontSize: 11),
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(width: 6),
              const Icon(Icons.arrow_forward_rounded, size: 18),
            ],
          ),
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
              Text(
                kind.title,
                style: const TextStyle(
                  fontSize: 30,
                  fontWeight: FontWeight.w800,
                ),
              ),
              const SizedBox(height: 8),
              Text(kind.subtitle, style: const TextStyle(color: muted)),
              const SizedBox(height: 24),
              Surface(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      kind.quantity,
                      style: const TextStyle(fontWeight: FontWeight.w700),
                    ),
                    const SizedBox(height: 12),
                    Text(
                      kind == SetKind.addition
                          ? '빈칸을 눌러 숫자를 입력하세요. 음수는 −/+ 버튼으로도 입력할 수 있어요.'
                          : '대소비교는 버튼으로, 분수 정렬은 큰 것부터 차례로 탭하세요.',
                    ),
                    const SizedBox(height: 12),
                    const Text(
                      '시작과 함께 새 문제와 타이머가 열립니다.\n일시정지는 없습니다. 다른 앱을 보는 동안에도 시간은 흐릅니다.\n연습 화면을 나가거나 앱이 종료되면 진행 내용은 사라집니다.',
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
                  label: const Text('시작'),
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
        const Eyebrow('YOUR PROGRESS'),
        const SizedBox(height: 12),
        const Text(
          '쌓이는 노력.',
          style: TextStyle(
            fontSize: 31,
            fontWeight: FontWeight.w800,
            letterSpacing: -1,
          ),
        ),
        const SizedBox(height: 8),
        const Text(
          '시간보다 중요한 건, 다시 시작한 당신.',
          style: TextStyle(color: muted, fontSize: 14),
        ),
        const SizedBox(height: 20),
        Wrap(
          spacing: 6,
          runSpacing: 4,
          children: [
            ChoiceChip(
              label: const Text('전체'),
              selected: filter == null,
              onSelected: (_) => setState(() => filter = null),
            ),
            for (final kind in SetKind.values)
              ChoiceChip(
                label: Text(kind.title),
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
                Text(
                  '첫 번째 기록을 기다리고 있어요.',
                  style: TextStyle(fontWeight: FontWeight.w700),
                ),
                SizedBox(height: 8),
                Text(
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
                  Text(
                    r.kind.title,
                    style: const TextStyle(
                      fontWeight: FontWeight.w800,
                      fontSize: 17,
                    ),
                  ),
                  const SizedBox(height: 6),
                  Text(
                    '${'${r.startedAt.hour}'.padLeft(2, '0')}:${'${r.startedAt.minute}'.padLeft(2, '0')}  ·  ${durationLabel(r.elapsedSeconds!)}',
                    style: const TextStyle(color: muted, fontSize: 13),
                  ),
                ],
              ),
            ),
            Text(
              '${r.correct}',
              style: numeric.copyWith(
                fontSize: 26,
                fontWeight: FontWeight.w800,
              ),
            ),
            Text('/${r.total}', style: const TextStyle(color: muted)),
            const SizedBox(width: 10),
            const Icon(Icons.chevron_right_rounded, color: muted),
          ],
        ),
      ),
    ),
  );
  Future<void> resetHistory() async {
    if (busy) return;
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (dialogContext) => AlertDialog(
        title: const Text('기록을 모두 초기화할까요?'),
        content: const Text(
          '메인 화면의 누적 통계와 나의 기록에 있는 모든 완료 기록이 삭제됩니다. 되돌릴 수 없습니다.',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(dialogContext, false),
            child: const Text('취소'),
          ),
          TextButton(
            key: const ValueKey('confirm-reset-history'),
            onPressed: () => Navigator.pop(dialogContext, true),
            child: const Text('모두 초기화', style: TextStyle(color: danger)),
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
              const Text(
                '당신의 연습, 당신의 기록.',
                style: TextStyle(fontWeight: FontWeight.w800, fontSize: 22),
              ),
              const SizedBox(height: 12),
              const Text(
                '연습 기록은 이 기기에 자동 저장됩니다. 앱을 삭제하면 기록도 삭제됩니다.',
                style: TextStyle(color: muted, height: 1.6),
              ),
              const SizedBox(height: 22),
              ListTile(
                contentPadding: EdgeInsets.zero,
                leading: const Icon(Icons.menu_book_rounded),
                title: const Text('풀이 안내서'),
                subtitle: const Text('기초부터 실전까지 · 원리, 예제, 함정, 연습'),
                trailing: const Icon(Icons.chevron_right_rounded),
                onTap: () {
                  Navigator.pop(sheetContext);
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (_) => const GuideScreen()),
                  );
                },
              ),
              const Divider(),
              ListTile(
                contentPadding: EdgeInsets.zero,
                leading: const Icon(
                  Icons.delete_outline_rounded,
                  color: danger,
                ),
                title: const Text('기록 초기화', style: TextStyle(color: danger)),
                subtitle: const Text('메인 통계와 나의 기록을 함께 삭제'),
                enabled: !busy && !c.loadFailed && c.records.isNotEmpty,
                onTap: () {
                  Navigator.pop(sheetContext);
                  resetHistory();
                },
              ),
              const SizedBox(height: 22),
              const Divider(),
              const SizedBox(height: 20),
              const Text(
                'GRIT  1.1.0',
                style: TextStyle(fontWeight: FontWeight.w800),
              ),
              const SizedBox(height: 6),
              const Text(
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
