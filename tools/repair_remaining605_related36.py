from fractions import Fraction as F
from itertools import product
import re,unicodedata
from PIL import Image
import pdfplumber
import review_remaining605 as r
b=r.folder(36);old={q['id']:q for q in r.read(b/'related295-before.json')};own={q['id']:q for q in r.read(b/'related295-own-solves.json')}
assert 'All tests passed!' in (b/'related295-host-before.log').read_text(encoding='utf-8-sig') and r.read(b/'related295-source-native-pixel-checks.json')['status']=='PASS'
assert r.sha(b/'related295-own-solves.json')==r.read(b/'related295-solve-frozen.json')['sha256']
ageCounts=[5,4,5,35,37,14,1];assert sum(ageCounts)==101
female=[5,4,5,31,0,0,0];male=[n-f for n,f in zip(ageCounts,female)]
femaleAge=sum(n*a for n,a in zip(female,range(20,81,10)))
assert sum(female)==45 and sum(male)==56 and femaleAge==1970<45*45
assert F(6,101)>F('.05') and 53-45==8 and sum(ageCounts[:4])==49<sum(ageCounts[4:])==52
# Every nonempty allocation of seven guests into exactly two legal rooms.
rates=[91000,168000,360000];base=[2,5,4];capacity=[4,8,4]
alloc=[]
for a,c in product(range(3),repeat=2):
 for n in range(1,7):
  m=7-n
  if n<=capacity[a] and m<=capacity[c]:alloc.append(dict(roomTypes=[a,c],guests=[n,m],cost=rates[a]+rates[c]+15000*(max(0,n-base[a])+max(0,m-base[c]))))
