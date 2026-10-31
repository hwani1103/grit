from pathlib import Path
import json,subprocess,sys
from psat_batch_tools import validate
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/verbal27'
subprocess.run([sys.executable,str(A/'solve.py')],check=True)
bank=json.loads((A/'authored-verbal27.json').read_text(encoding='utf-8'));models=json.loads((A/'model-proof.json').read_text(encoding='utf-8'))
assert [q['answer'] for q in bank]==[3,5,1,5,1,1,2,5,3,2]
for q in bank:
 m=models[f"{q['examDate'][:4]}-{q['number']}"];assert q['answer']==m['answer']
 if 'truth' in m:assert [i for i,c in enumerate(q['choices'],1) if [v in c for v in 'ㄱㄴㄷ']==m['truth']]==[q['answer']]
assert bank[3]['body'] in bank[4]['body']
assert bank[2]['body'].count(bank[2]['underlines'][0])==1
validate('verbal27',{'directModelProof':models,'manualSourceReview':'All10 source columns visually inspected;39/40 full common passage retained;38 underline preserved;no image formulas required;historical/read-only passage reasoning no external factual substitution.'},[('2024-03-02',n) for n in range(36,41)]+[('2023-03-04',n) for n in range(1,6)],0)
