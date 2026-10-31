from pathlib import Path
import json,re,hashlib,itertools,pdfplumber
from fractions import Fraction as F
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/situation08';P=R/'assets/psat/situation08.json';bank=json.loads((P if P.exists() else A/'authored-situation08.json').read_text(encoding='utf-8'))
def norm(s):return re.sub(r'[\s·․]+','',s)
keys={}
for y,post,book in [(2025,'5994','인'),(2021,'3982','나')]:
 with pdfplumber.open(next((R/f'artifacts/psat600_20261028/sources/{post}').glob('*.pdf'))) as pdf:
  text=next(p.extract_text() for p in pdf.pages if '영역 상황판단' in p.extract_text());assert f'{y}년도' in text and f'{book} 책형' in text;key={}
  for line in text.splitlines():
   if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
    v=list(map(int,line.split()));key.update(zip(v[::2],v[1::2]))
  assert len(key)==25;keys[y]=key
for q in bank:
 y=int(q['examDate'][:4]);n=q['number'];raw=(A/f'{y}-s{n}-source.txt').read_text(encoding='utf-8').split(f'{n}.',1)[1];prompt,tail=raw.split('?',1);body,opts=tail.rsplit('\n① ',1)
 if (y,n) in [(2025,24),(2021,4)]:
  tb=(A/f'{y}-s{n}-table-source.txt').read_text(encoding='utf-8');assert tb in body;body=body.replace(tb,'')
 if (y,n)==(2021,5):body=body.rsplit('\n㉠ ㉡',1)[0];assert q['choiceNote']=='선택지의 순서: ㉠ 최소 → ㉡ 최대'
 assert norm(q['prompt'])==norm(prompt+'?'),(y,n,'prompt')
 assert norm(q['body'])==norm(body),(y,n,'body')
 options=re.split('[①②③④⑤]','① '+opts)[1:];assert len(options)==5 and all(norm(a)==norm(b) for a,b in zip(options,q['choices'])),(y,n,'options')
 assert q['answer']==keys[y][n],(y,n,'key');assert len(q['steps'])==len(q['optionReasons'])==5
 for s,prefix in zip(q['steps'],['착안점: ','실전 풀이: ','답 확정 기준: ','정석 근거: ','적용 한계: ']):assert s.startswith(prefix) and len(s)>40
 assert (R/q['original'] if P.exists() else A/'staged'/q['original']).exists()
 assert not any('\ue000'<=c<='\uf8ff' or c in '\ufffd\u2060' for c in json.dumps(q,ensure_ascii=False))
for idx,post,pg in [(3,'6008',11),(8,'3977',1)]:
 with pdfplumber.open(next((R/f'artifacts/psat600_20261028/sources/{post}/pdf').glob('*상황*'))) as pdf:
  p=pdf.pages[pg];tb=p.crop((p.width/2,43,p.width,p.height-15)).extract_tables()[0]
  assert [[norm(v) for v in row] for row in tb[1:]]==[[norm(v) for v in row] for row in bank[idx]['tables'][0]['rows']]
  assert [norm(v) for v in tb[0]]==[norm(v) for v in bank[idx]['tables'][0]['columns']]
# Independent timed inventory simulation: fresh daily, Monday drop before pickup.
def shirts(n):
 clean=n;dirty=0;wear=0;queue={}
 for d in range(365):
  dirty+=wear;wear=0
  if clean==0:return False,d
  clean-=1;wear=1
  if d%7==0:
   queue[d+7]=dirty;dirty=0
   clean+=queue.pop(d,0)
 return True,None
shirt_results={n:shirts(n) for n in [7,8,14,15,16]};assert [shirt_results[n][0] for n in shirt_results]==[False,False,False,True,True]
# Four distinct cards, no transitive rule.
wins={('사자','얼룩말'),('불곰','사자'),('얼룩말','하이에나'),('하이에나','사자')}
def result(a,b):return 1 if (a,b) in wins else -1 if (b,a) in wins else 0
models=[x for x in itertools.permutations(['사자','불곰','얼룩말','하이에나']) if result(x[0],x[3])==-1 and result(x[1],x[3])==1 and result(x[2],x[3])==0]
assert len(models)==2 and all(x[2]=='불곰' for x in models)
assert set(models)=={('하이에나','사자','불곰','얼룩말'),('사자','얼룩말','불곰','하이에나')}
tickets=[(a,b) for a in range(14) for b in range(11) if 4500*a+5500*b==59000];assert tickets==[(7,5)]
# Six days determine all seven days' germination, day7 weather irrelevant.
weather=[]
for w in itertools.product('SR',repeat=6):
 def first(pred):
  return next((d+1 for d in range(1,7) if pred(d)),99)
 dates={'A':first(lambda d:d>=2 and w[d-2:d]==('S','S')),'B':first(lambda d:w[d-1]=='S'),'C':first(lambda d:w[:d].count('R')>=3),'D':first(lambda d:d>=2 and w[d-2:d]==('R','R'))}
 if [list(dates.values()).count(d) for d in range(1,8)]==[0,1,0,1,0,1,1]:weather.append((w,dates))
