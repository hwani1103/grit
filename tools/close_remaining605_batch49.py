import review_remaining605 as r
b=r.folder(49);assert not (b/'batch-verification.json').exists()
logs=['host-before.log','related295-host-before.log','host-after.log']
for n in logs:assert 'All tests passed!' in (b/n).read_text(encoding='utf-8-sig')
for file,receipt,key in [('own-solves.json','solve-frozen-before-reveal.json','solveFileSha256'),('ratings-before.json','ratings-frozen.json','ratingsSha256'),('related295-own-solves.json','related295-solve-frozen.json','sha256')]:assert r.sha(b/file)==r.read(b/receipt)[key]
for n in ['source-key-model-checks.json','related295-source-key-model-checks.json','related295-underline-source-strokes.json','repair-semantic-checks.json','preservation-check.json']:assert r.read(b/n)['status']=='PASS'
changes=r.read(r.OUT/'changes-batch49.json')
for x in changes:x['status']='verified'
r.write(r.OUT/'changes-batch49.json',changes)
ids={x['id'] for x in r.read(b/'own-solves.json')+r.read(b/'related295-own-solves.json')}
p=r.OUT/'cross-candidates-underline-period46.json';v=r.read(p)
rows=v if isinstance(v,list) else v.get('candidates',[])
for x in rows:
 if x.get('id')=='kr-mpm-2024-03-02-psat-l-08':x.update(status='source_terminal_strokes_repaired',evidence='batch49/related295-underline-source-strokes.json')
r.write(p,v)
p=r.OUT/'cross-validation.json';v=r.read(p)
for x in v['findings']:
 if x['id'] in ['R605-006','R605-010','R605-013','R605-017']:x.setdefault('subsequentBatchRepairs',[]).append(dict(batch=49,ids=sorted(ids),evidence='batch49/batch-verification.json'))
for x in r.read(b/'related295-assessment-before.json'):v['relatedPrior295Reviews'].append(dict(id=x['id'],batch=49,causeFamilies=['underline-terminal-range','experimental-boundary','context-substitution'],evidence='batch49/related295-source-key-model-checks.json',status='source_key_semantics_and_host_reverified',historicalScorePreserved=x['historicalScorePreserved'],currentAssessmentBeforeRepair=x['currentBeforeScore']))
r.write(p,v)
r.write(b/'visual-review.json',dict(status='PASS',before='All10 originals and before-starts inspected; both prior295 originals and related-before-starts inspected.',after='All12 after-starts1..3 and4 detail images inspected: l08 underline endings, l21 and l23 compound words, l27 corrected reason.',hostNotDevice=True))
r.write(b/'batch-verification.json',dict(status='verified',verifiedAt=r.now(),count=10,ownSolves='own-solves.json',solveFrozenReceipt='solve-frozen-before-reveal.json',ratings='ratings-before.json',frozenRatingsReceipt='ratings-frozen.json',beforeScoreTotal=46,beforeMean=4.6,targetQuestionsChanged=4,relatedPrior295Rechecked=2,relatedPrior295Changed=1,sourceKeyModels=['source-key-model-checks.json','related295-source-key-model-checks.json'],repairChecks='repair-semantic-checks.json',hostLogs=logs,hostSuccessfulTestCount=18,afterHostScope='All12 target+related questions in one6-check audit',visualReview='visual-review.json',preservation='preservation-check.json',solvesFrozenBeforeReveal=10,previouslyExposedOfficialAnswers=10,firstPassAnswerMatches=10,firstPassReasoningCorrections=0,limitations='Same-author review, not independent. All10 had historical official-key exposure; fresh solutions frozen before current reveal. New tail49 candidate remains pending. No intermediate APK.'))
print('Batch49 verified10;490 total after refresh')
