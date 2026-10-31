from pathlib import Path
import json,re,hashlib,itertools as it,pdfplumber
from fractions import Fraction as F
from PIL import Image
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/verbal12';P=R/'assets/psat/verbal12.json'
bank=json.loads((P if P.exists() else A/'authored-verbal12.json').read_text(encoding='utf-8'));tr=json.loads((A/'source-transcripts.json').read_text(encoding='utf-8'));proof={}
assert [q['number'] for q in bank]==list(range(13,23))
proof['13']={'violated':1,'obeyed':[2,3],'exceptionNeeded':'unavoidable human casualties in rescue;not robot self-damage','answer':3}
p=F(4,5);assert p!=1-p
# A independent distribution and B transition table are separate countermodels.
transition={'X':F(1,4),'Y':F(3,4)}
assert transition['XY'[-1]]==transition['YY'[-1]]
proof['14']={'truth':[False,True,False],'AUnequalProbabilities':['4/5','1/5'],'BHistory':'XY and YY end in same Y'}
proof['15']={'truth':[True,True,True],'evidence':['diagnosis without prognosis not recognized','diagnosis and dietary advice recognized without drug prescription','diagnosis plus accurate prognosis recognized despite treatment failure'],'limit':'Do not invent prognosis in case B;that case supports rejecting a treatment-success criterion.'}
mountains=[]
for s,j,t,b in it.product([False,True],repeat=4):
 if (not s or j) and (not j or b) and not(j and b) and (not t or not s):mountains.append([s,j,t,b])
assert len(mountains)==4 and all(not x[0] and not x[1] for x in mountains) and max(map(sum,mountains))==2
proof['16']={'names':['설악','지리','속리','소백'],'allValid':mountains,'maximum':2}
staff=[]
for g,n,d,r,m in it.product([False,True],repeat=5):
 if g!=n and (g or d or r) and (n or d) and (not d or not g) and (not r or not m) and m:staff.append([g,n,d,r,m])
assert staff==[[False,True,True,False,True]]
proof['17']={'names':['가훈','나연','다솜','라은','마현'],'allValid':staff,'count':3}
schedules=[]
for people in it.permutations('갑을병정'):
 for movies in it.permutations('ABCD'):
  if not people.index('갑')>people.index('병'):continue
  if not movies.index('A')==people.index('정')+1:continue
  if not movies.index('B')<movies.index('C'):continue
  if len({0,people.index('병'),people.index('정'),movies.index('D')})!=4:continue
  schedules.append([list(people),list(movies)])
assert schedules==[[list('을정병갑'),list('BCAD')]]
proof['18']={'allSchedules':schedules,'days':['Tue','Wed','Thu','Fri'],'truth':[True,True,True,False,True]}
experiments=[('A',3,2),('A',2,3),('B',2,3)] # first seen, A count, B count
pred=[[first,'A' if a<b else 'B'] for first,a,b in experiments]
assert pred==[['A','B'],['A','A'],['B','A']]
results=['B','B','A'];effects=[['strengthen' if result==guess else 'weaken' for guess in pair] for pair,result in zip(pred,results)]
assert effects==[['weaken','strengthen'],['weaken','weaken'],['weaken','strengthen']]
proof['19']={'predictedHigherSurvival':pred,'observedHigher':results,'effects':effects,'truth':[True,False,False]}
# One internally consistent monotonic model; numeric ranks are not treated as measured intensity.
light={'A':F(1),'B':F(3,2),'C':F(1)};response={'I':{'A':5,'B':2,'C':2},'II':{'A':1,'B':4,'C':4}}
signal={d:{x:light[x]*response[d][x] for x in light} for d in response}
assert signal['II']['A']<signal['I']['C']<signal['I']['B']<signal['II']['C']<signal['I']['A']<signal['II']['B']
assert light['B']>light['A'] and response['I']['A']>response['II']['A'] and response['I']['B']<response['II']['B']
proof['20']={'rankTable':[['I',5,3,2],['II',1,6,4]],'directions':['B>A','A:II<I','B:II>I'],'consistentIllustrativeModel':{d:{x:str(v) for x,v in row.items()} for d,row in signal.items()},'limit':'model is a consistency witness;rank numbers do not imply ratios'}
cases=[dict(prior=a,positive=b,unshielded=c,initial=a and b,revised=a and b and c) for a,b,c in it.product([False,True],repeat=3)]
assert any(x['positive'] and not x['initial'] for x in cases)
assert any(x['positive'] and x['initial'] for x in cases)
assert any(x['positive'] and x['revised'] for x in cases)
assert any(x['positive'] and not x['revised'] for x in cases)
proof['21']={'definitionTruthTable':cases,'invalid':2,'reason':'initial theory also requires temporal precedence'}
proof['22']={'order':['overload','delay','down'],'truth':[False,True,True],'shielding':'Within the passage definition, absent overload delay does not increase down probability.','conditional':'O causes D; if O causes S then common cause of D,S.','limit':'Given event universe and passage definitions;not universal causal-identification rule.'}
with pdfplumber.open(next((R/'artifacts/psat600_20261028/sources/6001').glob('*.pdf'))) as pdf:
 t=next(p.extract_text() for p in pdf.pages if '영역 언어논리' in p.extract_text());assert '2025' in t and '혁' in t;keys={}
 for line in t.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
   v=list(map(int,line.split()));keys.update(zip(v[::2],v[1::2]))
 assert len(keys)==25
