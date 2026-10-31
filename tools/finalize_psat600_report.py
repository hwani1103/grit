"""Close the user-requested milestone only after final host checks pass."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'artifacts/psat600_20261028'
FINAL = ART / 'final600'
log = (FINAL / 'flutter-all.log').read_text(encoding='utf-8-sig')
analysis = (FINAL / 'flutter-analyze.log').read_text(encoding='utf-8-sig')
assert 'All tests passed!' in log and '[E]' not in log
assert 'No issues found!' in analysis
tests = int(re.findall(r'\+(\d+): All tests passed!', log)[-1])
integrity = json.loads((FINAL / 'integrity.json').read_text(encoding='utf-8'))
assert integrity['status'] == 'PASS' and integrity['questions'] == 600
report_name = '600문항_중간보고_2026-10-29.txt'
report = f'''GRIT 600문항 중간 보고 — 2026-10-29

현재 호스트 소스: 언어논리200 · 상황판단200 · 자료해석200 = 총600문항.
과목별20개 Set, 총60개 Set이며 각 Set은 고정10문항이다.
사용자가 지정한 과목별200/총600 경계에 도달하여 신규 제작을 중단했다.
과목별400은 이후 목표이며, 후속 사용자 지시 전에는 추가하지 않는다.

이번 재개에서 완료한 범위
기존450문항을 유지하고 과목별16~20번 묶음, 총15묶음150문항을 추가했다.
450 시점에 준비했던50문항과 자료17 초안을 다시 대조·완성한 뒤 이어갔다.
각10문항마다 공식 원본·시험일·책형·원번호·최종 정답, 직접 풀이,
다섯 선택지의 근거, 반례·경계조건, 원본 이미지 및 앱 표시를 검증했다.
완료 증빙은 artifacts/psat600_20261028/{{verbal,situation,data}}{{16..20}}/
각 폴더의 content-checks.json, completion.txt, flutter-final.log,
visual-review.json과 화면 캡처에 보존했다.

해설 방향
착안점 → 실전 풀이 → 답 확정 기준 → 정석 근거 → 적용 한계를 유지했다.
근거 위치·주체·범위·예외를 먼저 찾고, 계산은 공통분모·증감분·상하한으로
줄일 수 있는 경우에만 줄였다. 조합형은 실제 선택지에서 답이 유일하게
남는지 확인했고, 근삿값은 오차 때문에 판정이 뒤집히지 않는 범위를 밝혔다.
자료17의 연령 평균은 구체적 반례, 자료19의 교차표는 가능한 생산액 하한,
자료20의 반영 비율은 가중평균과 반올림 오차로 검산했다.
반복 어구 중 일부만 밑줄인 문항은 원본 이미지로 정확한 위치를 보존했다.
자료 표·그래프의 단위·주석·범례와 이어지는 오른쪽 열도 포함했다.

최종 검증
- Flutter 전체 호스트 테스트: {tests}개 PASS.
- Flutter analyze: No issues found.
- 600개 고유 문항·과목별200·60개 Set·Set당10·중복 소속 없음: PASS.
- 기존450문항 관련 자산 {integrity['preservedBaselineAssets']}개 해시 일치 및 기존45개 Set 동일: PASS.
- 새15묶음 원고 JSON과 게시본 동일, 스테이징 파일 {integrity['stagedFilesMatchPublished']}개 동일: PASS.
- psat_model.dart와 pubspec.yaml은 새 JSON15개 등록 외 기존 내용 동일: PASS.
- 묶음별 본문/그림 확대 및 전체해설 스크롤 검사, 좁은 폰·펼친 폴더블·가로 화면 검사를 수행했다.
  저장·기록 스냅샷·완료진도·폴더블 확인창 등 기존 기능은 전체 회귀검사에 포함된다.
로그: artifacts/psat600_20261028/final600/flutter-all.log
분석: artifacts/psat600_20261028/final600/flutter-analyze.log
보존 검사: artifacts/psat600_20261028/final600/integrity.json

적용 범위와 남은 경계
600문항은 호스트 소스의 검증 완료 수다. APK 빌드·설치, ADB/SRTL 연결,
물리 폰·태블릿 조작, 사용자 데이터 초기화는 하지 않았다.
기존 UI·기능·문항 ID·고정 Set 및 과거 완료 기록의 스냅샷 계약을 유지했다.
기존 설치 APK에는 이번150문항을 전달하지 않았다.
호스트 화면 검증을 실기기 검증이나 사용자 최종 시각 승인으로 표현하지 않는다.
자체 풀이와 도구 검산을 거쳤으며 전문가의 독립 감수나 무오류 보장을 뜻하지 않는다.

다음 세션
루트 인수인계문 최상단과 본 보고서를 먼저 읽고, 사용자 후속 지시를 기다린다.
재개 준비 기록의 미게시50문항/자료17 초안 표기는450 당시 이력이며 지금은 완료됐다.
그 준비 스크립트를 다시 실행하거나 같은 묶음을 중복 게시하지 않는다.
'''
(ROOT / report_name).write_text(report, encoding='utf-8')
summary = f'''[최신 상태 2026-10-29 — 과목별200/총600 완료, 제작 중단·중간보고]
언어논리200·상황판단200·자료해석200, 총600문항/60 Set 호스트 검증 완료.
이번 재개에서15묶음150문항을10개씩 원본·공식정답·직접풀이·5단계해설·표시 검증 후 추가했다.
전체 Flutter {tests} PASS / analyze No issues found / 기존450 자산788개·45 Set 보존 PASS.
사용자 지정600 경계에서 중단. 후속 지시 전 새 문항 제작·게시를 실행하지 않는다.
기존UI/기능 유지, APK 빌드·설치·기기 조작 없음. 설치본과 호스트600문항은 구분한다.
중간보고: {report_name}
최종검사: artifacts/psat600_20261028/final600/
아래450 일시중지/재개준비/제작중 기록은 이전 이력이다.

'''
handoff = ROOT / '다음세션_600문항_제작_인수인계_2026-10-28.txt'
handoff.write_text(summary + handoff.read_text(encoding='utf-8'), encoding='utf-8')
resume = ART / 'resume-preparation-20261029/READ-ME-resume.txt'
resume.write_text(summary + '아래 준비50문항 및 자료17 초안은 이번 재개에서 모두 검증·게시 완료했다. 재게시 금지.\n\n' + resume.read_text(encoding='utf-8'), encoding='utf-8')
for filename in ('AGENTS.md', 'PSAT_CONTENT_REVIEW.md', 'VERIFICATION.md'):
    with (ROOT / filename).open('a', encoding='utf-8') as file:
        file.write('\n\n' + summary)
readme = ROOT / 'README.md'
text = readme.read_text(encoding='utf-8')
notice = f'2026-10-29 최신 콘텐츠: 과목별200, 총600문항/60 Set 검증 완료 후 제작 중단. 전체 호스트 검사{tests} PASS, 분석 오류 없음. 기존 설치 APK는 변경하지 않았다. 상세: [{report_name}]({report_name}). 아래 날짜별 이전 기록보다 이 상태를 우선한다.\n\n'
readme.write_text(text.replace('# GRIT\n\n', '# GRIT\n\n' + notice, 1), encoding='utf-8')
path = ART / 'progress.json'
progress = json.loads(path.read_text(encoding='utf-8'))
progress['previousPausedAtVerifiedTotal'] = progress.pop('pausedAtVerifiedTotal', 450)
progress.update(nextBatch='없음:600 중간보고 완료, 후속 사용자 지시 대기', parked='준비50문항과 자료17 초안 모두 검증·게시 완료', partialDraft=None,
                currentTaskStatus='과목별200/총600 검증 완료;사용자 지정 경계에서 제작 중단·중간보고',
                currentVersion='Existing installed APK unchanged;host source600questions;no build/install',
                milestoneStopped=True, milestoneReport=report_name,
                lastVerification=f'final600:Flutter {tests} PASS;analyze No issues;600 unique/60sets;788 baseline assets and45sets preserved',
                verifiedInAppMeaning='호스트 소스 검증 완료 수. 설치 APK 반영 수 또는 실기기 검증 수가 아님.')
progress['candidateGrade5']['reviewedAtEarlierSnapshot'] = progress['candidateGrade5'].pop('reviewed', None)
progress['candidateGrade5']['reviewedCountNote'] = '이전 reviewed=5는 과거 후보 검수 시점의 값. 다운로드1200과 현재 검증완료600을 혼동하지 않음.'
path.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'Final report saved: {report_name}; full tests={tests}')
