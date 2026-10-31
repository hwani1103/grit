import re
import review_remaining605 as r
b=r.folder(47);old={x['question']['id']:x['question'] for x in r.read(b/'revealed-current.json')};related={q['id']:q for q in r.read(b/'related295-before.json')}
for n in ['host-before.log','related295-host-before.log']:assert 'All tests passed!' in (b/n).read_text(encoding='utf-8-sig')
for n in ['source-key-model-checks.json','related295-source-key-model-checks.json']:assert r.read(b/n)['status']=='PASS'
notes={39:'원형 대칭 배치와 교 분류, 공전 기준 및 입춘/우수/입하 구분 정확. 긴 한 문단의 기·입·교·극 분류를 각각 분리해 탐색 개선.',1:'자료요청 주체/필요조건, 평가 예외의 이 조 범위, 보고 방향 정확. 줄갈이에서 갈라진 전략위원회와 기본계획 괄호 연결.',2:'지정/승인/해제 주체, 의견진술/통보 및3개월 조건 정확. 구청장과 바로 뒤 정의 괄호 연결.',3:'규모와 국내영향 결합조건, 발생/규모예상 및 예외 승인 절차 정확. 발견없음.',4:'예치금→적립금·수혈비용/부작용보상, 채혈/수혈과 재량 구별 정확. 손해배상청구소송 어절 연결.',6:'신청분야 경력·마감일3년 경계 및 지급해말2025년 기한 정확. 발견없음.',7:'분모1.2배의 역수5/6, 감소율/%p 구별 및 고정분자 반례의 한계 정확. 발견없음.',8:'X6km/L/20L와16L당88km 차, 갤런/리터 및 역수 지표 구별 정확. 발견없음.',9:'두 사람별6개 금리와 우대 상한·신규·소득 및 미지청약의 무관성 정확. 원표 픽셀/줌 검사; 발견없음.',10:'전체1000후보 중0000/3310만 조건 충족, 합0/7 및 존재/필연 구별 정확. 발견없음.'}
fix={39,1,2,4};ratings=[dict(id=i,scoreBeforeFix=4 if q['number'] in fix else 5,assessment=notes[q['number']],needsChange=q['number'] in fix) for i,q in old.items()]
assert not (b/'ratings-before.json').exists();r.write(b/'ratings-before.json',dict(method='Same-author original solves frozen before reveal; original/native/key and exact models; pre-edit target and related host views reviewed.',ratings=ratings));r.write(b/'ratings-frozen.json',dict(frozenAt=r.now(),ratingsSha256=r.sha(b/'ratings-before.json'),total=46,count=10,beforeChanges=True))
hist={x['id']:x for x in r.read(r.PREP/'previously-scored295.json')['questions']}
r.write(b/'related295-assessment-before.json',[dict(id=i,historicalScorePreserved=hist[i]['scoreBeforeFix'],currentBeforeScore=4 if q['examDate'].startswith('2025') else 5,assessment='원문24절기 배치와 기준제외12칸 및 모든선지 간격 정확. 공통39와 동일하게 분류별 문단 분리.' if q['examDate'].startswith('2025') else '40%하락의 역산·동일시점 가격비·예산 및5개수량 검산 정확, 발견없음.',notReplacementOfHistoricalScore=True,changed=q['examDate'].startswith('2025')) for i,q in related.items()])
def classify(body):
 for marker in ['‘기’는 사계절의 기본','‘입’은 계절로 들어서는','‘교’는 계절이 교차하는','‘극’은 계절의 절정']:
  assert body.count(' '+marker)==1;body=body.replace(' '+marker,'\n\n'+marker)
 return body
changes=[]
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  is_related=q['id'] in related
  if not((q['id'] in old and q['number'] in fix) or (is_related and q['examDate'].startswith('2025'))):continue
  prev=(related if is_related else old)[q['id']];assert q==prev;snap=r.OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();r.write(snap,prev)
  if q['examDate'].startswith('2025'):q['body']=classify(q['body'])
  elif q['number']==1:q['body']=q['body'].replace('전략 위원회','전략위원회').replace('기본계획 (이하','기본계획(이하')
  elif q['number']==2:q['body']=q['body'].replace('구청장 (이하','구청장(이하')
  elif q['number']==4:q['body']=q['body'].replace('손해배상청구 소송','손해배상청구소송')
  assert q!=prev and re.sub(r'\s','',q['body'])==re.sub(r'\s','',prev['body'])
  fields=sorted(k for k in q if q[k]!=prev.get(k));assert fields==['body'];q['revision']+=1;touched=True
  changes.append(dict(id=q['id'],file=p.relative_to(r.ROOT).as_posix(),oldRevision=prev['revision'],newRevision=q['revision'],changedFields=fields,beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason=notes[39] if is_related else notes[q['number']],status='repaired_pending_reverification'))
 if touched:r.write(p,data)
assert len(changes)==5;r.write(r.OUT/'changes-batch47.json',changes)
bank=r.bank();assert bank['kr-mpm-2025-03-08-psat-s-39']['body'].split('<보 기>')[0].strip()==bank['kr-mpm-2025-03-08-psat-s-40']['body'].split('<상 황>')[0].strip()
r.write(b/'repair-semantic-checks.json',dict(status='PASS',count=5,bodyWhitespaceOnly=True,allAnswersOptionsStepsUnchanged=True,shared39340PrefixIdenticalAfter=True,tableAssetUnchanged=True))
r.write(b/'after-sample.json',dict(sample=[dict(id=i) for i in list(old)+list(related)]))
print('Frozen46/50;4targets+1related whitespace-only;all text characters preserved')
