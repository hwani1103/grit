from pathlib import Path
from fractions import Fraction as F
from itertools import permutations
import json,re,hashlib
import pdfplumber
from PIL import Image
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/data04';P=R/'assets/psat/data04.json';bank=json.loads((P if P.exists() else A/'authored-data04.json').read_text(encoding='utf-8'))
checks={}
def note(y,n,key,evidence):
 q=next(q for q in bank if q['examDate'].startswith(str(y)) and q['number']==n);assert q['answer']==key;checks[f'{y}-{n}']=evidence
assert 1990+550==2540<2350+540==2890
assert F(400000000)*F(48,10000)==1920000<2000000
assert F(10000000000)*F(127,10000)==127000000<10*(F(1000000000)*F(120,10000)+3250000)
note(2023,20,1,{'statements':[True,False,False],'costsWon':[25400000,28900000,1920000,127000000,15250000]})
assert 219-62-47-21-21==68<4*21
electors=[110818,73381,32591,6818,2554];assert sum(electors)==226162
assert F(73381,62)>1000>F(32591,47)
assert F(25629*100,32591)>F(687,10) and F(25629*100,32591)<83
assert F(830-687,10)<15
voters=[106496,68213,36170,8210,2892];rates=[740,717,849,849,854]
intervals=[]
for v,r,e in zip(voters,rates,electors):
 # Published percentage rounded to one decimal: rate in[(r-.5)/1000,(r+.5)/1000).
 lo=F(v*2000,2*r+1)-e;hi=F(v*2000,2*r-1)-e;intervals.append((lo,hi))
assert all(intervals[i][0]>intervals[i+1][1] for i in range(4))
approx=[round(F(v*1000,r)-e) for v,r,e in zip(voters,rates,electors)]
assert approx==[33096,21756,10012,2852,832]
note(2023,21,3,{'statements':[False,False,True,True],'roundedDifferences':approx,'roundingSafeIntervals':[[float(a),float(b)] for a,b in intervals]})
occ=[[258,65,29,96,160],[250,46,38,119,162],[244,110,61,132,228],[277,108,69,128,203],[246,96,54,149,174]]
vict=[[35,20,25,3,60],[19,25,1,0,52],[10,19,0,16,52],[8,25,2,8,79],[9,27,3,3,76]]
rat=[F(v,c) for v,c in zip(vict[3],occ[3])];assert sorted(range(5),key=lambda i:rat[i],reverse=True)==[4,1,3,2,0]
assert [abs(a-b) for a,b in zip(vict[3],vict[4])]==[1,2,1,5,3]
valid=[]
for labels in permutations(['안전사고','전복','충돌','침몰','화재폭발']):
 idx={s:labels.index(s) for s in labels};safe,roll,crash,sink,fire=[idx[s] for s in ['안전사고','전복','충돌','침몰','화재폭발']]
 if not(occ[0][safe]<occ[1][safe]<occ[2][safe]):continue
 if roll!=1 or fire!=3:continue
 if not all(row[crash]>=2*row[roll] for row in occ):continue
 if not sum(row[sink] for row in vict)*2<=sum(row[safe] for row in vict):continue
 valid.append(labels)
