from fractions import Fraction as F
from itertools import combinations
import review_remaining605 as r
b=r.folder(42);checks=[]
def check(n,**details):checks.append(dict(number=n,**details))
assert 40*180<99*76 and 76*37>9*256
assert F('9.065')*180<4*F('6.275')*76 and F('2.175')*76/90<2
check(12,truth=[False,True,False,True],roundingEndpointsSafe=True)
ends=[1636,1624,1546,1364,1461];agree=[849,824,861,871,905];arb=[0,0,0,2,1];success=[181,158,154,116,97];dismiss=[11,16,8,7,9]
counts=[[216,225,259,184],[210,235,254,164],[228,190,269,171],[175,154,277,217],[191,202,258,209]]
units=[[13699,11670,7876,5081],[17315,16136,9899,7263],[11578,18540,9827,6118],[14081,11593,8360,5802],[15708,11871,9784,10326]]
est=[a+s+t for a,s,t in zip(agree,success,arb)];omitted=[e-sum(row) for e,row in zip(est,counts)]
assert est==[1030,982,1015,989,1003] and sum(est)==5019 and omitted==[146,119,157,166,143]
assert all(max(row)==row[2]>missing for row,missing in zip(counts,omitted))
rates=[F(e,n-d)*100 for e,n,d in zip(est,ends,dismiss)];assert rates.index(max(rates))==3 and rates[1]<rates[0]
assert units[3][0]>units[2][0] and units[3][3]<units[2][3]
check(13,established=est,rates=list(map(float,rates)),omittedInstitutionUpperBounds=omitted,truth=[True,False,True,False],ownReasoningSupplement='Original own solve omitted non-displayed institutions; app already contains correct bound. Immutable solve retained.')
amounts=[F(c*u,1000) for c,u in zip(counts[-1],units[-1])];percent=[F(a,n-t)*100 for a,n,t in zip(agree,ends,arb)];growth=[F(units[i][1]-units[i-1][1],units[i-1][1])*100 for i in range(1,5)]
assert [round(x) for x in amounts]==[3000,2398,2524,2158] and [round(float(x),1) for x in percent]==[51.9,50.7,55.7,64,62]
assert [sum(row) for row in counts]==[884,863,858,823,860] and [round(float(x),1) for x in growth]==[38.3,14.9,-37.5,2.4]
assert round(256/1460*100,1)==17.5 and round(120/1460*100,1)==8.2
check(14,optionTruth=[False,True,True,True,True],amounts=list(map(float,amounts)),agreementPercents=list(map(float,percent)),growth=list(map(float,growth)))
grades=[[31,55,96,99,109,94],[13,40,69,119,100,11],[22,84,226,332,331,308],[32,99,234,262,282,26],[83,130,224,79,48,116]]
valid=[]
for i,row in enumerate(grades):
 upper,middle,lower=[F(sum(row[j:j+2]),sum(row))*100 for j in [0,2,4]]
 if upper>F('10.2') and 40<=middle<F('47.7') and abs(lower-F('11.6'))>=30:valid.append(i+1)
