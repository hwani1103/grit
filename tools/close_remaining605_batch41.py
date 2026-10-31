import review_remaining605 as r
b=r.folder(41);assert not (b/'batch-verification.json').exists()
logs=['host-before.log','host-after.log','related295-host-before.log','related295-host-after.log']
for name in logs:assert 'All tests passed!' in (b/name).read_text(encoding='utf-8-sig')
for file,receipt,key in [('own-solves.json','solve-frozen-before-reveal.json','solveFileSha256'),('ratings-before.json','ratings-frozen.json','ratingsSha256'),('related295-own-solves.json','related295-solve-frozen.json','sha256')]:assert r.sha(b/file)==r.read(b/receipt)[key]
for name in ['source-key-model-checks.json','repair-semantic-checks.json','related295-source-key-checks.json','related295-repair-model-checks.json','preservation-check.json']:assert r.read(b/name)['status']=='PASS'
changes=r.read(r.OUT/'changes-batch41.json');ids={x['id'] for x in changes}
for x in changes:x['status']='verified'
r.write(r.OUT/'changes-batch41.json',changes)
for name in ['cross-candidates-word-unit-and-conditional-direction.json','cross-candidates-situation-raster-body.json']:
 p=r.OUT/name;v=r.read(p);rows=v if isinstance(v,list) else v.get('candidates',[])
 for x in rows:
  if x['id'] in ids:x.update(status='source_semantics_and_host_reverified',evidence='batch41/batch-verification.json')
 r.write(p,v)
p=r.OUT/'cross-validation.json';v=r.read(p)
for x in v['findings']:
 if x['id'] in ['R605-008','R605-013']:x.setdefault('subsequentBatchRepairs',[]).append(dict(batch=41,ids=sorted(ids),evidence='batch41/batch-verification.json'))
for x in r.read(b/'related295-assessment-before.json'):v['relatedPrior295Reviews'].append(dict(id=x['id'],batch=41,causeFamilies=['word-boundary','date-exception','percentage-base-and-rank'],evidence='batch41/related295-repair-model-checks.json',status='source_key_semantics_and_host_reverified',historicalScorePreserved=x['historicalScorePreserved'],currentAssessmentBeforeRepair=x['currentBeforeScore']))
r.write(p,v)
r.write(b/'visual-review.json',dict(status='PASS',before='All10 before-starts1..3 and related295-before-starts1 inspected; original all10+2 images viewed.',after='All10 after-starts1..3 and after-prose checked; both original geometry table crops viewed; related295-after-starts1 inspected.',hostNotDevice=True))
r.write(b/'batch-verification.json',dict(status='verified',verifiedAt=r.now(),count=10,ownSolves='own-solves.json',solveFrozenReceipt='solve-frozen-before-reveal.json',ratings='ratings-before.json',frozenRatingsReceipt='ratings-frozen.json',beforeScoreTotal=44,beforeMean=4.4,targetQuestionsChanged=6,relatedPrior295RecheckedAndChanged=2,sourceKeyModels='source-key-model-checks.json',repairChecks='repair-semantic-checks.json',relatedChecks='related295-repair-model-checks.json',hostLogs=logs,hostSuccessfulTestCount=24,visualReview='visual-review.json',preservation='preservation-check.json',solvesFrozenBeforeReveal=10,previouslyExposedOfficialAnswers=0,firstPassAnswerMatches=10,firstPassReasoningCorrections=0,limitations='Same-author review, not independent. Original-only exhaustive code and epistemic models; unchanged solar power/energy source notation with physical distinction retained. Remaining605/cross queues continue; no intermediateAPK.'))
print('Batch41 verified10;410 total after refresh')
