import review_remaining605 as r
b=r.folder(48);assert not (b/'batch-verification.json').exists()
logs=['host-before.log','related295-host-before.log','host-after.log']
for n in logs:assert 'All tests passed!' in (b/n).read_text(encoding='utf-8-sig')
for file,receipt,key in [('own-solves.json','solve-frozen-before-reveal.json','solveFileSha256'),('ratings-before.json','ratings-frozen.json','ratingsSha256'),('related295-own-solves.json','related295-solve-frozen.json','sha256')]:assert r.sha(b/file)==r.read(b/receipt)[key]
for n in ['source-native-pixel-checks.json','related295-source-native-pixel-checks.json','exact-model-checks.json','related295-underline-source-strokes.json','repair-semantic-checks.json','preservation-check.json']:assert r.read(b/n)['status']=='PASS'
changes=r.read(r.OUT/'changes-batch48.json')
for x in changes:x['status']='verified'
r.write(r.OUT/'changes-batch48.json',changes)
ids={x['id'] for x in r.read(b/'own-solves.json')+r.read(b/'related295-own-solves.json')}
for p in r.OUT.glob('cross-candidates-*.json'):
 v=r.read(p);rows=v if isinstance(v,list) else v.get('candidates',[]);changed=False
 for x in rows:
  if isinstance(x,dict) and x.get('id') in ids:
   x.update(status='source_semantics_and_host_reverified',evidence='batch48/batch-verification.json');changed=True
   if p.name=='cross-candidates-underline-period46.json':x.update(status='source_terminal_strokes_match_including_periods',evidence='batch48/related295-underline-source-strokes.json')
 if changed:r.write(p,v)
p=r.OUT/'cross-validation.json';v=r.read(p)
for x in v['findings']:
 if x['id'] in ['R605-006','R605-009','R605-011','R605-015']:x.setdefault('subsequentBatchRepairs',[]).append(dict(batch=48,ids=sorted(ids),evidence='batch48/batch-verification.json'))
for x in r.read(b/'related295-assessment-before.json'):v['relatedPrior295Reviews'].append(dict(id=x['id'],batch=48,causeFamilies=['data-prose-density','denominator-and-unit','underline-terminal-range','all-years-counterexample'],evidence='batch48/related295-source-native-pixel-checks.json',status='source_key_semantics_and_host_reverified',historicalScorePreserved=x['historicalScorePreserved'],currentAssessmentBeforeRepair=x['currentBeforeScore']))
r.write(p,v)
r.write(b/'visual-review.json',dict(status='PASS',before='All10 original source pages, original map/legend enlarged before reveal and all10 before-starts inspected. Both prior295 original pages and related-before-starts inspected before repair.',after='All12 after-starts1..3 and8 detail screenshots after-detail1..2 inspected: report between main and candidate tables, paragraphs, full3payment rules before statements, CO2subscript and A->B->C->D header, source-matched underline punctuation.',hostNotDevice=True))
r.write(b/'batch-verification.json',dict(status='verified',verifiedAt=r.now(),count=10,ownSolves='own-solves.json',solveFrozenReceipt='solve-frozen-before-reveal.json',ratings='ratings-before.json',frozenRatingsReceipt='ratings-frozen.json',beforeScoreTotal=47,beforeMean=4.7,targetQuestionsChanged=3,relatedPrior295Rechecked=2,relatedPrior295Changed=1,sourceKeyModels=['source-native-pixel-checks.json','related295-source-native-pixel-checks.json','exact-model-checks.json'],repairChecks='repair-semantic-checks.json',hostLogs=logs,hostSuccessfulTestCount=18,afterHostScope='All12 target+related questions in one6-check audit',visualReview='visual-review.json',preservation='preservation-check.json',solvesFrozenBeforeReveal=10,previouslyExposedOfficialAnswers=0,firstPassAnswerMatches=10,firstPassReasoningCorrections=4,ownCorrectionEvidence='post-reveal-reasoning-corrections.json',limitations='Same-author review, not independent. Allanswers matched but4own written explanations needed corrections after reveal; originals retained. Source41fresh figure crops,12exact models; no intermediate APK.'))
print('Batch48 verified10;480 total after refresh')
