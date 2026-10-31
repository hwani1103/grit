import re,unicodedata
import pdfplumber
import review_remaining605 as r
b=r.folder(27);rows=r.read(b/'revealed-current.json');bank=r.bank();reg={x['newAsset']:x for x in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/native-image-repairs.json')['figures']};checks=[]
indices={25:1,2:1,7:1,8:1,9:0,11:1,12:1}
norm=lambda s:re.sub(r'\s','',unicodedata.normalize('NFKC',s))
for row in rows:
 old=row['question'];q=bank[old['id']];n=q['number'];fields=sorted(k for k in q.keys()|old.keys() if q.get(k)!=old.get(k))
 if n in indices:
  i=indices[n];rec=reg[old['figures'][i]['asset']]
  with pdfplumber.open(r.ROOT/rec['source']) as pdf:text=pdf.pages[rec['page1based']-1].crop(rec['rect']).extract_text()
  assert norm(text)==norm(q['body']),(q['id'],norm(text),norm(q['body']))
  assert q['figures']==[f for j,f in enumerate(old['figures']) if j!=i]
  assert fields==sorted(['body','figures','revision']+(['figuresAfterBody'] if n==9 else ['bodyAfterFigureCount'] if n==7 else []))
  if n==9:assert q['figuresAfterBody']
  if n==7:assert q['bodyAfterFigureCount']==1
  checks.append(dict(id=q['id'],exactSourceProse=True,sourcePage=rec['page1based'],sourceRect=rec['rect'],originalDisplayAssetRetained=(r.ROOT/old['figures'][i]['asset']).is_file(),order='report before choices' if n==9 else 'table/report/four choice tables' if n==7 else 'table or graph before prose'))
 elif n==23:
  assert fields==['choices','revision'];assert [norm(s) for s in q['choices']]==[norm(s) for s in old['choices']]
  assert not any(re.search(r'\d\s+%',s) for s in q['choices']);checks.append(dict(id=q['id'],choicePercentWhitespaceOnly=True))
 else:assert q==old
 if n in indices or n==23:assert q['revision']==old['revision']+1
assert r.sha(b/'own-solves.json')==r.read(b/'solve-frozen-before-reveal.json')['solveFileSha256']
assert r.sha(b/'ratings-before.json')==r.read(b/'ratings-frozen.json')['ratingsSha256']
r.write(b/'repair-semantic-checks.json',dict(status='PASS',checks=checks,ownSolvesAndFirstScoresUnchanged=True,allStepsReasonsAnswersUnchanged=True,existingNonnegativeIncomeLimitationPreserved=True))
print('PASS7 exact source prose, preserved original sequence;1 percent-choice whitespace-only repair.')