assert valid==[('충돌','전복','침몰','화재폭발','안전사고')]
note(2023,22,1,{'permutations':120,'uniqueMapping':valid,'victimTotals':[sum(r[i] for r in vict) for i in range(5)]})
refusal17=4166-sum([1110,125,1001,123,241]);night18=4131-sum([1694,701,301,174,382]);night22=2067-sum([43,193,268,114,187])
tot20=sum([717,1128,51,769,2845,475]);tot21=sum([130,355,40,1214,1064,484])
assert [refusal17,night18,night22,tot20,tot21]==[1566,879,1262,5985,3287]
assert max([4166,4131,5354,tot20,tot21,2067])==tot20
assert 1566<125*13 and 717>51*14
note(2023,23,3,{'missingValues':[refusal17,night18,night22,tot20,tot21],'ratioCounterexample':'2017<13,2020>14','shareRise':'769/5985<1214/3287'})
pet=[[1840,1825,1979],[1795,1849,1982],[1801,1867,2006],[1807,1852,1979]]
diesel=[[1843,1852,2014],[1806,1894,2029],[1806,1885,2013],[1827,1895,2024]]
assert all(a<b<c for a,b,c in diesel)
gaps=[[diesel[i][j]-pet[i][j] for i in range(4)] for j in range(3)]
assert [max(range(4),key=lambda i:gaps[j][i]) for j in range(3)]==[3,1,1]
assert all(g>0 for g in gaps[0])
assert diesel[2][2]-diesel[2][1]==128<139==pet[2][2]-pet[2][1]
note(2023,24,4,{'dieselAllIncreasing':True,'monthlyFuelGaps':gaps,'CMayJune':[139,128]})
area=[924470,924291,906106,905034,903885]
assert [area[i-1]-area[i] for i in range(1,5)]==[179,18185,1072,1149]
barley=[128,166,177,180,98];rate=[F((v-128)*100,128) for v in barley[1:]]
shown=[F(297,10),F(383,10),F(406,10),F(-234,10)]
assert all(abs(a-b)<F(1,20) for a,b in zip(rate,shown))
amount=[143938,201,30740,10054,36338];shown=[F(651,10),F(1,10),F(139,10),F(45,10),F(164,10)]
assert sum(amount)==221271
assert all(abs(F(a*100,221271)-s)<F(1,20) for a,s in zip(amount,shown))
note(2024,21,4,{'statements':[True,False,True,True],'swapped2021':'잡곡 should30972;서류 should35576','baseArea':128,'pieRoundingErrorLessThan':0.05})
pops=[14056,23556,29204,21779,11224,16792,19163,27146,23813,29649,36326,15226]
old=[2790,3365,3495,3889,2300,2043,2469,4045,2656,5733,7596,2798]
female=[1501,None,3615,2614,1272,2754,3421,4533,4123,3046,3625,1725]
indices=[F(f,o) if f is not None else F(88,100) for f,o in zip(female,old)]
caution=[chr(65+i) for i,v in enumerate(indices) if F(1,2)<=v<1]
normal=[i for i,v in enumerate(indices) if 1<=v<F(3,2)]
assert caution==list('ABDEJL') and normal==[2,5,6,7]
assert max(range(12),key=lambda i:indices[i])==8 and min(range(12),key=lambda i:indices[i])==10
assert old[8]*10>=pops[8] and sum(pops[i] for i in normal)==92305
assert F(885,1000)*3365<3421 # includes upper rounding bound forB
note(2024,22,1,{'caution':caution,'normalPopulation':92305,'highest':'I','lowest':'K','BcomparisonRoundingSafe':True})
assert 291<F(15,100)*2270 and 403<870
assert F(286,1143)>F(1,5)>F(1,20)>F(1,21)
assert 870>F(3,4)*1106 and 447<F(9,10)*565
note(2024,23,3,{'optionTruth':[False,False,True,False,False],'strictShareBounds':'공공>20%,자가<5%'})
rates3=[[18.4,15.9,16.3],[22.6,15.9,12.8],[35.9,39.9,38.4],[33.3,36,38.1],[22.2,30.6,36],[28.1,47.7,35.8],[33,38.1,50.9],[7.7,16.7,0],[23.3,19.6,22.3],[21.4,14.1,18.2],[23.6,28.5,24.3],[26.7,19.9,23.1],[31.7,34,22.1],[36.2,34.5,23.8],[10.6,23.3,22.9],[18.5,25.7,12.4],[31.6,25.3,26.2]]
assert [i for i,(a,b,c) in enumerate(rates3) if a>b>c]==[1,13]
assert max(range(17),key=lambda i:rates3[i][2])==6
assert F(362*51,100)*F(3,2)==F(27693,100)<277<350
note(2024,24,4,{'statements':[True,True,False],'ulsanUpperBoundUsing51percent':184.62,'upperTimes1_5':276.93,'gyeonggiGraphLowerBound':350,'monotoneThrough2022':['부산','전남'],'graphProof':'京/서울/경남 bothaxesup;경북 oldx<400 oldy<100,newx>600;부산 oldtotal<=362,newx>400. Visual bounds, not invented exactcoordinates.'})
man=[15000,20000,30000,35000];assert sum(man)==4*25000 and F(man[1]+man[2],2)==25000
executiveMin=[24000,25600,25600,48000,48000,48000,48000,55000]
assert sum(executiveMin)==322200 and F(sum(executiveMin),8)==40275
assert 2+26+8+18==54
note(2024,25,5,{'statements':[True,True,True,False],'manager':man,'executiveMinimum':executiveMin,'meanLowerBound':40275,'countLowerBound':54,'equalityProof':'x4<=x5<=x6=48000 and x4+x5=96000 forces allthree48000'})
keys={}
for y,post,suffix,book in [(2023,4341,2,'인'),(2024,4564,1,'사')]:
 with pdfplumber.open(R/f'artifacts/psat600_20261028/sources/{post}/BBSMSTR_000000000138_{post}_{suffix}.pdf') as pdf:
  found=[p.extract_text() for p in pdf.pages if '영역 자료해석' in p.extract_text()];assert len(found)==1;t=found[0];assert str(y)+'년도' in t and book in t;ans={}
  for line in t.splitlines():
   if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
    v=list(map(int,line.split()));ans.update(zip(v[::2],v[1::2]))
  assert len(ans)==25;keys[y]=ans
