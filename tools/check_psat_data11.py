from pathlib import Path
import json,re,hashlib,pdfplumber
from fractions import Fraction as F
from PIL import Image
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/data11';P=R/'assets/psat/data11.json';bank=json.loads((P if P.exists() else A/'authored-data11.json').read_text(encoding='utf-8'));proof={}
old={'Bangkok':1941,'London':1906,'Paris':1545,'Dubai':1487,'Singapore':1311,'NewYork':1270,'Seoul':1239,'Kuala':1128,'Tokyo':1115,'Istanbul':916};new={'Dubai':3231,'NewYork':3197,'London':2523,'Seoul':2365,'Singapore':2148,'Bangkok':1643,'Paris':1466,'Tokyo':1203};upper={k:new.get(k,976)-v for k,v in old.items()};assert max(upper,key=upper.get)=='NewYork' and upper['NewYork']==1927 and 916<940<976
assert 3231>=2*1487 and F(2365-1239,1239)>F(2148-1311,1311)
proof['1']={'invalid':2,'IstanbulCounterexample':940,'unlistedUpper':976,'increaseUpperBounds':upper}
imm=[16852,16529,18091,18079,18736,19470];rec=[3100,2370,3069,4710,5009,24955-19470];perm=[12357,15649,13637,13291,14549,11009+3607];total=[x+y for x,y in zip(imm,rec)];direction=[(imm[i]>imm[i-1])==(rec[i]>rec[i-1]) for i in range(1,6)];assert direction==[True,True,False,True,True]
assert rec[-1]>=F(3,2)*rec[0] and total[-1]>total[-2] and perm[-1]>perm[-2] and all(x>=3*y for x,y in zip(imm,rec))
rates=[F(a,b) for a,b in zip(perm,total)];assert rates[1]>F(4,5) and all(r<F(7,10) for i,r in enumerate(rates) if i!=1)
proof['2']={'invalid':1,'filled':[total[-2],rec[-1],perm[-1]],'sameDirections':direction,'rates':list(map(str,rates))}
male=[9684,8324];female=[4663,4087];tot=[14347,12411];assert all(m+f==t for m,f,t in zip(male,female,tot));maleRates=[F(m,t)*100 for m,t in zip(male,tot)];assert maleRates[0]-maleRates[1]>=F(4,10)
assert sum([1171,1548,3925,4739,1028])==12411 and round(3925/12411*100,1)==31.6 and round(4739/12411*100,1)==38.2
assert sum([1286,929,3424,4190,2582])==12411
proof['3']={'needed':[True,True,False,True],'maleShareDropPp':str(maleRates[0]-maleRates[1]),'alreadyDerivable':'age proportions from counts;sex shares from graph','notDerivable':'region;mean household size;size composition'}
viol=[[311,202,74,19,109],[56,229,48,15,166],[77,36,5,3,28],[341,200,16,4,180],[141,81,1,2,78],[29,107,16,5,86],[19,12,8,1,3],[184,75,7,0,68],[437,428,34,6,388]]
assert sum(r[0] for r in viol)==1595 and sum(r[1] for r in viol)==1370 and all(sum(r[2:])==r[1] for r in viol)
truth=[F(1595-1370,1595)>=F(1,10),all(r[1]<r[0] for r in viol),109<=74*F(3,2),all(r[3]<min(r[2],r[4]) for r in viol)];assert truth==[True,False,True,False];proof['4']={'truth':truth,'counterexampleTypeIncrease':'false statements56to229','counterexampleInvestigationSmallest':'facility2vscharge1'}
fac=[387+59,134+55,155+182,120+23,156+101];students=[874,459,715,277,682];loans=[756,2700,1637,1020,3469];cadavers=[[46,53,52,37],[15,23,35,41],[36,39,39,28],[34,37,38,50],[76,80,74,74]]
scores=[[3 if s<2*f else 2 if s<4*f else 1,3 if l<1000 else 2 if l<2000 else 1,3 if sum(c)>=200 else 2 if sum(c)>=120 else 1] for f,s,l,c in zip(fac,students,loans,cadavers)];assert list(map(sum,scores))==[8,4,6,7,6];proof['5']={'faculty':fac,'cadaverSums':list(map(sum,cadavers)),'scores':scores,'winner':'A'}
privateParcels=[7102,2051,468,778,1125];publicParcels=[790,621,162,110,649];privateAreas=[2269,706,64,120,215];publicAreas=[1225,402,148,36,72];privatePrices=[6563,249,61,55,681];publicPrices=[2254,1185,127,23,109]
assert [i for i,(a,b) in enumerate(zip(privatePrices,publicPrices)) if a<b]==[1,2]
assert max(publicParcels[1:])==649 and publicAreas[0]<2*sum(publicAreas[1:]) and all(a>b for a,b in zip(privateParcels,publicParcels)) and 1774<F(1,4)*7892
proof['6']={'blank':['Chungcheong','first','smaller'],'otherAreaSum':sum(publicAreas[1:]),'doubleOtherArea':2*sum(publicAreas[1:])}
rows=[[156,335,55,151,15,36],[295,253,143,132,21,19],[385,543,177,502,28,45],[344,375,303,123,18,35],[85,177,21,48,11,14]]
checks=[[v1>v0,s1>=F(3,2)*s0,F(t1,v1)>F(t0,v0),v1>10*s1] for v0,v1,t0,t1,s0,s1 in rows];assert [all(c) for c in checks]==[False,False,True,False,False];proof['7']={'checksInReportOrder':checks,'winner':'C','unitMultiplier':100}
# The source scatterplots are images, not exact numerical tables. Bounds below are conservative manual readings of visible tick intervals.
giniC=(F(52,100),F(53,100),F(33,100),F(34,100));giniB=(F(44,100),F(45,100),F(29,100),F(30,100));assert giniC[0]-giniC[3]>giniB[1]-giniB[2]
poverty={'A':(23,25,7,9),'B':(26,28,8,10),'C':(35,38,7,9),'D':(24,26,11,13),'E':(32,34,11,13),'F':(28,30,11,13),'G':(27,29,17,19)}
cu=F(poverty['C'][3],poverty['C'][0]);assert all(cu<F(b[2],b[1]) for k,b in poverty.items() if k!='C')
proof['8']={'truth':[True,False,True,False],'manualGraphRelations':'G highest vertical in both;D left of A but above A in Gini','giniDifferenceBounds':'C>=.18;B<=.16','povertyConservativeReadingBounds':poverty,'notClaimed':'exact coordinates or exact percentages absent from source'}
choices=[[4520,6620,6810,9920,9830,9610],[5520,6930,7810,9920,9830,9610],[4520,6930,7810,9920,9830,9610],[4980,6930,7810,9920,9830,9610],[4520,7620,7810,10920,9830,9610]]
checks=[[r[0]<=5000,r[3]<=10000,r[3]-r[1]<3000,2*r[0]<r[3]] for r in choices];assert [all(c) for c in checks]==[False,False,True,False,False];proof['9']={'checks':checks,'nonmedicalRanges':[r[3]-r[1] for r in choices]}
dis=[10213,11610,11512,12243,12331];women=[48967,53494,57896,63561,67332];soc=[4558,5166,5410,5864,6201];weak=[a+b+c for a,b,c in zip(dis,women,soc)];assert all(weak[i]>weak[i-1] for i in range(1,5)) and all(w>max(d,s) for w,d,s in zip(women,dis,soc))
allN=[471100,502710,536305,572118,602681];womenN=[108105,118908,131203,144924,156406];assert 4*womenN[-1]>=allN[-1] and all(100*womenN[i]>=105*womenN[i-1] for i in range(1,5))
allMoney=[480545,513566,572121,595782,707205];assert all(10*w>=a for w,a in zip(women[:-1],allMoney[:-1])) and 10*women[-1]<allMoney[-1] and women[-1]>=67000 and all(women[i]>women[i-1] for i in range(1,5))
proof['10']={'truth':[False,True,True,True],'weakTotals':weak,'annualWomenCountGrowth':[str(F(womenN[i]-womenN[i-1],womenN[i-1])) for i in range(1,5)],'womenContractInTrillion':str(F(women[-1],10000)),'counterexampleInstitutionOrder':'publiccorp7>quasigov5;other3>localcorp1'}
with pdfplumber.open(next((R/'artifacts/psat600_20261028/sources/6001').glob('*.pdf'))) as pdf:
 t=next(p.extract_text() for p in pdf.pages if '영역 자료해석' in p.extract_text());assert '2025' in t and '혁' in t;keys={}
 for line in t.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
   v=list(map(int,line.split()));keys.update(zip(v[::2],v[1::2]))
 assert len(keys)==25
