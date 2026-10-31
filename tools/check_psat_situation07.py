from pathlib import Path
from fractions import Fraction as F
from itertools import product,permutations
import json,re,hashlib,pdfplumber
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/situation07';P=R/'assets/psat/situation07.json'
bank=json.loads((P if P.exists() else A/'authored-situation07.json').read_text(encoding='utf-8'));norm=lambda s:re.sub(r'[\s/]+','',s)
with pdfplumber.open(next((R/'artifacts/psat600_20261028/sources/5994').glob('*.pdf'))) as pdf:
 text=next(p.extract_text() for p in pdf.pages if '영역 상황판단' in p.extract_text());assert '2025년도' in text and '인 책형' in text
 key={}
 for line in text.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
   vs=list(map(int,line.split()));key.update(zip(vs[::2],vs[1::2]))
 assert len(key)==25
proof={'11':{'exceptionStillNotify':True,'consultation':'culturalheritageonly','trailApplicant':'stateorlocalgov','research':'allowedwithpermission'},'12':{'attendanceRequestedBy':'workerrepresentative','explanationRequest':'committeeORrepresentative','nightRestrictionBy':'employer','personalResults':'consentrequired','agencyEvaluation':'ministermaypublish'},'13':{'owner':'nocost','negligentInjury':'compensated','threatenedLand':'temporaryrestrictionsallowed','illegalparkingloss':'excluded','towCosts':'governormaypay'}}
# Enumerate all feasible daily factory allocations; fixed cost only when A used.
alloc={}
for q,fixed in [(120,100),(200,100),(200,50)]:
 rows=[(fixed*(a>0)+a+2*b,a,b) for a in range(151) for b in range(151) if a+b==q]
 low=min(x[0] for x in rows);opt=[x for x in rows if x[0]==low];alloc[f'{q}/{fixed}']=opt
assert alloc=={'120/100':[(220,120,0)],'200/100':[(350,150,50)],'200/50':[(300,150,50)]}
proof['14']=alloc
# Set countermodels: individual rates all +2pp with triple overlap unchanged.
base=[set(range(35)) for _ in range(3)];after=[s|set(range(35+2*i,37+2*i)) for i,s in enumerate(base)]
assert [len(x) for x in after]==[37]*3 and len(set.intersection(*after))==35
old=[{1,2},{1,3},{1,4}];new=[{1,2}]*3
assert [len(x) for x in old]==[len(x) for x in new] and len(set.intersection(*old))==1 and len(set.intersection(*new))==2
# Distinct populations, counterexample to unweighted average.
pops=[100,200,300,400,500];rates=[35,30,25,30,30];weighted=sum(F(n*r,100) for n,r in zip(pops,rates))/sum(pops)*100;assert weighted!=30
proof['15']={'tripleUnchanged':[35,35],'individualRates':[35,37],'fixedMarginsOverlap':[1,2],'weightedExample':str(weighted),'twoWayOrderCounterexample':{'B':30,'C':50}}
# Exhaustive legal score allocations, including >150 totals and all three accelerated choices.
fees=[]
for fast in range(3):
 rate=[5000,3000,10000];rate[fast]=[10000,7000,13000][fast]
 best=10**9;witness=[]
 for scores in product(range(40,101),repeat=3):
  if sum(scores)<150:continue
  cost=sum(a*b for a,b in zip(scores,rate))
  if cost<best:best=cost;witness=[scores]
  elif cost==best:witness.append(scores)
 fees.append({'fast':'ABC'[fast],'minimum':best,'scores':witness})
assert [f['minimum'] for f in fees]==[1010000,1030000,930000]
assert fees[2]['scores']==[(40,70,40)]
assert 40*(5000+3000+10000)+40*3000+30*3000==930000
proof['16']=fees
# Roles are keyed to actual grade; rank 3 is higher than rank 4.
roles={'A':[(3,'국장'),(4,'과장'),(5,'팀장')],'B':[(4,'국장'),(5,'과장')],'C':[(5,'국장')]};assign=[]
for offices in permutations('ABC'):
 if offices[0]=='C' or offices[2]=='A':continue
 for rs in product(*(roles[o] for o in offices)):
  if rs[0][0]==rs[1][0] and rs[2][0]<min(g for g,_ in roles[offices[1]]):assign.append(list(zip(offices,rs)))
