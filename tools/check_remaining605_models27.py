from fractions import Fraction as F
import review_remaining605 as r
b=r.folder(27);checks={}
returns=[F(70,3500),F(150,4500),F(220,5500)]
truth=[returns.index(max(returns))==1,F(70,440)<=F(15,100),1-F(660,13500)<=F(95,100),F(740,13500)>=F(5,100),F(440,13500)-F(440,16500)>=F(1,100)]
assert truth==[False,False,False,True,False]
assert 100*(F(440,13500)-F(440,16500))==F(16,27)
checks['2025d23']=dict(truth=truth,percentPointIncrease=str(F(16,27)))
age=[69+24,507+399,314+409,239+266,80+139];rent=[99,913,385,215,54]
assert sum(age)==2446 and sum(max(a,b) for a,b in zip(age,rent))==2459
assert 2446+max(0,rent[0]-age[0])==2452
assert F(1033,2318)>F(1045,2453) and F(654*150,855)>=100
assert F(654*150-201*100,855)<100
checks['2025d25']=dict(femaleShareHigher=True,meanLowerBoundUnderNonnegativeIncome=str(F(654*150,855)),fullUnionLowerBound=2459,sufficientOneBinLowerBound=2452,negativeIncomeCounterexample=str(F(654*150-201*100,855)),existingPublishedLimitation='Already explicitly states usual nonnegative income assumption; original not changed to force key.')
logs=[(2,'Thu','HR','lead','pain',1),(2,'Thu','finance','staff','digest',1),(3,'Fri','HR','deputy','digest',2),(6,'Mon','PR','lead','pain',1),(6,'Mon','HR','deputy','digest',2),(10,'Fri','finance','lead','hangover',2),(13,'Mon','finance','staff','pain',1),(13,'Mon','PR','staff','digest',1),(16,'Thu','HR','deputy','hangover',1),(17,'Fri','HR','deputy','pain',1),(20,'Mon','finance','lead','pain',2),(21,'Tue','HR','staff','pain',1),(24,'Fri','HR','deputy','hangover',1),(27,'Mon','PR','staff','digest',1),(27,'Mon','HR','lead','pain',2),(30,'Thu','finance','deputy','pain',1)]
assert not any(x[3]=='lead' and x[4]=='digest' for x in logs)
assert [x[0] for x in logs if x[4]=='hangover']==[10,16,24]
assert all(x[5]==1 for x in logs if x[3]=='staff')
assert {x[0] for x in logs if x[1]=='Mon' and x[4]=='pain'}=={6,13,20,27}
assert all(x[1]=='Mon' for x in logs if x[2]=='PR')
checks['2026d01']=dict(rows=logs,truth=[True,False,True,True,True])
fruit={'A':(9992,23254,10430,22875),'B':(997,8364,1001,8132),'C':(1210,8091,1214,8001),'D':(1523,12616,1424,12356),'E':(5203,15234,5168,15281)}
fruitChecks={k:[c+d>=10000,d<bb,2*d>=5*c] for k,(a,bb,c,d) in fruit.items()};assert [k for k,v in fruitChecks.items() if all(v)]==['D'];checks['2026d02']=fruitChecks
stops=[81,126,128,146,160];short=[20,52,50,83,105];totals=[a+b for a,b in zip(stops,short)];assert totals==[101,178,178,229,265]
assert F(short[1],totals[1])>F(short[2],totals[2]);assert all(a<3*b for a,b in zip(stops[1:],short[1:]));checks['2026d06']=dict(stops=stops,shortages=short,totals=totals,truth=[False,False,False,False,True])
use=[[85,175],[77,194],[35,116],[39,215]];assert [sum(v) for v in use]==[260,271,151,254]
assert max([148,111,222,74])==222 and max([282,305,172,281])==305
assert min([310,245,286])==245 and max([155,200,572])==572
assert 41+134==175 and 22+66==88;checks['2026d07']=dict(baseRatesTenths=[260,271,151,254],additional=['ㄱ','ㄷ','ㄹ'],irrelevant='ㄴ childcare mode is not work form or support use')
planned=[245,231,235,247,223];entered=[227,223,224,236,216];rates=[927,965,953,955,969]
growth=[F(entered[i]-entered[i-1],entered[i-1]) for i in range(1,5)]
assert planned.index(max(planned))==entered.index(max(entered))==3
assert F(11,227)<F(1,10) and F(38,927)<4*F(14,955)
assert growth.index(max(growth))+1==3 and rates.index(max(rates))==4
assert F(38,927)<F(5,100) and F(14,955)>F(14,1000)
checks['2026d08']=dict(planned=planned,entered=entered,ratesTenths=rates,growth=list(map(str,growth)),truth=[True,True,False,False],publishedLooseBoundsValid=True)
assert 849-528==321 and 876-581==295 and 800-757==43 and 76-71==5
assert 121744>77463>75794 and 121744+75794+77463==275001
assert round(float((F(275,181)-1)*100),1)==51.9
checks['2026d09']=dict(used=[1,2,3,4],unused=5,childCountParticipationNotExpenditure=True,gapTenths=[295,321],allReportStatementsCompared=True)
names=['항공','교량','교통','댐','식수','에너지','유해폐기물','내륙수로','제방','공원','항만','철도','도로','학교','고형오물','오수','폭우','통신']
a=list('BCBAAC')+list('EEDCCC')+list('BBCBBB');c=list('BCCAAC')+list('DDCDEA')+list('BADABB');d=list('ADCABB')+list('DCCDBA')+list('BADABB')
same=[n for n,x,y in zip(names,a,d) if x==y];improve1=[n for n,x,y in zip(names,a,c) if y<x];improve2=[n for n,x,y in zip(names,c,d) if y<x]
assert a.count('B')==7 and same==['댐','도로','폭우','통신'];assert len(improve1)==6 and len(improve2)==4
checks['2026d11']=dict(names=names,grades2015=a,grades2020=c,grades2025=d,same2015and2025=same,improvement2015to2020=improve1,improvement2020to2025=improve2)
assert F(44097,44551)>=F(95,100)
assert F(2154,48406)>F(152,5408)
assert F(44097,5104)<F(48406,5408) and F(46252,238)<F(48406,242)
assert 44097<F(88,10)*5104 and 48406>F(88,10)*5408
assert 46252<238*200 and 48406>242*200
checks['2026d12']=dict(truth=[True,False,True,False],personSeparator='8.8',universitySeparator=200)
r.write(b/'calculation-checks.json',dict(status='PASS',checks=checks,limitations='Exact rational/model checks on manually transcribed original data; same-author review.'))
print('PASS10 exact models, original grade matrix and pre-reveal nonnegative-income caveat matched existing limitation.')