norm=lambda s:re.sub(r'[\s·]+','',s)
for q in bank:
 n=q['number'];raw=(A/f'2025special-d{n}-source.txt').read_text(encoding='utf-8');prompt,tail=raw.split(f'{n}.',1)[1].split('?',1);assert norm(q['prompt'])==norm(prompt+'?')
 if n==9:assert q['choices']==[f'자료 {i}' for i in range(1,6)] and len(q['figures'])==6
 else:
  opts=[re.sub(r'\s+',' ',s).strip() for s in re.split('[①②③④⑤]','①'+tail.split('①',1)[1])[1:]];assert all(norm(a)==norm(b) for a,b in zip(q['choices'],opts))
 assert q['answer']==keys[n] and len(q['steps'])==len(q['optionReasons'])==5,(n,q['answer'],keys[n])
 for s,prefix in zip(q['steps'],['착안점: ','실전 풀이: ','답 확정 기준: ','정석 근거: ','적용 한계: ']):assert s.startswith(prefix) and len(s)>40
 assert not any('\ue000'<=c<='\uf8ff' or c in '\ufffd\u2060\u2024' for c in json.dumps(q,ensure_ascii=False)),n
manifest=json.loads((A/'crop-manifest.json').read_text(encoding='utf-8'));assert len(manifest)==32
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
 if path.name in ['sets.json','data11.json']:continue
 obj=json.loads(path.read_text(encoding='utf-8'))
 if isinstance(obj,list):
  for q in obj:
   k=(q.get('examDate',q['source'][:10].replace('.','-')),q['subject'],q['number']);assert k not in seen;seen.add(k);old+=1
for q in bank:
 k=(q['examDate'],q['subject'],q['number']);assert k not in seen;seen.add(k)
for path,digest in json.loads((A/'before-data11-hashes.json').read_text(encoding='utf-8')).items():
 if path!='assets/psat/sets.json':assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
proof.update(status='PASS',count=10,officialFinalKeys=10,figures=32,originals=10,preservedExisting=old,limitations='Same-author source/graph review and independent-form exact calculations;graph8 uses conservative manual bounds, not exact source coordinates;not independent expert certification.')
(A/'content-checks.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PASS10source/key/32figures10originals;models;preserved',old)