assert min(x['cost'] for x in alloc)==227000 and max(x['cost'] for x in alloc)==720000
assert 720000-227000==493000>=470000 and 91000<80000+15000 and 91000*2+30000>180000+15000
assert 116000+15000+15000==146000 and 2*120000+4*(15000+17000)==368000>168000+3*15000+8*17000==349000 and 70000+2*8000==86000
hist={q['id']:q for q in r.read(r.PREP/'previously-scored295.json')['questions']}
assess=[dict(id=i,historicalScorePreserved=hist[i]['scoreBeforeFix'],currentBeforeScore=4,historicalEvidence=hist[i]['evidence'],assessment='원문·공식키·새풀이 일치. '+('여성 평균의 가능한 반례·국적 교집합 하한이 정확하다. 작은 보기와 판정형 이유를 보완한다.' if q['number']==20 else '합법적인 객실별 인원 배정과 초과요금,최대최소 또는 반례가 정확하다. 작은 원문 보기/대화를 네이티브로 전환하고 공통 도입문 및 개별 근거를 보완한다.'),notReplacementOfHistoricalScore=True) for i,q in old.items()]
assert not (b/'related295-assessment-before.json').exists();r.write(b/'related295-assessment-before.json',assess)
norm=lambda s:re.sub(r'\s','',unicodedata.normalize('NFKC',s))
reg={x['newAsset']:x for x in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/native-image-repairs.json')['figures']}
intro='다음은 A리조트의 객실 요금 및 관광 상품 가격에 관한 자료이다. 다음 물음에 답하시오.'
underlines=['㉠회원 3명은 금요일에 146,000원으로 ‘단풍 유람선’ 패키지 상품을 이용할 수 있습니다.','㉡가장 저렴한 방법은 ‘나루 유람선’ 패키지 상품을 이용하는 것이고 비용은 368,000원입니다.','㉢회원 2명이 일요일에 ‘소담’ 객실에서 1박하고 ‘동굴’ 관광 상품을 이용한다면, 86,000원에 이용할 수 있습니다.']
checks=[];changes=r.read(r.OUT/'changes-batch36.json')
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  if q['id'] not in old:continue
  prev=old[q['id']];assert q==prev;n=q['number'];snap=r.OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();r.write(snap,prev)
  rec=reg[q['figures'][-1]['asset']]
  with pdfplumber.open(r.ROOT/rec['source']) as pdf:
   page=pdf.pages[rec['page1based']-1];raw=page.crop(rec['rect']).extract_text()
   if n==32:
    # Original underline strokes extend through each sentence's final period.
    endpoints=[(666.00,487.68),(633.99,562.50),(587.34,712.15)]
    for end,y in endpoints:
     line=next(z for z in page.lines if abs(z['x1']-end)<.02 and abs(z['top']-y)<.02)
     dot=next(c for c in page.chars if c['text']=='.' and c['x0']>page.width/2 and 0<line['top']-c['bottom']<2 and abs(line['x1']-c['x1'])<.1)
  body=re.sub(r'\s+',' ',raw).strip().replace('<보 기>','<보기>').replace('<대 화>','<대화>')
  if n in [20,31]:
   body=body.replace('<보기> ','<보기>\n\n');body=re.sub(r' (?=[ㄱㄴㄷㄹ]\. )','\n\n',body)
   body=re.sub(r'(?<=\d) (?=%)','',body)
  else:
   body=body.replace('<대화> ','<대화>\n\n');body=re.sub(r' (?=(?:직원|고객):)','\n\n',body)
  assert norm(raw)==norm(body),(n,raw,body)
  q['body']=body;q['figures']=q['figures'][:-1]
  if n in [31,32]:
   src=next(x['sourceText'] for x in r.read(b/'related295-source.json') if x['id']==q['id']);assert norm(intro) in norm(src)
   q['prompt']=intro+'\n\n'+q['prompt']
  if n==32:
   # Keep the source illustration as an image; only its text moves to native prose.
   imageSource=r.ROOT/prev['figures'][-1]['asset'];source=Image.open(imageSource)
   box=[60,84,1340,764] # original PDF rect [387,130,707,300], at4px/point
   crop=source.crop(box);asset='assets/psat/figures/2026grade5-d32-dialogue-illustration.png';dest=r.ROOT/asset;assert not dest.exists();crop.save(dest)
   q['figures'].append(dict(asset=asset,caption='상담 직원과 고객',width=crop.width,height=crop.height))
   q['underlines']=underlines;q['underlineLabelAnchors']=True
   for s in underlines:assert s in body,(s,body)
   r.write(b/'related295-illustration-crop.json',dict(source=prev['figures'][-1]['asset'],sourceSha256=r.sha(imageSource),sourcePixelBox=box,asset=asset,sha256=r.sha(dest),officialSource=rec['source'],sourcePage=16,pdfRect=[387,130,707,300],sourcePixelsAlreadyFreshVerified=True))
  q['optionReasons']=own[q['id']]['optionReasons']
  fields=sorted(k for k in q.keys()|prev.keys() if q.get(k)!=prev.get(k));q['revision']+=1;touched=True
  assert q['answer']==own[q['id']]['answer']==prev['answer'] and q['choices']==prev['choices']
  changes.append(dict(id=q['id'],file=p.relative_to(r.ROOT).as_posix(),oldRevision=prev['revision'],newRevision=q['revision'],changedFields=fields,beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason='Original prose readability, shared introduction and concrete all-option grounds; source illustration and underline endpoints preserved.',cohort='prior295',status='repaired_pending_reverification'))
  checks.append(dict(id=q['id'],exactNativeProse=True,answersAndChoicesUnchanged=True,sourceImagesRetained=True,sourceUnderlineEndpointsVerified=n==32))
 if touched:r.write(p,data)
assert len(changes)==12;r.write(r.OUT/'changes-batch36.json',changes)
r.write(b/'related295-repair-model-checks.json',dict(status='PASS',checks=checks,femaleAgeCounterexample=dict(female=female,male=male,ageSum=femaleAge,mean=str(F(femaleAge,45))),roomAllocations=alloc,minimum=227000,maximum=720000,packageCounterexample349000=True,sourceUnderlinePeriodsIncluded=True,historicalScoresAndSolvesPreserved=True))
print('3 prior295 repaired; source/models/underline endpoints PASS')
