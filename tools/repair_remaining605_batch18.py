"""Explicit prose-only transcriptions after original visual and fresh-solve review."""
from pathlib import Path
import datetime,hashlib,json
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/psat_remaining605_20261030';B=OUT/'batch18'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
now=lambda:datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).isoformat()
old={x['question']['id']:x['question'] for x in read(B/'revealed-current.json')}
assert not (B/'ratings-before.json').exists() and not (OUT/'changes-batch18.json').exists()
assessments=[
('두선차 금융비율과GDP곱 실제채무액을 분리해ㄱㄷ이다. 매년증가·매년절반 두전칭을2019/2017반례로제외하면②가유일한중단기준도정확하다.','보기 네 문장을 본문 글자로 전환한다. 두그래프의 축·범례·국가채무 정의는 그대로 유지한다.'),
('재작업100에서폐기50/조립합류50,검사950에서폐기190으로합240이며출하760과합1000이다. 분기별분모·재작업방향·보존식과오답230의원인까지정확하다.','발견 없음. 도식과 분수 정의·예시를 원형 유지한다.'),
('국어평균81/총점차35/가중점수丁91과丙성별양쪽모형을검산해ㄱㄷㄹ이다. 미정성별자체를알필요없는풀이와같은개수평균의합계비교가타당하다.','보기 문장이 작게 표시되어 본문 글자로 전환한다. 성별 빈칸과 과목별 점수표는 유지한다.'),
('2023비중12.1과2027규모>3500,AI성장>250%·시스템성장0~50%로ㄱㄴㄷ이다. 표시비중 오차±0.05%p를허용한경계도유지된다.','보기 본문 전환과 해설의 연도·증가율 단어 경계를 개선하고, 사용한 안전경계가 반올림오차에서도 유지됨을 명시한다.'),
('출발행합/도착열합과대각선상쇄를구분하여A/B/D세곳,C외부합687·절대차15최소,G도착·내부출발비중최대다. 8×8모든셀과행열합을원문에서검산한다.','보기의 작은 이미지 문장을 본문으로 전환한다. 데이터 표·대각선·합계·주석은 원형 유지한다.'),
('증감B−106으로세종,A요원대비1.8미만으로충남,D외국인비중45%초과로대전을정해C충북/D대전②다. 요원부담과외국인비중의분모를구분하고현재값·증감을혼동하지않는다.','대화 전체를 본문 글자로 옮긴다. 표·산식과 C→D 선택지 순서를 보존한다.'),
('네나라원조액합31.4십억하한·29국전체172.5상한·독일증액후비율.686%로ㄱㄴ이다. 미제시14국을0으로두지않고금액단위도환산한다.','보기 본문 전환과 단위 십억/보기의 억의 경계를 고친다. 독일의 반올림 오차에도.70%미만임을 명시한다.'),
('모든달사상자>사고2배와총합7472/3218,최소492<최대841의60%로ㄱㄴ이다. 잔여비중22.9<7×3.4와65.25%최소경계에서도불이행사고>2000을확인한다.','보기 본문 전환으로 글자를 읽기 쉽게 한다. 세그래프의수치·범례·주석과 비율의 합계 기준은 유지한다.'),
('58.5≤가<65.7,나최저,다체육시설4위,라≥92.5를실제후보에적용해④유일이다. 더낮다의부정에등호를포함하며동률일반규칙을임의추가하지않는다.','정보 네 문장을 본문으로 전환한다. 일곱 지표의 표·빈칸과 가→나→다→라 선택지 순서는 유지한다.'),
('국공립881감소/사립1463증가와카드47/196약24%로㉡㉢을제외하고㉠증가폭·㉣공공납부현황을대조해③이다. 표의역연도순서·분모·수용률과인원의차이를확인했다.','긴 보고서를 본문으로 전환하며 원문 네 밑줄과 틀린 진술 자체를 그대로 보존한다. 해설의 으로약 단어 경계를 고친다.')]
ratings=[dict(id=qid,scoreBeforeFix=5 if old[qid]['number']==5 else 4,assessment=a,deduction=d,needsChange=old[qid]['number']!=5) for qid,(a,d) in zip(old,assessments)]
assert sum(r['scoreBeforeFix'] for r in ratings)==41
write(B/'ratings-before.json',dict(method='Same-author pre-edit individual source/choice assessment; original images and all10 default screens reviewed.',ratings=ratings));write(B/'ratings-frozen.json',dict(frozenAt=now(),ratingsSha256=hashlib.sha256((B/'ratings-before.json').read_bytes()).hexdigest(),total=41,count=10,beforeChanges=True))
spec={
3:dict(body='보기\n\nㄱ. 2020년 국가채무는 2014년의 1.5배 이상이다.\n\nㄴ. GDP 대비 금융성채무 비율은 매년 증가한다.\n\nㄷ. 적자성채무는 2019년부터 300조 원 이상이다.\n\nㄹ. 금융성채무는 매년 국가채무의 50% 이상이다.'),
7:dict(body='보기\n\nㄱ. 국어 평균 점수는 80점 이상이다.\n\nㄴ. 3개 과목 평균 점수가 가장 높은 학생과 가장 낮은 학생의 평균 점수 차이는 10점 이하이다.\n\nㄷ. 국어, 영어, 수학 점수에 각각 0.4, 0.2, 0.4의 가중치를 곱한 점수의 합이 가장 큰 학생은 ‘정’이다.\n\nㄹ. ‘갑’～‘무’의 성별 수학 평균 점수는 남학생이 여학생보다 높다.'),
8:dict(body='보기\n\nㄱ. 인공지능반도체 비중은 매년 증가한다.\n\nㄴ. 2027년 시스템반도체 시장규모는 2021년보다 1,000억 달러 이상 증가한다.\n\nㄷ. 2022년 대비 2025년의 시장규모 증가율은 인공지능반도체가 시스템반도체의 5배 이상이다.'),
9:dict(body='보기\n\nㄱ. 도착 화물보다 출발 화물이 많은 지역은 3개이다.\n\nㄴ. 지역 내 이동 화물이 가장 적은 지역은 도착 화물도 가장 적다.\n\nㄷ. 지역 내 이동 화물을 제외할 때, 출발 화물과 도착 화물의 합이 가장 작은 지역은 출발 화물과 도착 화물의 차이도 가장 작다.\n\nㄹ. 도착 화물이 가장 많은 지역은 출발 화물 중 지역 내 이동 화물의 비중도 가장 크다.'),
10:dict(body='대화\n\n갑: 감염병 확산에 대응하기 위한 회의를 시작합시다. 오늘은 대전, 세종, 충북, 충남의 4월 4일 기준 자가격리자 및 모니터링 요원 현황을 보기로 했는데, 각 지자체의 상황이 어떤가요?\n\n을: 4개 지자체 중 세종을 제외한 3개 지자체에서 4월 4일 기준 자가격리자가 전일 기준 자가격리자보다 늘어났습니다.\n\n갑: 모니터링 요원의 업무 부담과 관련된 통계자료도 있나요?\n\n을: 4월 4일 기준으로 대전, 세종, 충북은 모니터링 요원 대비 자가격리자의 비율이 1.8 이상입니다.\n\n갑: 지자체에 모니터링 요원을 추가로 배치해야 할 것 같습니다. 자가격리자 중 외국인이 차지하는 비중이 4개 지자체 가운데 대전이 가장 높으니, 외국어 구사가 가능한 모니터링 요원을 대전에 우선 배치하는 방향으로 검토해 봅시다.'),
12:dict(body='보기\n\nㄱ. 국민총소득 대비 공적개발원조액 비율이 UN권고 비율보다 큰 국가의 공적개발원조액 합은 250억 달러 이상이다.\n\nㄴ. 공적개발원조액 상위 5개국의 공적개발원조액 합은 개발원조위원회 29개 회원국 공적개발원조액 합의 50% 이상이다.\n\nㄷ. 독일이 공적개발원조액만 30억 달러 증액하면 독일의 국민총소득 대비 공적개발원조액 비율은 UN권고 비율 이상이 된다.'),
16:dict(body='보기\n\nㄱ. 월별 교통사고 사상자는 가장 적은 달이 가장 많은 달의 60% 이하이다.\n\nㄴ. 2020년 교통사고 건당 사상자는 1.9명 이상이다.\n\nㄷ. ‘안전거리 미확보’가 사고원인인 교통사고 건수는 ‘중앙선 침범’이 사고원인인 교통사고 건수의 7배 이상이다.\n\nㄹ. 사고원인이 ‘안전운전의무 불이행’인 교통사고 건수는 2,000건 이하이다.'),
17:dict(body='정보\n\n○ 재정자립도가 E보다 높은 지역은 A, C, F임.\n\n○ 시가화 면적 비율이 가장 낮은 지역은 주택노후화율이 가장 높은 지역임.\n\n○ 10만 명당 문화시설수가 가장 적은 지역은 10만 명당 체육시설수가 네 번째로 많은 지역임.\n\n○ 주택보급률이 도로포장률보다 낮은 지역은 B, C, D, F임.'),
18:dict(body='보고서\n\n2020년 대학 기숙사 수용률은 22.4%로, 2019년의 22.2%에 비해 증가하였지만 여전히 20%대 초반에 그쳤다. 대학유형별 기숙사 수용률은 사립대학보다는 국공립대학이 높고, 수도권 대학보다는 비수도권 대학이 높았다. 한편, ㉠2019년 대비 2020년 대학유형별 기숙사 수용률은 국공립대학보다 사립대학이, 비수도권대학보다 수도권대학이 더 큰 폭으로 증가하였다.\n\n2020년 대학 기숙사 수용가능 인원의 변화를 설립주체별로 살펴보면, ㉡국공립대학은 전년 대비 800명 이상 증가하였으나, 사립대학은 전년 대비 1,400명 이상 감소하였다. 소재지별로 살펴보면 수도권 대학의 기숙사 수용가능 인원은 2019년 119,940명에서 2020년 122,099명으로 2,100명 이상 증가하였으나, 비수도권 대학은 2019년 234,227명에서 2020년 232,650명으로 1,500명 이상 감소하였다.\n\n2020년 대학 기숙사비 납부 방식을 살펴보면, ㉢전체 대학 중 기숙사비 카드납부가 가능한 대학은 37.9%에 불과하였다. 이를 기숙사 유형별로 자세히 보면, ㉣카드납부가 가능한 공공기숙사는 없었고, 현금분할납부가 가능한 공공기숙사도 사립대학 9개교뿐이었다.')}
transcriptions={};changes=[]
for path in (ROOT/'assets/psat').glob('*.json'):
 data=read(path)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  if q['id'] not in old or q['number'] not in spec:continue
  previous=old[q['id']];assert q==previous
  snap=OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();write(snap,previous)
  s=spec[q['number']];s['remove']=[len(q['figures'])-1];q['body']=s['body'];q['figures']=previous['figures'][:-1]
  if q['number']==8:
   for i,v in enumerate(q['steps']):
    for year in ['2023','2025','2027']:v=v.replace(year+'비중',year+'년 비중').replace(year+'시스템',year+'년 시스템').replace(year+'총규모',year+'년 총규모')
    q['steps'][i]=v.replace('250%초과','250% 초과')
   q['steps'][4]+=' 표시 비중에 ±0.05%p 오차를 허용해도 3,500×31.35%=1,097.25<1,179, 3,465×19.85%=687.8025>657로 사용한 경계는 유지된다.'
  if q['number']==12:
   q['pitfall']=q['pitfall'].replace('단위십억','단위 십억').replace('보기의억','보기의 억')
   q['steps'][4]+=' 독일의 기존 비율에 ±0.005%p, 금액에 ±0.05십억 달러 오차를 허용해도 최대 새 비율은 0.615%×27.05/24.05<0.70%여서 판단은 유지된다.'
  if q['number']==18:
   q['steps']=[v.replace('으로약','으로 약') for v in q['steps']]
   q['underlines']=['㉠2019년 대비 2020년 대학유형별 기숙사 수용률은 국공립대학보다 사립대학이, 비수도권대학보다 수도권대학이 더 큰 폭으로 증가하였다.','㉡국공립대학은 전년 대비 800명 이상 증가하였으나, 사립대학은 전년 대비 1,400명 이상 감소하였다.','㉢전체 대학 중 기숙사비 카드납부가 가능한 대학은 37.9%에 불과하였다.','㉣카드납부가 가능한 공공기숙사는 없었고, 현금분할납부가 가능한 공공기숙사도 사립대학 9개교뿐이었다.'];q['underlineLabelAnchors']=True
  q['editNote']+=' 보기·대화·정보·보고서의 문장은 본문 글자로 표시하고, 표·그래프·공정도·수식·단위·범례·주석은 원형으로 유지한다. 원문 보기에서 전체 배치를 확인할 수 있다.'
  q['revision']+=1;touched=True;transcriptions[q['id']]=s
  changes.append(dict(id=q['id'],file=path.relative_to(ROOT).as_posix(),oldRevision=previous['revision'],newRevision=q['revision'],changedFields=sorted(k for k in q.keys()|previous.keys() if k!='revision' and q.get(k)!=previous.get(k)),beforeSnapshot=snap.relative_to(ROOT).as_posix(),reason='글 블록의 본문 표시·네밑줄 복원·단어경계와 안전한 오차 경계 보강. 정답·선지·자료·산식·기존 자산·기록 보존.',status='repaired_pending_reverification'))
 if touched:write(path,data)
assert len(changes)==9;write(OUT/'changes-batch18.json',changes);write(B/'native-prose-transcriptions.json',dict(status='implemented_pending_verification',transcriptions=transcriptions,dataFiguresUnchanged=True,dataFiguresRelativeOrderPreserved=True,proseAfterData=True,allOriginalAssetsRetained=True,uiCodeChanged=False))
print('Frozen41/50 before repairs; nine native prose blocks; all figures/data and false report claims retained.')
