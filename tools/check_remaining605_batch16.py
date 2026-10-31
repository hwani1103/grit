"""Original/key matching, finite countermodels and two criterion assignments."""
from pathlib import Path
from itertools import product
import hashlib,json,re,shutil,subprocess
import pdfplumber
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/psat_remaining605_20261030';B=OUT/'batch16'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
norm=lambda s:re.sub(r'[\s①②③④⑤ㆍ·․「」『』\uf000\uf001/]','',s)
rows=read(B/'revealed-current.json');sources={x['id']:x for x in read(B/'blind-source.json')};solves={x['id']:x for x in read(B/'own-solves.json')}
reg={x['newAsset']:x for x in read(ROOT/'artifacts/psat_final_quality_20261029/full900/native-image-repairs.json')['figures']};checks=[];pixels=[]
for row in rows:
 q=row['question'];m=sources[q['id']];native=norm(re.sub(r'^.*?\b'+str(q['number'])+r'[.]\s*','',m['sourceText'],count=1,flags=re.S))
 for f in q.get('figures',[]):
  r=reg[f['asset']]
  with pdfplumber.open(ROOT/r['source']) as pdf:figtext=norm(pdf.pages[r['page1based']-1].crop(r['rect']).extract_text() or '')
  assert native.count(figtext)==1;native=native.replace(figtext,'',1)
  assert hashlib.sha256((ROOT/r['source']).read_bytes()).hexdigest()==r['sha256']
  d=B/'fresh-source-renders';d.mkdir(exist_ok=True);prefix=d/f"{r['sha256'][:16]}-p{r['page1based']:02d}"
  subprocess.run([shutil.which('pdftoppm'),'-r',str(r['resolution']),'-f',str(r['page1based']),'-l',str(r['page1based']),'-singlefile','-png',str(ROOT/r['source']),str(prefix)],check=True,capture_output=True)
  with Image.open(prefix.with_suffix('.png')) as im,Image.open(ROOT/f['asset']) as actual:
   a=im.convert('RGB').crop(r['pixelBox']);b=actual.convert('RGB');assert a.size==b.size and a.tobytes()==b.tobytes()
  pixels.append(dict(id=q['id'],asset=f['asset'],pixelMatch=True))
 if q['number']==18 and q['examDate']=='2021-07-10':
  t=q['tables'][0];assert t==dict(caption='입안 지원 신청 조례안별 분류',columns=['기준','(가)','(나)','(다)'],rows=[['A','㉠','㉡','㉢'],['B','㉣','㉤','㉥']],afterParagraph=2)
  block=norm('<표> 입안 지원 신청 조례안별 분류 조례안 (가) (나) (다) 기준 A ㉠ ㉡ ㉢ B ㉣ ㉤ ㉥');assert native.count(block)==1;native=native.replace(block,'',1)
 expected=norm(q['prompt']+q['body'].replace('□','')+''.join(q['choices']))
 if native!=expected:
  i=next((i for i,(a,b) in enumerate(zip(native,expected)) if a!=b),min(len(native),len(expected)))
  raise AssertionError((q['id'],i,native[max(0,i-20):i+120],expected[max(0,i-20):i+120]))
 with pdfplumber.open(ROOT/row['officialKey']) as pdf:
  pi,t=next((i+1,p.extract_text()) for i,p in enumerate(pdf.pages) if '영역 언어논리' in (p.extract_text() or ''))
 assert q['examDate'][:4] in t and f"책형 {q['book']}" in t
 answers={}
 for line in t.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
   z=list(map(int,line.split()));answers.update(zip(z[::2],z[1::2]))
 assert answers[q['number']]==q['answer']==solves[q['id']]['answer']
 checks.append(dict(id=q['id'],source=m['source'],sourcePage=m['page'],nativePromptBodyAndFiveChoicesMatch=True,key=row['officialKey'],keyPage=pi,answer=q['answer']))

