import re,unicodedata,hashlib
import pdfplumber
import review_remaining605 as r
b=r.folder(21)
norm=lambda s:re.sub(r'[\s<>〈〉]','',unicodedata.normalize('NFKC',re.sub('[·ㆍ]','',s)))
old={x['question']['id']:x['question'] for x in r.read(b/'revealed-current.json')}
current=r.bank(); specs=r.read(b/'native-prose-transcriptions.json')['transcriptions']
registry={x['newAsset']:x for x in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/native-image-repairs.json')['figures']}
checks=[]
for qid,s in specs.items():
    before=old[qid];after=current[qid];chunks=[]
    for index in s['remove']:
        record=registry[before['figures'][index]['asset']]
        with pdfplumber.open(r.ROOT/record['source']) as pdf:
            chunks.append(pdf.pages[record['page1based']-1].crop(record['rect']).extract_text() or '')
    actual=norm(after['body']);expected=norm(''.join(chunks))
    assert actual==expected,(qid,actual,expected)
    assert after['figures']==[f for i,f in enumerate(before['figures']) if i not in s['remove']]
    for k in ['answer','choices','prompt','steps','optionReasons','pitfall','transfer','original','source']:
        assert before.get(k)==after.get(k),(qid,k)
    assert bool(after.get('figuresAfterBody'))==bool(s.get('figuresAfterBody'))
    checks.append(dict(id=qid,nativeBodyMatchesPDF=True,retainedFiguresUnchanged=True,answerChoicesExplanationPreserved=True))
for qid in ['kr-mpm-2021-07-10-psat-d-24','kr-mpm-2025-11-15-psat-d-05']:
    before=old[qid];after=current[qid]
    assert len(before['steps'])==len(after['steps'])==5
    assert all(norm(a)==norm(z) for a,z in zip(before['steps'],after['steps']))
    assert {k:v for k,v in before.items() if k not in ['revision','steps']}=={k:v for k,v in after.items() if k not in ['revision','steps']}
    checks.append(dict(id=qid,onlyStepWhitespaceChanged=True))
assert hashlib.sha256((b/'own-solves.json').read_bytes()).hexdigest()==r.read(b/'solve-frozen-before-reveal.json')['solveFileSha256']
assert hashlib.sha256((b/'ratings-before.json').read_bytes()).hexdigest()==r.read(b/'ratings-frozen.json')['ratingsSha256']
r.write(b/'repair-semantic-checks.json',dict(status='PASS',checks=checks,firstSolvesAndRatingsUnchanged=True))
print('PASS six PDF-exact prose blocks; two whitespace-only explanations; frozen records intact.')
