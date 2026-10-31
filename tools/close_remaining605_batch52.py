import review_remaining605 as r
b=r.folder(52);assert not (b/'batch-verification.json').exists()
logs=['host-before.log','related295-host-before.log','host-after.log']
for n in logs:assert 'All tests passed!' in (b/n).read_text(encoding='utf-8-sig')
for file,receipt,key in [('own-solves.json','solve-frozen-before-reveal.json','solveFileSha256'),('ratings-before.json','ratings-frozen.json','ratingsSha256'),('related295-own-solves.json','related295-solve-frozen.json','sha256')]:assert r.sha(b/file)==r.read(b/receipt)[key]
for n in ['source-key-checks.json','related295-source-key-checks.json','exact-model-checks.json','underline-source-strokes.json','repair-semantic-checks.json','preservation-check.json']:assert r.read(b/n)['status']=='PASS'
changes=r.read(r.OUT/'changes-batch52.json')
for x in changes:x['status']='verified'
r.write(r.OUT/'changes-batch52.json',changes)
ids={x['id'] for x in r.read(b/'own-solves.json')+r.read(b/'related295-own-solves.json')}
for p in r.OUT.glob('cross-candidates-*.json'):
 v=r.read(p);rows=v if isinstance(v,list) else v.get('candidates',[]);changed=False
 for x in rows:
  if isinstance(x,dict) and x.get('id') in ids:x.update(status='source_semantics_and_host_reverified',evidence='batch52/batch-verification.json');changed=True
 if changed:r.write(p,v)
p=r.OUT/'cross-validation.json';v=r.read(p)
for x in v['findings']:
 if x['id'] in ['R605-001','R605-003','R605-006','R605-007','R605-017']:x.setdefault('subsequentBatchRepairs',[]).append(dict(batch=52,ids=sorted(ids),evidence='batch52/batch-verification.json'))
for x in r.read(b/'related295-assessment-before.json'):v['relatedPrior295Reviews'].append(dict(id=x['id'],batch=52,causeFamilies=['underline-terminal-punctuation','conditional-logic','context-reference'],evidence='batch52/related295-source-key-checks.json',status='source_key_semantics_and_host_reverified',historicalScorePreserved=x['historicalScorePreserved'],currentAssessmentBeforeRepair=x['currentBeforeScore']))
r.write(p,v)
r.write(b/'exposure-clarification.json',dict(historicalKeyExposureCount=10,evidence='solve-frozen-before-reveal.json',clarification='Source-only refers to this batch original reasoning before current reveal; all10 had earlier key exposure and are not blind. Frozen ratings/own text retained. Related21l13 also on previously viewed2021 key page; no claim of blind related review.'))
r.write(b/'visual-review.json',dict(status='PASS',before='All10 original targets including shared39/40, both related originals and all12 before-starts inspected.',after='All12 after-starts and underline-detail screenshots inspected; terminal particles and punctuation kept outside underline; related21l13 circled anchor retained to avoid marking the repeated later occurrence.',hostNotDevice=True))
r.write(b/'batch-verification.json',dict(status='verified',verifiedAt=r.now(),count=10,ownSolves='own-solves.json',solveFrozenReceipt='solve-frozen-before-reveal.json',ratings='ratings-before.json',frozenRatingsReceipt='ratings-frozen.json',beforeScoreTotal=48,beforeMean=4.8,targetQuestionsChanged=2,relatedPrior295Rechecked=2,relatedPrior295Changed=2,sourceKeyModels=['source-key-checks.json','related295-source-key-checks.json','exact-model-checks.json'],repairChecks='repair-semantic-checks.json',hostLogs=logs,hostSuccessfulTestCount=20,afterHostScope='All12 in6-check audit plus2underline boundary checks',visualReview='visual-review.json',preservation='preservation-check.json',solvesFrozenBeforeReveal=10,previouslyExposedOfficialAnswers=10,firstPassAnswerMatches=10,firstPassReasoningCorrections=0,preFreezeReasoningCorrection='l34 draft5 corrected to4 by source-only exhaustive counterexample before own freeze/current reveal; app answer and reasoning already correct.',limitations='Same-author review, not independent or blind: all10 have historical key exposure recorded sincebatch04. No intermediate APK.'))
print('Batch52 verified10;520 total after refresh')
