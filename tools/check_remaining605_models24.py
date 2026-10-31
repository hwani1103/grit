from fractions import Fraction as F
import review_remaining605 as r
b=r.folder(24);checks={}
# Values transcribed from original images, before deriving the results.
disabled=[10213,11610,11512,12243,12331];women=[48967,53494,57896,63561,67332];social=[4558,5166,5410,5864,6201]
totals=[sum(v) for v in zip(disabled,women,social)]
assert all(a<c for a,c in zip(totals,totals[1:])) and all(w>max(d,s) for d,w,s in zip(disabled,women,social))
enterprises=[471100,502710,536305,572118,602681];femaleEnterprises=[108105,118908,131203,144924,156406]
assert femaleEnterprises[-1]*4>=enterprises[-1]
assert all(c*100>=a*105 for a,c in zip(femaleEnterprises,femaleEnterprises[1:]))
allContracts=[480545,513566,572121,595782,707205]
assert [w*10>=t for w,t in zip(women,allContracts)]==[True]*4+[False]
assert F(women[-1],10000)>=F('6.7')
assert [7,5,1,3]!=sorted([7,5,1,3],reverse=True) # original public subcategories: company, quasi, local, other
checks['d10']=dict(socialTotals=totals,womenAllLargest=True,womenEnterpriseGrowth=[str(F(c-a,a)) for a,c in zip(femaleEnterprises,femaleEnterprises[1:])],statements=[False,True,True,True],answer=5)

totalRD=[168777,177428,189231,190942,194615];health=[9319,11315,11050,11368,11317]
ministries={'과기정통부':[2548,2711,3335,3577,4111],'농식품부':[487,462,479,590,682],'산업부':[1887,3089,1583,1929,1491],'복지부':[3830,4410,4924,4608,4531],'환경부':[82,123,134,138,149],'식약처':[218,272,313,335,353],'농진청':[267,248,282,191,0]}
assert [sum(v[i] for v in ministries.values()) for i in range(5)]==health
monotone=[k for k,v in ministries.items() if all(c>a for a,c in zip(v,v[1:]))]
growth={k:F(v[-1]-v[-2],v[-2]) for k,v in ministries.items()};shares=[F(h,t) for h,t in zip(health,totalRD)]
assert monotone==['과기정통부','환경부','식약처'] and max(growth,key=growth.get)=='농식품부'
assert ministries['농식품부'][-1]-ministries['농식품부'][-2]==92
assert growth['농식품부']>F('.15')>growth['과기정통부']
assert all(s>=F('.055') for s in shares) and [s>F('.06') for s in shares]==[False,True,False,False,False]
checks['d11']=dict(monotone=monotone,growth={k:str(v) for k,v in growth.items()},shares=list(map(str,shares)),agricultureIncrease=92,ownFrozenCorrection='own-arithmetic-correction.json',answer=4)

fresh=[[F(x) for x in row] for row in [('99.5','98.3','99.6','100'),('99.4','95.2','99.8','100'),('92.9','68.5','98.7','99.9')]]
enrolled=[[F(x) for x in row] for row in [('95.7','79.7','95.2','104.8'),('97.8','89.5','97','103'),('94.7','82.1','96.2','101.9')]]
assert min(range(3),key=lambda i:fresh[i][1])==min(range(3),key=lambda i:fresh[i][2])==2
assert max(range(3),key=lambda i:fresh[i][0])==0 and max(range(3),key=lambda i:enrolled[i][0])==1
distances=[abs(v[0]-v[2]) for v in enrolled];assert distances==[F('.5'),F('.8'),F('1.5')]
assert F('64.3')>F('63.6') # Fifth-largest strictly exceeds sixth-largest median in 11 distinct values.
checks['d12']=dict(distances=list(map(str,distances)),medianDescendingRank=6,statements=[True,False,True,True],answer=4)

assert 33353>7564*4 and 3871-3705==166 and 166<F(3871,20)
assert F(396,7564)<F(3297,7168) and F(8558,33353)<F(18243,24795)
assert F(6552,9645*4)<F(3871,9645)
checks['d13']=dict(restaurant1980=166,spending4x=30256,food4x=15484,statements=[True,False,False,True],answer=3)

unit=[210,120,100,80];facility=[200,100,50,60];operation=[10,20,50,20];output=[59,40,153,212]
assert [a+c for a,c in zip(facility,operation)]==unit
cost=[a*c for a,c in zip(unit,output)];operating=[a*c for a,c in zip(operation,output)]
assert cost==[12390,4800,15300,16960] and operating==[590,800,7650,4240]
assert unit[1]<unit[0] and output[1]<output[0]
assert F(operation[0],unit[0])<F(operation[3],unit[3]) and output[0]<output[3]
checks['d14']=dict(costProducts=cost,operatingProducts=operating,statements=[False,True,False,True],answer=4)
average=F(sum(unit),4);subsidy=unit[0]-average
updated=[facility[0]*F('.1')+operation[0],facility[1]*F('1.4')+operation[1],facility[2]*F('.5')+operation[2]+25,facility[3]*F('.5')+operation[3]+10]
assert average==F('127.5') and subsidy==F('82.5') and updated==[30,160,100,60]
checks['d15']=dict(arithmeticAverage=str(average),subsidy=str(subsidy),updatedCosts=list(map(str,updated)),gap=max(updated)-min(updated),answer=3)
checks['d15']['gap']=str(checks['d15']['gap'])

