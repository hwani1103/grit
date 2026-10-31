
from pathlib import Path
from fractions import Fraction as F
import json,re,hashlib
import pdfplumber
from PIL import Image
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/data03_2024';P=R/'assets/psat/data03.json'
bank=json.loads((P if P.exists() else A/'authored-data03.json').read_text(encoding='utf-8'));checks={}
def add(n,answer,proof):
 q=bank[n-11];assert q['answer']==answer
 checks[str(n)]={'answer':answer,'proof':proof}
assert sum([83,111,19])-sum([11,61,46])==95 and 1351>=3*437
raw=(A/'q11-source.txt').read_text(encoding='utf-8');cancellation=raw.split('<표 2>',1)[1].split('<보 기>',1)[0]
lines=cancellation.splitlines()
jan=[l for l in lines if re.fullmatch(r'1(?: 0){10}',l)]
mar=[l for l in lines if re.fullmatch(r'3(?: 0){10}',l)]
assert len(jan)==len(mar)==1
add(11,4,{'Q3DelayIncrease':95,'SepCancellationThreshold':1311,'allJanuaryMarchCancellations':0,'statements':[False,True,True]})
grad=[800,700,500];jobs=[500,400,200];education=[60,50,40]
assert F(500,800)>F(400,700)
assert 1-F(450,700)<1-F(240,500)
assert F(150,2000)*F('1.2')==F('.09')
assert F(1100,2000)*F('1.1')==F('.605')
assert F(40,500)>max(F(60,800),F(50,700))
add(12,3,{'newEducationRate':'9%','newEmploymentRate':'60.5%','options':[True,True,False,True,True]})
# Manually transcribed from source symbols after visual review.
cucumber={'촉성':{'sow':[11],'plant':[1,12],'harvest':[2,3,4,5]},'반촉성':{'sow':[1],'plant':[2],'harvest':[3,4,5,6]},'조숙':{'sow':[3],'plant':[4],'harvest':[5,6,7,8]},'보통':{'sow':[4],'plant':[5],'harvest':[6,7,8]},'억제':{'sow':[5],'plant':[6],'harvest':[7,8,9,10,11]}}
pepper={'촉성':{'sow':[10],'plant':[12],'harvest':[1,2,3,4,5]},'반촉성':{'sow':[11],'plant':[2],'harvest':[3,4,5,6,7]},'조숙':{'sow':[2],'plant':[4],'harvest':[5,6,7,8,9,10]},'보통':{'sow':[3],'plant':[5],'harvest':[6,7,8,9,10]},'억제':{'sow':[4],'plant':[6],'harvest':[7,8,9,10,11]}}
overlap=lambda crops:sorted(set(x for v in crops.values() for x in v['plant'])&set(x for v in crops.values() for x in v['harvest']))
assert overlap(cucumber)==overlap(pepper)==[2,4,5,6]
gaps=[(v['plant'][0]-v['sow'][0])%12 for v in pepper.values()]
assert gaps==[2,3,2,2,2]
harvest_counts={m:sum(m in v['harvest'] for v in pepper.values()) for m in range(1,13)}
assert [m for m,c in harvest_counts.items() if c==max(harvest_counts.values())]==[7]
assert min(cucumber,key=lambda k:len(cucumber[k]['harvest']))=='보통'
add(13,3,{'cucumber':cucumber,'pepper':pepper,'overlapBoth':[2,4,5,6],'pepperHarvestCounts':harvest_counts,'options':[True,True,False,True,True]})
seaweed=[781,837,853,880,812];oysters=[1292,1314,1317,1293,1277];cockles=[1076,1093,1096,1115,1121];clams=[570,587,576,582,565];kelp=[802,920,898,882,678];totals=[4521,4751,4740,4752,4453]
assert [sum(v) for v in zip(seaweed,oysters,cockles,clams,kelp)]==totals
pairs=[a+b for a,b in zip(oysters,cockles)];margins=[2*a-t for a,t in zip(pairs,totals)]
assert margins==[215,63,86,64,343] and min(pairs[1:])==2398 and max(totals[1:])==4752
assert F(17,570)>F(6,576)
assert [v[-1]>v[-2] for v in [seaweed,oysters,cockles,clams,kelp]]==[False,False,True,False,False]
add(14,2,{'pairTwiceMinusTotal':margins,'options':[False,True,False,False,False]})
imports={'A':[2201,400,348,416,453,102,3920],'B':[2245,453,346,400,416,120,3980],'C':[2264,416,400,346,453,106,3985],'D':[2022,322,346,416,400,40,3546],'E':[2010,346,322,400,416,142,3636]}
conditions={}
for name,v in imports.items():
 assert sum(v[:-1])==v[-1]
 conditions[name]=[v[-1]>=3358*F('1.1'),v[0]*2>=v[-1],v[2]>=11*30,v[4]==sorted(v[:-1],reverse=True)[1],v[3]>v[1],v[3]>315]