norm=lambda s:re.sub(r'\s+','',s.replace(' / ',' '))
for q in bank:
 y=int(q['examDate'][:4]);n=q['number'];raw=(A/f'{y}-d{n}-source.txt').read_text(encoding='utf-8');t=raw.split(f'{n}.',1)[1]
 if (y,n)==(2023,24):t=t.split('\n25.',1)[0]
 prompt,tail=t.split('?',1);opt=tail.split('①',1)[1];choices=re.split('[①②③④⑤]','①'+opt)[1:]
 assert q['answer']==keys[y][n] and norm(q['prompt'])==norm(prompt+'?')
 assert len(choices)==len(q['choices'])==5
 for x,z in zip(choices,q['choices']):assert norm(x)==norm(z)
 assert len(q['steps'])==len(q['optionReasons'])==5
 for s,prefix in zip(q['steps'],['착안점: ','실전 풀이: ','답 확정 기준: ','정석 근거: ','적용 한계: ']):assert s.startswith(prefix) and len(s)>35
 assert (R/q['original'] if P.exists() else A/'staged'/q['original']).exists()
# Source pixel matching and crop boundary coverage: text inside a figure's section span must be fully included.
manifest=json.loads((A/'crop-manifest.json').read_text(encoding='utf-8'))
for item in manifest:
 source=R/item['source'];assert hashlib.sha256(source.read_bytes()).hexdigest()==item['sourceSHA256']
 with pdfplumber.open(source) as pdf:
  for f in item['figures']:
   im=pdf.pages[f['page1based']-1].crop(tuple(f['rect'])).to_image(resolution=f['resolution']).original.convert('RGB')
   actual=Image.open(R/f['asset'] if P.exists() else A/'staged'/f['asset']).convert('RGB')
   assert im.size==actual.size and im.tobytes()==actual.tobytes()
   # Words that touch the crop must not be cut, allowing tiny coordinate rounding.
   x0,y0,x1,y1=f['rect']
   for w in pdf.pages[f['page1based']-1].extract_words():
    if w['x1']<=x0 or w['x0']>=x1 or w['bottom']<=y0 or w['top']>=y1:continue
    assert w['x0']>=x0-.5 and w['x1']<=x1+.5 and w['top']>=y0-.5 and w['bottom']<=y1+.5,(f['asset'],'cutword',w['text'],w['top'],w['bottom'])
seen=set()
for path in (R/'assets/psat').glob('*.json'):
 if path.name in ['sets.json','data04.json']:continue
 obj=json.loads(path.read_text(encoding='utf-8'))
 if isinstance(obj,list):
  for q in obj:
   k=(q.get('examDate',q['source'][:10].replace('.','-')),q['subject'],q['number']);assert k not in seen;seen.add(k)
for q in bank:
 k=(q['examDate'],q['subject'],q['number']);assert k not in seen;seen.add(k)
for path,digest in json.loads((A/'before-data04-hashes.json').read_text(encoding='utf-8')).items():
 if path=='assets/psat/sets.json':continue
 assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
checks.update(status='PASS',count=10,officialFinalKeys=10,figures=24,limitations='Same-author visual review, exact fractions/bounds/enumeration. Not independent expert review; plotted bounds not exact point coordinates.')
(A/'content-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PASS:10 officialkeys,24 pixel-matched figures,rounding intervals,120 mappings,exact shares/quantile bounds;110existing preserved.')