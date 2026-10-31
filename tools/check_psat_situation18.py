from fractions import Fraction as F
from psat_batch_tools import validate,read,ROOT
proof={'originalReview':'All ten original columns visually read; law1-5 actor/scope/may/must/hearing and original quotes matched.'}
assert F(10)*F(20,100)==2
x=F(200-65,5);assert (x,2*x,x+40,x+25)==(27,54,67,52)
budgets=[(b,min(1000,1080-4*b),min(1000,400+12*b)) for b in range(121)]
assert min(b for b,a,c in budgets if c>a)==43
def state(v,t):
 z=v*t%20
 return (z,1) if z<10 else (20-z,-1)
events=[]
for a,b in [(8,10),(8,12),(10,12)]:
 found=[]
 for k in range(1,10):
  t=F(20*k,a+b)
  if t>F(5,2):break
  sa,sb=state(a,t),state(b,t)
  assert sa[0]==sb[0] and sa[1]!=sb[1] and 0<sa[0]<10
  found.append(str(t))
 assert len(found)==2
 events.append([a,b,found])
flowers=[('장미','빨강',7,12000),('백합','하양',3,6000),('팬지','보라',5,9000),('카네이션','빨강',8,10000),('데이지','하양',10,7000)]
def price(f,d):
 n,c,h,p=f
 if n=='장미' and 1<=d<=7:p=p*70//100
 if n=='백합' and 10<=d<=20:p=p*150//100
 if n=='카네이션' and 8<=d<=15:p=p*85//100
 return p
d=1;last=None;buys=[]
while d<=31:
 f=min((f for f in flowers if f[1]!=last),key=lambda f:price(f,d))
 buys.append((d,f[0],price(f,d)));last=f[1];d+=f[2]+1
assert buys==[(1,'백합',6000),(5,'장미',8400),(13,'데이지',7000),(24,'팬지',9000),(30,'백합',6000)]
assert d==34 and all(v<10000 for _,_,v in buys)
bank=read(ROOT/'artifacts/psat600_20261028/situation18/authored-situation18.json')
table=bank[9]['tables'][0];assert len(table['rows'])==5 and table['columns']==['종류','색깔','보유기간','1개당 가격','비고']
assert [r[:4] for r in table['rows']]==[[n,c,str(h)+'일',format(p,',')+'원'] for n,c,h,p in flowers]
assert bank[8]['choiceNote']=='甲 → 丙'
assert '청문을 하여야 한다' in bank[2]['body'] and '「민법」' in bank[2]['body']
proof.update(ownAnswers=[3,4,2,5,1,1,3,3,2,1],budget=[27,54,67,52],minimumB=43,reflectedOppositeMeetings=events,flowerPurchases=buys,nextJuneDay=3,legalTruthSets={'q3':['ㄱ','ㄴ'],'q5':'ability+prosecutorRequest+courtOrder;paidImmediateRelease'},nativeTableRows=5)
validate('situation18',proof,[('2026-03-07',i) for i in range(1,11)])
