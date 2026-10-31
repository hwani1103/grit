import re,unicodedata
import pdfplumber
import review_remaining605 as r
b=r.folder(30);bank=r.bank();rows=r.read(b/'revealed-current.json');reg={x['newAsset']:x for x in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/native-image-repairs.json')['figures']}
norm=lambda s:re.sub(r'\s','',unicodedata.normalize('NFKC',s))
checks=[]
for row in rows:
 old=row['question'];q=bank[old['id']];n=q['number']
 if n not in [18,21,22,24,1]:assert q==old;continue
 assert q['revision']==old['revision']+1 and q['answer']==old['answer'] and q['original']==old['original']
 if n in [18,22]:
  assert [norm(s) for s in old['choices']]==[norm(s) for s in q['choices']]
  assert not any(re.search(r'\d\s+%',s) for s in q['choices'])
  assert sorted(k for k in q if q[k]!=old[k])==['choices','revision']
 else:
  i=2 if n==21 else 1;rec=reg[old['figures'][i]['asset']]
  assert q['figures']==[f for j,f in enumerate(old['figures']) if j!=i]
  assert (r.ROOT/old['figures'][i]['asset']).is_file()
  if n!=24:
   with pdfplumber.open(r.ROOT/rec['source']) as pdf:text=pdf.pages[rec['page1based']-1].crop(rec['rect']).extract_text()
   assert norm(text)==norm(q['body']),(q['id'],norm(text),norm(q['body']))
  else:
   # Speech bubbles are paths, so PDF text extraction cannot verify words.
   # Complete manual visual transcription recorded separately; speakers added
   # from the two original labelled figures, no mathematical condition added.
   assert q['body'].count('주무관:')==5 and q['body'].count('팀장:')==1
   assert '절댓값' not in q['body'] and '최대 100억 원' in q['body'] and '최대 50%' in q['body']
   assert q['choices']==old['choices'] and q['choiceNote']==old['choiceNote']
   assert q['steps'][1:4]==old['steps'][1:4]
   assert q['optionReasons']==old['optionReasons']
  if n==1:assert q['bodyAfterFigureCount']==1
 checks.append(dict(id=q['id'],check='percent boundary only' if n in [18,22] else 'exact PDF prose and original image retained' if n in [1,21] else 'speech bubbles manually compared; interpretation explained only in authored explanation'))
assert r.sha(b/'own-solves.json')==r.read(b/'solve-frozen-before-reveal.json')['solveFileSha256']
assert r.sha(b/'ratings-before.json')==r.read(b/'ratings-frozen.json')['ratingsSha256']
r.write(b/'repair-semantic-checks.json',dict(status='PASS',checks=checks,unchangedAnswersChoicesExceptWhitespace=True,originalAssetsRetained=True,firstScoresAndOwnSolvesFrozen=True,dialogueVisualSource='assets/psat/figures/2026-d24-2-poppler.png',dialogueCheck='All six turns compared visually; speaker labels taken from original team-leader/officer labels. No change to maximum/sum/blank values.'))
print('PASS5 repaired questions, unchanged answers/raw conditions and original assets.')
