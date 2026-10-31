from pathlib import Path
import json,re,hashlib,itertools,pdfplumber
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/verbal07';P=R/'assets/psat/verbal07.json'
bank=json.loads((P if P.exists() else A/'authored-verbal07.json').read_text(encoding='utf-8'))
def norm(s):return re.sub(r'[\s□·]+','',s.replace('\ue09d','α').replace('\ue09e','β'))
with pdfplumber.open(next((R/'artifacts/psat600_20261028/sources/5994').glob('*.pdf'))) as pdf:
 text=next(p.extract_text() for p in pdf.pages if '영역 언어논리' in p.extract_text());assert '2025년도' in text and '인 책형' in text
 key={}
 for line in text.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
   vs=list(map(int,line.split()));key.update(zip(vs[::2],vs[1::2]))
 assert len(key)==25
for q in bank:
 n=q['number'];raw=(A/f'2025-l{n}-source.txt').read_text(encoding='utf-8').split(f'{n}.',1)[1];prompt,tail=raw.split('?',1);body,opts=tail.rsplit('\n① ',1)
 if n in [13,19]:body=body.rsplit('\n(가) (나) (다)',1)[0];assert q['choiceNote']=='선택지의 순서: (가) → (나) → (다)'
 assert norm(q['prompt'])==norm(prompt+'?'),(n,'prompt')
 assert norm(q['body'])==norm(body),(n,'body')
 options=re.split('[①②③④⑤]','① '+opts)[1:];assert len(options)==5
 assert all(norm(a)==norm(b) for a,b in zip(options,q['choices'])),(n,'options')
 assert q['answer']==key[n],(n,'key')
 assert len(q['steps'])==len(q['optionReasons'])==5
 for s,prefix in zip(q['steps'],['착안점: ','실전 풀이: ','답 확정 기준: ','정석 근거: ','적용 한계: ']):assert s.startswith(prefix) and len(s)>40
 for u in q.get('underlines',[]):assert q['body'].count(u)==1
 assert not any('\ue000'<=c<='\uf8ff' or c in '\ufffd\u2060' for c in json.dumps(q,ensure_ascii=False))
 assert (R/q['original'] if P.exists() else A/'staged'/q['original']).exists()
assert sum(len(q.get('underlines',[])) for q in bank)==2
assert '왜냐하면 □.' in bank[6]['body']
# Independent boolean enumeration, separate from explanation text.
imp=lambda a,b:not a or b
m16=[]
for p,i,s,n,o in itertools.product([False,True],repeat=5):
 if imp(p,o) and imp(i,n) and imp(s,p) and (s or i):m16.append((p,i,s,n,o))
def options16(x):
 p,i,s,n,o=x;return [n,i and s,p or s,imp(not o,p),n or o]
u16=[all(options16(x)[j] for x in m16) for j in range(5)];assert u16==[False]*4+[True]
for x,inds in [((True,False,True,False,True),[0,1]),((False,True,False,True,False),[2,3])]:
 assert x in m16 and all(not options16(x)[j] for j in inds)
m17=[]
for s,d,p,k,u in itertools.product([False,True],repeat=5):
 if imp(s,d) and imp(s and d,p) and imp(p,k) and imp(k,u):m17.append((s,d,p,k,u))
def premise17(x):
 s,d,p,k,u=x;return [d,imp(not d,not s),k,not u,p]
entails=[all(not x[0] for x in m17 if premise17(x)[j]) for j in range(5)];assert entails==[False,False,False,True,False]
assert all(any(premise17(x)[j] for x in m17) for j in range(5))
m18=[]
for x in itertools.product(range(4),repeat=6):
 counts=[x.count(k) for k in range(4)]
 if sorted(counts)!=[1,1,2,2] or counts[0]!=1:continue
 if any(x[j]==1 for j in range(3)):continue
 if len(set(x[:3]))<3 or len(set(x[3:]))<3:continue
 if counts[x[0]]!=1 or counts[x[3]]!=1:continue
 m18.append(x)
assert len(m18)==4
op18=lambda x:[x[0]==0 and x[2]==3,imp(x[1]==2,x[4]==3),x[1]!=3 and x[2]==2,x[3]!=1 and x[0]!=0,imp(x[5]==3,x[4]==2)]
assert [all(op18(x)[j] for x in m18) for j in range(5)]==[False]*4+[True]
assert (0,2,3,1,2,3) in m18 and (0,3,2,1,2,3) in m18
# Gap comparison proof: strict increase/decrease; integer grid and explicit countermodels.
groups={'>':[], '<':[], '=':[]}
for a0,b0,a1,b1 in itertools.product(range(1,12),repeat=4):
 if not(a0<b0 and a1>a0 and b1<b0):continue
 sign='>' if a1>b1 else '<' if a1<b1 else '='
 groups[sign].append(abs(a1-b1)<b0-a0)
assert all(groups['<']) and all(groups['=']) and any(groups['>']) and not all(groups['>'])
assert abs(4-3)<5-1 and abs(10-2)>5-1
# Poison-mimic table follows observed experiments.
avoid={'X1':{'a','c','d'},'X2':{'b','d'}};assert set.intersection(*avoid.values())=={'d'}
seen=set();old=0
for p in (R/'assets/psat').glob('*.json'):
 if p.name in ['sets.json','verbal07.json']:continue
 obj=json.loads(p.read_text(encoding='utf-8'))
 if isinstance(obj,list):
  for q in obj:
   k=(q.get('examDate',q['source'][:10].replace('.','-')),q['subject'],q['number']);assert k not in seen;seen.add(k);old+=1
for q in bank:
 k=(q['examDate'],q['subject'],q['number']);assert k not in seen;seen.add(k)
for path,digest in json.loads((A/'before-verbal07-hashes.json').read_text(encoding='utf-8')).items():
 if path!='assets/psat/sets.json':assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
proof={'status':'PASS','count':10,'officialFinalKeys':10,'normalizedSource':'all prompts/passages/options;Greek/blank restored;choice headers explicit','underlines':2,'q11':'outside acceleration before injection;density compensation possibility not arbitrary increase guarantee','q12':[True,True,False],'q13':['도지','소작인','타작'],'q14':'3500BC steppe domestication in passage','q15':'unit analysis efficacy challenged','q16':{'models':m16,'universalOptions':u16},'q17':{'models':m17,'sufficientPremises':entails},'q18':{'models':m18,'singletons':'A갑D을','answer':5},'q19':['강한','약한','약한'],'q20':{'truth':[False,True,True],'counterexamples':[[1,5,4,3],[1,5,10,2]],'sampleCount':sum(map(len,groups.values()))},'preservedExisting':old,'limitations':'Same-author review, not independent expert certification.'}
(A/'content-checks.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PASS10 source/key,2underlines/blank/Greek,logic exhaustive,4arrangements,gapcounterexamples;preserved',old)