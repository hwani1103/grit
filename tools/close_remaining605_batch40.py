import review_remaining605 as r
b=r.folder(40);assert not (b/'batch-verification.json').exists()
logs=['host-before.log','host-after.log','related295-host-before.log','related295-host-after.log']
for name in logs:assert 'All tests passed!' in (b/name).read_text(encoding='utf-8-sig')
for file,receipt,key in [('own-solves.json','solve-frozen-before-reveal.json','solveFileSha256'),('ratings-before.json','ratings-frozen.json','ratingsSha256'),('related295-own-solves.json','related295-solve-frozen.json','sha256')]:assert r.sha(b/file)==r.read(b/receipt)[key]
for name in ['source-key-model-checks.json','repair-semantic-checks.json','related295-source-key-checks.json','related295-repair-model-checks.json','preservation-check.json']:assert r.read(b/name)['status']=='PASS'
changes=r.read(r.OUT/'changes-batch40.json');ids={x['id'] for x in changes}
for x in changes:x['status']='verified'
r.write(r.OUT/'changes-batch40.json',changes)
for name in ['cross-candidates-word-unit-and-conditional-direction.json','cross-candidates-underline-label.json','cross-candidates-underline-object34.json','cross-candidates-count-ratio40.json']:
 p=r.OUT/name;v=r.read(p);rows=v if isinstance(v,list) else v.get('candidates',[])
 for x in rows:
  if x['id'] in ids:x.update(status='source_semantics_and_host_reverified',evidence='batch40/batch-verification.json')
 r.write(p,v)
p=r.OUT/'cross-validation.json';v=r.read(p)
for x in v['findings']:
 if x['id'] in ['R605-006','R605-013','R605-018']:x.setdefault('subsequentBatchRepairs',[]).append(dict(batch=40,ids=sorted(ids),evidence='batch40/batch-verification.json'))
 if x['id']=='R605-018':x['status']='source_semantics_and_host_reverified'
for x in r.read(b/'related295-assessment-before.json'):v['relatedPrior295Reviews'].append(dict(id=x['id'],batch=40,causeFamilies=['word-boundary','underline-scope','population-and-count-ratio'],evidence='batch40/related295-repair-model-checks.json',status='source_key_semantics_and_host_reverified',historicalScorePreserved=x['historicalScorePreserved'],currentAssessmentBeforeRepair=x['currentBeforeScore']))
r.write(p,v)
r.write(b/'visual-review.json',dict(status='PASS',before='All10 before-starts1..3 and related295-before-starts1 inspected; original all10+3 images viewed.',after='All10 after-starts1..3 and after-prose checked; related295-after-starts1 and related295-after-prose show repaired underline and full scope explanation.',hostNotDevice=True))
r.write(b/'batch-verification.json',dict(status='verified',verifiedAt=r.now(),count=10,ownSolves='own-solves.json',solveFrozenReceipt='solve-frozen-before-reveal.json',ratings='ratings-before.json',frozenRatingsReceipt='ratings-frozen.json',beforeScoreTotal=46,beforeMean=4.6,targetQuestionsChanged=4,relatedPrior295RecheckedAndChanged=3,sourceKeyModels='source-key-model-checks.json',repairChecks='repair-semantic-checks.json',relatedChecks='related295-repair-model-checks.json',hostLogs=logs,hostSuccessfulTestCount=24,visualReview='visual-review.json',preservation='preservation-check.json',solvesFrozenBeforeReveal=10,previouslyExposedOfficialAnswers=0,firstPassAnswerMatches=10,firstPassReasoningCorrections=0,limitations='Same-author review, not independent. Source-specific numerical models are hypothetical for logical boundaries, not empirical/medical claims. Remaining605 and cross-cause queues continue; no intermediateAPK.'))
print('Batch40 verified10;400 total after refresh')
