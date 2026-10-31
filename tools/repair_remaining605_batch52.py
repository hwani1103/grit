import re
import review_remaining605 as r
b=r.folder(52);old={x['question']['id']:x['question'] for x in r.read(b/'revealed-current.json')};related={q['id']:q for q in r.read(b/'related295-before.json')}
for n in ['host-before.log','related295-host-before.log']:assert 'All tests passed!' in (b/n).read_text(encoding='utf-8-sig')
for n in ['source-key-checks.json','related295-source-key-checks.json','exact-model-checks.json','underline-source-strokes.json']:assert r.read(b/n)['status']=='PASS'
notes=['조건문단순화/외과0명반례/3명하한증명과6명달성모두정확. 자체초안은전수검산중반례발견후공개전수정했으며게시해설은이미정확.','세논거별강화방향/비율과총비용구별정확.기증자에게서가원문줄갈이로분리되어어절연결필요.','이론성공/실재의연결원리와사실판단분리정확,가능성과단정부재관계정확.','가설별원인기제수명변수대응과강화의한계정확.','측정차−지연차의부호/양방향반례정확.㉠원문밑줄은길어진다까지이며뒤는은밑줄밖이라범위수정.','엄격한p<유의수준/같은자료문턱변경예와사후확률혼동방지정확.','의도없는선택편향가능성과B약효불명확구별/p분포단정불가정확.','왕과국가와요청대상과시기대응정확.','사전사후보고/관행과관서구별/계유정난과원상시기정확.','발명자와전달자구별/바이킹전체언어/고형라틴어와시기범위정확.']
fix={list(old)[1],list(old)[4]};ratings=[dict(id=i,scoreBeforeFix=4 if i in fix else 5,assessment=n,needsChange=i in fix) for i,n in zip(old,notes)]
assert not (b/'ratings-before.json').exists();r.write(b/'ratings-before.json',dict(method='Source-only own answers frozen before current/key reveal. All10 match; initial source-only hiring draft5 corrected to4 by exhaustive check before freeze/reveal, disclosed in pre-reveal models.',ratings=ratings));r.write(b/'ratings-frozen.json',dict(frozenAt=r.now(),ratingsSha256=r.sha(b/'ratings-before.json'),total=48,count=10,beforeChanges=True))
hist={x['id']:x for x in r.read(r.PREP/'previously-scored295.json')['questions']}
r.write(b/'related295-assessment-before.json',[dict(id=i,historicalScorePreserved=hist[i]['scoreBeforeFix'],currentBeforeScore=4,assessment='원문풀이와5선지근거정확. PDF선끝밖마침표를밑줄에서제외;본문마침표는보존.',notReplacementOfHistoricalScore=True,changed=True) for i in related])
proof={x['id']:x['sourceRanges'] for x in r.read(b/'underline-source-strokes.json')['checks']};changes=[]
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  i=q['id']
  if i not in fix and i not in related:continue
  prev=(related if i in related else old)[i];assert q==prev;snap=r.OUT/f"before-changes/{i}-r{q['revision']}.json";assert not snap.exists();r.write(snap,prev)
  if i==list(old)[1]:
   assert q['body'].count('기증자 에게서')==1;q['body']=q['body'].replace('기증자 에게서','기증자에게서');reason=notes[1]
  else:
   q['underlines']=proof[i].copy()
   if i=='kr-mpm-2021-07-10-psat-l-13':q['underlines'][1]='㉠ '+q['underlines'][1];assert q['underlineLabelAnchors'] is True
   reason='원문PDF선끝일치: 뒤의 는 또는 마침표를 밑줄에서 제외. 반복구문용㉠앵커보존;문장원문그대로.'
  assert re.sub(r'\s','',q['body'])==re.sub(r'\s','',prev['body']) and q['answer']==prev['answer'] and q['choices']==prev['choices'] and q['steps']==prev['steps'] and q['optionReasons']==prev['optionReasons']
  fields=sorted(k for k in q if q[k]!=prev.get(k));q['revision']+=1;touched=True;changes.append(dict(id=i,file=p.relative_to(r.ROOT).as_posix(),oldRevision=prev['revision'],newRevision=q['revision'],changedFields=fields,beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason=reason,status='repaired_pending_reverification'))
 if touched:r.write(p,data)
assert len(changes)==4;r.write(r.OUT/'changes-batch52.json',changes)
r.write(b/'repair-semantic-checks.json',dict(status='PASS',targetChanged=2,relatedChanged=2,allAnswersChoicesStepsReasonsUnchanged=True,bodyCharactersPreserved=True,underlineEvidence='underline-source-strokes.json',historicalScoresPreserved=True))
r.write(b/'after-sample.json',dict(sample=[dict(id=i) for i in list(old)+list(related)]))
print('48/50 frozen;2target +2related repaired')
