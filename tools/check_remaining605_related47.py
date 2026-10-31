import re,unicodedata
from fractions import Fraction as F
import pdfplumber
import review_remaining605 as r
b=r.folder(47);rows=r.read(b/'related295-before.json');src={x['id']:x for x in r.read(b/'related295-source.json')};own={x['id']:x for x in r.read(b/'related295-own-solves.json')};ledger={x['id']:x for x in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/current900-evidence-ledger.json')['questions']}
norm=lambda s:re.sub(r'\s','',unicodedata.normalize('NFKC',re.sub(r'[①②③④⑤]','',s.replace('ㆍ','·'))))
checks=[]
for q in rows:
 m=src[q['id']];s=re.sub(r'책형\s*\d+쪽','',m['sourceText']);s=re.sub(r'^\s*\[39～\s*40\] 다음 글을 읽고 물음에 답하시오[.]\s*','',s);s=re.sub(r'(?m)^\s*40[.]\s*','',s,count=1)
 assert norm(q['prompt']) in norm(s);s=norm(s).replace(norm(q['prompt']),'',1);assert norm(s)==norm(q['body']+''.join(q['choices'])),q['id']
 key=ledger[q['id']]['officialKey']
 with pdfplumber.open(r.ROOT/key) as pdf:pi,t=next((j+1,p.extract_text()) for j,p in enumerate(pdf.pages) if '영역 상황판단' in (p.extract_text() or ''))
 assert q['examDate'][:4] in t and f"책형 {q['book']}" in t.replace('㉮','가').replace('㉯','나');ans={}
 for line in t.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):z=list(map(int,line.split()));ans.update(zip(z[::2],z[1::2]))
 assert ans[q['number']]==q['answer']==own[q['id']]['answer'];checks.append(dict(id=q['id'],source=m['source'],page=m['page'],key=key,keyPage=pi,nativeAndFiveChoicesMatch=True,ownAnswerMatches=True))
terms=r.read(b/'source-key-model-checks.json')['solarTerms'];indices=[(terms.index(x)-terms.index('우수'))%24 for x in rows[0]['choices']];assert indices==[4,7,11,12,16]
sugar=12/F('.6');beef=sugar/F('2.5');amount=(52-sugar)/beef;assert sugar==20 and beef==8 and amount==4 and sugar+4*beef==52
current=r.bank();assert rows[0]['body'].split('<상 황>')[0].strip()==current['kr-mpm-2025-03-08-psat-s-39']['body'].split('<보 기>')[0].strip()
r.write(b/'related295-source-key-model-checks.json',dict(status='PASS',count=2,checks=checks,seasonOptionOffsets=indices,price=dict(sugar1884=20,beef1884=8,beefPurchased=4,checkBudget=52),shared39340PrefixIdentical=True))
print('PASS2 related original/key/native;5 offsets;price inverse and budget check')
