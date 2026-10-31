from fractions import Fraction as F
from datetime import date,timedelta
import itertools as it,math
import review_remaining605 as r
b=r.folder(45);out={}
Q=lambda x:F(str(x))
def tenths(v):return (v*10+F(1,2)).numerator//(v*10+F(1,2)).denominator/10
dep=[56,48,34,27,20];elder=[16,21,19,12,9];pop=[8705,3400,2450,1619,6514];work=[F(x,y)*100 for x,y in zip(elder,dep)];merged=F(21*3400+9*6514,3400+6514)
assert work.index(min(work))==0 and merged<15 and elder[2]>elder[0] and dep[2]<dep[0];out['24']=dict(workShares=list(map(str,work)),merged=str(merged))
under=[1040,4050+4640,5020,5950,4430,1350];grad=[0,19+102,224,340,280,64];total=[a+g for a,g in zip(under,grad)]
assert sum(under)==26480 and sum(grad)==1029 and under.index(max(under))==1 and grad.index(max(grad))==3 and F(280,4430)>F(340,5950)
assert 340-(1029-19)//10==239 and 26480-5090==21390<5090*5 and max(total)==8811<min(total)*9;out['25']=dict(under=under,graduate=grad,total=total,employed40Lower=239)
debt=list(map(Q,[1828.8,1998.3,2192.4,2260.1,2241.4]));ratios=list(map(Q,[89.6,97.1,98.7,97.3,93.6]));gdp=[x/y*100 for x,y in zip(debt,ratios)]
assert list(map(tenths,gdp))==[2041.1,2058.0,2221.3,2322.8,2394.7]
mortgage=list(map(Q,[534,583.9,629.6,644.1,672.1]));diff=[mortgage[j+1]-mortgage[j] for j in range(4)];assert diff==list(map(Q,[49.9,45.7,14.5,28]))
assert Q(1757.1)>debt[2]*F(4,5) and Q(767.7)>Q(737.2);out['27']=dict(gdp=list(map(str,gdp)),mortgageDiff=list(map(str,diff)))
expense=[488100,537857,539790,588111,680711];growth=[F(expense[j+1]-expense[j],expense[j])*100 for j in range(4)];assert list(map(tenths,growth))==[10.2,.4,9,15.7]
hospital=7564*Q(19.52);outpatient=48189*Q(29.46);share=hospital/(hospital+outpatient)*100;assert tenths(share)==9.4
assert all(tenths(7564*(Q(19.52)+e)/1567411*100)==9.4 for e in [-F(5,1000),F(5,1000)])
institutions=[54634,90052,82324,67288,484185,4435,71882,6822,90374,7633,439435];assert sorted(institutions,reverse=True)[:5]==[484185,439435,90374,90052,82324] and tenths(F(82324,1399064)*100)==5.9
out['28']=dict(growth=list(map(str,growth)),approxAdmissionDays=str(hospital),approxOutpatientDays=str(outpatient),admissionShare=str(share),actualHospitalShare=str(F(82324,1399064)*100),clinicCost='Not supplied; cannot derive clinic-specific per-day cost.')
infected=[3047,2415,5554,3621];vaccinated=[5615,10610,12491,6698];rates=[F(i,v)*100 for i,v in zip(infected,vaccinated)];assert list(map(tenths,rates))==[54.3,22.8,44.5,54.1]
ages24=[Q(a)*Q(p)/100 for a,p in zip([1465,2368,1725,2091],[58,33.4,49.3,53.5])];assert ages24[1]<ages24[0]
# Original table2 rounding still cannot invert B<A or create the shown A/C split.
age2=[Q(n)*Q(p)/100 for n,p in zip(infected,[27.9,32.7,15.3,30.9])];assert infected[1]*Q(32.75)<infected[0]*Q(27.85)
out['30']=dict(infectionRates=list(map(str,rates)),age24FromTable3=list(map(str,ages24)),age24FromTable2=list(map(str,age2)),Cshares=[17.8,28.4,15.3,21.5,17],genderDenominator='Sex-specific vaccinated populations absent.')
dist=[605,988,795,1793];speeds=list(map(Q,[3.2,2.5,3.5,5]));capacity=[48,6,40,50];trips=[math.ceil(F(200,c)) for c in capacity];times=[F(d)/s for d,s in zip(dist,speeds)];alltimes=[t*n for t,n in zip(times,trips)];fares=[53000,86000,36000,60000]
assert trips==[5,34,5,4] and alltimes.index(min(alltimes))==0 and times[1]>=300>times[2] and fares.index(max(fares))==1 and fares.index(min(fares))==2;out['32']=dict(trips=trips,times=list(map(str,times)),totals=list(map(str,alltimes)),fares=fares)
solutions=[(c,k) for c in range(1,7) for k in range(6,11) if 7*(6-c)+k*c==38];assert solutions==[(4,6)] and 8*7==56 and 8*3==24;out['33']=dict(solutions=solutions,Cprice=42000)
monitors=[('갑',32,60,360,True),('을',27,100,480,True),('병',32,60,230,False),('정',32,75,530,True),('무',27,120,420,True)]
eligible=[m for m in monitors if m[1]>=30 and m[4]];best=max(eligible,key=lambda m:F(m[2],m[3]));assert best[0]=='갑'
cards=[('가',163,24,3100),('나',68,12,680),('다',52,8,520),('라',115,24,1600),('마',77,16,740),('바',39,8,380)]
feasible=[c for c in cards if c[1]>best[2] and 10*best[3]+32*c[3]<=30000];chosen=max(feasible,key=lambda c:c[2]);assert chosen[0]=='마' and 10*best[3]+32*chosen[3]==27280
out['35']=dict(eligibleMonitorNames=[m[0] for m in eligible],monitor=best,feasibleCards=feasible,selectedCard=chosen,total=27280)
prices=[78,77,76,76,75,74,73,73,72,70,70,68,67,66,65,64,63,62,63,64,65,66,67,68,70,71,72,73,73,74,75]
assert sum(prices)==2170
ships=[(date(2024,9,18),20,5,Q(1.1)),(date(2024,10,7),20,5,Q(1)),(date(2024,9,22),30,3,Q(1.1)),(date(2024,9,4),30,3,Q(1))];final=[];windows=[]
for day,lag,n,coef in ships:
 start=day+timedelta(days=lag);assert start.month==10;values=prices[start.day-1:start.day-1+n];assert len(values)==n;final.append(F(sum(values),n)*coef);windows.append([str(start),str(start+timedelta(days=n-1))])
