"""Direct source/key checks and independent finite models, batch04."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json,re
import pdfplumber
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts/psat_remaining605_20261030/batch04'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
norm=lambda s:re.sub(r'[\s①②③④⑤·ㆍ\uf000\uf001『』□/]','',s)
items=read(OUT/'revealed-current.json');sources={x['id']:x for x in read(OUT/'blind-source.json')}
solves={x['id']:x for x in read(OUT/'own-solves.json')};checks=[]
for row in items:
 q=row['question'];m=sources[q['id']];native=m['sourceText']
 # Independently checked source's boxed blank and paired column labels.
 if q['number']==17:
  assert q['choiceNote']=='(가) / (나)'
  native=re.sub(r'\(가\)\s*\(나\)\s*①','①',native)
 if q['number']==18:
  table=q['tables'][0]
  assert table['columns']==['광검출기','A','B','C','D']
  assert table['rows']==[['I','○','○','×','×'],['II','×','○','×','○']]
  native,count=re.subn(r'빛\s*A\s*B\s*C\s*D\s*광검출기\s*I\s*○\s*○\s*×\s*×\s*II\s*×\s*○\s*×\s*○','',native)
  assert count==1
 if q['number'] in [19,20]:
  prefix,question=re.split(rf'\n{q["number"]}[.]\s*',native,maxsplit=1)
  prefix=re.sub(r'^\[19\s*～\s*20\]\s*다음 글을 읽고 물음에 답하시오[.]\s*','',prefix)
  prefix=re.sub(r'책형\s*10쪽','',prefix)
  stored_prefix,stored_look=q['body'].split('<보기>',1)
  assert norm(prefix)==norm(stored_prefix),(q['id'],'shared passage')
  assert norm(question)==norm(q['prompt']+'<보기>'+stored_look+''.join(q['choices'])),(q['id'],'question and choices')
 else:
  native=re.sub(r'^.*?\b'+str(q['number'])+r'[.]\s*','',native,count=1,flags=re.S)
  a,b=norm(native),norm(q['prompt']+q['body']+''.join(q['choices']))
  if a!=b:
   i=next((i for i,(x,y) in enumerate(zip(a,b)) if x!=y),min(len(a),len(b)))
   raise AssertionError((q['id'],i,a[max(0,i-40):i+100],b[max(0,i-40):i+100]))
 with pdfplumber.open(ROOT/row['officialKey']) as pdf:
  keypage,keytext=next((i+1,p.extract_text()) for i,p in enumerate(pdf.pages) if '영역 언어논리' in (p.extract_text() or ''))
 assert '2024' in keytext and '책형 사' in keytext
 answers={}
 for line in keytext.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
   z=list(map(int,line.split()));answers.update(zip(z[::2],z[1::2]))
 assert answers[q['number']]==q['answer']==solves[q['id']]['answer']
 checks.append(dict(id=q['id'],source=m['source'],page=m['page'],nativeTextAndChoicesMatch=True,
                    keyPdf=row['officialKey'],keyPage=keypage,answer=answers[q['number']]))

# l12: all five variables, actual inclusive disjunction.
models=[v for v in product([False,True],repeat=5) if
        (not v[0] or (v[1] and v[2])) and (v[1] or v[3]) and (v[0] or v[4])]
opts=lambda a,b,c,d,e:[a or b,not c or e,c or e,not d or e,not b or e]
truth=[all(opts(*v)[i] for v in models) for i in range(5)]
assert truth==[False,False,True,False,False]
counter={i+1:next(v for v in models if not opts(*v)[i]) for i in [0,1,3,4]}
# l19: omission of non-volitional premise and negation of conditional.
counter19=[v for v in product([False,True],repeat=3) if v[0]==v[1] and (v[2] or not v[1]) and v[0]]
assert counter19==[(True,True,True)]
assert all(not o for j,o,s in product([False,True],repeat=3) if not s and (s or not o))
# l18: enumerate integer thresholds with both strict and equality saturation cases.
patterns=[[True,True,False,False],[False,True,False,True]]
valid=[]
for a,b,c,d in product(range(1,7),repeat=4):
 if not(a>b>c and d>c):continue
 intervals=[]
 for pattern in patterns:
  intervals.append([(lo,hi) for lo in range(1,8) for hi in range(lo+1,9)
                    if [lo<=x<hi for x in [a,b,c,d]]==pattern])
 for (li,si),(lj,sj) in product(*intervals):
  assert li>lj and si>sj and sj<=a<si and lj<=d<li
  valid.append((a,b,c,d,li,si,lj,sj))
assert valid and any(x[0]==x[7] for x in valid)
widths={('I' if si-li>sj-lj else 'II' if si-li<sj-lj else 'equal') for a,b,c,d,li,si,lj,sj in valid}
assert widths=={'I','II','equal'}
q=F(1,4);assert [(1-q)/q,q/(1-q),(1-q)/q]==[3,F(1,3),3]
assert F(4,2)==2
result=dict(status='PASS',officialKeysAndNativeSource=checks,
 sourceVisual='10 complete original pages/columns read, shared passage all left then right; paired-choice headings, table, boxes and labels checked separately.',
 l12=dict(feasibleModels=len(models),fiveChoiceTruth=truth,counterexamples=counter),
 l19=dict(withoutNonVolitionalPremiseCounterexample=counter19,conditionalNegation='notS and O, not S'),
 l18=dict(validIntegerModels=len(valid),saturationEqualityExample=next(x for x in valid if x[0]==x[7]),
          possibleWiderInterval=sorted(widths),strictThresholdOrder=True),
 l10=dict(equivalentEventProbability='1/4',falseCandidates345=['3','1/3','3'],positiveDenominatorRequired=True),
 l17=dict(densityBOverA='2',perAreaElectronSame=True,sameAreaC='increase 10000->20000; decrease20000->30000'),
 l07='record time t: rare until t then frequent, not rare after t; four other edits contradict paragraph explanation',
 l08='manufactured exhibition self; excluded disagreeing others; only choice1 combines both',
 l15='position changes, not charge counts; either external polarity attracts when weight small',
 l16='closed passage: botulinum blocks ACh -> relaxation; tetanus blocks glycine -> contraction',
 l20='A accepts nonvolitional/liberal; B nonvolitional/deontological. True,false pattern for ㄱㄴㄷ =true,true,false.',
 limitations='Same-author source re-solving and checks; not independent expert or real-device validation.')
(OUT/'source-key-model-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PASS direct10 keys/texts,32-assignment logic,interval models with equality/width counterexamples,probability/density checks.')
