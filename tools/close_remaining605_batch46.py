import review_remaining605 as r
b=r.folder(46);assert not (b/'batch-verification.json').exists()
logs=['host-before.log','related295-host-before.log','host-after.log']
for n in logs:assert 'All tests passed!' in (b/n).read_text(encoding='utf-8-sig')
for file,receipt,key in [('own-solves.json','solve-frozen-before-reveal.json','solveFileSha256'),('ratings-before.json','ratings-frozen.json','ratingsSha256'),('related295-own-solves.json','related295-solve-frozen.json','sha256')]:assert r.sha(b/file)==r.read(b/receipt)[key]
for n in ['source-key-model-checks.json','related295-source-key-model-checks.json','repair-semantic-checks.json','preservation-check.json']:assert r.read(b/n)['status']=='PASS'
changes=r.read(r.OUT/'changes-batch46.json')
for x in changes:x['status']='verified'
r.write(r.OUT/'changes-batch46.json',changes)
ids={x['id'] for x in r.read(b/'own-solves.json')+r.read(b/'related295-own-solves.json')}
for p in r.OUT.glob('cross-candidates-*.json'):
 v=r.read(p);rows=v if isinstance(v,list) else v.get('candidates',[]);changed=False
 for x in rows:
  if isinstance(x,dict) and x.get('id') in ids:x.update(status='source_semantics_and_host_reverified',evidence='batch46/batch-verification.json');changed=True
 if changed:r.write(p,v)
p=r.OUT/'cross-validation.json';v=r.read(p)
for x in v['findings']:
 if x['id'] in ['R605-006','R605-013']:x.setdefault('subsequentBatchRepairs',[]).append(dict(batch=46,ids=sorted(ids),evidence='batch46/batch-verification.json',followup='cross-candidates-underline-period46.json:19 candidates, not yet cleared'))
for x in r.read(b/'related295-assessment-before.json'):v['relatedPrior295Reviews'].append(dict(id=x['id'],batch=46,causeFamilies=['conditional-direction','capacity-bound','underline-boundary'],evidence='batch46/related295-source-key-model-checks.json',status='source_key_semantics_and_host_reverified',historicalScorePreserved=x['historicalScorePreserved'],currentAssessmentBeforeRepair=x['currentBeforeScore']))
r.write(p,v)
r.write(b/'visual-review.json',dict(status='PASS',before='All10 original images and all10 before-starts1..3 plus both related originals/host starts inspected before repairs; case18 saved pages3/4 inspected.',after='All12 after-starts1..3 and after-detail inspected: reordered13 proof and options,15 both underline terminals, related16 labelled statements; no truncation observed.',hostNotDevice=True))
r.write(b/'batch-verification.json',dict(status='verified',verifiedAt=r.now(),count=10,ownSolves='own-solves.json',solveFrozenReceipt='solve-frozen-before-reveal.json',ratings='ratings-before.json',frozenRatingsReceipt='ratings-frozen.json',beforeScoreTotal=48,beforeMean=4.8,targetQuestionsChanged=2,relatedPrior295Rechecked=2,relatedPrior295Changed=0,sourceKeyModels=['source-key-model-checks.json','related295-source-key-model-checks.json'],repairChecks='repair-semantic-checks.json',hostLogs=logs,hostSuccessfulTestCount=18,afterHostScope='All12 target+related questions in one6-check audit',visualReview='visual-review.json',preservation='preservation-check.json',solvesFrozenBeforeReveal=10,previouslyExposedOfficialAnswers=10,firstPassAnswerMatches=10,firstPassReasoningCorrections=0,limitations='Same-author review, not independent or blind; all10 official keys were exposed historically. New19 underline-period candidates remain pending in global cross-validation queue. No intermediate APK.'))
print('Batch46 verified10;460 total after refresh')
