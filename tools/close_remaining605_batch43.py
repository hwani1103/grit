import review_remaining605 as r
b=r.folder(43);assert not (b/'batch-verification.json').exists()
for name in ['host-before.log','related295-host-before.log','underline-boundary-final.log']:
 assert 'All tests passed!' in (b/name).read_text(encoding='utf-8-sig')
mixed=(b/'host-after.log').read_text(encoding='utf-8-sig')
assert '+7 -1' in mixed and '<보 기>' in mixed
for file,receipt,key in [('own-solves.json','solve-frozen-before-reveal.json','solveFileSha256'),('ratings-before.json','ratings-frozen.json','ratingsSha256'),('related295-own-solves.json','related295-solve-frozen.json','sha256')]:assert r.sha(b/file)==r.read(b/receipt)[key]
for name in ['source-key-model-checks.json','related295-source-key-model-checks.json','repair-semantic-checks.json','preservation-check.json']:assert r.read(b/name)['status']=='PASS'
changes=r.read(r.OUT/'changes-batch43.json')
for x in changes:x['status']='verified'
r.write(r.OUT/'changes-batch43.json',changes)
ids={x['id'] for x in r.read(b/'own-solves.json')+r.read(b/'related295-own-solves.json')}
for p in r.OUT.glob('cross-candidates-*.json'):
 v=r.read(p);rows=v if isinstance(v,list) else v.get('candidates',[]);changed=False
 for x in rows:
  if isinstance(x,dict) and x.get('id') in ids:
   x.update(status='source_semantics_and_host_reverified',evidence='batch43/batch-verification.json');changed=True
 if changed:r.write(p,v)
p=r.OUT/'cross-validation.json';v=r.read(p)
for x in v['findings']:
 if x['id'] in ['R605-006','R605-013']:x.setdefault('subsequentBatchRepairs',[]).append(dict(batch=43,ids=sorted(ids),evidence='batch43/batch-verification.json'))
for x in r.read(b/'related295-assessment-before.json'):v['relatedPrior295Reviews'].append(dict(id=x['id'],batch=43,causeFamilies=['conditional-direction','shared-passage-scope'],evidence='batch43/related295-source-key-model-checks.json',status='source_key_semantics_and_host_reverified',historicalScorePreserved=x['historicalScorePreserved'],currentAssessmentBeforeRepair=x['currentBeforeScore']))
r.write(p,v)
r.write(b/'unit-harness-correction.json',dict(status='PASS',initialLog='host-after.log',initialResult='Six audit checks and one underline unit check passed; one plaintext expectation failed because existing renderer normalizes <보 기> to 보 기.',repair='Expected plaintext now follows existing heading normalization. App code unchanged.',finalLog='underline-boundary-final.log',finalResult='Both underline unit checks passed. Original mixed failure log retained.'))
r.write(b/'visual-review.json',dict(status='PASS',before='All10 original source images, all10 before-starts1..3, and both related source/host starts inspected.',after='All10 after-starts1..3 and after-detail inspected, covering28 blank particle,35 compound spacing,36 experiment heading,37 O/X table;30 underline restricted to four letters confirmed against PDF stroke.',hostNotDevice=True))
r.write(b/'batch-verification.json',dict(status='verified',verifiedAt=r.now(),count=10,ownSolves='own-solves.json',solveFrozenReceipt='solve-frozen-before-reveal.json',ratings='ratings-before.json',frozenRatingsReceipt='ratings-frozen.json',beforeScoreTotal=46,beforeMean=4.6,targetQuestionsChanged=4,relatedPrior295Rechecked=2,relatedPrior295Changed=0,sourceKeyModels=['source-key-model-checks.json','related295-source-key-model-checks.json'],repairChecks='repair-semantic-checks.json',hostLogs=['host-before.log','host-after.log','related295-host-before.log','underline-boundary-final.log'],hostSuccessfulTestCount=20,harnessCorrection='unit-harness-correction.json',visualReview='visual-review.json',preservation='preservation-check.json',solvesFrozenBeforeReveal=10,previouslyExposedOfficialAnswers=2,firstPassAnswerMatches=10,firstPassReasoningCorrections=0,limitations='Same-author review, not independent. Eight previously unexposed answers and two prior key exposures. No intermediate APK.'))
print('Batch43 verified10;430 total after refresh')
