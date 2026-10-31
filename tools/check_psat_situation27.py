from pathlib import Path
import json,subprocess,sys
from psat_batch_tools import validate
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/situation27'
subprocess.run([sys.executable,str(A/'solve.py')],check=True)
bank=json.loads((A/'authored-situation27.json').read_text(encoding='utf-8'));models=json.loads((A/'model-proof.json').read_text(encoding='utf-8'))
assert [q['answer'] for q in bank]==[3,4,3,1,2,5,2,5,2,5]
for q in bank:assert q['answer']==models[str(q['number']) if q['number']!=1 else '2023-1']['answer']
assert bank[7]['body'] in bank[8]['body']
assert not bank[5]['body'] and bank[6]['figuresAfterBody']
assert [i for i,c in enumerate(bank[4]['choices'],1) if [x in c for x in 'ㄱㄴㄷㄹ']==[False,False,True,False]]==[2]
validate('situation27',{'directModelProof':models,'manualSourceReview':'All source columns10 read visually;36 rolling table retained;37 full scoring box and case box preserve weights/note;38 conditions native before original case table;39/40 full common text;2023law title/6paragraphs/4items retained.'},[('2024-03-02',n) for n in range(32,41)]+[('2023-03-04',1)],4)
