from pathlib import Path
import json,re,hashlib,math,itertools as it,datetime,pdfplumber
from fractions import Fraction as F
from PIL import Image
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/data14';P=R/'assets/psat/data14.json'
bank=json.loads((P if P.exists() else A/'authored-data14.json').read_text(encoding='utf-8'));proof={}
assert [(q['examDate'],q['number']) for q in bank]==[('2026-07-18',n) for n in range(6,16)]
stop=[81,126,128,146,160];short=[20,52,50,83,105];tot=[a+b for a,b in zip(stop,short)]
truth=[all(a<b for a,b in zip(tot,tot[1:])),stop[0]>short[3],all(a>b for a,b in zip(short,stop)),all(F(short[i],tot[i])<F(short[i+1],tot[i+1]) for i in range(4)),all(stop[i]<3*short[i] for i in range(1,5))]
assert truth==[False]*4+[True] and tot==[101,178,178,229,265]
proof['q6']={'stop':stop,'shortage':short,'total':tot,'truth':truth}
usage=[[85,175],[77,194],[35,116],[39,215]];incomeLow=[148,111,222,74];incomeHigh=[282,305,172,281];workFlex=[310,245,286];workRemote=[155,200,572]
assert [sum(x) for x in usage]==[260,271,151,254] and incomeLow.index(max(incomeLow))==2 and incomeHigh.index(max(incomeHigh))==1 and workFlex.index(min(workFlex))==1 and workRemote.index(max(workRemote))==2 and 41+134==175 and 22+66==88
proof['q7']={'needed':['ㄱ','ㄷ','ㄹ'],'unneeded':'ㄴ measures childcare method,not work form or support usage','usagePercent':['26.0','27.1','15.1','25.4']}
planned=[245,231,235,247,223];entered=[227,223,224,236,216];rates=list(map(F,['92.7','96.5','95.3','95.5','96.9']));growth=[F(b-a,a) for a,b in zip(entered,entered[1:])];rg=[(b-a)/a for a,b in zip(rates,rates[1:])]
truth=[planned.index(max(planned))==entered.index(max(entered)),F(entered[0]-entered[-1],entered[0])<=F(1,10),rg[0]>=4*rg[-1],growth.index(max(growth))+1==rates.index(max(rates))]
assert truth==[True,True,False,False] and rg[0]<F(5,100) and rg[-1]>F(14,1000)
proof['q8']={'truth':truth,'enteredGrowth':list(map(str,growth)),'rateGrowth':list(map(str,rg)),'safeBounds':'2022<5%;2025>1.4%;four times2025>5.6%'}
assert F(849-528,10)==F('32.1')>F(876-581,10) and round((27.5/18.1-1)*100,1)==51.9
proof['q9']={'unused':5,'mismatch':'participation rate cannot determine per-person monthly cost','used':[1,2,3,4],'limit':'The four used choices do not supply the missing child-count cost data.'}
profits=[50,64,224-50-64-50,50];sales=[500,800,400,1000];salesOld=[476,714,408,926];inc=[a-b for a,b in zip(sales,salesOld)];margin=[F(a,b) for a,b in zip(profits,sales)]
truth=[profits.index(max(profits))==2,inc.index(max(inc))==3,F(profits[1],sum(profits))>=F(3,10),margin.index(min(margin))==0,F(sum(sales),4)>=600]
assert truth==[False]*4+[True] and sum(sales)==2700 and F(sum(sales),4)==675
proof['q10']={'truth':truth,'profits':profits,'salesIncrease':inc,'margins':list(map(str,margin)),'average':675}
names=['항공','교량','교통','댐','식수','에너지','유해폐기물','내륙수로','제방','공원','항만','철도','도로','학교','고형오물','오수','폭우','통신']
g15=list('BCBAAC'+'EEDCCC'+'BBCBBB');g20=list('BCC AAC'.replace(' ','' )+'DDCDEA'+'BADABB');g25=list('AD CABB'.replace(' ','' )+'DCCDBA'+'BADABB')
assert len(g15)==len(g20)==len(g25)==18
same=[n for n,a,b in zip(names,g15,g25) if a==b];up20=[n for n,a,b in zip(names,g15,g20) if b<a];up25=[n for n,a,b in zip(names,g20,g25) if b<a]
assert g15.count('B')==7 and same==['댐','도로','폭우','통신'] and up20==['유해폐기물','내륙수로','제방','철도','학교','오수'] and up25==['항공','에너지','내륙수로','항만']
proof['q11']={'grades':[g15,g20,g25],'same':same,'improved2020':up20,'improved2025':up25,'truth':[True,True,False]}
budget=[49109,44551,46830];support=[48406,44097,46252];people=[5408,5104,5256];universities=[242,235,238]
truth=[F(support[1],budget[1])>=F(95,100),F(support[0]-support[2],support[0])<F(people[0]-people[2],people[0]),F(support[1],people[1])<F(support[0],people[0]),F(support[2],universities[2])>F(support[0],universities[0])]
assert truth==[True,False,True,False] and F(support[1],people[1])<F('8.8')<F(support[0],people[0]) and F(support[2],universities[2])<200<F(support[0],universities[0])
assert F(support[0]-support[2],support[0])>F(4,100) and F(people[0]-people[2],people[0])<F(3,100)
proof['q12']={'truth':truth,'perPersonBridge':'8.8million','perUniversityBridge':'200million','budgetRemainder':44551-44097}
old=24856+22363;new=64816;sea=new-31818;detectSea=226-135
truth=[F(new-old,old)>=F(4,10),24856>22363 and 31818>sea,F(detectSea,943)<=F(1,10),F(1925,new)<F(2165,old)]
assert truth==[False,False,True,True] and old==47219 and sea==32998 and detectSea==91
proof['q13']={'truth':truth,'oldTotal':old,'newSea':sea,'oldSeaDetected':detectSea,'increase':new-old}
lot=[[39687,2466,1040,655,43848],[43181,3103,1029,619,47932],[47370,3688,2255,839,54152],[51371,4416,2913,1053,59753],[54468,5679,2930,1216,64293],[56526,6580,3151,1251,67508],[59562,8947,3417,1424,73350],[62168,9623,3413,1378,76582]]
assert all(sum(r[:4])==r[4] for r in lot)
truth=[all(a[3]<b[3] for a,b in zip(lot,lot[1:])),F(lot[2][4]-lot[1][4],lot[1][4])<=F(1,10),all((b[0]>a[0])==(b[4]>a[4]) for a,b in zip(lot,lot[1:])),F(lot[6][0],lot[6][4])>=F(9,10),max(range(8),key=lambda i:lot[i][1])==max(range(8),key=lambda i:lot[i][2])]
assert truth==[False,False,True,False,False]
proof['q14']={'truth':truth,'rows':lot,'maxInstantYear':2025,'maxCombinedYear':2024}
weather=['sun','part','snow','part','rain','snow','snow','part','sun','sun','cloud','rain','sun','sun','sun','sun','part','part','rain','snow','sun','snow','rain','part','rain','snow','part','rain','rain','sun','sun']
hi=[3,5,9,10,6,4,6,8,5,12,13,8,15,17,21,17,18,12,12,5,8,15,14,14,10,8,17,14,17,19,16];lo=[-5,-6,-1,-1,-2,-2,-1,-1,-2,-2,7,-1,-1,7,11,7,6,1,4,0,1,1,6,5,6,1,1,11,9,7,6]
from collections import Counter
counts=Counter(weather);spread=[a-b for a,b in zip(hi[:10],lo[:10])];freq=Counter(spread);maxDays={kind:[i+1 for i,w in enumerate(weather) if w==kind and hi[i]==max(hi[j] for j,x in enumerate(weather) if x==kind)] for kind in counts};rainLow=[lo[i] for i,w in enumerate(weather) if w=='rain'];bins=[sum(x<0 for x in rainLow),sum(0<=x<5 for x in rainLow),sum(5<=x<10 for x in rainLow),sum(x>=10 for x in rainLow)]
assert [counts[x] for x in ['sun','part','cloud','snow','rain']]==[10,7,1,6,7] and sum(counts.values())==31
assert spread==[8,11,10,11,8,6,7,9,7,14] and freq[11]==2 and freq[12]==0 and maxDays['part']==[17] and bins==[2,1,3,1]
proof['q15']={'truth':[True,False,False,True],'weatherDays':dict(counts),'first10Spreads':spread,'maximumDays':maxDays,'rainLow':rainLow,'rainBins':bins}
keys={}
for post,date,year,book in [(6016,'2026-07-18','2026','사')]:
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
 if n==9:opts=[s.split('(단위:',1)[0].strip() for s in opts]
 assert len(opts)==5 and all(norm(a)==norm(b) for a,b in zip(q['choices'],opts))
 assert q['answer']==keys[q['examDate']][n] and len(q['steps'])==len(q['optionReasons'])==5
 for s,prefix in zip(q['steps'],['착안점: ','실전 풀이: ','답 확정 기준: ','정석 근거: ','적용 한계: ']):assert s.startswith(prefix) and len(s)>40
 assert not any('\ue000'<=c<='\uf8ff' or c in '\ufffd\u2060\u2024' for c in json.dumps(q,ensure_ascii=False)),n
