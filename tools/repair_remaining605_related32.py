import re
import pdfplumber
import review_remaining605 as r
b=r.folder(32);before=r.read(b/'related295-before.json')[0];qid=before['id']
assert 'All tests passed!' in (b/'related295-host-before.log').read_text(encoding='utf-8-sig')
historic=next(x for x in r.read(r.PREP/'previously-scored295.json')['questions'] if x['id']==qid)
assert historic['scoreBeforeFix']==5
r.write(b/'related295-assessment-before.json',dict(id=qid,historicalScorePreserved=5,currentBeforeScore=4,assessment='원문 여섯 곳의 법령명 인용 괄호가 PDF 추출에서 사라져 조사 앞 공백이 남았다. 직접 풀이와 기존 다섯 선지·5단계 해설은 정확하다. 여섯 인용을 복원하고 상/은/에를 붙인다.',historicalEvidence=historic['evidence'],notReplacementOfHistoricalScore=True))
ledger=next(x for x in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/current900-evidence-ledger.json')['questions'] if x['id']==qid)
with pdfplumber.open(r.ROOT/ledger['officialKey']) as pdf:pi,t=next((i+1,p.extract_text()) for i,p in enumerate(pdf.pages) if '영역 언어논리' in (p.extract_text() or ''))
assert '2023' in t and '책형 인' in t.replace('㉯','나')
answers={}
for line in t.splitlines():
 if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):v=list(map(int,line.split()));answers.update(zip(v[::2],v[1::2]))
assert answers[24]==before['answer']==r.read(b/'related295-own-solves.json')[0]['answer']==5
src=r.read(b/'related295-source.json')['sourceText'];src=re.sub(r'^.*?24[.]\s*','',src,flags=re.S)
norm=lambda s:re.sub(r'[\s①②③④⑤「」□]','',s)
assert norm(src)==norm(before['prompt']+before['body']+''.join(before['choices']))
changes=r.read(r.OUT/'changes-batch32.json');found=False
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 for q in data:
  if q['id']!=qid:continue
  assert q==before;found=True;snap=r.OUT/f"before-changes/{qid}-r{q['revision']}.json";assert not snap.exists();r.write(snap,before)
  assert q['body'].count('재난안전법')==5 and q['body'].count('지방자치법')==1
  q['body']=q['body'].replace('재난안전법','「재난안전법」').replace('지방자치법','「지방자치법」')
  q['body']=re.sub(r'」 (상|은|에)',r'」\1',q['body']);q['revision']+=1
  assert norm(q['body'])==norm(before['body']) and q['steps']==before['steps'] and q['optionReasons']==before['optionReasons']
  changes.append(dict(id=qid,file=p.relative_to(r.ROOT).as_posix(),oldRevision=before['revision'],newRevision=q['revision'],changedFields=['body'],beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason='Restore six visually confirmed original statutory quotation marks and attached particles; no semantic alteration.',cohort='prior295',status='repaired_pending_reverification'));r.write(p,data);break
assert found;r.write(r.OUT/'changes-batch32.json',changes)
assert r.sha(b/'related295-own-solves.json')==r.read(b/'related295-solve-frozen.json')['sha256']
r.write(b/'related295-source-key-checks.json',dict(status='PASS',id=qid,source=r.read(b/'related295-source.json'),key=ledger['officialKey'],keyPage=pi,answer=5,nativeAndChoicesExactIgnoringRestoredQuoteMarks=True,sourceQuoteOccurrences=6,ownAndHistoricalRatingsPreserved=True,visualOriginal='related295-l24-source.png'))
print('Prior295 l24 r4→5 original six law quotation marks restored; original/key/solve checks PASS.')
