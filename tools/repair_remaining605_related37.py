import re
from fractions import Fraction as F
import pdfplumber
import review_remaining605 as r
b=r.folder(37);old={q['id']:q for q in r.read(b/'related295-before.json')};src={x['id']:x for x in r.read(b/'related295-source.json')};own={x['id']:x for x in r.read(b/'related295-own-solves.json')}
assert 'All tests passed!' in (b/'related295-host-before.log').read_text(encoding='utf-8-sig')
ledger={x['id']:x for x in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/current900-evidence-ledger.json')['questions']}
norm=lambda s:re.sub(r'[\s①②③④⑤]','',s)
checks=[]
for i,q in old.items():
 m=src[i];s=re.sub(r'책형\s*\d+쪽','',m['sourceText']);s=re.sub(r'^\s*\d+[.]\s*','',s);assert norm(s)==norm(q['prompt']+q['body']+''.join(q['choices']))
 with pdfplumber.open(r.ROOT/ledger[i]['officialKey']) as pdf:pi,t=next((j+1,p.extract_text()) for j,p in enumerate(pdf.pages) if '영역 언어논리' in (p.extract_text() or ''))
 assert '2026' in t and '책형 나' in t.replace('㉯','나');answers={}
 for line in t.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):z=list(map(int,line.split()));answers.update(zip(z[::2],z[1::2]))
 assert answers[q['number']]==q['answer']==own[i]['answer'];checks.append(dict(id=i,source=m['source'],page=m['page'],directKey=ledger[i]['officialKey'],keyPage=pi,sourceAndAllFiveChoicesMatch=True,ownAnswerMatches=True))
# A finite countermodel separates mass divisibility from charge divisibility.
assert F(1)/F(2)==F(1,2) and F(2)/F(3)==F(2,3)
assert F(1)*1==F(2)*F(1,2) and F(2)*1==F(3)*F(2,3)
# Both masses are integer multiples of1; their chosen charges need not equal
# integer multiples of a prespecified unit2 (q=3 is a counterexample).
assert 3%2!=0 and [2,3,4]==[n*1 for n in [2,3,4]] and 1 not in [2,3,4]
assert min(b-a for a,b in zip([2,4,6],[4,6,8]))==2
hist={q['id']:q for q in r.read(r.PREP/'previously-scored295.json')['questions']}
assess=[dict(id=i,historicalScorePreserved=hist[i]['scoreBeforeFix'],currentBeforeScore=4,historicalEvidence=hist[i]['evidence'],assessment='원문·공식키·새풀이 일치. '+('무처치집단의 부분회복을 정확히 설명하며 모든환경 일반화를 금한다. 본문2 %·7 % 어절을 개선한다.' if q['number']==18 else '같은질량 통제와 단위전하관측부재의 반례가 정확하다. 마지막선지의 이유를 구체화하고 표본최소차이를 기본단위와 같다고 볼 조건을 설명한다.'),notReplacementOfHistoricalScore=True) for i,q in old.items()]
assert not (b/'related295-assessment-before.json').exists();r.write(b/'related295-assessment-before.json',assess)
changes=r.read(r.OUT/'changes-batch37.json')
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  if q['id'] not in old:continue
  prev=old[q['id']];assert q==prev;snap=r.OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();r.write(snap,prev)
  if q['number']==18:q['body']=q['body'].replace('2 %','2%').replace('7 %','7%')
  else:
   q['optionReasons'][4]='같은 질량에서 E의 연속 분포는 q=mg/E도 연속이 되게 하므로 ㄱ만 적절하다. ㄴ은 E가 통제되지 않은 질량만으로 전하를 판단했고, ㄷ은 2e·3e·4e만 관측되어도 기본 단위 e와 양립한다는 반례를 놓쳤다.'
   q['steps'][4]+=' 표본 전하량의 최소 차이를 기본 단위 e로 읽으려면 전자 수가 1만큼 다른 방울 쌍 등이 관측되어야 한다. 예를 들어 2e·4e·6e만 측정하면 최소 차이는 2e다. 기본 단위의 존재와 특정 단위를 가진 방울의 관측을 구별한다.'
  fields=sorted(k for k in q if q[k]!=prev[k]);assert fields;q['revision']+=1;touched=True
  assert norm(q['body'])==norm(prev['body']) and q['choices']==prev['choices'] and q['answer']==prev['answer']
  changes.append(dict(id=q['id'],file=p.relative_to(r.ROOT).as_posix(),oldRevision=prev['revision'],newRevision=q['revision'],changedFields=fields,beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason='Source word boundary and explicit hypothesis/observation limits; all original words/options preserved.',cohort='prior295',status='repaired_pending_reverification'))
 if touched:r.write(p,data)
r.write(r.OUT/'changes-batch37.json',changes)
assert r.sha(b/'related295-own-solves.json')==r.read(b/'related295-solve-frozen.json')['sha256']
r.write(b/'related295-source-key-model-checks.json',dict(status='PASS',checks=checks,coral='Untreated group0→2%→7%; partial recovery and environment-acquisition explanation, not universal proof.',charge='q=mg/E; mass alone uncontrolled; no e observation compatible with2e3e4e; sample2e4e6e has minimum gap2e.',historicalScoresAndFrozenSolvesPreserved=True))
print('2 prior295 repaired; source/key/models PASS')
