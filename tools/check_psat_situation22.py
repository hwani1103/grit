from pathlib import Path
from fractions import Fraction as F
from datetime import date
from itertools import product
import json
from psat_batch_tools import validate
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/situation22'
bank=json.loads((A/'authored-situation22.json').read_text(encoding='utf-8'));own=json.loads((A/'own-solve-before-key.json').read_text(encoding='utf-8'))
nums=list(range(22,32));answers=[5,1,1,5,2,1,4,4,1,4]
assert [q['answer'] for q in bank]==[own[str(n)]['answer'] for n in nums]==answers
p={str(n):{'directSolve':own[str(n)]['proof'],'answer':own[str(n)]['answer']} for n in nums}
def match(n,truth,answer):
 q=next(q for q in bank if q['number']==n)
 assert [i+1 for i,c in enumerate(q['choices']) if [k in c for k in 'ㄱㄴㄷㄹ'[:len(truth)]]==truth]==[answer]
 assert own[str(n)]['truth']==truth;p[str(n)]['truth']=truth
# 22: limited list, direction and exception precede color default.
def permitted(doc,direction=None):
 return (doc=='official' and direction=='toForeign') or doc in ['grade1Appointment','medal','medalCertificate','presidentAward','civilID','publicUniversityDegree','overseasMission','governmentVessel','governmentAircraft','currency']
assert not permitted('primeMinisterAward') and not permitted('official','fromForeign') and permitted('official','toForeign')
color=lambda iron:'none' if iron else 'goldPetals'
assert color(True)=='none'
p['22']['ruleApplications']={'primeMinisterAward':'outside list despite recipient grade','ironColor':color(True),'WHOtoKorea':False,'foreignEmbassyLabelLanguage':'Korean','KoreatoUKEmbassy':['permitted','topCenter']}
# 23: additional digital deposit requires the primary obligation first.
def subject(online,number):return not online or number
def digital(public,online,number):return public and subject(online,number)
assert subject(True,True) and not digital(True,True,False)
collection=lambda domestic,value:domestic and value
assert collection(True,True)
p['23']['models']={'numberedOnlineDeposit':True,'publicUnnumberedOnlineDigital':False,'saleCompensationStateException':False,'unchangedReprintNewDeadline':'not implied by supplied rule','unnumberedHighValueDomesticCollection':True}
# 24: independent exemptions combined by OR; reference date, not future use end.
cutoff=date(2024,12,1)
def exemption(publicFreeStart=None,temporaryBuilt=None,emergencyVessel=False,demolition=None):
 return (publicFreeStart is not None and publicFreeStart.replace(year=publicFreeStart.year+1)<=cutoff) or (temporaryBuilt is not None and temporaryBuilt<=cutoff<temporaryBuilt.replace(year=temporaryBuilt.year+1)) or emergencyVessel or (demolition is not None and demolition<=cutoff)
truth=[not exemption(demolition=date(2025,1,1)),not exemption(publicFreeStart=date(2023,1,1)),not exemption(temporaryBuilt=date(2024,4,19)),not exemption(publicFreeStart=date(2024,3,1),emergencyVessel=True)]
match(24,truth,1)
assert not exemption(temporaryBuilt=date(2023,12,1)) and exemption(demolition=cutoff)
p['24']['boundary']={'exactOneYearTemporary':False,'demolitionAtCutoff':True,'ZIndependentEmergencyExemption':True}
# 25: values in ten-thousand KRW, thresholds inclusive.
def applicable(building,registered,region,deposit,monthly=0,annual=None):
 limit={'A':90000,'B':68000,'C':55000}.get(region,40000)
 rent=F(annual,12) if annual is not None else monthly
 return building and registered and deposit+100*rent<=limit
