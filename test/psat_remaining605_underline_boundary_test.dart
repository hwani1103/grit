import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:grit/psat_sets.dart';
import 'package:grit/psat_text.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  test(
    'original underline strokes exclude labels and adjacent suffixes',
    () async {
      final catalog = await loadPsatCatalog();
      final shared = ['A의 주장', 'B의 주장', 'X의 지속적인 사용은 미국 사회의 인종차별을 고착화한다'];
      for (final entry in {
        "kr-mpm-2023-03-04-psat-l-31": ["자율적 군사로봇의 사용은 비윤리적이다."],
        "kr-mpm-2023-03-04-psat-l-32": ["동물들이 유사한 기능을 발휘하기 위해 항상 유사한 메커니즘이 요구되는 것은 아니다."],
        "kr-mpm-2023-07-22-psat-l-21": ["이는 수용하기 어렵다"],
        "kr-mpm-2024-07-27-psat-l-19": ["만약 우리가 p를 믿는다는 것이 인식적으로 정당화된다면 그것을 믿어야 하고, 만약 우리가 p를 믿는다는 것이 인식적으로 정당화되지 않는다면 그것을 믿어야 하는 것은 아니다", "우리가 p를 믿는다는 것은 자유롭게 선택할 수 있는 것이 아니다", "만약 우리가 p를 믿는다는 것이 자유롭게 선택할 수 있는 것이 아니라면, 우리에게 p를 믿어야 할 인식적 의무는 없다", "우리가 p를 믿는다는 것은 인식적으로 정당화되지 않는다"],
        "kr-mpm-2024-07-27-psat-l-20": ["만약 우리가 p를 믿는다는 것이 인식적으로 정당화된다면 그것을 믿어야 하고, 만약 우리가 p를 믿는다는 것이 인식적으로 정당화되지 않는다면 그것을 믿어야 하는 것은 아니다", "우리가 p를 믿는다는 것은 자유롭게 선택할 수 있는 것이 아니다", "만약 우리가 p를 믿는다는 것이 자유롭게 선택할 수 있는 것이 아니라면, 우리에게 p를 믿어야 할 인식적 의무는 없다", "우리가 p를 믿는다는 것은 인식적으로 정당화되지 않는다"],
        "kr-mpm-2024-03-02-psat-d-33": ["2020∼2023년 교통사고 발생건수당 사망자수 역시 매년 감소하여 2023년 교통사고 발생건수 100건당 사망자수는 1.8명 이하였다.", "2020～2023년 부상자수 중 중상자수의 비율도 매년 감소하여 2023년에는 부상자수 중 중상자수의 비율이 25% 이하였다.", "2020∼2023년 특별광역시도의 교통사고 발생건수는 매년 감소하였다.", "일반국도의 교통사고 발생건수는 2022년과 2023년 각각 16,000건을 넘지 않았다."],
        "kr-mpm-2023-03-04-psat-d-02": ["‘일부 반영’으로 응답한 비율이 중학교와 고등학교 각각 70.8%, 58.3%로 가장 높았다.", "‘전부 반영’으로 응답한 비율은 전년 대비 중학교가 2.8%p, 고등학교가 2.4%p 증가하였다.", "중학교는 ‘체험처 수용 인원 규모 초과’, 고등학교는 ‘수요 기반 체험처 미확보’로 응답한 비율이 가장 높았다.", "학생 의사 미반영 이유를 ‘이동 시간 부족’으로 응답한 교원의 수는 중학교와 고등학교가 동일하였다."],
        "kr-mpm-2026-03-07-psat-d-32": ["회원 3명은 금요일에 146,000원으로 ‘단풍 유람선’ 패키지 상품을 이용할 수 있습니다.", "가장 저렴한 방법은 ‘나루 유람선’ 패키지 상품을 이용하는 것이고 비용은 368,000원입니다.", "회원 2명이 일요일에 ‘소담’ 객실에서 1박하고 ‘동굴’ 관광 상품을 이용한다면, 86,000원에 이용할 수 있습니다."],
        "kr-mpm-2023-03-04-psat-l-10": ["부과되는 책임의 성격이 전쟁 범죄에 가담한 정도에 따라 달라야 한다", "나치 독일이 제정한 실정법을 지켰느냐 지키지 않았느냐의 문제는 아니다", "나치 정권의 집권에 반대표를 던졌다고 해서 모면할 수 있는 성질의 것이 아니다", "마음 속으로 동조하지 않았지만 나쁜 일에 직접 가담했다거나", "마음 속으로 동조한 적도 없으며 오히려 피해자가 될 뻔하기도 했지만"],
        "kr-mpm-2023-07-22-psat-l-22": ["이는 수용하기 어렵다"],
        'kr-mpm-2026-07-18-psat-l-06': ['전이'],
        'kr-mpm-2026-07-18-psat-l-16': ['두 개의 전제'],
        'kr-mpm-2024-03-02-psat-l-38': ['동일한 물질에 입사하는 빛의 파장이 짧을수록 전자의 전이시간이 더 길어진다'],
        'kr-mpm-2021-07-10-psat-l-13': [
          '당신은 나에게 10억 원을 지불한다',
          '그는 당신에게 10만 원을 돌려주지 않는다',
          '(1)은 참일 수밖에 없다',
          '당신은 그에게 10억 원을 지불한다',
        ],
        'kr-mpm-2025-03-08-psat-l-07': [
          '유선 인터넷망이 설치되어 이를 통한 소통이 가능하게 되었을 때만 해도 이만큼의 파급력은 없었다',
          '인터넷으로 메시지를 전하려면 적지 않은 시간과 비용이 필요했기 때문이다',
          '우리는 틈만 나면 스마트폰을 확인하며 늘 어딘가와 연결되어 있다는 사실에 안도한다',
          '스마트폰은 책상과 마찬가지로 사물이다',
          '스마트폰을 타자로 인식하는 순간 나는 스마트폰에 예속된다',
        ],
        'kr-mpm-2025-03-08-psat-l-30': ['이익조정'],
        'kr-mpm-2026-07-18-psat-l-09': ['자료 조사'],
        'kr-mpm-2021-07-10-psat-l-21': shared,
        'kr-mpm-2021-07-10-psat-l-22': shared,
        'kr-mpm-2025-11-15-psat-l-07': [
          '이성적으로 통제할 수 있다',
          '집단 내 결혼으로 발생하는 유전적 악화',
          '단순한 증여 행위가 아니라',
          '권리라는 점에서 자율적',
          '집단 외 결혼',
        ],
        'kr-mpm-2025-11-15-psat-l-13': ['로봇이 그 윤리 원칙을 위반했더라도 로봇의 당시 행위가 허용된다'],
        'kr-mpm-2025-11-15-psat-l-14': ['A－연쇄', 'B－연쇄'],
        'kr-mpm-2025-11-15-psat-l-21': [
          '원인은 그것이 없었다면 발생하지 않았을 사건인 결과를 발생하게 한다',
          '초기 확률 인과 이론',
          '수정된 확률 인과 이론',
        ],
        'kr-mpm-2025-11-15-psat-l-22': [
          '원인은 그것이 없었다면 발생하지 않았을 사건인 결과를 발생하게 한다',
          '초기 확률 인과 이론',
          '수정된 확률 인과 이론',
        ],
      }.entries) {
        final q = catalog.questions[entry.key]!;
        final spans = psatInlineSpans(
          q.body,
          q.underlines,
          underlineLabelAnchors: q.data['underlineLabelAnchors'] == true,
        );
        final marked = spans
            .where((s) => s.style?.decoration == TextDecoration.underline)
            // Label separators have no ink; compare the visible source glyphs.
            .map((s) => s.text?.trim())
            .toList();
        expect(marked, entry.value, reason: entry.key);
        expect(
          TextSpan(children: spans).toPlainText(),
          q.body
              .replaceAll('<보기>', '보기')
              .replaceAll('<보 기>', '보 기')
              .replaceAll('<상황>', '상황')
              .replaceAll('<실 험>', '실 험')
              .replaceAll('<논증>', '논증')
              .replaceAll('<보고서>', '보고서')
              .replaceAll('<대화>', '대화'),
          reason: entry.key,
        );
      }
    },
  );
  test('quoted source anchors mark only the labelled occurrence', () {
    const body = '전이, ㉠ ‘전이’란 전이의 한 예다. ㉡“자료 조사”와 자료 조사.';
    final spans = psatInlineSpans(body, [
      '㉠ ‘전이’',
      '㉡“자료 조사”',
    ], underlineLabelAnchors: true);
    expect(TextSpan(children: spans).toPlainText(), body);
    expect(
      spans
          .where((s) => s.style?.decoration == TextDecoration.underline)
          .map((s) => s.text)
          .toList(),
      ['전이', '자료 조사'],
    );
    final ordinary = psatInlineSpans('‘전이’', ['‘전이’']);
    expect(ordinary.single.text, '‘전이’');
    expect(ordinary.single.style?.decoration, TextDecoration.underline);
  });
}
