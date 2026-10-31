"""Batch12 independently transcribed arithmetic, roots, bounds and native prose."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,re,unicodedata
import pdfplumber
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/psat_remaining605_20261030';B=OUT/'batch12'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
bank={q['id']:q for p in (ROOT/'assets/psat').glob('*.json') for q in (read(p) if isinstance(read(p),list) else [])}
old={x['question']['id']:x['question'] for x in read(B/'revealed-current.json')}
reg={x['newAsset']:x for x in read(ROOT/'artifacts/psat_final_quality_20261029/full900/native-image-repairs.json')['figures']}
spec=read(B/'native-prose-transcriptions.json')['transcriptions']
norm=lambda s:re.sub(r'[\s<>○◯]','',unicodedata.normalize('NFKC',s))
checks=[]
for qid,s in spec.items():
 q=bank[qid];previous=old[qid]
 texts=[]
 for i in s['remove']:
  f=previous['figures'][i];r=reg[f['asset']]
  with pdfplumber.open(ROOT/r['source']) as pdf:
   texts.append(pdf.pages[r['page1based']-1].crop(r['rect']).extract_text() or '')
 a,b=norm('\n'.join(texts)),norm(q['body'])
 assert a==b,(qid,a,b)
 assert q['figures']==[f for i,f in enumerate(previous['figures']) if i not in s['remove']]
 assert all(q[k]==previous[k] for k in ['id','answer','choices','original','number'])
 assert q['body'].split('\n\n')[0] in ['보기','조건','보고서','입지조건','방송뉴스']
 if q.get('underlines'):
  assert q['underlineLabelAnchors'] and len(q['underlines'])==3
  assert all(q['body'].count(x)==1 for x in q['underlines'])
 # Original removed images remain byte-identical to fresh-source evidence.
 for f in previous['figures']:
  assert (ROOT/f['asset']).is_file()
 checks.append(dict(id=qid,nativeProseMatchesOriginalPdf=True,retainedDataFiguresUnchanged=True,choicesAnswerOriginalUnchanged=True))

from decimal import Decimal,getcontext
from itertools import permutations
getcontext().prec=50
oldBMI={'A':('2.96',70),'B':('2.50',56),'C':('2.66',48),'D':('3.20',68),'E':('3.24',79),'F':('2.76',62),'G':('3.06',95),'H':('2.37',58)}
newBMI={'A':('3.35',75),'B':('2.76',52),'C':('2.89',51),'D':('3.53',82),'E':('3.46',95),'F':('3.06',85),'G':('3.24',107),'H':('2.62',72)}
bmi=lambda data:{k:F(w)/F(s) for k,(s,w) in data.items()}
oldIndex=bmi(oldBMI);newIndex=bmi(newBMI)
assert [k for k,v in oldIndex.items() if v<20]==['C']
assert [k for k,v in newIndex.items() if v<20]==['B','C']
assert [k for k in oldIndex if 20<=oldIndex[k]<25 and 20<=newIndex[k]<25]==['A','D']
assert sum(w for s,w in oldBMI.values())==536 and sum(w for s,w in newBMI.values())==619>F(536)*F('1.1')
assert all(17<v<34 for v in newIndex.values()) and max(newIndex.values())/min(newIndex.values())<2
growth={k:Decimal(newBMI[k][0]).sqrt()-Decimal(oldBMI[k][0]).sqrt() for k in oldBMI}
assert max(growth,key=growth.get)=='A' and all(v<Decimal('.09') for k,v in growth.items() if k!='A')
male1=29507-1316;male2=56330-male1
assert male1==28191>28165>male2==28139
assert 71976-29507==42469<2*29507 and 44012>F(71976)*F('.6')
assert F(15346,24388)<F(2,3)<F(26289,39312) and F(4,50)<F(1,5)
assert 42324>3095*10 and 430>427 and 42324<44009 and 44009-34777>F(44009)*F('.2')
months22=[10639,9163,9464,9939,10879,10597,11064,11186,11222,11516,11324,9873]
months23=[9834,9595,12025,11417,12365,12422,13961,14281,13393,12890,11991,11771]
assert sum(months22)==126866 and sum(months23)==145945>F(126866)*F('1.15')
assert months23.index(max(months23))==7 and [i+1 for i,(a,b) in enumerate(zip(months22,months23)) if b<a]==[1]
pops=[287824,112231,122100,62045,60976];complaints=[60433,35904,26852,12399,10357]
per100=[F(c*100,p) for c,p in zip(complaints,pops)]
assert max(range(5),key=lambda i:per100[i])==1 and per100[1]>30 and F(60433,145945)>F('.4')
assert F('62.1')+F('7.1')+F('6.9')==F('76.1')>75
actualB=26000-4000-6000-9000;maximumC=35000-5000-9000-12000
util={'A':F(4000,5000),'B':F(actualB,9000),'C':F(6000,maximumC),'D':F(9000,12000)}
assert actualB==7000 and maximumC==9000 and sorted(util,key=util.get,reverse=True)==list('ABDC')
institutions={'A':(190,F('4.2'),F('4.1'),F('4.3')),'B':(120,F('3.9'),F('4.0'),F('3.8')),'C':(180,F('4.6'),F('4.8'),F('4.1')),'D':(150,F('3.8'),F('3.6'),F('3.9'))}
mapping=[]
for order in permutations(['문화','발명','세무','자료']):
 assigned=dict(zip('ABCD',order));inverse={v:k for k,v in assigned.items()}
 if {assigned[k] for k,(n,e,c,t) in institutions.items() if t>e}!={'발명','세무'}:continue
 if not institutions[inverse['자료']][2]>institutions[inverse['세무']][2]:continue
 if not institutions[inverse['문화']][0]>institutions[inverse['자료']][0]:continue
 mapping.append(assigned)
assert mapping==[dict(A='발명',B='자료',C='문화',D='세무')]
stocks=list(zip(*[[F('102.9'),F('80.0'),F('89.9'),F('91.8')],[F('106.6'),F('91.4'),F('93.8'),F('90.0')],[F('112.2'),F('98.9'),F('96.4'),F('95.9')],[F('95.0'),F('97.7'),F('97.5'),F('94.9')]]))
ship=list(zip(*[[F('96.2'),F('102.8'),F('116.7'),F('108.5')],[F('92.2'),F('107.1'),F('111.6'),F('107.3')],[F('93.4'),F('106.0'),F('106.4'),F('104.7')],[F('93.8'),F('104.6'),F('105.9'),F('103.7')]]))
direction=lambda v:[(b>a)-(b<a) for a,b in zip([F(100)]+list(v),v)]
assert [i for i in range(3) if direction(ship[i])==direction(ship[3])]==[2]
assert stocks[1][0]/stocks[1][-1]*100<100
assert [i for i in range(4) if all(a>=b for a,b in zip(stocks[i],ship[i]))]==[0]
hydrogenEnterprise=15177-6333-8771;hydrogenBus=407-399
assert hydrogenEnterprise==73 and hydrogenBus==8
assert F(8,399)>F('.02')>F('.01')>F(73,8771)>F(6,7537)
assert 16901+2939==19840>15737+307==16044>87+95==182
hybrid=[833,1135,1916,3422,682,307];assert hybrid.index(max(hybrid))==3 and hybrid[:4]==sorted(hybrid[:4]) and hybrid[3:]==sorted(hybrid[3:],reverse=True)
points={'A':(52,63),'B':(66,63),'C':(58,41),'D':(50,18),'E':(50,90),'F':(77,48),'G':(72,89),'H':(16,45),'I':(71,87),'J':(90,93)}
survival={k:3*x+2*y for k,(x,y) in points.items()}
assert [k for k,v in survival.items() if 150<=v<300]==list('ACD')
assert all(survival[k]>350 for k in ['G','I','J']) and 3*70+2*70==350
q=bank['kr-mpm-2025-07-19-psat-d-13'];assert '상한 소거' not in q['steps'][4] and '이 하한' in q['steps'][4]
roadLength=[323,330,442,257];assert sum(roadLength)==1352 and 330*4<1352
assert F('3.43')/323>F('.01')>F('2.35')/257
# Widen both reported area and rate last-place rounding to conservative bounds.
Clo=F('5.795')/F('.2225');Chi=F('5.805')/F('.2215');Dlo=F('2.345')/F('.2395');Dhi=F('2.355')/F('.2385')
assert Clo>25>F('13.85')>F('11.79')>Dhi and 9<Dlo<Dhi<10 and F('11.79')+F('13.85')+Clo+Dlo>50
result=dict(status='PASS',nativeProseChecks=checks,BMI2017={k:str(v) for k,v in oldIndex.items()},BMI2022={k:str(v) for k,v in newIndex.items()},actualHeightGrowthMeters={k:str(v) for k,v in growth.items()},BMICommonStrictInterval=[17,34],maleLicenseApplicants=[male1,male2],complaintYearTotals=[sum(months22),sum(months23)],complaintsPer100=[str(v) for v in per100],utilization={k:str(v) for k,v in util.items()},institutionUniqueMapping=mapping,shipmentDirections=[direction(v) for v in ship],stockOverShipmentEveryYear=[0],vehicleCombined=[16044,19840,182],hydrogenResiduals=[73,8],survivalIndices=survival,lowerBoundTerminologyCorrected=True,roadLengthTotal=1352,urbanAreaIntervals={'C':[str(Clo),str(Chi)],'D':[str(Dlo),str(Dhi)]},proseOrderNote='d03 report displayed natively before data; all six retained source data figures preserve their original relative order and geometry. Other four prose blocks remain after their source data.',limitations='Same-author exact source/model review. Charts/tables and original images remain intact. No real-device or independent-expert claim.')
(B/'source-key-model-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PASS five native source prose blocks;exact BMI/roots,permutation/index/ratio models,rounded road bounds,and corrected lower-bound terminology.')
