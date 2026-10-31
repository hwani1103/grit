import review_remaining605 as r
b=r.folder(42);assert not (b/'batch-verification.json').exists()
logs=['host-before.log','host-after.log','related295-host-before.log','related295-host-after.log']
for name in logs:assert 'All tests passed!' in (b/name).read_text(encoding='utf-8-sig')
for file,receipt,key in [('own-solves.json','solve-frozen-before-reveal.json','solveFileSha256'),('ratings-before.json','ratings-frozen.json','ratingsSha256'),('related295-own-solves.json','related295-solve-frozen.json','sha256')]:assert r.sha(b/file)==r.read(b/receipt)[key]
for name in ['source-native-pixel-checks.json','exact-model-checks.json','repair-semantic-checks.json','related295-source-native-pixel-checks.json','related295-repair-model-checks.json','preservation-check.json']:assert r.read(b/name)['status']=='PASS'
changes=r.read(r.OUT/'changes-batch42.json');ids={x['id'] for x in r.read(b/'own-solves.json')+r.read(b/'related295-own-solves.json')}
for x in changes:x['status']='verified'
r.write(r.OUT/'changes-batch42.json',changes)
for name in ['cross-candidates-data-raster-prose.json','cross-candidates-structure-and-extrema.json','cross-candidates-choice-percent-boundaries24.json']:
 p=r.OUT/name;v=r.read(p);rows=v if isinstance(v,list) else v.get('candidates',[])
 for x in rows:
  if x['id'] in ids:x.update(status='source_semantics_and_host_reverified',evidence='batch42/batch-verification.json')
 r.write(p,v)
p=r.OUT/'cross-validation.json';v=r.read(p)
for x in v['findings']:
 if x['id'] in ['R605-003','R605-009']:x.setdefault('subsequentBatchRepairs',[]).append(dict(batch=42,ids=sorted(ids),evidence='batch42/batch-verification.json'))
for x in r.read(b/'related295-assessment-before.json'):v['relatedPrior295Reviews'].append(dict(id=x['id'],batch=42,causeFamilies=['denominator-and-population','intersection-bounds','raster-prose'],evidence='batch42/related295-repair-model-checks.json',status='source_key_semantics_and_host_reverified',historicalScorePreserved=x['historicalScorePreserved'],currentAssessmentBeforeRepair=x['currentBeforeScore']))
r.write(p,v)
r.write(b/'visual-review.json',dict(status='PASS',before='All10 before-starts1..3 inspected before repair. Related before-starts image inspected after its repair using saved pre-edit render. Original10 and related2 source images inspected.',after='All10 after-starts1..3 and after-prose1..2 inspected, including all changed bodies and related21/39.',hostNotDevice=True))
r.write(b/'batch-verification.json',dict(status='verified',verifiedAt=r.now(),count=10,ownSolves='own-solves.json',solveFrozenReceipt='solve-frozen-before-reveal.json',ratings='ratings-before.json',frozenRatingsReceipt='ratings-frozen.json',beforeScoreTotal=43,beforeMean=4.3,targetQuestionsChanged=7,relatedPrior295Rechecked=2,relatedPrior295Changed=1,sourceKeyModels=['source-native-pixel-checks.json','exact-model-checks.json'],repairChecks='repair-semantic-checks.json',relatedChecks='related295-repair-model-checks.json',hostLogs=logs,hostSuccessfulTestCount=24,visualReview='visual-review.json',preservation='preservation-check.json',solvesFrozenBeforeReveal=10,previouslyExposedOfficialAnswers=0,firstPassAnswerMatches=10,firstPassReasoningCorrections=1,reasoningCorrection='post-reveal-reasoning-correction.json',limitations='Same-author review, not independent. Own d13 omitted-institution bound incomplete; corrected separately; existing app already correct. Original assets retained; no intermediateAPK.'))
print('Batch42 verified10;420 total after refresh')
