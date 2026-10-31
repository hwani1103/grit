import review_remaining605 as r
b=r.folder(50);assert not (b/'batch-verification.json').exists()
for n in ['host-before.log','related295-host-before.log','underline-final.log']:assert 'All tests passed!' in (b/n).read_text(encoding='utf-8-sig')
log=(b/'host-after.log').read_text(encoding='utf-8-sig');assert '+9 -1: Some tests failed.' in log and log.count('[E]')==1 and 'underline_boundary_test.dart: original underline strokes' in log
for file,receipt,key in [('own-solves.json','solve-frozen-before-reveal.json','solveFileSha256'),('ratings-before.json','ratings-frozen.json','ratingsSha256'),('related295-own-solves.json','related295-solve-frozen.json','sha256')]:assert r.sha(b/file)==r.read(b/receipt)[key]
for n in ['source-key-checks.json','related295-source-key-checks.json','exact-model-checks.json','repair-semantic-checks.json','preservation-check.json']:assert r.read(b/n)['status']=='PASS'
changes=r.read(r.OUT/'changes-batch50.json')
for x in changes:x['status']='verified'
r.write(r.OUT/'changes-batch50.json',changes)
ids={x['id'] for x in r.read(b/'own-solves.json')+r.read(b/'related295-own-solves.json')}
for p in r.OUT.glob('cross-candidates-*.json'):
 v=r.read(p);rows=v if isinstance(v,list) else v.get('candidates',[]);changed=False
 for x in rows:
  if isinstance(x,dict) and x.get('id') in ids:
   x.update(status='source_semantics_and_host_reverified',evidence='batch50/batch-verification.json');changed=True
   if p.name=='cross-candidates-underline-tail49.json':x.update(status='source_particle_excluded_and_host_reverified',evidence='batch50/exact-model-checks.json')
 if changed:r.write(p,v)
p=r.OUT/'cross-validation.json';v=r.read(p)
for x in v['findings']:
 if x['id'] in ['R605-003','R605-005','R605-006','R605-008','R605-009']:x.setdefault('subsequentBatchRepairs',[]).append(dict(batch=50,ids=sorted(ids),evidence='batch50/batch-verification.json'))
for x in r.read(b/'related295-assessment-before.json'):v['relatedPrior295Reviews'].append(dict(id=x['id'],batch=50,causeFamilies=['source-raster-prose','source-reading-order','underline-terminal-particle','conditional-counterexample'],evidence='batch50/related295-source-key-checks.json',status='source_key_semantics_and_host_reverified',historicalScorePreserved=x['historicalScorePreserved'],currentAssessmentBeforeRepair=x['currentBeforeScore']))
r.write(p,v)
p=r.OUT/'source-changes-batch27.json';v=r.read(p);v[0]['status']='verified';v[0]['subsequentChanges'][-1].update(status='verified',verification='batch50/batch-verification.json');r.write(p,v)
r.write(b/'visual-review.json',dict(status='PASS',before='All10 originals, all10 before-starts, both related source pages and both related-before-starts inspected.',after='All12 after-starts1..3 and4 detail screenshots inspected; source table now after clause2 before clause3; native age rules precede table then dialogue; revised underline leaves particle outside.',hostNotDevice=True))
r.write(b/'test-repair-receipt.json',dict(initial='host-after.log',initialPassed=9,initialFailed=1,cause='New l16 fixture contains <논증>; existing renderer removes named-label brackets. Underline range assertion passed but full-text expectation omitted this established formatting rule.',fix='Expected plain text includes existing <논증> -> 논증 presentation; no application change from this test failure.',final='underline-final.log',finalPassed=2,finalFailed=0,scope='Six viewport/zoom audit checks plus prefix-order and existing report-order checks passed in initial run. Only boundary file rerun.'))
r.write(b/'batch-verification.json',dict(status='verified',verifiedAt=r.now(),count=10,ownSolves='own-solves.json',solveFrozenReceipt='solve-frozen-before-reveal.json',ratings='ratings-before.json',frozenRatingsReceipt='ratings-frozen.json',beforeScoreTotal=46,beforeMean=4.6,targetQuestionsChanged=4,relatedPrior295Rechecked=2,relatedPrior295Changed=2,sourceKeyModels=['source-key-checks.json','related295-source-key-checks.json','exact-model-checks.json'],repairChecks='repair-semantic-checks.json',hostLogs=['host-before.log','related295-host-before.log','host-after.log','underline-final.log'],hostSuccessfulTestCount=23,hostInitialFailureAndResolution='test-repair-receipt.json',afterHostScope='All12 questions in6-check audit; prefix/report order checks; underline2finalPASS',visualReview='visual-review.json',preservation='preservation-check.json',solvesFrozenBeforeReveal=10,previouslyExposedOfficialAnswers=0,relatedKnownAnswerBeforeSolve=['kr-mpm-2026-07-18-psat-l-16'],firstPassAnswerMatches=10,firstPassReasoningCorrections=0,limitations='Same-author review, not independent. Related l16 answer exposed before solve; recorded separately. No intermediate APK.'))
print('Batch50 verified10;500 total after refresh')
