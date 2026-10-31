
from pathlib import Path
from itertools import product,combinations
from fractions import Fraction as F
import json,re,hashlib,math
import pdfplumber
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/situation03_2024';P=R/'assets/psat/situation03.json'
bank=json.loads((P if P.exists() else A/'authored-situation03.json').read_text(encoding='utf-8'))
checks={}
def add(n,answer,proof):
 q=bank[n-11];assert q['number']==n and q['answer']==answer
 checks[str(n)]={'answer':answer,'proof':proof}
add(11,1,{'sourceClauses':'第1条4項但書+1号: fraudulent designation MUST cancel; other grounds MAY cancel/suspend; establishment=nation only; individuals eligible for overseas support','options':[True,False,False,False,False]})
sheets=[math.ceil(2/1),math.ceil(34/2),math.ceil(5/4),math.ceil(3/2)]
assert sheets==[2,17,2,2] and sum(sheets)==23
add(12,4,{'pagesPerSheet':[1,2,4,2],'sheets':sheets,'total':sum(sheets)})
assert 'Jon'<'Thor' and 'Stefan'+'s'+'son'=='Stefansson' and 'Jon'+'s'+'dottir'=='Jonsdottir'
add(13,3,{'options':[False,False,True,False,False],'names':['Jon','Thor'],'fatherNameNotPatronym':True})
remaining=[1,3,4,6,7,9,10];assignments=[]
for c in combinations(remaining,3):
 a=tuple(x for x in remaining if x not in c)
 if max(c)<min(a):assignments.append((a,c))
assert assignments==[((6,7,9,10),(1,3,4))]
a,c=assignments[0];b=(2,5,8)
teams=lambda rank:'A' if rank in a else 'B' if rank in b else 'C'
reps=min(x for x in combinations(range(1,11),4) if set(map(teams,x))==set('ABC'))
assert reps==(1,2,3,6)
statements=[teams(1)=='C',max(a)==9,max(reps)==7,teams(3)==teams(4)]
assert statements==[True,False,False,True]
add(14,3,{'assignments':assignments,'representatives':reps,'statements':statements})
a_l,b_l=200,100;x_l,y_l=a_l,2*a_l
assert x_l*1+y_l*2==1000
costs={z:F(1000)+4*z+3*(200-z) for z in range(201)}
assert min(costs.values())==1600 and costs[0]==1600
add(15,5,{'fixedX':x_l,'fixedY':y_l,'BrawLitres':200,'BcostFormula':'600+z, 0<=z<=200; nonnegative z gives continuous minimum at zero','totalMin':1600})
valid=[]
for n in range(4,15):
 for seq in product([-1,1],repeat=n):
  diffs=[];d=0
  for point in seq:d+=point;diffs.append(d)
  if diffs[-1]==2 and all(abs(x)<2 for x in diffs[:-1]):valid.append((seq,diffs))
assert valid and all(len(s)%2==0 and s[-2]==1 and d[-3]==0 for s,d in valid)
assert any(s[-4]==-1 for s,d in valid)
assert ( (-1,1,1,1),[-1,0,1,2]) in valid
add(16,5,{'finiteValidSequences':len(valid),'range':'n=4..14, supplementary to last-two-games and parity proofs','statements':[False,False,True,True],'witness':['乙','甲','甲','甲']})
scores=[100,50,30,20,10,8,6,4,2,1]
ties=[(r+1,k,F(sum(scores[r:r+k]),k)) for k in [2,3] for r in range(11-k)]
solutions=[]
for r1,r2 in product(range(1,11),repeat=2):
 for rank,k,points in ties:
  if scores[r1-1]+scores[r2-1]+points==157:solutions.append((r1,r2,rank,k,points))
assert solutions==[(1,2,6,2,F(7)),(2,1,6,2,F(7))]
ordinary_without100=scores[1:];sums={a+b for a,b in product(ordinary_without100,repeat=2)}
assert 97 not in sums and 82 not in sums
assert {v for _,_,v in ties if v>=57}=={F(60),F(75)}
add(17,2,{'allExactRationalCombinations':len(scores)**2*len(ties),'solutions':[list(map(str,s)) for s in solutions],'rankSum':9,'noOrdinary100Proof':'only joint60 or75 can cover >=57 deficit; ordinary97 or82 impossible'})
# Bit0 mail, bit1 notice, bit2 approval, bit3 inquiry; set bits mean unavailable.
models=[]
for ga,eul,byeong,jeong in product(range(1,16),repeat=4):
 if ga.bit_count()!=2 or not(ga&4):continue
 if ga&(eul|byeong|jeong):continue
 if ((byeong|jeong)&eul)!=(byeong|jeong):continue
 if byeong&8 or byeong&2 or not(jeong&2):continue
 models.append((ga,eul,byeong,jeong))
assert models==[(12,3,1,2),(12,3,1,3)]
for ga,eul,byeong,jeong in models:
 opts=[bool(ga&2),bool(eul&1),4-eul.bit_count()==2,not(jeong&8),bool((~ga&~byeong)&15)]
 assert opts==[False,True,True,True,True]
