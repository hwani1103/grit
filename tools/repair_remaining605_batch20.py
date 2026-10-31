"""Freeze scores, transcribe two prose blocks and restore three word boundaries."""
from pathlib import Path
import datetime,hashlib,json
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/psat_remaining605_20261030';B=OUT/'batch20'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
now=lambda:datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).isoformat()
old={x['question']['id']:x['question'] for x in read(B/'revealed-current.json')};assert not (B/'ratings-before.json').exists() and not (OUT/'changes-batch20.json').exists()
assessments=[
(5,'甲기타/乙법정 유형 고정 후 신청·결과 통지·타기관 이송·반복종결 제외를 각각 대조해④다. 한 단계의 예외를 다른 단계의 의무 면제로 넓히지 않는다.','발견 없음. 원문 민원 종류·신청·접수·이송·통지·반복 처리 여섯 규칙과 상황이 보존된다.'),
(5,'A기본 두 기준 미달,영어B만족도90이상이면27/45로허용이라는 대우,실습C평균18미만에서x≤15를 확인해ㄴㄷ이다. x16의 경계도 허용으로 검산한다.','발견 없음. 평균/단년 기준의90%와 이상/미만의 부정을 정확히 적용한다.'),
(4,'건축물 허용·정부 연계 확대·합의 이동·시범 항목 삭제를 대응해㉯㉰㉲이다. III의 총점10유지와 하위7/3→3/7변경을 분리하며 수정합50도 확인한다.','설명·협의 결과 두 이미지 글 블록이 작다. 본문 글자로 전환하고 가운데 수정안 표·밑줄은 원형 유지한다. 협의 결과를 표 앞에 배치하는 순서 변경을 기록한다.'),
(5,'기본 일정9모형과 후보별4/1/7/3/2모형을 전수 비교해②만 유일하다.乙월저녁/甲화점심/丙수점심의 달성 및 네 오답의 복수 배치가 모두 정확하다.','발견 없음. 날짜까지 서로 달라야 한다고 가정하지 않으며 후기 뒤 예약의 시간관계를 보존한다.'),
(5,'5일32이력 중111포함8개와 최초달성일별4/2/2개로누적50000명이다. 금요일 첫달성에서 월요일을 자유롭게 두고 이미 설치한 사람을 제거하거나 중복 합산하지 않는다.','발견 없음. 최초 설치일별25000/12500/12500과 명시된8이력이 모두 일치한다.'),
(5,'장관 요구 주민투표 실시의 의회 의견 예외로①이며,경유 의무·2000명 연서·추천 주체를 대조했다. 공통 제시문의 위원수 산식과 올림 규칙도 원문에 보존된다.','발견 없음. 건의와 통합 의사 확인 및 공동위원회 구성의 단계를 섞지 않는다.'),
(5,'명부 작성의 장관/송출국가 기관장 협의로②다. 내국인 신청·상담·수수료 허용·기관장 추천·사용자 허가서 발급을 주체와 상대방별로 정확히 분리한다.','발견 없음. 허용된 수수료를 무료 의무로 바꾸거나 후보자를 허가서 수신자로 오인하지 않는다.'),
(5,'조제/판매·전문/일반·처방전/장소 예외를 분리해ㄴㄷ이다. 사회봉사 예외가 장소나 전문약 판매의 모든 제한을 없앤다는 잘못된 확대가 없다.','발견 없음. 제시된 법문만 적용하며 추가 현실 의료·약사 규정으로 답을 바꾸지 않는다.'),
(5,'2024실거주와 설치전 전입 최우선 예외를 적용해甲27만/乙48만합75만이다. 원문 설치일·전입일 열과 두 실제기간,표 삽입 위치를 대조했다.','발견 없음. 주민등록 계속 유지와12개월 실제 거주를 동일시하지 않으며 별도 일할 계산을 추가하지 않는다.'),
(4,'지역별 기본25/20/25만원과2종10%·1종30%·3종추가없음을 적용해27.5>26>25로①이다. 높은 가산율만으로 최종액을 비교하지 않는다.','丙은추가·2종은기준액·1종은기준액으로 붙은 단어 경계를 복원한다. 금액·가산율·정답·선지·본문은 유지한다.')]
ratings=[dict(id=qid,scoreBeforeFix=score,assessment=a,deduction=d,needsChange=score<5) for qid,(score,a,d) in zip(old,assessments)];assert sum(r['scoreBeforeFix'] for r in ratings)==48
write(B/'ratings-before.json',dict(method='Same-author pre-edit source/all5options/models/host assessment; no prior official key exposures.',ratings=ratings));write(B/'ratings-frozen.json',dict(frozenAt=now(),ratingsSha256=hashlib.sha256((B/'ratings-before.json').read_bytes()).hexdigest(),total=48,count=10,beforeChanges=True))
body='○ ‘대학 캠퍼스 혁신파크 사업’을 담당하는 A주무관은 신청 조건과 평가지표 및 배점을 포함한 <사업 공모 지침 수정안>을 작성하였다. 평가지표는 I～IV의 지표와 그 하위 지표로 구성되어 있다.\n\n상황\n\nA주무관은 <사업 공모 지침 수정안>을 작성한 후 뒤늦게 ‘관계부처 협의 결과’를 전달받았다. 그 내용은 다음과 같다.\n\n○ 대학이 부지를 확보하는 것이 쉽지 않으므로 신청 사업부지 안에 건축물이 포함되어 있어도 신청 허용\n\n○ 도시재생뉴딜사업, 창업선도대학 등 ‘관련 정부사업과의 연계가능성’ 평가비중 확대\n\n○ 시범사업 기간이 종료되었으므로 시범사업 조기 활성화와 관련된 평가지표를 삭제하되 ‘대학 내 주체 간 합의 정도’는 타 지표로 이동하여 계속 평가\n\n○ 논의된 내용 이외의 하위 지표의 항목과 배점은 사업의 안정성을 위해 현행 유지'
changes=[];targets={r['id'] for r in ratings if r['needsChange']}
for path in (ROOT/'assets/psat').glob('*.json'):
 data=read(path)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  if q['id'] not in targets:continue
  previous=old[q['id']];assert q==previous;snap=OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();write(snap,previous)
  if q['id']=='kr-mpm-2021-07-10-psat-s-20':
   q['body']=body;q['figures']=[previous['figures'][1]];q['figuresAfterBody']=True
   q['editNote']+=' 사업 설명과 협의 결과는 본문 글자로 표 앞에 표시하며, 수정안 표·밑줄·수치·신청 조건은 원형으로 유지한다. 원문 보기에서 원래 전체 배치를 확인할 수 있다.'
  else:
   q['steps']=[v.replace('丙은추가','丙은 추가').replace('2종은기준액','2종은 기준액').replace('1종은기준액','1종은 기준액') for v in q['steps']]
  q['revision']+=1;touched=True
  changes.append(dict(id=q['id'],file=path.relative_to(ROOT).as_posix(),oldRevision=previous['revision'],newRevision=q['revision'],changedFields=sorted(k for k in q.keys()|previous.keys() if k!='revision' and q.get(k)!=previous.get(k)),beforeSnapshot=snap.relative_to(ROOT).as_posix(),reason='설명·협의 결과의 본문 전환 또는 유류비 해설의 세 단어 경계 복원. 정답·선지·원문·수정안 표·자산·기록 보존.',status='repaired_pending_reverification'))
 if touched:write(path,data)
