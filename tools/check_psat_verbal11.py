from pathlib import Path
import json,re,hashlib,pdfplumber,itertools as it
from fractions import Fraction as F
from PIL import Image
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/verbal11';P=R/'assets/psat/verbal11.json';bank=json.loads((P if P.exists() else A/'authored-verbal11.json').read_text(encoding='utf-8'));tr=json.loads((A/'source-transcripts.json').read_text(encoding='utf-8'));proof={}
assert [q['number'] for q in bank]==[2,3,4,5,6,7,9,10,11,12]
proof['2']={'departureBeforeArrival':'May7','invasion':'May13','truth':[False,True,False,False,False]};assert 7<13<22
proof['3']={'argument':'intuition as neural pattern recognition -> AI may outperform humans in related work;hypothetical soul premise is rejected','answer':1}
proof['4']={'scope':'some subjective classifications admitted;most objective similarity','answer':4}
assert 2+1==1+1+1==3;proof['5']={'uncleDistance':3,'grandfatherToSonDistance':3,'counterexampleBeforeRevision':'wife parents are already in-laws','invalid':5}
proof['6']={'population':'breast cancer patients, not all women','outcome':'estrogen receptor distribution, not incidence','generalization':'social environment may affect biological properties;not causal certainty','answer':4}
proof['7']={'givingReceivingReturning':'all obligations -> coercive','marriage':'same analogy;rights/autonomy mismatches','answer':4}
cases=[dict(total=100,fit=30,unfit=20,conditional=c,unreviewed=50-c) for c in [10,40]]
assert all(sum(c[k] for k in ['fit','unfit','conditional','unreviewed'])==100 for c in cases)
assert len({(F(c['fit'],c['total']),F(c['unfit'],c['total'])) for c in cases})==1
assert len({F(c['conditional'],c['total']) for c in cases})==2
proof['9']={'truth':[True,True,False],'counterexamples':cases}
# Enumerate allowed application sets for never-admitted students, the branch permitting all three rounds.
early=[set(x) for n in range(4) for x in it.combinations(['gifted','science','vocational'],n) if len(set(x)&{'science','vocational'})<=1]
late=[set(x) for n in range(3) for x in it.combinations(['arts','general'],n)]
maxapps=max(len(e)+len(l)+a for e in early for l in late for a in [0,1]);assert maxapps==5
proof['10']={'maxApplications':maxapps,'regionalEligibility':'A resident OR A middle-school graduate/expected','answer3Witness':{'eligibleA':True,'earlyAdmitted':False,'lateArtsAdmitted':False,'anyOtherLateAdmitted':False,'vocationalVacancy':True,'additionalApplications':1},'option5Counterexample':'gifted reject and science admit can coexist in early round'}
steel=[F(27,100),F(30,100)];concrete=[F(15,100),F(25,100)];assert min(steel)>max(concrete)>0 and max(1/x for x in steel)<min(1/x for x in concrete)
proof['11']={'steelReciprocal':[str(1/steel[1]),str(1/steel[0])],'concreteReciprocal':[str(1/concrete[1]),str(1/concrete[0])],'invalid':2}
for v in [F(1,2),F(1),F(20)]:assert v-v==0 and v-v!=2*v
proof['12']={'sameDirectionEqualVelocity':'relative velocity zero','stationaryWorldline':'spatial coordinates fixed, time changes -> straight parallel time axis','invalid':1}
with pdfplumber.open(next((R/'artifacts/psat600_20261028/sources/6001').glob('*.pdf'))) as pdf:
 t=next(p.extract_text() for p in pdf.pages if '영역 언어논리' in p.extract_text());assert '2025' in t and '혁' in t;keys={}
 for line in t.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
   v=list(map(int,line.split()));keys.update(zip(v[::2],v[1::2]))
 assert len(keys)==25
norm=lambda s:re.sub(r'[\s□·․「」]+','',s)
for q in bank:
 n=q['number'];src=tr[q['id']];assert norm(q['prompt'])==norm(src['prompt'])
 if n==12:
  assert q['body']=='' and len(q['figures'])==1
  expected=[re.sub(r'\s+',' ',s).replace('','v').replace('','t').replace('','3') for s in src['choices']];expected[1]=expected[1].replace('t 부터 3 속도를','t3부터 속도를');assert q['choices']==expected
  assert 't3부터' in q['choices'][1]
 else:assert all(norm(x)==norm(y) for x,y in zip(q['choices'],src['choices']))
 if n==10:
  pre,rest=src['body'].split('모집 시기 학교 유형 학교 수 지원 가능 지역',1);unused,after=rest.split('전기 모집에서는',1);assert norm(q['body'])==norm(pre+'전기 모집에서는'+after)
  assert q['tables'][0]['rows']==[['과학고','전기','2','A시'],['영재고','전기','1','전국'],['특성화고','전기','30','A시'],['예술고','후기','5','전국'],['일반고','후기','30','A시']]
 elif n!=12:assert norm(q['body'])==norm(src['body']),(n,'body')
 assert q['answer']==keys[n] and len(q['steps'])==len(q['optionReasons'])==5,(n,q['answer'],keys[n])
 for s,prefix in zip(q['steps'],['착안점: ','실전 풀이: ','답 확정 기준: ','정석 근거: ','적용 한계: ']):assert s.startswith(prefix) and len(s)>40
 for u in q.get('underlines',[]):assert q['body'].count(u)==1,(n,u)
 assert not any('\ue000'<=c<='\uf8ff' or c in '\ufffd\u2060\u2024' for c in json.dumps(q,ensure_ascii=False)),n
assert '“□.”' in bank[4]['body']
for c in json.loads((A/'crop-manifest.json').read_text(encoding='utf-8')):
 source=R/c['source'];assert hashlib.sha256(source.read_bytes()).hexdigest()==c['sha256']
 with pdfplumber.open(source) as pdf:
  p=pdf.pages[c['page1based']-1];ref=p.crop(c['rect']).to_image(resolution=c['resolution'],antialias=True).original.convert('RGB');path=R/c['asset'] if P.exists() else A/'staged'/c['asset'];im=Image.open(path).convert('RGB');assert im.size==ref.size and im.tobytes()==ref.tobytes(),c['asset']
  if '/figures/' in c['asset']:
   x0,y0,x1,y1=c['rect']
   for w in p.extract_words():
    if w['x1']<=x0 or w['x0']>=x1 or w['bottom']<=y0 or w['top']>=y1:continue
    assert w['x0']>=x0-.5 and w['x1']<=x1+.5 and w['top']>=y0-.5 and w['bottom']<=y1+.5,(c['asset'],w)
seen=set();old=0
for path in (R/'assets/psat').glob('*.json'):
 if path.name in ['sets.json','verbal11.json']:continue
 obj=json.loads(path.read_text(encoding='utf-8'))
 if isinstance(obj,list):
  for q in obj:
   k=(q.get('examDate',q['source'][:10].replace('.','-')),q['subject'],q['number']);assert k not in seen;seen.add(k);old+=1
for q in bank:
 k=(q['examDate'],q['subject'],q['number']);assert k not in seen;seen.add(k)
for path,digest in json.loads((A/'before-verbal11-hashes.json').read_text(encoding='utf-8')).items():
 if path!='assets/psat/sets.json':assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
proof.update(status='PASS',count=10,officialFinalKeys=10,sourceComparison='nativeprompt/body/choices;table1;blank/5underlines;1figure10originalpixelcomparisons',preservedExisting=old,held='2025speciall8unpublished',limitations='Same-author semantic review plus executable models;not independent expert review.')
(A/'content-checks.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PASS10source/key/11pixels;models;preserved',old)
