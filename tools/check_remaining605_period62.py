import re,pdfplumber
import review_remaining605 as r
b=r.folder(62);src={x['id']:x for x in r.read(b/'source.json')};checks=[]
for q in r.read(b/'before.json')[:6]:
 m=src[q['id']];ranges=[]
 with pdfplumber.open(r.ROOT/m['source']) as pdf:
  p=pdf.pages[m['page']-1]
  bounds={'2024-07-27':(393,90,710,270),'2023-07-22':(39,400,356,570),'2021-07-10':(332,400,579,716) if q['number']==2 else (43,480,290,775),'2025-03-08':(393,450,710,685) if q['number']==5 else (393,315,710,537)}[q['examDate']]
  region=p.crop(bounds)
  for phrase in q['underlines']:
   if not phrase.endswith('.'):continue
   tail=re.sub(r'\s','',phrase[-22:]);pattern=r'\s*'.join(re.escape(c) for c in tail)
   hits=region.search(pattern);assert len(hits)==1,(q['id'],phrase,hits)
   c=hits[0]['chars'][-1];assert c['text']=='.'
   ls=[l for l in p.edges if l['height']<.01 and l['width']>8 and c['bottom']-.6<=l['top']<=c['bottom']+3 and l['x0']-.2<=(c['x0']+c['x1'])/2<=l['x1']+.2]
   assert ls,(q['id'],phrase,c)
   ranges.append(dict(phrase=phrase,terminalPeriodIncluded=True,periodBox=[c[k] for k in ['x0','top','x1','bottom']],sourceStrokes=[{k:l[k] for k in ['x0','x1','top']} for l in ls]))
 checks.append(dict(id=q['id'],source=m['source'],page=m['page'],terminalRanges=ranges,changeRequired=False,labelAnchorsAlreadyHandled=q.get('underlineLabelAnchors',False)))
assert sum(len(x['terminalRanges']) for x in checks)==20
r.write(b/'terminal-period-check.json',dict(status='PASS',checks=checks,method='Each existing terminal period checked against original PDF horizontal stroke; six full original pages inspected. All20 periods are covered, so retain them.'))
print('20 source terminal periods correctly included; no changes')
