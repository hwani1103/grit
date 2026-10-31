from pathlib import Path
import json,re,hashlib,math,itertools as it,datetime,pdfplumber
from fractions import Fraction as F
from PIL import Image
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/data16';P=R/'assets/psat/data16.json'
bank=json.loads((P if P.exists() else A/'authored-data16.json').read_text(encoding='utf-8'));proof={}
assert [(q['examDate'],q['number']) for q in bank]==[('2026-03-07',n) for n in range(1,11)]
out={}
rates=[F(36,234)*100,F(45,221)*100,F(166,226)*100];roundInt=lambda x:(x+F(1,2)).numerator//(x+F(1,2)).denominator
assert list(map(roundInt,rates))==[15,20,73] and roundInt(F(198-60,198)*100)==70
assert roundInt(F(455,44)*10)==103 and roundInt(F(551,56)*10)==98
out['q1']={'needed':[True,True,False],'reportRoundedPercent':[15,20,73],'dropRounded':70,'perSpecialistTenthsThousand':[103,98]}
feasible=[]
for youngFemale in range(1001):
 cells=[youngFemale,440-youngFemale,756-youngFemale,1000-440-756+youngFemale]
 if min(cells)>=0:feasible.append(youngFemale)
assert min(feasible)==196 and max(feasible)==440 and F(768,232)>=3 and F(756,244)>=3
out['q2']={'truth':[False,True,True],'intersectionRangeTenthsPercent':[196,440],'allFeasibleCrossTabs':len(feasible)}
rows=[[233,367],[82,318]]
assert [sum(r) for r in rows]==[600,400] and [sum(r[i] for r in rows) for i in range(2)]==[315,685]
truth=[F(233,315)>=F(7,10),F(600,1000)-F(367,685)>=F(1,10),F(233,600)<F(2,5),F(82,400)>=F(1,5)]
assert truth==[True,False,True,True];out['q3']={'table':rows,'truth':truth,'thresholds':['233>220.5','367>342.5','233<240','82>=80']}
out['q4']={'used':[False,True,True,True,True],'unusedScope':'districts within Seoul','reportScope':'nationwide provincial share and Seoul average business days','scopeLimits':'provided choices need not reconstruct every report sentence','market':[194,263,2000,3000],'openings':[169,952,1151,996],'closures':[68,623,394]}
assert roundInt(F(608,2609)*1000)==233
travel23=[955,296977,465391,37816];travel24=[954,291825,448498,36800];assert all(a>b for a,b in zip(travel23,travel24)) and travel24[1]>=290000 and travel24[2]>=440000 and travel24[3]>=36000
season23=[195,652,91,62];season24=[194,646,79,81];assert sorted(range(4),key=lambda i:season23[i],reverse=True)!=sorted(range(4),key=lambda i:season24[i],reverse=True)
assert [4716,3976,2738,1978,658]==sorted([4716,3976,2738,1978,658],reverse=True)
assert [601,292,86,21]==sorted([601,292,86,21],reverse=True) and 601>583
assert [211,118,101,93,92,89]==sorted([211,118,101,93,92,89],reverse=True)
out['q5']={'matches':[True,True,False,True,True],'seasonsTenthsPercent':[season23,season24],'reversal':['holiday season','public holiday']}
deptPlan=[28,21,23,21,67];deptActual=[28,22,22,21,66];gradePlan=[1,5,23,52,56,23];gradeActual=[1,5,23,52,52,26]
assert sum(deptPlan)==sum(gradePlan)==160 and sum(deptActual)==sum(gradeActual)==159
assert F(sum(gradeActual[:3]),159)<=F(1,5) and max(range(6),key=lambda i:F(gradeActual[i],gradePlan[i]))==5
assert sum(a<p for a,p in zip(deptActual,deptPlan))==2 and sum(a<p for a,p in zip(gradeActual,gradePlan))==1
out['q6']={'truth':[True,True,True],'grade4to6':29,'departmentBelow100':2,'gradeBelow100':1}
y23=[361,298,125,49,40,19,19,89];y24=[288,208,96,185,13,28,22,160];y25=[283,238,98,227,50,27,26,51]
assert sum(y23)==sum(y24)==sum(y25)==1000
assert [i for i in range(8) if y23[i]<y24[i]<y25[i]]==[3,6]
changes=[b-a for a,b in zip(y23,y25)];assert [i for i in range(7) if changes[i]>changes[4]]==[3]
forces=[[284,239,100,228,45,26,23,55],[282,246,90,228,53,27,31,43],[278,229,91,270,45,21,20,46],[287,235,109,176,66,36,35,56]]
assert all(sum(row)==1000 for row in forces)
assert [sorted(range(8),key=lambda i:row[i],reverse=True)[:2] for row in forces]==[[0,1],[0,1],[0,3],[0,1]]
out['q7']={'answer':['세탁',1,'공군'],'changesTenthsPp':changes,'allThreeYears':[y23,y24,y25]}
# columns 신규,승진,재등록,재공개,퇴직,의무면제,정기변동
months=[[15,18,1,0,23,1,0],[21,23,0,0,38,3,2],[17,24,2,2,59,1,1718],[37,21,2,4,35,5,0],[24,9,4,1,41,8,0],[21,10,0,3,148,1,2],[17,9,0,1,60,1,0],[15,7,0,0,27,0,6],[622,14,1,1,566,4,0],[25,19,0,0,19,4,0],[20,16,2,0,28,2,2],[18,11,0,0,20,0,0]]
totals=list(map(sum,months));assert totals==[58,87,1823,104,87,185,88,55,1208,67,70,49]
rank=sorted(range(12),key=lambda i:totals[i],reverse=True);assert rank[:5]==[2,8,5,3,6]
regular=[i+1 for i,row in enumerate(months) if row[6]];counter=[m for m in regular if totals[m-1]<=totals[m-2]];assert counter==[8]
quarter=[sum(row[i] for row in months[9:]) for i in range(7)];assert quarter==[63,46,2,0,67,6,2]
assert F(25,19)>F(13,10) and F(622,566)<F(11,10)
out['q8']={'truth':[True,False,True,False],'totals':totals,'regularMonths':regular,'counterexampleMonths':counter,'quarterTotals':quarter}
matrices=[[[4800,3400,700],[7500,5800,900],[9800,1100,800],[6900,1400,900],[8200,6400,4100]],[[4800,3500,700],[7600,5200,950],[9800,1000,850],[7200,1400,950],[8500,6600,4400]],[[4900,3500,750],[7400,5800,900],[7100,1200,800],[9600,1500,950],[8700,6600,4300]],[[5500,3900,900],[8100,6200,1200],[9200,1100,950],[6700,1700,1000],[8900,6800,3900]],[[5200,3600,800],[7800,6100,1000],[9400,1200,900],[7000,1500,1000],[5900,6600,4200]]]
conditions=[]
for m in matrices:conditions.append([m[2][0]>max(row[0] for i,row in enumerate(m) if i!=2),[i for i,row in enumerate(m) if row[0]<6000]==[0],all(4*m[i][1]>=3*m[i][0] for i in [1,4]),m[4][2]>=4000])
assert [all(c) for c in conditions]==[True,False,False,False,False];out['q9']={'conditions':conditions,'matrices':matrices}
coords=[(10,10),(15,25),(15,40),(30,20),(40,20),(10,35),(20,30),(25,25),(35,10),(25,10)];scores=[(2*x+y,x+2*y) for x,y in coords];different=[chr(65+i) for i,(a,b) in enumerate(scores) if (a>=60)!=(b>=60)]
assert different==['B','F','I','J'] and scores[9]==(60,45)
out['q10']={'coords':coords,'scores':scores,'different':different,'inclusiveThreshold':60}

