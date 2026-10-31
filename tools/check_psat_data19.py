from fractions import Fraction as F
import itertools as it
from psat_batch_tools import validate
proof={}
standard=[2,5,4];capacity=[4,8,4];friday=[91,168,360]
def room(k,n,price):return price[k]+max(0,n-standard[k])*15
costs=[room(a,n,friday)+room(b,7-n,friday) for a,b in it.product(range(3),repeat=2) for n in range(1,7) if n<=capacity[a] and 7-n<=capacity[b]]
assert (min(costs),max(costs))==(227,720)
assert 91<80+15 and 2*91+2*15>180+15
proof['31']={'truth':[False,True,True],'allTwoRoomCosts':costs,'range':[227,720],'difference':493}
best=[0]+[10**9]*8
for n in range(1,9):
 for k in range(3):
  for size in range(1,min(n,capacity[k])+1):
   price=room(k,size,friday)+size*17
   if k==0:price=min(price,120+max(0,size-2)*32)
   best[n]=min(best[n],best[n-size]+price)
assert best[8]==349 and 116+15+15==146 and 70+16==86
proof['32']={'truth':[True,False,True],'minimumEightByDynamicProgramming':349,'packageTwoRooms':368}
total=[3570,3887,4085,4176,4223];large=[65+39,90+52,95+57,87+65,89+68]
assert all(F(a,b)>=F(2,100) for a,b in zip(large,total))
assert 485*10>2296*2
minimum=sum(([0]*1932+[1]*916+[10]*471+[50]*132+[100]*119)[:2894]);assert minimum==1376>1300
proof['33']={'truth':[True,True,True],'largeEmployees':large,'minimumProductionOf2894':'1376hundredMillion','remainingAtLeast10':46}
assert F(397080,1091970)*100>36
i2020=F(277236,197327)*100;i2040=F(609573,144898)*100
assert i2040>F(5,2)*i2020
youth=F(1091970+397080,9);assert youth==165450 and F(397080,youth)*100==240<250
assert F(197327+397080,1091970)>F(197327+277236,1156237)
proof['34']={'truth':[True,False,False,True],'youth':165450,'index':240,'indexChange':str(i2040/i2020)}
households=[39492,30685,30225,19175,17365];apartments=[28104,8319,15148,6024,5437];detached=[10343,19862,13184,13079,9224];multi=[895,950,881,923,269];town=[1656,1549,1603,1979,999];plex=[1182,786,934,1163,1108];other=[694,692,597,510,476]
homes=[a+b+c+d+e for a,b,c,d,e in zip(apartments,detached,town,plex,other)]
assert homes==[41979,31208,31466,22755,17244]
ownerFamilies=[23335,19740,17778,12298,10266];private=[32472,27802,25726,19804,13057];local=[26089,21092,20614,13106,10904];outside=[6383,6710,5112,6698,2153]
assert max(range(5),key=lambda i:F(detached[i],apartments[i]))==1
limitLow=F(30225)*F('1.2005')-31466+881;limitHigh=F(30225)*F('1.2015')-31466+881
assert limitLow>5500 and local[3]<F(3,5)*homes[3]
proof['35']={'truth':[True,True,False],'separateUnitRange':[str(limitLow),str(limitHigh)],'DlocalRatio':str(F(local[3],homes[3]))}
round1=lambda v:F(int(v*10+F(1,2)),10)
ownership=[round1(F(a,b)*100) for a,b in zip(ownerFamilies,households)]
assert ownership==list(map(F,['59.1','64.3','58.8','64.1','59.1']))
assert sum(homes)==144652 and sum(private)==118861 and round1(F(sum(private),sum(homes))*100)==F('82.2')
actualOutside=[round1(F(a,b)*100) for a,b in zip(outside,local)];assert actualOutside==list(map(F,['24.5','31.8','24.8','51.1','19.7']))
proof['36']={'truth':[True,False,True,False],'ownership':list(map(str,ownership)),'privateSum':118861,'total':144652,'outsideRatios':list(map(str,actualOutside))}
parking=[154,107,53,44,27,21,14,13,11,3];bikes=[1700,1553,1600,458,424,267,568,130,514,493];hires=[964937,1580187,1227900,160133,213070,99606,47244,60117,62570,392633]
directKnown={3,5,7};unknown={2,4,6,8,9};solutions=[]
for extra in it.combinations(unknown,2):
 direct=directKnown|set(extra)
 for x in direct:
  if F(hires[x],parking[x])>=5000 and all(bikes[x]>bikes[y] and parking[x]<parking[y] and F(hires[x],bikes[x])<F(hires[y],bikes[y]) for y in direct-{x}) and F(hires[x],bikes[x])>=100:solutions.append((x,sorted(direct)))
