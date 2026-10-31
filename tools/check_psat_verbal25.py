from pathlib import Path
import subprocess,sys,json
from psat_batch_tools import validate,norm
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/verbal25'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
subprocess.run([sys.executable,str(A/'solve.py')],check=True)
bank=read(A/'authored-verbal25.json');proof=read(A/'model-proof.json');qs={q['number']:q for q in bank}
for q in bank:
 p=proof['questions'][str(q['number'])];assert q['answer']==p['answer']
 if q['number'] in [16,17,18,20,24]:
  assert [i for i,c in enumerate(q['choices'],1) if [k in c for k in 'ㄱㄴㄷ']==p['truth']]==[q['answer']]
 else:
  target=False if q['number']==25 else True
  assert [i for i,t in enumerate(p['truth'],1) if t==target]==[q['answer']]
anchors={16:['언어표현의 의미는','동일한 대상을 지칭한다','인지적 차이가 있다'],17:['위험 대비 이익이 명확히 클 경우에만','약화되지 않는다','뇌에 어떠한 문제도 유발하지 않는다고'],18:['서로 크기가 같고 지구까지 거리가 같은','다른 행성에 의한 식','약 1년'],19:['통제 조건을 충족하더라도 인식 조건은 갖추지 못한','위임 관계에 의존하여'],20:['총괄 관리자만이','전체 프로젝트를 설명할 능력을 갖추고 있지 않다면'],21:['진평왕의 딸 천명부인','진골로서 왕이 된 첫 인물이 아니라는'],22:['원하는 경우','100일 이내','초사 등이 첨부되지 않았다'],23:['실질적인 법안 심의가 어디에서','검토를 의도적으로 늦춤으로써'],24:['가중치는 0보다 큰 값','그 총합은 1이다'],25:['정치적 활동성이 0점인 행동유형','비슷한 수준의 행동지표','위계적 강도']}
for n,parts in anchors.items():
 for p in parts:assert norm(p) in norm(qs[n]['body']),(n,p)
assert qs[19]['body']==qs[20]['body'].split('\n\n<보 기>')[0]
assert len(qs[16]['underlines'])==6
assert '『경국대전』' in qs[22]['body'] and '『경국대전』' in qs[22]['choices'][4]
proof['reviewedSourceAnchors']=anchors
proof['reviewLimit']='Source anchors support transcription; direct semantic review and all five option reasons are separately retained, not replaced by keyword checks.'
validate('verbal25',proof,[('2024-03-02',n) for n in range(16,26)],0)
