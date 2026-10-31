from fractions import Fraction as F
from datetime import date,timedelta
from psat_batch_tools import validate
p={}
assert F('5.68')<F('6.98') and F(100)-F('16.67')==F('83.33')>=80
assert F('19.36')>F('13.89')
awareness=list(map(F,['3.7','4.2','2.8','1.5','3.3']));satisfaction=list(map(F,['4.2','3.5','3.3','4.1','2.9']))
assert 1+sum(v>awareness[0] for v in awareness)==2 and max(satisfaction)==satisfaction[0]
p['1']={'truth':[False,True,False,True],'underHour':'83.33','wrongOrder':['shopping5.68<business6.98','failures19.36>network13.89']}
assert all(a<b for a,b in zip([48225,13093,5527],[51004,13173,5543]))
assert [51004-48225,13173-13093,5543-5527]==[2779,80,16]
assert min([35430,738,14836])==738 and min([10149,181,2843])==181 and min([4098,103,1342])==103
assert F(36217,52116)<F(10248,13262) and F(120,5340)>F(103,5543)
p['2']={'ABC':['버스','작았다','증가'],'carRatios':[str(F(36217,52116)),str(F(10248,13262))]}
first=list(map(F,['185','84.7','71.2','51.4','28.6','22.7','22.3','21.4','14.7','10.6','9','8.4','8.5','5.7','8.6','5.1']));last=list(map(F,['206','112.2','96.3','55.3','26','24.4','22.9','20.8','20','12.2','9.9','9','8.6','6.4','4.6','4.2']))
assert F(185)/F('557.9')*100>33 and last[8]-first[8]==F('5.3')!=F('-2.7')
p['3']={'truth':[True,False,True,False],'all2023Levels':list(map(str,last)),'all2021to2023Differences':list(map(str,[b-a for a,b in zip(first,last)])),'resourceSeries':[['314.8','350.2','369.4'],['60.2','62.8','71.6'],['182.9','194.6','197.7']]}
central=[26,19,49,28,35,37,29,16,34,54,17,33,31,29];south=[31,30,46,28,36,29,32,14,35,38,17,34,33,36]
assert max(range(14),key=lambda i:south[i])+2011==2013 and sum(a>=40 and b>=40 for a,b in zip(central,south))==1
end2014=date(2014,7,2)+timedelta(days=27);assert (end2014.month,end2014.day)==(7,29)
start2017=date(2017,7,29)-timedelta(days=28);assert start2017==date(2017,7,1)
assert date(2015,6,25)+timedelta(days=34)==date(2015,6,24)+timedelta(days=35)==date(2015,7,29)
p['4']={'truth':[False,True,False,True],'central2017Start':'07-01','2015Ends':['07-29','07-29']}
recruitA=[4,3,5,16,32];recruitB=[14,26,15,3,5];applyA=[156,30,97,248,702];applyB=[229,358,201,19,42]
assert [sum(recruitA),sum(recruitB),sum(applyA),sum(applyB)]==[60,63,1233,849]
assert F(1233,849)>F('1.2') and applyA.index(max(applyA))==recruitA.index(max(recruitA))==4 and applyB.index(max(applyB))==recruitB.index(max(recruitB))==1
ratA=[F(a,b) for a,b in zip(applyA,recruitA)];ratB=[F(a,b) for a,b in zip(applyB,recruitB)]
assert F(1233,60)>20>F(849,63) and 1+sum(r>ratA[4] for r in ratA)==2 and min(ratB)==ratB[3]<ratB[4]
p['5']={'truth':[True,True,True,True,False],'ratiosA':list(map(str,ratA)),'ratiosB':list(map(str,ratB))}
assert len([1147,2513,2600,2692,17652,1236,5536,4031,3000,3200])==10
jeolla=list(map(F,['19.6','14.4','10.7','7.8','5.1','4','3','7.1','12.2']))
assert all(a>b for a,b in zip(jeolla[:7],jeolla[1:7])) and jeolla[6]<jeolla[7]<jeolla[8]
p['6']={'notDirect':3,'reason':'shareOfPassersDoesNotGiveExamFrequency','sourceMatches':{'1':'10years+1676:17652','2':['5.1','4.7','4','2.2'],'4':list(map(str,jeolla)),'5':[33,8]}}
confirmed=[4,4,9,8,2,5,2,3,2,3];changed=[2,5,4,1,4,3,4,2,8,0];execution=[0,0,0,1,0,3,0,2,0,0];mitigation=[2,5,2,0,4,0,0,0,6,0]
stock=[40]
for c,v in zip(confirmed[1:],changed[1:]):stock.append(stock[-1]+c-v)
assert stock==[40,39,44,51,49,51,49,50,44,47]
assert all(stock[i]>stock[i-1] for i in range(1,10) if execution[i]>0)
assert sum(mitigation[1:])==17<3*sum(execution[1:])==18
assert F(7,44)>F(5,39) and F(5,51)<F(4,40)
p['7']={'truth':[False,False,True,False,False],'stock':stock,'mitigation17vsExecution6':[17,6]}
national=list(map(F,['265.4','293.6','293.5','285.5','344.1']));local=list(map(F,['80.4','84.3','90.5','102','112.8']));total=[a+b for a,b in zip(national,local)];localShare=[a/b for a,b in zip(local,total)]
assert all(a<b for a,b in zip(total,total[1:])) and total[-1]==F('456.9')
assert national[-1]-national[-2]>national[-2]*F('.2')
growth=[F(b-a,a) for a,b in zip(local,local[1:])];assert max(range(4),key=lambda i:growth[i])==2 and all(s>=F('.2') for s in localShare)
assert localShare[-1]<localShare[-2] and max(range(5),key=lambda i:national[i]-local[i])==4
p['8']={'truth':[True,True,True,False,True],'totals':list(map(str,total)),'localShares':list(map(str,localShare)),'localGrowth':list(map(str,growth))}
incoming=[14717,11136,8920,14455,6958,15814];outgoing=[13677,11935,9663,15165,7068,14488];pureOff=[3869,18560-11935,9216,24088-15165,7663-7068,7482]
assert incoming[5]>incoming[3] and outgoing[5]<outgoing[3] and all(a>b for a,b in zip(outgoing,pureOff))
general={'A':(944,634),'C':(1036,1106),'D':(2383,2331),'E':(1463,1276),'F':(2897,2736),'H':(5455,5614),'K':(1690,1407),'L':(3235,3294),'N':(359,372),'O':(1366,1381),'Q':(1344,1298)}
assert min(general,key=lambda k:abs(general[k][0]-general[k][1]))=='N'
p['9']={'truth':[False,True,True],'pureOff':pureOff,'generalDifferences':{k:abs(a-b) for k,(a,b) in general.items()},'counterexample':'P/JinflowUpOutflowDown'}
mean=(149*F('79.4')+39*F('80.6'))/188
assert F(383,12413)<F('.05') and F(9096,11573)<F('.8') and F(522,2559)>F('.2') and F(9014,11573)>F('.7')
assert mean+F('.05')<80
p['10']={'truth':[True,True,False,True,True],'weightedMean':str(mean),'upperWithRounding':str(mean+F('.05')),'femaleBoundary':[522*5,2559]}
validate('data20',p,[('2025-03-08',i) for i in range(1,11)],figure_count=31)
