from pathlib import Path
import subprocess,sys,json
from psat_batch_tools import validate
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/data24'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
subprocess.run([sys.executable,str(A/'solve.py')],check=True)
proof=read(A/'model-proof.json');bank=read(A/'authored-data24.json')
for q in bank:
 p=proof['questions'][str(q['number'])];assert q['answer']==p['answer']
 if q['number'] in [5,6,8,9,10]:
  truth=p['truth']
  assert [i for i,c in enumerate(q['choices'],1) if [k in c for k in 'ㄱㄴㄷㄹ'[:len(truth)]]==truth]==[q['answer']]
assert '①과 ⑤' in bank[2]['steps'][2] and 'ㄹ이 거짓' in bank[2]['steps'][2]
assert '①과 ④' in bank[6]['steps'][2] and 'ㄹ이 거짓' in bank[6]['steps'][2]
assert len(bank[8]['underlines'])==5
validate('data24',proof,[('2024-03-02',n) for n in range(3,13)],figure_count=29)
