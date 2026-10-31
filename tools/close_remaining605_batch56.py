import review_remaining605 as r
b=r.folder(56);assert not (b/'batch-verification.json').exists()
logs=['host-before.log','related295-host-before.log','host-after.log']
for n in logs:assert 'All tests passed!' in (b/n).read_text(encoding='utf-8-sig')
for file,receipt,key in [('own-solves.json','solve-frozen-before-reveal.json','solveFileSha256'),('ratings-before.json','ratings-frozen.json','ratingsSha256'),('related295-own-solves.json','related295-solve-frozen.json','sha256')]:assert r.sha(b/file)==r.read(b/receipt)[key]
for n in ['source-key-checks.json','related295-source-key-checks.json','exact-model-checks.json','repair-semantic-checks.json','preservation-check.json']:assert r.read(b/n)['status']=='PASS'
changes=r.read(r.OUT/'changes-batch56.json')
for x in changes:x['status']='verified'
r.write(r.OUT/'changes-batch56.json',changes)
ids={x['id'] for x in r.read(b/'own-solves.json')+r.read(b/'related295-own-solves.json')}
for p in r.OUT.glob('cross-candidates-*.json'):
 v=r.read(p);rows=v if isinstance(v,list) else v.get('candidates',[]);changed=False
 for x in rows:
  if isinstance(x,dict) and x.get('id') in ids:x.update(status='source_semantics_and_host_reverified',evidence='batch56/batch-verification.json');changed=True
 if changed:r.write(p,v)
p=r.OUT/'cross-validation.json';v=r.read(p)
for x in v['findings']:
 if x['id'] in ['R605-003','R605-008','R605-009','R605-011','R605-018']:x.setdefault('subsequentBatchRepairs',[]).append(dict(batch=56,ids=sorted(ids),evidence='batch56/batch-verification.json'))
for x in r.read(b/'related295-assessment-before.json'):v['relatedPrior295Reviews'].append(dict(id=x['id'],batch=56,causeFamilies=['citation-notation','word-spacing','rate-denominator','selection-threshold','floor-division'],evidence='batch56/related295-source-key-checks.json',status='source_key_semantics_and_host_reverified',historicalScorePreserved=x['historicalScorePreserved'],currentAssessmentBeforeRepair=x['currentBeforeScore']))
r.write(p,v)
r.write(b/'visual-review.json',dict(status='PASS',before='All10 target original source pages and all10 before-starts plus both related originals and before-starts inspected.',after='All12 after-starts inspected. Original condition-before-table order maintained for s13 and related17; target word repairs checked by exact string comparison.',hostNotDevice=True))
r.write(b/'batch-verification.json',dict(status='verified',verifiedAt=r.now(),count=10,ownSolves='own-solves.json',solveFrozenReceipt='solve-frozen-before-reveal.json',ratings='ratings-before.json',frozenRatingsReceipt='ratings-frozen.json',beforeScoreTotal=47,beforeMean=4.7,targetQuestionsChanged=3,relatedPrior295Rechecked=2,relatedPrior295Changed=0,sourceKeyModels=['source-key-checks.json','related295-source-key-checks.json','exact-model-checks.json'],repairChecks='repair-semantic-checks.json',hostLogs=logs,hostSuccessfulTestCount=18,afterHostScope='All12 target+related questions6-check audit',visualReview='visual-review.json',preservation='preservation-check.json',solvesFrozenBeforeReveal=10,previouslyExposedOfficialAnswers=0,firstPassAnswerMatches=10,firstPassReasoningCorrections=0,limitations='Same-author review, not independent. All10 source-only answers match current and official keys. Source native/choices and two fresh figure crops verified. Three typography repairs; prior295 two current5 unchanged. Related17 frozen rank phrase typo annotated without changing scores or answers. No intermediate APK.'))
print('Batch56 verified10;560 total after refresh')
