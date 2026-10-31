from pathlib import Path
import json,subprocess,sys
from psat_batch_tools import validate,norm
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/data25'
subprocess.run([sys.executable,str(A/'solve.py')],check=True)
bank=json.loads((A/'authored-data25.json').read_text(encoding='utf-8'));qs={q['number']:q for q in bank};models=json.loads((A/'model-proof.json').read_text(encoding='utf-8'))
assert [q['answer'] for q in bank]==[models['questions'][str(q['number'])]['answer'] for q in bank]==[2,4,4,3,5,2,4,1,3,1]
for n,truth in [(14,[True,False,True,False]),(16,[True,False,True]),(19,[False,True,True,False]),(23,[True,True,False,False])]:
 assert [i for i,c in enumerate(qs[n]['choices'],1) if [x in c for x in 'ㄱㄴㄷㄹ'[:len(truth)]]==truth]==[qs[n]['answer']]
for n in [17,21]:assert qs[n]['choiceNote']=='A → B → C'
assert qs[22]['choiceNote']=='B → C'
assert qs[22]['body'].startswith('<보고서>') and '다음으로 ‘갑’시에' in qs[22]['body']
assert len(qs[23]['figures'])==7 and not qs[23]['body']
assert not any(q['number']==13 for q in bank)
validate('data25',{'directModelProof':models,'heldCandidate':'2024D13 signed/magnitude change-rate ambiguity;unpublished;separate record','manualSourceReview':'All native columns14..23 visually read;15 map age/structure legend enlarged and matched;22/23 shared tables/report retained;23 incomegraph29.1%p bound;19 rounded rates treated as intervals.'},[('2024-03-02',n) for n in range(14,24)],21)
