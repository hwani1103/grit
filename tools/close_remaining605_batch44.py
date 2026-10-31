import review_remaining605 as r
b=r.folder(44);assert not (b/'batch-verification.json').exists()
logs=['host-before.log','related295-host-before.log','host-after.log']
for name in logs:assert 'All tests passed!' in (b/name).read_text(encoding='utf-8-sig')
for file,receipt,key in [('own-solves.json','solve-frozen-before-reveal.json','solveFileSha256'),('ratings-before.json','ratings-frozen.json','ratingsSha256'),('related295-own-solves.json','related295-solve-frozen.json','sha256')]:assert r.sha(b/file)==r.read(b/receipt)[key]
for name in ['source-key-checks.json','related295-source-key-checks.json','exact-model-checks.json','repair-semantic-checks.json','preservation-check.json']:assert r.read(b/name)['status']=='PASS'
changes=r.read(r.OUT/'changes-batch44.json');ids={x['id'] for x in r.read(b/'own-solves.json')+r.read(b/'related295-own-solves.json')}
for x in changes:x['status']='verified'
r.write(r.OUT/'changes-batch44.json',changes)
for p in r.OUT.glob('cross-candidates-*.json'):
 v=r.read(p);rows=v if isinstance(v,list) else v.get('candidates',[]);changed=False
 for x in rows:
  if isinstance(x,dict) and x.get('id') in ids:x.update(status='source_semantics_and_host_reverified',evidence='batch44/batch-verification.json');changed=True
 if changed:r.write(p,v)
p=r.OUT/'cross-validation.json';v=r.read(p)
for x in v['findings']:
 if x['id'] in ['R605-003','R605-008','R605-013']:x.setdefault('subsequentBatchRepairs',[]).append(dict(batch=44,ids=sorted(ids),evidence='batch44/batch-verification.json'))
for x in r.read(b/'related295-assessment-before.json'):v['relatedPrior295Reviews'].append(dict(id=x['id'],batch=44,causeFamilies=['integer-extrema','counterexample','word-boundary'],evidence='batch44/exact-model-checks.json',status='source_key_semantics_and_host_reverified',historicalScorePreserved=x['historicalScorePreserved'],currentAssessmentBeforeRepair=x['currentBeforeScore']))
r.write(p,v)
r.write(b/'visual-review.json',dict(status='PASS',before='All10 target before-starts1..3 inspected before repair. Related before-starts inspected after repair using saved pre-edit renders. All12 original source images inspected.',after='All12 combined after-starts1..3 and after-details inspected:28 fraction/body,32 word-list separation,36 stars/full rules/grammar,37 table/full conditions,38 particle. Related title-only change included in combined audit.',hostNotDevice=True))
r.write(b/'batch-verification.json',dict(status='verified',verifiedAt=r.now(),count=10,ownSolves='own-solves.json',solveFrozenReceipt='solve-frozen-before-reveal.json',ratings='ratings-before.json',frozenRatingsReceipt='ratings-frozen.json',beforeScoreTotal=44,beforeMean=4.4,targetQuestionsChanged=6,relatedPrior295Rechecked=2,relatedPrior295Changed=1,sourceKeyModels=['source-key-checks.json','related295-source-key-checks.json','exact-model-checks.json'],repairChecks='repair-semantic-checks.json',hostLogs=logs,hostSuccessfulTestCount=18,afterHostScope='All12 target+related questions in one6-check audit',visualReview='visual-review.json',preservation='preservation-check.json',solvesFrozenBeforeReveal=10,previouslyExposedOfficialAnswers=0,firstPassAnswerMatches=10,firstPassReasoningCorrections=0,extraCrossCheck='quoted-underline-followup.json',limitations='Same-author review, not independent. Original assets preserved, no intermediate APK.'))
print('Batch44 verified10;440 total after refresh')
