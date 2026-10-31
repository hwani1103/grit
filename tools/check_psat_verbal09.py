from pathlib import Path
import json,re,itertools as it,hashlib,pdfplumber
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/verbal09';P=R/'assets/psat/verbal09.json';bank=json.loads((P if P.exists() else A/'authored-verbal09.json').read_text(encoding='utf-8'));proof={}
imp=lambda a,b:not a or b
# q6: three people incl an unnamed third; all qualifying people represent.
states=[(g,c,p,s) for g,c,p,s in it.product([False,True],repeat=4) if not(g and(c or p))];count=[0]*5;counter=[None]*5
for people in it.product(states,repeat=3):
 rep=[(c or p) and s for g,c,p,s in people]
 if not any(rep):continue
 g,c,p,s=people[0];G,C,Pp,S=people[1]
 opts=[c and s,(c or p or C or Pp),(not g and s and not G and S),imp(not Pp,not S),all(imp(c or p,s) for g,c,p,s in people)]
 for attends in [False,True]:
  if not imp(rep[0] or rep[1],attends):continue
  for i,v in enumerate(opts):
   if v:
    count[i]+=1
    if not attends:counter[i]=people
assert all(count) and [c is None for c in counter]==[True,False,False,False,False]
proof['6']={'optionCounterexamples':counter,'modelsPerOption':count}
# q7: 2 attendees x 2 ideas realises the relevant quantifier patterns.
models=[]
for rel in it.product([False,True],repeat=4):
 rows=[rel[:2],rel[2:]];truth=[any(all(row[j] for row in rows) for j in range(2)),all(any(row) for row in rows),any(rel),not any(rel)]
 for culprit in range(4):
  second=[culprit!=1,culprit in [2,3],culprit!=3,culprit==0]
  if truth==second:models.append((rel,truth,culprit))
assert models and any(t[0] and t[2] for r,t,c in models) and any(t[1] and t[2] for r,t,c in models)
assert any(sum(t)==3 for r,t,c in models) and all(imp(sum(t)==3,c==2) for r,t,c in models)
proof['7']={'models':models,'truth':[True,False,True]}
# q8 full propositional valuation.
models=[]
for p,q,r,c,s,m in it.product([False,True],repeat=6):
 if all([imp(p,q),imp(r,p and q),imp(p and c,s),imp(q,r or m),c and not s]):models.append((p,q,r,c,s,m))
assert models and [all(v for v in col) for col in zip(*[(not p and not q,not r and c,imp(q,m)) for p,q,r,c,s,m in models])]==[False,True,True]
proof['8']={'models':models,'truth':[False,True,True]}
# q9 complete assignments: Copenh=0,Born=1,Einstein=2,Many=3,Other=4.
counter=[None]*5;modelcount=0
for vals in it.product(range(5),repeat=6):
 a,d,e,f,g,h=vals;v=[a,0,1,d,e,f,g,h]
 if a not in [0,1] or d not in [0,1] or sum(x in [0,1] for x in v)!=5 or 2 not in v:continue
 modelcount+=1;opts=[3 in v,imp(v.count(1)==2,a!=d),imp(a!=d,v.count(0)>=2),imp(v.count(3)==1,v.count(2)==2),imp(v.count(0)==3,1 in [a,d])]
 for i,b in enumerate(opts):
  if not b and counter[i] is None:counter[i]=v
assert modelcount and [v is None for v in counter]==[False,False,True,False,False]
proof['9']={'modelCount':modelcount,'counterexamples':counter}
# q12 weakened premise still entails conclusion; extra goals irrelevant.
models=[]
for f1,f2,discard,psych,extra in it.product([False,True],repeat=5):
 if (f1 or f2) and imp(f1 or f2,discard) and imp(discard,psych):models.append((f1,f2,discard,psych,extra))
