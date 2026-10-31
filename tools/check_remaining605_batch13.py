"""Direct source/key review, propositional models and exact Bayesian checks."""
from pathlib import Path
from itertools import product
from fractions import Fraction as F
import json,re
import pdfplumber
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/psat_remaining605_20261030/batch13'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
norm=lambda s:re.sub(r'[\s①②③④⑤ㆍ·「」『』\uf000\uf001/]','',s.replace('','α').replace('','β'))
rows=read(OUT/'revealed-current.json');sources={x['id']:x for x in read(OUT/'blind-source.json')};solves={x['id']:x for x in read(OUT/'own-solves.json')};checks=[]
for row in rows:
 q=row['question'];m=sources[q['id']];native=m['sourceText']
 if m['sharedPassageRange']:
  prefix,question=re.split(rf'\n{q["number"]}[.]\s*',native,maxsplit=1)
  prefix=re.sub(r'^\[21\s*～\s*22\]\s*다음 글을 읽고 물음에 답하시오[.]\s*','',prefix)
  prefix=re.sub(r'책형\s*11쪽','',prefix)
  if q['number']==21:stored=q['body'];tail=''
  else:stored,tail=q['body'].split('<사례>',1);tail='<사례>'+tail
  assert norm(prefix)==norm(stored),(q['id'],'shared source passage')
  a,b=norm(question),norm(q['prompt']+tail+''.join(q['choices']))
 else:
  native=re.sub(r'^.*?\b'+str(q['number'])+r'[.]\s*','',native,count=1,flags=re.S)
  if q['number']==13:
   native,n=re.subn(r'\(가\)\s*\(나\)\s*\(다\)\s*①','①',native);assert n==1
  if q['number']==23:
   t=q['tables'][0]
   assert t['columns']==['유형','활동','점수'] and t['rows']==[['Ⅰ','혁신적인 아이디어 제안','0～1'],['Ⅰ','예산을 절감하는 성과 창출','0～2'],['Ⅰ','국민 중점 민원 해결','0～3'],['Ⅱ','타 부서의 적극행정 추진에 협력','1'],['Ⅱ','적극행정 신규 사례 발굴','2']] and t['afterParagraph']==0
   block='유형 활동 점수 혁신적인 아이디어 제안 0～1 Ⅰ 예산을 절감하는 성과 창출 0～2 국민 중점 민원 해결 0～3 타 부서의 적극행정 추진에 협력 1 Ⅱ 적극행정 신규 사례 발굴 2'
   native=norm(native);assert native.count(norm(block))==1;native=native.replace(norm(block),'',1)
  expected=q['prompt']+q['body']+''.join(q['choices'])
  if q['number']==17:
   assert q['body'].count('□')==1
   expected=expected.replace('□','') # Source blank is a drawn box, not a text character.
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
 assert answers[q['number']]==q['answer']==solves[q['id']]['answer']
 checks.append(dict(id=q['id'],source=m['source'],page=m['page'],shared=m['sharedPassageRange'],sourceAndFiveChoicesMatch=True,key=row['officialKey'],keyPage=pi,answer=q['answer']))

models=[(p,i,s,n,o) for p,i,s,n,o in product([False,True],repeat=5) if (not p or o) and (not i or n) and (not s or p) and (s or i)]
options=lambda p,i,s,n,o:[n,i and s,p or s,o or p,n or o]
truth=[all(options(*v)[i] for v in models) for i in range(5)]
assert truth==[False,False,False,False,True]
counter={i+1:next(v for v in models if not options(*v)[i]) for i in range(4)}
# Mind-existence chain, retaining the conjunction in the second premise.
base=[v for v in product([False,True],repeat=5) if (not v[0] or v[1]) and (not(v[0] and v[1]) or v[2]) and (not v[2] or v[3]) and (not v[3] or v[4])]
extra=lambda m,d,e,k,u:[d,d or not m,k,not u,e]
completion=[all(not v[0] for v in base if extra(*v)[i]) for i in range(5)]
assert completion==[False,False,False,True,False]
assert all(not m or u for m,d,e,k,u in base)
# Gap algebra: old gap-new gap=(b0-b1)+(a1-a0)>0 when order stays.
gapCounts={'notCrossed':0,'equal':0,'crossSmaller':0,'crossLarger':0}
for a0,b0,a1,b1 in product(range(1,13),repeat=4):
 if not(a0<b0 and a1>a0 and b1<b0):continue
 if b1>a1:assert b1-a1<b0-a0;gapCounts['notCrossed']+=1
 elif b1==a1:assert 0<b0-a0;gapCounts['equal']+=1
 elif a1-b1<b0-a0:gapCounts['crossSmaller']+=1
 elif a1-b1>b0-a0:gapCounts['crossLarger']+=1