proof=out
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
 if n in [4,5,9]:assert len(opts)==5;opts=[f'자료 {i}' for i in range(1,6)]
 if n==7:assert q['choiceNote']=='(가) → (나) → (다)'
 assert len(opts)==5 and all(norm(a)==norm(b) for a,b in zip(q['choices'],opts))
 assert q['answer']==keys[q['examDate']][n] and len(q['steps'])==len(q['optionReasons'])==5
 for s,prefix in zip(q['steps'],['착안점: ','실전 풀이: ','답 확정 기준: ','정석 근거: ','적용 한계: ']):assert s.startswith(prefix) and len(s)>40
 assert not any('\ue000'<=c<='\uf8ff' or c in '\ufffd\u2060\u2024' for c in json.dumps(q,ensure_ascii=False)),n
manifest=json.loads((A/'crop-manifest.json').read_text(encoding='utf-8'));assert len(manifest)==37
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
regions={1:[(1,0,109,946)],2:[(1,1,110,381)],3:[(1,1,555,888)],4:[(2,0,91,987),(2,1,50,462)],5:[(3,0,91,924),(3,1,50,545)],6:[(3,1,625,945)],7:[(4,0,111,820)],8:[(4,1,91,611)],9:[(5,0,109,843),(5,1,50,363)],10:[(5,1,438,914)]}
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
 if path.name in ['sets.json','data16.json']:continue
 obj=json.loads(path.read_text(encoding='utf-8'))
 if isinstance(obj,list):
  for q in obj:
   k=(q.get('examDate',q['source'][:10].replace('.','-')),q['subject'],q['number']);assert k not in seen;seen.add(k);old+=1
for q in bank:
 k=(q['examDate'],q['subject'],q['number']);assert k not in seen;seen.add(k)
for path,digest in json.loads((A/'before-data16-hashes.json').read_text(encoding='utf-8')).items():
 if path!='assets/psat/sets.json':assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
proof.update(status='PASS',count=10,officialFinalKeys=10,figures=37,originals=10,preservedExisting=old,limitations='Same-author source review with exact rational calculations and countermodels;not independent expert certification.')
(A/'content-checks.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PASS10source/key/37figures10originals;models;preserved',old)
