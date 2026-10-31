import re,unicodedata,itertools,pdfplumber
from fractions import Fraction as F
import review_remaining605 as r
b=r.folder(49);rows=r.read(b/'revealed-current.json');src={x['id']:x for x in r.read(b/'blind-source.json')};own={x['id']:x for x in r.read(b/'own-solves.json')}
def norm(s):
 s=s.replace('\uf000경국대전\uf000','『경국대전』').replace('ㆍ','·')
 return re.sub(r'\s','',unicodedata.normalize('NFKC',re.sub(r'[①②③④⑤]','',s))).replace('「','').replace('」','')
checks=[]
for row in rows:
 q=row['question'];m=src[q['id']];s=re.sub(r'책형\s*\d+쪽','',m['sourceText']);s=re.sub(r'^\s*\[19～20\] 다음 글을 읽고 물음에 답하시오[.]\s*','',s);s=re.sub(r'(?m)^\s*'+str(q['number'])+r'[.]\s*','',s,count=1)
 if q['number'] in [19,20]:
  assert norm(s).count(norm(q['prompt']))==1;s=norm(s).replace(norm(q['prompt']),'',1);expected=q['body']+''.join(q['choices'])
 else:expected=q['prompt']+q['body']+''.join(q['choices'])
 a,e=norm(s),norm(expected)
 if a!=e:
  j=next((j for j,(x,y) in enumerate(zip(a,e)) if x!=y),min(len(a),len(e)));raise AssertionError((q['id'],j,a[j:j+100],e[j:j+100]))
 with pdfplumber.open(r.ROOT/row['officialKey']) as pdf:pi,t=next((j+1,p.extract_text()) for j,p in enumerate(pdf.pages) if '영역 언어논리' in (p.extract_text() or ''))
 assert '2024' in t and '책형 나' in t.replace('㉯','나');ans={}
 for line in t.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):z=list(map(int,line.split()));ans.update(zip(z[::2],z[1::2]))
 assert ans[q['number']]==q['answer']==own[q['id']]['answer'];checks.append(dict(id=q['id'],source=m['source'],page=m['page'],key=row['officialKey'],keyPage=pi,nativeAndAllFiveChoicesMatch=True,ownMatches=True))
assert sum(x*y for x,y in zip([2,2,-1],[F(1,10),F(1,10),F(8,10)]))==F(-2,5)
assert sum(x*y for x,y in zip([10,10,-1],[F(1,100),F(1,100),F(98,100)]))==F(-78,100)
positiveExamples=[]
for changes in itertools.product([0,1,2],repeat=3):
 if not any(changes):continue
 for w in [(F(1,3),)*3,(F(1,100),F(1,100),F(98,100))]:
  assert sum(w)==1 and min(w)>0 and sum(x*y for x,y in zip(changes,w))>0;positiveExamples.append([changes,list(map(str,w))])
triples=[set(x) for x in itertools.combinations('ABCD',3)];assert len(triples)==4 and not set.intersection(*triples)
scale=[list(range(n)) for n in range(5)];assert len(scale)==5 and scale[3]==[0,1,2]
worlds=[(a,c,p) for a,c,p in itertools.product([False,True],repeat=3) if not a or c]
assert (True,True,False) in worlds and (True,True,True) in worlds
# Option4 adds notP->notC, equivalent C->P, removing counterexample.
with4=[v for v in worlds if v[2] or not v[1]];assert all(not a or p for a,c,p in with4)
r.write(b/'source-key-model-checks.json',dict(status='PASS',count=10,checks=checks,weightedCounterexamples=['+2,+2,-1 with .1,.1,.8 -> -.4','+10,+10,-1 with .01,.01,.98 -> -.78'],strictPositiveProof='Each xi>=0, some xi>0, every wi>0 -> each product>=0 and some>0 ->sum>0. Sumweights1 is normalization, not enough alone.',weightedBoundaryExamples=len(positiveExamples),index3Combinations=list(map(sorted,triples)),index3CertainActions=[],scaleStates=scale,activationWorlds=worlds,option4Worlds=with4,sharedPassage1920=True,historicalKeyExposureCount=10,limitations='Same-author source re-solving with historical key exposure; no claim of blind or independent review.'))
print('PASS10 source/key/native; weighted counterexamples/general proof;scale5types;activation truth table')
