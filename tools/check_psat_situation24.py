from pathlib import Path
from fractions import Fraction as F
from itertools import product
from datetime import date
import json
from psat_batch_tools import validate,norm
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/situation24'
bank=json.loads((A/'authored-situation24.json').read_text(encoding='utf-8'));own=json.loads((A/'own-solve-and-models.json').read_text(encoding='utf-8'));qs={q['number']:q for q in bank};proof={}
anchors={2:['상인조직을 대표하는 자가','시·도지사의 승인을 받아','기념품 및 지역특산품','3개월 이내에','의견진술의 기회를 주어야','중소벤처기업부장관, 문화체육관광부장관 및 시장 등'],3:['주요 자연지진','알릴 수 있다','국내에 상당한 영향을 미칠 것으로 예상되는','학문연구를 위하여','기상청장의 승인을 받아야'],4:['헌혈증서를 양도받은 사람','그 비용을 해당 의료기관에 보상하여야','헌혈환급예치금으로 헌혈환급적립금','용도에만','채혈부작용이라고 결정된 사람 또는 그 가족'],5:['증축되는 부분의 연면적이 1만 제곱미터','기숙사 및 공공건설임대주택은 제외','국가 및 지방자치단체는 제외','1백분의 70','그 차액을'],6:['국적에 관계없이 한국에서','신청 분야와 활동 분야가 동일한 경우','최초 공연일(희곡 분야에 한함)','지급받은 해의 12월 말일까지'],7:['현재 대기 중의 수증기량을 현재 온도의 포화 수증기량으로 나눈 값','포화 수증기량은 기온이 올라갈수록 증가'],8:['1갤런은 4L, 1마일은 1.6km','15mpg, 8L/100km, 18km/L'],9:['급여이체 계좌는 바꿀 수 없어','40만 원','2,200만 원','70만 원','3,600만 원'],10:['0부터 9까지의 정수','㉠과 ㉡은 같다'],11:['75마리를 팔면','20일 더','100마리 사면','15일 일찍']}
for n,parts in anchors.items():
 for part in parts:assert norm(part) in norm(qs[n]['body']),(n,part)
 proof[str(n)]={'sourceAnchors':parts,'directRationale':own['solutions'][str(n)]['rationale']}
# Legal conditions are read from the provided fictionalized rules, not current-law advice.
assert 12000-7000<10000 and F(30*10000,100)==3000 and F((45-40)*10000*5,1000)==250
proof['5']['exactCalculations']={'extensionSquareMetres':5000,'municipalAmountTenThousandWon':3000,'designDifferenceTenThousandWon':250}
assert date(2015,4,16)<=date(2021,6,30) and date(2020,6,28)<=date(2021,6,30)
proof['6']['eligibilityCutoff']='2021-06-30';proof['6']['publicationDeadline']='2025-12-31'
assert F(60,120)==F(1,2) and F(60,120)/F(60,100)==F(5,6) and F(60,100)*F(8,10)!=F(1,2)
proof['7']['counterexample']={'fixedCurrentWater':60,'saturationBefore':100,'saturationAfter':120,'humidityBeforePercent':60,'humidityAfterPercent':50,'relativeDrop':'1/6','percentagePointDrop':10,'limit':'A fixed numerator is a case,not a consequence of sealed space when evaporation is possible.'}
assert F(120,1)/(15*F(16,10)/4)==20
assert 16*18-16*F(100,8)==88
proof['8']['exactFuelAndGap']=[20,88]
rates=own['models']['9'];assert rates=={'甲':{'A':'57/10','B':'6','C':'49/10'},'乙':{'A':'26/5','B':'9/2','C':'11/2'}}
assert qs[9]['figures'] and not qs[9].get('figuresAfterBody',False)
assert qs[8]['choiceNote']=='㉠ → ㉡' and qs[9]['choiceNote']=='甲 → 乙'
proof['9']['allBankRates']=rates
models=[list(a) for a in product(range(10),repeat=4) if a[0]==a[1] and sum(n%2 for n in a)==a[1] and a.count(1)==a[2] and a.count(2)==a[3]]
assert models==own['models']['10']==[[0,0,0,0],[3,3,1,0]]
assert [int(c) for c in qs[10]['choices'] if int(c) in set(map(sum,models))]==[7]
proof['10']['full10000TupleEnumeration']=models
proof['11']['optionDurationChecks']=[]
for n in [100,200,300,400,500]:
 tSell=F(4*n,15)-20;tBuy=F(3*n,20)+15
 proof['11']['optionDurationChecks'].append({'N':n,'saleImpliedDays':str(tSell),'purchaseImpliedDays':str(tBuy),'both':tSell==tBuy})
assert 300*60==225*80==400*45==18000
for n,truth,answer in [(6,[False,True,False,True],4),(7,[False,True,False],2)]:
 assert [i for i,c in enumerate(qs[n]['choices'],1) if [k in c for k in 'ㄱㄴㄷㄹ'[:len(truth)]]==truth]==[answer]
 proof[str(n)]['truth']=truth
assert [q['answer'] for q in bank]==[own['solutions'][str(q['number'])]['answer'] for q in bank]==[5,5,5,3,4,2,4,4,4,3]
validate('situation24',{'semanticAndModelProof':proof,'keyExposureDisclosure':own['keyExposureDisclosure'],'manualOriginalReview':'All10 source images read;legal titles/paragraphs/items and exception scopes compared;bank table/ceiling/special-rate note kept as original image before native dialogue;choice headers relocated explicitly.'},[('2024-03-02',n) for n in range(2,12)],1)
