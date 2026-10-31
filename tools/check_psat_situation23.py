from pathlib import Path
import json,subprocess,sys
from psat_batch_tools import validate,norm
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/situation23'
subprocess.run([sys.executable,str(A/'solve.py')],check=True)
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
bank=read(A/'authored-situation23.json');own=read(A/'own-solve-before-key.json');proof=read(A/'model-proof.json')
for q in bank:
 k=f'{q["examDate"][:4]}-{q["number"]}';assert q['answer']==own[k]['answer']
for idx,truth in [(0,[False,True,True]),(7,[True,True,False,False])]:
 q=bank[idx];letters='ㄱㄴㄷㄹ'[:len(truth)]
 assert [i for i,c in enumerate(q['choices'],1) if [k in c for k in letters]==truth]==[q['answer']]
assert bank[7]['body'].split('<보 기>')[0].strip()==bank[8]['body'].split('<상 황>')[0].strip()
assert all(bank[i]['figuresAfterBody'] for i in range(3,7))
assert '이하 이 조에서 같다' in bank[-1]['body']
assert '제00조(공공데이터의 제공 운영실태 평가)\n\n①' in bank[-1]['body']
selection=[('2025-03-08',n) for n in range(32,41)]+[('2024-03-02',1)]
validate('situation23',proof,selection,figure_count=4)
