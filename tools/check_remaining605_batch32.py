import re
from itertools import product
from fractions import Fraction as F
from datetime import date
import pdfplumber
import review_remaining605 as r
b=r.folder(32);rows=r.read(b/'revealed-current.json');sources={x['id']:x for x in r.read(b/'blind-source.json')};own={x['id']:x for x in r.read(b/'own-solves.json')};checks=[]
norm=lambda s:re.sub(r'[\s①②③④⑤「」]','',s).replace('ㆍ','·')
tableRows={18:[['사탕','2'],['스티커','5'],['키링','8'],['인형','15'],['찻잔','20']],28:[['1개당 제작 소요시간','3시간','1시간'],['1개당 대금','10,000원','3,000원']],34:[['1','7','8'],['2','5','3'],['3','3','2']],37:[['1','천사 탱고','스피드 코리아 2026','겸손과 편견'],['2','거미의 예언','White 심리학','White 심리학'],['3','스피드 코리아 2026','AI 프롬프트','거미의 예언'],['4','White 심리학','호밀밭의 방관자','일관'],['5','일관','일관','호밀밭의 방관자'],['6','호밀밭의 방관자','실전 AI 에이전트 2','이타적 유전자 100가지']]}
tableRegex={18:r'경품 포인트\s*사탕 2\s*스티커 5\s*키링 8\s*인형 15\s*찻잔 20',28:r'구분 동작 이모티콘 정지 이모티콘\s*1개당 제작 소요시간 3시간 1시간\s*1개당 대금 10,000원 3,000원',34:r'라운드 A에 투표한 참가자 수 B에 투표한 참가자 수\s*1 7 8\s*2 5 3\s*3 3 2',37:r'<베스트셀러 순위>.*?(?=①)'}
for row in rows:
 q=row['question'];n=q['number'];m=sources[q['id']];native=re.sub(r'책형 \d+쪽','',m['sourceText']);native=re.sub(r'^.*?\b'+str(n)+r'[.]\s*','',native,count=1,flags=re.S)
 if n in tableRows:
  native,c=re.subn(tableRegex[n],'',native,flags=re.S);assert c==1
  assert q['tables'][0]['rows']==tableRows[n]
  assert q['tables'][0]['afterParagraph']=={18:5,28:0,34:5,37:5}[n]
  if n==37:
   with pdfplumber.open(r.ROOT/m['source']) as pdf:
    ts=pdf.pages[m['page']-1].extract_tables()
   expected=[q['tables'][0]['columns']]+tableRows[n]
   assert any([[norm(s or '') for s in rr] for rr in t]==[[norm(s) for s in rr] for rr in expected] for t in ts)
 if n==33:
  native,c=re.subn(r'甲공장 乙공장','',native);assert c==1 and q['choiceNote']=='甲공장 → 乙공장'
 if n==29:
  native=re.sub(r'[\ue000-\uf8ff]','',native)
  native,c=re.subn(r'쌀의.*?나에게 다오[.]','쌀의 1/5, 둘째 날은 1/4, 셋째 날은 1/2, 넷째 날은 4/5를 나에게 다오.',native,count=1,flags=re.S);assert c==1
 a,z=norm(native),norm(q['prompt']+q['body']+''.join(q['choices']))
 if a!=z:
  i=next((i for i,(u,v) in enumerate(zip(a,z)) if u!=v),min(len(a),len(z)));raise AssertionError((q['id'],i,a[max(0,i-20):i+100],z[max(0,i-20):i+100]))
 with pdfplumber.open(r.ROOT/row['officialKey']) as pdf:pi,t=next((i+1,p.extract_text()) for i,p in enumerate(pdf.pages) if '영역 상황판단' in (p.extract_text() or ''))
 assert q['examDate'][:4] in t and f"책형 {q['book']}" in t.replace('㉯','나')
 answers={}
 for line in t.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):v=list(map(int,line.split()));answers.update(zip(v[::2],v[1::2]))
 assert answers[n]==q['answer']==own[q['id']]['answer']
 checks.append(dict(id=q['id'],source=m['source'],page=m['page'],nativeAndFiveChoices=True,key=row['officialKey'],keyPage=pi,answer=q['answer'],tablesManuallyCompared=n in tableRows,bookTableCellsExactlyExtracted=n==37,fourFractionGlyphsManuallyCompared=n==29))
points=lambda n:n+(0 if n<6 else 2 if n<=10 else 5)
fish=[]
for a in range(20):
 if not(2<=points(a)<4<=points(a+1)):continue
 for bb in range(20):
  if not(10<=points(bb)<12<=points(bb)+points(a)-2):continue
  for c in range(20):
   if points(c)!=5:continue
   for d in range(20):
    if not(15<=points(d)<20):continue
    for e in range(20):
     if points(e)==16 and (points(d)-15)//2>1 and d>max(a,bb,c,e):fish.append([a,bb,c,d,e])
