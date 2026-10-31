import itertools as it
from fractions import Fraction as F
import review_remaining605 as r
b=r.folder(44);out={}
assert 275*4-90*6==560 and F(560)*3/8==210
out['28']=dict(day=210,afterFlood=280,subsequentSaving=260,winterNeed=540)
days=[n for n in range(1,1000) if set(str(37*n))=={'9'}];assert min(days)==27;out['29']=dict(minimum=27,smallerTotals=[9,99])
teams=[(2,1,2,1),(2,2,1,1),(1,1,1,3)];moves=[(-1,1,0,0),(0,-1,0,1),(1,0,0,-1)]
for t,d in zip(teams,moves):
 a,b1,c,d1=[x+y for x,y in zip(t,d)];assert min(a,b1,c,d1)>=0 and a+b1==c+d1==a+c==b1+d1==3
out['30']=dict(total=18,feasibleCrossCells=teams)
words=['apple','banana','cherry','grape','orange','peach'];letters=sorted(set(''.join(words)))
pairs=[(a,b1) for a,b1 in it.combinations(letters,2) if sum(a in w or b1 in w for w in words)==4]
assert not any('a' in p for p in pairs) and ('c','n') in pairs and [p for p in pairs if 'o' in p]==[('o','p')];out['32']=dict(validPairs=pairs)
def penetrated(order,power):
 n=0
 for d in order:
  if power<d:break
  power-=d;n+=1
 return n
valid=[p for p in it.permutations(range(1,6)) if penetrated(p,8)==3 and penetrated([p[j] for j in [1,4,0,2,3]],3)==2 and penetrated([p[j] for j in [4,3,2,1,0]],8)==2]
assert valid==[(3,1,4,5,2),(4,1,3,5,2)];out['33']=dict(valid=valid)
def lifts(f):return {1 if f%2==0 else 2,3 if f<=5 else 4}
valid=[]
for a,e,c,d,w in it.permutations(range(2,11),5):
 if not (6<=a<e and e%2==0 and w<=3):continue
 if lifts(c)&lifts(e) or not(lifts(c)&lifts(w)):continue
 if lifts(d)&lifts(w) or not all(lifts(d)&lifts(x) for x in [a,e,c]):continue
 valid.append((a,e,c,d,w))
possible=[sorted({p[j] for p in valid}) for j in range(5)];assert possible[-1]==[2] and all(len(x)>1 for x in possible[:4]);out['34']=dict(count=len(valid),possibleFloors=possible,valid=valid)
valid=[]
for a,c,d,e in it.product(range(1,10),repeat=4):
 seq=[a,c,14,d,e]
 if len(set(seq))!=5 or [x%2 for x in seq]!=[0,1,0,0,0]:continue
 rem=[49-sum(seq[:j+1]) for j in range(5)]
 if [x%3==0 for x in rem]!=[True,True,False,False,False]:continue
 if min(rem[:4])>=25 and rem[-1]<25:valid.append(seq)
assert valid==[[4,3,14,2,6]];out['35']=dict(valid=valid)
stars=[[3.5,3,3,4],[3.5,5,4.5,3.5],[2,1.5,3,2],[3.5,2.5,2,4],[2,3,4,3]]
rank=[(2*(s[1]+s[3])-s[0]-s[2],s[3],s[1],-s[2],i) for i,s in enumerate(stars) if s[0]+s[2]<=7]
assert max(rank)[-1]==0;out['36']=dict(stars=stars,eligibleRanks=rank,boundary='Exactly7 is eligible; priority order is lexicographic.')
cost=[50+350*.2+20,60+300*.2+20,80+150*.2+20,120+20,140];assert cost[1:]==[140,130,140,140];out['37']=dict(costThousand=cost,eligible=[1,2,3,4],winner=2)
practice=[[75,70,80],[75,65,75],[85,55,90],[65,85,80],[80,75,90]];interview=[[70,90,85],[75,80,80],[80,90,75],[80,75,85],[70,75,75]]
selected=sorted((sum(sorted(s)[1:]),i) for i,s in enumerate(practice) if min(s)>60)[-3:]
final=[(sum(practice[i])+sum(interview[i]),sum(interview[i]),i) for _,i in selected];assert max(final)[-1]==0;out['38']=dict(selected=selected,final=final)
# Exhaust all nonnegative fish-count partitions for 3,4,5 fish.
def fish(n):return [(a,b,n-a-b) for a in range(n+1) for b in range(n-a+1)]
score=lambda v:sum(x*y for x,y in zip(v,[30,20,10]))
fishworlds=[v for v in it.product(fish(3),fish(4),fish(5)) if score(v[0])>score(v[1])>score(v[2])]
assert all(v[0][0]>0 and v[2][2]>0 for v in fishworlds) and any(score(v[1])==80 and v[1][1]==0 for v in fishworlds)
out['related11']=dict(worldCount=len(fishworlds),counterexample=[[3,0,0],[2,0,2],[0,0,5]])
pill={str(a):sorted({z for x,y,z in fish(8) if 2*x+z==a and 2*y+z==16-a}) for a in [8,9,6]}
assert pill=={'8':[0,2,4,6,8],'9':[1,3,5,7],'6':[0,2,4,6]};out['related31']=dict(ABDaysByATotal=pill)
r.write(b/'exact-model-checks.json',dict(status='PASS',models=out,phase='After frozen original-only solves; no answers changed.'))
print('PASS all10 exact models plus2 prior295 enumerations')
