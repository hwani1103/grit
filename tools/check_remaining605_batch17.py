"""Source/table/key fidelity and complete finite numeric witnesses for batch17."""
from pathlib import Path
from itertools import combinations,permutations
from fractions import Fraction as F
import json,re
import pdfplumber
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/psat_remaining605_20261030';B=OUT/'batch17'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
norm=lambda s:re.sub(r'[\s①②③④⑤ㆍ·․「」『』\uf000\uf001/]','',s.translate(str.maketrans({'²':'2','＝':'=','＋':'+'})))
expected={
4:[dict(columns=['기업','2020년도 총매출(억 원)','소요 광고비(억 원)','사업분야'],rows=[['A','600','1','백신'],['B','500','2','비대면'],['C','400','3','농산물'],['D','300','4','인공지능'],['E','200','5','비대면'],['F','100','6','의류'],['G','30','4','백신']],after=4,native='2020년도 소요 광고비 기업 사업분야 총매출(억 원) (억 원) A 600 1 백신 B 500 2 비대면 C 400 3 농산물 D 300 4 인공지능 E 200 5 비대면 F 100 6 의류 G 30 4 백신')],
6:[dict(columns=['기획력','창의력','추진력','통합력'],rows=[['90','100','110','60']],after=3,native='기획력 창의력 추진력 통합력 90 100 110 60')],
12:[dict(columns=['구분','벽돌','나무','지푸라기'],rows=[['1개당 가격(원)','6,000','3,000','1,000'],['1m²당 필요 개수','15','20','30']],after=2,native='구 분 벽돌 나무 지푸라기 1개당 가격(원) 6,000 3,000 1,000 1m2당 필요 개수 15 20 30')],
15:[dict(columns=['항목','기준'],rows=[['대장균','불검출/100mL'],['일반세균','100CFU/mL 이하'],['잔류염소','4mg/L 이하'],['질산성 질소','10mg/L 이하']],after=11,native='항목 기준 항목 기준 대장균 불검출/100mL 일반세균 100CFU/mL 이하 잔류염소 4mg/L 이하 질산성 질소 10mg/L 이하'),dict(columns=['검사지점','검사대상','검사결과','검사빈도'],rows=[['정수장 A','잔류염소','2mg/L','매일 1회'],['정수장 B','질산성 질소','11mg/L','매일 1회'],['정수장 C','일반세균','70CFU/mL','매월 1회'],['수도꼭지 D','대장균','불검출/100mL','매주 1회'],['배수지 E','잔류염소','2mg/L','매주 1회']],after=12,native='검사지점 검사대상 검사결과 검사빈도 정수장 A 잔류염소 2mg/L 매일 1회 정수장 B 질산성 질소 11mg/L 매일 1회 정수장 C 일반세균 70CFU/mL 매월 1회 수도꼭지 D 대장균 불검출/100mL 매주 1회 배수지 E 잔류염소 2mg/L 매주 1회')]}
sources={x['id']:x for x in read(B/'blind-source.json')};solves={x['id']:x for x in read(B/'own-solves.json')};checks=[]
for row in read(B/'revealed-current.json'):
 q=row['question'];m=sources[q['id']];native=norm(re.sub(r'^.*?\b'+str(q['number'])+r'[.]\s*','',m['sourceText'],count=1,flags=re.S))
 for i,t in enumerate(expected.get(q['number'],[])):
  table=q['tables'][i];assert table['columns']==t['columns'] and table['rows']==t['rows'] and table['afterParagraph']==t['after']
  assert native.count(norm(t['native']))==1,(q['id'],'source table',i);native=native.replace(norm(t['native']),'',1)
 if q['number']==12:
  assert native.count(norm('첫째 둘째 셋째'))==1;native=native.replace(norm('첫째 둘째 셋째'),'',1)
 expectedText=norm(q['prompt']+q['body']+''.join(q['choices']))
 if native!=expectedText:
  i=next((i for i,(a,b) in enumerate(zip(native,expectedText)) if a!=b),min(len(native),len(expectedText)))
  raise AssertionError((q['id'],i,native[max(0,i-25):i+120],expectedText[max(0,i-25):i+120]))
 with pdfplumber.open(ROOT/row['officialKey']) as pdf:
  pi,t=next((i+1,p.extract_text()) for i,p in enumerate(pdf.pages) if '영역 상황판단' in (p.extract_text() or ''))
 assert q['examDate'][:4] in t and f"책형 {q['book']}" in t
 answers={}
 for line in t.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
   z=list(map(int,line.split()));answers.update(zip(z[::2],z[1::2]))
 assert answers[q['number']]==q['answer']==solves[q['id']]['answer']
 checks.append(dict(id=q['id'],source=m['source'],sourcePage=m['page'],nativeTextAndFiveChoicesMatch=True,tables=len(expected.get(q['number'],[])),key=row['officialKey'],keyPage=pi,answer=q['answer']))

