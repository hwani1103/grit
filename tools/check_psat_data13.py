from pathlib import Path
import json,re,hashlib,math,itertools as it,datetime,pdfplumber
from fractions import Fraction as F
from PIL import Image
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/data13';P=R/'assets/psat/data13.json'
bank=json.loads((P if P.exists() else A/'authored-data13.json').read_text(encoding='utf-8'));proof={}
assert [(q['examDate'],q['number']) for q in bank]==[('2025-11-15',n) for n in range(21,26)]+[('2026-07-18',n) for n in range(1,6)]
cities=[[620,570,319],[298,255,195],[294,336,94],[226,201,258],[200,136,265],[139,148,101],[124,130,153],[116,154,37],[115,147,67],[114,73,67]]
up=[i for i,x in enumerate(cities) if x[0]>x[1]];assert up==[0,1,3,4,9]
left=395-116-115;assert left==164 and math.ceil(F(left,114))==2 and 265*2>473
proof['special21']={'cities2023to2021':cities,'increasedIndices':up,'SpainRemainder':left,'omittedCityUpperBound':114,'minimumSpainCities':4,'Japan2021to2023':[408,399,493],'pastTopUnknownCountermodel':'An omitted US city can have400 in2021<=country512 and<=114 in2023;not claimed historical fact.'}
old=[6521,6771,6987,7346,7501];rec=[4353,4495,4581,4869,5027];full=[3979,4154,4161,4413,4532];reduced=[374,341,420,456,495]
assert all(a==b+c for a,b,c in zip(rec,full,reduced))
assert reduced[1]<reduced[0] and F(rec[-1],old[-1])<=F(7,10) and full[2]<10*reduced[2] and F(old[-1]-old[0],old[0])<F(1,5)
assert F(reduced[0],rec[0])<F(9,100)<F(reduced[-1],rec[-1])
proof['special22']={'truth':[False,True,False,False,False],'full':full,'reduced':reduced,'bridgeComplement':'9%'}
sales=[3500,4500,5500];returns=[70,150,220];rates=[F(a,b) for a,b in zip(returns,sales)];delta=100*(F(440,13500)-F(440,16500))
assert rates.index(max(rates))==2 and F(70,440)>F(15,100)
assert 440*F(3,2)==660<675 and 440+300==740>675 and delta==F(16,27)<1
proof['special23']={'truth':[False,False,False,True,False],'returnRates':list(map(str,rates)),'fivePercentCount':675,'returnAfter50Percent':660,'returnAfter100Each':740,'netSalesIncreasePp':str(delta)}
income14=[6500,7000,3500,4500];income24=[7500,8900,4500,6000];med14=[400,700,300,350];med24=[800,900,400,450];members=[4,5,1,2];growth=list(map(F,['-0.04','0.10','-0.06','0.05']))
med23=[F(v)/(1+r) for v,r in zip(med24,growth)];inc=[F(b-a,n) for a,b,n in zip(income14,income24,members)];ratio14=[F(x,y) for x,y in zip(med14,income14)];ratio24=[F(x,y) for x,y in zip(med24,income24)]
assert med23.index(max(med23))==0 and inc==[250,380,1000,750] and ratio14.index(min(ratio14))==0 and ratio24.index(min(ratio24))==3
proof['special24']={'truth':[False,True,False],'med2023':list(map(str,med23)),'perPersonIncomeIncrease':list(map(str,inc)),'lowestRatio14and24':[0,3]}
sex=[[320,1045,629,335,124],[398,1033,460,297,130]]
age=[[424,518,154,48,7],[201,654,212,79,28],[69,507,314,239,80],[24,399,409,266,139]]
house=[[50,169,213,223,134],[99,913,385,215,54],[549,952,432,153,42],[20,44,59,41,24]]
assert [sum(r) for r in sex]==[2453,2318] and [sum(r) for r in age]==[1151,1174,1209,1237] and [sum(r) for r in house]==[789,1666,2128,188]
assert [sum(r[j] for r in sex) for j in range(5)]==[sum(r[j] for r in age) for j in range(5)]==[sum(r[j] for r in house) for j in range(5)]
assert F(1033,2318)>F(1045,2453)
meanLower=F(654*150,201+654);assert meanLower>100
older=[a+b for a,b in zip(age[2],age[3])];extra=[max(0,b-a) for a,b in zip(older,house[1])]
assert sum(older)==2446 and extra==[6,7,0,0,0] and sum(older)+extra[0]==2452>=2450 and sum(older)+sum(extra)==2459
proof['special25']={'truth':[False,True,True],'femaleMaleShares':[str(F(1033,2318)),str(F(1045,2453))],'nonnegativeIncomeLowerBound':str(meanLower),'olderByIncome':older,'minimumJeonseOutsideByIncome':extra,'sufficientUnionLowerBound':2452,'strongerUnionLowerBound':2459,'limit':'Income lower bound assumes nonnegative income in the stated table context.'}
med=[(2,'인사','팀장','진통',1),(2,'재무','사원','소화',1),(3,'인사','대리','소화',2),(6,'홍보','팀장','진통',1),(6,'인사','대리','소화',2),(10,'재무','팀장','숙취',2),(13,'재무','사원','진통',1),(13,'홍보','사원','소화',1),(16,'인사','대리','숙취',1),(17,'인사','대리','진통',1),(20,'재무','팀장','진통',2),(21,'인사','사원','진통',1),(24,'인사','대리','숙취',1),(27,'홍보','사원','소화',1),(27,'인사','팀장','진통',2),(30,'재무','대리','진통',1)]
day=lambda d:datetime.date(2026,4,d).weekday()
assert not any(rank=='팀장' and drug=='소화' for d,dept,rank,drug,n in med)
assert [(d,day(d)) for d,dept,rank,drug,n in med if drug=='숙취']==[(10,4),(16,3),(24,4)]
assert all(sum(n for dd,dp,r,drug,n in med if dd==d and dp==dept and r=='사원')<=1 for d,dept,rank,drug,n in med if rank=='사원')
mondays=[d for d in range(1,31) if day(d)==0];assert mondays==[6,13,20,27] and all(any(dd==d and drug=='진통' for dd,dept,rank,drug,n in med) for d in mondays)
assert all(day(d)==0 for d,dept,rank,drug,n in med if dept=='홍보')
proof['regular1']={'truth':[True,False,True,True,True],'counterexampleDate':'2026-04-16 Thursday','mondays':mondays,'rows':med}
young24=[9992,997,1210,1523,5203];old24=[23254,8364,8091,12616,15234];young25=[10430,1001,1214,1424,5168];old25=[22875,8132,8001,12356,15281]
conditions=[[a+b>=10000,b<c,2*b>=5*a] for a,b,c in zip(young25,old25,old24)]
assert conditions==[[True,True,False],[False,True,True],[False,True,True],[True,True,True],[True,False,True]]
proof['regular2']={'candidates':'ABCDE','conditionMatrix':conditions,'winner':'D'}
pop=[6775,8320,5911,5174,4742,3825];mp=[925,667,600,300,615,443];per=[73243,124732,98516,172483,77099,86334];score=[100,90,96,88,98,97]
order=sorted(range(6),key=lambda i:per[i]);assert order==[0,4,5,2,1,3] and [score[i] for i in order]==[100,98,97,96,90,88] and pop.index(max(pop))!=mp.index(max(mp)) and mp[0]>=3*mp[3]
proof['regular3']={'truth':[False,True,True],'orderedCountries':'AEFCBD','orderedScores':[score[i] for i in order],'tripleThreshold':900}
appeal=[[2,14,1,3],[1,30,0,1],[2,22,2,4],[1,28,0,4]];den=[a+b for a,b,c,d in appeal];rates=[F(a,a+b) for a,b,c,d in appeal]
assert den==[16,31,24,29] and sorted(range(4),key=lambda i:rates[i],reverse=True)==[0,2,3,1] and F(6,100)<F(3,15)
proof['regular4']={'truth':[False,True,True,True,True],'rates':list(map(str,rates)),'correctDescending':[0,2,3,1],'decisionCounts':den}
month=[3,2,3,4,4,2,2,4,5,4,6,6];types=[15,8,5,17];assert sum(month)==sum(types)==45 and F(15,45)<F(35,100) and sum(month[:6])==18 and sum(month[6:])==27<36 and sum(month[6:])*2==54
proof['regular5']={'truth':[True,False,False,True],'firstHalf':18,'secondHalf':27,'year2026UnderAssumption':54}
keys={}
for post,date,year,book in [(6001,'2025-11-15','2025','혁'),(6016,'2026-07-18','2026','사')]:
 with pdfplumber.open(next((R/f'artifacts/psat600_20261028/sources/{post}').glob('*.pdf'))) as pdf:
  t=next(p.extract_text() for p in pdf.pages if '영역 자료해석' in p.extract_text());assert year in t and book in t;k={}
  for line in t.splitlines():
   if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
    v=list(map(int,line.split()));k.update(zip(v[::2],v[1::2]))
  assert len(k)==25;keys[date]=k
