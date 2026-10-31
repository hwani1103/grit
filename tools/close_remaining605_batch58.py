import review_remaining605 as r
b=r.folder(58);assert not (b/'batch-verification.json').exists()
logs=['host-before.log','related295-host-before.log','host-after-corrected.log']
for n in logs:assert 'All tests passed!' in (b/n).read_text(encoding='utf-8-sig')
for file,receipt,key in [('own-solves.json','solve-frozen-before-reveal.json','solveFileSha256'),('ratings-before.json','ratings-frozen.json','ratingsSha256'),('related295-own-solves.json','related295-solve-frozen.json','sha256')]:assert r.sha(b/file)==r.read(b/receipt)[key]
for n in ['source-key-checks.json','related295-source-key-checks.json','pre-reveal-exact-models.json','underline-source-strokes.json','repair-semantic-checks.json','preservation-check.json']:assert r.read(b/n)['status']=='PASS'
changes=r.read(r.OUT/'changes-batch58.json')
for x in changes:x['status']='verified'
r.write(r.OUT/'changes-batch58.json',changes)
ids={x['id'] for x in r.read(b/'own-solves.json')+r.read(b/'related295-own-solves.json')}
for p in r.OUT.glob('cross-candidates-*.json'):
 v=r.read(p);rows=v if isinstance(v,list) else v.get('candidates',[]);changed=False
 for x in rows:
  if isinstance(x,dict) and x.get('id') in ids:x.update(status='source_semantics_and_host_reverified',evidence='batch58/batch-verification.json');changed=True
 if changed:r.write(p,v)
p=r.OUT/'cross-validation.json';v=r.read(p)
for x in v['findings']:
 if x['id'] in ['R605-003','R605-008','R605-009','R605-011','R605-018']:x.setdefault('subsequentBatchRepairs',[]).append(dict(batch=58,ids=sorted(ids),evidence='batch58/batch-verification.json'))
for x in r.read(b/'related295-assessment-before.json'):
 if x['reviewKind']!='prior295':
  v.setdefault('associated605Reviews',[]).append(dict(id=x['id'],batch=58,status='source_key_semantics_and_host_reverified',evidence='batch58/batch-verification.json'));continue
 v['relatedPrior295Reviews'].append(dict(id=x['id'],batch=58,causeFamilies=['underline-label','underline-punctuation','causal-scope','argument-direction','legal-authority'],evidence='batch58/related295-source-key-checks.json',status='source_key_semantics_and_host_reverified',historicalScorePreserved=x['historicalScorePreserved'],currentAssessmentBeforeRepair=x['currentBeforeScore']))
r.write(p,v)
r.write(b/'visual-review.json',dict(status='PASS',before='All10 target original source pages and all10 before-starts plus all4 related originals and before-starts inspected.',after='All14 after-starts plus all11 original underline ranges, repeated fourth occurrence anchor and l28 modal-scope explanation inspected; full revised explanation and original punctuation boundaries inspected.',hostNotDevice=True))
r.write(b/'batch-verification.json',dict(status='verified',verifiedAt=r.now(),count=10,ownSolves='own-solves.json',solveFrozenReceipt='solve-frozen-before-reveal.json',ratings='ratings-before.json',frozenRatingsReceipt='ratings-frozen.json',beforeScoreTotal=47,beforeMean=4.7,targetQuestionsChanged=3,relatedPrior295Rechecked=1,relatedPrior295Changed=0,associated605Rechecked=3,associated605Changed=3,sourceKeyModels=['source-key-checks.json','related295-source-key-checks.json','pre-reveal-exact-models.json'],repairChecks='repair-semantic-checks.json',hostLogs=logs,hostSuccessfulTestCount=20,afterHostScope='All14 target+related questions6-check audit plus underline boundary2 regressions',visualReview='visual-review.json',preservation='preservation-check.json',solvesFrozenBeforeReveal=10,previouslyExposedOfficialAnswers=10,firstPassAnswerMatches=10,firstPassReasoningCorrections=0,limitations='Same-author review, not independent. Native source and all choices verified. Source-only current-pass own answers all match; historical key exposure10 acknowledged. Three target and three associated605 repairs. Repeated fourth phrase retains stored anchor excluded by existing renderer. First failed audit retained as host-after.log; corrected audit passed. Rating prose erratum preserves original ratings and score. All bodies and answers unchanged. No intermediate APK.'))
print('Batch58 verified10;580 total after refresh')