assert all(gapCounts.values())
assert abs(4-3)<5-1<abs(10-2)
posterior=lambda prior,accuracy:prior*accuracy/(prior*accuracy+(1-prior)*(1-accuracy))
taxi80=posterior(F(1,10),F(4,5));taxi70=posterior(F(1,10),F(7,10))
assert taxi80==F(8,26)<F(1,2) and taxi70==F(7,34)<F(1,2) and F(80,260)==taxi80
prior=F(1,1000000);sensitivity=F(99,100);falsePositive=F(1,100)
positive=prior*sensitivity+(1-prior)*falsePositive;post=posterior(prior,sensitivity)
assert positive==F(1000098,100000000)<F(1,2) and post==F(99,1000098)<F(1,10000)
assert 100*sensitivity==99 and F(99999900)*falsePositive==999999
# Continuous score proof uses independent closed intervals; endpoints give extrema.
scores=[(F(1)+a,b,F(2)+c) for a,b,c in product([F(0),F(1,2),F(1)],[F(0),F(3,2),F(3)],[F(0),F(1),F(2)])]
scoreTruth=[all([a<=b,b<=c,a<=c][i] for a,b,c in scores) for i in range(3)]
assert scoreTruth==[False,False,True] and (F(2),F(0),F(2)) in scores and (F(1),F(3),F(2)) in scores
assert max(a for a,b,c in scores)==min(c for a,b,c in scores)==2
result=dict(status='PASS',officialSourceKeys=checks,nativeTableCellsAndPlacement=True,selectionModels=len(models),selectionTruth=truth,selectionCounterexamples=counter,mentalChainCompletionTruth=completion,gapExamples=gapCounts,gapContinuousProof='If a0<b0,a1>a0,b1<b0 and a1<b1: (b0-a0)-(b1-a1)=(b0-b1)+(a1-a0)>0; equality gives zero; crossing alone permits both gap directions.',taxiPosteriors=[str(taxi80),str(taxi70)],rareTestPositive=str(positive),rareTestPosterior=str(post),rare100millionCounts={'truePositive':99,'falsePositive':999999,'positiveTotal':1000098},scoreIntervals=[[1,2],[0,3],[2,4]],scoreTruth=scoreTruth,scoreNonintegerSamplesIncluded=True,qualitative={'l11':'Acceleration happens outside before injection; density-temperature tradeoff is possibility requiring sufficient density,not any increase.', 'l12':'Interior zero both before and after charging; surface outward; no transient-state generalization.', 'l13':'Fixed spring rent versus current crop-linked rent; windfall to tenant; Jipjo similar only in reflecting current yield,not exact half.', 'l15':'Option4 attacks unit-analysis explanatory contribution rather than repeating criticism of element analysis.', 'l21':'Correct conclusion does not establish use of all available evidence.', 'l22':'Unconditional positivity differs from posterior illness; descriptive base-rate neglect differs from correct inference.'},limitations='Same-author re-solving; source given examples contain their own stated answers as passage content,not exposure of the question official keys. Not independent expert or medical advice or device verification.')
(OUT/'source-key-model-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PASS10 official originals/keys;shared passage and table;32-assignment logic,continuous gap/range proofs,exact Bayesian fractions.')
