import re,unicodedata,pdfplumber
import review_remaining605 as r
b=r.folder(58)
def norm(s):return re.sub(r'\s','',unicodedata.normalize('NFKC',re.sub(r'[①②③④⑤]','',s).replace('ㆍ','·')))
ledger={x['id']:x for x in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/current900-evidence-ledger.json')['questions']}
for related in [False,True]:
 prefix='related295-' if related else '';rows=r.read(b/'related295-before.json') if related else [x['question'] for x in r.read(b/'revealed-current.json')]
 src={x['id']:x for x in r.read(b/('related295-source.json' if related else 'blind-source.json'))};own={x['id']:x for x in r.read(b/(prefix+'own-solves.json'))};checks=[]
 for q in rows:
  m=src[q['id']];s=re.sub(r'(?:가\s*)?책형\s*\d+쪽','',m['sourceText']);s=re.sub(r'^\s*\[\d+[～~]\s*\d+\] 다음 글을 읽고 물음에 답하시오[.]\s*','',s);s=re.sub(r'(?m)^\s*(?:문\s*)?'+str(q['number'])+r'[.]\s*','',s,count=1)
  a=norm(s);assert a.count(norm(q['prompt']))==1;a=a.replace(norm(q['prompt']),'',1);e=norm(q['body']+''.join(q['choices']))
  if q['id'] in ['kr-mpm-2023-03-04-psat-l-19','kr-mpm-2023-03-04-psat-l-20']:assert q['body'].count('[빈칸]')==3;e=e.replace('[빈칸]','') # Three original blank boxes visually verified.
  if q['id']=='kr-mpm-2023-03-04-psat-l-28':assert q['body'].count('[빈칸]')==1;e=e.replace('[빈칸]','') # Original vector blank visually verified.
  if a!=e:
   j=next((j for j,(aa,ee) in enumerate(zip(a,e)) if aa!=ee),min(len(a),len(e)));raise AssertionError((q['id'],j,a[j:j+120],e[j:j+120]))
  key=ledger[q['id']]['officialKey']
  with pdfplumber.open(r.ROOT/key) as pdf:pi,t=next((j+1,p.extract_text()) for j,p in enumerate(pdf.pages) if '영역 언어논리' in (p.extract_text() or ''))
  assert q['examDate'][:4] in t and ('책형 '+q['book']) in t.replace('㉮','가').replace('㉯','나');ans={}
  for line in t.splitlines():
   if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):z=list(map(int,line.split()));ans.update(zip(z[::2],z[1::2]))
  assert ans[q['number']]==q['answer']==own[q['id']]['answer'];checks.append(dict(id=q['id'],source=m['source'],page=m['page'],key=key,keyPage=pi,nativeAndAllFiveChoicesMatch=True,ownMatches=True))
 r.write(b/(prefix+'source-key-checks.json'),dict(status='PASS',checks=checks));print(prefix or 'target',len(checks),'source/key/native PASS')
