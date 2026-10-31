"""Batch06: original source/native images and independent exact arithmetic."""
from pathlib import Path
from fractions import Fraction as F
import json,re,hashlib,shutil,subprocess
import pdfplumber
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/psat_remaining605_20261030/batch06'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
norm=lambda s:re.sub(r'[\s①②③④⑤·ㆍ/]','',s)
items=read(OUT/'revealed-current.json');solves={x['id']:x for x in read(OUT/'own-solves.json')};sources={x['id']:x for x in read(OUT/'blind-source.json')}
reg={x['newAsset']:x for x in read(ROOT/'artifacts/psat_final_quality_20261029/full900/native-image-repairs.json')['figures']}
checks=[];pixels=[];cache={};pdfcache={}
try:
 for row in items:
  q=row['question'];m=sources[q['id']];src=ROOT/m['source']
  if src not in pdfcache:pdfcache[src]=pdfplumber.open(src)
  page=pdfcache[src].pages[m['page']-1];left=page.width*m['side']/2;right=page.width*(m['side']+1)/2
  marker=next(w for w in page.extract_words() if w['text']==str(q['number'])+'.' and left<=w['x0']<left+45)
  rectangles=[reg[f['asset']]['rect'] for f in q['figures']]
  def keep(obj):
   if obj.get('object_type')!='char':return True
   x=(obj['x0']+obj['x1'])/2;y=(obj['top']+obj['bottom'])/2
   return not any(a<=x<=c and b<=y<=d for a,b,c,d in rectangles)
  filtered=page.filter(keep)
  native=filtered.crop((left,marker['top']-1,right,page.height)).extract_text() or ''
  if m['columnContinuation']:
   tail=filtered.crop((page.width/2,30,page.width,page.height)).extract_text() or ''
   end=re.search(r'(?m)^\d+[.]\s+(?:다음|위 글|윗글)',tail)
   if end:tail=tail[:end.start()]
   tail=re.sub(r'책형\s*\d+쪽','',tail)
   native+='\n'+tail
  native=norm(re.sub(r'^\d+[.]\s*','',native))
  heading=None
  if q['number']==10:
   assert q['choiceNote']=='A / B / C';heading='ABC';assert native.count(heading)==1;native=native.replace(heading,'',1)
  a,b=native,norm(q['prompt']+q['body']+''.join(q['choices']))
  if a!=b:
   i=next((i for i,(x,y) in enumerate(zip(a,b)) if x!=y),min(len(a),len(b)))
   raise AssertionError((q['id'],i,a[max(0,i-30):i+120],b[max(0,i-30):i+120]))
  with pdfplumber.open(ROOT/row['officialKey']) as pdf:
   pi,t=next((i+1,p.extract_text()) for i,p in enumerate(pdf.pages) if '영역 자료해석' in (p.extract_text() or ''))
  assert q['examDate'][:4] in t and f"책형 {q['book']}" in t
  answers={}
  for line in t.splitlines():
   if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
    z=list(map(int,line.split()));answers.update(zip(z[::2],z[1::2]))
  assert answers[q['number']]==q['answer']==solves[q['id']]['answer']
  checks.append(dict(id=q['id'],source=m['source'],sourcePage=m['page'],actualSide=m['side'],questionTop=marker['top'],nativeTextAndFiveChoicesMatch=True,continuation=m['columnContinuation'],choiceHeading=heading,key=row['officialKey'],keyPage=pi,answer=answers[q['number']]))
  for f in q['figures']:
   r=reg[f['asset']];assert r['source']==m['source'];assert hashlib.sha256(src.read_bytes()).hexdigest()==r['sha256']
   sig=(m['source'],r['page1based'],r['resolution'])
   if sig not in cache:
    d=OUT/'fresh-source-renders';d.mkdir(exist_ok=True);prefix=d/f"{r['sha256'][:16]}-p{r['page1based']:02d}-r{r['resolution']}"
    subprocess.run([shutil.which('pdftoppm'),'-r',str(r['resolution']),'-f',str(r['page1based']),'-l',str(r['page1based']),'-singlefile','-png',str(src),str(prefix)],check=True,capture_output=True)
    cache[sig]=Image.open(prefix.with_suffix('.png')).convert('RGB')
   ref=cache[sig].crop(r['pixelBox']);actual=Image.open(ROOT/f['asset']).convert('RGB');assert actual.size==ref.size and actual.tobytes()==ref.tobytes()
   pixels.append(dict(id=q['id'],asset=f['asset'],page=r['page1based'],resolution=r['resolution'],pixelBox=r['pixelBox'],pixelMatch=True))
