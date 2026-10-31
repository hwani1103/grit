"""Batch08: source/native figures and independent finite constraint models."""
from pathlib import Path
from fractions import Fraction as F
import json,re,hashlib,shutil,subprocess
import pdfplumber
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/psat_remaining605_20261030/batch08'
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
  rectangles=[reg[f['asset']]['rect'] for f in q.get('figures',[])]
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
   pi,t=next((i+1,p.extract_text()) for i,p in enumerate(pdf.pages) if '영역 상황판단' in (p.extract_text() or ''))
  assert q['examDate'][:4] in t and f"책형 {q['book']}" in t
  answers={}
  for line in t.splitlines():
   if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
    z=list(map(int,line.split()));answers.update(zip(z[::2],z[1::2]))
  assert answers[q['number']]==q['answer']==solves[q['id']]['answer']
  checks.append(dict(id=q['id'],source=m['source'],sourcePage=m['page'],actualSide=m['side'],questionTop=marker['top'],nativeTextAndFiveChoicesMatch=True,continuation=m['columnContinuation'],choiceHeading=heading,key=row['officialKey'],keyPage=pi,answer=answers[q['number']]))
  for f in q.get('figures',[]):
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

from itertools import product,combinations,permutations
import datetime
scoreCandidates=[v for v in product([70,30],[70,30],[60,40],[60,40],[80,20]) if sum(v)==300 and sum(x<50 for x in v)==2]
assert scoreCandidates==[(70,70,40,40,80)]
calendar=[]
for april1 in range(7): # Monday0
 weekday=lambda d:(april1+d-1)%7
 lastSun=max(d for d in range(1,31) if weekday(d)==6)
 for date in [12,13,14]:
  days=[5,11,date,15,lastSun-1,lastSun]
  if weekday(date)==2 and days==sorted(days) and len({weekday(d) for d in days})==6:
   calendar.append(dict(april1Weekday=april1,dates=days,weekdays=[weekday(d) for d in days]))
assert len(calendar)==1 and calendar[0]['dates']==[5,11,13,15,23,24] and calendar[0]['weekdays'][0]==1
seating=[]
for seats in permutations('ABCD'): # frontleft,frontright,backleft,backright
 pos={name:i for i,name in enumerate(seats)}
 if pos['A']<2 or pos['D']<2 or pos['C']>=2:continue
 absentDay2=seats[pos['A']-2]
 if absentDay2=='B':continue
 absentDay3=seats[pos['C']+2];presentDay4={seats[pos['D']-2],'D'}
 attendance={x:2+int(x!=absentDay2)+int(x!=absentDay3)+int(x in presentDay4) for x in 'ABCD'}
 seating.append(dict(seats=seats,attendance=attendance))
assert len(seating)==2 and all(s['attendance']==dict(A=3,B=5,C=3,D=5) for s in seating)
def matchings(ns):
 if not ns:yield [];return
 first,*rest=ns
 for j,second in enumerate(rest):
  for pairs in matchings(rest[:j]+rest[j+1:]):yield [(first,second)]+pairs
constantDiff={}
for pairs in matchings(list(range(1,11))):
 diffs={abs(a-b) for a,b in pairs}
 if len(diffs)==1:constantDiff.setdefault(next(iter(diffs)),[]).append(pairs)
assert sorted(constantDiff)==[1,5]
water=0;timeline=[]
for i in range(1,75):
 date=datetime.date(2024,3,1)+datetime.timedelta(days=i-1);before=water;uncapped=water+900;water=min(10000,uncapped)
 timeline.append(dict(date=date.isoformat(),before=before,afterFill=water,uncapped=uncapped))
 if uncapped>=10000:break
 used=300 if date<=datetime.date(2024,3,5) else 500 if date<=datetime.date(2024,3,10) else 700
 water-=used+int(date==datetime.date(2024,3,15))*1000
assert timeline[-1]==dict(date='2024-04-06',before=9200,afterFill=10000,uncapped=10100)
assert timeline[-2]['afterFill']==9900 and max(r['afterFill'] for r in timeline[:-1])<10000
firstFour=[[1,0,1,1],[1,0,1,0],[1,1,0,0],[0,1,1,0]];counts=[sum(row[j] for row in firstFour) for j in range(4)]
base=[sum(F(4,counts[j]) for j in range(4) if row[j]) for row in firstFour];assert base==[F(20,3),F(8,3),F(10,3),F(10,3)]
last=[]
for five,six in product(combinations(range(4),2),repeat=2):
 score=[base[i]+2*int(i in five)+2*int(i in six) for i in range(4)];assert sum(score)==24
 last.append(dict(five=five,six=six,scores=score,allPass=all(v>=5 for v in score)))
assert max(row['scores'][0] for row in last)==F(32,3) and any(row['allPass'] for row in last)
# Four selected floors4,5,6,7 are interchangeable with any other two distinct>=6.
presses=[]
def compositions(total,n):
 if n==1:yield (total,);return
 for a in range(total+1):
  for tail in compositions(total-a,n-1):yield (a,)+tail
for v in compositions(10,5):
 if all(x%2==1 for x in v[:4]) and v[4]%2==0:
  assert all(any(y>=2 for j,y in enumerate(v) if i!=j) for i,x in enumerate(v) if x==5)
  presses.append(v)
assert (1,3,3,3,0) in presses and (3,3,1,1,2) in presses
assert sum([1,3,3,3,0])==sum([3,3,1,1,2])==10
correction=read(OUT/'post-reveal-reasoning-correction.json');assert len(correction['all144OutgoingCombinations'])==1
result=dict(status='PASS',officialKeysAndNative=checks,figurePixels=pixels,scorePossibilities=scoreCandidates,calendar=calendar,seating=seating,
 constantDifferenceMatchings=constantDiff,waterTimeline=timeline,baseScores=base,lastTwoCombinations=len(last),allPassExample=next(row for row in last if row['allPass']),maximumA=F(32,3),
 toggle=dict(countVectorsTested=len(presses),claim2All=True,claim3Counter=(1,3,3,3,0),claim4Counter=(3,3,1,1,2),claim1Counter='one person performs all10 operations'),
 contactGraph=correction['all144OutgoingCombinations'],ownReasoningCorrection='post-reveal-reasoning-correction.json',
 qualitativeChecks={'2023s03':'appointpolicechief;uniform+IDboth;penaltyonlyelection3;donationillegal+request mandatorydismiss.', '2023s05':'Mayplant/Octharvest;winterday/summerhalfday;heatingremovesodor;coagulate soyprotein in milk,not residue.'},
 limitations='Same-author review. Contactgraph initial invalid countermodel corrected after authored explanation reveal, not claimed unaided first-pass correct reasoning. No independent expert or realdevice validation.')
(OUT/'source-key-model-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2,default=str)+'\n',encoding='utf-8')
print('PASS10direct source/keys,4freshpixelcrops,32scores/7calendars/24seats/945matchings/36scorings/toggle/contact models.')
