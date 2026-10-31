from pathlib import Path
import json,re,hashlib,pdfplumber
from fractions import Fraction as F
from PIL import Image
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/data12';P=R/'assets/psat/data12.json';bank=json.loads((P if P.exists() else A/'authored-data12.json').read_text(encoding='utf-8'));proof={}
assert [q['number'] for q in bank]==list(range(11,21))
total=[168777,177428,189231,190942,194615];medical=[9319,11315,11050,11368,11317]
ministries={'science':[2548,2711,3335,3577,4111],'agri':[487,462,479,590,682],'industry':[1887,3089,1583,1929,1491],'welfare':[3830,4410,4924,4608,4531],'env':[82,123,134,138,149],'food':[218,272,313,335,353],'rural':[267,248,282,191,0]}
assert [sum(v[i] for v in ministries.values()) for i in range(5)]==medical
annual=[k for k,v in ministries.items() if all(v[i]>v[i-1] for i in range(1,5))];assert annual==['science','env','food']
growth={k:F(v[-1]-v[-2],v[-2]) for k,v in ministries.items()};assert max(growth,key=growth.get)=='agri' and growth['agri']>F(15,100)>growth['science']
ratios=[F(a,b) for a,b in zip(medical,total)];assert all(x>=F(55,1000) for x in ratios) and [x>F(6,100) for x in ratios]==[False,True,False,False,False]
proof['11']={'increasingMinistries':annual,'growth':{k:str(v) for k,v in growth.items()},'medicalShares':list(map(str,ratios)),'answer':['env','agri',2021]}
freshMean=[F(x) for x in ['99.5','99.4','92.9']];freshMin=[F(x) for x in ['98.3','95.2','68.5']];freshMedian=[F(x) for x in ['99.6','99.8','98.7']]
enrolledMean=[F(x) for x in ['95.7','97.8','94.7']];enrolledMedian=[F(x) for x in ['95.2','97.0','96.2']]
gap=[abs(a-b) for a,b in zip(enrolledMean,enrolledMedian)];assert gap==[F(1,2),F(4,5),F(3,2)]
assert freshMin.index(min(freshMin))==freshMedian.index(min(freshMedian))==2 and freshMean.index(max(freshMean))!=enrolledMean.index(max(enrolledMean)) and F('64.3')>F('63.6')
proof['12']={'truth':[True,False,True,True],'gaps':list(map(str,gap)),'rankArgument':'11 distinct values: fifth highest > sixth=64.3 > mean63.6'}
assert 33353>4*7564 and F(396,7564)<F(1,10)<F(3297,7168)
assert F(8558,33353)<F(18243,24795);outmeal=3871-3705;assert outmeal==166 and 20*outmeal<3871 and 6552<4*3871
proof['13']={'truth':[True,False,False,True],'outMeal1980':outmeal,'expenditure4x':4*7564,'food4x':4*3871,'conditionalIncome2024':4*9645}
unit=[210,120,100,80];facility=[200,100,50,60];oper=[10,20,50,20];volume=[59,40,153,212]
cost=[x*y for x,y in zip(unit,volume)];opcost=[x*y for x,y in zip(oper,volume)]
assert cost==[12390,4800,15300,16960] and opcost==[590,800,7650,4240]
assert unit[1]<unit[0] and volume[1]<volume[0] and F(oper[0],unit[0])<F(oper[3],unit[3]) and volume[0]<volume[3]
proof['14']={'truth':[False,True,False,True],'commonScaleCostProducts':cost,'commonScaleOperatingCostProducts':opcost,'counterPairs':['B,A','A,D'],'notActualWonAmounts':True}
avg=F(sum(unit),4);subsidy=unit[0]-avg;new=[facility[0]*F(1,10)+oper[0],facility[1]*F(14,10)+oper[1],facility[2]*F(1,2)+oper[2]+25,facility[3]*F(1,2)+oper[3]+10]
assert avg==F('127.5') and subsidy==F('82.5') and new==[30,160,100,60] and max(new)-min(new)==130
proof['15']={'average':str(avg),'subsidy':str(subsidy),'newUnitCosts':list(map(str,new)),'gap':130}
apps=[[53,67],[106,59],[65,75],[187,82]];passed=[[14,37],[32,27],[8,33],[42,29]]
bachelor=[F(p[0],a[0]) for a,p in zip(apps,passed)];master=[F(p[1],a[1]) for a,p in zip(apps,passed)];shares=[F(a[1],sum(a)) for a in apps]
assert [i for i,p in enumerate(passed) if p[1]>p[0]]==[0,2] and bachelor[1]>bachelor[0]
assert master[1]>F(45,100) and master[3]<F(36,100) and master[1]-master[3]>F(7,100)
assert all(x>F(3,10) for x in shares)
proof['16']={'truth':[True,False,True,False],'bachelorRates':list(map(str,bachelor)),'masterRates':list(map(str,master)),'masterApplicantShares':list(map(str,shares))}
traffic=[[9509,3177,217,53242],[13565,6204,327,86851],[2948,1675,64,16305],[3350,1464,72,20053],[2385,1211,68,17824],[1121,581,27,7376]]
assert [sum(r[j] for r in traffic) for j in range(4)]==[32878,14312,775,201651]
assert traffic[2][0]>traffic[4][0] and traffic[2][3]<traffic[4][3]
assert traffic[2][1]>traffic[3][1] and traffic[2][2]<traffic[3][2]
assert F(68,2385)>F(327,13565)
assert F(16305,1675)<10<12<F(7376,581)
assert F(16305,64)<260<F(201651,775)
proof['17']={'truth':[False,False,False,False,True],'accidentCostBridge':260,'C64Times260':64*260,'total775Times260':775*260,'counterexamples':['C/E population-cost','C/D cars-accidents','E>B per person','C<F per car']}
tax23=list(map(F,['115.8','80.4','14.6','73.8','8.8','6.1','10.8','7.3','4.6']))
budget=list(map(F,['125.8','77.7','14.7','81.4','10.2','5.4','15.3','8.9','4.1']))
actual=list(map(F,['117.4','62.5','15.3','82.2','8.7','4.8','11.4','7.0','4.2']))
assert list(map(sum,[tax23,budget,actual]))==list(map(F,['322.2','343.5','313.5']))
decrease=[a-b for a,b in zip(tax23,actual)];gap=[abs(a-b) for a,b in zip(tax23,budget)];errors=[abs(a-b)/a for a,b in zip(actual,budget)]
assert decrease.index(max(decrease))==1 and gap.index(max(gap))==0 and [x>F(1,3) for x in errors]==[False,False,False,False,False,False,True,False,False]
assert tax23[1]>tax23[3] and actual[1]<actual[3]
proof['18']={'truth':[True,True,True,False],'decreases':list(map(str,decrease)),'previousActualToBudgetGaps':list(map(str,gap)),'errorRates':list(map(str,errors)),'rankReversal':'corporation/VAT'}
passN=[2994,2043,1823,2050,2511];fixN=[2323,1580,1413,1557,1995];stopN=[59,63,49,53,63]
assert list(map(sum,[passN,fixN,stopN]))==[11421,8868,287]
delta=[passN[i]-passN[i-1] for i in range(1,5)];assert delta==[-951,-220,227,461]
sumN=sum(passN+fixN+stopN);parts=[round(sum(v)/sumN*100,1) for v in [passN,fixN,stopN]];assert parts==[55.5,43.1,1.4]
wrongDenom=[round(s/(p+f+s)*100,1) for p,f,s in zip(passN,fixN,stopN)];assert wrongDenom==[1.1,1.7,1.5,1.4,1.4]
assert round(59/2994*100,1)==2.0
proof['19']={'truth':[True,True,False,False],'increments':delta,'actualComposition':parts,'wrongChart4UsesTotal':wrongDenom,'correctStopPassRatio':[str(F(s,p)) for s,p in zip(stopN,passN)],'originalWrongGraphsPreserved':True}
m23=[21,13,8,34,48];m24=[31,17,15,30,37];act23=[10,7,23,15,14];act24=[14,8,20,19,17];pay23=[550,270,250,460,500];pay24=[650,340,200,520,600]
assert [sum(x) for x in [m23,m24,act23,act24,pay23,pay24]]==[124,130,69,78,2030,2310]
per23=[F(p,a) for p,a in zip(pay23,act23)];per24=[F(p,a) for p,a in zip(pay24,act24)]
assert per23.index(max(per23))==per24.index(max(per24))==0 and 34*5>=124
growth=[F(b-a,a) for a,b in zip(pay23,pay24)];assert growth.index(max(growth))==1 and m24[1]>m23[1]
eligible=[i for i in range(5) if act24[i]>act23[i]];assert eligible==[0,1,3,4] and sum(m24[i] for i in eligible)*3==345
proof['20']={'truth':[True,True,False,True,True],'growth':list(map(str,growth)),'perActivity23':list(map(str,per23)),'perActivity24':list(map(str,per24)),'eligibleMembers':115,'additionalManWon':345}
with pdfplumber.open(next((R/'artifacts/psat600_20261028/sources/6001').glob('*.pdf'))) as pdf:
 t=next(p.extract_text() for p in pdf.pages if '영역 자료해석' in p.extract_text());assert '2025' in t and '혁' in t;keys={}
 for line in t.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
   v=list(map(int,line.split()));keys.update(zip(v[::2],v[1::2]))
 assert len(keys)==25
