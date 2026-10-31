import re,pdfplumber
import review_remaining605 as r
b=r.folder(54);old={x['question']['id']:x['question'] for x in r.read(b/'revealed-current.json')};related={q['id']:q for q in r.read(b/'related295-before.json')}
for n in ['host-before.log','related295-host-before.log']:assert 'All tests passed!' in (b/n).read_text(encoding='utf-8-sig')
for n in ['source-key-checks.json','related295-source-key-checks.json','exact-model-checks.json','underline-source-strokes.json']:assert r.read(b/n)['status']=='PASS'
notes=['단위환산/4년추세/반올림후증가반례정확. 원문밑줄은기호제외마침표포함; 숫자·단위·조사공백개선.','소득반올림하한/25%경계/모든오답과최댓값정확. 해설숫자·단위·조사공백개선.','구간별달성가능반례와상하한정확;해군상위50합과순위도검산통과.','교집합하한/반올림보수하한/정수25법인배치반례정확.','등급소속의필연성과반올림구간/점수차경계정확.','집합별인원하한과엄격순위/네배치열거정확. 조건4개가작은이미지라원문정보를네이티브화.','세금공통계수/부가세연동/전체비중순위및인하폭정확.','하위조사분모138/125와반올림구간분리정확. 원문밑줄은기호제외하고따옴표·마침표포함.','남녀조건전체/5국가제외근거/두배절반경계정확.','전체6업종한정/절반과여집합/열별순위/내외차정확.']
fix={list(old)[j] for j in [0,1,5,7]};ratings=[dict(id=i,scoreBeforeFix=4 if i in fix else 5,assessment=n,needsChange=i in fix) for i,n in zip(old,notes)]
assert not (b/'ratings-before.json').exists();r.write(b/'ratings-before.json',dict(method='Original own10 frozen before reveal; exact source/key, all choices, source pixels and host before inspected.',ratings=ratings));r.write(b/'ratings-frozen.json',dict(frozenAt=r.now(),ratingsSha256=r.sha(b/'ratings-before.json'),total=46,count=10,beforeChanges=True))
hist={x['id']:x for x in r.read(r.PREP/'previously-scored295.json')['questions']}
r.write(b/'related295-assessment-before.json',[dict(id=i,historicalScorePreserved=hist[i]['scoreBeforeFix'],currentBeforeScore=5,assessment='원문전체조건과직접계산/5선지/공식키일치. 리조트최소349000모든객실조합검산; 기존밑줄마침표는원문에포함되어유지.' if q['number']==32 else '전연도증가율/인정률/인력당신청분수검산;모든선지근거일치.',notReplacementOfHistoricalScore=True,changed=False) for i,q in related.items()])
prefix='<정 보>\n\n○ 상의 종류는 개근상, 우등상, 봉사상만 있다.\n\n○ 학생 1명은 동일한 종류의 상을 중복해서 받을 수 없다.\n\n○ 개근상, 우등상, 봉사상 3개를 모두 받은 학생은 1반, 2반, 5반에서 각각 2명이고, 3반, 4반, 6반에서 각각 1명이다.\n\n○ 우등상을 받은 학생 수가 봉사상을 받은 학생 수보다 많다.'
proof={x['id']:x['sourceRanges'] for x in r.read(b/'underline-source-strokes.json')['checks']};changes=[];nativeProof=None
norm=lambda s:re.sub(r'\s','',s)
def clean(s):
 s=re.sub(r'(?<=\d)\s+(?=(?:백 명|천 건|건당|건|명|년|배|으로|이다|이하|을|은|의|보다|이(?:\s|[.,])|가(?:\s|[.,])|로(?:\s|[.,])))','',s)
 return re.sub(r'−\s+(?=\d)','−',s)
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  i=q['id']
  if i not in fix:continue
  prev=old[i];assert q==prev;snap=r.OUT/f"before-changes/{i}-r{q['revision']}.json";assert not snap.exists();r.write(snap,prev)
  if i in proof:q['underlines']=proof[i]
  if q['number'] in [33,34]:
   for f in ['steps','optionReasons','pitfall','transfer']:
    q[f]=[clean(s) for s in q[f]] if isinstance(q[f],list) else clean(q[f])
    assert norm(''.join(q[f]))==norm(''.join(prev[f]))
  if q['number']==39:
   asset=q['figures'][0]['asset'];reg=next(v for v in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/native-image-repairs.json')['figures'] if v['newAsset']==asset)
   with pdfplumber.open(r.ROOT/reg['source']) as pdf:txt=pdf.pages[reg['page1based']-1].crop(reg['rect']).extract_text()
   assert norm(txt)==norm(prefix);q['bodyBeforeFigures']=prefix;q['figures']=q['figures'][1:]
   nativeProof=dict(id=i,source=reg['source'],page=reg['page1based'],rect=reg['rect'],oldImagePreserved=asset,nativeSourceCharactersEqual=True,sourceOrder='native information, table1, table2 with choice header')
  assert q['answer']==prev['answer'] and q['choices']==prev['choices'] and q['body']==prev['body']
  if q['number'] not in [33,34]:assert q['steps']==prev['steps'] and q['optionReasons']==prev['optionReasons']
  fields=sorted(k for k in q if q[k]!=prev.get(k));assert fields;q['revision']+=1;touched=True;changes.append(dict(id=i,file=p.relative_to(r.ROOT).as_posix(),oldRevision=prev['revision'],newRevision=q['revision'],changedFields=fields,beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason=next(x['assessment'] for x in ratings if x['id']==i),status='repaired_pending_reverification'))
 if touched:r.write(p,data)
assert len(changes)==4;r.write(r.OUT/'changes-batch54.json',changes)
r.write(b/'repair-semantic-checks.json',dict(status='PASS',targetChanged=4,relatedChanged=0,answersChoicesUnchanged=True,underlinesSource='underline-source-strokes.json',terminalDotsAndOriginalQuotesPreserved=True,nativeProse=nativeProof,numericValuesAndReasoningUnchanged=True))
r.write(b/'after-sample.json',dict(sample=[dict(id=i) for i in list(old)+list(related)]))
print('46/50 frozen;4target repairs;2related unchanged;source punctuation retained')
