import 'word_text.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'main.dart' show Surface, Eyebrow, ink, muted, lime, toast;
import 'guide_content.dart';

const _readingStyle = TextStyle(fontSize: 16, height: 1.8);

class GuideScreen extends StatefulWidget {
  const GuideScreen({super.key});
  @override
  State<GuideScreen> createState() => _GuideScreenState();
}

class _GuideScreenState extends State<GuideScreen> {
  String query = '';
  @override
  Widget build(BuildContext context) {
    final q = query.trim().toLowerCase();
    return Scaffold(
      appBar: AppBar(title: const WordText('풀이 안내서')),
      body: _ReadingBody(
        children: [
          const Eyebrow('GRIT · LEARN'),
          const SizedBox(height: 10),
          const WordText(
            '원리를 알고,\n조금씩 빨라지기.',
            style: TextStyle(fontSize: 28, fontWeight: FontWeight.w800),
          ),
          const SizedBox(height: 14),
          const WordText(
            '수학이 낯설어도 괜찮습니다. 처음에는 1장부터 읽고, 한 가지 방법을 직접 풀어 본 뒤 다음으로 넘어가세요. 모든 풀이에는 예제, 장점, 주의점과 막혔을 때의 다음 방법이 있습니다.',
            style: _readingStyle,
          ),
          const SizedBox(height: 16),
          const Surface(
            color: lime,
            child: WordText(
              '6개 장 · 31개 풀이법 · 13개 확인 문제\n인터넷 없이 읽을 수 있습니다. 안내서의 확인 문제는 기록에 합산하지 않습니다.',
              style: TextStyle(height: 1.6),
            ),
          ),
          const SizedBox(height: 20),
          TextField(
            key: const ValueKey('guide-search'),
            decoration: const InputDecoration(
              labelText: '찾고 싶은 내용',
              hintText: '예: 용병법, 음수, 어림, 분모',
              prefixIcon: Icon(Icons.search_rounded),
              border: OutlineInputBorder(),
            ),
            onChanged: (value) => setState(() => query = value),
          ),
          const SizedBox(height: 16),
          if (q.isEmpty)
            for (var i = 0; i < guideChapters.length; i++) ...[
              _ChapterLink(index: i),
              const SizedBox(height: 10),
            ]
          else ...[
            for (var c = 0; c < guideChapters.length; c++)
              for (var t = 0; t < guideChapters[c].tips.length; t++)
                if (_matches(guideChapters[c].tips[t], q))
                  ListTile(
                    contentPadding: const EdgeInsets.symmetric(vertical: 6),
                    title: WordText(guideChapters[c].tips[t].title),
                    subtitle: WordText('${c + 1}장 · ${guideChapters[c].title}'),
                    trailing: const Icon(Icons.chevron_right_rounded),
                    onTap: () => _openTip(context, c, t),
                  ),
            if (!guideChapters.any((c) => c.tips.any((t) => _matches(t, q))))
              const Padding(
                padding: EdgeInsets.symmetric(vertical: 24),
                child: WordText('일치하는 풀이가 없습니다. 다른 낱말로 찾아보세요.'),
              ),
          ],
          const SizedBox(height: 16),
          const _Sources(indices: [0, 1, 2, 3, 4, 5, 6, 7]),
        ],
      ),
    );
  }

  bool _matches(GuideTip t, String q) =>
      '${t.title} ${t.level} ${t.when} ${t.steps} ${t.why} ${t.benefit} ${t.caution} ${t.next}'
          .toLowerCase()
          .contains(q);
}

class _ChapterLink extends StatelessWidget {
  final int index;
  const _ChapterLink({required this.index});
  @override
  Widget build(BuildContext context) {
    final chapter = guideChapters[index];
    return Surface(
      padding: EdgeInsets.zero,
      child: ListTile(
        key: ValueKey('guide-chapter-$index'),
        contentPadding: const EdgeInsets.symmetric(
          horizontal: 18,
          vertical: 12,
        ),
        leading: CircleAvatar(
          backgroundColor: lime,
          foregroundColor: ink,
          child: WordText('${index + 1}'),
        ),
        title: WordText(
          chapter.title,
          style: const TextStyle(fontWeight: FontWeight.w800),
        ),
        subtitle: WordText(
          '${chapter.subtitle}\n${chapter.tips.length}개 풀이법',
          style: const TextStyle(height: 1.6),
        ),
        trailing: const Icon(Icons.chevron_right_rounded),
        onTap: () => Navigator.push(
          context,
          MaterialPageRoute(
            builder: (_) => GuideChapterScreen(chapterIndex: index),
          ),
        ),
      ),
    );
  }
}

