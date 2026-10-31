import re,pdfplumber
import review_remaining605 as r
b=r.folder(65);old={q['id']:q for q in r.read(b/'before.json')};reg={x['newAsset']:x for x in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/native-image-repairs.json')['figures']}
assert 'All tests passed!' in (b/'host-before.log').read_text(encoding='utf-8-sig');assert r.read(b/'own-source-models.json')['status']=='PASS';assert r.sha(b/'own-solves.json')==r.read(b/'solve-frozen.json')['sha256']
for x in r.read(b/'own-solves.json'):assert old[x['id']]['answer']==x['answer']
configs={'kr-mpm-2021-07-10-psat-d-13':(1,1),'kr-mpm-2021-07-10-psat-d-21':(1,1),'kr-mpm-2021-07-10-psat-d-22':(4,4),'kr-mpm-2025-11-15-psat-d-03':(2,2),'kr-mpm-2025-11-15-psat-d-04':(1,1),'kr-mpm-2025-11-15-psat-d-06':(1,1),'kr-mpm-2025-11-15-psat-d-16':(1,1),'kr-mpm-2025-11-15-psat-d-24':(1,1),'kr-mpm-2026-07-18-psat-d-03':(1,1)}
norm=lambda s:re.sub(r'\s','',s);plans={};proof=[]
for i,(fi,pos) in configs.items():
 f=old[i]['figures'][fi];v=reg[f['asset']]
 with pdfplumber.open(r.ROOT/v['source']) as pdf:raw=pdf.pages[v['page1based']-1].crop(v['rect']).extract_text()
 text=' '.join(raw.splitlines()).replace('<보고서> ','<보고서>\n\n').replace('<보 기> ','<보 기>\n\n')
 text=re.sub(r' (?=[ㄱ-ㅎ][.] )','\n\n',text)
 # Source line wraps split these two words; do not store a false internal space.
 text=text.replace('지역문화 재단','지역문화재단').replace('철도ㆍ 궤도신설공사','철도ㆍ궤도신설공사')
 text=text.replace('종합 점수','종합점수').replace('설계적설 하중','설계적설하중').replace('(나) 로','(나)로').replace('(다) .','(다).')
 assert norm(raw)==norm(text);plans[i]=(fi,pos,text);proof.append(dict(id=i,asset=f['asset'],source=v['source'],page=v['page1based'],rect=v['rect'],nativeText=text,sourceExactIgnoringWhitespace=True,originalAssetPreserved=True,allOtherFiguresUnchanged=True))
prior={x['id']:x for x in r.read(r.PREP/'previously-scored295.json')['questions']}
assert not (b/'followup-assessment.json').exists();r.write(b/'followup-assessment.json',dict(scope='10 prior295. Recalculated all10 from originals and compared five options/5-stage explanations; original historical scores retained.',items=[dict(id=i,cohort='prior295' if i in prior else 'associated605',historicalScorePreserved=prior[i]['scoreBeforeFix'] if i in prior else 'original ratings-before.json',currentBeforeScore=3 if i in plans else 5,needsChange=i in plans,assessment='All calculations and option grounds agree. Long prose-only raster becomes native text.' if i in plans else 'Original contains short formula+table or actual charts, not a prose-only block. Original graphical structure, legends and symbols retained; zoom remains available.') for i in old]))
changes=[]
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  if q['id'] not in plans:continue
  fi,pos,text=plans[q['id']];prev=old[q['id']];assert q==prev;snap=r.OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();r.write(snap,prev)
  q['figures'].pop(fi);q['body']=text;q['bodyAfterFigureCount']=pos
  if q['id']=='kr-mpm-2025-11-15-psat-d-03':q['steps'][1]=q['steps'][1].replace('ㄱ,1인','ㄱ, 1인')
  if q['id']=='kr-mpm-2025-11-15-psat-d-06':q['optionReasons'][3]=q['optionReasons'][3].replace('높아(가)','높아 (가)')
  assert all(norm(q[k][j])==norm(prev[k][j]) for k in ['steps','optionReasons'] for j in range(5))
  fields=[k for k in q if q[k]!=prev.get(k)];q['revision']+=1;touched=True;changes.append(dict(id=q['id'],file=p.relative_to(r.ROOT).as_posix(),oldRevision=prev['revision'],newRevision=q['revision'],changedFields=fields,beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason='Original prose-only report/choices moved to native body in the same source order; historical ratings and all graphics preserved.',status='repaired_pending_reverification'))
 if touched:r.write(p,data)
assert len(changes)==9;r.write(r.OUT/'changes-batch65.json',changes);r.write(b/'repair-semantic-checks.json',dict(status='PASS',checks=proof,allAnswersChoicesUnchanged=True,explanationChangesWhitespaceOnly=True));r.write(b/'after-sample.json',r.read(b/'sample.json'));print('Nine prose repairs; ship graphs unchanged')
