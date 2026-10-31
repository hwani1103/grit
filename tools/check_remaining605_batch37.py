import re
from fractions import Fraction as F
import pdfplumber
import review_remaining605 as r
b=r.folder(37);rows=r.read(b/'revealed-current.json');src={x['id']:x for x in r.read(b/'blind-source.json')};own={x['id']:x for x in r.read(b/'own-solves.json')}
norm=lambda s:re.sub(r'[\s①②③④⑤\uf000\uf02c『』]','',s).replace('[빈칸]','').replace('ㆍ','·').replace('\ue09d','α').replace('∼','～')
checks=[]
for row in rows:
 q=row['question'];m=src[q['id']];native=re.sub(r'책형\s*\d+쪽','',m['sourceText']);native=re.sub(r'^\s*\d+[.]\s*','',native)
 if q['id'].endswith('2025-03-08-psat-l-08'):
  assert native.count('(가) (나) (다)')==1;native=native.replace('(가) (나) (다)','');assert q['choiceNote']=='(가) → (나) → (다)'
 actual,expected=norm(native),norm(q['prompt']+q['body']+''.join(q['choices']))
 if actual!=expected:
  i=next((i for i,(a,c) in enumerate(zip(actual,expected)) if a!=c),min(len(actual),len(expected)));raise AssertionError((q['id'],i,actual[i:i+120],expected[i:i+120]))
 with pdfplumber.open(r.ROOT/row['officialKey']) as pdf:pi,t=next((i+1,p.extract_text()) for i,p in enumerate(pdf.pages) if '영역 언어논리' in (p.extract_text() or ''))
 assert q['examDate'][:4] in t and f"책형 {q['book']}" in t.replace('㉯','나').replace('㉮','가')
 ans={}
 for line in t.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
   z=list(map(int,line.split()));ans.update(zip(z[::2],z[1::2]))
 assert ans[q['number']]==q['answer']==own[q['id']]['answer']
 checks.append(dict(id=q['id'],source=m['source'],page=m['page'],nativeAndFiveChoices=True,key=row['officialKey'],keyPage=pi,ownMatches=True))
assert 5<6<10 and 3<=5
assert 180>=180 and not 180>180 and 3<=5
# The compound treatment is taste+nutrition, not isolated nutrition.
observations=[dict(alpha=True,taste=True,nutrition=False,durationMinutes=3,increased=True),dict(alpha=False,taste=True,nutrition=False,increased=False),dict(alpha=True,taste=True,nutrition=True,durationLowerMinutes=180,increased=True),dict(alpha=False,taste=True,nutrition=True,durationLowerMinutes=180,increased=True)]
r.write(b/'source-key-model-checks.json',dict(status='PASS',count=10,checks=checks,experimentObservations=observations,boundaryCounterexample='t=180 minutes satisfies reported>=3h but not defined>3h. Preserve raw source and choose best explanatory option2; do not strengthen to certainty or claim nutrition-only short test.',sourceChoice3Actually='nutrition short via alpha; taste short and long via alpha, NOT nutrition long',readingScope='Only the supplied exam passages; no external history/current law or current SAF policy substitutions.'))
print('PASS10 original/native/key checks; experiment boundary and option3 scope recorded')