final.append(F(sum(prices),31)*Q(1.1));assert final==list(map(Q,[77.66,73.4,73.7,75,77]));assert [sum(prices[a:b])-70*(b-a) for a,b in [(0,7),(7,14),(14,21),(21,28),(28,31)]]==[39,-4,-44,-3,12];out['36']=dict(windows=windows,prices=prices,monthlySum=2170,final=list(map(str,final)))
names='ABCDEFGHIJKLMNOP';known=[(1,1,0,0),(0,1,1,0),(1,1,0,0),(1,0,1,1),(0,0,1,1),(0,1,1,0),(0,1,1,0),(1,1,1,0),(1,1,0,1),(0,0,1,0),(0,1,1,1),(1,1,0,0),(1,1,0,1),(0,0,1,1),(1,1,1,0),(1,0,0,0)]
party=['triangle']*16;party[10]=party[11]='black';totals={'triangle':[8,12,9,5],'black':[2,6,2,2],'circle':[1,0,0,0]};sums={p:[sum(k[j] for k,pa in zip(known,party) if pa==p) for j in range(4)] for p in totals};qparties=[]
for qp in totals:
 rem={p:[totals[p][j]-sums[p][j]-(p==qp) for j in range(4)] for p in totals}
 if all(min(v)>=0 for v in rem.values()):qparties.append(qp);remaining=rem
assert qparties==['black'] and remaining=={'triangle':[0,3,0,0],'black':[0,3,0,0],'circle':[1,0,0,0]}
assert sum(map(sum,remaining.values()))==24-17==7 and sum(sum(x)==1 for x in known)+7==9
assert sum(x[0] and x[2] for x in known)+1==4 and not any(x==(0,0,0,1) for x in known);out['37']=dict(knownPartySums=sums,Qparty='black',remaining=remaining,singleType=9,houseAndLand=4)
sexgaps=[n*Q(g)/100 for n,g in zip(infected,[36,50,10,14])];assert min(sexgaps)==sexgaps[3] and infected[3]*Q(14.1)<infected[2]*Q(9.9)
assert infected[0]*Q(27.85)>infected[3]*Q(22.55) and Q(44.4)<Q(49.3) and infected[2]*Q(21.45)>infected[1]*Q(30.05) and Q(4)<Q(4.8);out['related29']=dict(sexGaps=list(map(str,sexgaps)),Dupper=str(infected[3]*Q(14.1)/100),Clower=str(infected[2]*Q(9.9)/100))
series=[[[4.7,5.5,6.8,9.7],[3.2,3.9,4.5,6.9]],[[3.6,3.9,4.6,5.2],[3.3,4.7,6.3,8.3]],[[5.3,6.8,7.7,8.3],[3.8,5.8,5.3,6.7]],[[4.9,5.7,7.1,8.5],[2.1,2.7,3.1,3.4]],[[3.3,4.1,6.4,7.2],[4.6,5.5,8.4,9.7]]];conditions=[]
for m,f in series:
 m=list(map(Q,m));f=list(map(Q,f));dm=[m[j+1]-m[j] for j in range(3)];df=[f[j+1]-f[j] for j in range(3)];gap0=abs(m[0]-f[0]);gap2=abs(m[2]-f[2]);conditions.append([min(dm+df)>0,gap0*F(3,2)<=gap2<gap0*2,all(y>x for x,y in zip(dm,df)),m[3]>=m[1]*Q(1.3) and f[3]>=f[1]*Q(1.3)])
assert [i for i,c in enumerate(conditions) if all(c)]==[4];out['related26']=dict(conditions=conditions)
r.write(b/'exact-model-checks.json',dict(status='PASS',models=out,phase='After frozen original-only solves; no answers changed.'))
print('PASS10 target and2related exact models, strict bounds and rounding')