norm=lambda s:re.sub(r'[\s·]+','',s)
for q in bank:
 n=q['number'];raw=(A/f'2025special-d{n}-source.txt').read_text(encoding='utf-8');prompt,tail=raw.split(f'{n}.',1)[1].split('?',1);assert norm(q['prompt'])==norm(prompt+'?')
 if True:
  opts=[re.sub(r'\s+',' ',s).strip() for s in re.split('[①②③④⑤]','①'+tail.split('①',1)[1])[1:]];assert all(norm(a)==norm(b) for a,b in zip(q['choices'],opts))
 assert q['answer']==keys[n] and len(q['steps'])==len(q['optionReasons'])==5,(n,q['answer'],keys[n])
 for s,prefix in zip(q['steps'],['착안점: ','실전 풀이: ','답 확정 기준: ','정석 근거: ','적용 한계: ']):assert s.startswith(prefix) and len(s)>40
 assert not any('\ue000'<=c<='\uf8ff' or c in '\ufffd\u2060\u2024' for c in json.dumps(q,ensure_ascii=False)),n
manifest=json.loads((A/'crop-manifest.json').read_text(encoding='utf-8'));assert len(manifest)==24
for c in manifest+json.loads((A/'original-manifest.json').read_text(encoding='utf-8')):
 source=R/c['source'];assert hashlib.sha256(source.read_bytes()).hexdigest()==c['sha256']
 with pdfplumber.open(source) as pdf:
  p=pdf.pages[c['page1based']-1];ref=p.crop(c['rect']).to_image(resolution=c['resolution'],antialias=True).original.convert('RGB');path=R/c['asset'] if P.exists() else A/'staged'/c['asset'];im=Image.open(path).convert('RGB');assert im.size==ref.size and im.tobytes()==ref.tobytes(),c['asset']
  if '/figures/' in c['asset']:
   x0,y0,x1,y1=c['rect']
   for w in p.extract_words():
    if w['x1']<=x0 or w['x0']>=x1 or w['bottom']<=y0 or w['top']>=y1:continue
    assert w['x0']>=x0-.5 and w['x1']<=x1+.5 and w['top']>=y0-.5 and w['bottom']<=y1+.5,(c['asset'],w)
seen=set();old=0
for path in (R/'assets/psat').glob('*.json'):
 if path.name in ['sets.json','data12.json']:continue
 obj=json.loads(path.read_text(encoding='utf-8'))
 if isinstance(obj,list):
  for q in obj:
   k=(q.get('examDate',q['source'][:10].replace('.','-')),q['subject'],q['number']);assert k not in seen;seen.add(k);old+=1
for q in bank:
 k=(q['examDate'],q['subject'],q['number']);assert k not in seen;seen.add(k)
for path,digest in json.loads((A/'before-data12-hashes.json').read_text(encoding='utf-8')).items():
 if path!='assets/psat/sets.json':assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
proof.update(status='PASS',count=10,officialFinalKeys=10,figures=24,originals=10,preservedExisting=old,limitations='Same-author source/graph review and independent-form exact calculations;not independent expert certification.')
(A/'content-checks.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PASS10source/key/24figures10originals;models;preserved',old)
