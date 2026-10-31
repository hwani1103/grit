from fractions import Fraction as F
from itertools import combinations
from psat_batch_tools import validate
p={}
h=258-57-199;assert h==2
assert [F(749,931)>=F(4,5),F(690,869)>=F(4,5),F(662,832)>=F(4,5)]==[True,False,False]
assert F(59,62)>F(9,10) and 13+12+7+h<57 and 258*3-597-h==175
p['21']={'truth':[False,True,False,True],'hydrogenHalf':2,'annualElectricUpper':175}
business=[32457,4862,36259,6872,9612,1155,6639];staff=[182874,13543,69942,31403,84970,52597,74616];sales=[23895591,2739495,12633331,5903094,22964221,25402196,19419770];exports=[497290,177957,1222535,56291,8394003,1047219,337693];imports=[270991,6404,16971,48846,253765,65758,108959]
assert [sum(x) for x in [business,staff,sales,exports,imports]]==[97856,509945,112957698,11732988,771694]
balances=[x-y for x,y in zip(exports,imports)];ratio=[F(x,y) for x,y in zip(exports,sales)]
assert business[0]+business[2]>=F(sum(business))*F(7,10) and staff.index(max(staff))==0
assert sales.index(max(sales))==5 and max(range(7),key=lambda i:F(sales[i],business[i]))==5
assert exports[4]>=8*exports[5] and exports[4]>=F(sum(exports))*F(7,10)
rank=lambda vals,i:1+sum(v>vals[i] for v in vals)
assert (rank(exports,0),rank(balances,0))==(4,5)
assert max(ratio)-min(ratio)>F(35,100) and F(sum(exports),sum(sales))>F(1,10)
p['22']={'truth':[True,True,True,False,True],'publicationRanks':[4,5],'balances':balances,'maxMinGap':str(max(ratio)-min(ratio))}
dom=[(35444,9478,5493),(60985,10319,7494),(36149,17742,10514),(12139,3732,2032)];foreign=[(6161,2312,689),(9594,1358,788),(13569,6950,4932),(1065,232,90)];design=[(1493,119,99),(3231,282,242),(1030,194,130),(325,24,22)]
assert 60985+9594<2*(35444+6161)
assert F(119,1493)<F(282,3231)
assert max(range(4),key=lambda i:F(dom[i][2],dom[i][1]))==1
assert sum(F(c,b)>=F(9,10) for a,b,c in design)==1
assert F(2312,6161)>F(1358,9594) and F(689,2312)<F(788,1358)
p['23']={'truth':[False,False,True,False,False],'domesticRevenueRatios':[str(F(c,b)) for a,b,c in dom]}
income=[10181,10622,12240,15065,16454];balance=[-3175,-4329,-5715,-9692,-10038];spend=[a-b for a,b in zip(income,balance)];growth=lambda v:[F(b-a,a) for a,b in zip(v,v[1:])]
assert spend==[13356,14951,17955,24757,26492] and all(x>0 for x in growth(income)+growth(spend))
assert max(range(4),key=lambda i:growth(income)[i])==max(range(4),key=lambda i:growth(spend)[i])==2
visitors=F(10622*4041,10985*10181);travel=F(17955*3827,2739*12240)
assert visitors<F(2,5) and travel<3
p['24']={'truth':[True,True,False,False],'spend':spend,'remainingVisitorRatio':str(visitors),'travelerRatio':str(travel)}
players=[623,398,431,476,601,283,343,144,402,458];gold=[40,40,20,18,16,15,14,13,12,12];silver=[44,27,12,19,26,7,22,9,13,13];bronze=[42,24,13,16,22,12,29,10,15,8];total=[a+b+c for a,b,c in zip(gold,silver,bronze)]
r1=[rank(gold,i) for i in range(10)];r2=[rank(total,i) for i in range(10)]
assert r1[7]<r2[7] and sum(a==b for a,b in zip(r1,r2))==2
assert F(40,623)>2*F(12,402) and F(18,53)<F(12,33)
p['25']={'truth':[True,True,True,False],'totals':total,'goldRanks':r1,'totalRanks':r2}
assert 12328-1254-5007-1105-4812==150<1699-1534==165
assert 261+1814+2000+3116+379==7570<2*3807
assert 3807-350-652==2805>2623-14-64-66==2479>2152
assert 1690+14+150+25==1879>1872>33+1816+1==1850
assert 2192-2152-20==20
p['26']={'truth':[False,True,False,False,False],'sns':[150,165],'digitalWALK':2805,'changedTotal':1879,'rank':7,'omittedRowCounterexample':{'total':1600,'broadcast':100,'consistentTotalRank':11,'BreathingBroadcastRankAtLeast':6}}
processed=sum(map(F,['731.7','372.2','343','139','2861.6']));fert=F('207.6')*F('1.07');machineOld=F(660)/F('1.05')
assert processed==F('4447.5') and (processed-F('4034.4'))/F('4034.4')>F('0.05')
assert F('490.2')/F('1.2')==F('408.5')>400
assert F('731.7')-F('590.2')>4*(660-machineOld)
assert fert+F('67.2')>F('1502')*F('0.15')
# Rounded one-decimal growth percentages still leave strict margins.
assert F('490.2')/F('1.2005')>400
assert F('141.5')>4*(660-F(660)/F('1.0505'))
assert F('207.6')*F('1.0695')+F('67.2')>F('225.3')
p['27']={'truth':[True,False,True,False],'processed':str(processed),'roundedRateBoundaries':'399.5/4times/15pct all separated','fertilizer':str(fert)}
pos=[('A','C'),('A','E'),('B1','B5'),('B2','B3'),('B2','B5'),('B2','B6'),('B2','B9'),('B2','K'),('B5','B9'),('B5','B12'),('B5','C'),('B9','B12'),('B9','C'),('C','E')]
neg=[('A','B12'),('A','K'),('B1','B2'),('B1','B3'),('B1','B6'),('B1','B12'),('B1','C'),('B2','B12'),('B6','B12'),('B12','C'),('B12','E'),('D','E'),('E','K')]
P={frozenset(e) for e in pos};N={frozenset(e) for e in neg};assert not P&N
index=lambda combo:len(combo)+sum(1 if frozenset(e) in P else -2 if frozenset(e) in N else 0 for e in combinations(combo,2))
assert index(['B2','B9','K'])==5 and index(['B3','B5','B12','E'])==index(['B3','B5','E'])==3
counts=lambda v:(sum(v in e for e in P),sum(v in e for e in N))
assert counts('B2')==(5,2) and counts('B5')==(5,0)
p['28']={'truth':[False,True,False],'positive':pos,'negative':neg,'indices':[5,3,3]}
weights=list(map(F,['30.6','29.5','19.1','13.8','4','3']));rates=[[F(x) for x in row] for row in [['57.3','53.9','54.8','53.9','45.1','51.5'],['34.6','25.8','21.1','22.8','26.6','27.2'],['6.8','18.6','23.4','18.6','25.2','18.7'],['1.3','1.7','0.3','4.3','1.9','2.2'],['0','0','0.4','0.4','1.2','0.4']]]
# Use the original counts rather than compounding two rounded percentages.
sizes=[5536,5332,3452,2498,723,534];allRatios=[]
for row in rates:
 counts=[n*r for n,r in zip(sizes,row)];s=sum(counts);allRatios.append([int(v*100/s+F(1,2)) for v in counts])
assert allRatios[0]==[32,29,19,14,3,3]
witness=[71,92,10,108,14,12];totalWitness=sum(witness)
assert F('1.65')<=F(totalWitness*100,18075)<F('1.75')
for n,c,r in zip(sizes,witness,rates[3]):assert r-F('.05')<=F(c*100,n)<r+F('.05')
assert [int(F(c*100,totalWitness)+F(1,2)) for c in witness]==[23,30,3,35,5,4]
p['29']={'A':'현장실무','B':'경영','midpointApproximationsRounded':allRatios,'managementIntegerWitness':witness,'roundingNote':'Displayed rates have +/-0.05 pct uncertainty; management witness fits all six sectors, overall1.7 and pie integer labels.'}
results=[F(31)-F(3,5)*x for x in range(8,13)];assert results==list(map(F,['26.2','25.6','25','24.4','23.8']))
assert [x for x in range(17) if F('24.5')<=31-F(3,5)*x<F('25.5')]==[10]
p['30']={'companyMonths':10,'localStart':'2024-09','optionWeightedSums':list(map(str,results))}
validate('data18',p,[('2026-03-07',i) for i in range(21,31)],figure_count=24)
