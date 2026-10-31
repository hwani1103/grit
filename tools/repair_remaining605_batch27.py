import re,shutil
import review_remaining605 as r
b=r.folder(27);old={x['question']['id']:x['question'] for x in r.read(b/'revealed-current.json')}
bodies={
'2025-11-15-25':('<보기>\n\nㄱ. 청년 여성 중 소득이 150만 원 이상 300만 원 미만인 청년 여성의 비중은 청년 남성 중 소득이 150만 원 이상 300만 원 미만인 청년 남성의 비중보다 작다.\n\nㄴ. 소득이 300만 원 미만이고 연령이 23 ～ 26세인 청년인구 1명당 소득은 100만 원 이상이다.\n\nㄷ. 연령이 27세 이상이거나 주거형태가 전세인 청년인구는 2,450명 이상이다.',1),
'2026-07-18-02':('<정보>\n\n○ 2025년 포도 재배면적은 10,000ha 이상이다.\n\n○ 포도의 성목면적은 2025년이 2024년보다 작다.\n\n○ 2025년 포도는 성목면적이 유목면적의 2.5배 이상이다.',1),
'2026-07-18-07':('<보고서>\n\n‘갑’국 영유아 양육자의 돌봄시간 지원제도 이용 현황은 다음과 같다. 돌봄시간 지원제도별 이용률은 ‘유연근무’가 27.1%로 가장 높고, ‘육아기 근로시간 단축’ 26.0%, ‘가족돌봄휴가’ 25.4%, ‘재택근무’ 15.1% 순이다.\n\n월평균 가구 소득 구간별 돌봄시간 지원제도 이용률은 200만 원 미만 구간에서는 ‘재택근무’가 가장 높고, 500만 원 이상 구간에서는 ‘유연근무’가 가장 높다. 맞벌이 가구의 경우, ‘유연근무’ 이용률은 ‘전일제 근로와 시간제 근로’ 형태에서 가장 낮고, ‘재택근무’ 이용률은 ‘부부 모두 시간제 근로’ 형태에서 가장 높다. 한편, ‘재택근무’의 거주지역별 이용률은 대도시가 17.5%인데 반해 읍면지역은 8.8%에 그친다.',1),
'2026-07-18-08':('<보기>\n\nㄱ. 입영예정자 수가 가장 많은 해에 입영자 수도 가장 많다.\n\nㄴ. 2021년 대비 2025년 입영자 수의 감소율은 10% 이하이다.\n\nㄷ. 입영비율의 전년 대비 증가율은 2022년이 2025년의 4배 이상이다.\n\nㄹ. 입영자 수의 전년 대비 증가율이 가장 높은 해에 입영비율도 가장 높다.',1),
'2026-07-18-09':('<보고서>\n\n2025년 ‘갑’국의 초ㆍ중ㆍ고 사교육비 총액은 27.5조 원이었다. 학교급별 총액은 초등학교가 12.2조 원으로 가장 컸으며, 그다음은 고등학교, 중학교 순이었다. 초ㆍ중ㆍ고 사교육비 총액은 2016년 대비 51.9% 증가하였으나 전년에 비해서는 5.8% 감소하였다. 특히, 초등학교 사교육비 총액은 전년 대비 7.9% 감소하여 감소율이 가장 높았다. 한편, 가구 자녀수별로 살펴보면, 1인당 월평균 사교육비는 가구 자녀수가 3명 이상일 때 가장 적었다.\n\n2025년 사교육 참여율은 75.7%로 전년 대비 4.3%p 하락하였으며, 주당 참여시간은 7.1시간으로 전년 대비 0.5시간 감소하였다. 학교급별 참여율은 초등학교가 가장 높고, 그다음은 중학교, 고등학교 순이었으며, 모든 학교급에서 전년 대비 참여율이 감소한 것으로 분석되었다.\n\n가구 소득수준별로 살펴보면, 가구 소득수준이 높을수록 사교육 참여율이 높았다. 소득수준 800만 원 이상 가구의 참여율은 84.9%였던 반면, 소득수준 300만 원 미만 가구의 참여율은 52.8%였다. 두 집단 간 참여율 격차는 32.1%p로 전년 대비 증가한 것으로 나타났다.',0),
'2026-07-18-11':('<보기>\n\nㄱ. 2015년 안전등급이 B인 기반시설 분야 수는 7개이다.\n\nㄴ. 2015년 안전등급과 2025년 안전등급이 같은 기반시설 분야는 댐, 도로, 폭우, 통신뿐이다.\n\nㄷ. 2020년 대비 2025년 안전등급이 높아진 기반시설 분야 수는 2015년 대비 2020년 안전등급이 높아진 기반시설 분야 수보다 많다.',1),
'2026-07-18-12':('<보기>\n\nㄱ. 2024년 예산집행률은 95% 이상이다.\n\nㄴ. 2023년 대비 2025년 지원액 감소율은 2023년 대비 2025년 지원인원 수 감소율보다 낮다.\n\nㄷ. 지원인원 1인당 지원액은 2024년이 2023년보다 작다.\n\nㄹ. 참여대학 1개교당 지원액은 2025년이 2023년보다 크다.',1)}
assess={23:'반품률·순판매율 여집합과 세 제품별 증분을 합계에 반영한다. 네 오답 임계와16/27%p 증가 검산 일치.',25:'가중비중·비음수 소득 하한·합집합 하한2452/2459가 정확하다. 통상 비음수 전제가 기존 적용한계에 이미 명시되어 있고 새 풀이에도 공개 전 별도 기록했다.',1:'숙취해소제16일목요일 반례와 모든월요일·홍보팀·사원별 지급을 원문16행에 대조했다. 겸직금지 주석과 개인/부서 집계 구분이 정확하다.',2:'총면적·성목감소·2.5배 조건과 각 후보 탈락 이유를 검산하고 D의 세 조건을 모두 역대입했다.',6:'범례 중단/부족과 합계101/178/178/229/265를 대조했다. 비중하락 반례와2022이후 네 해3배미만 검산 정확.',7:'현재+필요시와 소득·근로형태·거주지역 분류를 대응한다. ㄴ은 무관하며 ㄱㄷㄹ의 모든 보고서 수치를 대조했다.',8:'인원·비율·비율증가율 분리와 실제 선택지에서ㄷ만 추가 판별하는 유일성 확인. 느슨한5%/5.6% 경계도 엄밀히 성립.',9:'보고서의 대상·기간·지표를 다섯 표와 대응한다. 자녀수별 참여율은 금액 근거가 아니며 네 표만으로 모든 문장이 작성된다는 과장도 배제한다.',11:'18×3등급을 직접 전사해2015B7개,장기불변4개,개선6→4를 확인했다. 상승폭과 분야수 구별 정확.',12:'예산·인원·학교수별 분모를 구분한다.8.8백만원과200백만원 분리기준 및 감소율4%초과/3%미만 경계를 검산했다.'}
ratings=[]
for qid,q in old.items():
 key=q['examDate']+f"-{q['number']:02}";change=key in bodies or q['number']==23
 ratings.append(dict(id=qid,scoreBeforeFix=4 if change else 5,assessment=assess[q['number']],deduction='이미지 보고서·보기·정보를 원문 그대로 네이티브 본문으로 옮기고 자료 순서를 유지한다.' if key in bodies else '선택지 수치와%기호 공백을 연결한다.' if change else '발견 없음.',needsChange=change))
