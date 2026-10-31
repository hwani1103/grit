from pathlib import Path
import json,subprocess,sys
from psat_batch_tools import validate
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/situation28'
subprocess.run([sys.executable,str(A/'solve.py')],check=True)
bank=json.loads((A/'authored-situation28.json').read_text(encoding='utf-8'));proof=json.loads((A/'model-proof.json').read_text(encoding='utf-8'))
assert [q['answer'] for q in bank]==[4,4,2,4,2,4,3,3,1,1]
for q in bank:assert q['answer']==proof[str(q['number'])]['answer']
assert '1/2박스' in bank[5]['body'] and bank[-1]['figuresAfterBody']
validate('situation28',{'directModelProof':proof,'manualSourceReview':'Read10 originals visually;lawtitles/numbered definitions/dates/speakers/choicecolumns/fraction/calendar retained. Direct all-option evidence;full dice and31calendar days;global attendance upper bound.'},[('2023-03-04',n) for n in range(2,12)],1)
