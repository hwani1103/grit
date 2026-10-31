from pathlib import Path
import json,re,hashlib,math,itertools as it,datetime,pdfplumber
from fractions import Fraction as F
from PIL import Image
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/data15';P=R/'assets/psat/data15.json'
bank=json.loads((P if P.exists() else A/'authored-data15.json').read_text(encoding='utf-8'));proof={}
assert [(q['examDate'],q['number']) for q in bank]==[('2026-07-18',n) for n in range(16,26)]
from pathlib import Path
from fractions import Fraction as F
import itertools,json
out={}
cap=[385,370,370,370,385,370];dis=[305,306,296,256,312,338];weight=[222,239,218,220,176,227];prices=[20900,17900,42100,35400,22300,21900]
assert max(range(6),key=lambda i:F(dis[i],cap[i]))==5
assert min([100,108,104,91,113,93])==91 and min([62,70,60,52,64,54])==52
assert max(weight[i] for i in [2,4])<min(weight[i] for i in [0,1,3,5])
assert F(prices[0]+prices[2],2)>F(sum(prices[i] for i in [1,3,4,5]),4)
assert prices[3]<2*min(prices)
out['q16']={'truth':[True,True,True,True,False],'magneticAverage':[31500,24375],'flashlightPrice':35400,'doubleMinimum':35800}
sp=[9680,2350,1203,860,811,744,717,640,530,439]
assert sum(sp[1:])==8294 and F(640000,1067)<600<F(860000,1350)
assert F(530,13)/F(717,65)<4
out['q17']={'truth':[False,True,False],'otherSum':8294,'GDPJapanSaudiRatio':'2650/717'}
tot=[25,29,21,12,14];pct=[[8,20,40,28,4],[6.9,13.8,41.4,20.7,17.2],[0,14.3,52.4,28.6,4.8],[0,25,58.3,16.7,0],[7.1,21.4,35.7,28.6,7.1]]
counts=[]
for n,row in zip(tot,pct):
 vals=[]
 for pc in row:
  x=F(str(pc));possible=[k for k in range(n+1) if max(0,x-F(1,20))<=F(100*k,n)<x+F(1,20)]
  assert len(possible)==1,(n,pc,possible);vals+=possible
 assert sum(vals)==n;counts.append(vals)