add(18,1,{'allPossibleUnavailabilityMasks':models,'totalAssignmentsEnumerated':15**4,'unknown':'丁 mail remains undecided','options':[False,True,True,True,True]})
h=F(240+220,2);delta=F(240-220,2)
assert h==230 and delta==10
witness=160,170
assert h+witness[1]-witness[0]==240 and h+witness[0]-witness[1]==220 and all(x<=h for x in witness)
add(19,3,{'height':str(h),'bMinusA':str(delta),'validWitness':witness,'absoluteValueSign':'0<=a,b<=H ensures upper-floor head not lower'})
orgs=[('A',30,'공연',F('1.8'),F('5.5')),('B',28,'교육',F('2'),F('4')),('C',27,'공연',F('3'),F('3')),('D',33,'교육',F('.8'),F('5'))]
eligible=sorted([o for o in orgs if o[1]<30 or o[3]<1],key=lambda o:-o[1]);remaining=F(4);paid={};calculated={}
for name,persons,kind,op,project in eligible:
 amount=op*(F('.5') if kind=='교육' else F('.2'))+project*(F('.2') if kind=='교육' else F('.5'))
 calculated[name]=amount;paid[name]=min(amount,remaining);remaining-=paid[name]
assert paid=={'D':F('1.4'),'B':F('1.8'),'C':F('.8')} and remaining==0
add(20,4,{'order':list(paid),'calculated':{k:str(v) for k,v in calculated.items()},'paid':{k:str(v) for k,v in paid.items()},'budget':4})
with pdfplumber.open(R/'artifacts/psat600_20261028/sources/4564/BBSMSTR_000000000138_4564_1.pdf') as pdf:
 text=pdf.pages[1].extract_text();assert '상황판단' in text and '사책형' in text and '2024년도' in text
 keys={}
 for line in text.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
   vals=list(map(int,line.split()));keys.update(zip(vals[::2],vals[1::2]))
 assert len(keys)==25
norm=lambda s:re.sub(r'\s+','',s)
for q in bank:
 n=q['number'];assert q['answer']==keys[n],(n,q['answer'],keys[n])
 raw=(A/f'q{n}-source.txt').read_text(encoding='utf-8')
 prompt,tail=raw.split('.',1)[1].strip().split('?',1);body,options=tail.rsplit('\n① ',1)
 if n==12:
  body,table=body.split('\n종류 유형',1)
  assert q['tables'][0]['rows']==[['A','보도자료','2','상'],['B','보도자료','34','중'],['C','보도자료','5','하'],['D','설명자료','3','상']]
  assert norm('종류 유형'+table)==norm('종류 유형 쪽수 중요도 A 보도자료 2 상 B 보도자료 34 중 C 보도자료 5 하 D 설명자료 3 상')
 if n==15:
  body,table=body.split('\n원료 X',1)
  assert norm('원료 X'+table)==norm('원료 X Y Z W 가격(만 원/리터) 1 2 4 3')
  assert q['tables'][0]['rows']==[['X','1'],['Y','2'],['Z','4'],['W','3']]
 if n==17:
  before,rest=body.split('\n순위 점수',1);table,after=rest.split('\n만약 어떤 순위',1)
  assert norm('순위 점수'+table)==norm('순위 점수 순위 점수 1 100 6 8 2 50 7 6 3 30 8 4 4 20 9 2 5 10 10 1')
  body=before+'\n만약 어떤 순위'+after
  assert q['tables'][0]['rows']==[[str(i+1),str(v)] for i,v in enumerate(scores)]
  assert q['tables'][0]['afterParagraph']==0 and q['body'].split('\n\n')[1].startswith('만약 어떤 순위')
 if n==20:
  body,table=body.split('\n단체 인원',1)
  assert norm('단체 인원'+table)==norm('단체 인원(명) 사업분야 운영비(억 원) 사업비(억 원) A 30 공연 1.8 5.5 B 28 교육 2.0 4.0 C 27 공연 3.0 3.0 D 33 교육 0.8 5.0')
  assert q['tables'][0]['rows']==[[o[0],str(o[1]),o[2],format(float(o[3]),'.1f'),format(float(o[4]),'.1f')] for o in orgs]
 assert norm(q['prompt'])==norm(prompt+'?'),(n,'prompt')
 assert norm(q['body'])==norm(body),(n,'body')
 opts=re.split('[①②③④⑤]','① '+options)[1:];assert len(opts)==len(q['choices'])==5
 for i,(x,y) in enumerate(zip(opts,q['choices'])):assert norm(x)==norm(y),(n,'choice',i)
 assert len(q['steps'])==len(q['optionReasons'])==5
 for s,prefix in zip(q['steps'],['착안점: ','실전 풀이: ','답 확정 기준: ','정석 근거: ','적용 한계: ']):assert s.startswith(prefix) and len(s)>30
 assert all(len(s)>20 for s in q['optionReasons']) and q['pitfall'] and q['transfer']
 assert not any(c in json.dumps(q,ensure_ascii=False) for c in ['\u2060','\ufffd'])
 assert (R/q['original'] if P.exists() else A/'staged'/q['original']).exists()
baseline=json.loads((A/'before-situation03-hashes.json').read_text(encoding='utf-8'))
for path,digest in baseline.items():
 if path=='assets/psat/sets.json':continue
 assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
checks.update(status='PASS',count=10,officialFinalKeys=10,choiceReasons=50,sourceTextAndTables='normalized exact match; 4 tables separately mapped',limitations='Same-author review plus exact/finitely-enumerated verification; not independent expert audit.')
(A/'content-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
print('PASS: situation11-20 original text/options/4 tables, official keys, exact calculations and exhaustive discrete models.')
