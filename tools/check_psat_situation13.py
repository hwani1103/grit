from pathlib import Path
import json,re,hashlib,itertools as it,pdfplumber
from PIL import Image
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/situation13';P=R/'assets/psat/situation13.json'
bank=json.loads((P if P.exists() else A/'authored-situation13.json').read_text(encoding='utf-8'));tr=json.loads((A/'source-transcripts.json').read_text(encoding='utf-8'))
assert [(q['examDate'],q['number']) for q in bank]==[('2025-11-15',n) for n in [21,22,23,24,25]]+[('2026-07-18',n) for n in [1,2,3,4,6]]

from fractions import Fraction as F
proof={}
new=[5,8]
for _ in range(4):new.append(sum(new[-2:]))
cancel=[0]+[2**n for n in range(1,6)]
net=[a-b for a,b in zip(new,cancel)];stock=[];v=0
for x in net:v+=x;stock.append(v)
assert new==[5,8,13,21,34,55] and sum(new)==136 and sum(cancel)==62 and stock==[5,11,20,33,51,74]
proof['special21']={'new':new,'cancelled':cancel,'stock':stock,'answer':74}
plans=[]
for p in range(16):
 for e in range(31):
  for m in range(16):
   if 2*p+e+2*m<=30 and e<=10*m:plans.append((80*p+50*e,p,e,m))
best=max(x[0] for x in plans);winner=[x for x in plans if x[0]==best]
assert winner==[(1240,3,20,2)] and sum(winner[0][1:])==25
assert [max(x[0] for x in plans if x[3]==m) for m in range(4)]==[1200,1220,1240,1200]
proof['special22']={'enumeratedFeasible':len(plans),'winnerScorePublicExpertManager':winner,'headcount':25,'manager0to3Max':[1200,1220,1240,1200],'manager3plusUpperBound':1200}
d=F(16,5);e=F(17,6);assert 0<1<d and e<d
proof['special23']={'truth':[True,True,False],'reason':'positive-weight average lies strictly between distinct input averages','counterexample':{'firstFourTermMeans':[4,4,4,4],'coursesEachTerm':1,'b':0,'c':1,'d':str(d),'e':str(e)}}
ends=[(a,b) for a,b in it.permutations(range(1,6),2) if a<=2 and b<=2];assert ends==[(1,2),(2,1)]
moves=[(1,2,3,1),(2,3,1,3),(3,1,2,5),(4,2,1,4),(5,1,3,2)]
state=[2]*5;history=[state.copy()]
for actor,src,dst,k in moves:
 assert actor!=src and actor!=dst and src!=dst and state[src-1]>=k and 1<=k<=5
 state[src-1]-=k;state[dst-1]+=k;history.append(state.copy())
assert state==[2]*5 and {x[3] for x in moves}==set(range(1,6)) and moves[0][3]+moves[-1][3]==3
proof['special24']={'boundaryPairs':ends,'witnessActorSourceDestinationCount':moves,'states':history,'answer':3,'limit':'boundary proof plus feasible witness;not enumeration of all move histories'}
rows=[]
for k,n,s in it.product([False,True],repeat=3):
 result=(not k or n) and (k or n or s) and not s
 assert result==(n and not s)
 rows.append([k,n,s,result])
proof['special25']={'columns':['Korean','noodle','seafood','accepted'],'truthTable':rows,'minimalAttributes':['noodle','seafood']}
proof['regular1']={'correct':4,'rejected':[1,2,3,5],'reasons':['foreign applicants included','adjustment application to tax commissioner','8year total ceiling not13','known tax>3years excepted'],'priority':'final judgment date overrides ordinary/extended end'}
proof['regular2']={'correct':3,'termYearsAtLeast':10,'cycleYears':5,'changeAppliesParagraphs':[2,3],'distinguish':'14day access belongs to designation notification,not master plan'}
proof['regular3']={'correct':4,'chair':'deputy head','appointingAuthority':'local government head','schoolsIncluded':True,'integrationRequiresOrdinance':True}
proof['regular4']={'correct':3,'panelJudges':3,'appointedBy':'chief justice','questionRequires':'presiding judge permission','report':'written or oral','noDisclosureExceptionStated':True}
annual=15+(7-1)//2;carry=min(F(5),F(17)-F(19,2));remaining=annual+carry-F(9,2)
assert annual==18 and carry==5 and remaining==F(37,2)
proof['regular6']={'annual':annual,'carry':str(carry),'used':'9/2','remaining':str(remaining)}
keys={}
for post,date,year,book in [(6001,'2025-11-15','2025','혁'),(6016,'2026-07-18','2026','사')]:
 with pdfplumber.open(next((R/f'artifacts/psat600_20261028/sources/{post}').glob('*.pdf'))) as pdf:
  t=next(p.extract_text() for p in pdf.pages if '영역 상황판단' in p.extract_text());assert year in t and book in t;k={}
  for line in t.splitlines():
   if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
    v=list(map(int,line.split()));k.update(zip(v[::2],v[1::2]))
  assert len(k)==25;keys[date]=k
