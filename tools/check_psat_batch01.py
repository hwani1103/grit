from pathlib import Path
import itertools as it,json,re
R=Path(__file__).resolve().parents[1]/'artifacts/psat_batch01_20261028'
bank=json.loads((R.parents[1]/'assets/psat/batch01.json').read_text(encoding='utf-8'))
base=json.loads((R/'sources/bank_base.json').read_text(encoding='utf-8'))
report={}
clean=lambda x:re.sub(r'\s+','',x)
for a,b in zip(bank,base):
 assert clean(a['prompt'])==clean(b['prompt'])
 if not a['tables'] and not a['id'].endswith('l-10'):assert clean(a['body'])==clean(b['body']),a['id']
 if not a['id'].endswith('l-10'):assert [clean(x) for x in a['choices']]==[clean(x) for x in b['choices']],a['id']
report['transcription']='20 prompts and original choices checked; 16 unchanged passages; 3 table remaps and l10 column labels visually checked'
models=[]
for P,L,G,J,E in it.product([False,True],repeat=5):
 if (not P or L) and (not G or (J and E)) and (not L or not E):models.append((P,L,G,J,E))
truth=[all((not p or not g) for p,l,g,j,e in models),all((j or not g) for p,l,g,j,e in models),all(not p for p,l,g,j,e in models)]
assert truth==[True,True,False];report['l14']={'models':len(models),'mandatory':truth,'counterexample':[1,1,0,0,0]}
# Enumerate all possible occupied attendance types, not just a small fixed number of people.
types=[x for x in it.product([False,True],repeat=4) if (not x[0] or x[2]) and (not x[1] or not x[2])]
valid=[]
for mask in range(1,1<<len(types)):
 people=[t for i,t in enumerate(types) if mask>>i&1]
 if not any(w and th for m,t,w,th in people):continue
 conclusion=any(not m and th for m,t,w,th in people)
 opts=[any(not m for m,t,w,th in people),any(not t for m,t,w,th in people),any(w and not th for m,t,w,th in people),any(m and not th for m,t,w,th in people),all(not(m and th) for m,t,w,th in people)]
 valid.append((conclusion,opts))
answers=[all(c for c,opts in valid if opts[i]) and any(opts[i] for c,opts in valid) for i in range(5)]
assert answers==[False,False,False,False,True];report['l15']={'occupied_type_models':len(valid),'sufficient_options':answers}
# Five labelled representatives, each with at least one yes and one no.
types=[x for x in it.product([0,1],repeat=4) if 0<sum(x)<4 and (not x[0] or x[1]) and not(x[1] and x[3]) and(not x[3] or x[2])]
valid=[]
for group in it.product(types,repeat=5):
 sums=[sum(x[i] for x in group) for i in range(4)]
 if sums[0]!=2 or sums[3]!=2:continue
 by=[x for x in group if x[1]]
 if sum(x[2] for x in by)*2!=len(by):continue
 valid.append((sums,[any(sum(x)==1 for x in group),sums[1]==2,sums[2]>max(sums[0],sums[1],sums[3])]))
assert valid and all(all(t) for s,t in valid)
assert set(tuple(s) for s,t in valid)=={(2,2,4,2)};report['l16']={'valid_assignments':len(valid),'counts':[2,2,4,2]}
# Target-component accounting, exact rational arithmetic.
from fractions import Fraction as F
assert F(4)*F(3,4)*F(1,2)==F(3,2);report['s06']='remaining component = 3/2 mL'
qualified=[]
for name,age,work,business,tax,service in [('甲',20,0,0,None,0),('乙',36,0,5000,None,0),('丙',29,3500,1000,2022,2),('丁',35,4500,0,2020,2),('戊',27,4000,1500,2021,0)]:
 if 19<=age-service<=34 and 0<work+business<=5000 and tax not in [2021,2022]:qualified.append(name)
assert qualified==['丁'];report['s08']=qualified
out=[]
for x in range(1,101):
 scores=[15-3*x,15-2*x,10-3*x,5,5-3*x]
 if [sum(s>=10 for s in scores),sum(0<=s<10 for s in scores),sum(s<0 for s in scores)]==[1,3,1]:out.append(x)
assert out==[2];report['s13']={'valid_x_1_to_100':out,'upper_bound_reason':'x>=6 gives no score >=10'}
sol=[(p,d,e) for p in range(1,1001) for d in range(21,32) for e in range(2,48) if p*d*e==1000]
assert max(p for p,d,e in sol)==20;report['s14']={'max':20,'witness':[20,25,2]}
# All integer-minute placements; analytic E overlap argument covers continuous positions as well.
counts={t:False for t in [4,10,15,21,24]};witness=None
for sa in range(18):
 for sc in range(14):
  if not(sa+13<=sc or sc+17<=sa):continue
  for sb,sd,se in it.product(range(16),range(10),range(6)):
   intervals=[(sa,sa+13),(sb,sb+15),(sc,sc+17),(sd,sd+21),(se,se+25)]
   for t in counts:
    if sum(a<=t<b for a,b in intervals)==1:
     counts[t]=True
     if t==4:witness=intervals
assert counts=={4:True,10:False,15:False,21:False,24:False};report['s15']={'possible_by_minute':counts,'witness':witness,'continuous_proof':'E necessarily covers (5,25); A+C cover all 30 minutes'}
sol=[x for x in it.product(range(1,5),repeat=4) if sum(x)==__import__('math').prod(x)]
assert set(tuple(sorted(x)) for x in sol)=={(1,1,2,4)};report['s16']={'ordered_solutions':len(sol),'unique_multiset':[1,1,2,4],'sum_product':8}
(R/'content_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=True,indent=2))