assert not (b/'ratings-before.json').exists();r.write(b/'ratings-before.json',dict(method='Same-author original/own solve/key/exact models and pre-edit host visual review.',ratings=ratings));r.write(b/'ratings-frozen.json',dict(frozenAt=r.now(),ratingsSha256=r.sha(b/'ratings-before.json'),total=42,count=10,beforeChanges=True))
changes=[]
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  if q['id'] not in old:continue
  key=q['examDate']+f"-{q['number']:02}"
  if key not in bodies and q['number']!=23:continue
  before=old[q['id']];assert q==before
  snap=r.OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();r.write(snap,before)
  if key in bodies:
   body,i=bodies[key];assert not q['body'];q['body']=body;q['figures']=[f for j,f in enumerate(q['figures']) if j!=i]
   if q['number']==9:q['figuresAfterBody']=True
   if q['number']==7:q['bodyAfterFigureCount']=1
  else:q['choices']=[re.sub(r'(?<=\d)\s+(?=%)','',s) for s in q['choices']]
  q['revision']+=1;touched=True
  changes.append(dict(id=q['id'],file=p.relative_to(r.ROOT).as_posix(),oldRevision=before['revision'],newRevision=q['revision'],changedFields=sorted(k for k in q.keys()|before.keys() if k!='revision' and q.get(k)!=before.get(k)),beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason='Original prose readable at native font; original table/report/choice order retained. Original assets and all reasoning/data preserved.',status='repaired_pending_reverification'))
 if touched:r.write(p,data)
assert len(changes)==8;r.write(r.OUT/'changes-batch27.json',changes)
source=r.ROOT/'lib/psat.dart';snap=b/'psat-before.dart';assert not snap.exists();shutil.copyfile(source,snap)
r.write(b/'reader-before.json',dict(file='lib/psat.dart',beforeSha256=r.sha(source),beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason='Optional bodyAfterFigureCount preserves original table/report/choice-table order when report becomes native prose. Defaults preserve existing all-before or all-after rendering. Vitamin unchanged.'))
print('Frozen42/50;7 native prose blocks and1choice boundary repair; reader snapshot before insertion support.')
