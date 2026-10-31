import re
from fractions import Fraction as F
from itertools import permutations,combinations
import pdfplumber
import review_remaining605 as r
b=r.folder(35);rows=r.read(b/'revealed-current.json');src={x['id']:x for x in r.read(b/'blind-source.json')};own={x['id']:x for x in r.read(b/'own-solves.json')}
norm=lambda s:re.sub(r'[\s①②③④⑤「」]','',s).replace('ㆍ','·')
checks=[]
for row in rows:
 q=row['question'];m=src[q['id']];s=re.sub(r'책형\s*\d+쪽','',m['sourceText']);s=re.sub(r'^\s*\d+[.]\s*','',s)
 if q['number']==9:
  s,n=re.subn(r'\n甲 丙\n','\n',s);assert n==1
 if q['number']==10:
  table=re.search(r'종류 색깔 보유기간 1개당 가격 비고.*?(?=<보 기>)',s,re.S);assert table
  s=s[:table.start()]+s[table.end():]
  t=q['tables'][0];assert t['columns']==['종류','색깔','보유기간','1개당 가격','비고'] and t['afterParagraph']==3
  assert t['rows']==[['장미','빨강','7일','12,000원','5/1 ～ 5/7 가정의 달 30% 할인 행사'],['백합','하양','3일','6,000원','5/10 ～ 5/20 수급 어려움으로 50% 가격 인상'],['팬지','보라','5일','9,000원','－'],['카네이션','빨강','8일','10,000원','5/8 ～ 5/15 어버이날 및 스승의 날 15% 할인 행사'],['데이지','하양','10일','7,000원','－']]
  assert q['body'].split('\n\n')[3]=='다음은 꽃집에서 판매하는 꽃다발에 대한 정보이다.'
 assert norm(s)==norm(q['prompt']+q['body']+''.join(q['choices'])),q['id']
 with pdfplumber.open(r.ROOT/row['officialKey']) as pdf:pi,t=next((i+1,p.extract_text()) for i,p in enumerate(pdf.pages) if '영역 상황판단' in (p.extract_text() or ''))
 assert '2026' in t and '책형 나' in t.replace('㉯','나')
 ans={}
 for line in t.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
   z=list(map(int,line.split()));ans.update(zip(z[::2],z[1::2]))
 assert ans[q['number']]==q['answer']==own[q['id']]['answer'];checks.append(dict(id=q['id'],source=m['source'],page=m['page'],nativeFiveChoices=True,answer=q['answer'],key=row['officialKey'],keyPage=pi))
# Exhaustive integer cap check, not just the intersection of uncapped lines.
budgets=[dict(b=n,A=min(1000,1080-4*n),B=min(1000,400+12*n)) for n in range(121)]
assert min(x['b'] for x in budgets if x['B']>x['A'])==43
assert 54+27+67+52==200 and 52==67-15 and 10*F(1,5)==2
# Piecewise physical trajectories independently intersected with rational times.
end=F(5,2);speeds=[8,10,12];events=[]
def pos(v,t):
 u=v*t%20;return u if u<=10 else 20-u
def velocity(v,t):return v if int(v*t/10)%2==0 else -v
for a,c in combinations(speeds,2):
 cuts=sorted({F(0),end}|{F(10*k,v) for v in [a,c] for k in range(1,5) if 0<F(10*k,v)<end});times=[]
 for lo,hi in zip(cuts,cuts[1:]):
  mid=(lo+hi)/2;va,vc=velocity(a,mid),velocity(c,mid)
  if va==vc:continue
  t=mid+(pos(c,mid)-pos(a,mid))/(va-vc)
  if lo<t<hi and va*vc<0:times.append(t)
 assert len(times)==2
 assert all(pos(a,t)==pos(c,t) for t in times);events.append(dict(pair=[a,c],times=list(map(str,times))))
assert events==[dict(pair=[8,10],times=['10/9','20/9']),dict(pair=[8,12],times=['1','2']),dict(pair=[10,12],times=['10/11','20/11'])]
# Simulate cheapest eligible purchase including all promotion boundaries.
flowers=[('장미','빨강',7,12000),('백합','하양',3,6000),('팬지','보라',5,9000),('카네이션','빨강',8,10000),('데이지','하양',10,7000)]
def cost(name,day,p):
 if name=='장미' and 1<=day<=7:return p*7//10
 if name=='백합' and 10<=day<=20:return p*3//2
 if name=='카네이션' and 8<=day<=15:return p*85//100
 return p
day=1;color=None;purchases=[]
while day<=31:
 choices=sorted((cost(n,day,p),n,c,l) for n,c,l,p in flowers if c!=color);price,name,color,life=choices[0];assert choices[0][0]<choices[1][0]
 purchases.append([day,name,price]);day+=life+1
assert purchases==[[1,'백합',6000],[5,'장미',8400],[13,'데이지',7000],[24,'팬지',9000],[30,'백합',6000]] and day==34
# Constructive sorting of all5040 permutations; preserve the highest pencil.
def restore(p):
 a=list(p);moves=0
 for n in range(6,0,-1):
  if a.index(n)+1==a.index(n+1):continue
  a.remove(n);a.insert(a.index(n+1),n);moves+=1
 assert a==list(range(1,8));return moves
allMoves=[restore(p) for p in permutations(range(1,8))];assert max(allMoves)==6
a=[2,4,1,5,7,6,3]
for n,idx in [(1,0),(3,2),(7,6)]:a.remove(n);a.insert(idx,n)
assert a==list(range(1,8))
r.write(b/'source-key-model-checks.json',dict(status='PASS',checks=checks,budgetBoundary=[budgets[42],budgets[43]],budgetCompleteDomain=121,physicalTrajectoryEvents=events,purchases=purchases,permutationCount=len(allMoves),constructiveMaxMoves=max(allMoves),legalSemantics={'s02':'Belowground/risk scope; notice not permission; individual lump sum; temporary use permitted.','s03':'All designation requirements; false designation mandatory cancellation with hearing; false funding discretionary.','s04':'Optional research/theft versus mandatory fire/export; dismantler/exporter substitution; export report.','s05':'Same-day appeal within7; ability conjunction; prosecutor/prison jurisdiction; tax chief disclosure; immediate release after payment.'},limitations='Same-author source/model review; native table checked against source image. No device validation.'))
print('PASS10 source/key/own;121 capped budgets;6 exact meetings;5 purchases;5040 constructed sorts')
