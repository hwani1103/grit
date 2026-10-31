"""D21 mathematical/decision gates, alongside exact official source pixels and keys."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal,ROUND_HALF_UP
import json
from psat_batch_tools import validate
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/data21'
bank=json.loads((A/'authored-data21.json').read_text(encoding='utf-8'))
own=json.loads((A/'own-solve-before-key.json').read_text(encoding='utf-8'))
p={};answers=[]
def decision(n,truth,expected):
 q=next(q for q in bank if q['number']==n)
 actual={i+1:tuple(k in c for k in 'ㄱㄴㄷㄹ'[:len(truth)]) for i,c in enumerate(q['choices'])}
 winners=[i for i,t in actual.items() if tuple(truth)==t]
 assert winners==[expected],(n,actual,truth)
 assert own[str(n)]['truth']==truth
 answers.append(expected)
 return actual
def early(n,known,expected):
 q=next(q for q in bank if q['number']==n)
 remaining=[i+1 for i,c in enumerate(q['choices']) if all((k in c)==v for k,v in known.items())]
 assert remaining==[expected],(n,remaining)
 return remaining

# 11: exact aggregated denominator, rate ranking and a simultaneous numerator/denominator change.
reported=[176,76,204];times=[966,320,910]
assert sum(reported)==456 and sum(times)==2196
truth=[F(sum(times),sum(reported))>=5,F(560,855)<min(F(570,747),F(480,654)),F(300,409)>=F(3,4)]
decision(11,truth,2)
p['11']={'truth':truth,'early':early(11,{'ㄱ':False,'ㄷ':False},2),'weightedRate':str(F(2196,456)),'afterHIncrease':str(F(300,409))}

# 12: rounded per-centre averages are intervals, not exact fractional people.
rural=[4,9,8,7,8,9,11,20];urban=[99,28,17,9,9,6,2,10]
assert sum(rural)==76 and sum(urban)==180
eps=F('.005');cityNurseUpper=180*(F('9.06')+eps);ruralNurseLower=76*(F('6.28')-eps)
socialUpper=76*(F('2.17')+eps)
truth=[F(sum(rural[5:]),76)>F(99,180),F(76,256)>F(9,37),cityNurseUpper>=4*ruralNurseLower,socialUpper/90<=2]
decision(12,truth,4);assert socialUpper<F('2.2')*76<180
p['12']={'truth':truth,'early':early(12,{'ㄱ':False,'ㄷ':False},4),'urbanNursesUpper':str(cityNurseUpper),'fourRuralNursesLower':str(4*ruralNurseLower),'newSocialMeanUpper':str(socialUpper/90)}

# 13-14: four displayed types are not presumed exhaustive.
end=[1636,1624,1546,1364,1461];agree=[849,824,861,871,905];dec=[342,358,331,238,256];fail=[161,200,177,122,159];dismiss=[11,16,8,7,9];arb=[0,0,0,2,1]
success=[a+d-f+b for a,d,f,b in zip(agree,dec,fail,arb)]
counts=[[216,225,259,184],[210,235,254,164],[228,190,269,171],[175,154,277,217],[191,202,258,209]]
amounts=[[13699,11670,7876,5081],[17315,16136,9899,7263],[11578,18540,9827,6118],[14081,11593,8360,5802],[15708,11871,9784,10326]]
assert success==[1030,982,1015,989,1003]
other=[s-sum(c) for s,c in zip(success,counts)]
assert other==[146,119,157,166,143] and all(0<=o<c[2] and c[2]==max(c) for o,c in zip(other,counts))
rates=[F(s,e-d) for s,e,d in zip(success,end,dismiss)]
directions=[(b[0]>a[0])==(b[3]>a[3]) for a,b in zip(amounts,amounts[1:])]
truth=[max(success)==success[0],max(rates)==rates[1],all(c[2]>o and c[2]==max(c) for o,c in zip(other,counts)),all(directions)]
decision(13,truth,2);assert rates[1]<F('.62')<F('.63')<rates[0]
p['13']={'truth':truth,'early':early(13,{'ㄴ':False,'ㄹ':False},2),'success':success,'unlistedAllTypesUpper':other,'rates':list(map(str,rates)),'amountDirectionSame':directions}
def rounded(f,places=1):
 return str((Decimal(f.numerator)/Decimal(f.denominator)).quantize(Decimal(1).scaleb(-places),rounding=ROUND_HALF_UP))
denom=end[-1]-arb[-1];assert denom==1460
money=[rounded(F(c*a,1000),0) for c,a in zip(counts[-1],amounts[-1])]
agreementPercent=[rounded(F(a*100,e-b)) for a,e,b in zip(agree,end,arb)]
fourTotals=list(map(sum,counts));general=[row[1] for row in amounts]
growth=[rounded(F((b-a)*100,a)) for a,b in zip(general,general[1:])]
assert rounded(F(25600,denom))=='17.5' and rounded(F(12000,denom))=='8.2'
assert money==['3000','2398','2524','2158']
assert agreementPercent==['51.9','50.7','55.7','64.0','62.0']
assert fourTotals==[884,863,858,823,860] and growth==['38.3','14.9','-37.5','2.4']
assert 256>F(denom,10)
answers.append(1)
p['14']={'incorrectGraph':1,'sourceIncorrectValuesPreserved':['7.5','18.2'],'correctDecisionNoAdjustment':['17.5','8.2'],'moneyMillions':money,'agreementPercent':agreementPercent,'fourTypesTotals':fourTotals,'growthPercent':growth}

# 15: eliminate candidates, then check every boundary for the survivor.
groups=[[31,55,96,99,109,94],[13,40,69,119,100,11],[22,84,226,332,331,308],[32,99,234,262,282,26],[83,130,224,79,48,116]]
results=[]
for row in groups:
 total=sum(row);up=F(sum(row[:2]),total);middle=F(sum(row[2:4]),total);lower=F(sum(row[4:]),total)
 results.append(up>F('.102') and F('.4')<=middle<F('.477') and abs(lower-F('.116'))>=F('.3'))
assert results==[True,False,False,False,False]
assert F('.116')-F('.3')<0 and F(106,1303)<F('.1') and F(188,352)>F('.5') and F(496,935)>F('.5') and F(164,680)<F('.25')
answers.append(1);p['15']={'candidates':results,'Aparts':[86,195,203],'Atotal':484}

# 16: a multiplicative dominance comparison and interval difference bound.
men=[3839,2766,1082,1707,4445];women=[3503,2820,1111,1605,4138]
pop=[a+b for a,b in zip(men,women)];ratios=[F(a,b) for a,b in zip(men,women)]
wf=F(sum(women[:2]),sum(women));mf=F(sum(men[2:]),sum(men))
truth=[sum(b>a for a,b in zip(men,women))==3,all(pop[i]<pop[i+1] and ratios[i]<ratios[i+1] for i in [2,3]),abs(wf-mf)<=F('.1')]
decision(16,truth,4)
assert 307>3*102 and 4138<3*1605 and ratios[2]<1<ratios[3]<ratios[4]
assert F('.45')<wf<F('.5')<mf<F('.55')
p['16']={'truth':truth,'regionTotals':pop,'femaleEupShare':str(wf),'maleMyeonShare':str(mf),'shareDifference':str(mf-wf)}

# 17: enumerate every feasible intersection consistent with both marginals.
public=[3193,3515,3721,3401,3655,3972,4308,4653,4572];univ=[2788,3784,4316,4076,4450,4486,4747,5610,4815];total=[a+b for a,b in zip(public,univ)]
paid=[718,1107,1587,1466,1796,2214,2485,2957,3002];free=[419,550,511,282,159,208,141,262,224]
licensePaid=[4098,5113,5385,4905,5158,4958,5465,6155,5441];licenseFree=[639,322,327,278,340,452,389,453,209];option=[0,0,1,0,0,0,0,1,0];other=[107,207,226,546,652,626,575,435,511]
assert [sum(col) for col in zip(paid,free,licensePaid,licenseFree,option,other)]==total
transfer=[a+b for a,b in zip(paid,free)];years=[2014+i for i,(x,t) in enumerate(zip(transfer,total)) if 4*x>=t]
N=9387;SME=8775;L=5441
feasible=[]
for both in range(min(SME,L)+1):
 cells=[both,SME-both,L-both,N-SME-L+both]
 if min(cells)>=0:feasible.append(both)
assert min(feasible)==4829 and max(feasible)==5441 and all(2*x>=SME for x in feasible)
assert years==[2016,2019,2020,2021,2022]
truth=[all(a>b for a,b in zip(univ,public)),all(2*x>=SME for x in feasible),len(years)==5]
decision(17,truth,4);p['17']={'truth':truth,'intersectionRange':[min(feasible),max(feasible)],'transfer':transfer,'qualifyingYears':years}

# 18: unknown equipment coordinates are never filled from guesses.
names=['Poland','Latvia','Lithuania','Estonia','USA','Finland','UK','Greece','Denmark','Romania']
old=list(map(F,['1.88','.94','.88','1.93','3.71','1.45','2.14','2.22','1.15','1.35']))
new=list(map(F,['4.12','3.15','2.85','3.43','3.38','2.41','2.33','3.08','2.37','2.25']))
growth=[b-a for a,b in zip(old,new)];equipment2024=[F(x) if x is not None else None for x in ['51.1','36.9','21.2','33.7','29.9',None,'36.1','36.1','29.8','30.8']]
# Finland is not exactly labelled; only its visually evident >21.2 relationship is used.
assert all(v is None or v>=F('21.2') for v in equipment2024)
assert new.index(max(new))==growth.index(max(growth))==0
assert growth[0]-growth[1]==F('.03') and growth[0]-F('.01')>max(growth[1:])+F('.01')
usOld=old[4]*26/100;usNew=new[4]*F('29.9')/100
assert usOld==F('.9646') and usNew==F('1.01062')
assert (F('3.38')-F('.005'))*(F('29.9')-F('.05'))>(F('3.71')+F('.005'))*(F(26)+F('.05'))
truth=[True,F('21.2')-F('14.1')<=F('29.9')-26,usNew<usOld]
decision(18,truth,1);p['18']={'truth':truth,'early':early(18,{'ㄴ':False,'ㄷ':False},1),'defenseGrowth':dict(zip(names,map(str,growth))),'USGDPbasedEquipmentPercent':[str(usOld),str(usNew)],'unlabelledEquipmentCoordinates':'not estimated; Finland minimum excluded visually from chart'}

# 19: all nine sectors, global extrema, and one counterexample to monotonicity.
old=[49087,4090,3838,8307,40731,11471,9680,24820,4186];new=[53814,4514,3911,8980,45114,14156,10648,29499,4580];employees=[201043,13666,9390,37142,143233,55279,29637,116557,21318]
assert [sum(old),sum(new),sum(employees)]==[156210,175216,627265]
rates=[F(b-a,a) for a,b in zip(old,new)];perStore=[F(e,n) for e,n in zip(employees,new)]
assert rates.index(max(rates))==5 and perStore[5]<4<perStore[8]
assert all(v<F('.2') for i,v in enumerate(rates) if i!=5) and rates[5]>F('.2')
truth=[rates.index(max(rates))==perStore.index(max(perStore)),sum(sorted(new)[-3:])>=F(3,4)*sum(new),all(F(c,t)>=F('.15') for c,t in [(old[7],sum(old)),(new[7],sum(new))]),all(employees[i]>=employees[j] for i in range(9) for j in range(9) if new[i]>new[j]),F(sum(employees),sum(new))>=4]
assert truth==[False,False,True,False,False]
answers.append(3);p['19']={'truth':truth,'top3Stores':sum(sorted(new)[-3:]),'employeesTotal':sum(employees),'coffeeShares':[str(F(old[7],sum(old))),str(F(new[7],sum(new)))]}

# 20: integer solutions under displayed one-decimal rounding, including a consistent whole table.
quit=[35,120,33,60,36,37];quitRate=list(map(F,['70','80','66','75','30','74']));circ=list(map(F,['15','25','8.5','8','30','12.5']))
def matches(actual,display):return display-F('.05')<=actual<display+F('.05')
hires=[];heads=[]
for q,qr,c in zip(quit,quitRate,circ):
 candidates=[h for h in range(1,1001) if matches(F(q*100,h),qr)]
 assert len(candidates)==1
 h=candidates[0];hires.append(h);heads.append([n for n in range(1,2001) if matches(F((h-q)*100,n),c)])
assert hires==[50,150,50,80,120,50] and heads[0]==[100] and heads[4]==[280]
oneWorld=[100,120,200,250,280,104]
assert all(n in options for n,options in zip(oneWorld,heads))
assert matches(F((sum(hires)-sum(quit))*100,sum(oneWorld)),F(17))
assert F(sum(quit)*100,sum(hires))==F('64.2')
truth=[not(heads[4][0]>heads[0][0] and quitRate[4]<quitRate[0]),hires[4]>=2*hires[0],F(quit[2],sum(quit))>=F('.1')]
decision(20,truth,4)
assert [i+1 for i,c in enumerate(bank[-1]['choices']) if 'ㄴ' in c and 'ㄷ' in c]==[4,5]
p['20']={'truth':truth,'hires':hires,'AandEHeadcounts':[heads[0],heads[4]],'consistentRoundedWorld':oneWorld,'totalCirculation':str(F(17900,1054)),'needsNegativeAForUniqueChoice':True}
assert answers==[2,4,2,1,1,4,4,1,3,4]
assert answers==[q['answer'] for q in bank]==[own[str(n)]['answer'] for n in range(11,21)]
validate('data21',p,[('2025-03-08',i) for i in range(11,21)],figure_count=29)
