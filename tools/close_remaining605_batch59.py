import review_remaining605 as r
b=r.folder(59);assert not (b/'batch-verification.json').exists()
logs=['host-before.log','related295-host-before.log','host-after.log']
for n in logs:assert 'All tests passed!' in (b/n).read_text(encoding='utf-8-sig')
for file,receipt,key in [('own-solves.json','solve-frozen-before-reveal.json','solveFileSha256'),('ratings-before.json','ratings-frozen.json','ratingsSha256'),('related295-own-solves.json','related295-solve-frozen.json','sha256')]:assert r.sha(b/file)==r.read(b/receipt)[key]
for n in ['source-key-checks.json','related295-source-key-checks.json','pre-reveal-exact-models.json','related295-pre-reveal-models.json','repair-semantic-checks.json','preservation-check.json']:assert r.read(b/n)['status']=='PASS'
changes=r.read(r.OUT/'changes-batch59.json')
for x in changes:x['status']='verified'
r.write(r.OUT/'changes-batch59.json',changes)
ids={x['id'] for x in r.read(b/'own-solves.json')+r.read(b/'related295-own-solves.json')}
for p in r.OUT.glob('cross-candidates-*.json'):
 v=r.read(p);rows=v if isinstance(v,list) else v.get('candidates',[]);changed=False
 for x in rows:
  if isinstance(x,dict) and x.get('id') in ids:x.update(status='source_semantics_and_host_reverified',evidence='batch59/batch-verification.json');changed=True
 if changed:r.write(p,v)
p=r.OUT/'cross-validation.json';v=r.read(p)
for x in v['findings']:
 if x['id'] in ['R605-003','R605-008','R605-009','R605-011','R605-018']:x.setdefault('subsequentBatchRepairs',[]).append(dict(batch=59,ids=sorted(ids),evidence='batch59/batch-verification.json'))
for x in r.read(b/'related295-assessment-before.json'):v['relatedPrior295Reviews'].append(dict(id=x['id'],batch=59,causeFamilies=['integer-extrema','positive-cost-cap','two-quorums','strict-gender-boundary','source-structure'],evidence='batch59/related295-source-key-checks.json',status='source_key_semantics_and_host_reverified',historicalScorePreserved=x['historicalScorePreserved'],currentAssessmentBeforeRepair=x['currentBeforeScore']))
r.write(p,v)
r.write(b/'visual-review.json',dict(status='PASS',before='All10 target and3 related originals plus all13 before-starts inspected.5 target original figure crops freshly matched. Related13 native table and afterParagraph placement verified.',after='All13 after-starts and route18 table/footnote/native tail screenshot inspected. Source prefix/table/tail order regression passed.',hostNotDevice=True))
r.write(b/'batch-verification.json',dict(status='verified',verifiedAt=r.now(),count=10,ownSolves='own-solves.json',solveFrozenReceipt='solve-frozen-before-reveal.json',ratings='ratings-before.json',frozenRatingsReceipt='ratings-frozen.json',beforeScoreTotal=44,beforeMean=4.4,targetQuestionsChanged=5,relatedPrior295Rechecked=3,relatedPrior295Changed=0,sourceKeyModels=['source-key-checks.json','related295-source-key-checks.json','pre-reveal-exact-models.json','related295-pre-reveal-models.json'],repairChecks='repair-semantic-checks.json',hostLogs=logs,hostSuccessfulTestCount=19,afterHostScope='All13 target+related6 checks plus1 source-prefix order regression',visualReview='visual-review.json',preservation='preservation-check.json',solvesFrozenBeforeReveal=10,previouslyExposedOfficialAnswers=0,firstPassAnswerMatches=10,firstPassReasoningCorrections=0,limitations='Same-author review, not independent. All13 source-only answers match. Route18 long raster conditions moved to native prose with original table/footnote and old asset preserved. Four other targets legal-reference/word-break improvements. No intermediate APK.'))
print('Batch59 verified;590 total after refresh')
