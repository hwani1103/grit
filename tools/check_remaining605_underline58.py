import re,pdfplumber
import review_remaining605 as r
b=r.folder(58);src=r.read(b/'blind-source.json')+r.read(b/'related295-source.json');bank=r.bank()
shared=[[(244.260,140,345),(262.966,65,345),(281.672,65,345),(300.379,65,122)],[(375.203,148,345),(393.910,65,161)],[(468.734,150,345),(487.441,65,345),(506.147,65,158)],[(585.888,115,345),(604.594,49,80)]]
configs={'kr-mpm-2023-03-04-psat-l-31':[[(610.350,98,293)]],'kr-mpm-2023-03-04-psat-l-32':[[(360.934,576,699),(380.120,403,699)]],'kr-mpm-2023-07-22-psat-l-21':[[(917.324,296,350),(936.510,50,110)]],'kr-mpm-2024-07-27-psat-l-19':shared,'kr-mpm-2024-07-27-psat-l-20':shared}
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
    text+=''.join(c['text'] for c in sorted(chars,key=lambda c:c['x0']));geometry += [{k:l[k] for k in ['x0','x1','top']} for l in ls]
   expected=re.sub(r'^[㉠-㉤]\s*','',old)
   if '2023-03-04' not in i:expected=expected.removesuffix('.')
   assert norm(text)==norm(expected),(i,text,expected);ranges.append(expected)
 checks.append(dict(id=i,source=m['source'],page=m['page'],sourceRanges=ranges,strokes=geometry,terminalPeriodsIncluded='2023-03-04' in i,labelsExcluded=True,changeRequired=ranges!=bank[i]['underlines']))
r.write(b/'underline-source-strokes.json',dict(status='PASS',checks=checks,method='Original PDF underline stroke geometry and character midpoints, independently per range. March31/32 include terminal dots; July source ranges exclude dots and labels.'))
print('11 ranges verified from original underline strokes')
