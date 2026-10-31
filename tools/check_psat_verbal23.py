"""V23 source/key gates plus logical countermodels; prose evidence remains reviewed manually."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,permutations
import json
import pdfplumber
from psat_batch_tools import validate,norm
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/verbal23'
bank=json.loads((A/'authored-verbal23.json').read_text(encoding='utf-8'));own=json.loads((A/'own-solve-before-key.json').read_text(encoding='utf-8'));p={}
qs={(int(q['examDate'][:4]),q['number']):q for q in bank}
def decision(year,n,truth,answer,known):
 q=qs[year,n];choices={i+1:tuple(k in c for k in 'ㄱㄴㄷ'[:len(truth)]) for i,c in enumerate(q['choices'])}
 assert [i for i,t in choices.items() if tuple(truth)==t]==[answer]
 assert [i for i,c in enumerate(q['choices'],1) if all((k in c)==v for k,v in known.items())]==[answer]
 assert own[f'{year}-{n}']['truth']==truth
 return choices
def anchors(year,n,parts):
 t=norm(qs[year,n]['body'])
 for part in parts:assert norm(part) in t,(year,n,part)
 return parts

# 36: exact symbolic inequality and all nonempty subsets of the exhaustive CNT types.
ratios=[]
for d in [F(1,10),F(1),F(3,2),F(10)]:
 for extraB,extraA in product([F(1,100),F(1),F(10)],repeat=2):
  gb=d+extraB;ga=gb+extraA;dg=gg=2*d
  assert ga/d>gb/d>gg/dg==1
  ratios.append(list(map(str,[ga/d,gb/d,gg/dg])))
subsets=[{t for t,on in zip(['SW','DW','MW'],flags) if on} for flags in product([False,True],repeat=3) if any(flags)]
peak=lambda types:bool(types&{'SW','DW'})
beta=[s for s in subsets if peak(s)];nopeak=[s for s in subsets if not peak(s)]
assert nopeak==[{'MW'}] and {'SW'} in beta and {'DW'} in beta
truth=[True,all(len(s)>=2 for s in beta),all(s=={'MW'} for s in nopeak)]
decision(2025,36,truth,4,{'ㄱ':True,'ㄴ':False})
p['2025-36']={'truth':truth,'betaPossibleTypes':[sorted(s) for s in beta],'noPeakTypes':[sorted(s) for s in nopeak],'inequality':'Dα=Dβ=d>0;Gα>Gβ>d;Gγ=Dγ=2d => Gα/d>Gβ/d>1','testedRationalInstances':len(ratios),'anchors':anchors(2025,36,['세 종류뿐이다','피크 높이로 나눈 값이 클수록','그리고 오직 그때에만'])}

# 37: observations read from the original circles/crosses, NOT from text extraction.
q37=qs[2025,37]
assert q37['figuresAfterBody'] is True
assert 'P 억제제는 뇌에서 ROS의 생성을 저해한다.' in q37['body']
assert all(s in q37['body'] for s in ['<실험 결과>를 얻었다.','실험 1:','실험 2:'])
transcripts=json.loads((A/'source-transcripts.json').read_text(encoding='utf-8'))
removed=transcripts[q37['id']]['removedBlocks']
assert len(removed)==1 and removed[0].startswith('<실험 결과>\n□ AMPK')
with pdfplumber.open(R/'artifacts/psat600_20261028/sources/4681/pdf/언어논리(가).pdf') as pdf:
 region=pdf.pages[18].crop((8,402,pdf.pages[18].width/2-6,641)).extract_text()
 assert norm(removed[0])==norm(region),'Every removed native word must exist inside its replacement image region'
states=[{'X','Y'},{'Y'},{'X'}] # M,MX,MY
observedAMPK={'saline':[False,False,False],'S1':[True,True,False]}
observedFood={'saline':[False,False,False],'S1':[True,False,False],'S2':[True,True,True]}
required=[set(),{'X'},{'Y'},{'X','Y'}];models=[]
for before,after in product(required,repeat=2):
 amp=[before<=s for s in states];food=[a and after<=s for a,s in zip(amp,states)]
 if amp==observedAMPK['S1'] and food==observedFood['S1']:
  # Saline turns the first stage off. S2 inhibits ROS directly in all mice.
  assert [False and after<=s for s in states]==observedFood['saline']
  assert [True for s in states]==observedFood['S2']
  models.append((before,after))
assert models==[({'Y'},{'X'}),({'Y'},{'X','Y'})]
claims=[lambda a,b:'X' in a and 'X' in b,lambda a,b:'X' in a and 'Y' in b,lambda a,b:'Y' in a and 'X' in b,lambda a,b:'Y' in a and 'Y' in b,lambda a,b:a=={'X','Y'} and not b]
entailed=[all(c(a,b) for a,b in models) for c in claims]
assert entailed==[False,False,True,False,False]
p['2025-37']={'AMPK':observedAMPK,'food':observedFood,'compatibleRequiredFactorModels':[{'beforeAMPK':sorted(a),'afterAMPK':sorted(b)} for a,b in models],'entailedChoiceClaims':entailed,'limit':'Only among the supplied explanations. Y involvement after AMPK is not excluded;no claim of exhaustive real biology.'}

# 38: fixed 2x2 factor design and every strict diversity ordering.
models=list(permutations(range(1,5)))
predA=lambda d:d[0]<d[2];predB=lambda d:d[1]>d[0]
items=[(lambda d:d[1]>d[0],predB,False),(lambda d:d[1]>d[0],predA,True),(lambda d:d[0]>d[2],predA,False),(lambda d:d[3]>d[2],predB,True),(lambda d:d[1]>d[3],predA,False)]
results=[];poss=[]
for premise,pred,target in items:
 values={pred(d) for d in models if premise(d)}
 results.append(values=={target});poss.append(sorted(values))
assert results==[False,False,True,False,False]
p['2025-38']={'modelFactors':{'1':['fertile','noHerbivore'],'2':['fertile','herbivore'],'3':['poor','noHerbivore'],'4':['poor','herbivore']},'hypothesisA':'D1<D3','hypothesisB':'D2>D1','comparisonPossibleTruth':poss,'correctEvaluation':results}

# 39-40: all three conjuncts required; no universal action premise and no necessity of determinism.
allCases=[]
for recognize,choose,execute in product([False,True],repeat=3):
 responsive=recognize and choose and execute
 allCases.append(dict(recognize=recognize,choose=choose,execute=execute,responsive=responsive))
missingExecution=next(c for c in allCases if c['recognize'] and c['choose'] and not c['execute'])
assert not missingExecution['responsive']
chip={'actionOccurs':True,'recognizesReason':False,'responsive':False}
detCases=[]
for deterministic in [False,True]:
 detCases.append({'deterministic':deterministic,'AresponsiveActionMayBeFree':True,'BepistemicBeliefChosen':False})
decision(2025,40,[False,False,True],2,{'ㄱ':False,'ㄴ':False})
assert qs[2025,39]['answer']==1
commonA=qs[2025,39]['body'];commonB=qs[2025,40]['body'].split('<보 기>',1)[0].strip()
assert commonA==commonB
p['2025-39']={'universalCounterexample':chip,'anchors':anchors(2025,39,['행위가 이유－반응적일 수 있으며','그 이유를 전혀 모른 채','인과적 결정론이 참인지 여부에 상관없이','그 믿음을 가졌다는 자체'])}
p['2025-40']={'allConjunctStates':allCases,'noncounterexample':missingExecution,'independenceOfDeterminism':detCases,'BexclusiveReasonClaim':'epistemic only;belief formed solely for moral reasons weakens,not strengthens'}

# Reading questions: explicit evidence anchors and reviewed rejection reasons, not fabricated numeric tests.
evidence={
1:['사은숙배와 사조를 모두 거친 자는 하직숙배','그 자리에서 파면당하는','경주인은 신임 수령이','통례원은 사은숙배를','사조는 오직 지방 수령에'],
2:['춥고 건조한 날씨에도 자랄 수 있는 개량 품종','그는 운남성에 유배된 적이 없으며','대도 근처 농촌에서','목화 재배에 성공한 사람은 그의 장인 정천익','홍원이라는 승려로부터'],
3:['금전적 대가를 지불하고','자신의 비용으로 구금하고 있는 포로','비공개로 진행했다','도덕적 비난의 대상이 될 수'],
4:['제도적 가족주의’가 공고한 사회','그 대표적인 예로 가족 부양자 모델','가족을 기본단위로 운용되며','불이익이 초래될 수 있다','부양과 돌봄을 둘러싸고 갈등'],
5:['경제적 불평등의 정도와','영아사망률이 그 대안이 될 수 있다','낮은 영아사망률은 양질의 생활에','1950년에 이르러서야 35～65명','인구가 많거나 인종적']}
verdicts={1:[False,False,False,False,True],2:[True,False,False,False,False],3:[False,False,False,False,True],4:[True,True,True,False,True],5:[False,True,True,True,True]}
for n in range(1,6):
 q=qs[2024,n];answer=own[f'2024-{n}']['answer'];supported=verdicts[n];seekFalse=n in [4,5]
 assert [i+1 for i,v in enumerate(supported) if v!=seekFalse]==[answer]
 p[f'2024-{n}']={'sourceAnchors':anchors(2024,n,evidence[n]),'supportedChoices':supported,'ownReason':own[f'2024-{n}']['proof'],'manualReview':'All five options compared with original text;absence of evidence distinguished from proven contrary facts.'}
assert [q['answer'] for q in bank]==[own[f"{q['examDate'][:4]}-{q['number']}"]['answer'] for q in bank]
assert [q['answer'] for q in bank]==[4,3,3,1,2,5,1,5,4,1]
validate('verbal23',{'semanticAndModelProof':p,'ownSolveBeforeKey':'own-solve-before-key.json','manualSourceReview':'All10 original questions plus shared39/40 passage viewed;37 table circles/crosses/legends preserved as original image;Greek and inverse-centimetre glyphs reviewed.'},[('2025-03-08',n) for n in range(36,41)]+[('2024-03-02',n) for n in range(1,6)],1)
