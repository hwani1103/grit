from pathlib import Path
import json,subprocess,sys
from psat_batch_tools import validate
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/data27'
subprocess.run([sys.executable,str(A/'solve.py')],check=True)
bank=json.loads((A/'authored-data27.json').read_text(encoding='utf-8'));models=json.loads((A/'model-proof.json').read_text(encoding='utf-8'))
assert [q['answer'] for q in bank]==[3,2,5,3,2,2,1,5,5,1]
for q in bank:assert q['answer']==models[str(q['number'])]['answer']
assert len(bank[6]['underlines'])==4 and len(bank[7]['figures'])==7
validate('data27',{'directModelProof':models,'manualSourceReview':'All ten original columns and two-column D3 read visually;interval endpoints,rounding,joint distribution counterexample,award memberships,tax response,conditional denominator checked;D36 held for signed/absolute ambiguity.'},[('2024-03-02',n) for n in [35,37,38,39,40]]+[('2023-03-04',n) for n in range(1,6)],21)
