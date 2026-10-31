"""Eight explicit prose transcriptions, with frozen assessments before edits."""
from pathlib import Path
import datetime,hashlib,json
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/psat_remaining605_20261030';B=OUT/'batch15'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
now=lambda:datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).isoformat()
old={x['question']['id']:x['question'] for x in read(B/'revealed-current.json')}
assert not (B/'ratings-before.json').exists() and not (OUT/'changes-batch15.json').exists()
assessments=[
('두 분류의 같은 전체를 확인한 교집합 하한92와 달성 가능한 교차표, 2022년 장식 증가·전광판 감소, 85% 경계를 모두 확인했다. 게시 해설은 정확하며 초벌 자체풀이의 열 머리글 오독은 별도 정정한다.','발견 없음. 자체풀이 오류를 게시 결함으로 돌리거나 수정 전 점수를 바꾸지 않는다.',False),
('누적 차이로 8월285·12월320, 3·4월 합586을 구한다. 9~12월 네 달과 미지 두 달 중 적어도 한 달이 연평균을 초과한다. 정확히 다섯 달이라고 단정하지 않는 한계도 적절하다.','보기 세 문장이 이미지로 축소되어 기본 화면에서 작다. 자료표와 정의는 유지하고 보기만 본문 글자로 전환한다.',True),
('B 비중 증가폭과 사업비654, 인건비 60% 기준 및 C 실제금액의 분리된 상하한을 확인했다. 반올림 오차 ±0.05%p를 허용해도 C 증가가 유지된다.','보기의 작은 이미지 글자를 본문으로 전환하고 ㄷ도각·C실제의 단어 경계를 고친다.',True),
('전체 응시463486와 미응시59184로 접수522670, 재학생 미응시 증감−956을 얻는다. 남은 B18082/E422와 총 미응시 증감−534도 일치한다.','보고서가 작은 이미지다. 보고서를 원래처럼 자료 앞 본문으로 표시하고 흐름도·주석은 원형 유지한다.',True),
('공통 세 표를 확인해 ㄱ의 반대 방향과 갈치 두 주 합29700>25500을 증명한다. 원문 부호 비교 답②와 사전 명시한 절댓값 대안⑤를 구분하며 기존 앱 보완조건에서 공식⑤가 성립한다.','보기 이미지 글자를 본문으로 전환한다. 기존 보완조건을 그대로 유지하고 원문 자체가 절댓값을 명시했다고 표현하지 않는다.',True),
('소매−도매 차이7400/12100/3800과 구매량으로 절감액85600/90300/80900/72600/64300을 확인했다. 동일 총량 대체 경로와 공식②가 정확하다.','발견 없음. 공통 세 표와 주석은 원형으로 유지한다.',False),
('배점10/20/70과 각 부문 반올림 순서를 확인했다. 독일 논문112는 기술51.0<프랑스51.1, 배점 교환에서 대만55.2>이스라엘53.9로 ㄱ만 참이다.','산정 방법과 보기의 이미지 문장이 작다. 두 글 블록을 본문으로 묶고 자료표·반올림 주석은 그대로 표시한다. 본문을 자료 앞에 두는 순서 변경을 기록한다.',True),
('구간41~50의 고소득7개와 111~133의 비저소득15개, 필리핀보다 앞선 중소득9개를 확인했다. 미제시 국가의 순위를 무조건 가정하지 않는 풀이가 타당하다.','보기 이미지 문장을 본문으로 전환한다. 그룹별 순위·전체 집단 크기·동순위 없음 주석을 그대로 유지한다.',True),
('ㄱ 교통사망 추세와 ㄷ 전체사망 추세만 보고서 근거가 된다. ㄴ 연속등급과 ㄹ 전년 전체센터는 2019 단년도·대형 지역 순위를 뒷받침하지 못한다.','보고서 문단이 작은 이미지다. 본문을 자료 앞에 표시하되 표와 보기 네 자료의 상대 순서·형태는 유지한다.',True),
('총규모27001·현재15350·2007년10월 활동4개를 각각 분리해 검산했다. 최장·최단·수단과 코모로 각각 두 임무단도 일치한다.','보고서의 긴 이미지 문장과 다섯 밑줄을 원문 범위대로 본문에 옮긴다. ㉢ 밑줄 뒤의 현재 인원 문장은 밑줄에 추가하지 않는다.',True)]
ratings=[dict(id=qid,scoreBeforeFix=4 if a[2] else 5,assessment=a[0],deduction=a[1],needsChange=a[2]) for qid,a in zip(old,assessments)]
assert sum(r['scoreBeforeFix'] for r in ratings)==42
write(B/'ratings-before.json',dict(method='Same-author pre-edit individual assessment after fresh source solve and host-before review. Published errors and own-solve errors distinguished.',ratings=ratings))
write(B/'ratings-frozen.json',dict(frozenAt=now(),ratingsSha256=hashlib.sha256((B/'ratings-before.json').read_bytes()).hexdigest(),total=42,count=10,beforeChanges=True))
spec={
'kr-mpm-2025-07-19-psat-d-19':dict(remove=[1],body='보기\n\nㄱ. 8월 물동량은 7월 물동량보다 많다.\n\nㄴ. 1월 대비 12월 물동량의 증가율은 15% 이상이다.\n\nㄷ. 2023년 월평균 물동량보다 물동량이 많은 달은 5개 이상이다.'),
'kr-mpm-2025-07-19-psat-d-20':dict(remove=[2],body='보기\n\nㄱ. 2018～2023년 동안 공공기관 예산액 중 B의 예산액 비중은 매년 1%p 이상 증가하였다.\n\nㄴ. 2023년 A는 사업비가 출연금의 3배 이상이다.\n\nㄷ. 2021～2023년 동안 A는 매년 인건비가 일반관리비의 60% 이상이다.\n\nㄹ. 2022년 C의 예산액은 전년 대비 증가하였다.'),
'kr-mpm-2025-07-19-psat-d-21':dict(remove=[0],afterBody=True,body='보고서\n\n2024학년도 대학입학시험 응시 현황을 살펴보면, 응시원서 접수 인원은 504,588명이었고, 응시 인원은 그중 88.2%에 해당하는 444,870명이었다. 응시원서 접수 인원 중 ‘재학생’은 326,646명, ‘졸업생 및 검정고시학력 인정자’는 177,942명이었다. 응시 인원 중 ‘재학생’은 287,502명, ‘졸업생 및 검정고시학력 인정자’는 157,368명으로, 각각 응시 인원의 64.6%, 35.4%를 차지하였다.'),
'kr-mpm-2025-07-19-psat-d-22':dict(remove=[3],body='보기\n\nㄱ. 냉동 고등어 가격의 전주 대비 증감 방향은 A도매점과 B소매점이 동일하다.\n\nㄴ. 냉장 수산물 중 1주 가격 대비 3주 가격 증감률이 가장 큰 어종은 A도매점과 B소매점이 동일하다.\n\nㄷ. A도매점이 B소매점보다 주별 냉동 갈치 가격이 높은 주가 있다.'),
'kr-mpm-2025-07-19-psat-d-24':dict(remove=[0,2],afterBody=True,body='국가별 기술점수 산정 방법\n\n○ 해당 국가의 원점수는 ‘논문’, ‘특허’, ‘전문가 평가’ 3가지 부문별로 집계한다.\n\n○ 해당 국가의 변환점수는 3가지 부문별로 다음과 같이 산출한다.\n－ 해당 부문에서 원점수가 가장 높은 국가 원점수 대비 해당 국가 원점수의 비율을 구한다.\n－ 위 비율에 해당 부문 배점을 곱하여 변환점수를 산출한다.\n(단, 3가지 부문 배점의 합은 100점임)\n\n○ 해당 국가의 기술점수는 3가지 부문 변환점수를 합하여 산정한다.\n\n보기\n\nㄱ. ‘전문가 평가’ 부문 배점은 ‘논문’과 ‘특허’ 부문 배점 합의 2배 이상이다.\n\nㄴ. 독일의 ‘논문’ 부문 원점수만 50점 증가한다면, 기술점수는 독일이 프랑스보다 높아진다.\n\nㄷ. ‘논문’과 ‘특허’ 부문 배점이 서로 바뀐다면, 기술점수는 이스라엘이 대만보다 높아진다.'),
'kr-mpm-2025-07-19-psat-d-25':dict(remove=[1],body='보기\n\nㄱ. GII 순위가 스위스보다 낮고 중국보다 높은 국가는 모두 고소득그룹 국가이다.\n\nㄴ. GII 순위 41위부터 50위까지 국가 중 고소득그룹 국가 수는 7개이다.\n\nㄷ. 마다가스카르보다 GII 순위가 낮으면서 저소득그룹이 아닌 국가 수는 14개이다.\n\nㄹ. 중상소득그룹과 중저소득그룹을 중소득그룹으로 묶으면, 필리핀의 중소득그룹 내 순위는 10위이다.'),
'kr-mpm-2021-07-10-psat-d-01':dict(remove=[1],afterBody=True,body='보고서\n\n2019년 생활안전 통계에 따르면 전국 473개소의 안전체험관이 운영 중인 것으로 확인되었다. 전국 안전체험관을 규모별로 살펴보면, 대형이 32개소, 중형이 7개소, 소형이 434개소였다. 이 중 대형 안전체험관은 서울이 가장 많고 경북, 충남이 그 뒤를 이었다.\n\n전국 안전사고 사망자 수는 2015년 이후 매년 감소하다가 2018년에는 증가하였다. 교통사고 사망자 수는 2015년 이후 매년 줄어들었고, 특히 2018년에 전년 대비 11.2% 감소하였다.\n\n2019년 분야별 지역안전지수 1등급 지역을 살펴보면 교통사고 분야는 서울, 경기, 화재 분야는 광주, 생활안전 분야는 경기, 부산으로 나타났다.'),
'kr-mpm-2021-07-10-psat-d-02':dict(remove=[1],body='보고서\n\n아프리카연합은 아프리카 지역 분쟁 해결 및 평화 구축을 위하여 2021년 5월 현재까지 9개의 임무단을 구성하고 평화유지활동을 주도하였다. ㉠평화유지활동 중 가장 오랜 기간 동안 활동한 임무단은 ‘소말리아 임무단’이다. 이 임무는 소말리아 과도 연방정부가 아프리카연합에 평화유지군을 요청한 것을 계기로 시작되어 현재에 이르고 있다. 한편, ㉡‘코모로 선거감시 지원 임무단’은 가장 짧은 기간 동안 활동하였다. 2006년 코모로는 대통령 선거를 앞두고 아프리카연합에 지원을 요청하였고 같은 해 3월 시작된 평화유지활동은 선거가 끝난 6월에 임무가 종료되었다.\n\n㉢아프리카연합이 현재까지 평화유지활동을 위해 파견한 임무단의 총규모는 25,000명 이상이며, 현재 활동 중인 임무단의 규모는 소말리아 6,000명, 수단 6,000명, 우간다 3,350명으로 총 15,000여 명이다.\n\n아프리카연합은 아프리카 내의 문제를 자체적으로 해결하기 위해 다양한 임무단 활동을 활발히 수행하였다. 특히 ㉣수단과 코모로에서는 각각 2개의 임무단이 활동하였다.\n\n현재 평화유지활동을 수행 중인 임무단은 3개이지만 ㉤2007년 10월 기준 평화유지활동을 수행 중이었던 임무단은 5개였다.')}
changes=[]
for path in (ROOT/'assets/psat').glob('*.json'):
 data=read(path)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  if q['id'] not in spec:continue
  previous=old[q['id']];assert q==previous
  snapshot=OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snapshot.exists();write(snapshot,previous)
  s=spec[q['id']];q['body']=s['body'];q['figures']=[f for i,f in enumerate(previous['figures']) if i not in s['remove']]
  if s.get('afterBody'):q['figuresAfterBody']=True
  if q['id']=='kr-mpm-2025-07-19-psat-d-20':
   q['steps'][2]=q['steps'][2].replace('ㄷ도각','ㄷ도 각');q['optionReasons'][3]=q['optionReasons'][3].replace('C실제','C 실제')
  if q['id']=='kr-mpm-2021-07-10-psat-d-02':
   q['underlines']=['㉠평화유지활동 중 가장 오랜 기간 동안 활동한 임무단은 ‘소말리아 임무단’이다.','㉡‘코모로 선거감시 지원 임무단’은 가장 짧은 기간 동안 활동하였다.','㉢아프리카연합이 현재까지 평화유지활동을 위해 파견한 임무단의 총규모는 25,000명 이상이며,','㉣수단과 코모로에서는 각각 2개의 임무단이 활동하였다.','㉤2007년 10월 기준 평화유지활동을 수행 중이었던 임무단은 5개였다.'];q['underlineLabelAnchors']=True
  q['editNote']+=' 보기·보고서·산정 방법의 문장은 본문 글자로 표시하고, 표·그래프·수식·단위·주석·범례는 원형으로 유지한다. 원문 보기에서 전체 배치를 확인할 수 있다.'
  q['revision']+=1;touched=True
  changes.append(dict(id=q['id'],file=path.relative_to(ROOT).as_posix(),oldRevision=previous['revision'],newRevision=q['revision'],changedFields=sorted(k for k in q.keys()|previous.keys() if k!='revision' and q.get(k)!=previous.get(k)),beforeSnapshot=snapshot.relative_to(ROOT).as_posix(),reason='글 블록의 본문 표시·원문 밑줄 복원과 단어 경계 개선. 데이터 그림·선지·정답·원문 이미지·기존 보완조건 보존.',status='repaired_pending_reverification'))
 if touched:write(path,data)
assert len(changes)==8
write(OUT/'changes-batch15.json',changes)
write(B/'native-prose-transcriptions.json',dict(status='implemented_pending_verification',transcriptions=spec,dataFiguresRelativeOrderPreserved=True,proseBeforeData=['kr-mpm-2025-07-19-psat-d-21','kr-mpm-2025-07-19-psat-d-24','kr-mpm-2021-07-10-psat-d-01'],originalWholeReadingOrderChangedFor24And2021d01=True,allOriginalAssetsRetained=True,uiCodeChanged=False))
print('Frozen 42/50 before repairs; revised eight prose blocks; data images and existing d22 condition preserved.')
