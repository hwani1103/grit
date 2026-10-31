import review_remaining605 as r
b=r.folder(29)
logs=['host-before.log','related295-host-before.log','host-after-final.log','host-reasons-final.log']
for name in logs:assert 'All tests passed!' in (b/name).read_text(encoding='utf-8-sig')
assert r.sha(b/'ratings-before.json')==r.read(b/'ratings-frozen.json')['ratingsSha256']
assert r.sha(b/'own-solves.json')==r.read(b/'solve-frozen-before-reveal.json')['solveFileSha256']
changes=r.read(r.OUT/'changes-batch29.json')
for x in changes:x['status']='verified'
r.write(r.OUT/'changes-batch29.json',changes)
ids={x['id'] for x in changes}
for name in ['cross-candidates-unit-exponent29.json','cross-candidates-verdict-only-reasons28.json','cross-candidates-word-unit-and-conditional-direction.json']:
 p=r.OUT/name;v=r.read(p)
 for x in v['candidates']:
  if x['id'] in ids:x.update(status='source_semantics_and_host_reverified',evidence='batch29/batch-verification.json')
  if x['id']=='kr-mpm-2026-07-18-psat-s-07':x.update(status='source_semantics_and_host_reverified',evidence='batch26/batch-verification.json')
 r.write(p,v)
p=r.OUT/'cross-validation.json';v=r.read(p)
for x in v['findings']:
 if x['id'] in ['R605-013','R605-016']:
  x.setdefault('subsequentBatchRepairs',[]).append(dict(batch=29,ids=sorted(ids),evidence='batch29/batch-verification.json',scope='Unit exponents, original word/percent boundaries, and substantive individual option reasons.'))
 if x['id']=='R605-013':x.setdefault('additionalScopes',[]).append('cross-candidates-unit-exponent29.json')
v['relatedPrior295Reviews'].append(dict(id='kr-mpm-2026-07-18-psat-s-19',batch=29,causeFamilies=['R605-013','R605-016'],evidence='batch29/repair-and-related-checks.json',status='source_key_semantics_and_host_reverified',historicalScorePreserved=5,currentAssessmentBeforeRepair=4))
r.write(p,v)
r.write(b/'visual-review.json',dict(status='PASS',before='All10 target start screens and related19 reviewed before edits.',after='All11 start screens and changed detail pages inspected in after-starts1..3/after-details1..2; final reason text after spacing refinement inspected in final-reasons-1.png and final-reasons-2.png.',hostNotDevice=True,reasonRefinement='reason-refinement.json'))
r.write(b/'batch-verification.json',dict(status='verified',verifiedAt=r.now(),count=10,ownSolves='own-solves.json',solveFrozenReceipt='solve-frozen-before-reveal.json',ratings='ratings-before.json',frozenRatingsReceipt='ratings-frozen.json',beforeScoreTotal=47,beforeMean=4.7,targetQuestionsChanged=3,relatedPrior295RecheckedAndChanged=1,sourceKeyModels='source-key-model-checks.json',repairChecks='repair-and-related-checks.json',hostLogs=logs,hostSuccessfulTestCount=24,interruptedLogNotPass='host-after.log',visualReview='visual-review.json',preservation='preservation-check.json',solvesFrozenBeforeReveal=10,previouslyExposedOfficialAnswers=0,firstPassAnswerMatches=10,firstPassReasoningCorrections=0,limitations='Same-author review. Broader cross queues pending; final release only after full completion.'))
