import review_remaining605 as r
b=r.folder(34);logs=['host-before.log','host-after.log','related295-host-before.log','related295-host-after.log']
for name in logs:assert 'All tests passed!' in (b/name).read_text(encoding='utf-8-sig')
assert r.sha(b/'ratings-before.json')==r.read(b/'ratings-frozen.json')['ratingsSha256']
assert r.sha(b/'own-solves.json')==r.read(b/'solve-frozen-before-reveal.json')['solveFileSha256']
assert r.sha(b/'related295-own-solves.json')==r.read(b/'related295-solve-frozen.json')['sha256']
for name in ['source-key-model-checks.json','repair-semantic-checks.json','related295-source-key-model-checks.json','preservation-check.json']:assert r.read(b/name)['status']=='PASS'
changes=r.read(r.OUT/'changes-batch34.json');ids={x['id'] for x in changes}
for x in changes:x['status']='verified'
r.write(r.OUT/'changes-batch34.json',changes)
p=r.OUT/'cross-candidates-underline-object34.json';v=r.read(p)
for x in v['candidates']:
 assert x['id'] in ids;x.update(status='source_semantics_and_host_reverified',evidence='batch34/repair-semantic-checks.json')
v['status']='exact_candidate_scope_closed';r.write(p,v)
p=r.OUT/'cross-candidates-word-unit-and-conditional-direction.json';v=r.read(p)
for x in v['candidates']:
 if x['id'] in ids:x.update(status='source_semantics_and_host_reverified',evidence='batch34/batch-verification.json')
r.write(p,v)
p=r.OUT/'cross-validation.json';v=r.read(p)
for x in v['findings']:
 if x['id'] in ['R605-003','R605-006','R605-013','R605-016']:
  relevant={'R605-003':['kr-mpm-2026-03-07-psat-l-08','kr-mpm-2026-03-07-psat-l-12','2023-07-22-l-11'],'R605-006':['kr-mpm-2026-03-07-psat-l-07'],'R605-013':sorted(ids-{'kr-mpm-2026-03-07-psat-l-12'}),'R605-016':['2023-07-22-l-11']}[x['id']]
  x.setdefault('subsequentBatchRepairs',[]).append(dict(batch=34,ids=relevant,evidence='batch34/batch-verification.json'))
  if x['id']=='R605-006':x.setdefault('additionalScopes',[]).append('cross-candidates-underline-object34.json')
v['relatedPrior295Reviews'].append(dict(id='2023-07-22-l-11',batch=34,causeFamilies=['R605-003','R605-013','R605-016'],evidence='batch34/related295-source-key-model-checks.json',status='source_key_semantics_and_host_reverified',historicalScorePreserved=4,currentAssessmentBeforeRepair=4))
r.write(p,v)
r.write(b/'visual-review.json',dict(status='PASS',before='All10 target initial screens before-starts1..3 and related295 initial screen inspected.',after='All10 target initial screens after-starts1..3, prose/underline/word/option-reason details after-details1..3, l08/l12 page04, related295 start/page04/page05 inspected. Native sentence joining, full source underline excluding period, probability upper-bound caveat and individual reasons readable.',hostNotDevice=True))
r.write(b/'batch-verification.json',dict(status='verified',verifiedAt=r.now(),count=10,ownSolves='own-solves.json',solveFrozenReceipt='solve-frozen-before-reveal.json',ratings='ratings-before.json',frozenRatingsReceipt='ratings-frozen.json',beforeScoreTotal=44,beforeMean=4.4,targetQuestionsChanged=6,relatedPrior295RecheckedAndChanged=1,sourceKeyModels='source-key-model-checks.json',repairChecks='repair-semantic-checks.json',relatedChecks='related295-source-key-model-checks.json',hostLogs=logs,hostSuccessfulTestCount=24,visualReview='visual-review.json',preservation='preservation-check.json',solvesFrozenBeforeReveal=10,previouslyExposedOfficialAnswers=0,firstPassAnswerMatches=10,firstPassReasoningCorrections=0,limitations='Same-author review. Exact underline-object candidate scope closed; other broader cross queues pending. Final release only after full completion.'))
print('Batch34 verified10; cumulative340 after refresh.')
