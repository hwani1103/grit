from pathlib import Path
from fractions import Fraction as F
import itertools as it,json,re,hashlib,pdfplumber
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/situation09';P=R/'assets/psat/situation09.json';bank=json.loads((P if P.exists() else A/'authored-situation09.json').read_text(encoding='utf-8'));proof={}
# all nonnegative integer allocations of100 efforts.
feasible=[]
for a in range(101):
 for b in range(101-a):
  for c in range(101-a-b):
   d=100-a-b-c;v=[360+3*a,400+3*b,440+3*c,240+3*d]
   if v[3]>max(v[:3]):feasible.append((a,b,c,d))
assert min(v[3] for v in feasible)==67 and (20,13,0,67) in feasible
proof['6']={'minimum':67,'witness':[20,13,0,67],'feasibleCount':len(feasible)}
# Two implementations: modular deletion and literal counting.
def fast(start):
 live=list(range(6));idx=start;out=[]
 while live:idx=(idx+5)%len(live);out.append(live.pop(idx))
 return out
def literal(start):
 live=list(range(6));idx=start;out=[]
 while live:
  for _ in range(5):idx=(idx+1)%len(live)
  out.append(live[idx]);live.pop(idx)
  if live:idx%=len(live)
 return out
sequences=[fast(i) for i in range(6)];assert all(fast(i)==literal(i) for i in range(6));match=[s for s in sequences if s[-1]==2];assert match==[[4,5,1,0,3,2]]
assert [n+1 for n in fast(0)]==[6,1,3,2,5,4]
q=next(q for q in bank if q['number']==7);assert '6→1→3→2→5→4' in q['steps'][1] and '팥→호박→인절미→쑥→무지개→송편' in q['steps'][3]
proof['7']={'allStarts':sequences,'matching':match,'draftCorrection':'unpublished numbering chain corrected against both implementations'}
# four positive integer weights; maxweight<54 because all weights positive.
solutions=[]
for d,c,b,a in it.combinations(range(1,54),4):
 if sorted([a+b,a+c,a+d,b+c,b+d,c+d])==[35,39,44,45,50,54]:solutions.append([a,b,c,d])
assert solutions==[[30,24,20,15]];proof['8']={'solutions':solutions,'relaxedNoninteger':[F(59,2).__str__(),F(49,2).__str__(),F(41,2).__str__(),F(29,2).__str__()]}
assert F(6,5)*10==12;proof['9']={'interval':str(F(6,5)),'lastOffset':12}
c=F(4);a=(6-c)/2;d=6-a;b=2*(6-d);e=(6-b)/2
assert [a,b,c,d,e]==[1,2,4,5,2];proof['10']={'completedSixths':list(map(str,[a,b,c,d,e]))}
allocations=[(a,b,c,4) for a,b,c in it.product(range(1,27),repeat=3) if sum([a,b,c,4])==30 and b>a>c>4]
assert max(v[2] for v in allocations)==7 and (8,11,7,4) in allocations;proof['11']={'max':7,'allocations':allocations}
areas=[6,3,2];cost=lambda kind,size:[9*size,6*size+20,3*size+5][kind];solutions=[]
for assign in it.permutations(range(3)):
 bills=[cost(k,s) for k,s in zip(assign,areas)]
 if bills[1]>max(bills[0],bills[2]):solutions.append((assign,bills))
assert solutions==[((2,1,0),[23,38,18])];proof['12']={'solutions':solutions}
def payment(i,dep,pages,draw,accepted):
 subtotal=1200000+max(i-1,0)*100000+dep*35000+max(pages-20,0)*9000+draw*15000;advance=min(subtotal,1400000);return subtotal,advance,advance*(2 if accepted else 1)
x=payment(1,2,14,3,True);y=payment(5,16,50,12,False);assert x==(1315000,1315000,2630000) and y==(2610000,1400000,1400000) and x[2]-y[2]==1230000;proof['13']={'applicants':[x,y],'difference':1230000}
pen=[3*2+6*F(1,2),5*2+3*F(3,2)+2*F(1,2),4*2+3+2*F(3,2)];grade=lambda x:'renew' if x>=70 else 'suspend' if x>=60 else 'cancel'
assert pen==[9,F('15.5'),14] and grade(60+15-pen[0])=='suspend';minimum=min(v for v in range(1,26) if grade(57+v-pen[1])!='cancel');assert minimum==19 and grade(78-pen[2])=='suspend' and grade(78-pen[2]+8)=='renew' and max(range(3),key=lambda i:pen[i])==1
proof['14']={'truth':[False,True,True,False],'penalties':list(map(str,pen)),'Bminimum':minimum,'CbeforeAfter':[64,72]}
# frequencies ordered quarter/month/week/day; C excluded from monthly exception.
required=[4,3,3,2,1];actual=[4,4,2,3,3];quality=[2<=4,11<=10,70<=100,True,2<=4];passes=[f>=r and ok for f,r,ok in zip(actual,required,quality)];assert passes==[True,False,False,True,True];proof['15']={'passes':passes,'requiredFrequency':required,'actual':actual,'quality':quality,'exception':'general bacteria explicitly excluded from monthly relaxation'}
keys={}
with pdfplumber.open(next((R/'artifacts/psat600_20261028/sources/3982').glob('*.pdf'))) as pdf:
 t=next(p.extract_text() for p in pdf.pages if '영역 상황판단' in p.extract_text());assert '2021년도' in t and '나 책형' in t
 for line in t.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
   v=list(map(int,line.split()));keys.update(zip(v[::2],v[1::2]))
