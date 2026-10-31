from pathlib import Path
import json,re,hashlib,itertools as it,pdfplumber
from PIL import Image
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/situation17';P=R/'assets/psat/situation17.json'
bank=json.loads((P if P.exists() else A/'authored-situation17.json').read_text(encoding='utf-8'));tr=json.loads((A/'source-transcripts.json').read_text(encoding='utf-8'))
assert [(q['examDate'],q['number']) for q in bank]==[('2026-03-07',n) for n in [16,17,21,22,23,24,25,26,29,30]]
from fractions import Fraction as F
from datetime import date
proof={}
cars=[(160,'승용','휘발유'),(240,'승용','경유'),(250,'화물','경유'),(280,'승합','휘발유'),(300,'화물','휘발유')]
amounts=[v+(v//5 if k=='화물' else 0)+(30 if k=='승용' else 50) * (fuel=='경유') for v,k,fuel in cars]
assert amounts==[160,270,350,280,360];assert sorted(amounts,reverse=True)[2]==amounts[3]
proof['16']={'amounts':amounts,'fastBound':{'below280':[160,270],'above280LowerBounds':[300,300]},'noTies':True}
people=[2350,820,3600,1200,2100,980];budgets=[95,185,210,130,160,80];homes=[True,True,True,True,False,True]
top=lambda xs:set(sorted(range(6),key=lambda i:xs[i],reverse=True)[:3]);eligible=top(people)|top(budgets)
scores=[(40 if p>=2000 else 30 if p>=1000 else 20)+(40 if b>=200 else 20 if b>=100 else 10)+(20 if h else 0) for p,b,h in zip(people,budgets,homes)]
selected=[i for i in eligible if scores[i]>=70];assert sorted(selected)==[0,2] and scores==[70,60,100,70,60,50]
proof['17']={'eligible':sorted(eligible),'scores':scores,'selected':selected,'boundary':'70inclusive;D70excluded by rank gate'}
proof['21']={'truth':[False,False,False,False,True],'ruleChecks':['change requires permission','minor not identical to incapacity','10days<1month exemption','deemed permission checked not renewed','no guardian => spouse before ascendant']}
assert 180>300/2 and date(2023,10,10)<date(2027,4,10)<date(2027,10,10) and date(2024,11,29)>date(2024,11,23) and date(2026,3,5)<date(2026,11,29)
proof['22']={'answer':4,'benefitCap':150,'possibleExtension':'3years6months within max4years','reEmployment':'within2years but quit after6months fails conjunction','dateCounting':'calendar month correspondence,not30day approximation'}
proof['23']={'answer':2,'bothBranches':['public trap fishing requires report','private listed fishing requires report'],'exceptions':['license not permission grants registerable right','specialcity direct ministry','unregistered not right-holder for extension','publicwork exception to mandatory extension']}
assert date(2024,3,10)>date(2023,4,10)
proof['24']={'answer':1,'minimum500Included':True,'directAcquisition3yearExceptionExpired':True,'wrong':['400below500','broker not seller','inheritance not resale','after30years expired']}
survivor=200*F(3,5);own=80+survivor*F(3,10);assert survivor==120 and own==116
proof['25']={'truth':[False,True,False,False],'survivor':120,'ownPlus30pct':116,'priority':'spouse incl de facto before child;disability age exemption not priority exemption','grandchild20failsUnder19':True}
proof['26']={'truth':[True,False,False,True],'dates':{'monks':'12thcentury','popular':'19thcentury'},'colors':['buffalo white','cow cream'],'yield':'equal100L, cow<buffalo24kg;daily12L irrelevant'}
fractions=[F(1,5),F(1,4),F(1,2),F(4,5)];gifts=[40,30,20,10]
def path(x):
 out=[];h=F(x)
 for f,g in zip(fractions,gifts):h=h*(1-f)+g;out.append(h)
 return out
solutions=[]
for x in range(1,1001):
 h=path(x)[-1];assert h==F(3,50)*x+20
 if x+100-h==9*h:solutions.append(x)
assert solutions==[250] and path(250)==[240,210,125,35]
proof['29']={'uniqueWithin1000':solutions,'globalLinearEquation':'3x+1000=5x+500 =>x250','path':[240,210,125,35],'total350':True}
alloc=[(perm,sum(w*10*(d-start) for w,d,start in zip([30,20,10],perm,[1,2,3]))) for perm in it.permutations([3,4,5])]
lo=min(alloc,key=lambda x:x[1]);hi=max(alloc,key=lambda x:x[1]);assert lo==((3,4,5),1200) and hi==((5,4,3),1600)
proof['30']={'all6':alloc,'minimum':lo,'maximum':hi,'ratio':'4/3','truth':[False,True,False,True],'proof':'all destinations >= starts; fixed origin term; pair exchange product determines extremum'}
keys={}
for post,date,year,book in [(5982,'2026-03-07','2026','㉯')]:
 with pdfplumber.open(next((R/f'artifacts/psat600_20261028/sources/{post}').glob('*.pdf'))) as pdf:
  t=next(p.extract_text() for p in pdf.pages if '영역 상황판단' in p.extract_text());assert year in t and book in t;k={}
  for line in t.splitlines():
   if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
    v=list(map(int,line.split()));k.update(zip(v[::2],v[1::2]))
  assert len(k)==(40 if post==5982 else 25);keys[date]=k
def norm(s):
 if '쌀의 , 둘째 날은 , 셋째 날은 , 넷째 날은 를' in s:
  a=s.index('   ');b=s.index('나에게 다오.',a);s=s[:a]+'쌀의 1/5, 둘째 날은 1/4, 셋째 날은 1/2, 넷째 날은 4/5를 '+s[b:]
 return re.sub(r'[\s·․]+','',s)
tableSources=json.loads((A/'table-source-text.json').read_text(encoding='utf-8'));rawTables={int(k):v for k,v in tableSources.items()}
expectedTables={
16:[(['구분','차량가액(만 원)','차종','유종'],[['甲','160','승용','휘발유'],['乙','240','승용','경유'],['丙','250','화물','경유'],['丁','280','승합','휘발유'],['戊','300','화물','휘발유']])],
17:[(['어업인 수','점수'],[['2,000명 이상','40점'],['1,000명 이상 2,000명 미만','30점'],['1,000명 미만','20점']]),
(['어업 분야 예산','점수'],[['200억 원 이상','40점'],['100억 원 이상 200억 원 미만','20점'],['100억 원 미만','10점']]),
(['주거공간 확보','점수'],[['가능','20점'],['불가능','0점']]),
(['후보지역','어업인 수(명)','어업 분야 예산(억 원)','주거공간 확보'],[[a,str(p) if p<1000 else f'{p:,}',str(b),'가능' if h else '불가능'] for a,p,b,h in zip('ABCDEF',people,budgets,homes)])]}
for q in bank:
 n=q['number'];src=tr[q['id']]
 assert norm(q['prompt'])==norm(src['prompt']),(n,'prompt')
 assert len(q['choices'])==5 and all(norm(x)==norm(y) for x,y in zip(q['choices'],src['choices'])),(n,'choices')
 originalBody=norm(src['body'])
 for rawTable in rawTables.get(n,[]):
  assert originalBody.count(norm(rawTable))==1;originalBody=originalBody.replace(norm(rawTable),'',1)
 assert len(q['tables'])==len(expectedTables.get(n,[]))
 for table,(columns,rows) in zip(q['tables'],expectedTables.get(n,[])):
  assert table['columns']==columns and table['rows']==rows,(n,'table cells')
  assert 0<=table['afterParagraph']<len(q['body'].split('\n\n'))
 if n==17:assert len({t['afterParagraph'] for t in q['tables'][:3]})==1 and q['tables'][3]['afterParagraph']>q['tables'][0]['afterParagraph']
 assert norm(q['body'])==originalBody,(n,'body')
 assert q['answer']==keys[q['examDate']][n] and len(q['steps'])==len(q['optionReasons'])==5
 assert not any('\ue000'<=c<='\uf8ff' or c in '\ufffd\u2060\u2024' for c in json.dumps(q,ensure_ascii=False)),n
 assert not re.search(r'\d{4}\.\s*\n\s*\n\s*\d{1,2}\.',q['body'])
for c in json.loads((A/'crop-manifest.json').read_text(encoding='utf-8')):
 source=R/c['source'];assert hashlib.sha256(source.read_bytes()).hexdigest()==c['sha256']
 with pdfplumber.open(source) as pdf:
  ref=pdf.pages[c['page1based']-1].crop(c['rect']).to_image(resolution=c['resolution'],antialias=True).original.convert('RGB');path=R/c['asset'] if P.exists() else A/'staged'/c['asset'];im=Image.open(path).convert('RGB');assert im.size==ref.size and im.tobytes()==ref.tobytes(),c['asset']
seen=set();old=0
for path in (R/'assets/psat').glob('*.json'):
 if path.name in ['sets.json','situation17.json']:continue
 obj=json.loads(path.read_text(encoding='utf-8'))
 if isinstance(obj,list):
  for q in obj:
   k=(q.get('examDate',q['source'][:10].replace('.','-')),q['subject'],q['number']);assert k not in seen;seen.add(k);old+=1
for q in bank:
 k=(q['examDate'],q['subject'],q['number']);assert k not in seen;seen.add(k)
for path,digest in json.loads((A/'before-situation17-hashes.json').read_text(encoding='utf-8')).items():
 if path!='assets/psat/sets.json':assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
proof.update(status='PASS',count=10,officialFinalKeys=10,sourceComparison='native prompt/body/choices;5native tables including three transposed rubric tables/4fractions/10originalpixels',preservedExisting=old,limitations='Same-author semantic review with logical countermodels;not independent expert review.')
(A/'content-checks.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PASS10source/key/10pixels;models;preserved',old)
