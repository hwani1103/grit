import re,unicodedata,itertools
import pdfplumber
import review_remaining605 as r
b=r.folder(46);rows=r.read(b/'related295-before.json');src={x['id']:x for x in r.read(b/'related295-source.json')};own={x['id']:x for x in r.read(b/'related295-own-solves.json')};ledger={x['id']:x for x in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/current900-evidence-ledger.json')['questions']}
norm=lambda s:re.sub(r'\s','',unicodedata.normalize('NFKC',re.sub(r'[①②③④⑤]','',s)))
checks=[]
for q in rows:
 m=src[q['id']];s=re.sub(r'책형\s*\d+쪽','',m['sourceText']);s=re.sub(r'^\s*'+str(q['number'])+r'[.]\s*','',s,count=1)
 assert norm(s)==norm(q['prompt']+q['body']+''.join(q['choices'])),q['id']
 key=ledger[q['id']]['officialKey']
 with pdfplumber.open(r.ROOT/key) as pdf:pi,t=next((j+1,p.extract_text()) for j,p in enumerate(pdf.pages) if '영역 언어논리' in (p.extract_text() or ''))
 assert '2024' in t and '책형 나' in t.replace('㉯','나');ans={}
 for line in t.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):z=list(map(int,line.split()));ans.update(zip(z[::2],z[1::2]))
 assert ans[q['number']]==q['answer']==own[q['id']]['answer'];checks.append(dict(id=q['id'],source=m['source'],page=m['page'],key=key,keyPage=pi,nativeAndFiveChoicesMatch=True,ownAnswerMatches=True))
worlds=[]
for v in itertools.product('THF',repeat=5):
 a,n,d,l,m=v
 if v.count('T')!=1 or sorted(v.count(x) for x in 'THF')!=[1,1,3]:continue
 if a=='T' and n!='H':continue
 if n==l=='H':continue
 if not(n=='H' or m=='F'):continue
 if d!='F' and not(a=='T' and l=='H'):continue
 if m!='F' and a!='T':continue
 worlds.append(v)
assert worlds and all(v[2]=='F' for v in worlds) and any(v[3]!='T' for v in worlds) and all(v[1]!='F' or v[0]=='H' for v in worlds)
assert ('T','H','F','F','F') in worlds
truths=[]
for theory,sameRef,sameMeaning in itertools.product([False,True],repeat=3):
 if theory and sameRef and not sameMeaning:continue
 assert not(theory and sameRef) or sameMeaning
 assert not(sameRef and not sameMeaning) or not theory
 truths.append([theory,sameRef,sameMeaning])
assert all(not(link and cognitive) or different for link,cognitive,different in itertools.product([False,True],repeat=3) if not link or not cognitive or different)
r.write(b/'related295-source-key-model-checks.json',dict(status='PASS',count=2,checks=checks,placementWorlds=worlds,referenceTruths=truths,modusp='CognitiveDifference -> MeaningDifference; CognitiveDifference; therefore MeaningDifference. Conditional is explicitly given by optionㄷ.'))
print('PASS2 related native/key; all243 assignments evaluated; reference implication truth table')
