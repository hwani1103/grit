"""Freeze individual evaluations, then make explicit source-preserving repairs."""
import hashlib
import review_remaining605 as r
b=r.folder(21);old={x['question']['id']:x['question'] for x in r.read(b/'revealed-current.json')}
assessments=[
('연봉배수와 연도별S1/A2/B3을 만족하는 두 배치 모두 합490. 개별값 미정과 합의 유일성을 구분한 해설이 정확하다.','발견 없음. 조건·등급표·성과급표의 원형을 유지한다.',False),
('L14/M12/S10과 I·II대형5개, II대형최소1000을 세어ㄱㄷㄹ. 하한과 실제값, 병합된 기준 범위가 정확하다.','보기 네 문장을 본문으로 전환한다.',True),
('순차배율과 마지막 하한 뒤 증가폭 E>D>A>B>C. 기온과 지표면온도 및 최종값과 증가폭 구분이 정확하다.','수정 규칙 네 단계를 본문으로 전환한다.',True),
('2017합계602/479 복원과 구성비의 분모차가 오류①의 원인. 나머지 네 그래프의 개별수치도 계산과 일치한다.','해설의 비는(, 로약, 은유형별 어절 경계를 개선한다. 모든 그래프를 유지한다.',True),
('산불평균473.7, 최대·최소연도의 검거율비교, 입산자217/620과 단조관계 반례가 정확하다.','보기 네 문장을 본문으로 전환한다.',True),
('미등재 상한976 안의 증가 반례와 뉴욕증가 최대의 상한 비교가 타당하다. 2027 예상치 주석도 유지되어 있다.','발견 없음. 순위 누락을0으로 바꾸지 않는 설명이 충분하다.',False),
('전임교원합·4년평균과 포함경계를 적용한 점수8/4/6/7/6. 후보상한7이 유효하고 정답도 유일하다.','해설의 188도평균 어절 경계를 개선한다.',True),
('전체물동량·선박1.5배·환적비중·단위계수100의 네조건에서C만 충족. 1000TEU 엄격경계와 배수/증가율을 구분한다.','긴 보고서를 본문 글자로 전환한다.',True),
('산점도의 높이·차이·원점기울기·역전쌍을 구분하여ㄱㄷ. 보수적 좌표구간에서도 C의 차이와 빈곤비율 판단이 유지된다.','보기 네 문장을 본문으로 전환한다. 두 그래프의 눈금·점·축을 유지한다.',True),
('비의료최대-최소2990과 의료4520<4960 등 네경계가③에서만 충족. 미제시 중간순위도 범위로 보장된다.','보고서를 본문으로 전환하고 다섯 선택지 표 앞에 배치한다.',True)]
assert not (b/'ratings-before.json').exists() and not (r.OUT/'changes-batch21.json').exists()
ratings=[dict(id=qid,scoreBeforeFix=4 if change else 5,assessment=a,deduction=d,needsChange=change) for qid,(a,d,change) in zip(old,assessments)]
r.write(b/'ratings-before.json',dict(method='Same-author individual pre-edit source, five-option, arithmetic and default-screen review.',ratings=ratings))
r.write(b/'ratings-frozen.json',dict(frozenAt=r.now(),ratingsSha256=hashlib.sha256((b/'ratings-before.json').read_bytes()).hexdigest(),total=42,count=10,beforeChanges=True))
spec={
'kr-mpm-2021-07-10-psat-d-20':dict(remove=[2],body='보기\n\nㄱ. 방류수의 생물학적 산소요구량 기준이 ‘5mg/L 이하’인 하수처리장 수는 5개이다.\n\nㄴ. 1일 하수처리용량 500m³ 이상인 하수처리장 수는 1일 하수처리용량 50m³ 미만인 하수처리장 수의 1.5배 이상이다.\n\nㄷ. Ⅱ등급 지역에서 방류수의 총인 기준이 ‘0.3mg/L 이하’인 하수처리장의 1일 하수처리용량 합은 최소 1,000m³이다.\n\nㄹ. 방류수의 총질소 기준이 ‘20mg/L 이하’인 하수처리장 수는 방류수의 화학적 산소요구량 기준이 ‘20mg/L 이하’인 하수처리장 수의 5배 이상이다.'),
'kr-mpm-2021-07-10-psat-d-23':dict(remove=[4],body='규칙\n\n단계 1: 각 도시의 설계적설하중을 50% 증가시킨다.\n\n단계 2: ‘월평균 지상 10m 기온’이 영하인 달이 3개 이상인 도시만 단계 1에 의해 산출된 값을 40% 증가시킨다.\n\n단계 3: 설계기본풍속이 40m/s 이상인 도시만 단계 1～2를 거쳐 산출된 값을 20% 감소시킨다.\n\n단계 4: 단계 1～3을 거쳐 산출된 값을 수정된 설계적설하중으로 한다. 단, 1.0kN/m² 미만인 경우 1.0kN/m²으로 한다.'),
'kr-mpm-2021-07-10-psat-d-25':dict(remove=[2],body='보기\n\nㄱ. 2011～2020년 연평균 산불 건수는 500건 이하이다.\n\nㄴ. 산불 건수가 가장 많은 연도의 검거율은 산불 건수가 가장 적은 연도의 검거율보다 높다.\n\nㄷ. 2020년에는 기타를 제외하고 산불 건수가 적은 산불 원인일수록 검거율이 높다.\n\nㄹ. 2020년 전체 산불 건수 중 입산자 실화가 원인인 산불 건수의 비율은 35%이다.'),
'kr-mpm-2025-11-15-psat-d-07':dict(remove=[1],body='보고서\n\n해운항만 정책을 수립하기 위해 ‘갑’항만의 주요지표 변화를 살펴본 결과는 다음과 같다. 우선, 2014년보다 2024년 전체 물동량이 증가한 것으로 나타났다. 출입항 선박 수도 증가하여 2024년에는 2014년의 150% 이상이 되었다. ‘갑’항만의 전체 물동량 중 환적 물동량이 차지하는 비중 역시 2024년이 2014년보다 큰 것으로 나타났다. 한편, 2024년 ‘갑’항만의 출입항 선박 수 대비 전체 물동량은 1척당 1,000TEU를 초과하였다. 따라서, 항만 기반 시설 확충 및 설비 고도화가 필요할 것으로 전망된다.'),
'kr-mpm-2025-11-15-psat-d-08':dict(remove=[2],body='보기\n\nㄱ. 세후 지니계수가 가장 높은 국가는 세후 빈곤율도 가장 높다.\n\nㄴ. 세전 지니계수와 세후 지니계수의 차이가 가장 큰 국가는 B이다.\n\nㄷ. 세전 빈곤율 대비 세후 빈곤율이 가장 낮은 국가는 C이다.\n\nㄹ. 세전 지니계수가 높은 국가일수록 세후 지니계수도 높다.'),
'kr-mpm-2025-11-15-psat-d-09':dict(remove=[0],figuresAfterBody=True,body='보고서\n\n2024년 국가기간·전략산업직군의 직종별 시간당 훈련비 지원단가를 조사한 결과, 지원단가의 조정 필요성이 제기되었다. 지원단가가 가장 낮은 직종은 의료기술로 5,000원 이하였고, 지원단가가 가장 높은 직종은 광산조사·탐사로 1만 원 이하였다. 의료기술을 제외한 모든 직종에서 두 직종 간 지원단가 차이는 3,000원 미만이었다. 그러나, 의료기술 지원단가는 광산조사·탐사 지원단가의 50% 미만으로 지원단가 조정을 검토할 필요가 있는 것으로 나타났다.')}
spacing={
'kr-mpm-2021-07-10-psat-d-24':{'비는(':'비는 (','로약':'로 약','은유형별':'은 유형별'},
'kr-mpm-2025-11-15-psat-d-05':{'188도평균':'188도 평균'}}
changes=[]
for path in (r.ROOT/'assets/psat').glob('*.json'):
    data=r.read(path)
    if not isinstance(data,list):continue
    touched=False
    for q in data:
        qid=q['id']
        if qid not in spec and qid not in spacing:continue
        before=old[qid];assert q==before
        snap=r.OUT/f"before-changes/{qid}-r{q['revision']}.json";assert not snap.exists();r.write(snap,before)
        if qid in spec:
            s=spec[qid];q['body']=s['body'];q['figures']=[v for i,v in enumerate(before['figures']) if i not in s['remove']]
            if s.get('figuresAfterBody'):q['figuresAfterBody']=True
            q['editNote']+=' 보기·규칙·보고서 문장을 본문 글자로 표시한다. 표·그래프·주석·단위와 선택지 자료는 원형으로 유지하며 원문 보기에서 전체 배치를 확인할 수 있다.'
        if qid in spacing:
            for a,z in spacing[qid].items():
                assert sum(v.count(a) for v in q['steps'])==1
                q['steps']=[v.replace(a,z) for v in q['steps']]
        q['revision']+=1;touched=True
        changes.append(dict(id=qid,file=path.relative_to(r.ROOT).as_posix(),oldRevision=before['revision'],newRevision=q['revision'],changedFields=sorted(k for k in q.keys()|before.keys() if k!='revision' and q.get(k)!=before.get(k)),beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason='본문 글자 전환 또는 해설 어절 경계 개선; 공식 내용·정답·선지·자료·기존 자산과 기록 보존.',status='repaired_pending_reverification'))
    if touched:r.write(path,data)
assert len(changes)==8
r.write(r.OUT/'changes-batch21.json',changes)
r.write(b/'native-prose-transcriptions.json',dict(status='implemented_pending_verification',transcriptions=spec,dataFiguresUnchanged=True,allOriginalAssetsRetained=True,readingOrder='All source prose remains after data except d09 report remains before choice tables using figuresAfterBody.',uiCodeChanged=False))
print('Frozen42/50; six native prose blocks and two spacing repairs.')
