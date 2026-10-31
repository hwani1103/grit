import itertools as it
from fractions import Fraction as F
from psat_batch_tools import validate,read,ROOT
def lis(seq):
 d=[]
 for x in seq:d.append(1+max([d[i] for i in range(len(d)) if seq[i]<x],default=0))
 return max(d)
assert 7-lis([2,4,1,5,7,6,3])==3
assert max(7-lis(s) for s in it.permutations(range(1,8)))==6
assert 7-lis([2,3,4,1,5,6,7])==1 and 7-lis([2,1,3,4,5,6,7])==1
ways={p:[(h,b) for h in range(7) for b in range(7) if 3*h+2*b==p] for p in range(2,14)}
solutions=[]
for a1,a2,b1,b3 in it.product(range(2,7),repeat=4):
 if a1+a2+7!=13 or b1+5+b3!=13 or not(a1>b1 and a2<5 and 7>b3):continue
 for ar in it.product(ways[a1],ways[a2],ways[7]):
  for br in it.product(ways[b1],ways[5],ways[b3]):
   ha=sum(h+b for h,b in ar);hb=sum(h+b for h,b in br)
   if ha<hb:solutions.append(dict(A=[a1,a2,7],B=[b1,5,b3],A_hits=ha,B_hits=hb))
assert len(solutions)==1 and solutions[0]==dict(A=[3,3,7],B=[2,5,6],A_hits=5,B_hits=6)
assert F('0.02')*1000/F('2.5')==8
assert F(20,1)/F(80,64)==16
groups=[]
for lone in range(1,8):
 left=set(range(1,8))-{lone}
 for a in it.combinations(left,3):
  b=left-set(a)
  if sum(a)==sum(b) and sum(a)%2:groups.append([lone,list(a),sorted(b)])
assert {g[0] for g in groups}=={2,6}
def response(kind,other,ate):
 if kind=='C':kind=other
 return ate if kind=='B' else not ate
worlds=[]
for a,b in it.permutations('ABC',2):
 for ma,mb in it.product([False,True],repeat=2):
  if response(b,a,mb) and not response(a,b,ma):worlds.append(dict(A=a,B=b,AteA=ma,AteB=mb))
assert any(w['A']=='A' and w['B']=='B' and w['AteB'] for w in worlds)
assert any(w['A']=='A' and w['B']=='C' and w['AteA'] for w in worlds)
assert any(not w['AteA'] and not w['AteB'] for w in worlds)
field=['화학','건축','건축','화학','보건복지'];months=[70,96,68,60,49];training=[15,11,8,9,2];done=[30,10,4,14,25]
pairs=[(0,1),(0,2),(1,3),(2,3),(2,4)]
tests=[[field[i]!=field[j],months[i]+months[j]>=120,max(training[i],training[j])>=10,abs(done[i]-done[j])<=10] for i,j in pairs]
assert [all(v) for v in tests]==[False,False,True,False,False]
lottery=[(F(3,10)*s+10)*F(3,5)*F(7,10) for s in [150,180,215,300,330]]
assert lottery==list(map(F,['23.1','26.88','31.29','42','45.78']))
bank=read(ROOT/'artifacts/psat600_20261028/situation19/authored-situation19.json')
assert len(bank[1]['tables'][0]['rows'])==3 and len(bank[6]['tables'][0]['rows'])==5
for i in [2,3]:assert '0.02' in bank[i]['body'] and '光' not in bank[i]['body'] and 'μ' in bank[i]['body']
proof={'11':{'truth':[True,False,True,False],'permutations':5040,'maximumMinMoves':6},'12':solutions,'19':{'poreMinimumMicrometers':20,'maxDust':2.5,'ratio':8},'20':{'massRatio':'1:4','particleMassRatio':'1:64','countRatio':'16:1'},'31':groups,'32':{'truth':[False,False,True],'worlds':worlds},'36':{'completeCounts':done,'conditionsByOption':tests},'39':{'lumpSumRatio':'0.6beforeTax','answer':5},'40':{'optionPostTax':list(map(str,lottery))},'2025-1':{'normalProcedure':'Minister hears opinions, committee deliberates, minister finalizes/notifies','exceptionCostPercent':15,'changePercent':20,'answer':5},'originalVisualReview':'Ten columns read; common19/20 and39/40 passage+right prompts matched; tables3+5rows inspected.'}
validate('situation19',proof,[('2026-03-07',n) for n in [11,12,19,20,31,32,36,39,40]]+[('2025-03-08',1)])