cases=[(False,True,'A',80000,0,None),(True,False,'B',50000,100,None),(True,True,'B',70000,0,None),(True,True,'C',40000,200,None),(True,True,'D',30000,0,1200)]
assert [applicable(*c) for c in cases]==[False,False,False,False,True]
assert applicable(True,True,'D',40000) and not applicable(True,True,'D',40001)
p['25']['conversions']={'C':60000,'D':40000,'DLimit':40000,'exactLimitIncluded':True}
# 26: source-backed attributes; folklore claim is not converted into efficacy proof.
p['26']['evidence']={'blackTemperature':[600,700],'whiteTemperature':[800,1300],'sameWeightAdsorptionWinner':'black','fuelDescribed':'white','folkloreNonFuel':'geumjul','completeCombustionPrevented':True}
# 27: both an ounce ledger and ml conversion yield the same two requested units.
gallon=128;pint=16;cup=8;quart=gallon/4
give=gallon-5*pint;leftA=40;usedA=5*pint-leftA;leftB=give-quart
ga=usedA/cup;na=leftB/cup*48/3
assert (ga,na)==(5,32) and leftA+leftB+usedA+quart==gallon
mlPerCup=48*5;mlPerOunce=F(mlPerCup,8)
assert usedA*mlPerOunce/mlPerCup==ga and leftB*mlPerOunce/(3*5)==na
p['27']['ozLedger']={'original':128,'Aretained':80,'givenB':48,'Aconsumed':40,'Bconsumed':32,'Afinal':40,'Bfinal':16,'answers':[5,32]}
# 28: simulate every candidate flood day, counting morning collection before night loss.
solutions=[];ending={}
for n in range(1,276):
 stock=F(0);low=F(0)
 for day in range(1,366):
  if day<=275:stock+=10
  stock-=6
  if day==n:stock*=F(1,3)
  low=min(low,stock)
 if stock==0 and low>=0:solutions.append(n)
 if n in [180,190,200,210,220]:ending[str(n)]=str(stock)
assert solutions==[210]
assert 275*4-90*6==560 and F(560)*F(3,2)/4==210
p['28']['dailySimulation']={'all275Nights':True,'uniqueSolution':solutions,'candidateFinalStocks':ending}
# 29: all positive days up to the solution, not only the offered options.
forest=142857*7;digits=set(str(forest));assert forest==999999 and digits=={'9'}
solutions=[d for d in range(1,28) if set(str(37*d))<=digits]
assert solutions==[27] and 9%37 and 99%37 and 999%37==0
p['29']['proof']={'forest':forest,'candidateTotals':{str(d):37*d for d in [17,23,25,27,37]},'positiveDays1to27Valid':solutions,'smallerPermittedTotals':[9,99]}
# 30: enumerate all joint sex/skill tables at feasible totals, applying each specified move.
ratios={'A':(1,1,2,1),'B':(2,1,1,1),'C':(1,2,1,2)}
changes={'A':(-1,1,0,0),'B':(0,-1,0,1),'C':(1,0,0,-1)}
valid={}
for team,(m,f,s,u) in ratios.items():
 tables=[]
 for N in range(1,61):
  if N*m%(m+f) or N*s%(s+u):continue
  male=N*m//(m+f);skilled=N*s//(s+u)
  for ms in range(max(0,male+skilled-N),min(male,skilled)+1):
   before=(ms,male-ms,skilled-ms,N-male-skilled+ms)
   after=tuple(a+b for a,b in zip(before,changes[team]))
   if min(after)>=0 and after[0]+after[1]==after[2]+after[3] and after[0]+after[2]==after[1]+after[3]:tables.append((N,before,after))
 assert {t[0] for t in tables}=={6};valid[team]=tables
example={'A':(2,1,2,1),'B':(2,2,1,1),'C':(1,1,1,3)}
assert all(any(t[1]==example[k] for t in v) for k,v in valid.items())
# Analytic totals: difference after = initial ratio unit -2=0, so unit2 and total6; range above is a cross-table check only.
p['30']['jointTables']=valid;p['30']['unboundedArgument']='each decisive 2:1 difference k becomes k-2; equal iff k=2; total3k=6 each'
# 31: all chronological daily pair sequences, with stock limits.
possible={2:set(),1:set(),4:set()};examples={}
for seq in product([0,1,2],repeat=8): # A consumed per day; AB corresponds to1
 a=sum(seq);b=16-a
 if a>10 or b>10:continue
 remainA=10-a;remainB=10-b;y=seq.count(1)
 if remainA in possible and remainB==4-remainA:
  possible[remainA].add(y);examples.setdefault((remainA,y),seq)
assert possible=={2:{0,2,4,6,8},1:{1,3,5,7},4:{0,2,4,6}}
assert sum([2,0,1,1,1,1,1,1])==8
truth=[possible[2]=={8},min(possible[1])>=1,5 not in possible[4]];match(31,truth,4)
p['31']['possibleCorrectDays']={str(k):sorted(v) for k,v in possible.items()};p['31']['counterexampleAperDay']=[2,0,1,1,1,1,1,1]
q=bank[-1];assert [i+1 for i,c in enumerate(q['choices']) if 'ㄴ' in c and 'ㄷ' in c]==[4,5]
validate('situation22',p,[('2025-03-08',n) for n in nums],figure_count=1)
