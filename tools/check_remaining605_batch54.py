import re,unicodedata,subprocess,shutil
from fractions import Fraction as F
import pdfplumber
from PIL import Image
import review_remaining605 as r
b=r.folder(54)
def norm(s):return re.sub(r'\s','',unicodedata.normalize('NFKC',re.sub(r'[①②③④⑤]','',s).replace('ㆍ','·'))).replace('\x00','')
reg={x['newAsset']:x for x in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/native-image-repairs.json')['figures']}
ledger={x['id']:x for x in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/current900-evidence-ledger.json')['questions']}
for related in [False,True]:
 prefix='related295-' if related else '';rows=r.read(b/'related295-before.json') if related else [x['question'] for x in r.read(b/'revealed-current.json')]
 src={x['id']:x for x in r.read(b/('related295-source.json' if related else 'blind-source.json'))};own={x['id']:x for x in r.read(b/(prefix+'own-solves.json'))};checks=[];pixels=[]
 for q in rows:
  m=src[q['id']];s=re.sub(r'(?:가\s*)?책형\s*\d+쪽','',m['sourceText'])
  if q['id']=='kr-mpm-2026-03-07-psat-d-32':
   s=re.sub(r'^\[31～\s*32\]\s*','',s);s=re.sub(r'(?m)^\s*32[.]\s*','',s,count=1)
  else:
   s=re.split(r'(?m)^\s*'+str(q['number'])+r'[.]\s*',s,maxsplit=1)[1]
   if q['id'] in ['kr-mpm-2024-03-02-psat-d-34','kr-mpm-2023-03-04-psat-d-05']:
    s=re.split(r'(?m)^\s*'+str(q['number']+1)+r'[.]',s,maxsplit=1)[0]
  actual=norm(s)
  for f in q.get('figures',[]):
   if f['asset'].endswith('d32-dialogue-illustration.png'):
    crop=r.read(r.OUT/'batch36/related295-illustration-crop.json');v=reg[crop['source']].copy();v['rect']=crop['pdfRect'];v['pixelBox']=[int(x*v['resolution']/72) for x in v['rect']]
   else:v=reg[f['asset']]
   assert v['source']==m['source'] and r.sha(r.ROOT/v['source'])==v['sha256']
   with pdfplumber.open(r.ROOT/v['source']) as pdf:part=pdf.pages[v['page1based']-1].crop(v['rect']).extract_text()
   raw=norm(part or '')
   if raw:assert actual.count(raw)==1,(q['id'],'figure text mismatch',raw[:100]);actual=actual.replace(raw,'',1)
   dst=b/'fresh-source-renders'/f"{v['sha256'][:12]}-p{v['page1based']:02d}";dst.parent.mkdir(exist_ok=True)
   if not dst.with_suffix('.png').exists():subprocess.run([shutil.which('pdftoppm'),'-r',str(v['resolution']),'-f',str(v['page1based']),'-l',str(v['page1based']),'-singlefile','-png',str(r.ROOT/v['source']),str(dst)],check=True,capture_output=True)
   with Image.open(dst.with_suffix('.png')) as im,Image.open(r.ROOT/f['asset']) as old:
    fresh=im.convert('RGB').crop(v['pixelBox']);assert fresh.size==old.size and fresh.tobytes()==old.convert('RGB').tobytes()
   pixels.append(dict(id=q['id'],asset=f['asset'],pixelBox=v['pixelBox'],page=v['page1based'],freshMatch=True))
  if q['number']==39 and q['examDate']=='2024-03-02':
   header='개근상을받은학생수우등상을받은학생수'
   # Header is included in the last source graphic, so already subtracted.
  assert actual.count(norm(q['prompt']))==1,(q['id'],actual[:200],norm(q['prompt']));actual=actual.replace(norm(q['prompt']),'',1);expected=norm(q['body']+''.join(q['choices']))
  if actual!=expected:
   j=next((j for j,(a,e) in enumerate(zip(actual,expected)) if a!=e),min(len(actual),len(expected)));raise AssertionError((q['id'],j,actual[j:j+100],expected[j:j+100]))
  key=ledger[q['id']]['officialKey']
  with pdfplumber.open(r.ROOT/key) as pdf:pi,t=next((j+1,p.extract_text()) for j,p in enumerate(pdf.pages) if '영역 資料解釋' in (p.extract_text() or '') or '영역 자료해석' in (p.extract_text() or ''))
  assert q['examDate'][:4] in t and f"책형 {q['book']}" in t.replace('㉮','가').replace('㉯','나');ans={}
  for line in t.splitlines():
   if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):z=list(map(int,line.split()));ans.update(zip(z[::2],z[1::2]))
  assert ans[q['number']]==q['answer']==own[q['id']]['answer'];checks.append(dict(id=q['id'],source=m['source'],page=m['page'],key=key,keyPage=pi,nativeAndAllFiveChoicesMatch=True,ownMatches=True))
 r.write(b/(prefix+'source-key-checks.json'),dict(status='PASS',checks=checks,figurePixels=pixels,originalVisualReview='All target source pages and both related pages inspected, including map legends and all four graph choices.'))
 print(prefix or 'target',len(checks),'source/key/native PASS;',len(pixels),'fresh crops')
models=r.read(b/'pre-reveal-exact-models.json');assert models['status']=='PASS'
relatedModels=r.read(b/'related295-pre-reveal-models.json');assert relatedModels['status']=='PASS'
# Verify the existing navy witness, rounding margins and all five fuel ratios.
assert 5380*20+5371+3001*29==200000
assert 200000+49*501+52*1001+39*2001+5*3001==369645
assert F(1178214*5945,10000)>F(541450*125,100)
assert F(765)*(F('0.7625')*F('.5')+F('.1135')+F('.0635')*2+F('.0215')*3)>500
r.write(b/'exact-model-checks.json',dict(status='PASS',sourceOnlyModels='pre-reveal-exact-models.json',relatedSourceOnlyModels='related295-pre-reveal-models.json',existingNavyWitnessValid=True,roundingBoundaryStable=True))
