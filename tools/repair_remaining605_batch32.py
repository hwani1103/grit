import re
import review_remaining605 as r
b=r.folder(32);old={x['question']['id']:x['question'] for x in r.read(b/'revealed-current.json')}
notes={18:'구간별 포인트 역함수와 남는 포인트를 모두 만족하는 유일 조합3·9·5·14·11을 확인했다. 보너스 중복 적용과 포인트 총합54를 구별한 해설이 정확하다.',28:'무료6·2, 유료8·1의 정수 최적값66000/71000을 전수 대입으로 확인했다.20 % 표기와 일부 단순 판정뿐인 오답 이유를 보완한다.',33:'3일/5일 주기와 A 최소 빈도로 유일 주기를 확인했다. 정석 근거의 B·C를각 공백을 바로잡는다.',34:'시민 수 기준·동률 예외·다음 라운드 진입을 모두 만족하는 최소 스파이6과 실현 배치를 확인했다. 3라운드 시작 시민5명을 제외하는 이유도 명시해 상한 증명을 완결한다.',37:'직전 달 순위·3개월 연속·중복 배제·가격별 잔액을 월별로 검산했다. 다중 표제의 실제 열 대응은 원본과 표 추출 양쪽으로 일치한다. 선택지1의 미구입 원인과 나머지 월별 구입 이유를 보완한다.',21:'동의능력과 미성년 예외, 변경허가, 단기휴업 선택, 허가간주 확인 및 배우자 우선순위를 분리했다. 원문과 해설의 다섯 판단이 맞다.',22:'취업일 기산·150만원 상한·국적·3.5년 연장 가능·6개월 퇴직 요건을 확인했다. 북한이탈주민/정착지원시설/취업보호의 공백과 원문의 법령명 인용 괄호를 복원한다.',24:'500만원 경계·직접 취득3년·청구상대·상속과 재판매·사후30년을 모두 검산했다. 원문과 답1 및 해설이 맞다.',25:'배우자 우선과 연령 예외를 구별하고 유족120/본인116을 계산했다.20세 손자녀의 임의 장애 가정을 배제한 해설이 맞으며 본문 퍼센트 앞 공백을 복원한다.',29:'교환 순서를 적용한 정확한 분수식과 총량보존으로250을 도출했다.5선지 역대입 및250→240→210→125→35 경로가 맞다.'}
fix={28,33,34,37,22,25}
ratings=[dict(id=qid,scoreBeforeFix=4 if q['number'] in fix else 5,assessment=notes[q['number']],needsChange=q['number'] in fix,deduction='원문 표기·어절 또는 개별 근거·경계 증명 보완' if q['number'] in fix else '발견 없음') for qid,q in old.items()]
assert not (b/'ratings-before.json').exists()
r.write(b/'ratings-before.json',dict(method='Same-author original-only solve, selected official key, native/table and exact models, pre-edit host review.',ratings=ratings))
r.write(b/'ratings-frozen.json',dict(frozenAt=r.now(),ratingsSha256=r.sha(b/'ratings-before.json'),total=44,count=10,beforeChanges=True))
changes=[]
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  if q['id'] not in old or q['number'] not in fix:continue
  before=old[q['id']];assert q==before
  snap=r.OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();r.write(snap,before)
  n=q['number']
  if n==28:
   q['body']=q['body'].replace('20 %','20%')
   q['optionReasons'][0]='유료로 동작 8개·정지 1개를 만들면 71,000원을 얻을 수 있다. 가능한 이 조합보다 작은 59,000원은 최대 수익이 아니다.'
   q['optionReasons'][2]='유료로 동작 8개만 만들면 68,000원이지만 0.8시간이 남는다. 그 시간에 정지 1개를 더 만들어 3,000원을 추가할 수 있다.'
  if n==33:q['steps']=[s.replace('B·C를각','B·C를 각') for s in q['steps']]
  if n==34:q['steps'][1]=q['steps'][1].replace('따라서 시작 시민은 3명이다.','시작 참가자는 총 5명이므로 남은 경우는 시민 5명인데, 이때도 더 많은 쪽의 시민이 최소 3명 살아남아 종료할 수 없다. 따라서 시작 시민은 3명이다.')
  if n==37:
   q['optionReasons']=['호밀밭의 방관자는 2만 원이다. 1월에는 앞선 책으로 예산을 모두 썼고, 2월에는 White 심리학·AI 프롬프트 구입 후, 3월에는 일관 우선 구입 후 각각 1만 원만 남아 사지 못한다.','2월에는 전월 순위의 White 심리학·AI 프롬프트를 산 뒤 1만 원이 남는다. 중간의 2만 원 책들을 건너뛰어 실전 AI 에이전트 2를 산다.','3월에는 연속 순위 조건을 충족한 일관을 먼저 산다. 남은 1만 원으로 전월 순위 6위의 이타적 유전자 100가지를 산다.','2월에는 이미 산 스피드 코리아 2026을 건너뛰고 White 심리학과 AI 프롬프트를 순서대로 각 1만 원에 산다.','일관은 12월·1월·2월 모두 5위 안에 들고 아직 사지 않은 책이다. 따라서 3월에 순위 우선 규칙으로 2만 원에 산다.']
  if n==22:
   q['body']=q['body'].replace('북한 이탈주민','북한이탈주민').replace('정착지원 시설','정착지원시설').replace('장애인복지법 에','「장애인복지법」에')
   q['choices']=[s.replace('취업 보호','취업보호') for s in q['choices']]
  if n==25:q['body']=re.sub(r'(50|60|30) %',r'\1%',q['body'])
  assert q!=before;q['revision']+=1;touched=True
  changes.append(dict(id=q['id'],file=p.relative_to(r.ROOT).as_posix(),oldRevision=before['revision'],newRevision=q['revision'],changedFields=sorted(k for k in q if k!='revision' and q[k]!=before[k]),beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason=notes[n],cohort='fixed605',status='repaired_pending_reverification'))
 if touched:r.write(p,data)
assert len(changes)==6;r.write(r.OUT/'changes-batch32.json',changes)
bank=r.bank();norm=lambda s:re.sub(r'[\s「」]','',s)
for qid,before in old.items():
 q=bank[qid]
 assert q['answer']==before['answer'] and q.get('tables')==before.get('tables')
 assert norm(q['body'])==norm(before['body']) and [norm(s) for s in q['choices']]==[norm(s) for s in before['choices']]
 assert len(q['steps'])==len(q['optionReasons'])==5
assert r.sha(b/'own-solves.json')==r.read(b/'solve-frozen-before-reveal.json')['solveFileSha256']
assert r.sha(b/'ratings-before.json')==r.read(b/'ratings-frozen.json')['ratingsSha256']
r.write(b/'repair-checks.json',dict(status='PASS',targetChanges=6,sourceWordsAndTablesAndAnswersPreserved=True,explicitLawQuotationRestored='s22 source 「장애인복지법」',gameFiveCitizenBoundary='Five total participants; with five citizens, majority has at least three, so game continues.',productionAlternative='Paid eight motions take19.2h; one still takes remaining0.8h; gross83k minus12k gives71k.',immutableReceipts=True))
print('Frozen44/50;6 target repairs; answer/table/source words preserved.')
