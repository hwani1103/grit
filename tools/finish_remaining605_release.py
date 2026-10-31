import re,shutil
import review_remaining605 as r
out=r.OUT/'final'
checks=r.read(out/'test-closure.json');preserved=r.read(out/'preservation-check.json');apk=r.read(out/'release-verification.json');cross=r.read(out/'cross-queue-closure.json');rating=r.read(out/'ratings-summary.json');changes=r.read(out/'change-summary.json');progress=r.read(r.OUT/'progress.json')
assert all(v['status']=='PASS' for v in [checks,preserved,apk,cross])
assert progress['verifiedCount']==605
assert len(progress['answerExposureBeforeSolve'])==69 and len(progress['postRevealReasoningCorrections'])==19
assert 'No issues found' in (out/'analyze.log').read_text(encoding='utf-8-sig')
assert r.read(out/'test-output-preservation.json')['status']=='PASS'
name='605문항_재검수_최종완료보고_2026-10-31.txt';path=r.ROOT/name;assert not path.exists()
text=f'''GRIT 고정605문항 재검수 및 최종 release 완료 / {r.now()}

1. 완료 범위
고정605개(언어202/상황202/자료201)를61묶음으로 원문 기반 새 직접풀이, 수정 전 개별 평가, 발견사항 개선, 공식 최종정답·선택지·표시 검증까지 마쳤다.
기존295개에서는 결함 원인에 연결된125개를 개별 재확인했고, 이번605개 중 연관16개도 추가 교차검증했다. 후속 교차묶음62~69와18개 원인군 대기 목록을 마감했다. 기존295개 전부를 이번에 새로 재풀이했다는 뜻은 아니다.
총900문항(과목별300),90 Set 유지.900개 공식정답 연결,원문·정답 파일41개 해시 및 자산을 최종 대조했다.

2. 최초 점수와 실제 개선
605개 수정 전 평균 {rating['mean']:.8f}/5. 5점354개/4점247개/3점4개.
언어4.6782,상황4.6287,자료4.4279. 최초 점수와 초벌 풀이·고정 목록은 보존했다.
이번605개 수정 전 평균은4.8에 못 미친다. 개선 후 점수를 올려 재평가하거나4.8을 달성했다고 표시하지 않았다.
605개 중257개,기존295개 중78개,합계335개를 근거에 따라 개정했다. 나머지565개는 객체 해시가 시작 시점과 같다. 문항revision과 변경 전 스냅샷을 보존했다.
주요 개선은 조건·경계·반례·정답 확정 경로,수치 근거,원문 밑줄 범위,조문·주석 구분,읽기 순서,작은 글씨 이미지 본문의 네이티브 전환이다. 필요한 원형 표·그래프·수식 이미지는 유지했다.

3. 최종 검사
전체 Flutter 검사 실행 로그: final/full-tests.log. 182개 통과·45개 실패가 기록된 뒤 실행 호스트 PowerShell이 CLR 오류로 종료되었다. 중단 당시 남은3개 검사 파일은100개씩 새 프로세스로 나누어 재실행했다(이미 완료한 두 화면규격의900문항 검사는 중복 실행하지 않음). 대화상자·화면전환·752/840폭 각 범주에서900개 고유ID가 모두 통과했음을 final/recovery-coverage.json으로 확인했다. 로그는 final/recovery/.
초기45건 실패는 수정 전 이미지 수·본문 위치·밑줄 등의 기대값이었다. 원문 검증 근거에 맞춰 기대값 검사45파일을 수정하고,3파일에는 기본 전수 범위를 유지하는 분할 실행 지원을 추가했다.48파일의 원본을 별도 보존했다.
변경한 일반검사46개와 영향받은/추가 화면검사4개를 재실행해 통과했다. 전체 실행 결과와 재검사 연결은 final/test-closure.json에 기록했다. 두 번째 전체 실행을 했다는 뜻은 아니다.
lib/test 정적분석 No issues found. 초기 분석 서버 인코딩·메모리 오류 및 스타일 지적 로그도 보존했다.
호스트 검사이며 실제 기기에서 검증한 결과는 아니다. 자동검사만으로 모든 문항의 무오류를 보장하지 않는다.

4. 보존
비타민 UI·시간 집계 수정,기존ID·Set·완료기록 저장 코드,답안·메모·과거 문항/해설 스냅샷,기존 원본/자료 자산과 release APK를 보존했다.
검사가 생성한 새 화면은 final/regression-screens에 분리했고 기존1611개 PNG는 원래 바이트로 복구했다.
폰·태블릿 조작,기기 설치,앱 데이터 초기화,컴퓨터 종료 없음.

5. APK
파일: {apk['apk']}
버전:1.3.1+5001 / com.gritpractice.grit / arm64-v8a
빌드 시 --build-name=1.3.1 --build-number=5001을 지정했다. pubspec.yaml의 기존 버전 문자열은 보존했다.
SHA-256: {apk['sha256']}
서명 인증서 SHA-256: {apk['certificateSha256']}
기존1.3.0+5000과 같은 서명임을 확인했다. 기존 release 파일은 덮어쓰지 않았다.
APK 내부900문항 JSON과Set,원본·자료이미지{apk['currentAndHistoricalImageBytesVerified']}개를 현재 소스와 바이트 대조했다. 비타민 수정도 이번 최종 APK에 포함된다.
설치 명령(실행하지 않음):
adb -s R5KL20DHWAE install -r "{apk['apk']}"

6. 검토 범위와 한계
같은 작성자의 재검토이며 독립 전문가 감수가 아니다. 일부69개는 새 풀이 전 답 노출 이력이 있고 해당 목록을 progress.json에 남겼다.
초벌 풀이의 정답 대조 후 교정19건은 원본을 덮어쓰지 않고 별도 근거로 보존했다. 이를 앱 정답 오류19건으로 해석해서는 안 된다.
67개 선택지 접두부와6개 상황 머리말 검사는 해당 구조만 확인한 검사이며 추가 전수 재풀이 수로 세지 않았다.

7. 증거 위치
artifacts/psat_remaining605_20261030/
preparation/: 고정목록·최초기준. batch01~61/:605개 개별근거. batch62~69/:후속 연관근거.
final/: 최초점수 집계,900공식키 대조,교차검증 마감,검사 원본/수정 영수증,실행 로그,보존 검사,APK 검증.
'''
path.write_text(text,encoding='utf-8')
progress.update(status='complete',finalPhase='complete',finalPhaseEvidence='final/release-verification.json',completedAt=r.now(),finalReport=name,releaseVerification='final/release-verification.json',finalVerification='final/test-closure.json',crossValidation='final/cross-queue-closure.json',releaseBuilt=True,installed=False,deviceOperations=0)
r.write(r.OUT/'progress.json',progress)
c=r.read(r.OUT/'cross-validation.json');c['status']='complete';c['finalEvidence']='final/cross-queue-closure.json';r.write(r.OUT/'cross-validation.json',c)
agent=r.ROOT/'AGENTS.md';shutil.copy2(agent,out/'AGENTS-before-final.txt')
prefix=f'[2026-10-31 최신 — 고정605 재검수·교차검증·최종 release 완료]\n고정605개61묶음 재풀이·수정 전 평가·개선 완료. 기존295 중 연관125개와605 중 연관16개 교차검증,18원인군 마감. 전체900개/90Set 유지,335개 개정·565개 보존. 최초605 평균4.578512는 상향 변경하지 않음. 전체 회귀 후45개 낡은 기대값 실패를 수정하고46일반검사+4화면검사 재실행 통과,lib/test 정적분석 통과. release1.3.1+5001 기존동일서명·APK내부900개/자산검증 완료. 비타민/기록/과거자산/기존APK 보존. 기기 설치·조작·종료 없음. 같은 작성자 검토이며 독립감수/무오류보장 아님. 상세 {name} 및 artifacts/psat_remaining605_20261030/final/. 이번 작업 종료,추가제작은 새 사용자 지시를 따른다.\n\n'
agent.write_text(prefix+agent.read_text(encoding='utf-8-sig'),encoding='utf-8')
resume=out/'RECOVERY-RESUME.txt'
resume.write_text('완료됨: 최종release검증과보고까지마감. 아래는복구중역사기록이며새실행지시가아니다. '+r.now()+'\n\n'+resume.read_text(encoding='utf-8-sig'),encoding='utf-8')
print('Completed report and progress:',name)
