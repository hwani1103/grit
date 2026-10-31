from fractions import Fraction as F
from itertools import combinations
import review_remaining605 as r
b=r.folder(36);checks={}
assert F(662,832)<F(4,5) and F(59,62)>F(9,10) and 13+12+7+(258-57-199)==34<57
assert 258*3-597-2==175
checks[21]={'hybrid2024':str(F(662,832)),'decreaseShare':str(F(59,62)),'hydrogenThroughHalf2025':34,'EVupper175':True}
dom=[(35444,9478,5493),(60985,10319,7494),(36149,17742,10514),(12139,3732,2032)]
profit=[F(z,y) for x,y,z in dom];assert profit[1]>F(7,10)>F(6,10)>max(profit[:1]+profit[2:])
assert 60985+9594<2*(35444+6161) and F(119,1493)<F(282,3231)
design=[F(99,119),F(242,282),F(130,194),F(22,24)]
assert sum(v>=F(9,10) for v in design)==1 and F(2312,6161)>F(1358,9594) and F(689,2312)<F(788,1358)
checks[23]={'domesticProfitRatios':list(map(str,profit)),'designAbove90':1,'allFiveOptionsChecked':True}
income=[10181,10622,12240,15065,16454];balance=[-3175,-4329,-5715,-9692,-10038];out=[a-z for a,z in zip(income,balance)]
growth=lambda a:[F(y-x,x) for x,y in zip(a,a[1:])]
gi,go=growth(income),growth(out);assert min(gi+go)>0 and gi.index(max(gi))==go.index(max(go))==2
inbound=F(10622,10985)/F(10181,4041);ratio=F(17955,2739)/F(12240,3827)
assert inbound<F(2,5) and ratio<3
checks[24]={'outlays':out,'incomeGrowth':list(map(str,gi)),'outlayGrowth':list(map(str,go)),'inboundRemaining':str(inbound),'outboundInbound2022':str(ratio)}
processed=sum(map(F,['731.7','372.2','343','139','2861.6']));assert processed==F('4447.5') and processed/F('4034.4')-1>F('.05')
assert 400*F('1.2005')<F('490.2')
machineMax=660-660/F('1.0505');assert F('731.7')-F('590.2')>4*machineMax
fertilizerMin=F('207.6')*F('1.0695');assert fertilizerMin+F('67.2')>1502*F('.15')
checks[27]={'processed':str(processed),'pesticide400TimesMaxGrowth':str(400*F('1.2005')),'machineIncrementUpper':str(machineMax),'fertilizerAndDrugLower':str(fertilizerMin+F('67.2')),'rateRoundingHalfUnit':'.0005'}
pos=[('A','C'),('A','E'),('B1','B5'),('B2','B3'),('B2','B5'),('B2','B6'),('B2','B9'),('B2','K'),('B5','B9'),('B5','B12'),('B5','C'),('B9','B12'),('B9','C'),('C','E')]
neg=[('A','B12'),('A','K'),('B1','B2'),('B1','B3'),('B1','B6'),('B1','B12'),('B1','C'),('B2','B12'),('B6','B12'),('B12','C'),('B12','E'),('D','E'),('E','K')]
edges={frozenset(x):v for pairs,v in [(pos,1),(neg,-2)] for x in pairs};assert len(edges)==len(pos)+len(neg)
effect=lambda xs:len(xs)+sum(edges.get(frozenset(pair),0) for pair in combinations(xs,2))
assert effect(['B2','B9','K'])==5 and effect(['B3','B5','E'])==effect(['B3','B5','B12','E'])==3
counts=lambda n:(sum(n in pair for pair in pos),sum(n in pair for pair in neg))
assert counts('B2')==(5,2) and counts('B5')==(5,0)
checks[28]={'positivePairs':pos,'negativePairs':neg,'B2':counts('B2'),'B5':counts('B5'),'effects':[5,3,3],'unorderedPairsOnly':True}
ns=[5536,5332,3452,2498,723,534];assert sum(ns)==18075
rates=[F(x) for x in ['57.3','53.9','54.8','53.9','45.1','51.5']];expected=[32,29,19,14,3,3]
intervals=[]
for n,v,g in zip(ns,rates,expected):
 lo=F(n,18075)*(v-F('.05'))/(F('54.7')+F('.05'))*100
 hi=F(n,18075)*(v+F('.05'))/(F('54.7')-F('.05'))*100
 assert lo<g+F(1,2) and hi>=g-F(1,2)
 intervals.append([str(lo),str(hi)])
management=[71,92,10,108,14,12];reported=[F(x) for x in ['1.3','1.7','.3','4.3','1.9','2.2']]
assert sum(management)==307
for c,n,p,g in zip(management,ns,reported,[23,30,3,35,5,4]):
 assert p-F('.05')<=F(c,n)*100<p+F('.05') and g-F('.5')<=F(c,307)*100<g+F('.5')
assert F('1.65')<=F(307,18075)*100<F('1.75')
checks[29]={'industrySizes':ns,'fieldACompatibleIntervals':intervals,'managementIntegerWitness':management,'witnessNotActualCounts':True}
xs=[x for x in range(17) if F('24.5')<=31-F('.6')*x<F('25.5')];assert xs==[10]
checks[30]={'companyMonths':xs,'candidateUnrounded':[str(31-F('.6')*x) for x in range(8,13)],'appointment':'2024-09'}
assert 485*10>2296*2 and all(F(a,t)>F('.02') for a,t in zip([104,142,152,152,157],[3570,3887,4085,4176,4223]))
# Select the smallest lower bounds; every cross-tab placement uses the same marginal multiset.
lower=[0]*1932+[1]*916+[10]*471+[50]*132+[100]*119
assert len(lower)==3570 and sum(sorted(lower)[:2894])==1376>=1300
checks[33]={'minimumFor2894Firms':1376,'sortedMarginalLowerBounds':[[0,1932],[1,916],[10,46]],'notActualCrossTab':True,'all100PlusSharesAbove2':True}
assert F(397080,1091970)*100>36 and F(609573,144898)/F(277236,197327)>F('2.5')
x=F(1091970+397080,9);assert x==165450 and F(397080,x)*100==240<250
assert F(197327+397080,1091970)>F(197327+277236,1156237)
checks[34]={'youth2030Conditional':str(x),'agingConditional':240,'onlyElderlyDependencyLower':str(F(397080,1091970)*100),'agingRatio':str(F(609573,144898)/F(277236,197327))}
detached=[10343,19862,13184,13079,9224];apt=[28104,8319,15148,6024,5437];ratios=[F(a,b) for a,b in zip(detached,apt)];assert max(range(5),key=lambda i:ratios[i])==1
lo=30225*F('1.2005')-31466+881;hi=30225*F('1.2015')-31466+881
assert 5500<lo<hi and 13106<22755*F('.6')
assert [a+d+y+m+o for a,d,y,m,o in zip(apt,detached,[1656,1549,1603,1979,999],[1182,786,934,1163,1108],[694,692,597,510,476])]==[41979,31208,31466,22755,17244]
checks[35]={'detachedApartment':list(map(str,ratios)),'separateQuartersInterval':[str(lo),str(hi)],'Dbelow60':True,'noDoubleCountingMultifamily':True}
r.write(b/'exact-model-checks.json',dict(status='PASS',checks=checks,method='Individually specified models from original tables/graphs; exact fractions and explicit rounding intervals, not assertions copied from explanations.'))
print('PASS10 original numeric/graph models')
