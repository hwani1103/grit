import re
import pdfplumber
import review_remaining605 as r
b=r.folder(35);q=r.read(b/'related295-before.json')[0];s=r.read(b/'related295-source.json')[0];own=r.read(b/'related295-own-solves.json')[0]
assert 'All tests passed!' in (b/'related295-host-before.log').read_text(encoding='utf-8-sig')
norm=lambda v:re.sub(r'[\s①②③④⑤]','',v).replace('ㆍ','·')
assert norm(re.sub(r'^23[.]\s*','',s['sourceText']))==norm(q['prompt']+q['body']+''.join(q['choices']))
key='artifacts/psat600_20261028/sources/5982/11eb95966d17447bb065c2c5fb0d4e05.pdf'
with pdfplumber.open(r.ROOT/key) as pdf:pi,t=next((i+1,p.extract_text()) for i,p in enumerate(pdf.pages) if '영역 상황판단' in (p.extract_text() or ''))
assert '2026' in t and '책형 나' in t.replace('㉯','나');ans={}
for line in t.splitlines():
 if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
  z=list(map(int,line.split()));ans.update(zip(z[::2],z[1::2]))
assert ans[23]==q['answer']==own['answer']==2
assert r.sha(b/'related295-own-solves.json')==r.read(b/'related295-solve-frozen.json')['sha256']
historic=next(x for x in r.read(r.PREP/'previously-scored295.json')['questions'] if x['id']==q['id'])
p=b/'related295-assessment-before.json';assert not p.exists();r.write(p,dict(id=q['id'],historicalScorePreserved=historic['scoreBeforeFix'],historicalEvidence=historic['evidence'],currentBeforeScore=4,assessment='면허·허가·신고, 공공·사유, 등록·연장·보고 경로가 모두 정확하다. 첫 괄호 뒤 조사 에서의 줄갈이 공백만 복원한다. batch01의 목록 구분 공백 수정은 유지한다.',notReplacementOfHistoricalScore=True));r.write(b/'related295-assessment-frozen.json',dict(frozenAt=r.now(),sha256=r.sha(p),beforeChanges=True))
changes=r.read(r.OUT/'changes-batch35.json');found=False
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 for item in data:
  if item['id']!=q['id']:continue
  assert item==q;snap=r.OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();r.write(snap,q)
  assert item['body'].count('같다) 에서')==1;item['body']=item['body'].replace('같다) 에서','같다)에서');item['revision']+=1
  assert norm(q['body'])==norm(item['body']) and q['steps']==item['steps'] and q['optionReasons']==item['optionReasons'];r.write(p,data)
  changes.append(dict(id=q['id'],file=p.relative_to(r.ROOT).as_posix(),oldRevision=q['revision'],newRevision=item['revision'],changedFields=['body'],beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason='Original particle boundary after parenthesis; all first-batch separator repairs and semantic proof preserved.',cohort='prior295',status='repaired_pending_reverification'));found=True;break
assert found;r.write(r.OUT/'changes-batch35.json',changes)
r.write(b/'related295-source-key-model-checks.json',dict(status='PASS',id=q['id'],source=s['source'],sourcePage=s['page'],nativeAndChoicesMatch=True,key=key,keyPage=pi,answer=2,ownMatches=True,branches=dict(publicTrap='report under first article3',privateTrap='report under second article2'),unregisteredLicense='No fishing right without registration;5-year base, not10.',publicProject='Exception to obligatory extension.',unchangedStepsReasonsAndEarlierRepair=True))
r.write(b/'sample-with-related.json',dict(sample=[dict(id=x['id']) for x in r.batch(35)]+[dict(id=q['id'])]))
print('PASS related source/key/semantics;historic5 preserved;current4 frozen;r4->5')
