from pathlib import Path
from itertools import product,combinations
from fractions import Fraction as F
import json,re,hashlib
import pdfplumber
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/situation05';P=R/'assets/psat/situation05.json'
bank=json.loads((P if P.exists() else A/'authored-situation05.json').read_text(encoding='utf-8'));norm=lambda s:re.sub(r'\s+','',s)
with pdfplumber.open(R/'artifacts/psat600_20261028/sources/4341/BBSMSTR_000000000138_4341_2.pdf') as pdf:
 t=pdf.pages[2].extract_text();assert '2023년도' in t and '상황판단' in t and '인' in t
 key={}
 for line in t.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
   v=list(map(int,line.split()));key.update(zip(v[::2],v[1::2]))
 assert len(key)==25
proof={}
costs={'A':2000+1000*20,'C':min(3000+1750*20,20000),'D':5000+700*20,'E':F(4,5)*(5000+1000*16)}
assert costs=={'A':22000,'C':20000,'D':19000,'E':16800}
proof['7']={'availableCosts':{k:int(v) for k,v in costs.items()},'B':'ineligible mid-size vehicle','EpaidHours':9,'Eextra30minutes':16}
endMax=[18,F(39,2),19,19];winnerMin=20
assert all(x<winnerMin for x in endMax)
# Counterexample to unlicensed strongest->Parfum inference.
strength={'甲':3,'乙':19,'丙':18,'丁':10,'戊':16}
assert strength['乙']==max(strength.values()) and 15<strength['乙']<20
proof['10']={'otherLatest':['18:00','19:30','19:00','19:00'],'winnerEarliest':'20:00','strongestCanBeEDP':strength,'reason':'any allowed fragrance <=10h; no unique grade inference'}
# Four distinct destination floors have odd positive counts.
# At most3 other buttons can have positive even counts because total spare6.
press=[]
for a,b,c,d in product(range(1,8,2),repeat=4):
 for e,f,g in product(range(0,7,2),repeat=3):
  ns=(a,b,c,d,e,f,g)
  if sum(ns)==10:press.append(ns)
assert press
five=[ns for ns in press if 5 in ns]
assert five and all(any(v>=2 for j,v in enumerate(ns) if j!=ns.index(5)) for ns in five)
assert (1,3,3,3,0,0,0) in press
assert (3,3,1,1,2,0,0) in press
proof['22']={'canonicalCountAssignments':len(press),'withFive':len(five),'statement2Always':True,'statement1Counterexample':'one passenger performs all10presses','statement3Counterexample':[1,3,3,3],'statement4Counterexample':[3,3,1,1,2],'extraEvenButtons':'at most3 distinct unused buttons; total surplus6'}
# Enumerate all outbound sets with prescribed outdegrees.
models=[]
for aset,bset,dset in product(combinations('BCDE',3),combinations('ACDE',2),combinations('ABCE',2)):
 out={'A':set(aset),'B':set(bset),'C':{'A'},'D':set(dset),'E':{'B'}}
 incoming=lambda person:{x for x in out if person in out[x]}
 if len(incoming('A'))!=3 or len(out['A']&incoming('A'))!=2:continue
 if incoming('B')!=set('ACDE')-out['B']:continue
 if 'C' not in out['A']:continue
 models.append(out)
