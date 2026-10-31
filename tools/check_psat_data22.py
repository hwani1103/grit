"""D22: exact arithmetic, decision uniqueness, rounding intervals, and source gates."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal,ROUND_HALF_UP
import json
from psat_batch_tools import validate
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/data22'
bank=json.loads((A/'authored-data22.json').read_text(encoding='utf-8'))
own=json.loads((A/'own-solve-before-key.json').read_text(encoding='utf-8'));p={};answers=[]
def decision(n,truth,expected):
 q=next(q for q in bank if q['number']==n)
 actual={i+1:tuple(k in c for k in 'ㄱㄴㄷㄹ'[:len(truth)]) for i,c in enumerate(q['choices'])}
 assert [i for i,t in actual.items() if tuple(truth)==t]==[expected]
 assert own[str(n)]['truth']==truth
 answers.append(expected)
def single(n,truth,expected,wrong=False):
 assert [i+1 for i,t in enumerate(truth) if t!=wrong]==[expected],(n,truth)
 assert own[str(n)]['truth']==truth
 answers.append(expected)
def early(n,known,expected):
 q=next(q for q in bank if q['number']==n)
 remaining=[i+1 for i,c in enumerate(q['choices']) if all((k in c)==v for k,v in known.items())]
 assert remaining==[expected],(n,remaining)
 return remaining
def rd(f,d=1):
 return str((Decimal(f.numerator)/Decimal(f.denominator)).quantize(Decimal(1).scaleb(-d),rounding=ROUND_HALF_UP))
def fs(xs):return list(map(F,map(str,xs)))

# 21: compare the original subgroups, not the overall columns; rates are rounded.
male=fs([24.2,22,21.9,20.6]);female=fs([23.8,21.1,20.3,19.2]);diff=[abs(a-b) for a,b in zip(male,female)]
eps=F('.0005');girl=4610*F('.194');boy=4160*F('.141')
girlLow=4610*(F('.194')-eps);boyHigh=4160*(F('.141')+eps)
count2024Low=13827*(F('.192')-eps);count2020AtMost=10000*(F('.25')+eps)
assert girlLow>F('1.5')*boyHigh and count2024Low>count2020AtMost
truth=[all(b>a for a,b in zip(diff,diff[1:])),all(b<a for a,b in zip(fs([21.9,14.8,20.3,14.9]),fs([20.6,14.2,19.2,14.6]))),13827*F('.192')/F('.25')<=10000,girl>=F('1.5')*boy]
decision(21,truth,4)
p['21']={'truth':truth,'early':early(21,{'ㄱ':False,'ㄷ':False},4),'differences':list(map(str,diff)),'girlLow':str(girlLow),'1.5boyHigh':str(F('1.5')*boyHigh),'count2024Low':str(count2024Low),'count2020AtMost':str(count2020AtMost)}

# 22: independent reading of both bar series and the unit.
old=[99,732,333,255,1184,768,823];new=[113,704,392,281,1205,620,727]
change=[b-a for a,b in zip(old,new)];avg=F(sum(new),7)
truth=[sum(d>0 for d in change)>sum(d<0 for d in change),old[5]-new[5]>=100,F(old[4],sum(old))>=F('.3'),change.index(max(change))==2,sum(v>avg for v in new)==4]
single(22,truth,3,wrong=True);assert sum(old)==4194 and sum(new)==4042
p['22']={'truth':truth,'changes':change,'totals':[sum(old),sum(new)],'mean2024':str(avg),'Eshare':str(F(old[4],sum(old)))}

# 23: unknown != numerically false. Construct legal alternate values for the gap.
part2020=35354*F('.723');part2020Low=35354*F('.7225');rate2021=F(26120,35183)
alternatives=[F('.7'),F('.8')]
assert all(0<x<1 and 0<F('.382')<1 for x in alternatives)
assert [x-rate2021>=F('.03') for x in alternatives]==[False,True]
truth=[part2020Low>25413,F(9000,26120)>F('.365'),False,27350*F('.415')>27020*F('.4')]
decision(23,truth,2);assert F(9000,26120)<F('.35')
p['23']={'supportedTruth':truth,'unknown':['ㄷ'],'early':early(23,{'ㄴ':False,'ㄷ':False},2),'participation2020Lower':str(part2020Low),'participation2022PossibleAlternatives':list(map(str,alternatives)),'graduation2022InAlternatives':[str(34915*x*F('.382')) for x in alternatives]}

# 24: ratio cancellation and a weighted midpoint; no age-complement assumption.
depend=fs([56,48,34,27,20]);elder=fs([16,21,19,12,9]);pop=[8705,3400,2450,1619,6514]
work=[e/d for e,d in zip(elder,depend)]
merged=(pop[1]*elder[1]+pop[4]*elder[4])/(pop[1]+pop[4])
truth=[all(not elder[i]>elder[j] or depend[i]>depend[j] for i in range(5) for j in range(5)),work.index(min(work))==0,merged<=15]
decision(24,truth,5)
assert work[0]<F('.3') and all(v>F('.4') for v in work[1:]) and pop[4]>pop[1] and 21-15==15-9
p['24']={'truth':truth,'early':early(24,{'ㄴ':True,'ㄷ':True},5),'workingRatios':list(map(str,work)),'mergedElderPercent':str(merged)}

# 25: preserve the two different classification axes, and prove a sharp lower bound.
under=[1040,4050+4640,5020,5950,4430,1350];grad=[0,19+102,224,340,280,64]
adultGrad=sum(grad)-19;nonworkers=F(adultGrad,10);low=grad[3]-nonworkers
assert sum(grad)==1029 and adultGrad==1010 and nonworkers==101 and low==239
# Both lower and upper bounds are feasible (other-age graduates can hold all remaining workers).
assert 0<=F(adultGrad*9,10)-low<=adultGrad-grad[3]
assert 0<=F(adultGrad*9,10)-grad[3]<=adultGrad-grad[3]
school=1040+4050;adult=sum(under)-school;total=[a+b for a,b in zip(under,grad)]
truth=[under.index(max(under))==3,grad.index(max(grad))==max(range(6),key=lambda i:F(grad[i],under[i])),low>=200,adult>=5*school,max(total)>=9*min(total)]
single(25,truth,3)
assert F(340,5950)<F('.06')<F(280,4430)
p['25']={'truth':truth,'ageTotals':total,'adultAndSchoolUndergrad':[adult,school],'workers40Range':[int(low),340],'nonworkers':int(nonworkers)}

# 26: every adjacent interval for both sexes, not only the endpoints.
data=[[[4.7,5.5,6.8,9.7],[3.2,3.9,4.5,6.9]],[[3.6,3.9,4.6,5.2],[3.3,4.7,6.3,8.3]],[[5.3,6.8,7.7,8.3],[3.8,5.8,5.3,6.7]],[[4.9,5.7,7.1,8.5],[2.1,2.7,3.1,3.4]],[[3.3,4.1,6.4,7.2],[4.6,5.5,8.4,9.7]]]
conditions=[]
for m0,f0 in data:
 m,f=fs(m0),fs(f0);dm=[b-a for a,b in zip(m,m[1:])];df=[b-a for a,b in zip(f,f[1:])]
 gap1=abs(m[0]-f[0]);gap3=abs(m[2]-f[2])
 conditions.append([all(v>0 for v in dm+df),F('1.5')*gap1<=gap3<2*gap1,all(abs(y)>abs(x) for x,y in zip(dm,df)),m[3]>=F('1.3')*m[1] and f[3]>=F('1.3')*f[1]])
single(26,[all(c) for c in conditions],5)
p['26']={'fourConditionsByCity':conditions,'EchangesMale':['0.8','2.3','0.8'],'EchangesFemale':['0.9','2.9','1.3']}

# 27: graphs deliberately contain false numbers; verify but retain their original pixels.
debt=fs([1828.8,1998.3,2192.4,2260.1,2241.4]);gdpRatio=fs([89.6,97.1,98.7,97.3,93.6])
gdp=[rd(d*100/r) for d,r in zip(debt,gdpRatio)]
loan=fs([1504.9,1633.6,1757.1,1749.8,1767.3]);mortgage=fs([534,583.9,629.6,644.1,672.1]);bankamt=fs([767.7,849.9,910.1,902.6,916]);other=fs([737.2,783.7,847,847.2,851.3])
increase=[rd(b-a) for a,b in zip(mortgage,mortgage[1:])];ratios=[rd(a*100/b) for a,b in zip(bankamt,other)]
truth=[gdp==['2041.1','2058.0','2221.3','2322.8','2394.7'],F('1757.1')/F('2192.4')<F('.8'),increase==['49.9','45.7','14.5','28.0'],ratios==['96.7','95.9','105.8','117.7','118.1']]
decision(27,truth,2);assert bankamt[0]>other[0] and loan[2]>F('.8')*debt[2]
p['27']={'truth':truth,'early':early(27,{'ㄴ':False,'ㄷ':True},2),'GDP':gdp,'mortgageIncreases':increase,'bankOtherPercent':ratios,'loan2022Percent':rd(loan[2]*100/debt[2])}

# 28: rounded patient-days do not imply exact counts. Unknown clinic cost has free allocations.
cost=[488100,537857,539790,588111,680711];growth=[rd(F((b-a)*100,a)) for a,b in zip(cost,cost[1:])]
inpatientLow=7564*(F('19.52')-F('.005'));inpatientHigh=7564*(F('19.52')+F('.005'));total2020=1567411
assert rd(inpatientLow*100/total2020)==rd(inpatientHigh*100/total2020)=='9.4'
instit2022=[54634,90052,82324,67288,484185,4435,71882,6822,90374,7633,439435]
assert sum(instit2022)==1399064
top5=sorted(instit2022,reverse=True)[:5];top5Percent=[rd(F(v*100,1399064)) for v in top5]
truth=[growth==['10.2','0.4','9.0','15.7'],True,top5Percent==['34.6','31.4','6.5','6.4','3.9'],False]
decision(28,truth,1)
assert top5==[484185,439435,90374,90052,82324] and 82324>F('.05')*1399064
# Changing the clinic share of costs changes its per-day cost while all supplied aggregates/days remain fixed.
clinicCosts=[F(cost[0],10),F(cost[0],5)]
assert len({v/F(547466) for v in clinicCosts})==2 and all(0<v<cost[0] for v in clinicCosts)
p['28']={'supportedTruth':truth,'unknown':['ㄹ'],'early':early(28,{'ㄷ':False,'ㄹ':False},1),'growth':growth,'inpatientDayInterval':list(map(str,[inpatientLow,inpatientHigh])),'top5Percent':top5Percent,'clinicCostPossibleAllocations':list(map(str,clinicCosts))}

# 29-30: cross-check composition-based and vaccine/rate-based counts; allow displayed rounding.
vacc=[5615,10610,12491,6698];infect=[3047,2415,5554,3621];male=fs([.32,.25,.55,.43]);female=[1-v for v in male]
age=[[4.7,15.7,27.9,1.6,50.1],[10.4,9.9,32.7,30,17],[17.8,28.4,15.3,21.5,17],[37.8,4,30.9,22.5,4.8]]
age=[fs(a) for a in age]
counts=[[infect[i]*a/100 for a in age[i]] for i in range(4)]
diff=[infect[i]*abs(male[i]-female[i]) for i in range(4)]
diffLow=[infect[i]*(abs(male[i]-female[i])-F('.001')) for i in range(4)]
diffHigh=[infect[i]*(abs(male[i]-female[i])+F('.001')) for i in range(4)]
assert diffHigh[3]<min(diffLow[:3])
truth=[counts[0][2]<counts[3][3],F('44.4')>F('49.3'),diff.index(min(diff))==3,max(range(4),key=lambda i:counts[i][3])==1,counts[3].index(min(counts[3]))==4]
single(29,truth,3)
assert F(1465)*F('.58')>F(1092)*F('.747')
assert infect[0]*(age[0][2]-F('.05'))>infect[3]*(age[3][3]+F('.05'))
p['29']={'truth':truth,'sexCountDifferences':list(map(str,diff)),'Dupper':str(diffHigh[3]),'Clower':str(diffLow[2]),'ageCountApproximations':[[rd(c) for c in a] for a in counts]}

overall=[rd(F(i*100,v)) for i,v in zip(infect,vacc)]
age24=[a[2] for a in counts];composition=[rd(a*100/sum(age24)) for a in age24]
sourceComp=['26.1','30.6','14.3','28.9']
truth=[False,composition==sourceComp,overall==['54.3','22.8','44.5','54.1'],age[2]==fs([17.8,28.4,15.3,21.5,17])]
decision(30,truth,5)
# Even broad, independent rounding intervals keep A/C counts close; the graph would require A/C > 1.8.
aHigh=infect[0]*(age[0][2]+F('.05'));cLow=infect[2]*(age[2][2]-F('.05'))
assert aHigh/cLow<F('1.01') and (F('26.1')-F('.05'))/(F('14.3')+F('.05'))>F('1.8')
# Male vaccine denominators can vary without changing the supplied infected-sex composition.
infectMale=infect[0]*male[0];infectFemale=infect[0]*female[0]
maleVacc=[F(1500),F(2000)]
assert all(v>infectMale and vacc[0]-v>infectFemale for v in maleVacc)
p['30']={'supportedTruth':truth,'unknown':['ㄱ'],'early':early(30,{'ㄱ':False,'ㄴ':False},5),'overallPercent':overall,'age24CorrectApproxComposition':composition,'ACratioMax':str(aHigh/cLow),'maleVaccinePossibleValues':list(map(str,maleVacc))}

assert answers==[own[str(n)]['answer'] for n in range(21,31)]==[q['answer'] for q in bank]
validate('data22',{'mathAndDecisionProof':p,'ownSolveBeforeKey':'own-solve-before-key.json','manualSourceReview':'All10 originals viewed; graph titles/legends, table units/notes and cross-column/common data reviewed.'},[('2025-03-08',n) for n in range(21,31)],32)