region=[sum(r[j] for r in counts) for j in range(5)]
assert region==[5,18,45,25,8]
assert counts[3][2]==counts[0][3]==7 and max(r[2] for r in counts)<3*min(r[2] for r in counts)
assert counts[4][3]<2*counts[2][1] and F(counts[1][4],region[4])>F(1,2)
out['q18']={'regionOrder':['Oceania','Europe','Asia','Americas','Africa'],'counts':counts,'columnSums':region,'truth':[True,False,False,False,False],'uniqueRoundingIntervals':True}
new=[6,276,175,8,23,6,1,None,87];old=[1,303,170,7,17,None,1,14,78]
new[7]=589-sum(x for x in new if x is not None);old[5]=598-sum(x for x in old if x is not None)
assert new[7]==old[5]==7
assert max(range(8),key=lambda i:new[i]-old[i])==4
con=[159,0,15,16,40,13,8,1,13,2,1,3,0,5,0];cd=[-23,-3,1,-14,8,-11,0,0,9,2,0,3,-1,2,0]
man=[21,0,21,18,21,3,41,0,3,35,1,6,1,4,0];md=[-10,0,3,-11,4,-3,5,-1,0,13,-2,5,-1,3,0]
assert sum(con)==276 and sum(man)==175 and sum(cd)==-27 and sum(md)==5
assert sum(m>c for m,c in zip(man,con))==6
out['q19']={'filledFarm2025':new[7],'filledForestry2024':old[5],'deathChanges':[a-b for a,b in zip(new,old)],'truth':[True,False,True,True,True],'manufacturingHigherTypes':[i for i in range(15) if man[i]>con[i]]}
c24=[a-b for a,b in zip(con,cd)];m24=[a-b for a,b in zip(man,md)]
assert sorted(range(15),key=lambda i:c24[i],reverse=True)[:2]==[0,4]
assert sorted(range(15),key=lambda i:m24[i],reverse=True)[:2]==[6,0]
out['q20']={'construction2024':c24,'manufacturing2024':m24,'second':['물체에 맞음','떨어짐']}
cases=[31681,30982,21832,18902,19039,23360];loss=[7000,7744,5438,4472,7257,11330]
assert F(loss[0],cases[0])<F(23,100)<F(loss[3],cases[3])
assert F(loss[4]-loss[3],loss[3])>F(3,5)>F(loss[5]-loss[4],loss[4])
assert 8883+1625+2324+3156+2135+779==18902 and F(15988,18902)<F(9,10)
out['q21']={'truth':[False,True,False],'under60':15988,'total2023':18902}
trees=[[25922,1600,14430,6784],[15553,1210,2658,1719],[74254,5374,19747,17890],[3679,0,3190,2137],[14550,1415,8127,2509],[18229,123,1215,465],[13379,0,1519,0],[334,0,76,0],[0,0,0,2045]]
totals=[165900,9722,50962,33549];herb=[8723,34327,11246,14510];area=[7300,6130,10470,4530]
assert [sum(r[i] for r in trees) for i in range(4)]==totals
rank=sorted(range(4),key=lambda i:F(trees[2][i],trees[0][i]),reverse=True)
assert rank==[1,0,3,2] and sum(r[0]>0 for r in trees)==8
assert trees[3][0]<sum(trees[3][1:])
assert [sorted(range(9),key=lambda j:trees[j][i],reverse=True)[2] for i in [0,1]]==[5,4]
assert min(range(4),key=lambda i:F(herb[i],area[i]))==2 and F(herb[3],totals[3])<2*F(herb[2],totals[2])
assert F(herb[3],totals[3])<F(44,100) and F(herb[2],totals[2])>F(22,100)
out['q22']={'ratioRanking':rank,'truth':[False,True,False,False,False],'speciesSeo':8}
pop=[105077,292837,217032,431587,416012];staff=[197,267,200,337,334];dispatch=[2590,3759,2712,5634,6793];action=[2148,3108,2257,4887,5172];rescue=[482,702,426,611,676]
assert max(range(5),key=lambda i:F(staff[i],pop[i]))==0
assert sorted(range(5),key=lambda i:F(dispatch[i],staff[i]),reverse=True)==[4,3,1,2,0]
assert max(range(5),key=lambda i:F(action[i],dispatch[i]))==3
assert F(rescue[3],action[3])<F(13,100)<F(rescue[4],action[4])
assert F(dispatch[4],staff[4])>20 and F(dispatch[3],staff[3])>16 and F(dispatch[1],staff[1])>14>F(dispatch[2],staff[2])>F(27,2)>F(dispatch[0],staff[0])
out['q23']={'truth':[True,True,False,False],'Daction':4887}
a24=[300,150,50,100,250];a25=[300,100,50,400,150]
valid=[[x for x in range(1001) if abs(x-a)<=100 and 2*abs(x-b)<=b and 175<=a+b+x<=800] for a,b in zip(a24,a25)]
intervals=[[min(xs),max(xs)] for xs in valid];assert intervals==[[200,200],[50,150],[75,75],[200,200],[150,225]]
assert sum(x[0] for x in intervals)==675 and sum(x[1] for x in intervals)==850
out['q24']={'all0to1000IntegersPerBusinessChecked':True,'intervals':intervals,'extremes':[675,850]}
y70=[841,728,394,789,457,543];y20=[719,347,248,356,278,371];o70=[60,68,163,73,159,117];o20=[63,131,295,134,258,201]
assert max(range(6),key=lambda i:y70[i]-y20[i])==3 and min(range(6),key=lambda i:abs(y20[i]-o20[i]))==4
assert max(range(6),key=lambda i:F(o70[i],y70[i]))==max(range(6),key=lambda i:F(o20[i],y20[i]))==2
assert min(range(6),key=lambda i:y20[i]+o20[i])==1
assert F(y20[4],1000+y20[4]+o20[4])>F(y20[2],1000+y20[2]+o20[2])
out['q25']={'truth':[True,True,True,False,True],'dependencySumsTenths':[a+b for a,b in zip(y20,o20)],'largestWorkingAge':'B'}

proof=out
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
 if n==20:assert q['choiceNote']=='건설업 → 제조업'
 if n==24:assert q['choiceNote']=='(가) → (나)'
 assert len(opts)==5 and all(norm(a)==norm(b) for a,b in zip(q['choices'],opts))
 assert q['answer']==keys[q['examDate']][n] and len(q['steps'])==len(q['optionReasons'])==5
 for s,prefix in zip(q['steps'],['착안점: ','실전 풀이: ','답 확정 기준: ','정석 근거: ','적용 한계: ']):assert s.startswith(prefix) and len(s)>40
 assert not any('\ue000'<=c<='\uf8ff' or c in '\ufffd\u2060\u2024' for c in json.dumps(q,ensure_ascii=False)),n
manifest=json.loads((A/'crop-manifest.json').read_text(encoding='utf-8'));assert len(manifest)==20
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
regions={16:[(8,1,91,465)],17:[(9,0,109,508)],18:[(9,1,90,397)],19:[(10,0,49,800)],20:[(10,0,49,800)],21:[(11,0,91,618)],22:[(11,1,90,480)],23:[(12,0,91,398)],24:[(12,1,128,862)],25:[(13,0,92,382)]}
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
 if path.name in ['sets.json','data15.json']:continue
 obj=json.loads(path.read_text(encoding='utf-8'))
 if isinstance(obj,list):
  for q in obj:
   k=(q.get('examDate',q['source'][:10].replace('.','-')),q['subject'],q['number']);assert k not in seen;seen.add(k);old+=1
for q in bank:
 k=(q['examDate'],q['subject'],q['number']);assert k not in seen;seen.add(k)
for path,digest in json.loads((A/'before-data15-hashes.json').read_text(encoding='utf-8')).items():
 if path!='assets/psat/sets.json':assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
proof.update(status='PASS',count=10,officialFinalKeys=10,figures=20,originals=10,preservedExisting=old,limitations='Same-author source review with exact rational calculations and countermodels;not independent expert certification.')
(A/'content-checks.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PASS10source/key/20figures10originals;models;preserved',old)
