import itertools
from fractions import Fraction as F
import review_remaining605 as r
b=r.folder(61);assert not (b/'own-solves.json').exists()
rows=[
(2,'정의 예측이 참이면 갑은 환경부이므로 무의 예측이 거짓이다. 그런데 갑·을의 예측을 모두 참으로 두면 을 환경부→병 통일부가 되어 정의 병 비통일부와 충돌한다. 따라서 정만 거짓이고 나머지 네 예측은 참이다. 무의 예측으로 갑 통일부·정 교육부, 갑 비환경부와 병의 예측으로 병·무 통일부가 확정된다. 을은 어느 부처도 가능하여②만 반드시 참은 아니다. 각 사람의 배치는 하나지만 여러 사람이 같은 부처에는 가능하다.', ['무의 참인 예측이 갑 통일부 배치를 직접 보장한다.','을은 환경부 또는 다른 부처여도 네 참 한 거짓이 성립하여 필연은 아니다.','갑이 환경부가 아니므로 병의 참인 예측에 따라 병 통일부다.','무의 참인 예측의 두 번째 성분으로 정 교육부가 확정된다.','갑 비환경부에서 병의 예측으로 무 통일부도 동시에 확정된다.']),
(5,'중점P·협의C·예산B·장기L·재배치R·즉시I로 쓰면 P→¬R,C→¬I,L∧¬C→R,R→¬B이다. ㄱ은 L∧I→¬C→R→¬B로 참. ㄴ은 존재하는 P∧L 사례에서 ¬R이므로 C가 필요하며 그 결과 ¬I라서 존재한다. ㄷ은 존재하는 B∧I 사례에서 ¬R·¬C이며 L이면 R모순이므로 ¬L이다. 존재를 보장하는 두 문장을 따로 증인으로 써서ㄴㄷ을 도출한다. 세 보기 모두 참⑤.', ['ㄱ뿐 아니라 중점장기 증인의 ㄴ과 예산즉시 증인의 ㄷ도 참이다.','예산즉시 증인으로 ㄷ은 맞지만 ㄱ과 ㄴ을 누락했다.','ㄱㄴ은 맞으며 예산즉시 과제가 장기일 수 없어 ㄷ도 참이다.','ㄴㄷ뿐 아니라 장기즉시라면 재배치가 필요해 예산은 불가능하므로 ㄱ도 참이다.','전칭 추론 ㄱ과 명시적 존재 증인에서 나온 ㄴㄷ이 모두 성립한다.']),
(4,'정확한 지수를 ABC라 두면 첫 오류는 A를6/5배, 두 번째 계산은 그 오류를 유지한 채 B를4/5배 한다. 결과는24/25 ABC이므로 정확한 값보다1/25작다. 그 차가3이므로 ABC=75다. A=B라는 조건은 각각 더하고 빼는 양이 같다는 오해의 원인이지 곱이 유지되는 근거가 아니다. 앞의 A증가를 취소한 것으로 읽지 않고 동일하게 유지한다. 선택지별4%차를 검산하면75만3이다.', ['66의25분의1은2.64이므로 차3을 만들지 못한다.','69의25분의1은2.76으로 조건의 차3과 다르다.','72는75에24/25를 곱한 잘못 계산된 결과이지 정확한 지수가 아니다.','75에서24/25인72를 빼면3으로 조건이 성립한다.','84의25분의1은3.36으로 주어진 차3보다 크다.']),
(1,'2019인구2739372에서3년간 매년1명 이상600명 이하 증가하므로2022는2739375~2741172이다. 이 구간의 좌우대칭7자리 정수는2740472하나뿐이며 천의 자리는0이다. 직전대칭2739372는증가조건 위반, 다음2741472는2100명 증가로1800상한 초과다. 후보2740472는1100증가이므로366·366·368명으로 매년조건을 만족한다. 대칭수의 자릿수올림을 전체인구1000증가로 오해하지 않는다.', ['가능한 유일 대칭수2740472의 천의 자리는0이다.','천의 자리1인 다음 대칭수2741472는2100명 증가라 상한1800을 넘는다.','천의 자리2인2742472는3100명 증가라 허용되지 않는다.','천의 자리3인2743472는4100명 증가라 허용되지 않는다.','천의 자리4인2744472는5100명 증가라 허용되지 않는다.']),
(2,'2021상위10업종의2017대비 증감폭은 순서대로8580,7086,6683,1717,1988,241,−1605,−626,−659,−427이다.②는 감소한 운송·교육·여가·제조를 양수로 그리고 일부 업종 크기도 바꿔 틀렸다.①은 각 연도 남녀 원표와 일치.③여성증가율−3.4,16.4,.2,−13.9%가 반올림 일치.④상위10남103465/160715=64.4%,여35.6%.⑤상위3각 업종 내부 남성비59.9,76.2,74.2%라 맞다.⑤의 분모는상위3합계가 아니라 각 업종합계이다.', ['다섯 연도 남성·여성 건수의 두 계열이 표1의 수치를 그대로 나타낸다.','운송5517−7122=−1605 등 감소를 양수로 표시해 원자료와 부합하지 않는다.','전년도 여성 건수를 분모로 한 네 증감률이 표시된 소수첫째자리와 일치한다.','상위10합160715 중 남103465·여57250의 구성비64.4·35.6퍼센트다.','각 업종 합계로 남녀를 나누면 남성59.9·76.2·74.2퍼센트로 그림과 맞다.'])]
models=[]
for a,e,c,d,m in itertools.product(range(4),repeat=5):
 pred=[a!=0 or e==0,e!=0 or c==1,a==0 or (m==1 and c==1),c!=1 and a==0,a==1 and d==2]
 if sum(pred)==4:models.append([a,e,c,d,m])
