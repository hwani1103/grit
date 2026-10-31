"""Close the completed unit and save the user's requested safe pause."""
import hashlib
import importlib.util
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/psat_remaining605_20261030'
B = OUT / 'batch08'
def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p, value):
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

assert not (OUT / 'batch09/own-solves.json').exists()
assert sha(B / 'own-solves.json') == read(B / 'solve-frozen-before-reveal.json')['solveFileSha256']
assert sha(B / 'ratings-before.json') == read(B / 'ratings-frozen.json')['ratingsSha256']
ratings = read(B / 'ratings-before.json')['ratings']
assert len(ratings) == 10 and sum(q['scoreBeforeFix'] for q in ratings) == 47
for name in ['source-key-model-checks.json', 'native-after-source-checks.json',
             'density-prior295-review.json', 'preservation-check.json']:
    assert read(B / name)['status'] == 'PASS', name
logs = ['host-before.log', 'host-after.log', 'host-density-prior295.log',
        'host-density-prior295-after.log', 'snapshot-regression.log']
for name in logs:
    assert 'All tests passed!' in (B / name).read_text(encoding='utf-8-sig'), name
now = datetime.now(ZoneInfo('Asia/Seoul')).isoformat()
write(B / 'visual-review.json', {
    'status': 'reviewed', 'reviewedAt': now,
    'scope': 'Same-author manual inspection of all ten original source pages and the before-display contact sheets; selected after-display pages of the three changed targets and three related prior295 questions. Automated host coverage uses four viewport configurations; this is not device testing.',
    'targetAfterScreens': [
        'screens-after/kr-mpm-2023-07-22-psat-s-20-390-start.png',
        'screens-after/kr-mpm-2023-07-22-psat-s-20-390-page-04.png',
        'screens-after/kr-mpm-2023-07-22-psat-s-20-390-page-05.png',
        'screens-after/kr-mpm-2024-07-27-psat-s-24-390-start.png',
        'screens-after/kr-mpm-2024-07-27-psat-s-24-390-page-02.png',
        'screens-after/kr-mpm-2024-07-27-psat-s-24-390-page-03.png',
        'screens-after/kr-mpm-2024-07-27-psat-s-23-390-page-02.png',
        'screens-after/kr-mpm-2024-07-27-psat-s-23-390-page-03.png'],
    'relatedAfterScreens': [
        'screens-density-prior295-after/kr-mpm-2025-03-08-psat-s-17-390-start.png',
        'screens-density-prior295-after/kr-mpm-2025-03-08-psat-s-17-390-page-01.png',
        'screens-density-prior295-after/kr-mpm-2025-03-08-psat-s-18-390-start.png',
        'screens-density-prior295-after/kr-mpm-2024-03-02-psat-s-27-390-start.png',
        'screens-density-prior295-after/kr-mpm-2024-03-02-psat-s-27-390-page-02.png'],
    'findings': 'Native body text and adaptive table cards are legible at 390 width, with more scrolling. All source symbols, unknown cells, units and fractions were separately checked in native-after-source-checks.json and density-prior295-review.json. Water explanation now separates April 5 after filling from April 6 during filling. Existing original images and past snapshots remain available.',
    'limitations': 'Selected screenshots were manually inspected; no claim of manual inspection of every generated screenshot or real-device validation.'
})
visual = read(B / 'visual-review.json')
for name in visual['targetAfterScreens'] + visual['relatedAfterScreens']:
    assert (B / name).is_file(), name
changes = read(OUT / 'changes-batch08.json')
assert len(changes) == 6
for change in changes:
    change['status'] = 'source_key_semantics_and_host_reverified'