assert len(changes)==2;write(OUT/'changes-batch20.json',changes)
write(B/'native-prose-transcriptions.json',dict(status='implemented_pending_verification',id='kr-mpm-2021-07-10-psat-s-20',remove=[0,2],body=body,tableFigureExactlyPreserved=True,allOriginalAssetsRetained=True,figuresAfterBody=True,originalReadingOrderChanged='The agreement prose now precedes the unchanged proposal table; original full page remains available.',uiCodeChanged=False))
# Scan selected word-boundary spellings only, retaining frozen target text.
prior={q['id'] for q in read(OUT/'preparation/previously-scored295.json')['questions']};hits=[]
for path in (ROOT/'assets/psat').glob('*.json'):
 data=read(path)
 if not isinstance(data,list):continue
 for q in data:
  v=old[q['id']] if q['id'] in targets else q;text='\n'.join(v.get('steps',[]));patterns=[p for p in ['丙은추가','2종은기준액','1종은기준액'] if p in text]
  if patterns:hits.append(dict(id=q['id'],cohort='prior295' if q['id'] in prior else 'fixed605',patterns=patterns,status='batch20_repaired_pending_verification' if q['id'] in targets else 'pending_source_and_semantic_review'))
write(OUT/'cross-candidates-fuel-word-boundaries20.json',dict(cause='R605-013-extension',method='All900 exact three selected spellings only; no global word-spacing clearance.',candidates=hits))
print('Frozen48/50; revised one raster prose question and three word boundaries. Other exact hits',len(hits)-1)
