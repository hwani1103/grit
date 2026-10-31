import re,unicodedata
import pdfplumber
import review_remaining605 as r
b=r.folder(33);bank=r.bank();rows=r.read(b/'revealed-current.json');reg={x['newAsset']:x for x in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/native-image-repairs.json')['figures']}
norm=lambda s:re.sub(r'[\s·ㆍ]','',unicodedata.normalize('NFKC',s))
indices={2:1,4:0,5:0,7:2,8:1,13:1,17:1,18:1};checks=[]
for row in rows:
 before=row['question'];q=bank[before['id']];n=q['number']
 assert q['revision']==before['revision']+1 and q['answer']==before['answer'] and q['original']==before['original']
 assert [norm(s) for s in q['choices']]==[norm(s) for s in before['choices']]
 if n in indices:
  i=indices[n];rec=reg[before['figures'][i]['asset']]
  assert q['figures']==[f for j,f in enumerate(before['figures']) if i!=j]
  assert (r.ROOT/before['figures'][i]['asset']).is_file()
  with pdfplumber.open(r.ROOT/rec['source']) as pdf:raw=pdf.pages[rec['page1based']-1].crop(rec['rect']).extract_text()
  assert norm(raw)==norm(q['body']),(q['id'],norm(raw),norm(q['body']))
  if n in [4,5]:assert q['bodyAfterFigureCount']==0
  else:assert not q.get('figuresAfterBody') and q.get('bodyAfterFigureCount') is None
 else:
  assert not any(re.search(r'\d\s+%',s) for s in q['choices'])
  assert sorted(k for k in q if q[k]!=before[k])==['choices','revision']
 assert len(q['steps'])==len(q['optionReasons'])==5
 checks.append(dict(id=q['id'],originalProseExact=n in indices,figureBlockIndex=indices.get(n),sourceAssetsRetained=True,answerAndChoicesPreserved=True))
assert r.sha(b/'own-solves.json')==r.read(b/'solve-frozen-before-reveal.json')['solveFileSha256']
assert r.sha(b/'ratings-before.json')==r.read(b/'ratings-frozen.json')['ratingsSha256']
r.write(b/'repair-semantic-checks.json',dict(status='PASS',checks=checks,sourceProseBlocks=8,percentOnlyQuestions=2,originalAssetsRetained=True,firstScoresAndOwnSolvesFrozen=True))
print('PASS8 exact source prose blocks,2 percent-only choices,all answers/immutable evidence retained.')
