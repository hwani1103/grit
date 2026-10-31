import re,unicodedata,pdfplumber
import review_remaining605 as r
b=r.folder(51);old={x['question']['id']:x['question'] for x in r.read(b/'revealed-current.json')};related={q['id']:q for q in r.read(b/'related295-before.json')}
for n in ['source-key-checks.json','related295-source-key-checks.json','exact-model-checks.json']:assert r.read(b/n)['status']=='PASS'
for n in ['host-before.log','related295-host-before.log']:assert 'All tests passed!' in (b/n).read_text(encoding='utf-8-sig')
notes={16:'전체12개 가중합/변화량 및수정상용76/78/90 모두 정확. 정보/보기 네이티브, 발견없음.',17:'부분비중과 전체18.3%감소, 전방법감소율순서와 겹치지 않는 근사범위 정확. 발견없음.',19:'공통분모 차와B재원반올림 범위4230.232~4231.24, 정답안정성 정확. 발견없음.',21:'2022단가 역산과수입중량/금액최저/15% 재대입 및톤×원/kg단위 정확. 발견없음.',22:'고저위험배수/혼자함께14.1%p/성별6.5>5.7의 다중조건 정확. 공통보고서네이티브 확인, 발견없음.',25:'두비율 순위/10%경계/7개전체검산 및5710 정확. 해설의 숫자·단위·조사 공백을 연결하고 수상작품수의 단위를 명료화.',27:'지도5개국15개범주 및가중점수12/12/13/14/6 정확. 해설숫자·단위공백연결.',29:'5개연도사과/두계열면적 및배/포도와복숭아/배교체 정확. 해설숫자·단위·조사공백연결.',30:'표밖최대1.9/잔여20.05로최소11개/제작사반례와점유율÷시간 정확. 해설숫자·단위공백연결.',31:'계좌차와인구분모/역산반올림상하한/가입자상승6.87% 정확. 해설숫자·단위·조사공백연결.'}
fix={25,27,29,30,31};ratings=[dict(id=i,scoreBeforeFix=4 if q['number'] in fix else 5,assessment=notes[q['number']],needsChange=q['number'] in fix) for i,q in old.items()]
assert not (b/'ratings-before.json').exists();r.write(b/'ratings-before.json',dict(method='Original-only solves frozen before reveal; full-series graph/calculation models, native source and fresh pixel checks; before host inspected.',ratings=ratings));r.write(b/'ratings-frozen.json',dict(frozenAt=r.now(),ratingsSha256=r.sha(b/'ratings-before.json'),total=45,count=10,beforeChanges=True))
hist={x['id']:x for x in r.read(r.PREP/'previously-scored295.json')['questions']}
r.write(b/'related295-assessment-before.json',[dict(id=i,historicalScorePreserved=hist[i]['scoreBeforeFix'],currentBeforeScore=4,assessment='보고서의 자녀연령/소득분류와29.1%p격차 정확. 작은 보고서이미지를 공통22와같은 네이티브본문으로 전환.' if q['number']==23 else '3개 옳은그래프 전체값/ㄹ여러증가율오류/기준연도와부호 정확. 해설 숫자·조사/음수기호공백 정리.',notReplacementOfHistoricalScore=True,changed=True) for i,q in related.items()])
def clean(s):
 s=re.sub(r'(?<=\d)\s+(?=(?:만 원|만 명|달러|천 톤|천 개|천 명|년|점|개|위|인당|대 과일|분의|으로|이다|을|은|의|보다|이(?:\s|[.,])|인(?:\s|[.,])|로(?:\s|[.,])))','',s)
 return re.sub(r'−\s+(?=\d)','−',s)
norm=lambda s:re.sub(r'\s','',unicodedata.normalize('NFKC',s))
changes=[];reportProof=None
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  ir=q['id'] in related
  if not(ir or (q['id'] in old and q['number'] in fix)):continue
  prev=(related if ir else old)[q['id']];assert q==prev;n=q['number'];snap=r.OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();r.write(snap,prev)
  if ir and n==23:
   asset=q['figures'][2]['asset'];rec=next(x for x in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/native-image-repairs.json')['figures'] if x['newAsset']==asset)
   with pdfplumber.open(r.ROOT/rec['source']) as pdf:sourceReport=pdf.pages[rec['page1based']-1].crop(rec['rect']).extract_text()
   body=old['kr-mpm-2024-03-02-psat-d-22']['body'];assert norm(sourceReport)==norm(body)
   q['body']=body;q['figures']=[f for j,f in enumerate(q['figures']) if j!=2];q['bodyAfterFigureCount']=2
   reportProof=dict(id=q['id'],removedFigureRetainedOnDisk=asset,source=rec['source'],page=rec['page1based'],rect=rec['rect'],sourceCharactersMatch=True,shared22BodyExactlyEqual=True)
   reason='원표2개→네이티브공통보고서→4개추가자료의 원래 읽기순서 유지.'
  else:
   for f in ['steps','optionReasons','pitfall','transfer']:
    q[f]=[clean(s) for s in q[f]] if isinstance(q[f],list) else clean(q[f])
   if n==25:
    q['steps'][3]=q['steps'][3].replace('수상 10인','수상작 10개인').replace('수상 14인','수상작 14개인')
   reason='숫자·단위/조사와 음수기호의 불필요한 공백 정리; 모든 수치와 의미 보존.'
   for f in ['steps','optionReasons','pitfall','transfer']:
    a=''.join(q[f]) if isinstance(q[f],list) else q[f];e=''.join(prev[f]) if isinstance(prev[f],list) else prev[f]
    if n==25 and f=='steps':a=a.replace('수상작 10개인','수상 10인').replace('수상작 14개인','수상 14인')
    assert norm(a)==norm(e),(q['id'],f)
  assert q!=prev and q['answer']==prev['answer'] and q['choices']==prev['choices'];fields=sorted(k for k in q if q[k]!=prev.get(k));q['revision']+=1;touched=True
  changes.append(dict(id=q['id'],file=p.relative_to(r.ROOT).as_posix(),oldRevision=prev['revision'],newRevision=q['revision'],changedFields=fields,beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason=reason,status='repaired_pending_reverification'))
 if touched:r.write(p,data)
assert len(changes)==7;r.write(r.OUT/'changes-batch51.json',changes)
r.write(b/'repair-semantic-checks.json',dict(status='PASS',targetChanged=5,relatedChanged=2,report=reportProof,allAnswersChoicesUnchanged=True,allNumericalReasoningUnchanged=True,clarifiedUnit='25수상10/14 -> 수상작10개/14개; no numerical change',otherExplanationChangesWhitespaceOnly=True))
r.write(b/'after-sample.json',dict(sample=[dict(id=i) for i in list(old)+list(related)]))
print('Frozen45/50;5target+2related repairs; report matches source and shared22 exactly')
