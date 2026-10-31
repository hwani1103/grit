"""Direct originals and selected official keys; two-row and eligibility models."""
from pathlib import Path
from itertools import product
import json,re
import pdfplumber
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/psat_remaining605_20261030/batch10'
read=lambda f:json.loads(f.read_text(encoding='utf-8-sig'))
norm=lambda s:re.sub(r'[\s①②③④⑤ㆍ·「」『』\uf000\uf001]','',s)
rows=read(OUT/'revealed-current.json');sources={x['id']:x for x in read(OUT/'blind-source.json')};solves={x['id']:x for x in read(OUT/'own-solves.json')};checks=[]
for row in rows:
 q=row['question'];m=sources[q['id']];native=m['sourceText']
 native=re.sub(r'^.*?\b'+str(q['number'])+r'[.]\s*','',native,count=1,flags=re.S)
 if q['id']=='kr-mpm-2023-07-22-psat-l-23':
  t=q['tables'][0];assert t['columns']==['기준','(가)','(나)','(다)','(라)']
  assert t['rows']==[['A','㉠','㉡','㉢','㉣'],['B','㉤','㉥','㉦','㉧']] and t['afterParagraph']==3
  block='<표> 적극행정 국민신청안 처리 현황 안건 (가) (나) (다) (라) 기준 A ㉠ ㉡ ㉢ ㉣ B ㉤ ㉥ ㉦ ㉧'
  native=norm(native);assert native.count(norm(block))==1;native=native.replace(norm(block),'',1)
 a,b=norm(native),norm(q['prompt']+q['body']+''.join(q['choices']))
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
 assert answers[q['number']]==q['answer']==solves[q['id']]['answer']
 checks.append(dict(id=q['id'],source=m['source'],sourcePage=m['page'],sourceAndFiveChoicesMatch=True,key=row['officialKey'],keyPage=pi,answer=q['answer']))

# No need to assign a fictional rejection reason to a never-submitted case.
models=[]
for unknown in [False,True,None]:
 prior=[True,True,True,False];reason=[False,True,True,unknown]
 for A,B in [(prior,reason),(reason,prior)]:
  g=(A is not prior) or A[0]==A[1]
  n=(A[0]==A[2]) or (B is reason)
  d=(B[0]!=B[1]) or B[2]==B[3]
  models.append(dict(unassignedReason=unknown,A='prior' if A is prior else 'reason',truth=[g,n,d]))
assert [all(m['truth'][i] for m in models) for i in range(3)]==[True,False,False]
# Uniform support: both students and all independently proposed amendments.
students={'갑':('A','B'),'을':('B','A')}
current={s:[school=='A',resident=='B'] for s,(resident,school) in students.items()}
assert current=={'갑':[False,False],'을':[True,True]}
amendments={s:[resident=='A' and school=='A',resident=='A' and school=='A',school=='B'] for s,(resident,school) in students.items()}
assert amendments['갑']==[False,False,True]
qualitative={
 '2023l07':'Each meeting request mapped to the actual provided information. Option4 still sends readers to the phone for documents. Three-year limit is an example newly supplied by the option, not a number given by the dialogue or verified legal advice.',
 '2025l01':'Hwangnam turquoise bracelet versus Gyerim garnet sword; sender Naemul, transit permission Sosurim, audience Fujian; only first choice explicitly supported.',
 '2025l04':'Photographs and originals both treated as learned expert interpretation; Venus/pyramid later interpretation supports option5, not impossibility of learning.',
 '2025l05':'Final papers/access, intermediate outputs/data, other information/collaboration. Excluded categories remain excluded; no offline platform inferred.',
 '2025l06':'1948 association < 1960s semiconductor introduction;1960 quantity law<1965 joint venture<1966 qualitative law; goal versus actual consequence kept separate.',
 '2025l07':'Teacher at home defeats necessity of actual school location but not the student normative school destination. Future home destination does not equal speaker current location.',
 '2025l08':'Uncle specificity is paternal blood male older than father; generic true generation information is insufficient, not false. Future distance is the variable, not predictability.',
 '2025l09':'Manual/stress and camera notice/abusive complaints paired. C is still discussing termination authority. Relevance of before/after data is not complete causal proof.'}
result=dict(status='PASS',officialSourceKeys=checks,sourceTableAndPlacement=True,twoCriteriaModels=models,uniformCurrentEligibility=current,uniformIndependentAmendments=amendments,qualitativeChecks=qualitative,limitations='Same-author re-solving. Initial own solve unnecessarily set never-submitted rejection reason to false; correct proof leaves it unconstrained and original solve is retained. Not expert independence or device validation.')
(OUT/'source-key-model-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PASS direct10 official keys/source prose/five choices;1 native table;6 criterion models and independent ordinance amendments.')