traffic={'A':[9509,3177,217,53242],'B':[13565,6204,327,86851],'C':[2948,1675,64,16305],'D':[3350,1464,72,20053],'E':[2385,1211,68,17824],'F':[1121,581,27,7376]}
total=[sum(v[i] for v in traffic.values()) for i in range(4)];assert total==[32878,14312,775,201651]
assert traffic['C'][0]>traffic['E'][0] and traffic['C'][3]<traffic['E'][3]
assert traffic['C'][1]>traffic['D'][1] and traffic['C'][2]<traffic['D'][2]
perPopulation={k:F(v[2],v[0]) for k,v in traffic.items()};perVehicle={k:F(v[3],v[1]) for k,v in traffic.items()}
assert perPopulation['E']>perPopulation['B'] and perVehicle['C']<10<12<perVehicle['F']
assert F(16305,64)<260<F(201651,775)
checks['d17']=dict(total=total,perPopulation={k:str(v) for k,v in perPopulation.items()},perVehicle={k:str(v) for k,v in perVehicle.items()},separatingValue=260,answer=5)

taxes={'소득세':('115.8','125.8','117.4'),'법인세':('80.4','77.7','62.5'),'증여세':('14.6','14.7','15.3'),'부가가치세':('73.8','81.4','82.2'),'개별소비세':('8.8','10.2','8.7'),'증권거래세':('6.1','5.4','4.8'),'교통세':('10.8','15.3','11.4'),'관세':('7.3','8.9','7'),'종합부동산세':('4.6','4.1','4.2')}
taxes={k:list(map(F,v)) for k,v in taxes.items()};assert [sum(v[i] for v in taxes.values()) for i in range(3)]==list(map(F,['322.2','343.5','313.5']))
decrease={k:v[0]-v[2] for k,v in taxes.items()};budgetDiff={k:abs(v[0]-v[1]) for k,v in taxes.items()};error={k:abs(v[2]-v[1])/v[2] for k,v in taxes.items()}
assert max(decrease,key=decrease.get)=='법인세' and max(budgetDiff,key=budgetDiff.get)=='소득세' and max(error,key=error.get)=='교통세'
assert [k for k,v in error.items() if v>F(1,3)]==['교통세']
assert taxes['법인세'][0]>taxes['부가가치세'][0] and taxes['법인세'][2]<taxes['부가가치세'][2]
checks['d18']=dict(decrease={k:str(v) for k,v in decrease.items()},budgetDiff={k:str(v) for k,v in budgetDiff.items()},error={k:str(v) for k,v in error.items()},statements=[True,True,True,False],answer=4)

cities={'브뤼셀':[620,570,319],'빈':[298,255,195],'리스본':[294,336,94],'도쿄':[226,201,258],'서울':[200,136,265],'런던':[139,148,101],'파리':[124,130,153],'마드리드':[116,154,37],'바르셀로나':[115,147,67],'두바이':[114,73,67]}
increased=[k for k,v in cities.items() if v[0]>v[1]];assert increased==['브뤼셀','빈','도쿄','서울','두바이']
assert 408>399<493 and 265>F(473,2)
residual=395-116-115;assert residual==164>114 and (residual+113)//114==2
# Countermodel for option2: an omitted US city may have2021=350,2023=100;
# remaining US totals are162 and533, distributable over other omitted cities.
assert 350>319 and 350<=512 and 100<=114 and 633-100==533
checks['d21']=dict(increasedCities=increased,residualSpain=164,omittedCityUpperBound=114,minAdditionalSpainCities=2,option2Countermodel=dict(country='US',year2021City=350,country2021=512,year2023City=100,country2023=633),answer=5)

assert 4495-4154==341<374 and 5027*10<7501*7 and 4581-420==4161<4200
assert 7501-6521==980<F(6521,5)
assert F(4532,5027)<F(3979,4353)
assert F(374,4353)<F('.09')<F(495,5027)
checks['d22']=dict(reduced2021=341,full2022=4161,populationIncrease=980,fullShares=[str(F(3979,4353)),str(F(4532,5027))],answer=2)
r.write(b/'calculation-checks.json',dict(status='PASS',method='Same-author fresh exact-arithmetic checks from original charts and tables; no independent reviewer claim.',checks=checks,ownReasoningCorrections=['d11 subtraction102 corrected to92; frozen original retained; published explanation already92; answer4 unchanged.']))
print('PASS10 original-data models and thresholds; d11 own arithmetic corrected transparently.')
