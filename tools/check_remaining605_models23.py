from itertools import permutations,combinations
from fractions import Fraction as F
import review_remaining605 as r
b=r.folder(23)
# Enumerate all face-connected eight-cell shapes up to translation only.
# Every optimal arrangement can be connected; joining components removes faces.
dirs=[(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]
shapes={((0,0,0),)};counts=[1]
for n in range(2,9):
 nxt=set()
 for shape in shapes:
  occupied=set(shape)
  candidates={tuple(p[i]+d[i] for i in range(3)) for p in shape for d in dirs}-occupied
  for p in candidates:
   points=shape+(p,);mins=tuple(min(x[i] for x in points) for i in range(3))
   nxt.add(tuple(sorted(tuple(x[i]-mins[i] for i in range(3)) for x in points)))
 shapes=nxt;counts.append(len(shapes))
surfaces={}
for shape in shapes:
 occupied=set(shape);faces=sum(tuple(p[i]+d[i] for i in range(3)) not in occupied for p in shape for d in dirs)
 surfaces[faces]=surfaces.get(faces,0)+1
assert min(surfaces)==24 and surfaces[24]==1
game=[]
beats={('바위','가위'),('보','바위'),('엄지척','보'),('가위','엄지척')}
for p in permutations(['가위','바위','보','엄지척']):
 bb=list(p)+[p[0],p[1]];aa=['가위']+bb[:-1]
 if aa[2]!='엄지척' or aa[5]!='보' or bb[3]!='가위':continue
 winners=[]
 for a,e in zip(aa,bb):
  w='tie' if a==e else 'A' if (a,e) in beats else 'B' if (e,a) in beats else winners[-1] if winners else 'tie'
  winners.append(w)
 game.append(dict(A=aa,B=bb,winners=winners))
assert len(game)==1 and game[0]['winners']==['tie','B','B','A','A','B']
female=F(500)*F('.2')/2;experienced=female*4
assert female==50 and experienced==200 and experienced/F('.4')==500
paid=[]
for year in range(2022,2025):
 for month in range(1,13):
  t=year*12+month
  if 2022*12+2<=t<=2024*12+7 and not 2022*12+9<=t<2024*12+2:paid.append([year,month])
assert len(paid)==13 and len(paid)*50000==650000
ages=[v for v in combinations(range(23),4) if sum(v)==22]
assert max(v[1] for v in ages)==6 and (1,6,7,8) in ages
assert max(v[1] for v in ages if v[0]>=1)==6
fac={'A':(200,250,1800),'B':(250,300,2000),'C':(600,400,3600),'D':(450,350,2500),'E':(350,200,2000)}
fees=[]
for exhibit,seminar in permutations(fac,2):
 if fac[exhibit][0]<300 or fac[seminar][1]<200:continue
 names={exhibit,seminar};fee=F(sum(fac[x][2] for x in names))
 if names=={'D','A'}:fee-=F(2500)*F('.3')
 if names=={'E','B'}:fee-=F(2000)*F('.25')
 fees.append(dict(exhibition=exhibit,seminar=seminar,fee=int(fee)))
fees.append(dict(exhibition='C',seminar='C',fee=3600))
assert min(x['fee'] for x in fees)==3500
assert [(x['exhibition'],x['seminar']) for x in fees if x['fee']==3500]==[('E','B')]
make={'甲':10,'乙':8,'丙':8,'丁':7};size={'대형':7,'중형':8,'준중형':9,'소형':6};color={'흰색':10,'검은색':10,'회색':7,'파란색':9}
def price(p):return 9 if 1000<=p<2500 else 8 if 2500<=p<4000 else 7 if p>=4000 else None
assert [price(x) for x in [1000,2499,2500,3999,4000]]==[9,9,8,8,7]
cars=[('A','乙','중형','회색',2400),('B','丁','대형','검은색',3000),('C','甲','소형','회색',4500),('D','丙','대형','흰색',5000),('E','丁','준중형','파란색',4700)]
scores={a:(make[m]+size[s]+color[c]+price(p),make[m],price(p)) for a,m,s,c,p in cars}
assert [v[0] for v in scores.values()]==[32,32,30,32,32] and max(scores,key=scores.get)=='A'
new=[5,8]
for _ in range(4):new.append(sum(new[-2:]))
revoked=[0]+[2**n for n in range(1,6)];stock=[]
for i in range(6):stock.append(sum(new[:i+1])-sum(revoked[:i+1]))
assert new==[5,8,13,21,34,55] and stock==[5,11,20,33,51,74]
assert [n for n in range(11) if n>10/2]==[6,7,8,9,10]
r.write(b/'independent-calculation-paths.json',dict(status='PASS',method='Same-author computation from original conditions; independent calculation paths, not an independent reviewer.',polycubeTranslationCounts=counts,surfaceCounts=surfaces,minSurface=24,game=game,related10Female=str(female),related10Experienced=str(experienced),paidMonths=paid,totalAllowance=650000,ageCases=len(ages),maxFirstSonAge=6,ageWitness=[8,7,6,1],facilityAllFeasible=fees,carLexicographicScores=scores,newProducts=new,revokedProducts=revoked,stock=stock,quorumMinimum=6))
print('PASS: all eight-cell polycubes minimum24; game24 permutations; monthly payment13; age extrema; all facility pairs; car scores and stock74.')