class GuideChapterScreen extends StatelessWidget {
  final int chapterIndex;
  const GuideChapterScreen({super.key, required this.chapterIndex});
  @override
  Widget build(BuildContext context) {
    final chapter = guideChapters[chapterIndex];
    return Scaffold(
      appBar: AppBar(title: WordText('${chapterIndex + 1}장 · 풀이 안내서')),
      body: _ReadingBody(
        children: [
          WordText(
            chapter.title,
            style: const TextStyle(fontSize: 27, fontWeight: FontWeight.w800),
          ),
          const SizedBox(height: 16),
          WordSelectableText(chapter.intro, style: _readingStyle),
          const SizedBox(height: 20),
          _Section(title: '이 순서로 골라 쓰세요', text: chapter.route, color: lime),
          const SizedBox(height: 12),
          for (var i = 0; i < chapter.tips.length; i++)
            ListTile(
              key: ValueKey('guide-tip-$chapterIndex-$i'),
              contentPadding: const EdgeInsets.symmetric(vertical: 8),
              title: WordText(
                chapter.tips[i].title,
                style: const TextStyle(fontWeight: FontWeight.w700),
              ),
              subtitle: WordText(
                '${chapter.tips[i].level} · ${chapter.tips[i].when}',
              ),
              trailing: const Icon(Icons.chevron_right_rounded),
              onTap: () => _openTip(context, chapterIndex, i),
            ),
          const SizedBox(height: 24),
          const WordText(
            '직접 풀고 확인하기',
            style: TextStyle(fontSize: 21, fontWeight: FontWeight.w800),
          ),
          const SizedBox(height: 8),
          const WordText(
            '먼저 스스로 답과 이유를 생각한 뒤 펼쳐 보세요.',
            style: TextStyle(color: muted),
          ),
          for (var i = 0; i < chapter.quizzes.length; i++)
            ExpansionTile(
              key: ValueKey('guide-quiz-$chapterIndex-$i'),
              tilePadding: EdgeInsets.zero,
              title: WordText(
                'Q${i + 1}. ${chapter.quizzes[i].question}',
                style: const TextStyle(height: 1.6),
              ),
              subtitle: const WordText('눌러서 정답과 풀이 확인'),
              children: [
                Padding(
                  padding: const EdgeInsets.only(bottom: 24),
                  child: Align(
                    alignment: Alignment.centerLeft,
                    child: WordSelectableText(
                      chapter.quizzes[i].answer,
                      style: _readingStyle,
                    ),
                  ),
                ),
              ],
            ),
          const SizedBox(height: 20),
          _Sources(indices: chapter.sources),
          if (chapterIndex + 1 < guideChapters.length) ...[
            const SizedBox(height: 20),
            FilledButton(
              onPressed: () => Navigator.pushReplacement(
                context,
                MaterialPageRoute(
                  builder: (_) =>
                      GuideChapterScreen(chapterIndex: chapterIndex + 1),
                ),
              ),
              child: WordText(
                '다음 장 · ${guideChapters[chapterIndex + 1].title}',
                textAlign: TextAlign.center,
              ),
            ),
          ],
        ],
      ),
    );
  }
}

void _openTip(BuildContext context, int chapter, int tip) => Navigator.push(
  context,
  MaterialPageRoute(
    builder: (_) => GuideTipScreen(chapterIndex: chapter, initialTip: tip),
  ),
);

class GuideTipScreen extends StatefulWidget {
  final int chapterIndex, initialTip;
  const GuideTipScreen({
    super.key,
    required this.chapterIndex,
    required this.initialTip,
  });
  @override
  State<GuideTipScreen> createState() => _GuideTipScreenState();
}

class _GuideTipScreenState extends State<GuideTipScreen> {
  late int index = widget.initialTip;
  final scroll = ScrollController();
  @override
  void dispose() {
    scroll.dispose();
    super.dispose();
  }

  void go(int value) {
    setState(() => index = value);
    scroll.jumpTo(0);
  }

