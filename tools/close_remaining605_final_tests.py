import re
import review_remaining605 as r
out=r.OUT/'final';log=(out/'full-tests.log').read_text(encoding='utf-8-sig');assert r.read(out/'full-run-interruption.json')['status']=='interrupted_not_pass'
failed=re.findall(r'^\S+ \+\d+ -\d+: .*[/\\](test[/\\][^:]+): (.+) \[E\]$',log,re.M)
plan={x['file']:x for x in r.read(out/'test-changes.json')};covered=[]
unit=r.read(out/'updated-unit-test-titles.json')
widget=['all nine native situation tables fit cover and open widths','situation Set10 special text fits cover and opened fold','verbal Set11 special text fits cover and opened fold','verbal Set19 special text fits cover and opened fold']
for file,title in failed:
 file=file.replace('\\','/');assert file in plan,(file,title)
 old=(r.ROOT/plan[file]['beforeSnapshot']).read_text(encoding='utf-8-sig');new=(r.ROOT/file).read_text(encoding='utf-8-sig')
 oldunits=re.findall(r"(?<![A-Za-z])test\(\s*'([^']+)'",old);newunits=re.findall(r"(?<![A-Za-z])test\(\s*'([^']+)'",new)
 if title in oldunits:fixedtitle=newunits[oldunits.index(title)];assert fixedtitle in unit
 else:assert title in widget;fixedtitle=title
 covered.append(dict(file=file,originalTitle=title,retestedTitle=fixedtitle))
assert len(covered)==45,len(covered)
unitTag='unit-final';widgetTag='widget-final'
for tag in [unitTag,widgetTag]:
 assert r.read(out/(tag+'-exit.json'))['exitCode']==0
 assert 'All tests passed!' in (out/(tag+'.log')).read_text(encoding='utf-8-sig')
assert 'No issues found!' in (out/'analyze.log').read_text(encoding='utf-8-sig')
runs=r.read(out/'recovery-runs.json');assert runs['status']=='PASS' and len(runs['runs'])==30
for row in runs['runs']:
 assert row['exitCode']==0 and 'All tests passed!' in (r.ROOT/row['log']).read_text(encoding='utf-8-sig')
coverage={}
for kind in ['dialogs','transitions','explanations-752','explanations-840']:
 files=list((out/'recovery-scopes').glob(kind+'-*.json'));assert len(files)==9
 ids=[]
 for p in files:
  v=r.read(p);assert v['status']=='PASS' and v['kind']==kind and len(v['questionIds'])==100;ids+=v['questionIds']
 assert len(ids)==len(set(ids))==900 and set(ids)==set(r.bank())
 coverage[kind]=dict(count=900,distinct=900,ranges=9,allCatalogIdsCovered=True)
r.write(out/'recovery-coverage.json',dict(status='PASS',categories=coverage,initialSuccessfulOtherSizes=[320,390],method='Assertions are unchanged. Each new process covers100 IDs; successful scope receipts cover900 unique catalog IDs per category. Initial320/390 tests each logged900/900 and successful completion before host interruption.'))
r.write(out/'test-closure.json',dict(status='PASS',checkedAt=r.now(),initialFullLog='full-tests.log',initialFailures=45,allInitialFailuresMappedToSuccessfulRetests=True,retestedOrdinaryCount=len(unit),retestedWidgetCount=len(widget),resolved=covered,ordinaryLog=unitTag+'.log',widgetLog=widgetTag+'.log',recoveryLogIndex='recovery-runs.json', recoveryCoverage='recovery-coverage.json', initialRunInterrupted=True, method='Initial suite interrupted after182passes and45 stale-expectation failures by host runtime failure. All three active files recovered with fresh processes per100 IDs and full900 coverage proven per category, except two heavy PsatReader cases already passed; all45 failures mapped to successful reruns. Not a second full-suite run.'))
print('PASS all45 initial failures closed,46 ordinary tests and4 affected/new widget cases pass.')
