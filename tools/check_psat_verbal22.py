from pathlib import Path
from itertools import product
from fractions import Fraction as F
import json
from psat_batch_tools import validate
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/verbal22'
bank=json.loads((A/'authored-verbal22.json').read_text(encoding='utf-8'));own=json.loads((A/'own-solve-before-key.json').read_text(encoding='utf-8'))
nums=list(range(24,33))+[35];answers=[5,2,4,1,3,5,3,3,1,2]
assert [q['number'] for q in bank]==nums
assert [q['answer'] for q in bank]==[own[str(n)]['answer'] for n in nums]==answers
p={str(n):{'directSolve':own[str(n)]['proof'],'answer':own[str(n)]['answer']} for n in nums}
def early(n,known,expected):
 q=next(q for q in bank if q['number']==n)
 remaining=[i+1 for i,c in enumerate(q['choices']) if all((k in c)==v for k,v in known.items())]
 assert remaining==expected,(n,remaining)
 p[str(n)]['choiceElimination']={'known':known,'remaining':remaining}
for n,truth,answer in [(30,[True,False,True],3),(31,[True,True,False],3),(32,[True,False,False],1),(35,[False,False,True],2)]:
 q=next(q for q in bank if q['number']==n)
 matches=[i+1 for i,c in enumerate(q['choices']) if [k in c for k in 'ㄱㄴㄷ']==truth]
 assert matches==[answer] and truth==own[str(n)]['truth'];p[str(n)]['truth']=truth
early(30,{'ㄴ':False,'ㄷ':True},[3]);early(31,{'ㄱ':True,'ㄷ':False},[1,3]);early(32,{'ㄱ':True,'ㄴ':False},[1]);early(35,{'ㄱ':False,'ㄴ':False},[2])
# 27: assess both slots separately, using the actual duplicated text in choices.
q=bank[3];first=[c.split('\n')[0] for c in q['choices']];second=[c.split('\n')[1] for c in q['choices']]
assert first[0]==first[1] and first[2]==first[3]
assert second[0]==second[2]==second[4] and second[1]==second[3]
assert set([1,2]) & set([1,3,5])=={1}
p['27']['slots']={'firstMatches':[1,2],'secondMatches':[1,3,5],'both':[1]}
# 28: a family of possible costs, rather than inventing an exact missing marginal cost.
price=F('17.2');average=F('20.6')
assert average>price
possible=[]
for cents in range(0,172):
 marginal=F(cents,10);initialQuantity=100;fixed=(average-marginal)*initialQuantity
 before=price*initialQuantity-(fixed+marginal*initialQuantity)
 after=price*(initialQuantity+1)-(fixed+marginal*(initialQuantity+1))
 assert before<0 and after>before
 possible.append(str(after-before))
p['28']['model']={'testedMarginalCosts':'0.0..17.1 step0.1; examples, not a claimed exact cost','profitChangeIdentity':'price-marginal>0','allReduceLoss':True,'initialLoss':'340cents'}
# 31: enumerate truth assignments to preserve arrow directions and exhibit converse failure.
worlds=list(product([False,True],repeat=2))
A_worlds=[(law,natural) for law,natural in worlds if not law or natural]
B_worlds=[(natural,boundary) for natural,boundary in worlds if not natural or boundary]
assert all(natural for law,natural in A_worlds if law)
assert all(boundary for natural,boundary in B_worlds if natural)
assert (False,True) in B_worlds # clear boundary does not force natural kind
p['31']['models']={'A_lawImpliesNatural':A_worlds,'B_naturalImpliesBoundary':B_worlds,'reverseCounterexample':[False,True],'KoreanSocialAge40Meets65':40>=65,'A40Classification':'not required or inferred'}
# 32: four conjunctive conditions; necessity violation is J=true with one condition=false.
worlds=[(c,all(c)) for c in product([False,True],repeat=4)]
assert all(not j for c,j in worlds if not c[0])
assert not any(j for c,j in worlds if not c[2])
assert any(not j for c,j in worlds if not c[2])
assert all(not j for c,j in worlds if not c[1])
p['32']['model']={'all16ConjunctionStates':True,'A_noSeriousHarmButJustified':'violates necessity','B_noEvidenceAndNotJustified':'compatible','A_noInternalReportButJustified':'violates necessity','B_unstatedBeliefs':'not supplied'}
# 35: trace the shared link separately from the two different downstream mechanisms.
p['35']['links']={'common':'sexual>asexual genetic diversity','A':'diversity mitigates environmental extinction','B':'diversity mitigates same-resource competition','a':'high environmental variation/higher sexual share supports A','b':'asexual higher competition supports B','c':'asexual greater diversity contradicts common link','limit':'support is not a proof of exclusive causality'}
# Reading proofs cite exact native passage anchors; semantic judgments remain explicit author review.
anchors={24:['인간의 근력 말고는 다른 동력원','그 양은 매우 적었다','문자도 없었고'],25:['사용료를 도시보다 더 높게','민영화에 반대하는 사람들은','민영화를 국가 정책으로 추진'],26:['학제가 아니라 문제에서 시작','학제에 정통할 수 있는 연구자의 역량','학제의 의례와 규범을 초월'],29:['제곱미터당 약 100그램','500그램까지','가장 효율적인 동물도 아니지만','즉시 보충하지 않아도'],30:['자금의 흐름에 실제로 영향을','실질적인 자원의 흐름과는 무관하게','광고비를 대폭 늘려 지출'],31:['자연종이 되기 위해서는','65세 이상이라는 속성'],32:['경우 그리고 오직 그 경우에만','그 어떤 조치도 취해지지 않았어야'],35:['무성생식보다 더 많은 유전적 다양성','유성생식만큼은 경쟁을 완화하지 못한다']}
for n,items in anchors.items():
 q=next(q for q in bank if q['number']==n)
 for item in items:assert item in q['body'],(n,item)
 p[str(n)]['nativeEvidence']=items
assert bank[2]['body'].count('[빈칸]')==1 and bank[3]['body'].count('[빈칸]')==2 and bank[4]['body'].count('[빈칸]')==3
assert bank[6]['underlines']==['‘이익조정’']
validate('verbal22',p,[('2025-03-08',n) for n in nums],figure_count=0)
