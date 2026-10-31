"""Original/shared text and keys; denominator counterexamples and underline ink."""
from pathlib import Path
from collections import deque
from fractions import Fraction as F
import json,re
import pdfplumber
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/psat_remaining605_20261030';B=OUT/'batch19'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
write=lambda p,v:p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
norm=lambda s:re.sub(r'[\s①②③④⑤ㆍ·․「」『』\uf000\uf001/]','',s)
rows=read(B/'revealed-current.json');sources={x['id']:x for x in read(B/'blind-source.json')};solves={x['id']:x for x in read(B/'own-solves.json')};checks=[]
key21=None
for row in rows:
 q=row['question'];m=sources[q['id']];native=m['sourceText']
 if m['sharedPassageRange']:
  assert q['id']=='kr-mpm-2021-07-10-psat-l-22'
  common,question=re.split(r'\n(?:문\s*)?22[.]\s*',native,maxsplit=1)
  common=re.sub(r'^※\s*\[(?:문\s*)?21[.]?\s*[～~∼-]\s*(?:문\s*)?22[.]?\]\s*다음 글을 읽고 물음에 답하시오[.]\s*','',common)
  stored,tail=q['body'].split('<보기>',1)
  assert norm(common)==norm(stored),(q['id'],'shared source')
  native=question;expected=q['prompt']+'<보기>'+tail+''.join(q['choices'])
 else:
  native=re.sub(r'^.*?\b'+str(q['number'])+r'[.]\s*','',native,count=1,flags=re.S)
  expected=q['prompt']+q['body'].replace('□','')+''.join(q['choices'])
 a,b=norm(native),norm(expected)
 if a!=b:
  i=next((i for i,(x,y) in enumerate(zip(a,b)) if x!=y),min(len(a),len(b)))
  raise AssertionError((q['id'],i,a[max(0,i-25):i+120],b[max(0,i-25):i+120]))
 with pdfplumber.open(ROOT/row['officialKey']) as pdf:
  pi,t=next((i+1,p.extract_text()) for i,p in enumerate(pdf.pages) if '영역 언어논리' in (p.extract_text() or ''))
 assert q['examDate'][:4] in t and f"책형 {q['book']}" in t
 answers={}
 for line in t.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
   z=list(map(int,line.split()));answers.update(zip(z[::2],z[1::2]))
 assert answers[q['number']]==q['answer']
 ownCorrect=solves[q['id']]['answer']==q['answer']
 if not ownCorrect:
  assert q['id']=='kr-mpm-2021-07-10-psat-l-19' and solves[q['id']]['answer']==5 and q['answer']==3
  correction=read(B/'post-reveal-reasoning-correction.json');assert correction['correctedAnswer']==3 and correction['publishedAnswerAndExplanationAlreadyCorrect']
 if q['examDate']=='2021-07-10':key21=answers[21]
 checks.append(dict(id=q['id'],source=m['source'],sourcePage=m['page'],fullNativePassageAndFiveChoicesMatch=True,key=row['officialKey'],keyPage=pi,publishedAnswerMatchesOfficial=True,ownInitialAnswer=solves[q['id']]['answer'],ownInitialAnswerMatches=ownCorrect))
assert key21==read(B/'related295-shared21-before.json')['answer']==read(B/'related295-shared21-own.json')['answer']==1

# Explicit original underline strokes, excluding labels and un-underlined suffixes.
def underlineText(qid,ys):
 m=sources[qid];out=[]
 with pdfplumber.open(ROOT/m['source']) as pdf:
  page=pdf.pages[m['page']-1]
  for y in ys:
   ls=[ln for ln in page.lines if abs(ln['top']-y)<.01 and abs(ln['top']-ln['bottom'])<.1]
   assert len(ls)==1,(qid,y,len(ls));ln=ls[0]
   chars=[c for c in page.chars if ln['x0']<=(c['x0']+c['x1'])/2<=ln['x1'] and ln['top']-10<c['bottom']<ln['top']+2]
   out.append(''.join(c['text'] for c in chars))
 return out
