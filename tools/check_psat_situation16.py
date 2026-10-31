from pathlib import Path
import json,re,hashlib,itertools as it,pdfplumber
from PIL import Image
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/situation16';P=R/'assets/psat/situation16.json'
bank=json.loads((P if P.exists() else A/'authored-situation16.json').read_text(encoding='utf-8'));tr=json.loads((A/'source-transcripts.json').read_text(encoding='utf-8'))
assert [(q['examDate'],q['number']) for q in bank]==[('2026-03-07',n) for n in [14,15,18,27,28,33,34,35,37,38]]
import collections
proof={}
# All collinear sign patterns attain the triangle-inequality global bounds.
r=[5,10,15,20,25];ds=[]
for signs in it.product([-1,1],repeat=5):
 x=[0]+[a*b for a,b in zip(r,signs)];ds.append(sum(abs(a-b) for a,b in zip(x,x[1:])))
assert min(ds)==25 and max(ds)==125;proof['14']={'minDistance':25,'maxDistance':125,'differenceHours':4,'signPatterns':32,'globalBound':'sum absolute radius differences <= distance <= sum adjacent radii;both attained'}
rounds=[r for r in range(2,52) if 51%r==0 and 51//r>=6];assert rounds==[3];sol=[]
for z in range(1,17):
 for y in range(z+1,17):
  x=17-y-z
  if x<=y:continue
  for rows in it.product(list(it.permutations([x,y,z])),repeat=3):
   if rows[-1][1]==x and [sum(r[i] for r in rows) for i in range(3)]==[20,16,15]:sol.append(dict(scores=[x,y,z],rows=rows))
assert len(sol)==1 and sol[0]['rows'][1][1]==4;proof['15']=sol
points=lambda n:n+(0 if n<=5 else 2 if n<=10 else 5)
cands=[]
for a,b,c,d,e in it.product(range(15),repeat=5):
 pa,pb,pc,pd,pe=map(points,[a,b,c,d,e])
 if not(2<=pa<4 and points(a+1)>=4 and 10<=pb<12 and pb-10+pa-2>=2 and pc==5 and 15<=pd<20 and (pd-15)//2>1 and pe==16 and d>max(a,b,c,e)):continue
 cands.append([a,b,c,d,e])
assert cands==[[3,9,5,14,11]];proof['18']={'fish':cands[0],'points':list(map(points,cands[0])),'sum':42,'allAssignments0to14':15**5}
ages=[x for x in it.combinations_with_replacement(range(1,37),3) if x[0]*x[1]*x[2]==36];groups=collections.defaultdict(list)
for x in ages:groups[sum(x)].append(x)
ambiguous={k:v for k,v in groups.items() if len(v)>1};remaining=[x for v in ambiguous.values() for x in v if x[2]>x[1]];assert remaining==[(2,2,9)];proof['27']={'all':ages,'ambiguousSums':dict(ambiguous),'answer':9}
best=[]
for paid,H in [(False,20),(True,25)]:
 opts=[dict(x=x,y=y,profit=10000*x+3000*y-(12000 if paid else 0)) for x in range(H//3+1) for y in range(H+1) if 3*x+y<=H]
 best.append(max(opts,key=lambda x:x['profit']))
assert [b['profit'] for b in best]==[66000,71000];proof['28']=best
models=[]
for c3 in it.product('ABC',repeat=3):
 a=[c3[(d-1)%3] for d in range(1,31)]
 if any(x==y for x,y in zip(a,a[1:])) or a[3]!='B':continue
 for c5 in it.product('ABC',repeat=5):
  b=[c5[(d-1)%5] for d in range(1,31)]
  if a[5:10]!=b[5:10]:continue
  counts=[b[:15].count(x) for x in 'ABC']
  if not(counts[0]<counts[1] and counts[0]<counts[2]):continue
  models.append(dict(c3=c3,c5=c5,answer=[a[13],b[13]],counts=counts))
assert len(models)==1 and models[0]['answer']==['A','C'];proof['33']=models
roundModels=[]
# survivor counts force B in round1, A in round2; enumerate all citizen allocations.
for a1,b1 in it.product(range(8),range(9)):
 if b1<=a1 or b1<3:continue
 for a2,b2 in it.product(range(6),range(4)):
  if a2+b2!=b1 or a2<=b2 or a2<3:continue
  for a3,b3 in it.product(range(4),range(3)):
   if a3+b3!=a2:continue
   survivedCit=a3+b3 if a3==b3 else max(a3,b3)
   if survivedCit>2:continue
   roundModels.append(dict(citizens=[[a1,b1],[a2,b2],[a3,b3]],spies=15-a1-b1))
assert min(m['spies'] for m in roundModels)==6;proof['34']={'modelCount':len(roundModels),'minSpies':6,'witness':next(m for m in roundModels if m['spies']==6),'all':roundModels}
stoneModels=[]
for blacks in it.combinations(range(12),5):
 row=['B' if i in blacks else 'W' for i in range(12)]
 if row[0]!='W' or row[-1]!='W' or row[2]!='B':continue
 good=True
 for i,j in it.combinations(range(12),2):
  if row[i]!=row[j]:continue
  mid=row[i+1:j];b=mid.count('B');w=mid.count('W')
  if (row[i]=='B' and w!=b+1) or (row[i]=='W' and b not in [w,w+1]):good=False;break
 if good:stoneModels.append(''.join(row))
assert stoneModels==['WWBWBWBWBWBW'];proof['35']={'all792PlacementsChecked':True,'models':stoneModels,'optionTruth':[False,False,False,False,True]}
ranks=[['천사 탱고','거미의 예언','스피드 코리아 2026','White 심리학','일관','호밀밭의 방관자'],['스피드 코리아 2026','White 심리학','AI 프롬프트','호밀밭의 방관자','일관','실전 AI 에이전트 2'],['겸손과 편견','White 심리학','거미의 예언','일관','호밀밭의 방관자','이타적 유전자 100가지']]
import re
cost=lambda title:1 if re.search('[A-Za-z0-9]',title) else 2
owned=set();purchases=[];priority=set.intersection(*(set(r[:5]) for r in ranks))
for month in range(3):
 budget=3;buy=[];queue=(sorted(priority) if month==2 else [])+ranks[month]
 for title in queue:
  if title not in owned and cost(title)<=budget:budget-=cost(title);owned.add(title);buy.append(title)
 assert budget==0;purchases.append(buy)
assert purchases==[['천사 탱고','스피드 코리아 2026'],['White 심리학','AI 프롬프트','실전 AI 에이전트 2'],['일관','이타적 유전자 100가지']]
proof['37']={'ranks':ranks,'priority':sorted(priority),'purchases':purchases,'notBought':'호밀밭의 방관자'}
raw=[[14.3,1.6,21.1,82],[15.1,1.9,23.5,86],[13,2.1,19.5,89],[11.5,2.2,24.1,90],[14.1,2,20.1,84]];thresholds=[[15,12,9,6],[2,1.5,1,.5],[25,20,15,10],[90,80,70,60]]
score=lambda v,ts:next((20-3*i for i,t in enumerate(ts) if v>=t),8)
scores=[[score(v,ts) for v,ts in zip(row,thresholds)] for row in raw];totals=list(map(sum,scores));order=sorted(range(5),key=lambda i:(totals[i],scores[i][1],scores[i][0],scores[i][2],scores[i][3]),reverse=True)
assert totals==[68,71,68,71,71] and order[0]==4
proof['38']={'raw':raw,'scores':scores,'totals':totals,'winnerIndex':4,'boundary2percent':score(2,thresholds[1])}
keys={}
for post,date,year,book in [(5982,'2026-03-07','2026','㉯')]:
 with pdfplumber.open(next((R/f'artifacts/psat600_20261028/sources/{post}').glob('*.pdf'))) as pdf:
  t=next(p.extract_text() for p in pdf.pages if '영역 상황판단' in p.extract_text());assert year in t and book in t;k={}
  for line in t.splitlines():
   if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
    v=list(map(int,line.split()));k.update(zip(v[::2],v[1::2]))
  assert len(k)==(40 if post==5982 else 25);keys[date]=k
def norm(s):
 s=re.sub(r'\uf000([^\uf000]+)\uf000',r'『\1』',s)
 return re.sub(r'[\s·․]+','',s.replace('\uf000','『').replace('\uf001','』'))
tableSources=json.loads((A/'table-source-text.json').read_text(encoding='utf-8'))

rawTables={int(k):v for k,v in tableSources.items()}
expectedTables={
18:[(['경품','포인트'],[['사탕','2'],['스티커','5'],['키링','8'],['인형','15'],['찻잔','20']])],
28:[(['구분','동작 이모티콘','정지 이모티콘'],[['1개당 제작 소요시간','3시간','1시간'],['1개당 대금','10,000원','3,000원']])],
34:[(['라운드','A에 투표한 참가자 수','B에 투표한 참가자 수'],[['1','7','8'],['2','5','3'],['3','3','2']])],
37:[(['순위','2025년 12월','2026년 1월','2026년 2월'],[[str(i+1)]+[r[i] for r in ranks] for i in range(6)])],
38:[(['구분','점수'],[['15% 이상','20'],['12% 이상 15% 미만','17'],['9% 이상 12% 미만','14'],['6% 이상 9% 미만','11'],['6% 미만','8']]),
(['구분','점수'],[['2.0% 이상','20'],['1.5% 이상 2.0% 미만','17'],['1.0% 이상 1.5% 미만','14'],['0.5% 이상 1.0% 미만','11'],['0.5% 미만','8']]),
(['구분','점수'],[['25% 이상','20'],['20% 이상 25% 미만','17'],['15% 이상 20% 미만','14'],['10% 이상 15% 미만','11'],['10% 미만','8']]),
(['구분','점수'],[['90점 이상','20'],['80점 이상 90점 미만','17'],['70점 이상 80점 미만','14'],['60점 이상 70점 미만','11'],['60점 미만','8']]),
(['기업','고용 증가(%)','지역사회 공헌도(%)','탄소배출 감소(%)','공급망 윤리성(점)'],[['甲','14.3','1.6','21.1','82'],['乙','15.1','1.9','23.5','86'],['丙','13.0','2.1','19.5','89'],['丁','11.5','2.2','24.1','90'],['戊','14.1','2.0','20.1','84']])]}
for q in bank:
 n=q['number'];src=tr[q['id']]
 assert norm(q['prompt'])==norm(src['prompt']),(n,'prompt')
 assert len(q['choices'])==5 and all(norm(x)==norm(y) for x,y in zip(q['choices'],src['choices'])),(n,'choices')
 originalBody=norm(src['body'])
 if n==33:
  assert originalBody.endswith(norm('甲공장 乙공장'));originalBody=originalBody.removesuffix(norm('甲공장 乙공장'));assert q['choiceNote']=='甲공장 → 乙공장'
 for rawTable in rawTables.get(n,[]):
  assert originalBody.count(norm(rawTable))==1;originalBody=originalBody.replace(norm(rawTable),'',1)
 assert len(q['tables'])==len(expectedTables.get(n,[]))
 for table,(columns,rows) in zip(q['tables'],expectedTables.get(n,[])):
  assert table['columns']==columns and table['rows']==rows,(n,'table cells')
  assert 0<=table['afterParagraph']<len(q['body'].split('\n\n'))
 if n==38:assert len({t['afterParagraph'] for t in q['tables'][:4]})==1 and q['tables'][4]['afterParagraph']>q['tables'][0]['afterParagraph']
 assert norm(q['body'])==originalBody,(n,'body')
 assert q['answer']==keys[q['examDate']][n] and len(q['steps'])==len(q['optionReasons'])==5
 assert not any('\ue000'<=c<='\uf8ff' or c in '\ufffd\u2060\u2024' for c in json.dumps(q,ensure_ascii=False)),n
 assert not re.search(r'\d{4}\.\s*\n\s*\n\s*\d{1,2}\.',q['body'])
for c in json.loads((A/'crop-manifest.json').read_text(encoding='utf-8')):
 source=R/c['source'];assert hashlib.sha256(source.read_bytes()).hexdigest()==c['sha256']
 with pdfplumber.open(source) as pdf:
  ref=pdf.pages[c['page1based']-1].crop(c['rect']).to_image(resolution=c['resolution'],antialias=True).original.convert('RGB');path=R/c['asset'] if P.exists() else A/'staged'/c['asset'];im=Image.open(path).convert('RGB');assert im.size==ref.size and im.tobytes()==ref.tobytes(),c['asset']
seen=set();old=0
for path in (R/'assets/psat').glob('*.json'):
 if path.name in ['sets.json','situation16.json']:continue
 obj=json.loads(path.read_text(encoding='utf-8'))
 if isinstance(obj,list):
  for q in obj:
   k=(q.get('examDate',q['source'][:10].replace('.','-')),q['subject'],q['number']);assert k not in seen;seen.add(k);old+=1
for q in bank:
 k=(q['examDate'],q['subject'],q['number']);assert k not in seen;seen.add(k)
for path,digest in json.loads((A/'before-situation16-hashes.json').read_text(encoding='utf-8')).items():
 if path!='assets/psat/sets.json':assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
proof.update(status='PASS',count=10,officialFinalKeys=10,sourceComparison='native prompt/body/choices;9native tables including four transposed rubric tables/choice header/10originalpixels',preservedExisting=old,limitations='Same-author semantic review with logical countermodels;not independent expert review.')
(A/'content-checks.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PASS10source/key/10pixels;models;preserved',old)
