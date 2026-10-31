import review_remaining605 as r
b=r.folder(36);logs=['host-before.log','host-after.log','related295-host-before.log','related295-host-after.log']
for name in logs:assert 'All tests passed!' in (b/name).read_text(encoding='utf-8-sig')
for file,receipt,key in [('own-solves.json','solve-frozen-before-reveal.json','solveFileSha256'),('ratings-before.json','ratings-frozen.json','ratingsSha256'),('related295-own-solves.json','related295-solve-frozen.json','sha256')]:assert r.sha(b/file)==r.read(b/receipt)[key]
for name in ['source-native-pixel-checks.json','exact-model-checks.json','repair-semantic-checks.json','related295-source-native-pixel-checks.json','related295-repair-model-checks.json','preservation-check.json']:assert r.read(b/name)['status']=='PASS'
changes=r.read(r.OUT/'changes-batch36.json');ids={x['id'] for x in changes}
for x in changes:x['status']='verified'
r.write(r.OUT/'changes-batch36.json',changes)
for name in ['cross-candidates-data-raster-prose.json','cross-candidates-structure-and-extrema.json','cross-candidates-choice-percent-boundaries.json']:
 p=r.OUT/name
 if not p.exists():continue
 v=r.read(p);rows=v if isinstance(v,list) else v.get('candidates',[])
 for x in rows:
  if x['id'] in ids:x.update(status='source_semantics_and_host_reverified',evidence='batch36/batch-verification.json')
 r.write(p,v)
p=r.OUT/'cross-validation.json';v=r.read(p)
for x in v['findings']:
 if x['id'] in ['R605-003','R605-006','R605-013','R605-016']:
  x.setdefault('subsequentBatchRepairs',[]).append(dict(batch=36,ids=sorted(ids),evidence='batch36/batch-verification.json'))
hist={q['id']:q for q in r.read(r.PREP/'previously-scored295.json')['questions']}
for q in r.read(b/'related295-before.json'):v['relatedPrior295Reviews'].append(dict(id=q['id'],batch=36,causeFamilies=['extremum-scope-premise','native-prose','all-option-grounds'],evidence='batch36/related295-repair-model-checks.json',status='source_key_semantics_and_host_reverified',historicalScorePreserved=hist[q['id']]['scoreBeforeFix'],currentAssessmentBeforeRepair=4))
r.write(p,v)
r.write(b/'visual-review.json',dict(status='PASS',before='All10 before-starts1..3 and related295-before-starts inspected.',after='All10 after-starts1..3, seven native prose blocks in after-prose1..4, related295-after-details1..3 including full dialogue with original illustration and three underlined sentences, and d27 rounding-interval explanation inspected.',hostNotDevice=True))
r.write(b/'batch-verification.json',dict(status='verified',verifiedAt=r.now(),count=10,ownSolves='own-solves.json',solveFrozenReceipt='solve-frozen-before-reveal.json',ratings='ratings-before.json',frozenRatingsReceipt='ratings-frozen.json',beforeScoreTotal=41,beforeMean=4.1,targetQuestionsChanged=9,relatedPrior295RecheckedAndChanged=3,sourceKeyPixels='source-native-pixel-checks.json',exactModels='exact-model-checks.json',repairChecks='repair-semantic-checks.json',relatedChecks='related295-repair-model-checks.json',hostLogs=logs,hostSuccessfulTestCount=24,visualReview='visual-review.json',preservation='preservation-check.json',solvesFrozenBeforeReveal=10,previouslyExposedOfficialAnswers=0,firstPassAnswerMatches=10,firstPassReasoningCorrections=0,limitations='Same-author review; explicit rounds/model witnesses are not actual unknown values. Broader cross-cause queues and remaining605 continue; no intermediate APK.'))
print('Batch36 verified10;360 total after refresh')
