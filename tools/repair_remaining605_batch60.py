import review_remaining605 as r
b=r.folder(60); old={x['question']['id']:x['question'] for x in r.read(b/'revealed-current.json')}; related={q['id']:q for q in r.read(b/'related295-before.json')}
for n in ['host-before.log','related295-host-before.log']:assert 'All tests passed!' in (b/n).read_text(encoding='utf-8-sig')
notes={22:'증가율과 구성비의 분모 구별, 감소 다섯 요인과 6% 경계 정확.',23:'내급비 소득−순수익 항등식과 축종별 전체 비교 정확.',24:'잔여 재활용량·윤년366일·재활용률 차의 서로 다른 분모 정확.',25:'남녀 합계/소년 구성비/소년과 성인 증가율 계열 구별 정확.',26:'대학당 가중 평균과 600백만원 상한 비교 정확. 실전 풀이의 모두 이하라는 표현을 대학당 평균 이하로 명확화.',29:'수입 복원·기금 잔여와 증가율/구성비 분모 정확.',30:'대졸 미만4명 제외한296명 분모와 비례43명, 보고서와 다섯 도표 대응 정확.',31:'편차합0과 제곱합의 두 해/극값 정확. 빈칸 값은가 띄어쓰기 개선.',32:'네 기업 평균3·6·11·10 복원과 요일 개수/평균합 비교 정확.',34:'남녀 후보/당선 분모와 당선자0 제외 성비, 교차 곱 경계 정확.'}
ratings=[dict(id=i,scoreBeforeFix=4 if q['number'] in [26,31] else 5,assessment=notes[q['number']],needsChange=q['number'] in [26,31]) for i,q in old.items()]
assert not (b/'ratings-before.json').exists();r.write(b/'ratings-before.json',dict(method='Original own10 and exact models frozen before reveal; all original regions, five choices and host starts inspected.',ratings=ratings));r.write(b/'ratings-frozen.json',dict(frozenAt=r.now(),ratingsSha256=r.sha(b/'ratings-before.json'),total=48,count=10,beforeChanges=True))
hist={x['id']:x for x in r.read(r.PREP/'previously-scored295.json')['questions']}
r.write(b/'related295-assessment-before.json',[dict(id=i,historicalScorePreserved=hist[i]['scoreBeforeFix'],currentBeforeScore=5,assessment={19:'최소 두 번째와 감소폭/율 구별 정확.',10:'여성 반영비율과 건수 가중 평균 정확. 기존 반올림 오차 상한79.70일도80일 미만.',14:'가입수 중복 하한/최대2제도/1인당 구좌와15개 지역 평균 정확. 총회원 반올림+500명에서도 중복 하한20078명으로2만명 초과.'}[q['number']],notReplacementOfHistoricalScore=True,changed=False) for i,q in related.items()])
changes=[]
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  if q['id'] not in old or q['number'] not in [26,31]:continue
  prev=old[q['id']];assert q==prev;snap=r.OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();r.write(snap,prev)
  if q['number']==26:
   assert '모두 6억 원 이하라면' in q['steps'][1];q['steps'][1]=q['steps'][1].replace('모두 6억 원 이하라면','대학당 평균이 6억 원 이하라면')
  else:
   assert '빈칸 값은가=3' in q['optionReasons'][0];q['optionReasons'][0]=q['optionReasons'][0].replace('빈칸 값은가=3','빈칸 값은 가=3')
  fields=[k for k in q if q[k]!=prev.get(k)];q['revision']+=1;touched=True;changes.append(dict(id=q['id'],file=p.relative_to(r.ROOT).as_posix(),oldRevision=prev['revision'],newRevision=q['revision'],changedFields=fields,beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason=notes[q['number']],status='repaired_pending_reverification'))
 if touched:r.write(p,data)
assert len(changes)==2;r.write(r.OUT/'changes-batch60.json',changes)
r.write(b/'repair-semantic-checks.json',dict(status='PASS',targetChanged=2,relatedChanged=0,allAnswersUnchanged=True,allSourceBodiesChoicesFiguresUnchanged=True,models=['pre-reveal-exact-models.json','related295-pre-reveal-models.json']))
r.write(b/'after-sample.json',dict(sample=[dict(id=i) for i in list(old)+list(related)]));print('48/50 frozen;2 repairs;3 prior295 unchanged')
