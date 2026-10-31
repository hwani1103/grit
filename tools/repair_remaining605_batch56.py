import re
import review_remaining605 as r
b=r.folder(56);old={x['question']['id']:x['question'] for x in r.read(b/'revealed-current.json')};related={q['id']:q for q in r.read(b/'related295-before.json')}
for n in ['host-before.log','related295-host-before.log']:assert 'All tests passed!' in (b/n).read_text(encoding='utf-8-sig')
for n in ['source-key-checks.json','related295-source-key-checks.json','pre-reveal-exact-models.json','related295-pre-reveal-models.json']:assert r.read(b/n)['status']=='PASS'
notes=['재량/의무와취소사유·기간정확. 해설의제⑤항을제5항으로인용표기정정.','허가대상과통보범위/귀속주체/부담금종류및감면위임근거정확.','정의와등록대상제외/협약예외/180일과궤도90일정확. 원문줄바꿈으로분리된기관명결합.','제재행위와대상/처분권자/교환또는환급/신고주체정확.','12일과4개월/가맹본부와가맹점주체구별/계약전청구정확.','네사용률합1/10및정의반박스조건정확;원문세로분수시각확인.','제작9번째와국내8번째/선개봉1·지연2보정정확. 영화명괄호·조사공백과주목받아서표기개선.','마지막동점뒤득점과상대최종점수초과구별/전체타임라인정확.','선행조건보존정렬/정책예외제외/다섯번째기사정확. 기존호스트는조건을표보다먼저표시하여변경불필요.','1024그래프중유효2개모두직접조약/우호/친밀/중립구분일치.']
fix={i for i,q in old.items() if q['number'] in [1,3,8]};ratings=[dict(id=i,scoreBeforeFix=4 if i in fix else 5,assessment=n,needsChange=i in fix) for i,n in zip(old,notes)]
assert not (b/'ratings-before.json').exists();r.write(b/'ratings-before.json',dict(method='All10 current-pass original solves frozen before reveal; full source/native/key, five options and host inspected.',ratings=ratings));r.write(b/'ratings-frozen.json',dict(frozenAt=r.now(),ratingsSha256=r.sha(b/'ratings-before.json'),total=47,count=10,beforeChanges=True))
hist={x['id']:x for x in r.read(r.PREP/'previously-scored295.json')['questions']}
r.write(b/'related295-assessment-before.json',[dict(id=i,historicalScorePreserved=hist[i]['scoreBeforeFix'],currentBeforeScore=5,assessment='두재원배분분리와기타54/공공66/32%전선지정확.' if q['number']==6 else '정수몫점수68/94/77/93/79와80점선정경계/11+6지급/최대3팀조건정확.',notReplacementOfHistoricalScore=True,changed=False) for i,q in related.items()])
def clean(s):return s.replace('제⑤항','제5항').replace('과학기술 정보통신부장관','과학기술정보통신부장관').replace('< 베타빌 > 은','<베타빌>은').replace('< 베타빌 > 보다','<베타빌>보다').replace('< 베타빌 > 이다','<베타빌>이다').replace('주목 받아서','주목받아서')
changes=[]
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  i=q['id']
  if i not in fix:continue
  prev=old[i];assert q==prev;snap=r.OUT/f"before-changes/{i}-r{q['revision']}.json";assert not snap.exists();r.write(snap,prev)
  for k in ['body','choices','steps','optionReasons','pitfall','transfer']:
   q[k]=[clean(s) for s in q[k]] if isinstance(q[k],list) else clean(q[k])
  fields=[k for k in q if q[k]!=prev[k]];assert fields and q['answer']==prev['answer'] and q['figures']==prev['figures'];q['revision']+=1;touched=True
  changes.append(dict(id=i,file=p.relative_to(r.ROOT).as_posix(),oldRevision=prev['revision'],newRevision=q['revision'],changedFields=fields,beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason=next(x['assessment'] for x in ratings if x['id']==i),status='repaired_pending_reverification'))
 if touched:r.write(p,data)
assert len(changes)==3;r.write(r.OUT/'changes-batch56.json',changes)
r.write(b/'exact-model-checks.json',dict(status='PASS',sourceOnlyModels='pre-reveal-exact-models.json',relatedModels='related295-pre-reveal-models.json',originalVerticalFraction='s07 private-use numerator1,denominator2,fraction bar visually verified and explicitly mapped for source comparison.',ownDraftTypo='Related17 frozen reasoning has an awkward rank phrase; explicit pre-reveal scores imply B>D>E>C>A and only B,D eligible. Scores, eligibility, final amount and all five option reasons correct; frozen text retained.'))
r.write(b/'repair-semantic-checks.json',dict(status='PASS',targetChanged=3,relatedChanged=0,answersAndAllReasoningValuesUnchanged=True,changes='Citation numeral normalization and original word/particle spacing only.',s13Order='Existing native condition body already precedes candidate table; no layout change needed.'))
r.write(b/'after-sample.json',dict(sample=[dict(id=i) for i in list(old)+list(related)]))
print('47/50 frozen;3 typography repairs;2 related current5 unchanged')