assert len(weather)==1 and weather[0][1]=={'A':6,'B':2,'C':7,'D':4}
# Enumerate all previous last-review rankings and quarterly result assignments.
depts=set(range(5));Q1={0,1,4};reviewmodels=[]
def next_review(fails,last):
 selected=set(fails)
 for j in sorted(depts-selected,key=lambda j:last[j]):
  if len(selected)>=3:break
  selected.add(j)
 return selected
for history in itertools.permutations(range(-5,0)):
 last=list(history)
 for j in Q1:last[j]=1
 for fail1bits in itertools.product([False,True],repeat=2):
  fail1={j for j,v in zip([0,4],fail1bits) if v};Q2=next_review(fail1,last)
  if 3 in Q2 or 4 not in Q2:continue
  last2=last.copy()
  for j in Q2:last2[j]=2
  for mask in itertools.product([False,True],repeat=len(Q2)):
   fail2={j for j,v in zip(sorted(Q2),mask) if v};Q3=next_review(fail2,last2)
   if 3 in Q3 or 4 not in Q3:continue
   for mask3 in itertools.product([False,True],repeat=len(Q3)):
    fail3={j for j,v in zip(sorted(Q3),mask3) if v}
    if len(Q3-fail3)!=3:continue
    reviewmodels.append((len(fail1),len(fail2),len(fail3)))
assert reviewmodels and set(reviewmodels)=={(2,3,0)}
# Eligibility/order/caps/budget separate.
firms=[('A',600,1,True),('B',500,2,True),('C',400,3,False),('D',300,4,True),('E',200,5,True),('F',100,6,False),('G',30,4,True)]
eligible=sorted((x for x in firms if x[1]<500),key=lambda x:(not x[3],x[1]*x[2]));remaining=F(6);pays={}
for name,sales,ad,priority in eligible:
 pay=min(F(12,5) if sales<=100 else F(6,5),F(ad,2),remaining);pays[name]=pay;remaining-=pay
assert [x[0] for x in eligible]==['G','E','D','F','C'] and pays['F']==F(8,5) and remaining==0
teams=[(a,b,c) for a,b,c in itertools.product(range(1,11),repeat=3) if a+b+c==10 and 5*a+6*b+7*c==57];assert teams==[(4,5,1),(5,3,2),(6,1,3)]
seen=set();old=0
for p in (R/'assets/psat').glob('*.json'):
 if p.name in ['sets.json','situation08.json']:continue
 obj=json.loads(p.read_text(encoding='utf-8'))
 if isinstance(obj,list):
  for q in obj:
   k=(q.get('examDate',q['source'][:10].replace('.','-')),q['subject'],q['number']);assert k not in seen;seen.add(k);old+=1
for q in bank:
 k=(q['examDate'],q['subject'],q['number']);assert k not in seen;seen.add(k)
for path,digest in json.loads((A/'before-situation08-hashes.json').read_text(encoding='utf-8')).items():
 if path!='assets/psat/sets.json':assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
proof={'status':'PASS','count':10,'officialFinalKeys':10,'sourceComparison':'all prompt/body/options;2tables PDFcells;3laws;min/max columns preserved','shirts365days':shirt_results,'cardsTwoModels':models,'tickets':tickets,'weather':weather,'quarterlyModels':len(reviewmodels),'quarterlyFailCounts':[2,3,0],'subsidy':{k:str(v) for k,v in pays.items()},'teams':teams,'preservedExisting':old,'limitations':'Same-author verification,not independent expert certification.'}
(A/'content-checks.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PASS10 source/key;2tables;365dayinventory;2cardmodels;64weather;quarterlyrankings;budget;teams;preserved',old)
