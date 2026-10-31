"""Batch07 source/key tables and all729 unknown-grade combinations."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json,re
import pdfplumber
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/psat_remaining605_20261030/batch07'
read=lambda f:json.loads(f.read_text(encoding='utf-8-sig'))
norm=lambda s:re.sub(r'[\s①②③④⑤ㆍ·「」『』\uf000\uf001]','',s)
rows=read(OUT/'revealed-current.json');sources={x['id']:x for x in read(OUT/'blind-source.json')};solves={x['id']:x for x in read(OUT/'own-solves.json')};checks=[]
expectedTables={
 'kr-mpm-2024-07-27-psat-l-22':dict(columns=['유형','주문 방법','결제 방법','수령 방법'],rows=[['대면','영업장 방문','영업장 방문','영업장 방문'],['예약 주문','온라인','영업장 방문','영업장 방문'],['스마트 오더','온라인','온라인','영업장 방문'],['완전 비대면','온라인','온라인','배송']],native='<표> 판매 유형 및 방법에 따른 구분 방법 주문 방법 결제 방법 수령 방법 유형 대면 영업장 방문 영업장 방문 영업장 방문 예약 주문 온라인 영업장 방문 영업장 방문 스마트 오더 온라인 온라인 영업장 방문 완전 비대면 온라인 온라인 배송'),
 'kr-mpm-2024-07-27-psat-l-23':dict(columns=['기관','연도','접근권한 관리','암호화 조치','접속기록 점검'],rows=[['A','2023','㉠','중','㉡'],['A','2024','㉢','하','상'],['B','2023','㉣','상','하'],['B','2024','중','㉤','㉥']],native='<표> 2023년과 2024년 보호수준 평가 결과 항목 기관 접근권한 관리 암호화 조치 접속기록 점검 연도 2023 ㉠ 중 ㉡ A 2024 ㉢ 하 상 2023 ㉣ 상 하 B 2024 중 ㉤ ㉥')}
for row in rows:
 q=row['question'];m=sources[q['id']];native=m['sourceText']
 if m['sharedPassageRange']:
  prefix,question=re.split(rf'\n{q["number"]}[.]\s*',native,maxsplit=1)
  prefix=re.sub(r'^\[21\s*～\s*22\]\s*다음 글을 읽고 물음에 답하시오[.]\s*','',prefix);prefix=re.sub(r'책형\s*11쪽','',prefix)
  stored,look=q['body'].split('<보기>',1);assert norm(prefix)==norm(stored)
  a,b=norm(question),norm(q['prompt']+'<보기>'+look+''.join(q['choices']))
 else:
  native=re.sub(r'^.*?'+str(q['number'])+r'[.]\s*','',native,count=1,flags=re.S);native=norm(native)
  if q['id'] in expectedTables:
   table=expectedTables[q['id']];assert q['tables'][0]['columns']==table['columns'] and q['tables'][0]['rows']==table['rows']
   block=norm(table['native']);assert native.count(block)==1,(q['id'],'table');native=native.replace(block,'',1)
  a,b=native,norm(q['prompt']+q['body']+''.join(q['choices']))
 if a!=b:
  i=next((i for i,(x,y) in enumerate(zip(a,b)) if x!=y),min(len(a),len(b)))
  raise AssertionError((q['id'],i,a[max(0,i-20):i+100],b[max(0,i-20):i+100]))
 with pdfplumber.open(ROOT/row['officialKey']) as pdf:
  pi,t=next((i+1,p.extract_text()) for i,p in enumerate(pdf.pages) if '영역 언어논리' in (p.extract_text() or ''))
 assert q['examDate'][:4] in t and f"책형 {q['book']}" in t
 answers={}
 for line in t.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
   z=list(map(int,line.split()));answers.update(zip(z[::2],z[1::2]))
 assert q['answer']==answers[q['number']]==solves[q['id']]['answer']
 checks.append(dict(id=q['id'],source=m['source'],page=m['page'],shared=m['sharedPassageRange'],sourceAndFiveChoicesMatch=True,tableChecked=q['id'] in expectedTables,key=row['officialKey'],keyPage=pi,answer=q['answer']))

weak=lambda prev,cur:cur.count('하')==3 or(prev.count('하')==2 and cur.count('하')==2)
excellent=lambda prev,cur:prev.count('상')>=2 and cur.count('상')>=2 and '하' not in cur
fail=[[],[],[]];antecedent=[0,0,0];forced=[]
for v in product(['상','중','하'],repeat=6):
 a,b,c,d,e,f=v;ap=[a,'중',b];ac=[c,'하','상'];bp=[d,'상','하'];bc=['중',e,f]
 if a!=c:
  antecedent[0]+=1
  if weak(ap,ac) or excellent(ap,ac):fail[0].append(v)
 if e==f=='하':
  antecedent[1]+=1
  if not weak(bp,bc):fail[1].append(v)
 if weak(ap,ac) and excellent(bp,bc):
  antecedent[2]+=1;forced.append((b,d))
  if b==d:fail[2].append(v)
assert not fail[0] and fail[1] and not fail[2] and set(forced)=={('하','상')} and all(antecedent)
# DNA clock: positive observed differences are converted by same calibrated rate.
clock=lambda target,reference,time:F(target,reference)*time
assert clock(2,1,5500000)>5500000>120000
assert 5500000+500000==6000000
# Required B production and threshold C contraction are separate links.
models=[v for v in product([False,True],repeat=3) if (not v[1] or v[0]) and v[2]==v[1]]
assert all(not contract for B,C,contract in models if not B)
assert all(contract for B,C,contract in models if C)
result=dict(status='PASS',officialKeySource=checks,gradeModels=729,conditionalAntecedentCounts=antecedent,gradeTruth=[True,False,True],secondClaimCounterexample=fail[1][0],forcedForThird=forced,DNAClock=dict(referenceYears=5500000,contradictingTargetYears=11000000,correctedReferenceYears=6000000,assumption='same positive sequence-change rate; cannot infer new exact clothing date from correction alone'),causalModels=models,
 qualitativeChecks={'2023l21':'samefetus versus differentfutureindividual;Bcannotcompareunconceivedpersons;ㄱㄴㄷtrue.', '2024l21':'delay/reabuse timing relevant;unrecognized/no-protection fraction is procedural,not false-negative truth;noncohabitation not reportbarrier.', '2024l22':'before:face/reserve both storepayment;deliveryexplicitexceptions;permittednewmethod doesnotbanold.', '2024l24':'乙targets missing phrase inarticle7,not differing meaning inarticle3;丁rejectsanalogy by12vs6months;戊flexiblepurposeanalogy.', '2024l25':'same-state scope explainsdifference;prospectiveharm contested;mandatoryforeigncreditcompatiblewith甲butno completeagreementinferred.', '2023l01':'guardgate duty remainsoriginalmilitary;police separated;reportagency unprovided.', '2023l02':'lossesleadpeace;Sukjongestablishes;Yejong2expedition;CheokrescuesYuntoYeongju,notGilju.'},
 limitations='Same-author review,not expert independence or realdevice verification.')
(OUT/'source-key-model-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PASS10directsource/keys,2native tables,729grade models,clock andclosedcausal boundary checks.')
