from pathlib import Path
import subprocess,sys,json
from psat_batch_tools import validate,norm
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/situation26'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
subprocess.run([sys.executable,str(A/'solve.py')],check=True)
bank=read(A/'authored-situation26.json');proof=read(A/'model-proof.json');qs={q['number']:q for q in bank}
for q in bank:
 p=proof['questions'][str(q['number'])];assert q['answer']==p['answer']
 if q['number']<=26:assert [i for i,t in enumerate(p['truth'],1) if t]==[q['answer']]
 else:
  values={27:1625,28:10,29:84000,30:2500,31:20}
  assert int(q['choices'][q['answer']-1].replace(',','').replace('원',''))==values[q['number']]
anchors={22:['참전 중 범죄행위','국적을 상실한 경우에도','신청에 따라 현금'],23:['국제선박으로 등록하기 전에','국제선박등록부에 등록','1개월 이내'],24:['특허표시를 할 수 있다','그 행위자를 벌하는 외에','물건의 용기나 포장'],25:['그중 단기로','면허의 유효기간 만료 전 마지막으로','250만 원을 초과할 수 없다'],26:['5～15°C','라거를 생산할 때는 주로 연수'],28:['모든 자리 숫자가 3'],29:['베타는 다른 종류의 열대어와 한 어항에서'],30:['사용포인트를 제외한 금액','속한 달의 말일'],31:['임용 전후 모두 20명','임용 전의 절반']}
for n,parts in anchors.items():
 for p in parts:assert norm(p) in norm(qs[n]['body']),(n,p)
proof['reviewedSourceAnchors']=anchors
proof['sourceTableCells']={'25':['5년','4년','3년','4년'],'27':[[600,75,300],[750,150,600],[1000,200,800],[400,11,60],[350,10,51]],'29':[[3000,400],[3500,500],[4000,300],[900,35000],[1500,40000]],'30':[[50000,5,0],[22000,2,2000],[25000,2,0],[50300,4,300],[10500,5,500]]}
validate('situation26',proof,[('2024-03-02',n) for n in range(22,32)],6)
