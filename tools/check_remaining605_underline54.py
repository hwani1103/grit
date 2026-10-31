import re,pdfplumber
import review_remaining605 as r
b=r.folder(54);src=r.read(b/'blind-source.json')+r.read(b/'related295-source.json');bank=r.bank()
configs={
'kr-mpm-2024-03-02-psat-d-33':[
[(531.688,416,710),(550.394,400,710),(569.100,400,450)],
[(569.100,487,710),(587.807,400,710),(606.513,400,450)],
[(643.925,416,710),(662.632,400,465)],
[(700.044,416,710),(718.750,400,525)]],
'kr-mpm-2023-03-04-psat-d-02':[
[(623.540,503,710),(642.726,400,615)],
[(642.726,628,710),(661.912,400,710),(681.098,400,465)],
[(719.470,463,710),(738.655,400,710)],
[(777.027,615,710),(796.213,400,710),(815.399,400,525)]],
'kr-mpm-2026-03-07-psat-d-32':[
[(468.974,509,710),(487.680,430,670)],
[(543.799,446,710),(562.505,430,640)],
[(674.743,568,710),(693.449,430,710),(712.155,430,595)]]}
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
   expected=re.sub(r'^[㉠-㉣]\s*','',old);assert norm(text)==norm(expected),(i,text,expected);ranges.append(expected)
 checks.append(dict(id=i,source=m['source'],page=m['page'],sourceRanges=ranges,strokes=geometry,terminalPeriodsIncluded=True,labelsExcluded=True,changeRequired=not bank[i].get('underlineLabelAnchors',False)))
r.write(b/'underline-source-strokes.json',dict(status='PASS',checks=checks,method='Each original horizontal PDF stroke and visible character midpoint; these three originals include terminal dots, unlike the batch52 examples. No blanket punctuation removal.'))
print('PASS original11 underline ranges, terminal dots INCLUDED; labels excluded')
