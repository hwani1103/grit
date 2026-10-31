import review_remaining605 as r
b=r.folder(62);assert not (b/'cross-verification.json').exists()
for n in ['host-before.log','host-after.log']:assert 'All tests passed!' in (b/n).read_text(encoding='utf-8-sig')
for n in ['terminal-period-check.json','source-key-checks.json','repair-semantic-checks.json','preservation-check.json']:assert r.read(b/n)['status']=='PASS'
old={q['id']:q for q in r.read(b/'before.json')};changes=r.read(r.OUT/'changes-batch62.json');bank=r.bank()
for c in changes:c['status']='verified'
r.write(r.OUT/'changes-batch62.json',changes)
for i,q in old.items():
 assert bank[i]['answer']==q['answer'] and bank[i]['steps']==q['steps'] and bank[i]['optionReasons']==q['optionReasons'] and bank[i]['choices']==q['choices']
 if i not in {c['id'] for c in changes}:assert bank[i]==q
for p in [r.OUT/'cross-candidates-data-raster-prose.json',r.OUT/'cross-candidates-underline-period46.json']:
 v=r.read(p);rows=v if isinstance(v,list) else v['candidates']
 for x in rows:
  if x['id'] in old:x.update(status='original_cause_and_host_reverified',evidence='batch62/cross-verification.json')
 r.write(p,v)
p=r.OUT/'cross-validation.json';v=r.read(p);v.setdefault('associated605Reviews',[]).extend([dict(id=i,batch=62,evidence='batch62/cross-verification.json',status='original_cause_and_host_reverified',cause='terminal-period-original-stroke' if j<6 else 'raster-prose-readability',changed=i in {c['id'] for c in changes}) for j,i in enumerate(old)]);r.write(p,v)
r.write(b/'visual-review.json',dict(status='PASS',originals='All10 source pages inspected. Six underline controls have20 correctly included terminal dots. Four report/choice source regions compared with native transcription.',before='All10 native390 starts inspected.',after='All10 native390 starts and report7 full first body page inspected; source table/formula/report order preserved.',hostNotDevice=True))
r.write(b/'cross-verification.json',dict(status='verified',verifiedAt=r.now(),count=10,new605Count=0,associated605Rechecked=10,changed=4,prior295Rechecked=0,immutableOriginalScoresPreserved=True,source='source-key-checks.json',terminalPeriods='terminal-period-check.json',repair='repair-semantic-checks.json',hostLogs=['host-before.log','host-after.log'],hostSuccessfulTestCount=13,visual='visual-review.json',preservation='preservation-check.json',limitations='Targeted follow-up using already frozen individual605 solves; not independent or newly blind assessment.'))
print('Cross62 closed:6 unchanged underline controls +4 native prose improvements')
