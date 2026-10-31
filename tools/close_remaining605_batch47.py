import review_remaining605 as r
b=r.folder(47);assert not (b/'batch-verification.json').exists()
logs=['host-before.log','related295-host-before.log','host-after.log']
for n in logs:assert 'All tests passed!' in (b/n).read_text(encoding='utf-8-sig')
for file,receipt,key in [('own-solves.json','solve-frozen-before-reveal.json','solveFileSha256'),('ratings-before.json','ratings-frozen.json','ratingsSha256'),('related295-own-solves.json','related295-solve-frozen.json','sha256')]:assert r.sha(b/file)==r.read(b/receipt)[key]
for n in ['source-key-model-checks.json','related295-source-key-model-checks.json','repair-semantic-checks.json','preservation-check.json']:assert r.read(b/n)['status']=='PASS'
changes=r.read(r.OUT/'changes-batch47.json')
for x in changes:x['status']='verified'
r.write(r.OUT/'changes-batch47.json',changes)
ids={x['id'] for x in r.read(b/'own-solves.json')+r.read(b/'related295-own-solves.json')}
for p in r.OUT.glob('cross-candidates-*.json'):
 v=r.read(p);rows=v if isinstance(v,list) else v.get('candidates',[]);changed=False
 for x in rows:
  if isinstance(x,dict) and x.get('id') in ids:x.update(status='source_semantics_and_host_reverified',evidence='batch47/batch-verification.json');changed=True
 if changed:r.write(p,v)
p=r.OUT/'cross-validation.json';v=r.read(p)
for x in v['findings']:
 if x['id'] in ['R605-007','R605-013']:x.setdefault('subsequentBatchRepairs',[]).append(dict(batch=47,ids=sorted(ids),evidence='batch47/batch-verification.json'))
for x in r.read(b/'related295-assessment-before.json'):v['relatedPrior295Reviews'].append(dict(id=x['id'],batch=47,causeFamilies=['time-anchor','percent-inverse','shared-passage-readability'],evidence='batch47/related295-source-key-model-checks.json',status='source_key_semantics_and_host_reverified',historicalScorePreserved=x['historicalScorePreserved'],currentAssessmentBeforeRepair=x['currentBeforeScore']))
r.write(p,v)
r.write(b/'visual-review.json',dict(status='PASS',before='All10 original source images and all10 before-starts1..3 inspected; both related source pages and before-related inspected before repairs.',after='All12 after-starts1..3 and after-detail inspected: joined legal terms, heading/paragraph separation and shared solar-term classification; original rate table preserved and zoom exercised by audit.',hostNotDevice=True))
r.write(b/'batch-verification.json',dict(status='verified',verifiedAt=r.now(),count=10,ownSolves='own-solves.json',solveFrozenReceipt='solve-frozen-before-reveal.json',ratings='ratings-before.json',frozenRatingsReceipt='ratings-frozen.json',beforeScoreTotal=46,beforeMean=4.6,targetQuestionsChanged=4,relatedPrior295Rechecked=2,relatedPrior295Changed=1,sourceKeyModels=['source-key-model-checks.json','related295-source-key-model-checks.json'],repairChecks='repair-semantic-checks.json',hostLogs=logs,hostSuccessfulTestCount=18,afterHostScope='All12 target+related questions in one6-check audit',visualReview='visual-review.json',preservation='preservation-check.json',solvesFrozenBeforeReveal=10,previouslyExposedOfficialAnswers=0,firstPassAnswerMatches=10,firstPassReasoningCorrections=0,limitations='Same-author review, not independent. Direct original/key/native comparison and fresh pixel table crop;1000 exhaustive self-reference candidates; no intermediate APK.'))
print('Batch47 verified10;470 total after refresh')
