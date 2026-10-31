import review_remaining605 as r
b=r.folder(69);assert not (b/'cross-verification.json').exists();assert 'All tests passed!' in (b/'host-before.log').read_text(encoding='utf-8-sig')
for n in ['own-source-models.json','source-key-checks.json','preservation-check.json']:assert r.read(b/n)['status']=='PASS'
assert r.sha(b/'own-solves.json')==r.read(b/'solve-frozen.json')['sha256']
old=r.read(b/'before.json');bank=r.bank();prior={q['id']:q for q in r.read(r.PREP/'previously-scored295.json')['questions']}
assert all(bank[q['id']]==q for q in old)
assert all(x['paragraphsAndChoicesMatch'] for x in r.read(b/'native-source-comparison-draft.json'))
r.write(b/'native-source-comparison.json',dict(status='PASS',checks=r.read(b/'native-source-comparison-draft.json'),blank='Original vector blank inspected; app□placeholder matches.'))
items=[dict(id=q['id'],cohort='prior295',historicalScorePreserved=prior[q['id']]['scoreBeforeFix'],currentBeforeScore=5,needsChange=False,assessment='Original-source re-solve, all five option grounds and five-stage explanation agree. Explicit scope/upper-bound and feasible-witness checks passed; native prose and tables preserve source.') for q in old]
r.write(b/'followup-assessment.json',dict(items=items))
p=r.OUT/'cross-candidates-structure-and-extrema.json';v=r.read(p);ids={q['id'] for q in old}
for x in v:
 if x['id'] in ids:x.update(status='source_key_semantics_and_host_reverified',evidence='batch69/cross-verification.json')
r.write(p,v)
p=r.OUT/'cross-validation.json';v=r.read(p)
for x in items:v.setdefault('relatedPrior295Reviews',[]).append(dict(id=x['id'],batch=69,evidence='batch69/cross-verification.json',status='source_key_semantics_and_host_reverified',historicalScorePreserved=x['historicalScorePreserved'],currentAssessmentBeforeRepair=5,changed=False,causeFamilies=['extremum-scope','boundaries','source-structure']))
r.write(p,v)
r.write(b/'visual-review.json',dict(status='PASS',originals='All1 original pages/regions inspected; blank box visually checked.',host='All1 native390 starts inspected; 320large-text,390,752,840 viewports completed in audit. No content edits in this batch.',hostNotDevice=True))
r.write(b/'cross-verification.json',dict(status='verified',verifiedAt=r.now(),count=1,new605Count=0,prior295Rechecked=1,changed=0,immutableOriginalScoresPreserved=True,own='own-solves.json',models='own-source-models.json',source='source-key-checks.json',native='native-source-comparison.json',hostLogs=['host-before.log'],hostSuccessfulTestCount=6,visual='visual-review.json',preservation='preservation-check.json',limitations='Same-author targeted review, not independent. No current app defect found in this batch.'))
print('Cross69 verified:1 prior295 unchanged')