manifest=json.loads((A/'crop-manifest.json').read_text(encoding='utf-8'));assert len(manifest)==28
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
regions={6:[(3,1,91,295)],7:[(4,0,108,880),(4,1,57,365)],8:[(4,1,523,911)],9:[(5,0,90,898),(5,1,49,299)],10:[(5,1,490,683)],11:[(6,0,91,678)],12:[(6,1,108,395)],13:[(7,0,108,433)],14:[(7,1,90,344)],15:[(8,0,108,947)]}
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
 if path.name in ['sets.json','data14.json']:continue
 obj=json.loads(path.read_text(encoding='utf-8'))
 if isinstance(obj,list):
  for q in obj:
   k=(q.get('examDate',q['source'][:10].replace('.','-')),q['subject'],q['number']);assert k not in seen;seen.add(k);old+=1
for q in bank:
 k=(q['examDate'],q['subject'],q['number']);assert k not in seen;seen.add(k)
for path,digest in json.loads((A/'before-data14-hashes.json').read_text(encoding='utf-8')).items():
 if path!='assets/psat/sets.json':assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
proof.update(status='PASS',count=10,officialFinalKeys=10,figures=28,originals=10,preservedExisting=old,limitations='Same-author source review with exact rational calculations and countermodels;not independent expert certification.')
(A/'content-checks.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PASS10source/key/28figures10originals;models;preserved',old)
