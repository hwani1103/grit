"""Official sources and exact independent models for batch11."""
from pathlib import Path
from itertools import product,permutations
from fractions import Fraction as F
import json,re
import pdfplumber
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/psat_remaining605_20261030/batch11'
read=lambda f:json.loads(f.read_text(encoding='utf-8-sig'))
norm=lambda s:re.sub(r'[\s①②③④⑤ㆍ·「」『』\uf000\uf001/]','',s)
tables={
 'kr-mpm-2025-07-19-psat-s-07':dict(columns=['정답','A','B','C','D','E'],rows=[['문항 개수','2','0','3','5','5']],after=3,native='정답 A B C D E 문항 개수 2 0 3 5 5'),
 'kr-mpm-2025-07-19-psat-s-08':dict(columns=['장소','세미나 당일 타 부서 예약 현황','프로젝터 사용 가능 여부','최대 수용 가능 인원','다과 제공 가능 여부'],rows=[['A','13:00～15:00','○','65명','○'],['B','없음','○','40명','○'],['C','11:00～12:30','○','50명','×'],['D','없음','×','80명','×'],['E','없음','○','45명','○']],after=4,native='세미나 당일 프로젝터 사용 최대 수용 다과 제공 장소 타 부서 예약 현황 가능 여부 가능 인원 가능 여부 A 13:00～15:00 ○ 65명 ○ B 없음 ○ 40명 ○ C 11:00～12:30 ○ 50명 × D 없음 × 80명 × E 없음 ○ 45명 ○'),
 'kr-mpm-2025-07-19-psat-s-15':dict(columns=['지역','A','B','C','D','E'],rows=[['건강생활실천율(%)','35','30','25','30','30']],after=0,native='지역 A B C D E 건강생활실천율(%) 35 30 25 30 30')}
rows=read(OUT/'revealed-current.json');sources={x['id']:x for x in read(OUT/'blind-source.json')};solves={x['id']:x for x in read(OUT/'own-solves.json')};checks=[]
for row in rows:
 q=row['question'];m=sources[q['id']];native=m['sourceText']
 native=norm(re.sub(r'^.*?\b'+str(q['number'])+r'[.]\s*','',native,count=1,flags=re.S))
 if q['id'] in tables:
  t=tables[q['id']];actual=q['tables'][0]
  assert actual['columns']==t['columns'] and actual['rows']==t['rows'] and actual['afterParagraph']==t['after']
  assert native.count(norm(t['native']))==1,(q['id'],'table text');native=native.replace(norm(t['native']),'',1)
 if q['id']=='kr-mpm-2025-07-19-psat-s-07':
  heading=norm('16번 17번 18번 19번 20번');assert native.count(heading)==1;native=native.replace(heading,'',1)
 a,b=native,norm(q['prompt']+q['body']+''.join(q['choices']))
 if a!=b:
  i=next((i for i,(x,y) in enumerate(zip(a,b)) if x!=y),min(len(a),len(b)))
  raise AssertionError((q['id'],i,a[max(0,i-20):i+100],b[max(0,i-20):i+100]))
 with pdfplumber.open(ROOT/row['officialKey']) as pdf:
  pi,t=next((i+1,p.extract_text()) for i,p in enumerate(pdf.pages) if '영역 상황판단' in (p.extract_text() or ''))
 assert q['examDate'][:4] in t and f"책형 {q['book']}" in t
 answers={}
 for line in t.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
   z=list(map(int,line.split()));answers.update(zip(z[::2],z[1::2]))
 assert answers[q['number']]==q['answer']==solves[q['id']]['answer']
 checks.append(dict(id=q['id'],source=m['source'],page=m['page'],nativeTextAndFiveChoicesMatch=True,tableChecked=q['id'] in tables,key=row['officialKey'],keyPage=pi,answer=q['answer']))
clock=F(360)/F('5.5');assert 65<clock<70 and F('5.5')*clock==360
assert [x for x in range(100) if 1000*(2*x+2)+3000==15000]==[5]
letters='ABCDE';initial=dict(zip(letters,[2,0,3,5,5]));opts=['ABBCB','BABBC','BABDD','CBBBD','DBECA']
valid=[];frequencies=[]
for s in opts:
 counts={k:initial[k]+s.count(k) for k in letters};frequencies.append(counts)
 valid.append(all(2<=x<=6 for x in counts.values()) and not any(len(set(('AA'+s)[i:i+3]))==1 for i in range(5)))
assert valid==[False,True,False,False,False]
rooms={'A':(780,900,True,65,True),'B':(None,None,True,40,True),'C':(660,750,True,50,False),'D':(None,None,False,80,False),'E':(None,None,True,45,True)}
eligible=[k for k,(start,end,projector,capacity,snack) in rooms.items() if (start is None or end<=840 or start>=960) and projector and capacity>=43]
assert eligible==['C','E'] and [k for k in eligible if rooms[k][-1]]==['E']
# Explicit feasible counterexamples for intersection changes.
profiles=list(product([0,1],repeat=3))
def metrics(d):
 return [sum(n*v[i] for v,n in d.items()) for i in range(3)]+[d.get((1,1,1),0)]
before1={(1,1,1):35,(0,0,0):65};after1={(1,1,1):35,(0,0,0):59,(1,0,0):2,(0,1,0):2,(0,0,1):2}
assert [b-a for a,b in zip(metrics(before1),metrics(after1))]==[2,2,2,0]
before2={(1,1,1):30,(1,1,0):20,(0,0,1):20,(0,0,0):30};after2={(1,1,1):31,(1,1,0):19,(0,0,1):19,(0,0,0):31}
assert metrics(before2)[:3]==metrics(after2)[:3]==[50]*3 and metrics(after2)[3]>metrics(before2)[3]
assert all((not all(v)) or v[2] for v in profiles)
weights=[]
for populations in permutations([100,200,300,400,500]):
 weighted=sum(p*r for p,r in zip(populations,[35,30,25,30,30]))/sum(populations)
 exact=F(30)+F(5*(populations[0]-populations[2]),sum(populations))
 assert F(sum(p*r for p,r in zip(populations,[35,30,25,30,30])),sum(populations))==exact!=30
 weights.append(str(exact))
result=dict(status='PASS',officialSourceKey=checks,clockFirstMinutes=str(clock),clockRelativeDegreesPerMinute='11/2',fishcakeEatenByEul=5,answerSequenceValid=valid,answerFrequencies=frequencies,roomsEligible=eligible,roomSelected='E',intersectionCounterexamples=[dict(before=metrics(before1),after=metrics(after1)),dict(before=metrics(before2),after=metrics(after2))],weightedMeanFormula='30+5*(populationA-populationC)/totalPopulation',distinctWeightModels=120,weightedExamples=sorted(set(weights)),qualitative={'s03':'3or5 quorum; director may preside; majority; written-hearing exception; oral-only publicity.', 's04':'Medical association OR liability insurance inclusive; medical versus nonmedical,report versus registration,3year renewal before expiry.', 's05':'West coast largest; east boiling; west/south solar evaporation; Mapo distribution not production.', 's11':'Exceptions remove prohibition but not notice; state/local installation versus research purpose; heritage-only consultation.', 's12':'Representative request versus minister; committee OR representative; employer measures; institution assessment versus individual diagnosis confidentiality.'},limitations='Same-author source re-solving and finite/symbolic checks,not independent review or real-device validation.')
(OUT/'source-key-model-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PASS10 official keys/source,3 native tables,clock/quota/time models,feasible intersection counterexamples,120 distinct weighted populations.')
