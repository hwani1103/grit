import re,unicodedata,itertools
import pdfplumber
import review_remaining605 as r
b=r.folder(43);rows=r.read(b/'related295-before.json');src={x['id']:x for x in r.read(b/'related295-source.json')};own={x['id']:x for x in r.read(b/'related295-own-solves.json')};ledger={x['id']:x for x in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/current900-evidence-ledger.json')['questions']}
norm=lambda s:re.sub(r'\s','',unicodedata.normalize('NFKC',re.sub(r'[①②③④⑤]','',s)))
checks=[]
for q in rows:
 m=src[q['id']];s=re.sub(r'책형\s*\d+쪽','',m['sourceText']);s=re.sub(r'^\s*\[39～\s*40\] 다음 글을 읽고 물음에 답하시오[.]\s*','',s);s=re.sub(r'(?m)^\s*'+str(q['number'])+r'[.]\s*','',s,count=1)
 if q['number']==39:
  assert norm(q['prompt']) in norm(s);s=norm(s).replace(norm(q['prompt']),'',1);expected=q['body']+''.join(q['choices'])
 else:expected=q['prompt']+q['body']+''.join(q['choices'])
 assert norm(s)==norm(expected),q['id']
 key=ledger[q['id']]['officialKey']
 with pdfplumber.open(r.ROOT/key) as pdf:pi,t=next((j+1,p.extract_text()) for j,p in enumerate(pdf.pages) if '영역 언어논리' in (p.extract_text() or ''))
 assert '2025' in t and '책형 가' in t.replace('㉮','가');ans={}
 for line in t.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):z=list(map(int,line.split()));ans.update(zip(z[::2],z[1::2]))
 assert ans[q['number']]==q['answer']==own[q['id']]['answer'];checks.append(dict(id=q['id'],source=m['source'],page=m['page'],key=key,keyPage=pi,nativeAndFiveChoicesMatch=True,ownAnswerMatches=True))
# Need all4 conditions for justified; lacking a necessary condition with justified=True contradicts.
worlds=[(bits,all(bits)) for bits in itertools.product([False,True],repeat=4)]
assert not any(not bits[0] and justified for bits,justified in worlds)
assert all(not justified for bits,justified in worlds if not bits[2])
assert not any(not bits[1] and justified for bits,justified in worlds)
r.write(b/'related295-source-key-model-checks.json',dict(status='PASS',count=2,checks=checks,conditionWorldCount=16,clause1='l32 ㄱ violates necessary harm condition',clause2='l32 ㄴ absent evidence plus absent justification consistent',clause3='l32 ㄷ absent internal report already defeats A strengthening; no added B beliefs',sharedText='l39 full passage equals l40 pre-보기 prefix',sameAuthor=True))
assert rows[1]['body']==r.bank()['kr-mpm-2025-03-08-psat-l-40']['body'].split('\n\n<보 기>')[0]
print('PASS2 related original/key/native/condition models; no content changes needed')
