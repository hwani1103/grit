import collections,re,pdfplumber
import review_remaining605 as r
out=r.OUT/'final';out.mkdir(exist_ok=True);bank=r.bank();assert len(bank)==900
fixed={q['id']:n for n in range(1,62) for q in r.batch(n)};assert len(fixed)==605
ratings=[];frozen=[]
for n in range(1,62):
 b=r.folder(n);assert r.read(b/'batch-verification.json')['status']=='verified'
 own=r.read(b/'own-solves.json');assert {x['id'] for x in own}=={i for i,k in fixed.items() if k==n}
 assert r.sha(b/'own-solves.json')==r.read(b/'solve-frozen-before-reveal.json')['solveFileSha256']
 rows=r.read(b/'ratings-before.json')['ratings'];assert {x['id'] for x in rows}=={x['id'] for x in own};ratings+=rows
 frozen.append(dict(batch=n,ownSha256=r.sha(b/'own-solves.json'),ratingsSha256=r.sha(b/'ratings-before.json'),proofSha256=r.sha(b/'batch-verification.json')))
for n in range(62,70):assert r.read(r.folder(n)/'cross-verification.json')['status']=='verified'
assert len(ratings)==605
prior=r.read(r.PREP/'previously-scored295.json')['questions'];assert len(prior)==295 and not(set(fixed)&{q['id'] for q in prior}) and set(fixed)|{q['id'] for q in prior}==set(bank)
ledger=r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/current900-evidence-ledger.json')['questions'];keycache={};rows=[];sources=set()
subjectnames={'언어논리':['言語論理','言語論理','언어논리'],'상황판단':['狀況判斷','상황판단'],'자료해석':['資料解釋','자료해석']}
for row in ledger:
 q=bank[row['id']]
 for field in ['officialSource','officialKey']:
  pair=(row[field],row[field+'Sha256'])
  if pair not in sources:assert r.sha(r.ROOT/pair[0])==pair[1];sources.add(pair)
 k=(row['officialKey'],q['subject'])
 if k not in keycache:
  with pdfplumber.open(r.ROOT/k[0]) as pdf:text=next(p.extract_text() for p in pdf.pages if any('영역 '+s in (p.extract_text() or '') for s in subjectnames[k[1]]))
  answers={}
  for line in text.splitlines():
   if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):v=list(map(int,line.split()));answers.update(zip(v[::2],v[1::2]))
  keycache[k]=(text,answers)
 text,answers=keycache[k];assert q.get('examDate',q['source'])[:4] in text and f"책형 {q['book']}" in text.replace('㉮','가').replace('㉯','나')
 assert q['answer']==answers[q['number']]==row['officialAnswer'],q['id']
 assert len(q['choices'])==len(q['steps'])==len(q['optionReasons'])==5
 for a in [q['original']]+[x['asset'] for x in q.get('figures',[])]:assert (r.ROOT/a).is_file()
 rows.append(dict(id=q['id'],revision=q['revision'],questionSha256=r.digest(q),officialSource=row['officialSource'],officialKey=row['officialKey'],officialAnswer=q['answer'],individual605Batch=fixed.get(q['id'])))
sets=r.read(r.ROOT/'assets/psat/sets.json')['sets'];ids=[i for s in sets for i in s['questionIds']];assert len(sets)==90 and len(ids)==len(set(ids))==900 and set(ids)==set(bank)
assert collections.Counter(q['subject'] for q in bank.values())=={'언어논리':300,'상황판단':300,'자료해석':300}
stats={s:dict(count=len(v:=[x['scoreBeforeFix'] for x in ratings if bank[x['id']]['subject']==s]),total=sum(v),mean=sum(v)/len(v)) for s in subjectnames}
r.write(out/'ratings-summary.json',dict(count=605,total=sum(x['scoreBeforeFix'] for x in ratings),mean=sum(x['scoreBeforeFix'] for x in ratings)/605,distribution=dict(collections.Counter(x['scoreBeforeFix'] for x in ratings)),bySubject=stats,initialScoresNotRerated=True,frozenEvidence=frozen))
r.write(out/'current900-evidence-ledger.json',dict(status='PASS',checkedAt=r.now(),count=900,sets=90,sourceAndKeyFiles=len(sources),officialKeysFreshlyParsed=True,questions=rows,method='900 source/key hashes and exact book/date/number/final-answer matching;605 immutable individual proofs and295 prior history with targeted cross-reviews. Original assets preserved by preservation-check; not900freshblindsolves.'))
print('PASS:605 frozen solves/ratings,295 disjoint history,900 original keys,90 Sets;',len(sources),'source/key files; mean',sum(x['scoreBeforeFix'] for x in ratings)/605)
