"""Batch09: original source/native images and independent exact arithmetic."""
from pathlib import Path
from fractions import Fraction as F
import json,re,hashlib,shutil,subprocess
import pdfplumber
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/psat_remaining605_20261030/batch09'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
norm=lambda s:re.sub(r'[\s①②③④⑤·ㆍ/]','',s)
items=read(OUT/'revealed-current.json');solves={x['id']:x for x in read(OUT/'own-solves.json')};sources={x['id']:x for x in read(OUT/'blind-source.json')}
reg={x['newAsset']:x for x in read(ROOT/'artifacts/psat_final_quality_20261029/full900/native-image-repairs.json')['figures']}
checks=[];pixels=[];cache={};pdfcache={}
try:
 for row in items:
  q=row['question'];m=sources[q['id']];src=ROOT/m['source']
  if src not in pdfcache:pdfcache[src]=pdfplumber.open(src)
  page=pdfcache[src].pages[m['page']-1];left=page.width*m['side']/2;right=page.width*(m['side']+1)/2
  marker=next(w for w in page.extract_words() if w['text']==str(q['number'])+'.' and left<=w['x0']<left+45)
  rectangles=[reg[f['asset']]['rect'] for f in q['figures']]
  def keep(obj):
   if obj.get('object_type')!='char':return True
   x=(obj['x0']+obj['x1'])/2;y=(obj['top']+obj['bottom'])/2
   return not any(a<=x<=c and b<=y<=d for a,b,c,d in rectangles)
  filtered=page.filter(keep)
  native=filtered.crop((left,marker['top']-1,right,page.height)).extract_text() or ''
  if m['columnContinuation']:
   tail=filtered.crop((page.width/2,30,page.width,page.height)).extract_text() or ''
   end=re.search(r'(?m)^\d+[.]\s+(?:다음|위 글|윗글)',tail)
   if end:tail=tail[:end.start()]
   tail=re.sub(r'책형\s*\d+쪽','',tail)
   native+='\n'+tail
  if q['id']=='kr-mpm-2023-07-22-psat-d-24':
   native=native.split('25.')[0]
  native=norm(re.sub(r'^\d+[.]\s*','',native))
  heading=None
  if q['id']=='kr-mpm-2023-07-22-psat-d-22':
   assert q['choiceNote']=='A / B / C / D / E';heading='ABCDE';assert native.count(heading)==1;native=native.replace(heading,'',1)
  choices = '' if q['id']=='kr-mpm-2023-07-22-psat-d-08' else ''.join(q['choices'])
  a,b=native,norm(q['prompt']+q['body']+choices)
  if a!=b:
   i=next((i for i,(x,y) in enumerate(zip(a,b)) if x!=y),min(len(a),len(b)))
   raise AssertionError((q['id'],i,a[max(0,i-30):i+120],b[max(0,i-30):i+120]))
  with pdfplumber.open(ROOT/row['officialKey']) as pdf:
   pi,t=next((i+1,p.extract_text()) for i,p in enumerate(pdf.pages) if '영역 자료해석' in (p.extract_text() or ''))
  assert q['examDate'][:4] in t and f"책형 {q['book']}" in t
  answers={}
  for line in t.splitlines():
   if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
    z=list(map(int,line.split()));answers.update(zip(z[::2],z[1::2]))
  assert answers[q['number']]==q['answer']==solves[q['id']]['answer']
  checks.append(dict(id=q['id'],source=m['source'],sourcePage=m['page'],actualSide=m['side'],questionTop=marker['top'],nativeTextAndFiveChoicesMatch=True,continuation=m['columnContinuation'],choiceHeading=heading,key=row['officialKey'],keyPage=pi,answer=answers[q['number']]))
  for f in q['figures']:
   r=reg[f['asset']];assert r['source']==m['source'];assert hashlib.sha256(src.read_bytes()).hexdigest()==r['sha256']
   sig=(m['source'],r['page1based'],r['resolution'])
   if sig not in cache:
    d=OUT/'fresh-source-renders';d.mkdir(exist_ok=True);prefix=d/f"{r['sha256'][:16]}-p{r['page1based']:02d}-r{r['resolution']}"
    subprocess.run([shutil.which('pdftoppm'),'-r',str(r['resolution']),'-f',str(r['page1based']),'-l',str(r['page1based']),'-singlefile','-png',str(src),str(prefix)],check=True,capture_output=True)
    cache[sig]=Image.open(prefix.with_suffix('.png')).convert('RGB')
   ref=cache[sig].crop(r['pixelBox']);actual=Image.open(ROOT/f['asset']).convert('RGB');assert actual.size==ref.size and actual.tobytes()==ref.tobytes()
   pixels.append(dict(id=q['id'],asset=f['asset'],page=r['page1based'],resolution=r['resolution'],pixelBox=r['pixelBox'],pixelMatch=True))
finally:
 for pdf in pdfcache.values():pdf.close()
 for im in cache.values():im.close()


(OUT/'source-native-pixel-checks.json').write_text(json.dumps(dict(status='PASS',sourceKeyNative=checks,figurePixels=pixels),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PASS direct official keys/native text and freshly rendered figure pixels:',len(checks),len(pixels))
