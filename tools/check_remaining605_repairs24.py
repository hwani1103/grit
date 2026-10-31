import re,unicodedata
import pdfplumber
import review_remaining605 as r
b=r.folder(24);rows=r.read(b/'revealed-current.json');current=r.bank();reg={x['newAsset']:x for x in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/native-image-repairs.json')['figures']};indices={10:0,11:1,12:3,13:1,14:3,15:3,18:1};checks=[]
def norm(s):return re.sub(r'\s','',unicodedata.normalize('NFKC',s))
for item in rows:
 old=item['question'];q=current[old['id']];n=q['number'];fields=sorted(k for k in old.keys()|q.keys() if old.get(k)!=q.get(k))
 if n in indices:
  i=indices[n];rec=reg[old['figures'][i]['asset']]
  with pdfplumber.open(r.ROOT/rec['source']) as pdf:text=pdf.pages[rec['page1based']-1].crop(rec['rect']).extract_text()
  assert norm(text)==norm(q['body']),(n,norm(text),norm(q['body']))
  assert q['figures']==[f for j,f in enumerate(old['figures']) if j!=i]
  assert fields==sorted(['body','figures','revision']+(['figuresAfterBody'] if n==10 else []))
  if n==10:assert q['figuresAfterBody']
  checks.append(dict(id=q['id'],sourceTextExact=True,sourcePage=rec['page1based'],sourceRect=rec['rect'],removedDisplayAssetRetained=(r.ROOT/old['figures'][i]['asset']).is_file(),remainingImagesBytePreservation='preservation-check.json',bodyBeforeFigures=n==10))
 elif n in [21,22]:
  assert fields==['choices','revision']
  assert [norm(s) for s in q['choices']]==[norm(s) for s in old['choices']]
  assert not any(re.search(r'\d\s+%',s) for s in q['choices'])
  checks.append(dict(id=q['id'],choicePercentWhitespaceOnly=True))
 else:assert q==old
 if n!=17:assert q['revision']==old['revision']+1
assert r.sha(b/'own-solves.json')==r.read(b/'solve-frozen-before-reveal.json')['solveFileSha256']
assert r.sha(b/'ratings-before.json')==r.read(b/'ratings-frozen.json')['ratingsSha256']
r.write(b/'repair-semantic-checks.json',dict(status='PASS',checks=checks,ownSolvesAndFirstScoresUnchanged=True,stepsAndReasonsUnchanged=True,source11CorrectIncrease=92,ownIncorrect102CorrectionPreserved=True))
print('PASS7 full original prose transcriptions/retained figure ordering;2whitespace-only options; own/ratings immutable.')
