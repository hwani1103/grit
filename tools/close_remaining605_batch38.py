import review_remaining605 as r
b=r.folder(38);logs=['host-before.log','host-after.log','related295-host-before.log','related295-host-after.log']
for name in logs:assert 'All tests passed!' in (b/name).read_text(encoding='utf-8-sig')
for file,receipt,key in [('own-solves.json','solve-frozen-before-reveal.json','solveFileSha256'),('ratings-before.json','ratings-frozen.json','ratingsSha256'),('related295-own-solves.json','related295-solve-frozen.json','sha256')]:assert r.sha(b/file)==r.read(b/receipt)[key]
for name in ['source-key-model-checks.json','repair-semantic-checks.json','related295-source-key-model-checks.json','preservation-check.json']:assert r.read(b/name)['status']=='PASS'
changes=r.read(r.OUT/'changes-batch38.json');ids={x['id'] for x in changes}
for x in changes:x['status']='verified'
r.write(r.OUT/'changes-batch38.json',changes)
p=r.OUT/'cross-candidates-max-premise.json';v=r.read(p)
proofs={'2023-07-22-s-13':(2,'Only甲/乙 can attain10 for naturalx;乙max within that pair, not all people. Counterexample x6 gives乙3<丁5 explicitly retained.'),'kr-mpm-2021-07-10-psat-s-12':(17,'All six material permutations checked; fixed support costs mean area alone does not order total cost.'),'kr-mpm-2026-03-07-psat-s-19':(38,'p>=20,d<=2.5,d>0 prove p/d>=8; numerator min denominator max.'),'kr-mpm-2021-07-10-psat-l-03':(38,'High consensus efficiency A does not entail highest goal effectiveness; B can outperform A.')}
for x in v:
 n,proof=proofs[x['id']];x.update(status='source_semantics_and_host_reverified',evidence=f'batch{n:02d}/batch-verification.json',reconciledAt=r.now(),semanticGround=proof)
r.write(p,v)
for name in ['cross-candidates-structure-and-extrema.json','cross-candidates-choice-percent-boundaries24.json','cross-candidates-word-unit33.json']:
 p=r.OUT/name
 if not p.exists():continue
 v=r.read(p);rows=v if isinstance(v,list) else v.get('candidates',[])
 for x in rows:
  if x['id'] in ids:x.update(status='source_semantics_and_host_reverified',evidence='batch38/batch-verification.json')
 r.write(p,v)
p=r.OUT/'cross-validation.json';v=r.read(p)
for x in v['findings']:
 if x['id'] in ['R605-003','R605-006','R605-013','R605-016']:
  x.setdefault('subsequentBatchRepairs',[]).append(dict(batch=38,ids=sorted(ids),evidence='batch38/batch-verification.json'))
hist={q['id']:q for q in r.read(r.PREP/'previously-scored295.json')['questions']}
for q in r.read(b/'related295-before.json'):v['relatedPrior295Reviews'].append(dict(id=q['id'],batch=38,causeFamilies=['extremum-scope-premise','shared-source-word-boundaries','ratio-denominator'],evidence='batch38/related295-source-key-model-checks.json',status='source_key_semantics_and_host_reverified',historicalScorePreserved=hist[q['id']]['scoreBeforeFix'],currentAssessmentBeforeRepair=4 if q['number']==39 else 5))
r.write(p,v)
r.write(b/'visual-review.json',dict(status='PASS',before='All10 before-starts1..3 and related295-before-starts1 inspected.',after='All10 after-starts1..3; selected details show last law heading, mandatory vs optional spaces, lottery percent and pore-ratio reasons; related295-after-starts1 and selected table/particle/lottery details inspected.',hostNotDevice=True))
r.write(b/'batch-verification.json',dict(status='verified',verifiedAt=r.now(),count=10,ownSolves='own-solves.json',solveFrozenReceipt='solve-frozen-before-reveal.json',ratings='ratings-before.json',frozenRatingsReceipt='ratings-frozen.json',beforeScoreTotal=43,beforeMean=4.3,targetQuestionsChanged=7,relatedPrior295Rechecked=3,relatedPrior295Changed=1,sourceKeyModels='source-key-model-checks.json',repairChecks='repair-semantic-checks.json',relatedChecks='related295-source-key-model-checks.json',hostLogs=logs,hostSuccessfulTestCount=24,visualReview='visual-review.json',preservation='preservation-check.json',solvesFrozenBeforeReveal=10,previouslyExposedOfficialAnswers=0,firstPassAnswerMatches=10,firstPassReasoningCorrections=1,correction='post-reveal-reasoning-correction.json',limitations='Same-author review; own legal-subject memo error corrected separately, original memo retained. Max-premise exact5 candidates closed by explicit semantic evidence; broader cause checks continue. No intermediate APK.'))
print('Batch38 verified10;380 total after refresh')