assert [k for k,v in conditions.items() if all(v)]==['A']
add(15,1,{'threshold':'3693.8','candidateConditions':conditions,'unverifiableFromTable':'imported share of domestic use 84%, no domestic-use denominator supplied'})
culture=[8,8,10,11,12,12];craft=[14,14,11,10,10,9];residents=[3,3,5,6,8,8];experience=[0,0,1,3,4,5];lodging=[2,2,1,0,0,0];totals=[27,27,28,30,34,34]
assert [sum(v) for v in zip(culture,craft,residents,experience,lodging)]==totals
assert F(min(culture),max(totals))>F(1,5)
assert F(5-3,3)==2*F(8-6,6)
assert [2017+i for i,(l,e) in enumerate(zip(lodging,experience)) if l>e]==[2017,2018]
add(16,5,{'blank2019Lodging':1,'blank2021Craft':10,'blank2022Experience':5,'statements':[False,True,True,True]})
foreign=[31205,28724,30375,40657,45042,51631,65073,57299,76446];shares=list(map(F,['2.8','2.0','1.4','1.8','1.4','1.6','1.9','3.5','1.7']))
parts=[F(a)*b/100 for a,b in zip(foreign,shares)]
assert parts[-1]>1275>896>parts[0]
opts=[parts[-1]>parts[0],shares[6]<shares[5],parts[3]>=1000,F(foreign[-1]-foreign[-2],foreign[-2])>=F('.4'),foreign[2]>foreign[1] and shares[2]>shares[1]]
assert opts==[True,False,False,False,False]
add(17,1,{'graphValues':foreign,'graphShares':[str(x) for x in shares],'computedParts':[str(x) for x in parts],'options':opts})
shops=[14737,14593,10294,4082,787];avg=[583999,603529,465042,414841,559684];density=[26089,32543,25483,12557,15448]
assert sum(shops)==44493 and 50000-sum(shops)==5507
assert 700*7+607==5507 and max(700,607)<787 and 5+8<14
revenue=[n*a for n,a in zip(shops,avg)];area=[F(r,d) for r,d in zip(revenue,density)]
assert revenue.index(max(revenue))==avg.index(max(avg))==1
assert F(shops[1],shops[0])>F('.99') and F(avg[1],avg[0])>F('1.03') and F('.99')*F('1.03')>1
assert F(avg[-1],density[-1])<40 and shops[-1]<800 and area[-1]<32000
assert all(a>48000 for a in area[:-1])
add(18,4,{'brandCounterexample':{'existing':5,'additionalSizes':[700]*7+[607],'totalBrands':13},'revenues':revenue,'areas':[str(a) for a in area],'statements':[False,True,True]})
capacity=[800,48,750,400,900];annual=[163785,12540,169781,104176,238770];workers=[66,34,75,65,74]
assert sum(capacity)==2898 and sum(annual)==689052 and sum(workers)==314
ratios=[F(a,c) for a,c in zip(annual,capacity)]
assert all(r<264 for r in ratios[:-1]) and ratios[-1]>264
assert annual[4]>annual[2] and workers[4]<workers[2]
assert annual[0]>annual[3]*F('1.5') and capacity[2]<sum(capacity)*F('.3') and 48*250<12540
add(19,2,{'ratios':[str(v) for v in ratios],'commonThreshold':264,'options':[False,True,False,False,False],'capacityIsUpperBound':True})
nation=[4397532,4374899,4046574,4456952,4331597];local=[223472,228111,203893,237439,221271]
nation_area=[924470,924291,906106,905034,903885];local_area=[46724,47446,46615,47487,46542]
production=[[153944,150901,127387,155501,143938],[270,369,398,392,201],[29942,23823,30972,33535,30740],[9048,10952,9560,10899,10054],[30268,42066,35576,37112,36338]]
areas=[[29006,28640,28405,28903,28708],[128,166,177,180,98],[6804,6239,6289,6883,6317],[5172,5925,5940,5275,5741],[5614,6476,5804,6246,5678]]
assert [sum(t) for t in zip(*production)]==local and [sum(t) for t in zip(*areas)]==local_area
decrease_local=F(local[-2]-local[-1],local[-2]);decrease_nation=F(nation[-2]-nation[-1],nation[-2])
assert decrease_local>F('.06')>F('.03')>decrease_nation
changes=[F(p[-1]-p[0],p[0]) for p in production]
assert max(range(5),key=lambda i:abs(changes[i]))==1
assert all(2*r>=t for r,t in zip(areas[0],local_area))
yields=[F(p[-1],a[-1]) for p,a in zip(production,areas)]
assert all(x<6 for x in yields[:-1]) and yields[-1]>6
sign=lambda v:(v>0)-(v<0)
assert [sign(b-a) for a,b in zip(local,local[1:])]==[sign(b-a) for a,b in zip(local_area,local_area[1:])]==[1,-1,1,-1]
add(20,1,{'decreaseLocal':str(decrease_local),'decreaseNation':str(decrease_nation),'signedChanges':[str(v) for v in changes],'changeMagnitudeMax':'맥류; change magnitude distinguished from signed growth','yield':[str(v) for v in yields],'options':[False,True,True,True,True]})
with pdfplumber.open(R/'artifacts/psat600_20261028/sources/4564/BBSMSTR_000000000138_4564_1.pdf') as pdf:
 text=pdf.pages[2].extract_text();assert '자료해석' in text and '사책형' in text and '2024년도' in text
 keys={}
 for line in text.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
   vs=list(map(int,line.split()));keys.update(zip(vs[::2],vs[1::2]))
 assert len(keys)==25
