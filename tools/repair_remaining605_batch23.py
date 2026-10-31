import review_remaining605 as r
b=r.folder(23);before={x['question']['id']:x['question'] for x in r.read(b/'revealed-current.json')};related=r.read(b/'related295-shared10-before.json');before[related['id']]=related
assessments=[
(6,4,'바닥 포함24와 접촉12쌍 계산은 정확하다. 다만 최소라는 단정에 하한 근거를 덧붙이면 구성 예와 최소성의 차이가 분명해진다.','정석 근거에 세 방향 투영을 이용한 노출면 하한24를 추가한다.'),
(7,5,'손배열을 먼저 역추적하고 직전승자만 계승한다.24가지乙배열 중 유일배열과乙3승이 일치한다.','발견 없음. 첫회·직전무승부·일반승패의 적용범위가 정확하다.'),
(9,4,'사회적관련성,WHO직업분류,고소득방향,번아웃과FOMO특징을 정확히 구별한다.','공통 지문의25 %·20 %·40 %에서 수치와기호가분리되지않도록 공백을 제거한다.'),
(11,5,'임명주체·비위원간사·최소7명·과반수6명·선택자격을 조문에 따라 구별한다.','발견 없음. 회의 구성수와 출석수 및 찬성수 기준이 정확하다.'),
(13,5,'월별열거에서2022년7개월+2024년6개월=13개월.선발·휴직·퇴직다음달과복직그달 경계를 정확히 처리한다.','발견 없음. 휴직18개월 전체를 빼지 않는 경고가 적절하다.'),
(14,5,'수출입 방향과 중국 유래 증거 방향을 구별하고 정착·지도 근거로ㄷㄹ을 선택한다.','발견 없음. 기록의 존재와 실제 지리·기원 확증을 구별한다.'),
(17,5,'상한6과8·7·6·1의달성예를 모두 제시한다.0세허용 여부에 결론이 불변이며 완전열거도 최대6이다.','발견 없음. 첫째아들이 셋째자녀라는 순서와 정수나이 전제를 명확히 한다.'),
(19,5,'전시면적·세미나정원·C분할·특정시설만 할인 조건을 보존하며 모든 적격쌍 중E/B3500이 유일최소다.','발견 없음. 표의 모든 셀·단위·배치와 전시→세미나 선택지 머리말을 대조했다.'),
(20,5,'총점32/32/30/32/32 후 제조사8점A·D,가격점수9대7로A.가격구간2500·4000경계도 정확하다.','발견 없음. 다섯 표의 셀과 배치가 원문과 대응하고 실제가격과 점수를 구별한다.'),
(21,5,'신규누적136-해제62=74,순증누적도74.2025년1월 이후11월까지 동일함을 정확히 설명한다.','발견 없음. 신규·순증·보유수와 수열의 적용대상을 구별한다.')]
ratings=[dict(id=f'kr-mpm-2025-11-15-psat-s-{n:02}',scoreBeforeFix=score,assessment=a,deduction=d,needsChange=score<5) for n,score,a,d in assessments]
assert not (b/'ratings-before.json').exists()
r.write(b/'ratings-before.json',dict(method='Same-author individual pre-edit original/own solve/key/calculation/host review; no independent reviewer claim.',ratings=ratings))
r.write(b/'ratings-frozen.json',dict(frozenAt=r.now(),ratingsSha256=r.sha(b/'ratings-before.json'),total=48,count=10,beforeChanges=True))
changes=[]
for path in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(path)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  if q['id'] not in before or q['number'] not in [6,9,10]:continue
  old=before[q['id']];assert old==q
  snap=r.OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();r.write(snap,old)
  if q['number']==6:
   q['steps'][3]='정석 근거: 전체 48면에서 맞닿은 12쌍의 양쪽 면을 빼면 48－2×12＝24다. 최소성도 확인할 수 있다. 세 방향 투영에 보이는 격자 칸 수를 a, b, c라 하면 격자 입체의 투영 부등식으로 abc≥8²이다. 각 투영 칸의 앞뒤 끝에 적어도 두 면이 노출되므로 전체 노출면은 2(a＋b＋c) 이상이다. 산술·기하평균 부등식으로 a＋b＋c는 abc의 세제곱근의 3배 이상이며, abc≥64이므로 a＋b＋c≥12다. 따라서 노출면은 24개 이상이고 2×2×2 배치가 이 하한을 달성한다.'
  else:
   assert all(f'{v} %' in q['body'] for v in [25,20,40])
   for v in [25,20,40]:q['body']=q['body'].replace(f'{v} %',f'{v}%')
  q['revision']+=1;touched=True
  changes.append(dict(id=q['id'],file=path.relative_to(r.ROOT).as_posix(),oldRevision=old['revision'],newRevision=q['revision'],changedFields=[k for k in q if k!='revision' and q[k]!=old.get(k)],beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason='최소성의 하한 증명 추가 또는 원문 백분율 수치·기호 경계 복원. 원문·정답·보기·기존 기록은 보존.',status='repaired_pending_reverification'))
 if touched:r.write(path,data)
assert len(changes)==3
r.write(r.OUT/'changes-batch23.json',changes)
r.write(b/'related295-recheck.json',dict(id=related['id'],historicalScorePreserved=True,originalOwnSolveReceipt='related295-own-solves-receipt.json',ownAndOfficialAnswer=2,assessment='1990경험자100만→공통여성50만→2000경험자200만.40%는전체인구역산에만필요.5선지와5단계해설정확;공통지문백분율공백3곳만복원.',reason='Current605s09 shared-passage spacing issue checked bidirectionally in prior295s10.'))
print('Frozen48/50; two targets and one prior295 repaired, revisions advanced.')