companies=[('A',600,1,True),('B',500,2,True),('C',400,3,False),('D',300,4,True),('E',200,5,True),('F',100,6,False),('G',30,4,True)]
order=sorted([v for v in companies if v[1]<500],key=lambda v:(not v[3],v[1]*v[2]));assert [v[0] for v in order]==list('GEDFC')
balance=F(6);awards={}
for name,sales,ads,priority in order:
 award=min(F('2.4') if sales<=100 else F('1.2'),F(ads,2),balance);awards[name]=award;balance-=award
assert awards==dict(G=F(2),E=F('1.2'),D=F('1.2'),F=F('1.6'),C=F(0)) and balance==0

efforts=[]
for p in range(101):
 for c in range(101-p):
  for r in range(101-p-c):
   t=100-p-c-r;values=[360+3*p,400+3*c,440+3*r,240+3*t]
   if values[3]>max(values[:3]):efforts.append((p,c,r,t))
assert min(e[3] for e in efforts)==67 and (20,13,0,67) in efforts
assert 240+3*66<=440<240+3*67

sums=[35,39,44,45,50,54];weights=[]
for ascending in combinations(range(1,54),4):
 if sum(ascending)!=89:continue
 if sorted(a+b for a,b in combinations(ascending,2))==sums:weights.append(list(reversed(ascending)))
assert weights==[[30,24,20,15]]
halfWeights=[F('29.5'),F('24.5'),F('20.5'),F('14.5')]
assert sorted(a+b for a,b in combinations(halfWeights,2))==sums
assert F(6,5)*10==12

doneC=F(2,3);doneA=(1-doneC)/2;doneD=1-doneA;doneB=2*(1-doneD);doneE=(1-doneB)/2
done=dict(A=doneA,B=doneB,C=doneC,D=doneD,E=doneE)
assert done==dict(A=F(1,6),B=F(1,3),C=F(2,3),D=F(5,6),E=F(1,3))
assert sorted(done,key=done.get,reverse=True)[1]=='C'

allocations=[]
for a in range(1,31):
 for b in range(1,31):
  c=26-a-b
  if b>a>c>4:allocations.append((a,b,c,4))
assert max(v[2] for v in allocations)==7 and (9,10,7,4) in allocations and (8,11,7,4) in allocations
assert 3*8+7==31>30 # 31 is the exact minimum at8, not strictly above31.

area=[6,3,2];variable=dict(brick=9,wood=6,straw=3);fixed=dict(brick=0,wood=20,straw=5)
costs={name:[v*variable[name]+fixed[name] for v in area] for name in variable}
house=[]
for materials in permutations(variable):
 price=[costs[name][i] for i,name in enumerate(materials)]
 if price[1]>max(price[0],price[2]):house.append((materials,price))
assert house==[(('straw','wood','brick'),[23,38,18])]

quality=[2<=4,11<=10,70<=100,True,2<=4];requiredRank=[0,1,1,2,3];observedRank=[0,0,2,1,1]
passes=[quality[i] and observedRank[i]<=requiredRank[i] for i in range(5)]
assert passes==[True,False,False,True,True]
qualitative={'s02':'Clear role edges: manager orders custodian; custodian reports manager; manager requests contracting officer. Other-agency delegation and outside-storage exception have specified subjects.', 's03':'Mail inspection sanction is imprisonment AND disqualification; phone identifier provision sanction differs and legitimate activation is an exception. Own conversation not covered by other-parties rule; no broader evidence-law claim.'}
result=dict(status='PASS',count=10,sourceKeyTables=checks,allocationOrder=[v[0] for v in order],awards={k:str(v) for k,v in awards.items()},effortFeasibleCount=len(efforts),minimumIntegrationEffort=67,effortWitness=[20,13,0,67],integerWeightSolutions=weights,nonintegerWeightSolution=list(map(str,halfWeights)),clockElapsedSeconds=12,completedWork={k:str(v) for k,v in done.items()},performanceFeasibleAllocations=allocations,maximumBing=7,atEightExactMinimumTotal=31,houseSolution=house,waterPasses=passes,qualitative=qualitative,limitations='Same-author original-source solving. Native table data/placement checked; qualitative regulation reasoning scoped to given hypothetical text. No device/APK.')
(B/'source-key-model-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PASS10 direct sources/keys;five native tables;complete effort/weight/performance/house models and strict boundary witnesses.')