assert valid==[1];check(15,allThreeConditionsSatisfied=valid)
men=[3839,2766,1082,1707,4445];women=[3503,2820,1111,1605,4138]
assert sum(men)==13839 and sum(women)==13177 and sum(w>m for w,m in zip(women,men))==2
assert F(men[2],women[2])<F(men[3],women[3])<F(men[4],women[4])
assert abs(F(sum(women[:2]),sum(women))-F(sum(men[2:]),sum(men)))*100<10
check(16,truth=[False,True,True])
tot=[5981,7299,8037,7477,8105,8458,9055,10263,9387];paid=[718,1107,1587,1466,1796,2214,2485,2957,3002];free=[419,550,511,282,159,208,141,262,224]
years=[2014+i for i,(n,a,c) in enumerate(zip(tot,paid,free)) if 4*(a+c)>=n];assert years==[2016,2019,2020,2021,2022] and 2*(5441-(9387-8775))>8775
check(17,truth=[False,True,True],years=years,intersectionBounds=[4829,5441])
def14=list(map(F,['1.88','.94','.88','1.93','1.15','1.45','1.35','2.22','2.14','3.71']));def24=list(map(F,['4.12','3.15','2.85','3.43','2.37','2.41','2.25','3.08','2.33','3.38']))
deltas=[v-u for u,v in zip(def14,def24)];assert deltas.index(max(deltas))==def24.index(max(def24))==0
assert min(deltas[0]-F('.01')-(d+F('.01')) for d in deltas[1:])==F('.01')
assert F('21.2')-F('14.1')>F('29.9')-26 and F('3.38')*F('29.9')>F('3.71')*26
check(18,truth=[True,False,False],defenseRatioDeltas=list(map(float,deltas)),nearestRoundingMargin=float(F('.01')))
shops23=[49087,4090,3838,8307,40731,11471,9680,24820,4186];shops24=[53814,4514,3911,8980,45114,14156,10648,29499,4580];staff=[201043,13666,9390,37142,143233,55279,29637,116557,21318]
assert sum(shops23)==156210 and sum(shops24)==175216 and sum(staff)==627265
growth=[F(b-a,a) for a,b in zip(shops23,shops24)];average=[F(s,n) for s,n in zip(staff,shops24)]
assert growth.index(max(growth))==5 and average.index(max(average))==8
assert 4*sum(sorted(shops24)[-3:])<3*sum(shops24) and all(F(s[7],sum(s))>=F('.15') for s in [shops23,shops24])
assert shops24[6]>shops24[3] and staff[6]<staff[3] and sum(staff)<4*sum(shops24)
check(19,optionTruth=[False,False,True,False,False],staffTotal=sum(staff))
resign=[35,120,33,60,36,37];quit=list(map(F,['.7','.8','.66','.75','.3','.74']));circulate=list(map(F,['.15','.25','.085','.08','.3','.125']))
recruit=[F(q)/p for q,p in zip(resign,quit)];population=[(i-o)/c for i,o,c in zip(recruit,resign,circulate)];assert recruit==[50,150,50,80,120,50] and population==[100,120,200,250,280,104]
assert recruit[4]>=2*recruit[0] and 10*resign[2]>=sum(resign)
for idx in [0,4]:
 possible=[(inc,n) for inc in range(1,500) if abs(F(resign[idx],inc)-quit[idx])<=F('.0005') for n in range(1,1000) if abs(F(inc-resign[idx],n)-circulate[idx])<=F('.0005')]
 assert possible==[(int(recruit[idx]),int(population[idx]))]
check(20,truth=[False,True,True],recruit=list(map(int,recruit)),population=list(map(int,population)),AandEUniqueUnderRounding=True)
a=[99,732,333,255,1184,768,823];c=[113,704,392,281,1205,620,727];diff=[v-u for u,v in zip(a,c)]
assert sum(a)==4194 and sum(c)==4042 and sum(x>0 for x in diff)==4 and diff[5]==-148 and diff.index(max(diff))==2 and F(a[4],sum(a))<F('.3') and sum(x*7>sum(c) for x in c)==4
check(22,optionTruth=[True,True,False,True,True],differences=diff)
r.write(b/'exact-model-checks.json',dict(status='PASS',checks=checks))
receipt=b/'post-reveal-reasoning-correction.json'
if not receipt.exists():
 r.write(receipt,dict(id='kr-mpm-2025-03-08-psat-d-13',answerBefore=2,answerAfter=2,issue='Own original-only reasoning checked four displayed institutions but omitted remaining institution types; existing app correctly uses an upper bound.',source='blind-source.json and original13 image; table1 total minus table2 four institutions',correctedReasoning='For each year omitted institutions together total146,119,157,166,143, less than hospitals259,254,269,277,258. Each omitted type is bounded by that residual. Thus ㄷ holds for all types.',ownSolveSha256=r.sha(b/'own-solves.json'),originalSolvePreserved=True,appAlreadyCorrect=True))
 p=r.read(r.OUT/'progress.json');p.setdefault('postRevealReasoningCorrections',{})['kr-mpm-2025-03-08-psat-d-13']='batch42/post-reveal-reasoning-correction.json';r.write(r.OUT/'progress.json',p)
print('PASS10 models; own d13 missing-population bound supplemented without changing frozen solve')
