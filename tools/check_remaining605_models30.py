from fractions import Fraction as F
from collections import Counter
import review_remaining605 as r
out=[]
def record(n,evidence):out.append(dict(id=r.batch(30)[n]['id'],evidence=evidence))
weather=['sun','part','snow','part','rain','snow','snow','part','sun','sun','cloud','rain','sun','sun','sun','sun','part','part','rain','snow','sun','snow','rain','part','rain','snow','part','rain','rain','sun','sun']
high=[3,5,9,10,6,4,6,8,5,12,13,8,15,17,21,17,18,12,12,5,8,15,14,14,10,8,17,14,17,19,16]
low=[-5,-6,-1,-1,-2,-2,-1,-1,-2,-2,7,-1,-1,7,11,7,6,1,4,0,1,1,6,5,6,1,1,11,9,7,6]
counts=Counter(weather);diff=Counter(a-b for a,b in zip(high[:10],low[:10]));rain=[low[i] for i,w in enumerate(weather) if w=='rain']
bins=[sum(x<0 for x in rain),sum(0<=x<5 for x in rain),sum(5<=x<10 for x in rain),sum(x>=10 for x in rain)]
peak={w:max((high[i],i+1) for i,v in enumerate(weather) if v==w) for w in counts}
assert [counts[k] for k in ['sun','part','cloud','snow','rain']]==[10,7,1,6,7] and diff[11]==2 and diff[12]==0 and peak['part']==(18,17) and bins==[2,1,3,1]
record(0,dict(weatherCounts=counts,firstTenRanges=dict(diff),peakDays=peak,rainLows=rain,rainBins=bins,truth=[True,False,False,True]))
battery=[['38.5','30.5',62,100,222,20900],['37','30.6',70,108,239,17900],['37','29.6',60,104,218,42100],['37','25.6',52,91,220,35400],['38.5','31.2',64,113,176,22300],['37','33.8',54,93,227,21900]]
ratio=[F(x[1])/F(x[0]) for x in battery];assert ratio.index(max(ratio))==5
assert min(range(6),key=lambda i:battery[i][2])==min(range(6),key=lambda i:battery[i][3])==3
assert max(battery[i][4] for i in [2,4])<min(battery[i][4] for i in [0,1,3,5])
av=[sum(battery[i][5] for i in [0,2])//2,F(sum(battery[i][5] for i in [1,3,4,5]),4)]
assert av[0]>av[1] and battery[3][5]<2*min(x[5] for x in battery)
record(1,dict(ratios=list(map(str,ratio)),magnetMeans=list(map(str,av)),flashPrice=35400,doubleMinimum=35800,truth=[True,True,True,True,False]))
totals=[25,29,21,12,14];percent=[[8,20,40,28,4],[6.9,13.8,41.4,20.7,17.2],[0,14.3,52.4,28.6,4.8],[0,25,58.3,16.7,0],[7.1,21.4,35.7,28.6,7.1]]
city=[]
for total,ps in zip(totals,percent):
 row=[]
 for p in ps:
  matches=[k for k in range(total+1) if abs(F(100*k,total)-F(str(p)))<=F(1,20)]
  assert len(matches)==1;row+=matches
 assert sum(row)==total;city.append(row)
region=[sum(row[j] for row in city) for j in range(5)];assert region==[5,18,45,25,8]
assert city[3][2]==city[0][3]==7 and max(x[2] for x in city)<3*min(x[2] for x in city) and city[4][3]<2*city[2][1] and F(city[1][4],region[4])>F(1,2)
record(2,dict(integerCounts=city,regionTotals=region,rounding='Unique integer within ±0.05 percentage point of every displayed one-decimal percent.',truth=[True,False,False,False,False]))
industry=[[6,6,1,1],[272,276,297,303],[146,175,165,170],[8,8,7,7],[21,23,17,17],[6,6,7,7],[1,1,1,1],[7,7,14,14],[86,87,75,78]]
assert sum(x[1] for x in industry)==589 and sum(x[3] for x in industry)==598
growth=[F(x[0]-x[2],x[2]) for x in industry[:-1]];deathdiff=[x[1]-x[3] for x in industry[:-1]]
assert growth.index(max(growth))==0 and deathdiff.index(max(deathdiff))==4
types=['떨어짐','넘어짐','깔림ㆍ뒤집힘','부딪힘','물체에 맞음','무너짐','끼임','절단ㆍ베임ㆍ찔림','감전','화재ㆍ폭발ㆍ파열','이상온도 접촉','화학물질 누출ㆍ접촉','산소결핍','빠짐ㆍ익사','기타']
c25=[159,0,15,16,40,13,8,1,13,2,1,3,0,5,0];cd=[-23,-3,1,-14,8,-11,0,0,9,2,0,3,-1,2,0]
m25=[21,0,21,18,21,3,41,0,3,35,1,6,1,4,0];md=[-10,0,3,-11,4,-3,5,-1,0,13,-2,5,-1,3,0]
larger=[types[i] for i in range(15) if m25[i]>c25[i]];assert len(larger)==6 and cd[3]<0 and md[3]<0
record(3,dict(farm2025=7,forest2024=7,growth=list(map(str,growth)),deathIncrements=deathdiff,manufacturingGreater=larger,truth=[True,False,True,True,True]))
c24=[a-b for a,b in zip(c25,cd)];m24=[a-b for a,b in zip(m25,md)]
rank=lambda xs:sorted(zip(xs,types),reverse=True)
assert sum(c24)==303 and sum(m24)==170 and rank(c24)[1]==(32,'물체에 맞음') and rank(m24)[1]==(31,'떨어짐')
record(4,dict(construction2024=c24,manufacturing2024=m24,seconds=[rank(c24)[1],rank(m24)[1]],truth=[True,False,False,False,False]))
cases=[31681,30982,21832,18902,19039,23360];money=[7000,7744,5438,4472,7257,11330]
ratios=[F(a,b) for a,b in zip(money,cases)];increases=[F(money[i]-money[i-1],money[i-1]) for i in [4,5]]
assert ratios[0]<F(23,100)<ratios[3] and increases[0]>F(3,5)>increases[1] and F(8883+1625+2324+3156,cases[3])<F(9,10)
assert sum([8883,1625,2324,3156,2135,779])==cases[3]
record(5,dict(perCase=list(map(str,ratios)),growth=list(map(str,increases)),sixtyPlus=2914,truth=[False,True,False]))
trees=[[25922,1600,14430,6784],[15553,1210,2658,1719],[74254,5374,19747,17890],[3679,0,3190,2137],[14550,1415,8127,2509],[18229,123,1215,465],[13379,0,1519,0],[334,0,76,0],[0,0,0,2045]]
wood=[sum(row[j] for row in trees) for j in range(4)];assert wood==[165900,9722,50962,33549]
rr=[F(trees[2][j],trees[0][j]) for j in range(4)];second=sorted(range(4),key=lambda j:rr[j],reverse=True)[1]
assert second==0 and sum(row[0]>0 for row in trees)==8 and trees[3][0]<sum(trees[3][1:])
third=[sorted(range(9),key=lambda i:trees[i][j],reverse=True)[2] for j in [0,1]];assert third==[5,4]
herbs=[8723,34327,11246,14510];area=[7300,6130,10470,4530];density=[F(a,b) for a,b in zip(herbs,area)]
assert density.index(min(density))==2 and wood.index(max(wood))==0 and F(herbs[3],wood[3])<F(44,100)<2*F(herbs[2],wood[2])
record(6,dict(woodTotals=wood,ratios=list(map(str,rr)),thirdSpeciesIndices=third,herbDensity=list(map(str,density)),truth=[False,True,False,False,False]))
a=[300,150,50,100,250];bb=[300,100,50,400,150];assert sum(a)==850 and sum(bb)==1000
mag=[];signed=[]
for y,z in zip(a,bb):
 common=lambda x:175<=y+z+x<=800
 mm=[x for x in range(801) if common(x) and abs(x-y)<=100 and 2*abs(x-z)<=z]
 ss=[x for x in range(801) if common(x) and x-y<=100 and 2*(x-z)<=z]
 mag.append([min(mm),max(mm)]);signed.append([min(ss),max(ss)])
assert mag==[[200,200],[50,150],[75,75],[200,200],[150,225]]
assert [sum(x[j] for x in mag) for j in [0,1]]==[675,850] and [sum(x[j] for x in signed) for j in [0,1]]==[75,850]
record(7,dict(magnitudeIntervals=mag,signedUpperOnlyIntervals=signed,interpretation='Both interpretations recorded in original-only solve BEFORE reveal. Existing explanation already uses magnitude; raw dialogue will not be rewritten to add an absolute-value condition.',noPostRevealAnswerChange=True))
y0=list(map(F,['84.1','72.8','39.4','78.9','45.7','54.3']));y1=list(map(F,['71.9','34.7','24.8','35.6','27.8','37.1']));o0=list(map(F,['6','6.8','16.3','7.3','15.9','11.7']));o1=list(map(F,['6.3','13.1','29.5','13.4','25.8','20.1']))
diff=[a-b for a,b in zip(y0,y1)];gap=[abs(a-b) for a,b in zip(y1,o1)];burden=[a+b for a,b in zip(y1,o1)]
assert diff.index(max(diff))==3 and gap.index(min(gap))==4
for ys,os in [(y0,o0),(y1,o1)]:
 ratios=[o/y for o,y in zip(os,ys)];assert ratios.index(max(ratios))==2
assert burden.index(max(burden))==0 and burden.index(min(burden))==1 and y1[4]/(100+burden[4])>y1[2]/(100+burden[2])
record(8,dict(yearDifferences=list(map(str,diff)),absoluteGaps=list(map(str,gap)),totalBurden=list(map(str,burden)),truth=[True,True,True,False,True]))
quotas=[[210,69,72,61,53,25],[153,26,23,12,12,0],[808,347,366,293,239,118]]
actual=[[195,69,69,56,44,20],[52,5,2,1,0,0],[924,396,418,313,267,109]]
vac=[]
for qs,aa in zip(quotas,actual):
 qs=qs+[sum(qs)];aa=aa+[sum(aa)];vac.append([0 if q==0 or n>q else round(F(100*(q-n),q)) for q,n in zip(qs,aa)])
assert vac==[[7,0,4,8,17,20,8],[66,81,91,92,100,0,73],[0,0,0,0,0,8,0]]
assert round(F(4550,44))==103 and round(F(5510,56))==98
assert [round(F(100*(q-n),q)) for q,n in [(234,198),(221,176),(226,60)]]==[15,20,73] and round(F(100*(198-60),198))==70
record(9,dict(derivedVacancies=vac,historicalVacancyRounded=[15,20,73],patientPerSpecialistThousands=['455/44','551/56'],historicalActualReductionRounded=70,additionalNeeded=['ㄱ','ㄴ'],notNeeded='ㄷ is derivable from current table including zero-quota and overstaffed exceptions.'))
r.write(r.folder(30)/'independent-calculation-paths.json',dict(status='PASS',method='Exact fractions/exhaustive finite bounds from manually read original; same-author calculation crosscheck.',questions=out))
print('PASS exact models all10, including alternate signed-bound interpretation.')
