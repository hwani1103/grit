from pathlib import Path
import subprocess,sys,json
from psat_batch_tools import validate
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/data23'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
subprocess.run([sys.executable,str(A/'solve.py')],check=True)
bank=read(A/'authored-data23.json');proof=read(A/'model-proof.json');keys=read(A/'official-key-comparison.json')
for q in bank:assert q['answer']==keys[q['examDate'][:4]][str(q['number'])]
for year,n,truth in [(2025,37,[True,False,True,False]),(2025,39,[True,False,True,False]),(2025,40,[True,True,True]),(2024,1,[True,True,False])]:
 q=next(q for q in bank if q['examDate'].startswith(str(year)) and q['number']==n)
 assert [i for i,c in enumerate(q['choices'],1) if [k in c for k in 'ㄱㄴㄷㄹ'[:len(truth)]]==truth]==[q['answer']]
held={q['id'] for q in read(A/'held-candidates.json')['held']};assert not held&{q['id'] for q in bank}
proof['heldCandidates']=sorted(held)
validate('data23',proof,[('2025-03-08',n) for n in [32,33,35,36,37,38,39,40]]+[('2024-03-02',1),('2024-03-02',2)],figure_count=27)