# l06: finite people include a third person; never assume only named people exist.
persons=[(g,c,p,u) for g,c,p,u in product([False,True],repeat=4) if not(g and(c or p))]
rep=lambda x:(x[1] or x[2]) and x[3]
models=[];counter={};validCounts=[0]*5
for people in product(persons,repeat=3):
 if not any(map(rep,people)):continue
 a,e,third=people
 options=[a[1] and a[3],(a[1] or a[2] or e[1] or e[2]),not a[0] and not e[0] and a[3] and e[3],e[2] or not e[3],all(not(x[1] or x[2]) or x[3] for x in people)]
 namedRepresentative=rep(a) or rep(e)
 for i,hypothesis in enumerate(options):
  if not hypothesis:continue
  validCounts[i]+=1
  # For non-entailment choose A participation false, allowed when both names are nonrepresentatives.
  if not namedRepresentative and i+1 not in counter:counter[i+1]=people
 models.append(people)
assert validCounts[0]>0 and set(counter)=={2,3,4,5}
# A may participate for another reason: given namedRepresentative -> A does not establish necessity.
necessaryCounter=dict(people=counter[5],participationA=True,namedRepresentative=False)

# l12: both failures can be weakened to their disjunction, extra goal irrelevant.
chains=[]
for f1,f2,extra,discard,psychology in product([False,True],repeat=5):
 if (f1 or f2) and not discard:continue
 if discard and not psychology:continue
 chains.append((f1,f2,extra,discard,psychology))
assert all(v[4] for v in chains if v[0] and v[1])
assert all(v[4] for v in chains if v[0] or v[1])
assert {v[2] for v in chains if v[0] and v[1]}=={False,True}

# l18: exactly two distinct criteria, each sequence transcribed from source cases.
complete=[False,True,False];similar=[True,True,False];assignments=[dict(A=complete,B=similar),dict(A=similar,B=complete)]
assert all(s['B'][0]==s['B'][2] for s in assignments if s['A']==similar)
assert all(s['A'][0]==s['A'][2] for s in assignments if s['B']==similar)
assert any(s['B'][0]==s['B'][1] and s['A'][0]!=s['A'][1] for s in assignments)

# l02: same current state permits different final years, so no annual prediction follows.
assert 10-7-2==1 and 7/10==.7
possibleFinal=[(10,7),(10,9),(20,7),(20,10),(30,30)]
assert any(n/d>.6 for d,n in possibleFinal) and any(n/d<.6 for d,n in possibleFinal)
assert any(n!=9 for d,n in possibleFinal) and {d<15 for d,n in possibleFinal}=={False,True}

qualitative={
'2025l24':'Registration is the dialogue condition for mandatory closing; unregistered opening is separately referred to investigators. No inference about current real law.',
'2025l25':'Each option supplies a separate conditional interpretation: third party includes auction buyer; handwritten date accepted or not explains disagreement; tenant-choice purpose supports termination.',
'2021l10':'Treatment groups support reported per-cell synapse/capillary differences, not total neuron increases, relative effect size, mediator direction or improved performance.',
'2021l11':'Room2 A attacks/B none supports ultrasound fallback. Room3 B same as room1 supports distinction of different sound, not proof of ultrasound nonuse.',
'2021l14':'Source underline ends at each view, excluding author evaluation. Philosophy subset and unavoidable abduction refute universal nonnecessity; empirical-premise deduction is a counterexample to identifying empirical content with inductive method.',
'2021l17':'Old all agencies: announcement/application/documents/written/interview/result. New province first announcement/application/written, agencies documents/interview/result. Original figure blank labels and owner-box spans visually matched.'}
result=dict(status='PASS',count=10,officialSourceKeys=checks,figurePixels=pixels,nativeTableCellsAndPlacement=True,representativeModels=len(models),representativeHypothesisCounts=validCounts,representativeNonEntailmentCountermodels=counter,representativeIsSufficientNotNecessaryForA=necessaryCounter,chainAssignments=len(chains),criterionAssignments=assignments,currentVsFinalCounterexamples=possibleFinal,qualitative=qualitative,previousOfficialKeyExposureCount=8,limitations='Same-author review; eight key-exposed solves not blind. Finite countermodels supplement source reasoning; qualitative evidence is not mechanically proved. No APK/device.')
(B/'source-key-model-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PASS10 native source/key matches; original figure pixels/table; representative countermodels, weakened-premise chain and both criterion assignments.')
