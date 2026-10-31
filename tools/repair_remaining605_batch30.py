import re
import review_remaining605 as r
b=r.folder(30);old={x['question']['id']:x['question'] for x in r.read(b/'revealed-current.json')}
bodies={21:('<보기>\n\nㄱ. 발생건수 대비 피해액의 비율이 가장 낮은 해는 2023년이다.\n\nㄴ. 피해액의 전년 대비 증가율은 2024년이 2025년보다 높다.\n\nㄷ. 2023년 전체 발생건수 중 피해자 연령대가 50대 이하인 발생건수의 비중은 90% 이상이다.',2),
24:('<대화>\n\n주무관: 팀장님, 2026년 사업별 예산 편성지침에 대해 설명해 드리겠습니다.\n\n주무관: 먼저, 2024년 대비 2026년 사업별 편성 예산 증감액은 최대 100억 원입니다.\n\n주무관: 다음으로, 2025년 대비 2026년 사업별 편성 예산 증감률은 최대 50%입니다.\n\n주무관: 마지막으로, 사업별로 2024년부터 2026년까지 편성 예산의 합은 175억 원 이상 800억 원 이하여야 합니다.\n\n팀장: 그렇군요. 그러면 2026년 전체 편성 예산의 최소금액과 최대금액은 얼마인가요?\n\n주무관: 편성지침의 3가지 조건을 모두 만족할 때, 최소금액은 (가) 억 원이고, 최대금액은 (나) 억 원입니다.',1),
1:('<보고서>\n\n2024년 보훈병원 의료진 전체 정원과 현원을 살펴보면, 간호직의 경우 정원 2,171명, 현원 2,427명으로 현원이 정원을 초과하였다. 그러나 전문의는 정원 490명, 현원 453명으로 현원이 정원에 미치지 못하였으며, 특히 전공의는 정원 226명, 현원 60명으로 결원율이 매우 높았다.\n\n2024년 전문의 현원 1명당 연간 진료인원은 대전 10.3천 명, 대구 9.8천 명으로 전문의의 업무 부담이 과중한 것으로 나타나 보훈병원 의료진 부족 문제가 제기되는 상황이다.\n\n연도별 전공의 결원율은 2020년 15%에서 2022년 20%, 2024년 73%로 점차 악화되고 있다. 특히나 2020년 대비 2024년 전공의 현원이 70% 감소한 것으로 나타났다. 전공의가 부족할 경우 의료공백 문제가 발생하거나 보훈병원 전문 의료인력 양성에 차질이 생길 수 있으므로 보다 적극적인 유인방안 마련이 필요한 상황이다.',1)}
notes={15:'31일 날씨·최고/최저온도 전사, 모든 보기의 빈도·최댓값 날짜·구간을 검산했다. ㄱㄹ, 정답3. 달력·그림·표의 원형과 확대를 유지한다.',16:'F의 분자최대/분모최소, D의 두 시간최소, 방수 최대중량<비방수 최소, 자석식 평균31500>24375, 손전등35400<35800을 확인했다.',18:'정수 도시 수를 표시 구성비의 반올림 구간에서 유일하게 복원하고 지역합45/25/18/8/5 및 네 오답 경계를 검산했다. 선지50 % 공백을 연결한다.',19:'공통표의 빈칸7명/7명과 건수증감률·사망자증분·여섯 재해유형을 전부 대조했다. 사망자/발생건수 열 혼동이 없다.',20:'2024 사망자15유형을 양쪽 업종 모두 복원해 합303/170 및 두 번째32/31을 확인했다. 헤더 순서와 전년 증가 부호가 정확하다.',21:'2020/2023 건당피해 반례, 2024/2025 증가율60% 경계, 60대만으로10% 초과를 검산했다. raster 보기와 개별 판정형 해설을 네이티브·구체적 근거로 개선한다.',22:'네 능역의 비율순위와 수종8개, 잣나무 반례, 세 번째 수종, 초본밀도,44% 분리경계를 확인했다. 선택지50 % 공백을 연결한다.',24:'원문만 본 풀이에서 변화 크기 제한은675~850, 부호 있는 상한만 적용하면75~850임을 먼저 기록했다. 기존 해설도 크기를 사용하지만 그것을 증감률 일반규칙처럼 쓰면 안 된다. 대화 원문 보존·네이티브 표시와 해석 한계를 명시한다.',25:'연도차D43.3·부양비차E2·노령화C·부양비합A최대/B최소·E유소년비중우위를 유리수로 검산했다. 전체인구/청장년 분모 구별이 정확하다.',1:'보고서 모든 수치를 현재표/ㄱ과거자료/ㄴ진료인원에 대응하고 ㄷ의21개 결원율을 파생했다. 정원0/현원초과 예외와 반올림을 포함해 ㄱㄴ 필요성이 맞다. 보고서를 네이티브 본문으로 옮기되 앞 표와 뒤 보기표 순서를 보존한다.'}
fix={18,21,22,24,1}
ratings=[dict(id=qid,scoreBeforeFix=4 if q['number'] in fix else 5,assessment=notes[q['number']],needsChange=q['number'] in fix,deduction='원문 가독성·선지 경계·개별 근거 또는 적용한계 개선' if q['number'] in fix else '발견 없음') for qid,q in old.items()]
assert not (b/'ratings-before.json').exists();r.write(b/'ratings-before.json',dict(method='Same-author original-only solve then source/key/exact models/all-option/host pre-edit review.',ratings=ratings));r.write(b/'ratings-frozen.json',dict(frozenAt=r.now(),ratingsSha256=r.sha(b/'ratings-before.json'),total=45,count=10,beforeChanges=True))
changes=[]
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  if q['id'] not in old or q['number'] not in fix:continue
  before=old[q['id']];assert q==before;snap=r.OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();r.write(snap,before)
  n=q['number']
  if n in bodies:
   q['body'],index=bodies[n];q['figures']=[f for i,f in enumerate(q['figures']) if i!=index]
   if n==1:q['bodyAfterFigureCount']=1
  if n in [18,22]:q['choices']=[re.sub(r'(?<=\d)\s+(?=%)','',v) for v in q['choices']]
  if n==21:
   q['optionReasons']=['2020년 건당 피해액은 7,000/31,681로 약 0.221억 원이며, 2023년의 약 0.237억 원보다 작다. 따라서 ㄱ은 거짓이다.','2024년 증가율 2,785/4,472는 60%보다 크고, 2025년의 4,073/7,257은 60%보다 작다. ㄴ만 옳다.','2023년 60대 이상이 2,914건으로 전체 18,902건의 10%를 넘는다. 따라서 50대 이하가 90% 이상이라는 ㄷ은 거짓이다.','ㄴ은 맞지만, 2020년의 건당 피해액이 2023년보다 작으므로 ㄱ은 틀리다.','ㄴ은 맞지만, 2023년 50대 이하 비중은 15,988/18,902로 약 84.6%이므로 ㄷ은 틀리다.']
  if n==24:
   q['steps'][0]='착안점: 이 대화의 ‘증감액·증감률은 최대’는 증가와 감소의 크기를 제한하는 뜻으로 읽는다. 이를 전제로 사업마다 2026년 예산의 허용 구간 세 개를 구한 뒤 교집합을 취한다.'
   q['steps'][4]='적용 한계: 증감률을 항상 절댓값으로 바꾸는 규칙은 아니다. 이 풀이의 전제는 대화가 증가·감소의 크기를 제한한다는 해석이다. 부호 있는 증감액·증감률의 상한만 적용하면 최솟값은 75억 원이 되어 제시된 선택지와 달라진다. 또한 사업 간 합계 제한이나 상호 연계가 추가되면 개별 최솟값·최댓값의 합이 동시에 실현되는지 다시 확인해야 한다.'
   q['pitfall']='‘증감’이라는 말만으로 항상 절댓값을 취하지 않는다. 증가·감소의 크기 제한인지 부호 있는 증감률의 상한인지 먼저 구별한다.'
  q['revision']+=1;touched=True
  changes.append(dict(id=q['id'],file=p.relative_to(r.ROOT).as_posix(),oldRevision=before['revision'],newRevision=q['revision'],changedFields=sorted(k for k in q.keys()|before.keys() if k!='revision' and q.get(k)!=before.get(k)),beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason='Original prose and source assets preserved; native readability, percent boundaries, substantive reasons and magnitude-interpretation limit clarified.',status='repaired_pending_reverification'))
 if touched:r.write(p,data)
assert len(changes)==5;r.write(r.OUT/'changes-batch30.json',changes)
r.write(b/'interpretation-review.json',dict(id='kr-mpm-2026-07-18-psat-d-24',originalOnlyRecordedBeforeReveal=True,ownSolveReceipt='solve-frozen-before-reveal.json',existingExplanationAlreadyUsedMagnitude=True,noExistingAddedAppCondition=True,rawDialogueUnaltered=True,rawSourceSignedUpperOnly=[75,850],magnitudeInterpretation=[675,850],change='Clarified interpretation in authored explanation only; did not add an absolute-value condition to the original problem.',relatedEarlierReview='batch15: d22 explicit pre-existing app condition is different; do not conflate.'))
print('Frozen45/50;5 repairs applied, raw dialogue unchanged.')
