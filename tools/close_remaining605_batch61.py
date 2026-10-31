import review_remaining605 as r
b=r.folder(61);assert not (b/'batch-verification.json').exists()
logs=['host-before.log','host-after.log']
for n in logs:assert 'All tests passed!' in (b/n).read_text(encoding='utf-8-sig')
for file,receipt,key in [('own-solves.json','solve-frozen-before-reveal.json','solveFileSha256'),('ratings-before.json','ratings-frozen.json','ratingsSha256')]:assert r.sha(b/file)==r.read(b/receipt)[key]
for n in ['source-key-checks.json','pre-reveal-exact-models.json','repair-semantic-checks.json','preservation-check.json']:assert r.read(b/n)['status']=='PASS'
changes=r.read(r.OUT/'changes-batch61.json')
for x in changes:x['status']='verified'
r.write(r.OUT/'changes-batch61.json',changes);ids={x['id'] for x in r.read(b/'own-solves.json')}
for p in r.OUT.glob('cross-candidates-*.json'):
 v=r.read(p);rows=v if isinstance(v,list) else v.get('candidates',[]);changed=False
 for x in rows:
  if isinstance(x,dict) and x.get('id') in ids:x.update(status='source_semantics_and_host_reverified',evidence='batch61/batch-verification.json');changed=True
 if changed:r.write(p,v)
p=r.OUT/'cross-validation.json';v=r.read(p)
for x in v['findings']:
 if x['id'] in ['R605-008','R605-009','R605-011','R605-018']:x.setdefault('subsequentBatchRepairs',[]).append(dict(batch=61,ids=sorted(ids),evidence='batch61/batch-verification.json'))
r.write(p,v)
r.write(b/'visual-review.json',dict(status='PASS',before='All5 original regions and5 before-starts inspected;9 original figure crops freshly matched.',after='All5 after-starts and source30 native prefix/original formula/native tail inspected; source prefix order regression passed.',hostNotDevice=True))
r.write(b/'batch-verification.json',dict(status='verified',verifiedAt=r.now(),count=5,ownSolves='own-solves.json',solveFrozenReceipt='solve-frozen-before-reveal.json',ratings='ratings-before.json',frozenRatingsReceipt='ratings-frozen.json',beforeScoreTotal=23,beforeMean=4.6,targetQuestionsChanged=1,relatedPrior295Rechecked=0,relatedPrior295Changed=0,sourceKeyModels=['source-key-checks.json','pre-reveal-exact-models.json'],repairChecks='repair-semantic-checks.json',hostLogs=logs,hostSuccessfulTestCount=13,afterHostScope='All5 six host checks plus1 prefix-order regression',visualReview='visual-review.json',preservation='preservation-check.json',solvesFrozenBeforeReveal=5,previouslyExposedOfficialAnswers=2,firstPassAnswerMatches=5,firstPassReasoningCorrections=1,limitations='Same-author review, not independent. Source30 raster prose improved; formula retained. Own d36 reasoning narrowed to unambiguous swapped values after reveal; published explanation already correct. All605 individual batches verified, related-cause queues and final release still pending.'))
print('605 individual target reviews verified; cross-queue closure/final validation/build still pending')
