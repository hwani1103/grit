import re,unicodedata
import pdfplumber
import review_remaining605 as r
b=r.folder(36);old={x['question']['id']:x['question'] for x in r.read(b/'revealed-current.json')}
assert 'All tests passed!' in (b/'host-before.log').read_text(encoding='utf-8-sig')
assert r.read(b/'exact-model-checks.json')['status']==r.read(b/'source-native-pixel-checks.json')['status']=='PASS'
bodies={
21:'<보기>\n\nㄱ. 2022 ～ 2024년 동안 매년 하이브리드자동차 판매대수는 전체 판매대수의 80% 이상이다.\n\nㄴ. 2022년 대비 2023년 전체 판매대수 감소폭 중 하이브리드자동차 판매대수 감소폭의 비중은 90% 이상이다.\n\nㄷ. 2022년부터 2025년 상반기까지 수소전기자동차 판매대수의 합은 2025년 상반기 전기자동차 판매대수보다 많다.\n\nㄹ. 2025년 하반기 전체 판매대수가 상반기 전체 판매대수의 2배라면, 2025년 전기자동차 판매대수는 175대 이하이다.',
24:'<보기>\n\nㄱ. 관광수입과 관광지출은 매년 증가하였다.\n\nㄴ. 관광수입의 전년 대비 증가율이 가장 높은 해에 관광지출의 전년 대비 증가율도 가장 높다.\n\nㄷ. 2021년 ‘갑’국 방문 외래관광객 수의 전년 대비 감소율은 60% 이하이다.\n\nㄹ. 2022년 외국 방문 ‘갑’국민관광객 수는 ‘갑’국 방문 외래관광객 수의 3배 이상이다.',
27:'<보기>\n\nㄱ. 전년 대비 2025년 수출액 증가율은 가공식품이 농기자재보다 높다.\n\nㄴ. 2024년 농약 수출액은 400백만 달러 미만이다.\n\nㄷ. 전년 대비 2025년 수출액 증가폭은 라면이 농기계의 4배 이상이다.\n\nㄹ. 2025년 농산업 수출액에서 비료와 동물용의약품 수출액의 합이 차지하는 비중은 15% 미만이다.',
28:'<보기>\n\nㄱ. 비타민 B₂는 주요 비타민 중 ‘긍정’ 상호작용이 발생하는 비타민 수와 ‘부정’ 상호작용이 발생하는 비타민 수의 차이가 가장 크다.\n\nㄴ. (B₂, B₉, K) 비타민 조합의 효과 지수는 5이다.\n\nㄷ. (B₃, B₅, B₁₂, E) 비타민 조합의 효과 지수는 (B₃, B₅, E) 비타민 조합의 효과 지수보다 크다.',
33:'<보기>\n\nㄱ. 2021년은 생산액 규모가 ‘10억 원 이상 50억 원 미만’인 업체 생산액 합이 생산액 규모가 ‘1억 원 미만’인 업체 생산액 합의 2배 이상이다.\n\nㄴ. 종사자 규모가 100명 이상인 업체 수는 매년 전체 업체 수의 2% 이상이다.\n\nㄷ. 2019년은 종사자 규모가 ‘20명 미만’인 업체 생산액 합이 1,300억 원 이상이다.',
34:'<보기>\n\nㄱ. 2030년 총부양비는 36 이상이다.\n\nㄴ. 고령화지수는 2040년이 2020년의 2.5배 이하이다.\n\nㄷ. 2030년 유소년인구가 총인구의 10%라면 고령화지수는 250 이상이다.\n\nㄹ. 2030년 유소년인구가 2020년과 동일하다면, 총부양비는 2030년이 2020년보다 높다.',
35:'<보기>\n\nㄱ. ‘아파트’ 대비 ‘단독주택’ 비율이 가장 높은 지역은 B이다.\n\nㄴ. C지역의 구분거처수는 5,500 이상이다.\n\nㄷ. A ～ E지역 모두 ‘주택수’ 중 ‘해당지역 거주자소유 주택수’가 차지하는 비중은 60% 이상이다.'}
notes={21:'상반기수소2·누적34·감소59/62·연간전기상한175를 검산했다. 작은 보기 이미지를 원문 본문으로 바꾸고 판정형 오답 근거를 구체화한다.',23:'활용률·수익률의 서로 다른 분모와70%/60%의 분리 경계를 확인했다. 선지90 %의 어절 공백을 복원한다.',24:'적자부호로 복원한 지출,증가율전체,외래 감소율과출입국비율을 검산했다. 보기 가독성과 붙어쓴 해설 두 곳 및 일부 판정형 이유를 개선한다.',27:'계층합과 증가율·증가폭을 확인하고 반올림구간에서도400·4배·15%판정이 유지됨을 확인했다. 보기 가독성과 실제 오차구간 설명·개별 이유·어절을 보완한다.',28:'대칭행렬의 서로 다른 두 원소 쌍,양·음 가중치와 추가 증분0을 대조했다. 작은 보기 이미지를 아래첨자 보존 본문으로 바꾼다. 정의·예시 수식 이미지는 원형 유지한다.',29:'집단 크기를 반영한 구성비와 경영 정수 기업수의 양립 사례를 검증했다. 그 수를 실제 관측치가 아닌 가능 사례로 제시하며 다섯 선택지 근거도 구체적이다.',30:'36개월 및시작·종료월과반올림구간의 유일한 정수10개월을 검산했다. 함정 설명의 각경력을 띄어쓴다.',33:'구간 합의 상하한,전연도2%초과,가장 작은2894개 하한1376을 검산했다. 보기와 개별 선지 근거를 개선하고0은 실제 생산액이 아니라 하한임을 명시한다.',34:'분자·분모 단조성,지수배율약2.99,포함변수165450·지수240을 확인했다. 작은 보기를 본문으로 옮기고③의 반례 수치를 명시한다.',35:'단독·다가구 계층과 B최대,C반올림하한5700초과,D반례를 검산했다. 작은 보기를 본문으로 옮기고 공통 지문의 도입문을 복원하며⑤의 반례를 명시한다.'}
ratings=[dict(id=i,scoreBeforeFix=5 if q['number']==29 else 4,assessment=notes[q['number']],needsChange=q['number']!=29,deduction='발견 없음' if q['number']==29 else '보기 가독성·원문 맥락·개별 근거 또는 어절 개선') for i,q in old.items()]
assert not (b/'ratings-before.json').exists();r.write(b/'ratings-before.json',dict(method='Same-author fresh original solves, direct key/native/fresh pixels, exact interval/graph models, host before-edit inspection.',ratings=ratings));r.write(b/'ratings-frozen.json',dict(frozenAt=r.now(),ratingsSha256=r.sha(b/'ratings-before.json'),total=41,count=10,beforeChanges=True))
reg={x['newAsset']:x for x in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/native-image-repairs.json')['figures']}
norm=lambda s:re.sub(r'\s','',unicodedata.normalize('NFKC',s))
changes=[];checks=[]
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  if q['id'] not in old or q['number']==29:continue
  prev=old[q['id']];assert prev==q;n=q['number'];snap=r.OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();r.write(snap,prev)
  if n in bodies:
   q['body']=bodies[n];rec=reg[q['figures'][-1]['asset']]
   with pdfplumber.open(r.ROOT/rec['source']) as pdf:raw=pdf.pages[rec['page1based']-1].crop(rec['rect']).extract_text()
   if n==28:
    # PDF extraction emits subscripts on the next line. Record exact raw text
    # and validate every displaced index explicitly before normal comparison.
    raw=raw.replace('B 는','B₂는').replace('\n2\n','\n').replace('(B , B , K)','(B₂, B₉, K)').replace('\n2 9\n','\n').replace('(B , B , B , E)','(B₃, B₅, B₁₂, E)').replace('(B , B , E)','(B₃, B₅, E)').replace('\n3 5 12 3 5\n','\n')
   assert norm(raw)==norm(q['body']),(n,raw,q['body'])
   q['figures']=q['figures'][:-1]
  if n==21:
   q['steps']=[s.replace('비중은(','비중은 (') for s in q['steps']]
   q['optionReasons'][1]='연간 전체 774에서 하이브리드 597과 최소 수소 2를 빼 전기차 상한 175를 얻어 ㄹ은 맞다. 그러나 2023년 690<869×0.8로 ㄱ은 거짓이며 참인 ㄴ도 빠졌다.'
   q['optionReasons'][4]='ㄴ의 59/62와 ㄹ의 상한 175는 맞지만, 수소차 누적 13+12+7+2=34는 상반기 전기차 57보다 적다. ㄷ을 추가할 수 없다.'
  if n==23:q['choices']=[s.replace('90 %','90%') for s in q['choices']]
  if n==24:
   q['optionReasons']=[s.replace('감소율약','감소율 약').replace('각각감소율','각각 감소율') for s in q['optionReasons']]
   q['optionReasons'][3]='ㄱ·ㄴ은 맞지만 외래객 수의 남은 비율이 약 0.384라 감소율은 약 61.6%다. 60% 이하라는 ㄷ을 추가할 수 없다.'
  if n==27:
   q['steps']=[s.replace('보다약','보다 약').replace('비료만약','비료만 약') for s in q['steps']]
   q['steps'][4]='적용 한계: 증가율이 소수 첫째자리에서 표시되므로 실제 비율을 ±0.05%p 범위로 넓힌다. 농약은 400×1.2005=480.2<490.2여서 전년 400을 넘는다. 농기계 증가폭 상한은 660−660/1.0505<31.73이고 그 4배도 126.92 미만이라 라면 증가 141.5보다 작다. 비료는 207.6×1.0695>222이며 동물용 67.2를 더하면 15% 기준 225.3을 넘는다. 역산 소수를 확정 원수치로 쓰지 않는다.'
   q['optionReasons'][3]='농기계 증가폭의 4배보다 라면 증가 141.5가 커 ㄷ은 맞다. 그러나 비료·동물용 합 약 289.3은 농산업 1,502의 15%인 225.3보다 커 ㄹ은 틀리다.'
   q['optionReasons'][4]='ㄱ은 맞지만 농약 전년액 약 408.5는 400보다 크고, 비료·동물용 비중 약 19.3%는 15%보다 크다. ㄴ·ㄹ은 모두 경계를 반대로 판단했다.'
  if n==30:q['pitfall']=q['pitfall'].replace('각경력을','각 경력을')
  if n==33:
   q['steps'][2]=q['steps'][2].replace('1932개는 0,916개는 1억,','1932개의 하한은 0, 916개의 하한은 1억,')
   q['optionReasons'][0]='ㄱ의 생산액 하한 4,850억은 비교 집단 상한 2,296억의 2배보다 크다. 그러나 100명 이상 비율도 매년 2%를 넘고, ㄷ의 하한 1,376억도 성립해 ㄱ만 고르면 빠진다.'
   q['optionReasons'][1]='100명 이상 업체 비율은 매년 2%를 넘는다. 하지만 ㄱ은 4,850>2×2,296으로, ㄷ은 최소 1,376≥1,300으로 각각 참이므로 ㄴ만은 아니다.'
  if n==34:q['optionReasons'][2]='유소년 고정 시 분자 증가·분모 감소로 ㄹ은 참이다. 그러나 고령화지수는 2040년 약 420.69, 2020년 약 140.50으로 약 2.99배여서 ㄴ의 2.5배 이하가 아니다.'
  if n==35:
   q['prompt']='다음 <표>는 ‘갑’국 A ～ E지역의 주택 보급 및 소유 현황에 관한 자료이다. 다음 물음에 답하시오.\n\n'+q['prompt']
   src=next(x['sourceText'] for x in r.read(b/'blind-source.json') if x['id']==q['id'])
   assert norm(q['prompt'].split('\n\n')[0]) in norm(src)
   q['optionReasons'][4]='ㄱ·ㄴ은 참이지만 D의 해당지역 거주자소유 13,106은 전체 주택 22,755의 60%인 13,653보다 작다. ㄷ을 추가할 수 없다.'
  fields=sorted(k for k in q.keys()|prev.keys() if q.get(k)!=prev.get(k));assert fields
  q['revision']+=1;touched=True
  assert q['answer']==prev['answer'] and [norm(s) for s in q['choices']]==[norm(s) for s in prev['choices']]
  changes.append(dict(id=q['id'],file=p.relative_to(r.ROOT).as_posix(),oldRevision=prev['revision'],newRevision=q['revision'],changedFields=fields,beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason=notes[n],status='repaired_pending_reverification'))
  checks.append(dict(id=q['id'],nativeProseFromOriginal=n in bodies,sourceIndexRecoveryDocumented=n==28,sharedIntroductionRestored=n==35,answersChoicesAndOriginalAssetsPreserved=True))
 if touched:r.write(p,data)
assert len(changes)==9;r.write(r.OUT/'changes-batch36.json',changes);r.write(b/'repair-semantic-checks.json',dict(status='PASS',checks=checks,originalSourceProseExactIgnoringWhitespace=True))
print('Frozen41/50;9 repairs,7 native 보기 blocks; exact source/choices preserved')
