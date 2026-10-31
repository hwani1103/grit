from pathlib import Path
import json,subprocess,sys
from psat_batch_tools import validate
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/verbal28'
subprocess.run([sys.executable,str(A/'solve.py')],check=True)
bank=json.loads((A/'authored-verbal28.json').read_text(encoding='utf-8'));proof=json.loads((A/'model-proof.json').read_text(encoding='utf-8'))
assert [q['answer'] for q in bank]==[1,3,4,4,4,3,1,4,5,4]
for q in bank:assert q['answer']==proof[str(q['number'])]['answer']
assert bank[1]['body'].count('π')==2 and len(bank[4]['underlines'])==5 and '[빈칸]' in bank[-1]['body']
validate('verbal28',{'directModelProof':proof,'manualSourceReview':'Original10 columns read visually;paragraphs,pi,choice column headers,5 correction underlines,principle underline,logical blank preserved. Evidence and counterexamples for all choices;boolean32 valuations checked.'},[('2023-03-04',n) for n in range(6,16)],0)
