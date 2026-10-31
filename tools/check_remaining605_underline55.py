import re,pdfplumber
import review_remaining605 as r
b=r.folder(55);src=r.read(b/'blind-source.json')+r.read(b/'related295-source.json');bank=r.bank()
configs={
'kr-mpm-2023-03-04-psat-l-10':[
[(149.890,417,710),(169.075,400,470)],
[(245.819,639,710),(265.005,400,700)],
[(380.120,417,710),(399.306,400,530)],
[(495.235,676,710),(514.421,400,660)],
[(629.536,604,710),(648.722,400,660)]],
'kr-mpm-2023-07-22-psat-l-22':[
[(917.324,296,350),(936.510,50,110)]]}
norm=lambda s:re.sub(r'\s','',s)
checks=[]
for i,groups in configs.items():
 m=next(x for x in src if x['id']==i);ranges=[];geometry=[]
 with pdfplumber.open(r.ROOT/m['source']) as pdf:
  p=pdf.pages[m['page']-1]
  for group,old in zip(groups,bank[i]['underlines']):
   text=''
   for y,left,right in group:
    ls=[l for l in p.lines if abs(l['top']-y)<.002 and l['height']<.01 and left<=l['x0'] and l['x1']<=right];assert ls
    chars=[c for c in p.chars if y-15<c['top']<y and any(l['x0']-.2<=(c['x0']+c['x1'])/2<=l['x1']+.2 for l in ls)]
    text+=''.join(c['text'] for c in sorted(chars,key=lambda c:c['x0']))
    geometry += [{k:l[k] for k in ['x0','x1','top']} for l in ls]
   expected=re.sub(r'^[㉠-㉤]\s*','',old).removesuffix('.');assert norm(text)==norm(expected),(i,text,expected);ranges.append(expected)
 checks.append(dict(id=i,source=m['source'],page=m['page'],sourceRanges=ranges,strokes=geometry,terminalPeriodsIncluded=False,labelsExcluded=True,changeRequired=True))
r.write(b/'underline-source-strokes.json',dict(status='PASS',checks=checks,method='Each original horizontal PDF stroke and visible character midpoint; these source strokes exclude labels and terminal periods; compare individually, unlike batch54.'))
print('PASS original6 underline ranges, terminal dots and labels excluded')
