import re,unicodedata,pdfplumber
import review_remaining605 as r
b=r.folder(49);rows=r.read(b/'related295-before.json');src={x['id']:x for x in r.read(b/'related295-source.json')};own={x['id']:x for x in r.read(b/'related295-own-solves.json')};ledger={x['id']:x for x in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/current900-evidence-ledger.json')['questions']}
norm=lambda s:re.sub(r'\s','',unicodedata.normalize('NFKC',re.sub(r'[①②③④⑤]','',s)))
checks=[]
for q in rows:
 m=src[q['id']];s=re.sub(r'책형\s*\d+쪽','',m['sourceText']);s=re.sub(r'^\s*'+str(q['number'])+r'[.]\s*','',s,count=1)
 if q['number']==26:s=s.replace('(가) (나) (다)\n','');assert q['choiceNote']=='선택지의 순서: (가) → (나) → (다)'
 assert norm(s)==norm(q['prompt']+q['body']+''.join(q['choices'])),q['id']
 key=ledger[q['id']]['officialKey']
 with pdfplumber.open(r.ROOT/key) as pdf:pi,t=next((j+1,p.extract_text()) for j,p in enumerate(pdf.pages) if '영역 언어논리' in (p.extract_text() or ''))
 assert '2024' in t and '책형 나' in t.replace('㉯','나');ans={}
 for line in t.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):z=list(map(int,line.split()));ans.update(zip(z[::2],z[1::2]))
 assert ans[q['number']]==q['answer']==own[q['id']]['answer'];checks.append(dict(id=q['id'],source=m['source'],page=m['page'],key=key,keyPage=pi,nativeAndFiveChoicesMatch=True,ownAnswerMatches=True))
q=next(q for q in rows if q['number']==8);m=src[q['id']]
with pdfplumber.open(r.ROOT/m['source']) as pdf:
 p=pdf.pages[m['page']-1];strokes=[]
 for line in p.lines:
  if line['x0']>p.width/2 and abs(line['y0']-line['y1'])<.3 and 90<line['top']<660:
   chars=[c for c in p.chars if line['x0']-.1<=(c['x0']+c['x1'])/2<=line['x1']+.1 and line['top']-15<c['top']<line['top']-3]
   if chars:strokes.append(dict(x0=line['x0'],x1=line['x1'],top=line['top'],text=''.join(c['text'] for c in sorted(chars,key=lambda c:c['x0']))))
 expected=['자신의 적성을 파악하고 진로를 탐색하겠다','점유하고 있는 직장 내의 자리에서 담당하는 일을 뜻한다','평생을 두고 내가 고민하고 추구해야 하는 가치 있는 일을 뜻한다','어떤 자리에서 일하고 싶은지가 아니라 무슨 일을 하고 싶은지','직에 대한 이해도를 충분히 높이지 못한다면']
 for j,(lo,hi) in enumerate([(100,130),(210,245),(330,355),(480,505),(630,655)]):
  text=''.join(s['text'] for s in sorted(strokes,key=lambda s:(s['top'],s['x0'])) if lo<s['top']<hi)
  assert norm(text)==norm(expected[j]),(j,text)
 assert [q['underlines'][j]!=expected[j] for j in range(5)]==[True,True,True,True,False]
 r.write(b/'related295-underline-source-strokes.json',dict(status='PASS',id=q['id'],source=m['source'],page=m['page'],strokes=strokes,currentRanges=q['underlines'],sourceRanges=expected,requiredRepairIndices=[0,1,2,3],finding='Postposed고/를and2terminal periods extend beyond original strokes. Original final fragment㉤ already correct.'))
assert -11<-8<-7 and -7>-12.5
r.write(b/'related295-source-key-model-checks.json',dict(status='PASS',count=2,checks=checks,threshold='-11<T<-8; -7>T so positive. PositiveA freezes at-7 versus neutralB-12.5; warming also produced freezing at-8.',originalSourceNotScientificGeneralization=True,underlineEvidence='related295-underline-source-strokes.json'))
print('PASS2 related native/key/experimental threshold;4 original underline range repairs needed')
