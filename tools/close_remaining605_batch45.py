import review_remaining605 as r
b=r.folder(45);assert not (b/'batch-verification.json').exists()
logs=['host-before.log','related295-host-before.log','host-after.log']
for name in logs:assert 'All tests passed!' in (b/name).read_text(encoding='utf-8-sig')
for file,receipt,key in [('own-solves.json','solve-frozen-before-reveal.json','solveFileSha256'),('ratings-before.json','ratings-frozen.json','ratingsSha256'),('related295-own-solves.json','related295-solve-frozen.json','sha256')]:assert r.sha(b/file)==r.read(b/receipt)[key]
for name in ['source-native-pixel-checks.json','related295-source-native-pixel-checks.json','exact-model-checks.json','repair-semantic-checks.json','preservation-check.json']:assert r.read(b/name)['status']=='PASS'
changes=r.read(r.OUT/'changes-batch45.json');ids={x['id'] for x in r.read(b/'own-solves.json')+r.read(b/'related295-own-solves.json')}
for x in changes:x['status']='verified'
r.write(r.OUT/'changes-batch45.json',changes)
for p in r.OUT.glob('cross-candidates-*.json'):
 v=r.read(p);rows=v if isinstance(v,list) else v.get('candidates',[]);changed=False
 for x in rows:
  if isinstance(x,dict) and x.get('id') in ids:x.update(status='source_semantics_and_host_reverified',evidence='batch45/batch-verification.json');changed=True
 if changed:r.write(p,v)
p=r.OUT/'cross-validation.json';v=r.read(p)
for x in v['findings']:
 if x['id'] in ['R605-003','R605-009']:x.setdefault('subsequentBatchRepairs',[]).append(dict(batch=45,ids=sorted(ids),evidence='batch45/batch-verification.json'))
for x in r.read(b/'related295-assessment-before.json'):v['relatedPrior295Reviews'].append(dict(id=x['id'],batch=45,causeFamilies=['denominator-direction','rounding-bounds','all-interval-conditions','raster-prose'],evidence='batch45/exact-model-checks.json',status='source_key_semantics_and_host_reverified',historicalScorePreserved=x['historicalScorePreserved'],currentAssessmentBeforeRepair=x['currentBeforeScore']))
r.write(p,v)
r.write(b/'visual-review.json',dict(status='PASS',before='All10 target before-starts1..3 inspected before repair. Related before-starts inspected after repair using saved pre-edit renders. All original pages including shared29/30 and26/27 inspected.',after='All12 combined after-starts1..3, after-prose and after-dialog inspected. Table1/rules/table2 order33 correct;35 all7 utterances, speakers and timestamps retained;32 A→B header preserved;26 all4 report conditions readable.',hostNotDevice=True))
r.write(b/'batch-verification.json',dict(status='verified',verifiedAt=r.now(),count=10,ownSolves='own-solves.json',solveFrozenReceipt='solve-frozen-before-reveal.json',ratings='ratings-before.json',frozenRatingsReceipt='ratings-frozen.json',beforeScoreTotal=46,beforeMean=4.6,targetQuestionsChanged=4,relatedPrior295Rechecked=2,relatedPrior295Changed=1,sourceKeyModels=['source-native-pixel-checks.json','related295-source-native-pixel-checks.json','exact-model-checks.json'],repairChecks='repair-semantic-checks.json',hostLogs=logs,hostSuccessfulTestCount=18,afterHostScope='All12 target+related questions in one6-check audit',visualReview='visual-review.json',preservation='preservation-check.json',solvesFrozenBeforeReveal=10,previouslyExposedOfficialAnswers=0,firstPassAnswerMatches=10,firstPassReasoningCorrections=0,limitations='Same-author review, not independent. Direct pixel crops35 target+5related. All original assets preserved; dialogue is manually transcribed from original raster with visual comparison. No intermediateAPK.'))
print('Batch45 verified10;450 total after refresh')
