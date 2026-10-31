import review_remaining605 as r
b=r.folder(33);logs=['host-before.log','host-after.log','related295-host-before.log','related295-host-after.log']
for name in logs:assert 'All tests passed!' in (b/name).read_text(encoding='utf-8-sig')
assert r.sha(b/'ratings-before.json')==r.read(b/'ratings-frozen.json')['ratingsSha256']
assert r.sha(b/'own-solves.json')==r.read(b/'solve-frozen-before-reveal.json')['solveFileSha256']
assert r.sha(b/'related295-own-solves.json')==r.read(b/'related295-solve-frozen.json')['sha256']
for name in ['source-native-pixel-checks.json','exact-model-checks.json','repair-semantic-checks.json','related295-source-native-pixel-checks.json','related295-repair-model-checks.json','preservation-check.json']:assert r.read(b/name)['status']=='PASS'
changes=r.read(r.OUT/'changes-batch33.json');ids={x['id'] for x in changes}
for x in changes:x['status']='verified'
r.write(r.OUT/'changes-batch33.json',changes)
for name in ['cross-candidates-data-raster-prose.json','cross-candidates-choice-percent-boundaries24.json','cross-candidates-verdict-only-reasons28.json']:
 p=r.OUT/name;v=r.read(p)
 for x in v['candidates']:
  if x['id'] in ids:x.update(status='source_semantics_and_host_reverified',evidence='batch33/batch-verification.json')
  if name=='cross-candidates-verdict-only-reasons28.json' and x.get('status')=='repaired_and_host_verified_batch28':
   assert r.read(r.folder(28)/'batch-verification.json')['status']=='verified'
   x.update(status='source_semantics_and_host_reverified',evidence='batch28/batch-verification.json')
 if name=='cross-candidates-verdict-only-reasons28.json':
  assert all(x.get('status')=='source_semantics_and_host_reverified' for x in v['candidates']);v['status']='original_exact_candidates_closed';v['closedAt']=r.now();v['limitation']='Closes initial exact9 candidate scope only; later verdict-like cases reviewed in their own batches.'
 r.write(p,v)
p=r.OUT/'cross-validation.json';v=r.read(p)
for x in v['findings']:
 if x['id'] in ['R605-003','R605-009','R605-013','R605-016']:
  subset=sorted(ids) if x['id']=='R605-009' else [i for i in sorted(ids) if (x['id']=='R605-003' and i.endswith('2026-07-18-psat-d-23')) or (x['id']=='R605-013' and i.endswith(('2026-03-07-psat-d-14','2026-03-07-psat-d-16'))) or (x['id']=='R605-016' and i.endswith(('2026-03-07-psat-d-02','2026-03-07-psat-d-07','2026-03-07-psat-d-08','2026-03-07-psat-d-18','2026-07-18-psat-d-17','2026-07-18-psat-d-23')))]
  if x['id']=='R605-009':subset=[i for i in subset if not i.endswith(('2026-03-07-psat-d-14','2026-03-07-psat-d-16'))]
  x.setdefault('subsequentBatchRepairs',[]).append(dict(batch=33,ids=subset,evidence='batch33/batch-verification.json'))
  if x['id']=='R605-016':x['originalExactCandidateScope']='All9 initial exact candidates source/semantics/host reverified by batch33; no claim of all900 generic wording clearance.'
for n in [17,23]:v['relatedPrior295Reviews'].append(dict(id=f'kr-mpm-2026-07-18-psat-d-{n}',batch=33,causeFamilies=['R605-009','R605-016']+(['R605-003'] if n==23 else []),evidence='batch33/related295-repair-model-checks.json',status='source_key_semantics_and_host_reverified',historicalScorePreserved=5,currentAssessmentBeforeRepair=4))
r.write(p,v)
r.write(b/'visual-review.json',dict(status='PASS',before='All10 target initial screens in before-starts1..3 and both related prior295 starts inspected.',after='All10 target initial screens in after-starts1..3 and changed prose/reason pages in after-details1..4 inspected. Report→five figures order, table/graph→report order, all native 보기/정보 blocks confirmed. Related295 starts, revised interval proof, and all individual reasons inspected in related295-after-details1..3.',hostNotDevice=True))
r.write(b/'batch-verification.json',dict(status='verified',verifiedAt=r.now(),count=10,ownSolves='own-solves.json',solveFrozenReceipt='solve-frozen-before-reveal.json',ratings='ratings-before.json',frozenRatingsReceipt='ratings-frozen.json',beforeScoreTotal=40,beforeMean=4.0,targetQuestionsChanged=10,relatedPrior295RecheckedAndChanged=2,sourceKeysAnd27Crops='source-native-pixel-checks.json',exactModels='exact-model-checks.json',repairChecks='repair-semantic-checks.json',relatedSourceKeysAnd4Crops='related295-source-native-pixel-checks.json',relatedChecks='related295-repair-model-checks.json',hostLogs=logs,hostSuccessfulTestCount=24,visualReview='visual-review.json',preservation='preservation-check.json',solvesFrozenBeforeReveal=10,previouslyExposedOfficialAnswers=0,firstPassAnswerMatches=10,firstPassReasoningCorrections=0,limitations='Same-author review. Initial exact9 verdict-only candidate scope closed; broader cross queues remain. No intermediate build.'))
print('Batch33 verified10; cumulative330 after refresh.')
