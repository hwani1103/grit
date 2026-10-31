import json
import review_remaining605 as r
b=r.folder(58);old={x['question']['id']:x['question'] for x in r.read(b/'revealed-current.json')};related={q['id']:q for q in r.read(b/'related295-before.json')}
for n in ['host-before.log','related295-host-before.log']:assert 'All tests passed!' in (b/n).read_text(encoding='utf-8-sig')
for n in ['source-key-checks.json','related295-source-key-checks.json','pre-reveal-exact-models.json','underline-source-strokes.json']:assert r.read(b/n)['status']=='PASS'
notes=['기관별 관할/설치 목적과 세 빈칸 대응 정확.','상황 내 절대판정과 상황 간 기준 변동, 굴곡 존재와 요철 간주 구별 정확.','살수 철수 시점/공격 주체/회군 제안과 실제 명령 구별 정확.','정부 부과와 시장 가격 결정, 외부효과 내부화 방향 정확.','노동력 대비 생산성/거의 모두와 일부 함의 정확.','객관 시간과 주관 이미지 수/노화에 따른 상대적 느낌 구별 정확.','정답과 민감성 필요조건 반례 정확. ①의 모든 경우에 참이라는 필연성 범위를 일반적 참 조건과 구별하도록 개선.','합의 비용과 외부 비용의 반대 방향/합계 미정 정확.','로봇 사용과 책임 추궁이라는 행위 대상 구별 정확. 원문 밑줄의 기호 제외, 마침표 유지.','유사 기능과 다른 메커니즘/상사와 상동 구별 정확. 원문 밑줄의 기호 제외, 마침표 유지.']
fixes={i for i in old if i.endswith(('-l-28','-l-31','-l-32'))}
ratings=[dict(id=i,scoreBeforeFix=4 if i in fixes else 5,assessment=n,needsChange=i in fixes) for i,n in zip(old,notes)]
assert not (b/'ratings-before.json').exists();r.write(b/'ratings-before.json',dict(method='Original current-pass own10 frozen before current reveal. All10 historical key exposure disclosed; not blind or independent.',ratings=ratings));r.write(b/'ratings-frozen.json',dict(frozenAt=r.now(),ratingsSha256=r.sha(b/'ratings-before.json'),total=47,count=10,beforeChanges=True))
kinds=r.read(b/'related295-pre-reveal-models.json')['reviewKinds'];hist={x['id']:x for x in r.read(r.PREP/'previously-scored295.json')['questions']}
r.write(b/'related295-assessment-before.json',[dict(id=i,reviewKind=kinds[i],historicalScorePreserved=hist[i]['scoreBeforeFix'] if i in hist else 'Earlier fixed605 rating unchanged',currentBeforeScore=5 if kinds[i]=='prior295' else 4,assessment='군제 개편 시점/제안 취소와 실제 이관의 구별 정확; 수정 불필요.' if kinds[i]=='prior295' else '논증 방향과 조건문 반례 정확. 원문 밑줄 밖 마침표/기호를 제외한다.',notReplacementOfHistoricalScore=True,changed=kinds[i]!='prior295') for i in related])
proof={x['id']:x['sourceRanges'] for x in r.read(b/'underline-source-strokes.json')['checks']};changes=[]
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  i=q['id']
  if i not in fixes|set(proof):continue
  prev=(related if i in related else old)[i];assert q==prev;snap=r.OUT/f"before-changes/{i}-r{q['revision']}.json";assert not snap.exists();r.write(snap,prev)
  fields=[]
  if i in proof:
   q['underlines']=proof[i].copy();fields.append('underlines')
   if i in ['kr-mpm-2024-07-27-psat-l-19','kr-mpm-2024-07-27-psat-l-20']:q['underlines'][3]='㉣'+q['underlines'][3] # Stored occurrence anchor; renderer excludes its glyph.
  if i.endswith('2023-03-04-psat-l-28'):
   q['optionReasons'][0]='어떤 경우에서도 참이라는 말은 모든 가상 경우에도 참인 명제만 알 수 있다는 주장이다. 본문은 실제로 참이지만 다른 가상 경우에는 거짓일 수 있는 Q를 안다고 인정하므로 이 주장은 결론이 아니다.';fields.append('optionReasons')
  assert all(q[k]==prev[k] for k in prev if k not in fields);q['revision']+=1;touched=True
  changes.append(dict(id=i,file=p.relative_to(r.ROOT).as_posix(),oldRevision=prev['revision'],newRevision=q['revision'],changedFields=fields,beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason='필연 진리와 실제 참의 범위 구별 또는 PDF 선 끝에 맞춘 밑줄 범위 개선.',status='repaired_pending_reverification'))
 if touched:r.write(p,data)
assert len(changes)==6;r.write(r.OUT/'changes-batch58.json',changes)
r.write(b/'repair-semantic-checks.json',dict(status='PASS',targetChanged=3,associated605Changed=3,prior295Changed=0,sourceProof='underline-source-strokes.json',allBodiesAnswersChoicesFiguresUnchanged=True,historicalScoresPreserved=True))
r.write(b/'after-sample.json',dict(sample=[dict(id=i) for i in list(old)+list(related)]))
p=r.ROOT/'test/psat_remaining605_underline_boundary_test.dart';s=p.read_text(encoding='utf-8');anchor='      for (final entry in {\n';assert anchor in s
s=s.replace(anchor,anchor+''.join('        '+json.dumps(i)+': '+json.dumps(v,ensure_ascii=False)+',\n' for i,v in proof.items()),1);p.write_text(s,encoding='utf-8')
print('47/50 frozen;3target+3associated605 repaired; prior295 unchanged')
