from pathlib import Path
import json,subprocess,sys
from psat_batch_tools import validate
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/data26'
subprocess.run([sys.executable,str(A/'solve.py')],check=True)
bank=json.loads((A/'authored-data26.json').read_text(encoding='utf-8'));qs={q['number']:q for q in bank};models=json.loads((A/'model-proof.json').read_text(encoding='utf-8'))
numbers=[24,25,26,27,29,30,31,32,33,34]
assert [q['answer'] for q in bank]==[models['questions'][str(n)]['answer'] for n in numbers]==[3,5,3,4,2,5,4,4,1,1]
for n,truth in [(24,[True,False,False,True]),(26,[True,True,True,False]),(29,[True,False,False,True]),(30,[True,False,True,True]),(31,[True,False,True,True]),(33,[True,True,False,False])]:
 assert [i for i,c in enumerate(qs[n]['choices'],1) if [x in c for x in 'ㄱㄴㄷㄹ']==truth]==[qs[n]['answer']]
assert qs[24]['figuresAfterBody'] and qs[24]['body'].startswith('<보고서>')
assert len(qs[29]['figures'])==6 and not qs[29]['body']
assert len(qs[33]['underlines'])==4
assert 28 not in qs
validate('data26',{'directModelProof':models,'heldCandidate':'2024D28 signed/magnitude change-rate ambiguity;unpublished;separate record','manualSourceReview':'Original columns24..34 read;27 map shades/legends matched;30 omitted rows retained and explicit countermodel;31 rounded rates checked with intervals;33 report underlines preserved;34 lower rounding bound proves25%.'},[('2024-03-02',n) for n in numbers],26)