finally:
 for pdf in pdfcache.values():pdf.close()
 for im in cache.values():im.close()

# Independently transcribed from full source tables/graphs, not authored answers.
housing=dict(houses=[1813,1853],private=[1569,1597],owners=[1146,1173],households=[2034,2093],topRegions=[F('64.4'),F('63.0'),F('61.0')])
growth=lambda v:F(v[-1]-v[0],v[0])
assert [round(100*float(growth(housing[k])),1) for k in ['houses','private','owners']]==[2.2,1.8,2.4]
assert [round(float(F(n,d)*100),1) for n,d in zip(housing['owners'],housing['households'])]==[56.3,56.0]
jets={'A':[F('3.0'),12,1400,F('1.4'),1,0],'B':[F('1.5'),14,800,F('.8'),1,1],'C':[F('2.5'),9,1200,F('.9'),0,0],'D':[F('2.0'),10,1250,F('.7'),1,1],'E':[F('2.7'),8,1500,F('1.0'),0,1]}
scores={k:[] for k in jets}
for j in range(4):
 order=sorted(jets,key=lambda k:jets[k][j],reverse=j!=3)
 for i,k in enumerate(order):scores[k].append(5-i)
totals={k:sum(v)+sum(jets[k][4:]) for k,v in scores.items()};assert totals==dict(A=15,B=13,C=10,D=15,E=13)
assert min((k for k in totals if totals[k]==max(totals.values())),key=lambda k:jets[k][3])=='D'
driver=dict(young=F('40.0')+F('36.1'),old=F('36.4')+F('46.4'),experience=F('19.8')-F('7.4'),service=F('13.7')-F('2.8'),hours=F('10.8')-F('9.8'),days=F('25.4')-F('22.1'),costNew=[408,356],costUsed=[214,138]);assert driver['days']>3
local=[9,15,14,18,19,17,18];child=[10265,73060,55780,58680,61380,59559,72261];parents=[6700,19465,15785,13006,11660,9071,8619];operations=[11,30,38,35,39,38,40];volunteers=[2083,1600,2989,2144,2568,2406,2071]
direction=lambda v:[(b>a)-(b<a) for a,b in zip(v,v[1:])]
assert direction(local)==direction(child)!=direction(parents)
assert F(child[4],operations[4])<1600<F(child[3],operations[3]);assert F(child[2],volunteers[2])>10>5>F(child[0],volunteers[0])
# Rows: sow, transplant, harvest. Month union differs from per-method counts.
cucumber=[([11],[12,1],[2,3,4,5]),([1],[2],[3,4,5,6]),([3],[4],[5,6,7,8]),([4],[5],[6,7,8]),([5],[6],[7,8,9,10,11])]
pepper=[([10],[12],[1,2,3,4,5]),([11],[2],[3,4,5,6,7]),([2],[4],[5,6,7,8,9,10]),([3],[5],[6,7,8,9,10]),([4],[6],[7,8,9,10,11])]
intersection=lambda rows:sorted(set(x for s,t,h in rows for x in t)&set(x for s,t,h in rows for x in h))
assert intersection(cucumber)==intersection(pepper)==[2,4,5,6]
pepperCounts={m:sum(m in h for s,t,h in pepper) for m in range(1,13)};assert max(pepperCounts,key=pepperCounts.get)==7
assert min(range(5),key=lambda i:len(cucumber[i][2]))==3
fish=dict(kim=[781,837,853,880,812],oyster=[1292,1314,1317,1293,1277],cockle=[1076,1093,1096,1115,1121],clam=[570,587,576,582,565],seaweed=[802,920,898,882,678]);ftotal=[4521,4751,4740,4752,4453]
margin=[2*(a+b)-t for a,b,t in zip(fish['oyster'],fish['cockle'],ftotal)];assert margin==[215,63,86,64,343];assert 2*2398>4752
assert F(17,570)>F(6,576);assert sum(v[-1]>v[-2] for v in fish.values())==1
hanok=dict(culture=[8,8,10,11,12,12],craft=[14,14,11,10,10,9],residents=[3,3,5,6,8,8],experience=[0,0,1,3,4,5],hotel=[2,2,1,0,0,0]);htotal=[27,27,28,30,34,34]
assert [sum(row[i] for row in hanok.values()) for i in range(6)]==htotal
assert F(8,34)>F(1,5) and growth([3,5])==2*growth([6,8]);assert [i for i,(a,b) in enumerate(zip(hanok['hotel'],hanok['experience'])) if a>b]==[0,1]
burn={'A':(800,163785,66),'B':(48,12540,34),'C':(750,169781,75),'D':(400,104176,65),'E':(900,238770,74)}
ratios={k:F(y,c) for k,(c,y,n) in burn.items()};assert ratios['E']>264>max(v for k,v in ratios.items() if k!='E');assert 48*250<12540
production={'national':[4397532,4374899,4046574,4456952,4331597],'A':[223472,228111,203893,237439,221271],'rice':[153944,150901,127387,155501,143938],'barley':[270,369,398,392,201],'grain':[29942,23823,30972,33535,30740],'beans':[9048,10952,9560,10899,10054],'root':[30268,42066,35576,37112,36338]}
area={'A':[46724,47446,46615,47487,46542],'rice':[29006,28640,28405,28903,28708],'barley':[128,166,177,180,98],'grain':[6804,6239,6289,6883,6317],'beans':[5172,5925,5940,5275,5741],'root':[5614,6476,5804,6246,5678]}
regionalDrop=F(16168,237439);nationalDrop=F(125355,4456952);assert regionalDrop>F(6,100)>F(3,100)>nationalDrop
crops=['rice','barley','grain','beans','root'];rates={k:growth(production[k]) for k in crops};assert max(rates,key=lambda k:abs(rates[k]))=='barley' and max(rates,key=rates.get)=='root'
assert all(2*r>a for r,a in zip(area['rice'],area['A']))
yieldPerHa={k:F(production[k][-1],area[k][-1]) for k in crops};assert yieldPerHa['root']>6>max(v for k,v in yieldPerHa.items() if k!='root');assert direction(production['A'])==direction(area['A'])
adapted=next(row['question'] for row in items if row['question']['id']=='kr-mpm-2024-07-27-psat-d-20');assert 'GRIT 보완 조건' in adapted['choiceNote'] and '절댓값' in adapted['choiceNote'] and '원문에 명시되지 않은' in adapted['editNote']
assert F(10**9)*F('1.99')/100+5500000==25400000;assert F(10**9)*F('2.35')/100+5400000==28900000
assert F(4*10**8)*F('.48')/100==1920000<2000000
special10=F(10**9)*F('1.20')/100+3250000;special100=F(10**10)*F('1.27')/100;assert special100<10*special10
result=dict(status='PASS',sourceKeyNative=checks,figurePixels=pixels,housing=housing,jetScores=scores,jetTotals=totals,driverComparisons=driver,
 safetyClass=dict(direction=direction(local),perOperation2020=str(F(child[3],operations[3])),perOperation2021=str(F(child[4],operations[4])),perVolunteer2017=str(F(child[0],volunteers[0])),perVolunteer2019=str(F(child[2],volunteers[2]))),
 cropCalendar=dict(cucumber=cucumber,pepper=pepper,commonMonths=[2,4,5,6],pepperHarvestCounts=pepperCounts),fishHalfMargins=margin,hanok=hanok,burnRatios=ratios,
 cropProduction=dict(regionalDrop=regionalDrop,nationalDrop=nationalDrop,signedRates=rates,yieldPerHa=yieldPerHa,sourceAmbiguityConfirmed=True,explicitGrItConditionPreserved=True,signedMaximum='root',absoluteMaximum='barley'),
 construction=dict(tenBillionSpecial=special100,oneBillionSpecial=special10,differenceAt400million=1920000),
 limitations='Same-author fresh review. d20 original signed reading is ambiguous; app separately states absolute-value adaptation, not official original condition. No independent expert or real-device validation.')
(OUT/'source-key-model-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2,default=str)+'\n',encoding='utf-8')
print('PASS10 directPDF keys/native texts,20 fresh image pixel checks,exact models;d20original ambiguity/appcondition distinguished.')