assert fish==[[3,9,5,14,11]] and sum(fish[0])==42
opt={}
for paid in [False,True]:
 possible=[(10000*x+3000*y-(12000 if paid else 0),x,y) for x,y in product(range(26),repeat=2) if F(4,5)*(3*x+y)<=20] if paid else [(10000*x+3000*y,x,y) for x,y in product(range(21),repeat=2) if 3*x+y<=20]
 opt[str(paid)]=max(possible)
assert opt=={'False':(66000,6,2),'True':(71000,8,1)}
factories=[]
for a in product('ABC',repeat=3):
 aa=[a[i%3] for i in range(15)]
 if aa[3]!='B' or any(x==y for x,y in zip(aa,aa[1:])):continue
 for bb in product('ABC',repeat=5):
  b15=[bb[i%5] for i in range(15)]
  if aa[5:10]!=b15[5:10] or not(b15.count('A')<b15.count('B') and b15.count('A')<b15.count('C')):continue
  factories.append(dict(first=a,second=bb,day14=[aa[13],b15[13]]))
assert len(factories)==1 and factories[0]['day14']==['A','C']
def survived(ca,cb,a,bb):return (ca,a) if ca>cb else (cb,bb) if cb>ca else (ca+cb,a+bb)
games=[]
for c1a,c1b in product(range(8),range(9)):
 c2,total2=survived(c1a,c1b,7,8)
 if total2!=8 or c2<3:continue
 for c2a,c2b in product(range(6),range(4)):
  if c2a+c2b!=c2:continue
  c3,total3=survived(c2a,c2b,5,3)
  if total3!=5 or c3<3:continue
  for c3a,c3b in product(range(4),range(3)):
   if c3a+c3b!=c3:continue
   final,totalFinal=survived(c3a,c3b,3,2)
   if final<=2:games.append(dict(initialSpies=15-c1a-c1b,citizenVotes=[[c1a,c1b],[c2a,c2b],[c3a,c3b]],finalCitizens=final))
minimum=min(x['initialSpies'] for x in games);assert minimum==6
books=tableRows[37];months=[[row[j] for row in books] for j in [1,2,3]];persistent=set(months[0][:5])&set(months[1][:5])&set(months[2][:5]);assert persistent=={'White 심리학','일관'}
owned=set();purchases=[]
for month,rank in enumerate(months):
 budget=3;buy=[];priority=[x for x in rank if x in persistent] if month==2 else []
 for title in priority+rank:
  price=1 if re.search('[A-Za-z0-9]',title) else 2
  if title not in owned and price<=budget:owned.add(title);buy.append(title);budget-=price
 assert budget==0;purchases.append(buy)
assert purchases==[['천사 탱고','스피드 코리아 2026'],['White 심리학','AI 프롬프트','실전 AI 에이전트 2'],['일관','이타적 유전자 100가지']]
rice=[]
for initial in [200,230,250,300,350]:
 h=F(initial);n=F(100);trace=[str(h)]
 for fraction,gift in zip([F(1,5),F(1,4),F(1,2),F(4,5)],[40,30,20,10]):
  giving=fraction*h;h-=giving;n+=giving;assert n>=gift;n-=gift;h+=gift;assert n+h==initial+100;trace.append(str(h))
 rice.append(dict(initial=initial,H=str(h),N=str(n),ratioMatches=n==9*h,trace=trace))
assert [x['initial'] for x in rice if x['ratioMatches']]==[250]
assert date(2024,11,29)>date(2024,11,23) and date(2027,4,10)<date(2027,10,10)
assert date(2024,3,10)>date(2023,4,10) and not 500<500 and F(300,2)<180
survivor=200*F(3,5);ownPension=80+survivor*F(3,10);assert survivor==120 and ownPension==116
r.write(b/'source-key-model-checks.json',dict(status='PASS',checks=checks,fish=fish,productionOptima=opt,periodicFactoryModels=factories,gameFeasiblePaths=games,minimumSpies=minimum,bookPurchases=purchases,ricePaths=rice,ruleChecks={'s21':'Consent ability exception distinct from minor;change permission,10-day optional reporting,deemed-license confirmation,spouse priority.','s22':'150 cap;employment start;foreign-national exclusion;3.5years possible;Nov29 after six-month Nov23.','s24':'500 inclusive,3years expired;400 excluded;debtor seller;inheritance not resale;30years expired.','s25':'Spouse before disabled child;120 versus116;20-year grandchild outside19;de-facto spouse before child.'},limitations='Same-author original-based formalization; hypothetical statutory passages, not real-world legal advice.'))
print('PASS10 native/key;4tables;fish/production/periods/game/books/rice and4rule evaluations.')