assert len(keys)==25 and [keys[n] for n in range(6,16)]==[1,1,3,2,3,2,5,3,4,3]
norm=lambda s:re.sub(r'[\s·․]+','',s.replace('m²','m2'))
ts=json.loads((A/'table-sources.json').read_text(encoding='utf-8'))
for q in bank:
 n=q['number'];raw=(A/f'2021-s{n}-source.txt').read_text(encoding='utf-8');prompt,tail=raw.split('?',1);body,opts=tail.rsplit('\n① ',1);choices=re.split('[①②③④⑤]','① '+opts)[1:]
 for part in ts[str(n)]:assert part in body;body=body.replace(part,'')
 if n==12:body=body.rsplit('\n첫째 둘째 셋째',1)[0]
 assert norm(q['prompt'])==norm(prompt+'?') and norm(q['body'])==norm(body),(n,'body')
 assert len(choices)==5 and all(norm(a)==norm(b) for a,b in zip(q['choices'],choices)),(n,'choice')
 assert q['answer']==keys[n] and len(q['steps'])==len(q['optionReasons'])==5
 for s,prefix in zip(q['steps'],['착안점: ','실전 풀이: ','답 확정 기준: ','정석 근거: ','적용 한계: ']):assert s.startswith(prefix) and len(s)>40
 assert not any('\ue000'<=c<='\uf8ff' or c in '\ufffd\u2060\u2024' for c in json.dumps(q,ensure_ascii=False))
 for tab in q['tables']:assert 0<=tab['afterParagraph']<len(q['body'].split('\n\n'))
source=next((R/'artifacts/psat600_20261028/sources/3977/pdf').glob('*상황*'))
with pdfplumber.open(source) as pdf:
 for q in bank:
  n=q['number'];p=pdf.pages[(n-1)//2];s=(n-1)%2;m=p.width/2;tb=p.crop((m*s,43,m*(s+1),p.height-15)).extract_tables()
  if n in [6,12,13]:
   assert [[norm(x) for x in row] for row in q['tables'][0]['rows']]==[[norm(x) for x in row] for row in tb[0][1:]]
   assert [norm(x) for x in q['tables'][0]['columns']]==[norm(x) for x in tb[0][0]]
  if n==14:
   for target,src in zip(q['tables'],tb):assert target['rows']==src[2:]
   assert q['tables'][0]['columns']==['사업자']+tb[0][1][1:];assert q['tables'][1]['columns']==['사업자','과태료 부과']+tb[1][1][2:]
  if n==15:
   assert [[norm(x) for x in row] for row in q['tables'][1]['rows']]==[[norm(x) for x in row] for row in tb[1][1:]]
   assert q['tables'][1]['columns']==tb[1][0]
   # Wavy bottom border prevents automatic extraction of the last row; recover full two text rows directly.
   lines=ts['15'][0].strip().splitlines();assert lines[0]=='항목 기준 항목 기준' and len(lines)==3
   r=q['tables'][0]['rows'];assert norm(' '.join(sum(r[:2],[])))==norm(lines[1]) and norm(' '.join(sum(r[2:],[])))==norm(lines[2])
 for c in json.loads((A/'crop-manifest.json').read_text(encoding='utf-8')):
  assert hashlib.sha256(source.read_bytes()).hexdigest()==c['sha256'];ref=pdf.pages[c['page1based']-1].crop(c['rect']).to_image(resolution=c['resolution'],antialias=True).original.convert('RGB');path=R/c['asset'] if P.exists() else A/'staged'/c['asset'];im=Image.open(path).convert('RGB');assert im.size==ref.size and ImageChops.difference(im,ref).getbbox() is None
seen=set();old=0
for path in (R/'assets/psat').glob('*.json'):
 if path.name in ['sets.json','situation09.json']:continue
 obj=json.loads(path.read_text(encoding='utf-8'))
 if isinstance(obj,list):
  for q in obj:
   k=(q.get('examDate',q['source'][:10].replace('.','-')),q['subject'],q['number']);assert k not in seen;seen.add(k);old+=1
for q in bank:
 k=(q['examDate'],q['subject'],q['number']);assert k not in seen;seen.add(k)
for path,digest in json.loads((A/'before-situation09-hashes.json').read_text(encoding='utf-8')).items():
 if path!='assets/psat/sets.json':assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
proof.update(status='PASS',count=10,officialFinalKeys=10,nativeTables=7,sourceComparison='allnativeprompt/body/options;7PDFtables including wavy-border row;10originalpixelcomparisons',preservedExisting=old,limitations='Same-author review plus separate exact/exhaustive models;not independent expert certification.')
(A/'content-checks.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PASS10source/finalkey;7tables;10originals;exhaustive/exactmodels;preserved',old)
