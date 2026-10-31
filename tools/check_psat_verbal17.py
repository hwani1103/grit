from pathlib import Path
import json,re,hashlib,itertools as it,pdfplumber
from PIL import Image
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/verbal17';P=R/'assets/psat/verbal17.json'
bank=json.loads((P if P.exists() else A/'authored-verbal17.json').read_text(encoding='utf-8'));tr=json.loads((A/'source-transcripts.json').read_text(encoding='utf-8'))
assert [(q['examDate'],q['number']) for q in bank]==[('2026-03-07',n) for n in [30,31,32,35,39,40]]+[('2025-03-08',n) for n in [13,14,33,34]]
proof={};imp=lambda a,b:not a or b
worlds=[]
for C,H,D,F in it.product([False,True],repeat=4):
 statements=[imp(C,not H),C,imp(F,not D) and D,imp(not H,F) and imp(C,F),not H and D and imp(not H,F)]
 a,b,c,d,e=statements
 opts=[imp(a and b,d),imp(a and d,b),not(b and c),not(c and e),not(d and e)]
 worlds.append({'C':C,'H':H,'D':D,'R':F,'options':opts})
truth=[all(w['options'][i] for w in worlds) for i in range(5)];assert truth==[False,False,False,True,False]
proof['2025-13']={'truth':truth,'allWorlds':16,'counterexamples':{str(i+1):next(w for w in worlds if not w['options'][i]) for i in [0,1,2,4]}}
valid=[]
for A0,B,C,D,E,F,G in it.product([False,True],repeat=7):
 if not(imp(A0,not G) and imp(B,D) and imp(C or E,G) and imp(not F,not D)):continue
 opts=[imp(A0,B or C),imp(B,F),imp(C,not A0),imp(E,B),imp(F,not E)]
 valid.append({'values':[A0,B,C,D,E,F,G],'options':opts,'target':imp(A0,F)})
truth=[all(not w['options'][i] or w['target'] for w in valid) for i in range(5)];assert truth==[True,False,False,False,False]
proof['2025-14']={'truth':truth,'baseWorlds':len(valid),'counterexamples':{str(i+1):next(w for w in valid if w['options'][i] and not w['target']) for i in [1,2,3,4]}}
valid=[]
for a,b,c,d,e in it.product(range(1,8),repeat=5):
 good=lambda x:x.bit_count()==2
 if not(a&1 and good(a) and not(a&b) and not good(b) and b&c and good(c) and not(c&d) and d&2 and d&e and not(e&4) and sum(map(good,[a,b,c,d,e]))>=3):continue
 opts=[good(e),not good(d),all(not(x&2) or x&4 for x in [a,b,c,d,e]),all(not(x&1) or good(x) for x in [a,b,c,d,e]),all(not(x&4 and good(x)) or x&1 for x in [a,b,c,d,e])]
 valid.append(([a,b,c,d,e],list(map(bool,opts))))
assert valid==[([3,4,5,2,3],[True,True,False,True,True])]
proof['2025-33']={'uniqueAssignmentY1S2W4':valid[0][0],'truth':valid[0][1],'enumerated':7**5,'fastWitness':'4 is sphere only, always contradicts option3;fullassignment unnecessary'}
subset=lambda x,y: x&y==x
count=0
for P0,Q,S,T0 in it.product(range(8),repeat=4):
 if not(subset(P0,S) and subset(S,T0) and T0&~Q):continue
 assert subset(P0,T0) and not subset(T0,Q);count+=1
count2=0
for Q,R0,S in it.product(range(8),repeat=3):
 if R0&~S and subset(Q,S):assert Q!=R0;count2+=1
