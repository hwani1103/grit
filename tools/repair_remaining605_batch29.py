import review_remaining605 as r
b=r.folder(29);before={x['question']['id']:x['question'] for x in r.read(b/'revealed-current.json')};own={x['id']:x for x in r.read(b/'own-solves.json')}
notes={
 ('2026-07-18',14):'네 국기와 다섯 국기의 실제 좌우배치를 직접 작성해 세 보기와 모두 대조했다. 우선순위와 공간 순서, 관찰 방향을 정확히 구별한다.',
 ('2026-07-18',16):'50분5/6시간·3시간30분3.5시간으로 바꾸어1000+100+700=1800mAh, 성능0.9를 검산했다. 다섯 선택지의 환산 용량이 정확하다.',
 ('2026-07-18',17):'3g이하 제외·편도/왕복·5km이하 경계·정수 구매량을 모두 적용해 B19.5,C18,D20,E13.5g을 확인했다.',
 ('2026-07-18',18):'표의 전체 가중합50/52/45/50/45, 최고B제외와 A/D동점 중 재택A선택의 순서가 정확하다.',
 ('2026-07-18',20):'통행료만 할인하는 계산과 C양의 부분합 하한을 통한 중단 기준은 정확하다. 원문 면적단위 km²가 km2로 전사되어 있고50 %의 경계를 연결해야 한다. 같은 공통지문의 기존5점19번도 재확인한다.',
 ('2026-07-18',22):'각 종류 최소1·보유상한·100MB를 전수 탐색하여 유일한1/1/24/2구성91점28건을 확인했다. 손실8로92점이 불가능하고91점의 유일성을 증명한 기존 풀이가 타당하다.',
 ('2026-07-18',23):'여섯 경로의 C전후구간을 전수검산해 ACBDA/ADBCA만 가능함과 귀환잔량0/20km를 확인했다. 개별 선지 일부가 단순 정오 판정에 그쳐 구간 및 반례를 명시한다.',
 ('2026-03-07',13):'주제 크기 조합별 번호 존재 여부를 전수 검산해1-2최대5,2-2두개일때4-1최대4와 ㄷ필연성을 확인했다. 개별 조합선지에 구체적 이유를 보강하고 첫 질의 번호의 PDF 줄갈이 공백을 복원한다.',
 ('2026-03-07',14):'각 거리 상·하한뿐 아니라 같은방향/반대방향교대 배치로 모든구간의 동시 달성을 확인했다.125−25=100km,4시간이 정확하다.',
 ('2026-03-07',15):'총합51의 약수와 서로다른양의점수 최소합6으로3회 확정. 가능한 모든점수와 매회순열에서 X8Y5Z4·유일평가표를 확인했다. 앞두평가 X최대1회일때 갑최대18 설명도 타당하다.'}
fix={('2026-07-18',20),('2026-07-18',23),('2026-03-07',13)}
ratings=[dict(id=qid,scoreBeforeFix=4 if (q['examDate'],q['number']) in fix else 5,assessment=notes[(q['examDate'],q['number'])],deduction='원문 표시/개별 선지 근거 개선' if (q['examDate'],q['number']) in fix else '발견 없음',needsChange=(q['examDate'],q['number']) in fix) for qid,q in before.items()]
if not (b/'ratings-before.json').exists():
 r.write(b/'ratings-before.json',dict(method='Same-author pre-edit original/own solve/key/all options/models/host review.',ratings=ratings));r.write(b/'ratings-frozen.json',dict(frozenAt=r.now(),ratingsSha256=r.sha(b/'ratings-before.json'),total=47,count=10,beforeChanges=True))
else:
 assert r.read(b/'ratings-before.json')['ratings']==ratings
 assert r.read(b/'ratings-frozen.json')['ratingsSha256']==r.sha(b/'ratings-before.json')
related=r.read(b/'related295-before.json')[0];before[related['id']]=related
r.write(b/'related295-assessment-before.json',dict(id=related['id'],historicalScorePreserved=5,currentBeforeScore=4,assessment='같은 면적단위 km2 전사와25 %의 수치·기호 분리. 직접풀이/해설정답은 일치하며 개별선지 판정근거도 보강한다.',notReplacementOfHistoricalScore=True))
changes=[]
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  if q['id'] not in before:continue
  k=(q['examDate'],q['number'])
  if q['id'] not in before or not (k in fix or q['id']==related['id']):continue
  old=before[q['id']];assert q==old;snap=r.OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();r.write(snap,old)
  if q['number'] in [19,20]:
   assert q['body'].count('km2')==1;q['body']=q['body'].replace('km2','km²').replace('50 %','50%').replace('25 %','25%')
  if k==('2026-03-07',13):q['body']=q['body'].replace('질의 번호','질의번호')
  if q['number'] in [13,23]:q['optionReasons']=own[q['id']]['optionReasons']
  if q['number']==19:q['optionReasons']=r.read(b/'related295-own-solves.json')[0]['optionReasons']
  fields=[k for k in q if q[k]!=old[k]];q['revision']+=1;touched=True
  changes.append(dict(id=q['id'],file=p.relative_to(r.ROOT).as_posix(),oldRevision=old['revision'],newRevision=q['revision'],changedFields=fields,beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason='Original unit/word boundaries and substantive option reasons; original words, values and answer preserved.',cohort='prior295' if q['number']==19 else 'fixed605',status='repaired_pending_reverification'))
 if touched:r.write(p,data)
assert len(changes)==4;r.write(r.OUT/'changes-batch29.json',changes)
print('Frozen47/50;3targets+related historical5point question repaired without changing historic score.')
