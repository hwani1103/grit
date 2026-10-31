"""Four prior295 impact reviews: scope, exact bounds, feasible counterexamples."""
from pathlib import Path
from itertools import product
from fractions import Fraction as F
import json,re,math
import pdfplumber
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/psat_remaining605_20261030'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2,default=str)+'\n',encoding='utf-8')
expected={'2023-07-22-s-16':1,'kr-mpm-2024-07-27-psat-d-04':5,'kr-mpm-2024-07-27-psat-d-18':4,'kr-mpm-2024-07-27-psat-d-22':1}
bank={q['id']:q for f in (ROOT/'assets/psat').glob('*.json') if isinstance(v:=read(f),list) for q in v}
ledger={q['id']:q for q in read(ROOT/'artifacts/psat_final_quality_20261029/full900/current900-evidence-ledger.json')['questions']}
digits=[v for v in product(range(1,5),repeat=4) if sum(v)==math.prod(v)]
assert len(digits)==12 and {tuple(sorted(v)) for v in digits}=={(1,1,2,4)}
boats={'A':(170,60,6),'B':(350,80,8),'C':(200,150,10),'D':(50,40,3)}
subsidies={k:r+3*y+30*n for k,(r,y,n) in boats.items()};assert subsidies==dict(A=530,B=830,C=950,D=260)
assert all(boats['D'][j]<boats[k][j] for k in ['A','B','C'] for j in range(3))
assert all(boats['B'][j]>boats['A'][j] for j in range(3)) and subsidies['C']-subsidies['B']==120
brands={'A':(14737,583999,26089),'B':(14593,603529,32543),'C':(10294,465042,25483),'D':(4082,414841,12557),'E':(787,559684,15448)}
top=sum(v[0] for v in brands.values());tail=[700]*7+[607];assert top==44493 and top+sum(tail)==50000 and max(tail)<787 and len(tail)+5==13
sales={k:n*s for k,(n,s,a) in brands.items()};areas={k:F(n*s,a) for k,(n,s,a) in brands.items()}
assert max(sales,key=sales.get)=='B' and min(areas,key=areas.get)=='E'
assert F(14593,14737)>F('.99') and F(603529,583999)>F('1.03') and F('.99')*F('1.03')>1
assert areas['E']<32000<48000<min(v for k,v in areas.items() if k!='E')
pop={'A':(14056,2790,1501),'B':(23556,3365,None),'C':(29204,3495,3615),'D':(21779,3889,2614),'E':(11224,2300,1272),'F':(16792,2043,2754),'G':(19163,2469,3421),'H':(27146,4045,4533),'I':(23813,2656,4123),'J':(29649,5733,3046),'K':(36326,7596,3625),'L':(15226,2798,1725)}
index={k:F(w,o) if w is not None else F('.88') for k,(n,o,w) in pop.items()}
caution=[k for k,x in index.items() if F('.5')<=x<1];normal=[k for k,x in index.items() if 1<=x<F('1.5')]
assert caution==['A','B','D','E','J','L'] and normal==['C','F','G','H']
assert max(index,key=index.get)=='I' and min(index,key=index.get)=='K'
assert 2656>F(23813,10) and sum(pop[k][0] for k in normal)==92305
assert F('.885')*3365<3421 # actual rounded0.88 B bound, not exact integer reconstruction
proof=dict(status='PASS',digitSolutions=digits,boatSubsidies=subsidies,brandCounterexample=dict(top5=top,remainingBrands=tail,totalBrands=13,strictlyBelowFifth=True),totalSales=sales,totalAreas=areas,localIndices=index,caution=caution,normal=normal,normalPopulation=92305,BwomanUpperBound=F('.885')*3365)
notes={
 '2023-07-22-s-16':'原문1~4중복선택4자리만허용. 1개수0/1의최소곱−합은양수이고허용수증가로뒤집히지않는다.1두개에서(x−1)(y−1)=3으로2·4;256경우검산의12순열모두합곱8. 원인R605003의전제범위문제없음.',
 'kr-mpm-2024-07-27-psat-d-04':'잔존+3수익+30선원의양수가중합. D는모든나머지에3항목모두열세, A는B에열세라D최소와B/C최대후보축소가유효하다.C−B120이고정확한530/830/950/260검산도일치한다.',
 'kr-mpm-2024-07-27-psat-d-18':'최소14주장은나머지5507을700*7+607로분배한엄격5위미만의총13브랜드모형으로반박한다. B매출우위0.99*1.03>1와E총면적상한32000<타시설하한48000은양의분모/실제각행에서성립한다.면적당매출의원문정의로가중비율을검증했다.',
 'kr-mpm-2024-07-27-psat-d-22':'공식등급의0.5/1.0/1.5포함경계와E/I/K빈칸을확인했다.주의6곳,정상92305명,I최고/K최저모두성립한다.B지수0.88을정확한여성인구값으로역산하지않고반올림상한0.885에서도3421미만임을확인했다.'}
reviews=[]
for id,answer in expected.items():
 q=bank[id];e=ledger[id]
 with pdfplumber.open(ROOT/e['officialKey']) as pdf:
  pi,t=next((i+1,p.extract_text()) for i,p in enumerate(pdf.pages) if '영역 '+q['subject'] in (p.extract_text() or ''))
 answers={}
 for line in t.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
   z=list(map(int,line.split()));answers.update(zip(z[::2],z[1::2]))
 assert answers[q['number']]==q['answer']==answer
 reviews.append(dict(id=id,revision=q['revision'],status='source_key_scope_bounds_and_counterexample_rechecked_no_change',source=e['officialSource'],key=e['officialKey'],keyPage=pi,answer=answer,evaluation=notes[id],sourceImage='batch06/related-'+id+'-source.png',oldHistoricalScoreUntouched=True))
write(OUT/'batch06/related295-extrema-group01.json',dict(proof=proof,reviews=reviews,limitations='Same-author scope impact checks, not new independent ratings or real-device rendering.'))
queue=read(OUT/'cross-candidates-structure-and-extrema.json')
for x in queue:
 if x['id'] in expected:x.update(status='source_key_scope_bounds_rechecked_no_change',evidence='batch06/related295-extrema-group01.json')
 elif x['id']=='2023-07-22-s-12':x.update(status='source_key_semantics_and_host_reverified_in_batch02',evidence='batch02/source-key-model-checks.json')
write(OUT/'cross-candidates-structure-and-extrema.json',queue)
cross=read(OUT/'cross-validation.json');cross['relatedPrior295Reviews']+=reviews;write(OUT/'cross-validation.json',cross)
print('PASS4prior295scope/feasiblecounterexample/rounding reviews and directofficialkeys; no content change or historical rerating.')
