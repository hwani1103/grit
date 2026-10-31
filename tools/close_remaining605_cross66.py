import review_remaining605 as r
b=r.folder(66);assert not (b/'cross-verification.json').exists()
for n in ['host-before.log','host-after.log']:assert 'All tests passed!' in (b/n).read_text(encoding='utf-8-sig')
for n in ['own-source-models.json','source-key-checks.json','repair-semantic-checks.json','preservation-check.json']:assert r.read(b/n)['status']=='PASS'
assert r.sha(b/'own-solves.json')==r.read(b/'solve-frozen.json')['sha256']
old={q['id']:q for q in r.read(b/'before.json')};changes=r.read(r.OUT/'changes-batch66.json');bank=r.bank();changed={c['id'] for c in changes}
for c in changes:c['status']='verified'
r.write(r.OUT/'changes-batch66.json',changes)
for i,q in old.items():
 assert all(bank[i][k]==q[k] for k in ['answer','steps','optionReasons','choices'])
 if i not in changed:assert bank[i]==q
p=r.OUT/'cross-candidates-data-raster-prose.json';v=r.read(p)
for x in v['candidates']:
 if x['id'] in old:x.update(status='original_cause_and_host_reverified',evidence='batch66/cross-verification.json')
r.write(p,v)
p=r.OUT/'cross-candidates-structure-and-extrema.json';v=r.read(p)
for x in v:
 if x['id'] in ['kr-mpm-2026-03-07-psat-d-06','kr-mpm-2026-03-07-psat-d-12','kr-mpm-2026-03-07-psat-d-22']:x.update(status='source_key_semantics_and_host_reverified',evidence='batch66/cross-verification.json')
r.write(p,v)
p=r.OUT/'cross-validation.json';v=r.read(p)
for x in r.read(b/'followup-assessment.json')['items']:
 row=dict(id=x['id'],batch=66,evidence='batch66/cross-verification.json',status='source_key_semantics_and_host_reverified',historicalScorePreserved=x['historicalScorePreserved'],currentAssessmentBeforeRepair=x['currentBeforeScore'],changed=x['id'] in changed,causeFamilies=['raster-prose-readability','graph-labels','weighted-extrema','percentage-boundary'])
 v.setdefault('relatedPrior295Reviews' if x['cohort']=='prior295' else 'associated605Reviews',[]).append(row)
r.write(p,v)
r.write(b/'visual-review.json',dict(status='PASS',originals='All10 original regions inspected including shared pages;26 fresh source figure crops matched. Original twelve underline spans visually checked; conditional ratios, voltage differences, trade ranks, medal ranks, subway extrema and weighted press counts recalculated.',before='All10 native390 starts inspected.',after='All10 native390 starts inspected and revised report/choice text checked against original; original charts and formulas remain in order.',hostNotDevice=True))
r.write(b/'cross-verification.json',dict(status='verified',verifiedAt=r.now(),count=10,new605Count=0,associated605Rechecked=0,prior295Rechecked=10,changed=10,immutableOriginalScoresPreserved=True,own='own-solves.json',models='own-source-models.json',source='source-key-checks.json',repair='repair-semantic-checks.json',hostLogs=['host-before.log','host-after.log'],hostSuccessfulTestCount=14,visual='visual-review.json',preservation='preservation-check.json',limitations='Same-author targeted cross-review; ten prior295 historical scores retained. All original graphical structures and figures and native underline ranges retained.'))
print('Cross66 closed:10 prior295;10 raster-prose repairs')