assert assign==[[('A',(5,'팀장')),('C',(5,'국장')),('B',(4,'국장'))]];proof['17']=assign
apart=[('A',16,True,False,F('2.5'),True,'대한동'),('B',17,True,True,F('2.3'),False,'대한동'),('C',15,True,False,F('2.0'),False,'민국동'),('D',13,False,False,F('2.0'),True,'대한동'),('E',8,True,False,F('2.3'),False,'민국동')]
elig=[name for name,floor,july,debt,price,closet,area in apart if floor>=10 and july and not debt and price<=F('2.5' if closet else '2.3')];assert elig==['A','C'];proof['18']={'eligible':elig,'preferred':'A','tableNoteFloor806':8}
rent=[('甲',50,70,True,45,25),('乙',45,60,False,30,35),('丙',100,90,False,45,20),('丁',40,50,False,40,20),('戊',70,100,False,35,25)]
pay={n:min(cost,cap) if not own and (dist>=50 or mins>=60) else 0 for n,dist,mins,own,cost,cap in rent};assert list(pay.values())==[0,30,20,0,25] and sum(pay.values())==75;proof['19']=pay
company=[('A',1700,5,7,2021,False),('B',480,10,4,2017,False),('C',6250,6,2,2022,True),('D',3000,7,5,2023,False),('E',5000,3,3,2010,False)];scores={};selected=[]
for name,sales,complaints,bad,year,recent in company:
 val=(1 if sales<500 else 3 if sales<5000 else 5)+F(complaints,2)+F(3*bad,10)-(year>=2021)
 scores[name]=str(val)
 if val>7 and not recent:selected.append(name)
assert scores=={'A':'33/5','B':'36/5','C':'38/5','D':'7','E':'37/5'} and selected==['B','E'];proof['20']={'exactScores':scores,'selected':selected,'yearBoundary':'no2020cases;allselectedyearsunambiguous'}
# Compare table cells directly to PDF geometry extraction, not to another authored copy.
with pdfplumber.open(next((R/'artifacts/psat600_20261028/sources/6008/pdf').glob('*상황판단*'))) as pdf:
 for q in bank:
  n=q['number'];raw=(A/f'2025-s{n}-source.txt').read_text(encoding='utf-8').split(f'{n}.',1)[1];prompt,tail=raw.split('?',1);body,opts=tail.rsplit('\n① ',1)
  if n==15:body=body.split('\n지역 A B C D E',1)[0]
  if n==16:body=body.split('\n취득점수 1점당 수강료(원)',1)[0]
  if n==17:body=body.rsplit('\n甲 丙',1)[0];assert '甲의 근무처·직위 → 丙의 근무처·직위' in q['choiceNote']
  if n==18:
   before,rest=body.split('\n입주 가능 전세 보증금 담보',1);body=before+'\n※ '+rest.split('※ ',1)[1];assert q['tables'][0]['afterParagraph']==5
  if n==19:
   before,rest=body.split('\n지급기준 지원 한도액',1);middle=rest.split('<상 황>',1)[1].split('\n거주지와 근무지 간 주택 소유',1)[0];body=before+'\n<상 황>'+middle;assert [t['afterParagraph'] for t in q['tables']]==[2,3]
  if n==20:body=body.split('\n전년도 최근 1년간 전년도 성실 납세 최근 1년 내',1)[0]
  assert norm(q['prompt'])==norm(prompt+'?'),(n,'prompt')
  assert norm(q['body'])==norm(body),(n,'body')
  options=re.split('[①②③④⑤]','① '+opts)[1:];assert len(options)==5 and all(norm(a)==norm(b) for a,b in zip(options,q['choices'])),(n,'options')
  if q['tables']:
   side=(n-1)%2;c=pdf.pages[(n-1)//2].crop((364*side,43,364*(side+1),1016));tabs=c.extract_tables();assert len(tabs)==len(q['tables'])
   for src,dst in zip(tabs,q['tables']):
    if n==16:
     assert norm(src[0][1])==norm(dst['caption']);src=[[src[0][0],*src[1][1:]],*src[2:]]
    assert [[norm(c) for c in row] for row in src]==[[norm(c) for c in row] for row in [dst['columns'],*dst['rows']]],(n,'table')
  assert q['answer']==key[n] and len(q['steps'])==len(q['optionReasons'])==5
  for st,prefix in zip(q['steps'],['착안점: ','실전 풀이: ','답 확정 기준: ','정석 근거: ','적용 한계: ']):assert st.startswith(prefix) and len(st)>40
  assert not any(c in json.dumps(q,ensure_ascii=False) for c in ['\u2060','\ufffd'])
  assert (R/q['original'] if P.exists() else A/'staged'/q['original']).exists()
seen=set();old=0
for p in (R/'assets/psat').glob('*.json'):
 if p.name in ['sets.json','situation07.json']:continue
 obj=json.loads(p.read_text(encoding='utf-8'))
 if isinstance(obj,list):
  for q in obj:
   k=(q.get('examDate',q['source'][:10].replace('.','-')),q['subject'],q['number']);assert k not in seen;seen.add(k);old+=1
for q in bank:
 k=(q['examDate'],q['subject'],q['number']);assert k not in seen;seen.add(k)
for path,digest in json.loads((A/'before-situation07-hashes.json').read_text(encoding='utf-8')).items():
 if path!='assets/psat/sets.json':assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
proof.update(status='PASS',count=10,officialFinalKeys=10,source='complete text,5choices,6tables PDF cell comparison',preservedExisting=old,limitations='Same-author review, not independent expert certification.')
(A/'content-checks.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PASS10,6PDFtables,allcostallocations,sets/counterexamples,grades,rent,tax;preserved',old)