norm=lambda s:re.sub(r'\s+','',s)
for q in bank:
 n=q['number'];assert q['answer']==keys[n],(n,q['answer'],keys[n])
 raw=(A/f'q{n}-source.txt').read_text(encoding='utf-8')
 prompt=raw.split(f'{n}.',1)[1].split('?',1)[0]
 assert norm(q['prompt'])==norm(prompt+'?')
 options=re.split('[①②③④⑤]','① '+raw.rsplit('\n① ',1)[1])[1:]
 assert len(options)==len(q['choices'])==5
 for i,(x,y) in enumerate(zip(options,q['choices'])):assert norm(x)==norm(y),(n,i)
 assert len(q['steps'])==len(q['optionReasons'])==5 and all(len(r)>20 for r in q['optionReasons'])
 for s,prefix in zip(q['steps'],['착안점: ','실전 풀이: ','답 확정 기준: ','정석 근거: ','적용 한계: ']):assert s.startswith(prefix) and len(s)>30
 assert not any(c in json.dumps(q,ensure_ascii=False) for c in ['\u2060','\ufffd'])
 root=R if P.exists() else A/'staged'
 for fig in q['figures']:
  with Image.open(root/fig['asset']) as im:assert im.size==(fig['width'],fig['height']) and im.width>700
baseline=json.loads((A/'before-data03-hashes.json').read_text(encoding='utf-8'))
for path,digest in baseline.items():
 if path=='assets/psat/sets.json':continue
 assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
checks.update(status='PASS',count=10,officialFinalKeys=10,figureCount=sum(len(q['figures']) for q in bank),sourcePromptChoices='normalized exact match',limitations='Source images and chart transcriptions reviewed by same author; exact arithmetic supplements review, not independent expert audit.')
(A/'content-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
print('PASS data11-20: keys, source prompt/options, exact ratios, bounds, ranking and counterexamples.')
