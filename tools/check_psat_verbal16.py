from pathlib import Path
import json,re,hashlib,itertools as it,pdfplumber
from PIL import Image
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/verbal16';P=R/'assets/psat/verbal16.json'
bank=json.loads((P if P.exists() else A/'authored-verbal16.json').read_text(encoding='utf-8'));tr=json.loads((A/'source-transcripts.json').read_text(encoding='utf-8'))
assert [(q['examDate'],q['number']) for q in bank]==[('2026-03-07',n) for n in [15,16,17,18,19,20,25,26,27,28]]
proof={}
imp=lambda a,b:not a or b
experiments=[(True,False,False),(False,False,True),(False,True,False)]
fits=[(i and v,i,v or m) for i,v,m in experiments]
assert fits==[(False,True,False),(False,False,True),(False,False,True)]
proof['15']={'necessaryConditionFitsForIonlyMonlyVonly':fits,'truth':[False,False,True],'limits':'consistent successful cases support but do not establish necessity'}
# An explicit numeric countermodel to a forced chemical ranking in ㄱ/ㄷ.
E=[10,2,2];C=[1,8,7];S=[e+c for e,c in zip(E,C)]
assert S[0]>S[1]>S[2] and C[0]<C[1] and C[0]<C[2]
count=0
for S in it.combinations(range(1,10),3):
 for E in it.combinations(range(0,9),3):
  totals=list(reversed(S));chem=[x-y for x,y in zip(totals,E)]
  if min(chem)<0:continue
  assert chem[0]>chem[1]>chem[2];count+=1
proof['16']={'truth':[False,True,False],'reverseOrderSumModels':count,'countermodelFor1and3':{'E':[10,2,2],'C':[1,8,7],'total':[11,10,9]},'radiusLimit':'unknown optimum may be at A;size order alone cannot rank E'}
for cause,responsible in it.product([False,True],repeat=2):
 if imp(responsible,cause):assert imp(not cause,not responsible)
proof['17']={'truth':[False,True,False],'scopes':['individual','subgroup of at least2','humanity'],'necessaryOnly':'responsibility->cause does not entail cause->responsibility'}
proof['18']={'answer':4,'observedBothGroups':[0,2,7],'weeks':[0,3,6],'difference':'only group1 artificially exposed;both illuminated','boundary':'no artificial exposure does not mean isolated from environment'}
proof['19']={'answer':3,'bothRequired':['reject human exclusivity','reject empirical performance as sufficient test'],'notClaimed':'AI understanding forever impossible'}
proof['20']={'answer':5,'attack':'human brain also represents reality undermines proposed distinguishing criterion','notProved':'AI necessarily understands'}
proof['25']={'answer':4,'timeline':{'middle':'executor and disseminator already','late':'leading patrons and driving force'},'definitionSplit':['private profit middle','labor commodity late14-15century']}
proof['26']={'answer':5,'distinctions':['intentional selection vs malicious distortion','fabrication vs data selection'],'scope':'some scholars view in passage,not general permission'}
proof['27']={'answer':4,'analogy':['unexplained orbit residual','unknown nearby planet hypothesis'],'timeline':['Leverrier Newtonian hypothesis','Einstein general relativity explanation']}
proof['28']={'answer':4,'mapping':{'가':'criterion distinguishing just/unjust war','나':'moral constraints on specific combat acts'}}
keys={}
for post,date,year,book in [(5982,'2026-03-07','2026','㉯')]:
 with pdfplumber.open(next((R/f'artifacts/psat600_20261028/sources/{post}').glob('*.pdf'))) as pdf:
  t=next(p.extract_text() for p in pdf.pages if '영역 언어논리' in p.extract_text());assert year in t and book in t;k={}
  for line in t.splitlines():
   if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
    v=list(map(int,line.split()));k.update(zip(v[::2],v[1::2]))
  assert len(k)==(40 if post==5982 else 25);keys[date]=k
def norm(s):
 s=s.replace('c(1)','c₁').replace('c(n)','cₙ')
 s=s.replace('c , … , c 으로\n1 n\n','c₁, …, cₙ으로\n').replace('c , … , c 중 일부로 구성된 합산적 행위도 있다.\n1 n','c₁, …, cₙ 중 일부로 구성된 합산적 행위도 있다.')
 return re.sub(r'[\s·․]+','',s.replace('[빈칸]','').replace('m2','m²'))
for q in bank:
 n=q['number'];src=tr[q['id']]
 assert norm(q['prompt'])==norm(src['prompt']),(n,'prompt')
 assert len(q['choices'])==5 and all(norm(x)==norm(y) for x,y in zip(q['choices'],src['choices'])),(n,'choices')
 assert norm(q['body'])==norm(src['body']),(n,'body')
 assert not q['tables'] and not q['figures']
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
 if path.name in ['sets.json','verbal16.json']:continue
 obj=json.loads(path.read_text(encoding='utf-8'))
 if isinstance(obj,list):
  for q in obj:
   k=(q.get('examDate',q['source'][:10].replace('.','-')),q['subject'],q['number']);assert k not in seen;seen.add(k);old+=1
for q in bank:
 k=(q['examDate'],q['subject'],q['number']);assert k not in seen;seen.add(k)
for path,digest in json.loads((A/'before-verbal16-hashes.json').read_text(encoding='utf-8')).items():
 if path!='assets/psat/sets.json':assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
assert bank[4]['body']==bank[5]['body'] and bank[4]['body'].count('[빈칸]')==1
assert bank[2]['body'].count('c(1)')==2 and bank[2]['body'].count('c(n)')==2
assert bank[7]['body'].count('[빈칸]')==bank[8]['body'].count('[빈칸]')==1
assert bank[1]['underlines']==['화학적 증강은 금속 A에서 가장 작다']
proof.update(status='PASS',count=10,officialFinalKeys=10,sourceComparison='native prompt/body/choices;subscripts/1underline/shared dialogue/explicit blanks/10originalpixels',preservedExisting=old,limitations='Same-author semantic review with logical countermodels;not independent expert review.')
(A/'content-checks.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PASS10source/key/10pixels;models;preserved',old)
