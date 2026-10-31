from pathlib import Path
import json,re,hashlib,itertools as it,pdfplumber
from fractions import Fraction as F
from PIL import Image
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/data17';P=R/'assets/psat/data17.json'
bank=json.loads((P if P.exists() else A/'authored-data17.json').read_text(encoding='utf-8'));proof={}
assert [(q['examDate'],q['number']) for q in bank]==[('2026-03-07',n) for n in range(11,21)]
left=[4,20,4,13,11];right=[1,10,17,9,10];buoys=[1,4,22,9,12];bridges=[1,4,6,2,3];rail=[17,101,109,23,58]
conditions=[[left[i]>right[i],5*left[i]>=sum(left),5*buoys[i]<sum(buoys),100*bridges[i]<6*rail[i]] for i in range(5)]
assert [all(c) for c in conditions]==[False,True,False,False,False]
proof['11']={'conditions':conditions,'leftTotal':52,'buoysMean':'48/5','bridgeBounds':['D2/23>2/25=.08','B4/101<4/100=.04']}
temp=[F(x) for x in ['53.7','56.9','58.5','62.4','64.6','68.2','73.3','80.1','89.7']];power=[F(x) for x in ['112','118.9','123.1','130.6','139.3','147.2','158.4','168','179.8']]
diff=[b-a for a,b in zip(temp,temp[1:])];assert min(diff)==F('1.6') and max(diff)==F('9.6')
assert sum(b-a for a,b in zip(power,power[1:]))/8==F('8.475')
assert F('92.3')>F('64.5')*F('1.4') and F('197.8')>F('138.6')*F('1.4')
proof['12']={'truth':[False,False,True],'tempDiff':list(map(str,diff)),'powerMean':'8.475','startVoltage':'1.05not1.00'}
tasks=[[24,27,30],[88,107,122],[50,54,47],[31,40,45]];money=[[87039,88380,104201],[56793,67523,70960],[11623,12219,19786],[685,874,888]]
assert [all(a<b for a,b in zip(row,row[1:])) for row in tasks]==[True,True,False,True]
growth=[F(row[1]-row[0],row[0]) for row in money];assert growth.index(max(growth))==3
perTask=[F(m[2],t[2])>F(m[1],t[1]) for m,t in zip(money,tasks)];assert perTask==[True,False,True,False]
assert F(88380)*F(30,27)==98200<104201
proof['13']={'mapping':['주거','교육','복지·문화','참여·권리'],'perTaskRises':perTask,'budget2024Growth':list(map(str,growth))}
production=[[174,55,104,78],[166,52,75,74],[148,75,101,73],[154,103,106,78],[151,137,125,76],[127,98,99,92],[156,89,111,95],[144,68,130,91],[150,51,141,92],[146,37,155,91]]
rates=[['101','23','32.1','4.1'],['104.7','24.6','24.6','3.7'],['103.4','26','22','3.3'],['97.3','32.1','25.3','3.3'],['92.1','47.7','29.2','3.5'],['92.9','38.2','30.4','3.6'],['84.6','33.3','23.7','4.1'],['104.8','29.8','28.6','4.3'],['99.1','25.4','35.7','4.5'],['100.2','24.9','35.7','4.6']]
consumption=[[F(x)*100/F(y) for x,y in zip(row,rr)] for row,rr in zip(production,rates)]
assert all(row[3]>1400 and all(x<1000 for x in row[:3]) for row in consumption)
assert consumption[-1][0]<consumption[-2][0] and 4*production[4][1]>sum(production[4]) and F(rates[2][0])>100 and production[2][1]>=70
assert F(rates[6][2])<F(rates[5][2]) and rates[-1][2]==rates[-2][2]
proof['14']={'truth':[True,False,False,False,False],'consumptionExact':[[str(x) for x in row] for row in consumption],'bounds':[1400,1000],'barley2019':[137,489]}
exports=[604860,542233,512498,644400,683585];imports=[535202,503343,467633,615093,731370];textileX=[9303,9531,9875,11376,11880];textileM=[41427,40099,39880,48060,55489];productX=[2377,2505,2312,2825,3150];productM=[6125,5794,5621,6182,6959]
assert [a-b for a,b in zip(exports,imports)]==[69658,38890,44865,29307,-47785]
round1=lambda f:F((f*10+F(1,2)).numerator//(f*10+F(1,2)).denominator,10)
assert [round1(F(b-a,a)*100) for a,b in zip(productM,productM[1:])]==list(map(F,['-5.4','-3.0','10.0','12.6']))
assert [round1(F(a,b)*100) for a,b in zip(productX,textileX)]==list(map(F,['25.6','26.3','23.4','24.8','26.5']))
assert [round1(F(x,55489)*100) for x in [29722,10997,7811,6959]]==list(map(F,['53.6','19.8','14.1','12.5']))
assert 6959<F(15,100)*55000<F(15,100)*55489
proof['15']={'graphTruth':[True,False,True,True,True],'actual2025Composition':['53.6','19.8','14.1','12.5'],'boundary':'6959<8250<.15*55489'}
x=[1277,769,1969,373];m=[1968,694,1832,217];pop=list(map(F,['310.4','126.5','1318.2','143']));percap=list(map(F,['41.6','31.6','7.7','16.6']));gdp=[a*b for a,b in zip(pop,percap)];trade=[a+b for a,b in zip(x,m)];bal=[a-b for a,b in zip(x,m)]
truth=[x[2]>=F(3,2)*x[0],F(trade[1],gdp[1])>F(trade[3],gdp[3]),trade.index(max(trade))==2,F(bal[3],gdp[3])>F(bal[2],gdp[2]),F(trade[0],gdp[0])<F(1,5)];assert truth==[True,True,True,True,False]
assert gdp[0]<311*42 and F(1,5)*13062<3245 and F(trade[1],gdp[1])>F(3,10)>F(trade[3],gdp[3])
proof['16']={'truth':truth,'GDP':list(map(str,gdp)),'trade':trade,'balances':bal,'boundA':'GDP<13062 and trade3245>2612.4'}
grid=[[0,0,0,0,0,0,0,0],[1,2,0,0,0,0,0,0],[8,45,2,0,0,0,4,0],[0,26,1,3,0,0,1,0],[2,5,0,0,0,0,0,0],[0,6,3,0,0,1,0,0],[1,41,6,2,0,0,7,0],[1,4,0,0,0,0,0,0]]
rows=list(map(sum,grid));cols=[sum(row[j] for row in grid) for j in range(8)];assert sum(rows)==172 and cols==[13,129,12,5,0,1,12,0]
truth=[cols[1]>=4*rows[3],sum(grid[i][i] for i in range(8))>=F(172,10),grid[5][6]==grid[6][5]==0,rows[2]+cols[2]-grid[2][2]>=70];assert truth==[True,False,True,False]
proof['17']={'grid':grid,'rows':rows,'cols':cols,'truth':truth,'diagonal':15,'architectureUnion':69}
assert F(28-17,38-28)==F(11,10)<F(3,2) and 36>=22*F(3,2) and 1-F(32,36)>F(8,100)
proof['18']={'truth':[False,True,True],'maleFemale':'11/10','headcountRatio2024to2022':'8/9','decline':'1/9>8/100'}
dogs=[2242,2173,1821,3074,1236,1218,1354,359,15770,3905,3239,7554,6511,8009,7516,8157,3166];cats=[2084,2740,2532,2410,1270,337,1502,100,4797,1289,841,1372,2247,1346,1073,1164,722]
assert sorted(range(17),key=lambda i:dogs[i])[:2]==sorted(range(17),key=lambda i:cats[i])[:2]==[7,5]
assert 27826*4>106824 and 20946*5<106824 and 80467>77304 and 80467-77304==3163>3063==30889-27826
proof['19']={'truth':[True,False,False,False,False],'second':'대전','dogDecline':3163,'catDecline':3063}
age=[5,4,5,35,37,14,1];nationalities=[53,10,7,1,9,3,6,3,2,2,5];assert sum(age)==sum(nationalities)==101
female=[5,4,5,31,0,0,0];male=[a-b for a,b in zip(age,female)];assert sum(female)==45 and sum(male)==56
minimumMean=F(sum(a*b for a,b in zip(female,[20,30,40,50,60,70,80])),45);assert minimumMean==F(1970,45)<45 and 6*100>=5*101 and 53-45==8 and sum(age[:4])==49<52==sum(age[4:])
proof['20']={'truth':[False,True,True,False],'femaleCounterexample':female,'maleRemainder':male,'femaleMean':str(minimumMean),'agePartition':[49,52],'nationalityMaleLowerBound':8}
keys={}
for post,date,year,book in [(5982,'2026-03-07','2026','㉯')]:
 with pdfplumber.open(next((R/f'artifacts/psat600_20261028/sources/{post}').glob('*.pdf'))) as pdf:
  t=next(p.extract_text() for p in pdf.pages if '영역 자료해석' in p.extract_text());assert year in t and book in t;k={}
  for line in t.splitlines():
   if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
    v=list(map(int,line.split()));k.update(zip(v[::2],v[1::2]))
  assert len(k)==40;keys[date]=k
norm=lambda s:re.sub(r'[\s·]+','',s)
for q in bank:
 n=q['number'];prefix='2026grade5';raw=(A/f'{prefix}-d{n}-source.txt').read_text(encoding='utf-8');prompt,tail=raw.split('?',1)
 assert norm(q['prompt'])==norm(prompt+'?')
 opts=[re.sub(r'\s+',' ',s).strip() for s in re.split('[①②③④⑤]','①'+tail.split('①',1)[1])[1:]]
 if n==15:assert len(opts)==5;opts=[f'자료 {i}' for i in range(1,6)]
 if n==13:assert q['choiceNote']=='A → B → C'
 assert len(opts)==5 and all(norm(a)==norm(b) for a,b in zip(q['choices'],opts))
 assert q['answer']==keys[q['examDate']][n] and len(q['steps'])==len(q['optionReasons'])==5
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
   for imdata in p.images:
    if imdata['x1']<=x0 or imdata['x0']>=x1 or imdata['bottom']<=y0 or imdata['top']>=y1:continue
    assert imdata['x0']>=x0-.5 and imdata['x1']<=x1+.5 and imdata['top']>=y0-.5 and imdata['bottom']<=y1+.5,(c['asset'],'embedded image cut')
# Coverage catches omitted lines between crops, in addition to each crop's pixel and boundary checks.
regions={int(k):v for k,v in json.loads((A/'source-regions.json').read_text(encoding='utf-8')).items()}
with pdfplumber.open(R/manifest[0]['source']) as pdf:
 for n,rs in regions.items():
  assets={f['asset'] for f in next(q for q in bank if q['number']==n)['figures']};cs=[c for c in manifest if c['asset'] in assets]
  for pg,side,top,bottom in rs:
   page=pdf.pages[pg-1];mid=page.width/2
   for word in page.extract_words():
    if not(mid*side<=word['x0'] and word['x1']<=mid*(side+1) and top<=word['top'] and word['bottom']<=bottom):continue
    assert any(c['page1based']==pg and c['rect'][0]-.5<=word['x0'] and word['x1']<=c['rect'][2]+.5 and c['rect'][1]-.5<=word['top'] and word['bottom']<=c['rect'][3]+.5 for c in cs),(n,'uncovered body word',word)
proof['sourceCoverage']='All extractable body/option-table words within original source regions covered; embedded image whole bounds checked separately.'
seen=set();old=0
for path in (R/'assets/psat').glob('*.json'):
 if path.name in ['sets.json','data17.json']:continue
 obj=json.loads(path.read_text(encoding='utf-8'))
 if isinstance(obj,list):
  for q in obj:
   k=(q.get('examDate',q['source'][:10].replace('.','-')),q['subject'],q['number']);assert k not in seen;seen.add(k);old+=1
for q in bank:
 k=(q['examDate'],q['subject'],q['number']);assert k not in seen;seen.add(k)
for path,digest in json.loads((A/'before-data17-hashes.json').read_text(encoding='utf-8')).items():
 if path!='assets/psat/sets.json':assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
proof.update(status='PASS',count=10,officialFinalKeys=10,figures=24,originals=10,preservedExisting=old,limitations='Same-author source review with exact rational calculations and countermodels;not independent expert certification.')
(A/'content-checks.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PASS10source/key/24figures10originals;models;preserved',old)
