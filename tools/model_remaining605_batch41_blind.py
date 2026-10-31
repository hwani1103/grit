from itertools import permutations,combinations
from collections import defaultdict,Counter
from fractions import Fraction as F
import review_remaining605 as r
b=r.folder(41);assert not (b/'revealed-current.json').exists()
# Ranks B=0,A=1,S=2; each speaker knows only own two years plus prior public messages.
years=sorted(set(permutations([2,1,1,0,0,0])))
worlds=[tuple(zip(p,c)) for p in years for c in years if c[0]>p[0] and c[1]>p[1] and c[2]==p[2]]
byD=defaultdict(list)
for w in worlds:byD[w[3]].append(w)
dknows=[w for w in worlds if len({x[:3] for x in byD[w[3]]})==1]
byE=defaultdict(list)
for w in dknows:byE[w[4]].append(w)
eknows=[w for w in dknows if len(byE[w[4]])==1]
byF=defaultdict(list)
for w in eknows:byF[w[5]].append(w)
fknows=[w for w in eknows if len(byF[w[5]])==1]
assert fknows
print('s14counts',len(worlds),len(dknows),len(eknows),len(fknows));print('s14 worlds',fknows,'sixth',sorted({w[5] for w in fknows}))
codes=['AD10','BA13','BC03','BE02','CB11','CD08','DA14','DD12'];sets=[]
for cs in combinations(codes,6):
 if not {'BA13','CB11'}<=set(cs):continue
 freq=Counter(''.join(c[:2] for c in cs));sets.append(dict(codes=cs,letters=dict(freq),lastSum=sum(int(c[-1]) for c in cs)))
g=[x for x in sets if x['letters'].get('A',0)==1];assert all(x['letters']['D']==3 for x in g)
n=[x for x in sets if x['letters']['B']>max(v for k,v in x['letters'].items() if k!='B') and 'DD12' in x['codes']];assert n
d=[x for x in sets if x['lastSum']==21];assert all('CD08' in x['codes'] for x in d)
print('s12counter',n,'last21',d)
shuttle=[(a,bb,5*a,dd,e) for a in range(1,25) for bb in range(1,25,2) for dd in range(1,25) for e in range(bb+2,25,2) if a+bb+5*a+dd+e==24 and len({a,bb,5*a,dd,e})==5 and abs(15*a-2*dd)==3]
assert shuttle==[(1,3,5,6,9)]
assert 120000*F(4,5)==96000 and 96000<100000
assert F(1,2)*2*30==30 and 1000*4*30/250==480 and 500*1000/F(5,2)==200000
assert 3*100000000+12000000/12*100==400000000
assert (5*16-40)/8==5 and (128-5*16-128/4)/8*48/3==32
r.write(b/'blind-exact-models.json',dict(status='PASS',derivedBeforeReveal=True,shuttle=shuttle,codesAll15=sets,codeBMostCounterexample=n,gradeCounts=[len(worlds),len(dknows),len(eknows),len(fknows)],gradeFinalWorlds=fknows,gradeSixth=sorted({w[5] for w in fknows}),gradeRankMap=dict(B=0,A=1,S=2),physicalUnitsCaveat='Source uses power MW/kW as accumulated energy. Follow stated arithmetic for exam answer; physically accumulated output is MWh/kWh. Source text must remain unchanged; explanation should note distinction.'))
