import re
from fractions import Fraction as F
import pdfplumber
import review_remaining605 as r
b=r.folder(34);rows=r.read(b/'revealed-current.json');src={x['id']:x for x in r.read(b/'blind-source.json')};own={x['id']:x for x in r.read(b/'own-solves.json')}
norm=lambda s:re.sub(r'[\s①②③④⑤\uf000『』]','',s).replace('[빈칸]','').replace('ㆍ','·')
checks=[]
for row in rows:
 q=row['question'];m=src[q['id']];native=re.sub(r'책형\s*\d+쪽','',m['sourceText']);native=re.sub(r'^\s*\d+[.]\s*','',native)
 assert norm(native)==norm(q['prompt']+q['body']+''.join(q['choices'])),q['id']
 with pdfplumber.open(r.ROOT/row['officialKey']) as pdf:pi,t=next((i+1,p.extract_text()) for i,p in enumerate(pdf.pages) if '영역 언어논리' in (p.extract_text() or ''))
 assert q['examDate'][:4] in t and f"책형 {q['book']}" in t.replace('㉯','나')
 ans={}
 for line in t.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
   z=list(map(int,line.split()));ans.update(zip(z[::2],z[1::2]))
 assert ans[q['number']]==q['answer']==own[q['id']]['answer']
 checks.append(dict(id=q['id'],source=m['source'],page=m['page'],nativeAndFiveChoices=True,key=row['officialKey'],keyPage=pi,ownMatches=True))
# Explicit finite countermodels supplement the source-based reading review.
wealthModels=[(w,rite) for w in [False,True] for rite in [False,True] if not rite or w]
assert (False,True) not in wealthModels and (True,False) in wealthModels
luck=F(1,10)
for skill in [F(0),F(1,4),F(1,2),F(1)]:assert skill*luck<=luck
assert F(1,2)<F(2,3)
assert len(set(len(x.replace('-','')) for x in ['tse-nill','wol-la-chee','be-la-sana']))>1
r.write(b/'source-key-model-checks.json',dict(status='PASS',count=10,checks=checks,wealthCountermodels=wealthModels,probabilityBound='For every 0<=pSkill<=1, pSkill*pLuck<=pLuck. Option5 is contextual completion, not a necessary premise for the upper bound.',cropFraction='1/2<2/3 at fixed total land.',codeLength='Alternative encodings of A differ in length, including after hyphens removed.',readingScope='Exam passage comparisons only, not external agronomy or current law advice.',limitations='Same-author source/option review and formalization, not independent review.'))
print('PASS10 original/native/key/own and conditional/probability/encoding models')