write(OUT / 'changes-batch08.json', changes)
write(B / 'batch-verification.json', {
    'status': 'verified', 'verifiedAt': now, 'count': 10,
    'ownSolves': 'own-solves.json', 'solveFrozenReceipt': 'solve-frozen-before-reveal.json',
    'ratings': 'ratings-before.json', 'frozenRatingsReceipt': 'ratings-frozen.json',
    'beforeScoreTotal': 47, 'beforeMean': 4.7,
    'targetQuestionsChanged': 3, 'relatedPrior295RecheckedAndChanged': 3,
    'sourceKeyModels': 'source-key-model-checks.json',
    'nativeAfterSourceChecks': 'native-after-source-checks.json',
    'relatedSourceKeyModels': 'density-prior295-review.json',
    'hostBefore': logs[0], 'hostAfter': logs[1],
    'relatedHostBefore': logs[2], 'relatedHostAfter': logs[3],
    'hostTestCount': 24,
    'hostScope': 'Ten targets and three related prior295 questions, before/after, four viewport configurations and original-page pinch coverage.',
    'snapshotRegression': {'log': logs[4], 'testsPassed': 3,
        'catalogScope': 'Loaded after the three primary target repairs and before the final three related prior295 native-display repairs. Final related repairs have their own current-head six-test host pass. This is not final current-head acceptance of all900.'},
    'visualReview': 'visual-review.json', 'preservation': 'preservation-check.json',
    'previouslyExposedOfficialAnswers': 0, 'solvesFrozenBeforeReveal': 10,
    'firstPassReasoningCorrections': 1,
    'reasoningCorrection': 'post-reveal-reasoning-correction.json',
    'limitations': 'Same-author review. One initially invalid countermodel was corrected after reveal; original solve retained. Broader cross-candidate queues and final all900 acceptance remain pending. No APK/device operations.'
})
spec = importlib.util.spec_from_file_location('remaining_review', ROOT / 'tools/review_remaining605.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
import contextlib
with (B / 'refresh-close.log').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
    module.refresh()
progress = read(OUT / 'progress.json')
assert [progress[k] for k in ['solvedCount', 'scoredCount', 'verifiedCount', 'nextBatch']] == [80, 80, 80, 9]
progress.update(status='paused', pausedAt=now, lastVerifiedBatch=8,
                pauseReason='사용자 요청: 현재 10문항 단위와 연관 검증을 마감하고 안전하게 일시중지.',
                resumeNote='PAUSED-20261030.txt', remainingCount=525)
write(OUT / 'progress.json', progress)
note = '''2026-10-30 사용자 요청에 따른 단위 마감 후 일시중지

현재: 고정605개 중80개(1~8묶음) 새 재풀이·수정 전 평가·개선·10개 단위 검증 완료.
남은525개. 다음 시작은9번째 자료해석10문항. 9묶음은 시작하지 않았다.
재개는 사용자 명시 지시 후에만 한다. 기존 준비 전용 문서와 고정 목록은 그대로 둔다.
기준 상태: progress.json / batch08/batch-verification.json.

수정 전 누적 점수384/80=4.80. 수정으로 최초 점수를 올려 쓰지 않았다.
현재까지 대상16개와 연관 기존295 중10개, 총26개 문항을 개정했다.
이번8묶음은 대상3개와 연관 기존3개 수정. 기존295의 과거 개별점수 보존.
보존검사:3259파일, 미수정874문항,26개 명시된 revision만 변경. 모든 기존 자산·Set·비타민 수정·release APK 보존.
현재 묶음 전후 호스트검사24 PASS. 기존 스냅샷 회귀3 PASS는 마지막 연관3개 수정 전 로드된 카탈로그이며, 최종 연관3개는 별도 현재 소스 호스트6 PASS로 확인했다. 전체900 최종 인수 검사는 아직 남아 있다.
APK 빌드·설치·기기 조작은 하지 않았다.

재개 주의:
- init 재실행 금지. preparation/ 고정 목록·최초점수·기존 증거를 덮어쓰지 않는다.
- 기존 묶음 reveal 재실행 금지(수정 전 객체를 덮어쓸 수 있음).
- 양방향 교차검증은 cross-validation.json 및 cross-candidates-*.json의 미결 항목을 계속 처리한다. 전체 교차검증 완료 상태가 아니다.
- progress.answerExposureBeforeSolve에 공식키 사전 노출68개가 기록되어 있다. 해당 문항을 맹검으로 표현하지 않는다. 공식키 페이지 전체를 출력하지 않고 현재 문항 번호만 확인한다.
- batch08/post-reveal-reasoning-correction.json: 초벌 풀이1개의 잘못된 반례를 해설 대조 후 정정했다. 원풀이를 보존하며 완전히 자력으로 맞은 초벌 추론이라 표현하지 않는다.
- 자체 검토이며 독립 감수나 무오류 보장이 아니다. 전체605 작업은 미완료다.
- 비타민·기록·ID/Set·답안·메모·과거 스냅샷·자산 보존. 중간 APK 빌드·설치·기기 조작 금지 유지.
'''
(OUT / 'PAUSED-20261030.txt').write_text(note, encoding='utf-8')
agents = ROOT / 'AGENTS.md'
heading = '[2026-10-30 최신 — 사용자 요청에 따른 8묶음 마감 후 일시중지]'
existing = agents.read_text(encoding='utf-8-sig')
assert heading not in existing
agents.write_text(heading + '\n사용자가 “잠깐 멈출수있는 상태에서 멈춰봐. 갑자기멈추진말고, 한 단위 끝내고 나서.”라고 요청했다. 현재 8번째10문항과 연관 기존3개 수정·검증·보존 기록을 마감하여 고정605개 중80개 완료,525개 남음. 다음은9번째 자료해석10문항이며 아직 시작하지 않았다. 사용자 명시 재개 전 새 재풀이·평가·콘텐츠 수정을 시작하지 않는다. 실제 상태는 artifacts/psat_remaining605_20261030/progress.json 및 PAUSED-20261030.txt를 따른다. 비타민·기존기록·고정 목록·최초점수·자산·기기·release APK 보존, 중간 빌드 없음. 아래 진행 지시는 이번 일시중지로 대기 상태가 된다.\n\n' + existing, encoding='utf-8')
print('SAFE PAUSE SAVED: verified80/605, remaining525, nextBatch9; batch08 closed, no batch09 started.')
