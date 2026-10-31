import itertools as it
from datetime import date
from fractions import Fraction as F
from psat_batch_tools import validate,read,ROOT
proof={'2':{'answer':2,'exception':'privateRoomBan exemptPrison;recordingBan persists'},'3':{'answer':2,'roman':'BROWN KOKO KATHERINE','spaces':2,'Korean':'화이트존'},'4':{'answer':5,'expiryAbsolute':'2025-01-02','discovery':'2025-02-15'}}
assert date(2025,2,15)>date(2022+3,1,2)
assert date(2024,4,12)<date(2023+1,11-6,23)
assert date(2006+18,7,15)<date(2024,12,14)
assert date(2024,10,11)<date(2024,12,10)
proof['5']={'truth':[False,True,True,True],'withdrawalEnd':'2024-05-23 after announcement','age18':'2024-07-15 before secondExam','disability':'registered+impossibleToContinue exemptsSixMonths'}
proof['6']={'truth':[False,True,False,False],'sequence':['수궤','장'],'purpose':'minimizeDeformation','headCabinet':'innerRoomAndMensRoom'}
volumes=[30*7,30*5,F(60)*F('2.5'),40*9,20];assert volumes==[210,150,150,360,20] and sum(100<=v<200 for v in volumes)==2
proof['7']={'volumes':list(map(str,volumes)),'medium':2}
assert 1000-760==240 and (1+40//10)*760==3800
proof['8']={'difference':240,'pressure':3800,'baseIncluded':760}
assert 75-24==21+30 and 75-50==50-25
proof['9']={'marriageAge':24,'sonBornAge':25,'deathDayAge':50,'ownDeathAge':60}
solutions=[]
for a in range(1,25):
 c=5*a
 for d in range(1,25):
  if abs(3*c-2*d)!=3:continue
  for b in range(1,25):
   e=24-a-b-c-d
   if 0<b<e and b*e%2 and len({a,b,c,d,e})==5:solutions.append([a,b,c,d,e])
assert solutions==[[1,3,5,6,9]]
proof['10']={'uniqueDailyCounts':solutions[0],'difference':8}
def catch(n):return [(a,b,n-a-b,30*a+20*b+10*(n-a-b)) for a in range(n+1) for b in range(n-a+1)]
worlds=[(a,b,c) for a,b,c in it.product(catch(3),catch(4),catch(5)) if a[3]>b[3]>c[3]]
assert worlds and all(a[0]>=1 and c[2]>=1 for a,b,c in worlds)
assert ((3,0,0,90),(2,0,2,80),(0,0,5,50)) in worlds
assert any(b[3]==80 and b[1]==0 for a,b,c in worlds)
proof['11']={'truth':[True,False,False],'validCatchWorldCount':len(worlds),'counterexample':[[3,0,0,90],[2,0,2,80],[0,0,5,50]],'strictScoreBounds':[50,60,70]}
bank=read(ROOT/'artifacts/psat600_20261028/situation20/authored-situation20.json')
assert bank[-1]['tables'][0]['rows']==[['A','30'],['B','20'],['C','10']]
assert '「외래어 표기법」' in bank[1]['body'] and '「장애인복지법」' in bank[3]['body']
validate('situation20',proof,[('2025-03-08',i) for i in range(2,12)])
