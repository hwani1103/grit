from pathlib import Path
import subprocess,sys,json
from psat_batch_tools import validate,norm
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/verbal26'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
subprocess.run([sys.executable,str(A/'solve.py')],check=True)
bank=read(A/'authored-verbal26.json');proof=read(A/'model-proof.json');qs={q['number']:q for q in bank}
for q in bank:
 p=proof['questions'][str(q['number'])];assert q['answer']==p['answer']
 if q['number']>=32:assert [i for i,c in enumerate(q['choices'],1) if [k in c for k in 'ㄱㄴㄷ']==p['truth']]==[q['answer']]
 else:assert [i for i,t in enumerate(p['truth'],1) if t==(q['number'] not in [29,30])]==[q['answer']]
anchors={26:['—12.5°C','온도가 변하더라도 하전이 되지 않는','그렇게 하전된 이후에도'],27:['항상 함께 일어난다','3분의 2 이상의 세포'],28:['따라 나오지는 않는다','운동피질이 활성화된다면'],29:['정당한 보상을 위해서 업무 평가를 진행하는 것이 아니다','자기 상황에 맞춰'],30:['인간이 연구 대상자가 되는','직접적인 연관이 없을지라도'],31:['각각 검출기 하나가 손상되어','Y와 Z는 구분할 수 있었던 반면'],32:['비행 능력에 영향을 주지 않는다는','표적 식별에는 영향을 주지 못한다는'],33:['총무과에는 한 명만','그런 경우는 없다'],34:['가은은 내과에 합격하였다','세 명의 예측은 옳고'],35:['가난한 사람으로부터 부자에게로','사회의 모든 영역에서']}
for n,parts in anchors.items():
 for p in parts:assert norm(p) in norm(qs[n]['body']),(n,p)
assert len(qs[27]['underlines'])==5 and len(qs[32]['underlines'])==3
assert qs[26]['choiceNote']=='선택지의 순서: (가) → (나) → (다)'
proof['reviewedSourceAnchors']=anchors
proof['reviewLimit']='Anchors are transcription checks, not semantic scoring;all options and proof/limits directly reviewed.'
validate('verbal26',proof,[('2024-03-02',n) for n in range(26,36)],0)
