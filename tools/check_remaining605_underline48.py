import re,pdfplumber
import review_remaining605 as r
b=r.folder(48);q=next(q for q in r.read(b/'related295-before.json') if q['number']==11)
norm=lambda s:re.sub(r'\s','',s)
with pdfplumber.open(r.ROOT/'artifacts/psat600_20261028/sources/4440/pdf/자료해석(나).pdf') as pdf:
 page=pdf.pages[5];strokes=[]
 for line in page.lines:
  if line['x0']>page.width/2 and 130<line['top']<385 and abs(line['y0']-line['y1'])<.3:
   chars=[c for c in page.chars if line['x0']-1<=(c['x0']+c['x1'])/2<=line['x1']+1 and line['top']-15<c['top']<line['top']-3]
   text=''.join(c['text'] for c in sorted(chars,key=lambda c:c['x0']))
   strokes.append(dict(x0=line['x0'],x1=line['x1'],top=line['top'],text=text))
 # Join segments per statement; avoid duplicating chars at adjoining spans.
 ranges=[(130,170),(190,220),(230,254),(252,280),(340,385)]
 texts=[]
 for n,(lo,hi) in enumerate(ranges):
  selected=[s for s in strokes if lo<s['top']<hi and (n!=2 or s['top']<250 or s['x1']<570) and (n!=3 or s['top']>260 or s['x0']>570)]
  selected.sort(key=lambda s:(s['top'],s['x0']))
  chars=[]
  for c in page.chars:
   x=(c['x0']+c['x1'])/2
   if any(s['x0']-1<=x<=s['x1']+1 and s['top']-15<c['top']<s['top']-3 for s in selected):chars.append(c)
  chars.sort(key=lambda c:(min(s['top'] for s in selected if s['x0']-1<=(c['x0']+c['x1'])/2<=s['x1']+1 and s['top']-15<c['top']<s['top']-3),c['x0']))
  text=''.join(c['text'] for c in chars);texts.append(text)
  assert norm(text)==norm(q['underlines'][n]),(n,text,q['underlines'][n])
  assert text.endswith('.')
assert q['choices']==q['underlines']
r.write(b/'related295-underline-source-strokes.json',dict(status='PASS',id=q['id'],allFiveTerminalPeriodsIncludedInSourceStroke=True,unchanged=True,sourcePage=6,strokes=strokes,matchedStatements=texts,scope='This item only; other period candidates remain pending.'))
print('PASS all5 original underline ranges include terminal periods; no change')