assert models and all(x[3] for x in models);proof['12']={'weakenedPremiseModels':models}
# q13 the self-referential truth conditions admit only no-return and payment.
models=[(r,p) for r,p in it.product([False,True],repeat=2) if imp(r or p,not r) and imp(not(r or p),r)]
assert models==[(False,True)];proof['13']={'models':models,'rules':['DeMorgan','reductio','disjunctive syllogism']}
# q15 concrete countermodels and false equality interpretation.
scientist={0};athlete={0,1};philosopher={1};assert scientist&athlete and not philosopher&scientist and philosopher&athlete
red={0};holes={0,1};triangle={0};assert red<=holes and red<=triangle and not holes<=triangle
phys={0};sci={0,1};coder={1};assert phys<=sci and coder&sci and not coder&phys
proof['15']={'realValidity':[False,False,False],'explainedBySpecifiedTheory':[False,True,True],'countermodels':'3 distinct set assignments checked;all legitimate conversions preserve the first premises'}
proof['10']={'manualReview':'treatment vs measurement;no neuron count/effect magnitude/mediating causality demonstrated','answer':2}
proof['11']={'manualReview':'A vs B movement;room2 identical sound vs room3different;B cannot ultrasound;not statistically meaningful0.1sec','truth':[True,True,False]}
proof['14']={'manualReview':'philosophy vs all intellectual work;abduction explicitly inductive;empirical premise need not imply inductive method','truth':[False,True,False]}
keys={}
with pdfplumber.open(next((R/'artifacts/psat600_20261028/sources/3982').glob('*.pdf'))) as pdf:
 t=next(p.extract_text() for p in pdf.pages if '영역 언어논리' in p.extract_text());assert '2021년도' in t and '나 책형' in t
 for line in t.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
   v=list(map(int,line.split()));keys.update(zip(v[::2],v[1::2]))
assert len(keys)==25 and [keys[n] for n in range(6,16)]==[1,3,4,3,2,3,4,5,2,4]
norm=lambda s:re.sub(r'[\s□·․]+','',s)
for q in bank:
 n=q['number'];raw=(A/f'2021-l{n}-source.txt').read_text(encoding='utf-8');prompt,tail=raw.split('?',1);body,opts=tail.rsplit('\n① ',1);choices=re.split('[①②③④⑤]','① '+opts)[1:]
 assert norm(q['prompt'])==norm(prompt+'?') and norm(q['body'])==norm(body),(n,'source')
 assert len(choices)==5 and all(norm(a)==norm(b) for a,b in zip(q['choices'],choices)),(n,'choices')
 for u in q.get('underlines',[]):assert q['body'].count(u)==1,(n,u)
 assert q['answer']==keys[n] and len(q['steps'])==len(q['optionReasons'])==5
 for s,prefix in zip(q['steps'],['착안점: ','실전 풀이: ','답 확정 기준: ','정석 근거: ','적용 한계: ']):assert s.startswith(prefix) and len(s)>40
 assert not any('\ue000'<=c<='\uf8ff' or c in '\ufffd\u2060\u2024' for c in json.dumps(q,ensure_ascii=False))
assert '참가하는데, □ 때문이다.' in bank[0]['body']
source=next((R/'artifacts/psat600_20261028/sources/3977/pdf').glob('*언어*'))
with pdfplumber.open(source) as pdf:
 for c in json.loads((A/'crop-manifest.json').read_text(encoding='utf-8')):
  assert hashlib.sha256(source.read_bytes()).hexdigest()==c['sha256'];ref=pdf.pages[c['page1based']-1].crop(c['rect']).to_image(resolution=c['resolution'],antialias=c.get('antialias',False)).original.convert('RGB');path=R/c['asset'] if P.exists() else A/'staged'/c['asset'];im=Image.open(path).convert('RGB');assert im.size==ref.size and ImageChops.difference(im,ref).getbbox() is None
seen=set();old=0
for path in (R/'assets/psat').glob('*.json'):
 if path.name in ['sets.json','verbal09.json']:continue
 obj=json.loads(path.read_text(encoding='utf-8'))
 if isinstance(obj,list):
  for q in obj:
   k=(q.get('examDate',q['source'][:10].replace('.','-')),q['subject'],q['number']);assert k not in seen;seen.add(k);old+=1
for q in bank:
 k=(q['examDate'],q['subject'],q['number']);assert k not in seen;seen.add(k)
for path,digest in json.loads((A/'before-verbal09-hashes.json').read_text(encoding='utf-8')).items():
 if path!='assets/psat/sets.json':assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
proof.update(status='PASS',count=10,officialFinalKeys=10,sourceComparison='allnativeprompt/body/options;blankrestored;10originalpixelcomparisons',preservedExisting=old,limitations='Same-author original reading/manual semantics plus independent-form algorithmic models;not independent expert review.')
(A/'content-checks.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PASS10source/key/original;logicmodels;preserved',old)