norm=lambda s:re.sub(r'[\s□·․]+','',s)
for q in bank:
 n=q['number'];src=tr[q['id']]
 assert norm(q['prompt'])==norm(src['prompt']),(n,'prompt')
 assert all(norm(x)==norm(y) for x,y in zip(q['choices'],src['choices'])),(n,'choices')
 if n==20:
  before,table=src['body'].split('빛\nA B C\n검출기',1)
  assert norm(q['body'])==norm(before) and norm(table)=='I532II164'
  assert q['tables'][0]['rows']==[['I','5','3','2'],['II','1','6','4']]
 else:assert norm(q['body'])==norm(src['body']),(n,'body')
 assert q['answer']==keys[n] and len(q['steps'])==len(q['optionReasons'])==5,(n,q['answer'],keys[n])
 assert all(q['body'].count(u)==1 and '\n' not in u for u in q.get('underlines',[])),(n,'underline',q.get('underlines'))
 assert not any('\ue000'<=c<='\uf8ff' or c in '\ufffd\u2060\u2024' for c in json.dumps(q,ensure_ascii=False)),n
assert '하지만 □ 사회적으로' in bank[0]['body']
assert bank[8]['body'] in bank[9]['body']
for c in json.loads((A/'crop-manifest.json').read_text(encoding='utf-8')):
 source=R/c['source'];assert hashlib.sha256(source.read_bytes()).hexdigest()==c['sha256']
 with pdfplumber.open(source) as pdf:
  ref=pdf.pages[c['page1based']-1].crop(c['rect']).to_image(resolution=c['resolution'],antialias=True).original.convert('RGB');path=R/c['asset'] if P.exists() else A/'staged'/c['asset'];im=Image.open(path).convert('RGB');assert im.size==ref.size and im.tobytes()==ref.tobytes(),c['asset']
seen=set();old=0
for path in (R/'assets/psat').glob('*.json'):
 if path.name in ['sets.json','verbal12.json']:continue
 obj=json.loads(path.read_text(encoding='utf-8'))
 if isinstance(obj,list):
  for q in obj:
   k=(q.get('examDate',q['source'][:10].replace('.','-')),q['subject'],q['number']);assert k not in seen;seen.add(k);old+=1
for q in bank:
 k=(q['examDate'],q['subject'],q['number']);assert k not in seen;seen.add(k)
for path,digest in json.loads((A/'before-verbal12-hashes.json').read_text(encoding='utf-8')).items():
 if path!='assets/psat/sets.json':assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
proof.update(status='PASS',count=10,officialFinalKeys=10,sourceComparison='native prompt/body/choices;table1;blank/underlines;shared21and22;10originalpixelcomparisons',preservedExisting=old,limitations='Same-author semantic review with exhaustive models;not independent expert review.')
(A/'content-checks.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PASS10source/key/10pixels;models;preserved',old)