assert models==[[1,j,1,2,1] for j in range(4)]
types=[]
for p,c,budget,l,rr,i in itertools.product([False,True],repeat=6):
 if (not p or not rr) and (not c or not i) and (not l or c or rr) and (not rr or not budget):types.append((p,c,budget,l,rr,i))
assert all(not(l and i) or not budget for p,c,budget,l,rr,i in types)
w1=[v for v in types if v[0] and v[3]];w2=[v for v in types if v[2] and v[5]]
assert w1 and w2 and all(not v[4] and not v[5] for v in w1) and all(not v[3] for v in w2)
pal=[n for n in range(2739375,2741173) if str(n)==str(n)[::-1]];assert pal==[2740472]
delta=[a-c for a,c in zip([50703,38514,24706,11662,10162,10064,5517,5493,2430,1464],[42123,31428,18023,9945,8174,9823,7122,6119,3089,1891])];assert delta==[8580,7086,6683,1717,1988,241,-1605,-626,-659,-427]
female=[78119,75457,87797,87998,75730];growth=[round(100*(y-x)/x,1) for x,y in zip(female,female[1:])];assert growth==[-3.4,16.4,.2,-13.9]
assert round(100*103465/160715,1)==64.4 and [round(100*x/y,1) for x,y in zip([30352,29352,18341],[50703,38514,24706])]==[59.9,76.2,74.2]
r.write(b/'pre-reveal-exact-models.json',dict(status='PASS',assignments=models,validPredicateTypes=types,priorityLongWitnesses=w1,budgetImmediateWitnesses=w2,workFactor=str(F(6,5)*F(4,5)),workIndex=75,palindromes=pal,feasibleAnnualGrowth=[366,366,368],startupDifferences=delta,femaleGrowth=growth))
r.write(b/'own-solves.json',[dict(id=q['id'],answer=a,reasoning=s,optionReasons=o) for q,(a,s,o) in zip(r.batch(61),rows)])
r.write(b/'sample.json',dict(sample=[dict(id=q['id']) for q in r.batch(61)]));print('Own5 frozen before current reveal;2 historical exposure disclosures preserved')
