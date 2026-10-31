import re
import pdfplumber
import review_remaining605 as r
b=r.folder(34);q=r.read(b/'related295-before.json')[0];own=r.read(b/'related295-own-solves.json')[0]
assert 'All tests passed!' in (b/'related295-host-before.log').read_text(encoding='utf-8-sig')
norm=lambda s:re.sub(r'[\s①②③④⑤]','',s)
source=r.read(b/'related295-source.json')[0]
assert norm(re.sub(r'^11[.]\s*','',source['sourceText']))==norm(q['prompt']+q['body']+''.join(q['choices']))
key='artifacts/psat_batch01_20261028/sources/4342_e8e66da6cb48.pdf'
with pdfplumber.open(r.ROOT/key) as pdf:pi,t=next((i+1,p.extract_text()) for i,p in enumerate(pdf.pages) if '언어논리' in (p.extract_text() or ''))
assert '2023' in t and '인' in t
ans={}
for line in t.splitlines():
 if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
  z=list(map(int,line.split()));ans.update(zip(z[::2],z[1::2]))
assert ans[11]==q['answer']==own['answer']==1
assert r.sha(b/'related295-own-solves.json')==r.read(b/'related295-solve-frozen.json')['sha256']
prior=next(x for x in r.read(r.PREP/'previously-scored295.json')['questions'] if x['id']==q['id'])
assessment=b/'related295-assessment-before.json';assert not assessment.exists();r.write(assessment,dict(id=q['id'],historicalScorePreserved=prior['scoreBeforeFix'],historicalEvidence=prior['evidence'],currentBeforeScore=4,assessment='다른 요인 배제와 확률동일 반례를 잘 설명한다.20 %/80 %/10 % 경계 및 ④·⑤ 개별 근거의 단순 판정을 보완한다.',notReplacementOfHistoricalScore=True))
receipt=b/'related295-assessment-frozen.json';r.write(receipt,dict(frozenAt=r.now(),sha256=r.sha(assessment),beforeChanges=True))
changes=r.read(r.OUT/'changes-batch34.json');found=False
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 for item in data:
  if item['id']!=q['id']:continue
  assert item==q;snap=r.OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();r.write(snap,q)
  item['body']=re.sub(r'(20|80|10) %',r'\1%',item['body'])
  item['optionReasons'][3]='ㄴ은 다른 요인 배제 없이 확률 증가만으로 충분하다고 했고, ㄷ은 확률이 그대로여도 긍정적 효과가 없다는 반례를 놓쳤다.'
  item['optionReasons'][4]='ㄱ은 변화 없음과 다른 요인 배제를 함께 요구해 맞다. ㄴ은 통제 조건 누락, ㄷ은 동일 확률 반례 때문에 틀리므로 세 진술을 모두 고를 수 없다.'
  item['revision']+=1;assert norm(item['body'])==norm(q['body']) and item['steps']==q['steps'];r.write(p,data)
  changes.append(dict(id=q['id'],file=p.relative_to(r.ROOT).as_posix(),oldRevision=q['revision'],newRevision=item['revision'],changedFields=['body','optionReasons'],beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason='Probability boundary and control-condition crosscheck; repair percent word boundary and specific option4/5 reasons.',cohort='prior295',status='repaired_pending_reverification'));found=True;break
assert found;r.write(r.OUT/'changes-batch34.json',changes)
r.write(b/'related295-source-key-model-checks.json',dict(status='PASS',id=q['id'],nativeAndChoicesMatch=True,key=key,keyPage=pi,answer=1,ownMatches=True,controlledNoEffectCounterexample=dict(before=.2,after=.2,positive=False,lower=False),confoundingExample='Observed .2->.8 may be entirely due to another cause; increase alone insufficient.',unchangedFiveSteps=True,wordsAndAnswerPreserved=True))
print('PASS related295 source/key/model;historic4 preserved;current4 frozen;r5->6')