assert len(models)==1
expected={'A':{'C','D','E'},'B':{'A','C'},'C':{'A'},'D':{'A','B'},'E':{'B'}}
assert models[0]==expected
assert {x for x in expected if 'D' in expected[x]}=={'A'}
proof['23']={'enumeratedOutboundAssignments':4*6*6,'solutions':1,'outgoing':{k:sorted(v) for k,v in expected.items()}}
t=F(360,1)/(6-F(1,2));assert t==F(720,11) and 65<t<70
assert (t*6-t*F(1,2))%360==0
proof['24']={'relativeDegreesPerMinute':'11/2','firstPositiveMinutes':'720/11','secondsAfter1h5m':str((t-65)*60),'interval':[65,70]}
assert 22<F(22)+F(18,12)
proof['25']={'schoolMilitaryAgeLimitYears':'47/2 exclusive','age22Qualifies':True,'additionalBenefit':'30<=34 and5<=5;budgetcondition remains','overlapException':'childrearing may be paid'}
proof['1']={'leap':'included','leapsecondDecision':'internationalagency','minister':'announce','calendar':'followingyear'}
proof['3']={'donationWithName':'prohibited','chiefRemoval':'violation+stationrequest ->must','penaltyScope':'electioncampaign only in givenarticle'}
proof['5']={'rawTofu':'soybeans->groundboiledpulp->soymilk->coagulatedmass->pressedtofu','coagulant':'MgCl2 inbrine','summer':'halfday','winter':'fullday'}
proof['9']={'EDPmin15greaterEDCmax5':15>5,'mostused':'EDT','strongestcategory':'Parfum'}
for q in bank:
 n=q['number'];raw=(A/f'2023-s{n}-source.txt').read_text(encoding='utf-8').split(f'{n}.',1)[1]
 prompt,tail=raw.split('?',1);body,opts=tail.rsplit('\n① ',1)
 if n in [9,10]:body=(A/'shared9-10-source.txt').read_text(encoding='utf-8')+'\n'+body
 if n==7:
  body=body.split('\n기본요금 추가요금',1)[0]
  assert q['tables']==[{'caption':'주차장별 요금','columns':['구분','기본요금 (최초 1시간)','추가요금 (이후 30분마다)','비고'],'rows':[['A주차장','2,000원','1,000원','－'],['B주차장','3,000원','1,500원','경차 전용 주차장 / 저공해차량 30% 할인'],['C주차장','3,000원','1,750원','경차 50% 할인 / 일 주차권 20,000원 (당일 00:00～24:00 이용 가능)'],['D주차장','5,000원','700원','－'],['E주차장','5,000원','1,000원','경차, 저공해차량(1, 2종) 50% 할인 / 저공해차량(3종) 20% 할인 / 18:00～익일 07:00 무료']],'afterParagraph':4}]
 assert norm(q['prompt'])==norm(prompt+'?'),(n,'prompt')
 assert norm(q['body'])==norm(body),(n,'body')
 choices=re.split('[①②③④⑤]','① '+opts)[1:];assert len(choices)==5
 assert all(norm(a)==norm(b) for a,b in zip(choices,q['choices'])),(n,'choices')
 assert q['answer']==key[n],(n,'key',q['answer'],key[n])
 assert len(q['steps'])==len(q['optionReasons'])==5
 for s,prefix in zip(q['steps'],['착안점: ','실전 풀이: ','답 확정 기준: ','정석 근거: ','적용 한계: ']):assert s.startswith(prefix) and len(s)>40,(n,prefix)
 assert not any(c in json.dumps(q,ensure_ascii=False) for c in ['\u2060','\ufffd'])
 assert (R/q['original'] if P.exists() else A/'staged'/q['original']).exists()
seen=set();oldcount=0
for p in (R/'assets/psat').glob('*.json'):
 if p.name in ['sets.json','situation05.json']:continue
 obj=json.loads(p.read_text(encoding='utf-8'))
 if isinstance(obj,list):
  for q in obj:
   k=(q.get('examDate',q['source'][:10].replace('.','-')),q['subject'],q['number'])
   assert k not in seen,k;seen.add(k);oldcount+=1
for q in bank:
 k=(q['examDate'],q['subject'],q['number']);assert k not in seen,k;seen.add(k)
for path,digest in json.loads((A/'before-situation05-hashes.json').read_text(encoding='utf-8')).items():
 if path=='assets/psat/sets.json':continue
 assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
proof.update(status='PASS',count=10,officialFinalKeys=10,normalizedSource='complete passages and5choices',tables=1,preservedExisting=oldcount,limitations='Same-author source review and enumeration; not independent expert certification.')
(A/'content-checks.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(A/'prepublication-correction.txt').write_text('2026-10-29:10번의 가장 강한 향수=Parfum 단정을 게시 전 삭제. 乙19%,丙18%,戊16%인 EDP 반례가 가능. 모든 향수 최대10시간 상한만으로19:30<戊최소20:00 입증. 정답⑤유지.\n',encoding='utf-8')
print('PASS:10keys/source;parking costs;perfume bound+counterexample;button',len(press),'assignments;contacts144->1;exactclock;existing',oldcount)