shared=underlineText('kr-mpm-2021-07-10-psat-l-22',[202.94,648.37,249.93,265.63])
assert list(map(norm,shared))==list(map(norm,['A의 주장','B의 주장','X의 지속적인 사용은 미국 사회의','인종차별을 고착화한다']))
seven=underlineText('kr-mpm-2025-11-15-psat-l-07',[183.11,239.22,257.93,370.17,388.87,519.82,538.52,557.23])
assert list(map(norm,seven))==list(map(norm,['이성적으로 통제할 수 있다','집단 내 결혼으로','발생하는 유전적 악화','단순한','증여 행위가 아니라','권리라는 점에서','자율적','집단 외 결혼']))
robot=underlineText('kr-mpm-2025-11-15-psat-l-13',[589.13,607.83])
assert norm(''.join(robot))==norm('로봇이 그 윤리 원칙을 위반했더라도 로봇의 당시 행위가 허용된다')
write(B/'source-underline-boundaries.json',dict(status='source_confirmed',method='Match centers of original PDF glyphs immediately above each original underline stroke; original page images also inspected.',sharedPassageSource=shared,marriageSource=seven,robotCorrectControl=robot,requiredCorrections=['l22 label anchors must not be underlined','l22/l21 final period is outside underline','l07 suffix 고 after 있다 is outside underline'],limitations='Only specified stroke coordinates, not automatic blanket extraction of all PDF underlines.'))

# Same facility counts can reverse supply-per-population comparison.
assert F(10,1000)>F(300,1000000)>F(10,100000)
ageModels=[dict(willing5064=500,age5064=1000,disabledTotal=2000),dict(willing5064=500,age5064=1000,disabledTotal=20000)]
assert {F(v['age5064'],v['disabledTotal']) for v in ageModels}=={F(1,2),F(1,20)}
assert len({v['willing5064'] for v in ageModels})==1

# Four categories: accepted/rejected fixed, conditional differs with unreviewed.
categoryModels=[dict(total=100,accepted=40,rejected=20,conditional=10,unreviewed=30),dict(total=100,accepted=40,rejected=20,conditional=40,unreviewed=0)]
assert all(v['accepted']+v['rejected']+v['conditional']+v['unreviewed']==v['total'] for v in categoryModels)
assert len({(F(v['accepted'],v['total']),F(v['rejected'],v['total'])) for v in categoryModels})==1
assert len({F(v['conditional'],v['total']) for v in categoryModels})==2

def maxRun(seq):
 runs=[];last=None;run=0
 for value in seq:
  run=run+1 if value==last else 1;last=value;runs.append(run)
 return max(runs)
assert maxRun(['C','C','D','C'])==2 and ['C','C','D','C'].count('C')==3

edges=[('paternalGrandfather','father'),('father','me'),('me','son'),('paternalGrandfather','uncle'),('maternalGrandmother','mother'),('mother','me'),('maternalGrandmother','aunt'),('aunt','cousin')]
graph={}
for a,b in edges:graph.setdefault(a,[]).append(b);graph.setdefault(b,[]).append(a)
def distance(start,goal):
 pending=deque([(start,0)]);seen={start}
 while pending:
  node,n=pending.popleft()
  if node==goal:return n
  for neighbor in graph[node]:
   if neighbor not in seen:seen.add(neighbor);pending.append((neighbor,n+1))
assert distance('me','uncle')==distance('paternalGrandfather','son')==3 and distance('me','cousin')==4

qualitative={
'2021l22':'Equal highest-risk fraction in a subgroup does not strengthen overall racial disparity. Within-group accuracy versus base rate is not itself contradiction of nonbias. Same-crime source does not establish historical bias feedback; not strengthening does not mean disproving.',
'2021l23':'First refusal versus repeated identical request. Per recipient12000 not aggregate1080000. DifferentY andX matters; no profession link does not permit2000000 per occasion.',
'2021l25':'Term continuity and counting invalid reelection explain disputes conditionally; interveningD breaks consecutive-three ban.',
'2025l01':'Clerk records accessible to officials; internal6:3 composition is not cross-office headcount.',
'2025l04':'Some subjective classification allowed; most classifications grounded in objective similarity.',
'2025l07':'Reciprocity obligation and coercion apply consistently to gift and marriage. Original erroneous rights/autonomy phrase is the question, must remain in passage.',
'2025l13':'Human harm breaches first rule; refusal/self damage already subject to higher-priority exceptions. Additional accepted unavoidable rescue harm closes the missing justification, not merely self damage.'}
write(B/'source-key-model-checks.json',dict(status='PASS',count=10,officialSourceKeys=checks,initialAnswerCorrectCount=9,initialAnswerCorrection='post-reveal-reasoning-correction.json',relatedPrior295Shared21OfficialAnswer=1,relatedOldScorePreserved=True,ageCompositionCountermodels=ageModels,fourCategoryCountermodels=categoryModels,maximumConsecutiveChairTerms=2,kinshipDistances=[3,3,4],qualitative=qualitative,previousOfficialAnswerExposureCount=4,limitations='Same-author review. l19 original answer5 was wrong and remains frozen; published3 already correct. Four prior key exposures disclosed. Stroke evidence separate; no independent/device review.'))
print('PASS10 native original/published-key matches; own9/10 with one disclosed correction; related21, denominator/category countermodels and source underline strokes.')