proof['2025-34']={'truth':[True,True,True],'extensionalModels':count,'intensionalModels':count2,'proof':'P subset S subset T;T minus Q nonempty contradicts T=>Q;Q subset S and R minus S nonempty implies R!=Q'}
proof['2026-30']={'truth':[False,False,True],'distinctions':['unjustified privilege is distribution violation','bail is not punishment','3 and9 both within10;no claim about unseen procedure']}
proof['2026-31']={'truth':[True,True,True],'supportRoutes':['constitutional compensation','analogy to use-right fee','changed custom'],'notClaimed':'reinforcement is not conclusive real-world legal judgment'}
proof['2026-32']={'truth':[False,True,False],'scope':'conditional concession not own assertion;both accept possible misuse;critic rejects freedom conclusion'}
proof['2026-35']={'truth':[False,False,True],'directions':['income higher => collectivism lower','infection higher => collectivism higher','rice higher => collectivism higher'],'limits':'consistent observation not causal proof'}
proof['2026-39']={'answer':3,'halfThreshold':[70>50,95>50],'scope':'passage polyploid model;not universal biological theorem','wrongChoices':['unprovided total comparison','reversed rare-frequency benefit','new species vs persistence','birth vs fertility']}
proof['2026-40']={'truth':[True,True,False],'A':[60,40,20,60],'B':[0,20,40,0],'environments':['lake','lake','river','river'],'confound':'B2 unfamiliar rare vs B3 familiar common;equal result does not isolate either effect'}
keys={}
for post,date,year,book in [(5982,'2026-03-07','2026','㉯'),(4684,'2025-03-08','2025','㉮')]:
 with pdfplumber.open(next((R/f'artifacts/psat600_20261028/sources/{post}').glob('*.pdf'))) as pdf:
  t=next(p.extract_text() for p in pdf.pages if '영역 언어논리' in p.extract_text());assert year in t and book in t;k={}
  for line in t.splitlines():
   if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
    v=list(map(int,line.split()));k.update(zip(v[::2],v[1::2]))
  assert len(k)==40;keys[date]=k
def norm(s):return re.sub(r'[\s·․]+','',s)
removed=json.loads((A/'table-source-text.json').read_text(encoding='utf-8'))
for q in bank:
 n=q['number'];src=tr[q['id']]
 assert norm(q['prompt'])==norm(src['prompt']),(n,'prompt')
 assert len(q['choices'])==5 and all(norm(x)==norm(y) for x,y in zip(q['choices'],src['choices'])),(n,'choices')
 assert norm(q['body'])==norm(src['body']).replace(norm(removed.get(q['id'],'')),''),(n,'body')
 assert not q['figures']
 assert q['body'].count('『')==q['body'].count('』') and not re.search(r'『[^』]*『',q['body'])
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
 if path.name in ['sets.json','verbal17.json']:continue
 obj=json.loads(path.read_text(encoding='utf-8'))
 if isinstance(obj,list):
  for q in obj:
   k=(q.get('examDate',q['source'][:10].replace('.','-')),q['subject'],q['number']);assert k not in seen;seen.add(k);old+=1
for q in bank:
 k=(q['examDate'],q['subject'],q['number']);assert k not in seen;seen.add(k)
for path,digest in json.loads((A/'before-verbal17-hashes.json').read_text(encoding='utf-8')).items():
 if path!='assets/psat/sets.json':assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
assert norm(bank[4]['body']) in norm(bank[5]['body'])
assert bank[5]['tables']==[dict(caption='그물망별 물고기 수 · 단위 마리',columns=['구분','그물망 1','그물망 2','그물망 3','그물망 4'],rows=[['물고기 A','60','40','20','60'],['물고기 B','0','20','40','0']],afterParagraph=bank[5]['tables'][0]['afterParagraph'])]
assert norm(removed[bank[5]['id']])==norm('(단위: 마리) 그물망 1 그물망 2 그물망 3 그물망 4 물고기 A 60 40 20 60 물고기 B 0 20 40 0')
assert sum(len(q.get('underlines',[])) for q in bank)==7
proof.update(status='PASS',count=10,officialFinalKeys=10,sourceComparison='native prompt/body/choices;1table/7underlinedphrases/shared39-40/10originalpixels',preservedExisting=old,limitations='Same-author semantic review with logical countermodels;not independent expert review.')
(A/'content-checks.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PASS10source/key/10pixels;models;preserved',old)