  @override
  Widget build(BuildContext context) {
    final chapter = guideChapters[widget.chapterIndex];
    final tip = chapter.tips[index];
    return Scaffold(
      appBar: AppBar(
        title: WordText(
          '${widget.chapterIndex + 1}장 · ${index + 1}/${chapter.tips.length}',
        ),
      ),
      body: _ReadingBody(
        controller: scroll,
        children: [
          Eyebrow(tip.level),
          const SizedBox(height: 12),
          WordSelectableText(
            tip.title,
            style: const TextStyle(fontSize: 26, fontWeight: FontWeight.w800),
          ),
          const SizedBox(height: 20),
          _Section(title: '1. 언제 쓰나요?', text: tip.when, color: lime),
          _Section(title: '2. 한 단계씩 따라 해 보기', text: tip.steps),
          _Section(title: '3. 왜 이렇게 해도 되나요?', text: tip.why),
          _Section(title: '4. 이 방법의 장점', text: tip.benefit),
          _Section(
            title: '5. 주의할 점과 한계',
            text: tip.caution,
            color: const Color(0xFFF4E6D4),
          ),
          _Section(title: '6. 막히면 다음 방법', text: tip.next),
          const SizedBox(height: 8),
          Row(
            children: [
              Expanded(
                child: OutlinedButton(
                  onPressed: index > 0 ? () => go(index - 1) : null,
                  child: const WordText('이전 풀이'),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: FilledButton(
                  onPressed: index + 1 < chapter.tips.length
                      ? () => go(index + 1)
                      : () => Navigator.pop(context),
                  child: WordText(
                    index + 1 < chapter.tips.length ? '다음 풀이' : '목차 · 확인 문제',
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 20),
          _Sources(indices: chapter.sources),
        ],
      ),
    );
  }
}

class _Section extends StatelessWidget {
  final String title, text;
  final Color color;
  const _Section({
    required this.title,
    required this.text,
    this.color = Colors.white,
  });
  @override
  Widget build(BuildContext context) => Padding(
    padding: const EdgeInsets.only(bottom: 16),
    child: Surface(
      color: color,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          WordText(
            title,
            style: const TextStyle(fontSize: 17, fontWeight: FontWeight.w800),
          ),
          const SizedBox(height: 10),
          WordSelectableText(text, style: _readingStyle),
        ],
      ),
    ),
  );
}

class _ReadingBody extends StatelessWidget {
  final List<Widget> children;
  final ScrollController? controller;
  const _ReadingBody({required this.children, this.controller});
  @override
  Widget build(BuildContext context) => SafeArea(
    top: false,
    child: Center(
      child: ConstrainedBox(
        constraints: const BoxConstraints(maxWidth: 760),
        child: ListView(
          controller: controller,
          padding: EdgeInsets.fromLTRB(
            MediaQuery.sizeOf(context).width < 360 ? 16 : 24,
            16,
            MediaQuery.sizeOf(context).width < 360 ? 16 : 24,
            32,
          ),
          children: children,
        ),
      ),
    ),
  );
}

class _Sources extends StatelessWidget {
  final List<int> indices;
  const _Sources({required this.indices});
  @override
  Widget build(BuildContext context) => ExpansionTile(
    tilePadding: EdgeInsets.zero,
    title: const WordText('참고 자료와 작성 기준'),
    subtitle: const WordText('확인일 2026.10.26 · 원리와 예제는 직접 작성'),
    children: [
      const Padding(
        padding: EdgeInsets.only(bottom: 16),
        child: WordText(
          '국내 학습 자료에서 자주 등장하는 접근을 조사하고, 초보자를 위해 설명과 예제를 새로 구성했습니다. 강의의 표현이나 원문 문제를 옮긴 교재가 아닙니다. 아래에서 본문 확인과 영상 제목·설명만 확인한 자료를 구분했습니다. 링크는 복사해 브라우저에서 열 수 있습니다.',
          style: TextStyle(height: 1.6, color: muted),
        ),
      ),
      for (final i in indices)
        Padding(
          padding: const EdgeInsets.only(bottom: 18),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              WordText(
                guideSources[i].title,
                style: const TextStyle(fontWeight: FontWeight.w700),
              ),
              const SizedBox(height: 6),
              WordText(
                guideSources[i].note,
                style: const TextStyle(height: 1.6),
              ),
              const SizedBox(height: 6),
              WordSelectableText(
                guideSources[i].url,
                style: const TextStyle(fontSize: 12, color: muted),
              ),
              TextButton.icon(
                icon: const Icon(Icons.copy_rounded, size: 18),
                label: const WordText('출처 링크 복사'),
                onPressed: () async {
                  await Clipboard.setData(
                    ClipboardData(text: guideSources[i].url),
                  );
                  if (context.mounted) toast(context, '출처 링크를 복사했어요.');
                },
              ),
            ],
          ),
        ),
    ],
  );
}