norm=lambda s:re.sub(r'[\s·]+','',s)
for q in bank:
 n=q['number'];prefix='2025special' if q['examDate']=='2025-11-15' else '2026';raw=(A/f'{prefix}-d{n}-source.txt').read_text(encoding='utf-8');prompt,tail=raw.split('?',1)
 assert norm(q['prompt'])==norm(prompt+'?')
 opts=[re.sub(r'\s+',' ',s).strip() for s in re.split('[①②③④⑤]','①'+tail.split('①',1)[1])[1:]]
 assert len(opts)==5 and all(norm(a)==norm(b) for a,b in zip(q['choices'],opts))
 assert q['answer']==keys[q['examDate']][n] and len(q['steps'])==len(q['optionReasons'])==5
 for s,prefix in zip(q['steps'],['착안점: ','실전 풀이: ','답 확정 기준: ','정석 근거: ','적용 한계: ']):assert s.startswith(prefix) and len(s)>40
 assert not any('\ue000'<=c<='\uf8ff' or c in '\ufffd\u2060\u2024' for c in json.dumps(q,ensure_ascii=False)),n
manifest=json.loads((A/'crop-manifest.json').read_text(encoding='utf-8'));assert len(manifest)==17
for c in manifest+json.loads((A/'original-manifest.json').read_text(encoding='utf-8')):
 source=R/c['source'];assert hashlib.sha256(source.read_bytes()).hexdigest()==c['sha256']
 with pdfplumber.open(source) as pdf:
  p=pdf.pages[c['page1based']-1];ref=p.crop(c['rect']).to_image(resolution=c['resolution'],antialias=True).original.convert('RGB');path=R/c['asset'] if P.exists() else A/'staged'/c['asset'];im=Image.open(path).convert('RGB');assert im.size==ref.size and im.tobytes()==ref.tobytes(),c['asset']
  if '/figures/' in c['asset']:
   x0,y0,x1,y1=c['rect']
   for w in p.extract_words():
    if w['x1']<=x0 or w['x0']>=x1 or w['bottom']<=y0 or w['top']>=y1:continue
    assert w['x0']>=x0-.5 and w['x1']<=x1+.5 and w['top']>=y0-.5 and w['bottom']<=y1+.5,(c['asset'],w)
   for imdata in p.images:
    if imdata['x1']<=x0 or imdata['x0']>=x1 or imdata['bottom']<=y0 or imdata['top']>=y1:continue
    assert imdata['x0']>=x0-.5 and imdata['x1']<=x1+.5 and imdata['top']>=y0-.5 and imdata['bottom']<=y1+.5,(c['asset'],'embedded image cut')
seen=set();old=0
for path in (R/'assets/psat').glob('*.json'):
 if path.name in ['sets.json','data13.json']:continue
 obj=json.loads(path.read_text(encoding='utf-8'))
 if isinstance(obj,list):
  for q in obj:
   k=(q.get('examDate',q['source'][:10].replace('.','-')),q['subject'],q['number']);assert k not in seen;seen.add(k);old+=1
for q in bank:
 k=(q['examDate'],q['subject'],q['number']);assert k not in seen;seen.add(k)
for path,digest in json.loads((A/'before-data13-hashes.json').read_text(encoding='utf-8')).items():
 if path!='assets/psat/sets.json':assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
proof.update(status='PASS',count=10,officialFinalKeys=10,figures=17,originals=10,preservedExisting=old,limitations='Same-author source review with exact rational calculations and countermodels;not independent expert certification.')
(A/'content-checks.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PASS10source/key/17figures10originals;models;preserved',old)
