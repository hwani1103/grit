from pathlib import Path
import json,subprocess,sys
from psat_batch_tools import validate,norm
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/situation25'
subprocess.run([sys.executable,str(A/'solve.py')],check=True)
bank=json.loads((A/'authored-situation25.json').read_text(encoding='utf-8'));model=json.loads((A/'model-proof.json').read_text(encoding='utf-8'));qs={q['number']:q for q in bank}
assert [q['answer'] for q in bank]==[model['questions'][str(q['number'])]['answer'] for q in bank]==[1,5,3,1,3,1,4,2,3,3]
anchors={12:['정확히 1kg','모든 종류의 보석을 하나씩','쪼갤 수 없다'],13:['甲: 戊 우후','甲, 네가 나보다 1살','丙: 乙 이히','戊 이후'],14:['이틀 연속','13일에는 호우경보','11일에 하루 출장','13일에 하루 휴가'],15:['매주 같은 횟수','이튿날은 아침과 점심','점심, 저녁 연달아','한 번도 산책시키지 않으면','매주 수요일','금요일 저녁'],16:['1개의 점수만 제외','최고 득점 업체가 복수'],17:['초급 기술','실적 건수가 가장 많은'],18:['병역이행기간은 연령 계산 시 미산입','①과 ②를 충족','2023. 1. 1.'],19:['나누어지는 값','간접효과와 유발효과를 합쳐','최초 관광지출로 나눈'],20:['50%','10억 원 많으며','2.5'],21:['고등학교에 재학 중인 사람을 포함한다','확인한 후','1천 명 이상','3천만 원 이하']}
for n,parts in anchors.items():
 for part in parts:assert norm(part) in norm(qs[n]['body']),(n,part)
assert qs[14]['choiceNote']=='최솟값 → 최댓값' and qs[20]['choiceNote']=='직접효과 → 비율승수'
assert '제◇◇조(벌칙)\n\n①' in qs[21]['body']
assert not qs[13].get('figuresAfterBody',False)
for n in [12,16,17,18]:assert qs[n]['figuresAfterBody']
assert [i for i,c in enumerate(qs[19]['choices'],1) if [x in c for x in 'ㄱㄴㄷ']==[False,False,True]]==[2]
validate('situation25',{'directModels':model,'sourceAnchors':anchors,'originalReview':'All10 source columns read;19/20 shared passage kept whole;9 original figures retain conditions,table headers and units;21 legal heading◇ and clauses separated;weekly maximum proof does not assume identical weekly schedules.'},[('2024-03-02',n) for n in range(12,22)],9)
