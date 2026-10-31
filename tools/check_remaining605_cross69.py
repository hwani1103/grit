import re,pdfplumber,subprocess,shutil
from PIL import Image
import review_remaining605 as r
b=r.folder(69);src={x['id']:x for x in r.read(b/'source.json')};old=r.read(b/'before.json');reg={x['newAsset']:x for x in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/native-image-repairs.json')['figures']};ledger={x['id']:x for x in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/current900-evidence-ledger.json')['questions']}
index={q['id']:n for n in range(1,62) for q in r.batch(n)};checks=[];pixels=[]
for q in old:
 i=q['id'];own=next(x for x in r.read(b/'own-solves.json') if x['id']==i);assert own['answer']==q['answer'];assert r.sha(b/'own-solves.json')==r.read(b/'solve-frozen.json')['sha256']
 for f in q.get('figures',[]):
  v=reg[f['asset']];assert r.sha(r.ROOT/v['source'])==v['sha256'];dst=b/'fresh-source-renders'/f"{v['sha256'][:12]}-p{v['page1based']:02d}";dst.parent.mkdir(exist_ok=True)
  if not dst.with_suffix('.png').exists():subprocess.run([shutil.which('pdftoppm'),'-r',str(v['resolution']),'-f',str(v['page1based']),'-l',str(v['page1based']),'-singlefile','-png',str(r.ROOT/v['source']),str(dst)],check=True,capture_output=True)
  with Image.open(dst.with_suffix('.png')) as im,Image.open(r.ROOT/f['asset']) as a:
   c=im.convert('RGB').crop(v['pixelBox']);assert c.size==a.size and c.tobytes()==a.convert('RGB').tobytes()
  pixels.append(dict(id=i,asset=f['asset'],freshSourcePixelMatch=True))
 key=ledger[i]['officialKey']
 with pdfplumber.open(r.ROOT/key) as pdf:t=next(p.extract_text() for p in pdf.pages if any('영역 '+s in (p.extract_text() or '') for s in ['言語論理','言語論理','언어논리']))
 assert q['examDate'][:4] in t and f"책형 {q['book']}" in t.replace('㉮','가').replace('㉯','나');ans={}
 for line in t.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):v=list(map(int,line.split()));ans.update(zip(v[::2],v[1::2]))
 assert ans[q['number']]==q['answer'];checks.append(dict(id=i,ownSolve='own-solves.json',officialKey=key,answerStillMatches=True,sourceOnlyDisplayFollowup=True))
r.write(b/'source-key-checks.json',dict(status='PASS',checks=checks,figurePixels=pixels,method='All10 original-source calculations and five options recorded before current comparison; original key and fresh original graphics checked. Ten prior295; same-author review.'))
print('10 own-solves+official keys and',len(pixels),'fresh figure crops PASS')
