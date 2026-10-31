from fractions import Fraction as F
from psat_batch_tools import validate
proof={
'11':{'chain':'richSoil -> lowerNeedFungi -> lowerSignal;hostSorghum example','answer':5},
'12':{'missingLink':'ability probability stable;rare good luck not carried over','answer':5},
'21':{'months':12,'initialCounts':[6,6],'allowedChange':[1,-1],'answer':4},
'22':{'rule':'allNameChanges require permission;familyName has extra restrictions','answer':5},
'23':{'domesticSteps':['cooperation','agreedPlan','trial','commercial'],'2030':[3,5,6,10,10],'answer':4},
'24':{'operator':'community','financing':'production supported by state','aim':'welfare for vulnerable','answer':1},
'36':{'truth':[False,True,False],'gCounterexample':{'initial':3,'recurred':2},'dCountermodel':{'Dfirst':3,'Efirst':2,'Erecurrence':3,'eachMaternal':1},'answer':2},
'37':{'stimuli':{'sugar':['taste','nutrition'],'arabinose':['taste']},'normalArabinoseMinutes':3,'blockedArabinose':False,'blockedSugarLong':True,'unmeasured':'nutritionShort','answer':2},
'38':{'truth':[True,False,False],'equilibrium':'q=mg/E with m fixed','noSingleElectronCounterexample':[2,3,4],'answer':1},
'2025-1':{'rule':'attendance300','practice':'nonGraduate유학 allowed examination','answer':4}}
assert all(6+k>=6-k for k in [0,1])
assert 5<6 and 5<10
assert F(2)*1==2 and [F(2)/E for E in [F(1),F(2),F(3)]]==[2,1,F(2,3)]
validate('verbal19',proof,[('2026-03-07',n) for n in [11,12,21,22,23,24,36,37,38]]+[('2025-03-08',1)],figure_count=2)