assert solutions==[(8,[3,4,5,7,8])]
proof['37']={'reportRegion':'I','directRegions':'D E F H I','allAssignments':solutions,'answerPair':'E direct'}
rows=[[1,1,0,1,0,1,1,1,1,1],[1,1,0,0,1,0,1,1,1,1],[0,1,1,1,1,1,1,1,None,None],[1,1,1,1,1,1,1,1,None,None],[0,1,0,1,1,1,1,1,1,1],[0,1,1,1,1,0,1,1,None,None],[1,1,0,1,0,1,0,0,1,1],[1,1,1,1,1,1,1,0,None,None],[0,1,0,1,1,0,0,0,None,None],[1,0,0,1,1,0,1,0,None,None]]
correct=[8,7,8,9,8,7,6,8,5,4];points=[2]*5+[3]*5
assert sum(a*b for a,b in zip(correct,points))==170
valid=[]
for bits in it.product([0,1],repeat=4):
 rr=[r[:] for r in rows]
 for j,k in zip([2,3,5,7],bits):rr[j][8:]=[k,1-k]
 rr[8][8:]=[1,1];rr[9][8:]=[0,0]
 assert list(map(sum,rr))==correct
 scores=[sum(rr[j][s]*points[j] for j in range(10)) for s in range(10)]
 if len(set(scores))!=10:continue
 assert [scores[i] for i in [0,1,4,5,7]]==[15,22,20,14,13]
 all2=sum(all(rr[j][s] for j in range(5)) for s in range(10))
 tenth=[scores[s] for s in range(10) if rr[9][s]]
 assert max(scores)-min(scores)==13 and all2==4 and F(sum(tenth),len(tenth))==F(77,4)>scores[6]
 valid.append(scores)
assert len(valid)==2 and {tuple(sorted(v[8:])) for v in valid}=={(16,18)}
proof['38']={'truth':[False,True,True,True],'mean':17,'allScores':valid,'item10Mean':'77/4'}
flag=[{1,3,4,7,8,9},{1,2,5,7,8,9,10},{1,4,5,7,10},{1,2,5,6,8}];precision=list(map(F,['1/3','3/7','3/5','2/5']));recall=list(map(F,['2/3','1','1','2/3']));actual=[]
for bits in it.product([0,1],repeat=10):
 bad={i+1 for i,v in enumerate(bits) if v}
 if not bad:continue
 if all(F(len(bad&s),len(s))==p and F(len(bad&s),len(bad))==r for s,p,r in zip(flag,precision,recall)):actual.append(sorted(bad))
assert actual==[[1,5,7]]
assert len(flag[0]-set(actual[0]))==4
assert F(len(flag[3]&set(actual[0]))+len(set(range(1,11))-flag[3]-set(actual[0])),10)==F(3,5)
proof['39']={'truth':[True,False,True],'actualBad':actual[0],'AfalseBad':4,'Dconfusion':[2,4,3,1]}
temp=list(map(F,['.5','.4','1.2','.9','.2','-.7','-.8','.7','-.8','1']))
rainDelta=list(map(F,['35.8','22.4','9.9','18.7','-1.2','5.9','10','11.2','28.5','35.3']));rainRatio=[F(x)/100 for x in ['225.2','246.4','185.3','247.5','95.4','132.6','150.3','147.1','255.7','202.6']]
sunDelta=list(map(F,['-15.3','-22','-7.4','-14.2','-22.8','-26.5','-29.6','-24.8','-26.3','-26.3']));sunRatio=[F(x)/100 for x in ['76.6','65','88','75.2','62.9','57.5','54','58.2','59.5','50.7']]
rainBase=[d/(r-1) for d,r in zip(rainDelta,rainRatio)];sun=[d/(r-1)*r for d,r in zip(sunDelta,sunRatio)]
assert sum(t<0 for t in temp)==3 and max(range(10),key=lambda i:rainBase[i])==9
assert rainRatio.index(max(rainRatio))==8 and sunRatio.index(min(sunRatio))==9
assert sunRatio[5]/rainRatio[5]>F(2,5) and sun[9]<sun[6]
proof['40']={'truth':[False,False,False,False,True],'rainBaselines':list(map(str,rainBase)),'actualSun':list(map(str,sun))}
validate('data19',proof,[('2026-03-07',i) for i in range(31,41)],figure_count=30)
