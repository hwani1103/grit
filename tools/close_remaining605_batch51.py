import review_remaining605 as r
b=r.folder(51);assert not (b/'batch-verification.json').exists()
logs=['host-before.log','related295-host-before.log','host-after.log']
for n in logs:assert 'All tests passed!' in (b/n).read_text(encoding='utf-8-sig')
for file,receipt,key in [('own-solves.json','solve-frozen-before-reveal.json','solveFileSha256'),('ratings-before.json','ratings-frozen.json','ratingsSha256'),('related295-own-solves.json','related295-solve-frozen.json','sha256')]:assert r.sha(b/file)==r.read(b/receipt)[key]
for n in ['source-key-checks.json','related295-source-key-checks.json','exact-model-checks.json','repair-semantic-checks.json','preservation-check.json']:assert r.read(b/n)['status']=='PASS'
changes=r.read(r.OUT/'changes-batch51.json')
for x in changes:x['status']='verified'
r.write(r.OUT/'changes-batch51.json',changes)
ids={x['id'] for x in r.read(b/'own-solves.json')+r.read(b/'related295-own-solves.json')}
for p in r.OUT.glob('cross-candidates-*.json'):
 v=r.read(p);rows=v if isinstance(v,list) else v.get('candidates',[]);changed=False
 for x in rows:
  if isinstance(x,dict) and x.get('id') in ids:x.update(status='source_semantics_and_host_reverified',evidence='batch51/batch-verification.json');changed=True
 if changed:r.write(p,v)
p=r.OUT/'cross-validation.json';v=r.read(p)
for x in v['findings']:
 if x['id'] in ['R605-003','R605-009','R605-010','R605-011','R605-018']:x.setdefault('subsequentBatchRepairs',[]).append(dict(batch=51,ids=sorted(ids),evidence='batch51/batch-verification.json'))
for x in r.read(b/'related295-assessment-before.json'):v['relatedPrior295Reviews'].append(dict(id=x['id'],batch=51,causeFamilies=['source-raster-prose','shared-passage','all-series-chart-mapping','numeric-unit-spacing'],evidence='batch51/related295-source-key-checks.json',status='source_key_semantics_and_host_reverified',historicalScorePreserved=x['historicalScorePreserved'],currentAssessmentBeforeRepair=x['currentBeforeScore']))
r.write(p,v)
r.write(b/'visual-review.json',dict(status='PASS',before='All10 target source pages and all10 before-starts; related23/26 source pages were inspected within shared full pages11/13, and both related-before-starts inspected.',after='All12 after-starts and selected report/number-unit explanation details inspected; report after both source tables and before4candidate graphs, all originals retained.',hostNotDevice=True))
r.write(b/'batch-verification.json',dict(status='verified',verifiedAt=r.now(),count=10,ownSolves='own-solves.json',solveFrozenReceipt='solve-frozen-before-reveal.json',ratings='ratings-before.json',frozenRatingsReceipt='ratings-frozen.json',beforeScoreTotal=45,beforeMean=4.5,targetQuestionsChanged=5,relatedPrior295Rechecked=2,relatedPrior295Changed=2,sourceKeyModels=['source-key-checks.json','related295-source-key-checks.json','exact-model-checks.json'],repairChecks='repair-semantic-checks.json',hostLogs=logs,hostSuccessfulTestCount=18,afterHostScope='All12 target+related questions in one6-check audit',visualReview='visual-review.json',preservation='preservation-check.json',solvesFrozenBeforeReveal=10,previouslyExposedOfficialAnswers=0,firstPassAnswerMatches=10,firstPassReasoningCorrections=0,limitations='Same-author review, not independent. All source graphs checked against30fresh crops. No intermediate APK.'))
print('Batch51 verified10;510 total after refresh')
