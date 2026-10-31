import review_remaining605 as r
b=r.folder(32);logs=['host-before.log','host-after.log','related295-host-before.log','related295-host-after.log']
for name in logs:assert 'All tests passed!' in (b/name).read_text(encoding='utf-8-sig')
assert r.sha(b/'ratings-before.json')==r.read(b/'ratings-frozen.json')['ratingsSha256']
assert r.sha(b/'own-solves.json')==r.read(b/'solve-frozen-before-reveal.json')['solveFileSha256']
assert r.sha(b/'related295-own-solves.json')==r.read(b/'related295-solve-frozen.json')['sha256']
for name in ['source-key-model-checks.json','repair-checks.json','related295-source-key-checks.json','preservation-check.json']:assert r.read(b/name)['status']=='PASS'
changes=r.read(r.OUT/'changes-batch32.json')
for x in changes:x['status']='verified'
r.write(r.OUT/'changes-batch32.json',changes);ids={x['id'] for x in changes}
for name in ['cross-candidates-law-quotes32.json','cross-candidates-word-unit-and-conditional-direction.json']:
 p=r.OUT/name;v=r.read(p)
 for x in v['candidates']:
  if x['id'] in ids:x.update(status='source_semantics_and_host_reverified',evidence='batch32/batch-verification.json')
 r.write(p,v)
p=r.OUT/'cross-validation.json';v=r.read(p)
for x in v['findings']:
 if x['id'] in ['R605-003','R605-013','R605-016']:
  subset=[i for i in sorted(ids) if (x['id']=='R605-003' and i.endswith('s-34')) or (x['id']=='R605-016' and i.endswith(('s-28','s-37'))) or x['id']=='R605-013']
  x.setdefault('subsequentBatchRepairs',[]).append(dict(batch=32,ids=subset,evidence='batch32/batch-verification.json'))
 if x['id']=='R605-013':x.setdefault('additionalScopes',[]).append('cross-candidates-law-quotes32.json')
v['relatedPrior295Reviews'].append(dict(id='kr-mpm-2023-07-22-psat-l-24',batch=32,causeFamilies=['R605-013'],evidence='batch32/related295-source-key-checks.json',status='source_key_semantics_and_host_reverified',historicalScorePreserved=5,currentAssessmentBeforeRepair=4))
r.write(p,v)
r.write(b/'visual-review.json',dict(status='PASS',before='10 target initial screens in before-starts1..3 and prior295 l24 initial screen inspected.',after='10 target initial screens in after-starts1..3; law quote/word/percent bodies, s28 reasons, s33 corrected space, s34 five-citizen boundary and s37 all reasons inspected in after-details1..3. Prior295 l24 after start and page02 inspected for restored law quotes and particles.',hostNotDevice=True))
r.write(b/'batch-verification.json',dict(status='verified',verifiedAt=r.now(),count=10,ownSolves='own-solves.json',solveFrozenReceipt='solve-frozen-before-reveal.json',ratings='ratings-before.json',frozenRatingsReceipt='ratings-frozen.json',beforeScoreTotal=44,beforeMean=4.4,targetQuestionsChanged=6,relatedPrior295RecheckedAndChanged=1,sourceKeyModels='source-key-model-checks.json',repairChecks='repair-checks.json',relatedChecks='related295-source-key-checks.json',hostLogs=logs,hostSuccessfulTestCount=24,visualReview='visual-review.json',preservation='preservation-check.json',solvesFrozenBeforeReveal=10,previouslyExposedOfficialAnswers=0,firstPassAnswerMatches=10,firstPassReasoningCorrections=0,limitations='Same-author review. Exact law-space candidate scope closed; other broader cross queues pending. Final release only after full completion.'))
print('Batch32 verified10; cumulative320 after refresh.')