def norm(s):
 return re.sub(r'[\s·․]+','',s.replace('\uf000','『').replace('\uf001','』'))
for q in bank:
 n=q['number'];src=tr[q['id']]
 assert norm(q['prompt'])==norm(src['prompt']),(n,'prompt')
 assert len(q['choices'])==5 and all(norm(x)==norm(y) for x,y in zip(q['choices'],src['choices'])),(n,'choices')
 if q['examDate']=='2025-11-15' and n in [22,23]:
  if n==22:
   before,rest=src['body'].split('수행주체 보수 예상 단속 건수',1);table,after=rest.split('민간전문가를 활용',1);marker='민간전문가를 활용'
   assert norm(table)=='공무원200만원80건민간전문가100만원50건'
   assert q['tables'][0]['columns']==['수행주체','보수','예상 단속 건수'] and q['tables'][0]['rows']==[['공무원','200만 원','80건'],['민간전문가','100만 원','50건']]
  else:
   before,rest=src['body'].split('구분 2학년 2학기 3학년 1학기 3학년 2학기',1);table,after=rest.split('<보 기>',1);marker='<보기>'
   assert norm(table)=='학기평균평점abc누적평균평점4.0de'
   assert q['tables'][0]['columns']==['구분','2학년 2학기','3학년 1학기','3학년 2학기'] and q['tables'][0]['rows']==[['학기 평균 평점','a','b','c'],['누적 평균 평점','4.0','d','e']]
  assert norm(q['body'])==norm(before+marker+after),(n,'body')
 else:assert norm(q['body'])==norm(src['body']),(n,'body')
 assert q['answer']==keys[q['examDate']][n] and len(q['steps'])==len(q['optionReasons'])==5
 assert all(q['body'].count(u)==1 and '\n' not in u for u in q.get('underlines',[])),(n,'underline',q.get('underlines'))
 assert not any('\ue000'<=c<='\uf8ff' or c in '\ufffd\u2060\u2024' for c in json.dumps(q,ensure_ascii=False)),n
 assert not re.search(r'\d{4}\.\s*\n\s*\n\s*\d{1,2}\.',q['body'])
for c in json.loads((A/'crop-manifest.json').read_text(encoding='utf-8')):
 source=R/c['source'];assert hashlib.sha256(source.read_bytes()).hexdigest()==c['sha256']
 with pdfplumber.open(source) as pdf:
  ref=pdf.pages[c['page1based']-1].crop(c['rect']).to_image(resolution=c['resolution'],antialias=True).original.convert('RGB');path=R/c['asset'] if P.exists() else A/'staged'/c['asset'];im=Image.open(path).convert('RGB');assert im.size==ref.size and im.tobytes()==ref.tobytes(),c['asset']
seen=set();old=0
for path in (R/'assets/psat').glob('*.json'):
 if path.name in ['sets.json','situation13.json']:continue
 obj=json.loads(path.read_text(encoding='utf-8'))
 if isinstance(obj,list):
  for q in obj:
   k=(q.get('examDate',q['source'][:10].replace('.','-')),q['subject'],q['number']);assert k not in seen;seen.add(k);old+=1
for q in bank:
 k=(q['examDate'],q['subject'],q['number']);assert k not in seen;seen.add(k)
for path,digest in json.loads((A/'before-situation13-hashes.json').read_text(encoding='utf-8')).items():
 if path!='assets/psat/sets.json':assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
proof.update(status='PASS',count=10,officialFinalKeys=10,sourceComparison='native prompt/body/choices;table2/law headings/10originalpixels',preservedExisting=old,limitations='Same-author semantic review with budget enumeration,Boolean truth table,exact fractions and feasible move witness;not independent expert review.')
(A/'content-checks.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PASS10source/key/10pixels;models;preserved',old)
