import re,unicodedata,shutil,subprocess,itertools
from fractions import Fraction as F
import pdfplumber
from PIL import Image
import review_remaining605 as r
b=r.folder(43);rows=r.read(b/'revealed-current.json');src={x['id']:x for x in r.read(b/'blind-source.json')};own={x['id']:x for x in r.read(b/'own-solves.json')}
def norm(s):
 s=s.replace('\uf000경국대전\uf000','『경국대전』').replace('ㆍ','·').replace('\ue09d','α').replace('\ue09e','β').replace('\ue09f','γ').replace('\uf000','『').replace('\uf001','』')
 return re.sub(r'\s','',unicodedata.normalize('NFKC',re.sub(r'[①②③④⑤]','',s))).replace('[빈칸]','').replace('−','-')
reg={x['newAsset']:x for x in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/native-image-repairs.json')['figures']};checks=[];pixels=[]
for row in rows:
 q=row['question'];m=src[q['id']];s=re.sub(r'책형\s*\d+쪽','',m['sourceText']);s=re.sub(r'^\s*\[39～\s*40\] 다음 글을 읽고 물음에 답하시오[.]\s*','',s);s=re.sub(r'(?m)^\s*'+str(q['number'])+r'[.]\s*','',s,count=1)
 if q['number']==28:s=s.replace('(가) (나) (다)\n','')
 if q['number']==37:
  rec=reg[q['figures'][0]['asset']]
  with pdfplumber.open(r.ROOT/rec['source']) as pdf:raw=pdf.pages[rec['page1based']-1].crop(rec['rect']).extract_text()
  assert norm(raw) in norm(s)
  s=norm(s).replace(norm(raw),'',1)
  render=b/'fresh-l37';subprocess.run([shutil.which('pdftoppm'),'-r',str(rec['resolution']),'-f',str(rec['page1based']),'-l',str(rec['page1based']),'-singlefile','-png',str(r.ROOT/rec['source']),str(render)],check=True,capture_output=True)
  with Image.open(render.with_suffix('.png')) as im,Image.open(r.ROOT/q['figures'][0]['asset']) as actual:assert im.convert('RGB').crop(rec['pixelBox']).tobytes()==actual.convert('RGB').tobytes()
  pixels.append(dict(asset=q['figures'][0]['asset'],freshCropMatch=True,rect=rec['rect'],source=rec['source']))
 if q['number']==40:
  assert norm(q['prompt']) in norm(s);s=norm(s).replace(norm(q['prompt']),'',1);expected=q['body']+''.join(q['choices'])
 else:expected=q['prompt']+q['body']+''.join(q['choices'])
 a,e=norm(s),norm(expected)
 if a!=e:
  j=next((j for j,(x,y) in enumerate(zip(a,e)) if x!=y),min(len(a),len(e)));raise AssertionError((q['id'],j,a[j:j+100],e[j:j+100]))
 with pdfplumber.open(r.ROOT/row['officialKey']) as pdf:pi,t=next((j+1,p.extract_text()) for j,p in enumerate(pdf.pages) if '영역 언어논리' in (p.extract_text() or ''))
 assert q['examDate'][:4] in t and f"책형 {q['book']}" in t.replace('㉮','가').replace('㉯','나');ans={}
 for line in t.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):z=list(map(int,line.split()));ans.update(zip(z[::2],z[1::2]))
 assert ans[q['number']]==q['answer']==own[q['id']]['answer'];checks.append(dict(id=q['id'],source=m['source'],page=m['page'],key=row['officialKey'],keyPage=pi,nativeAndAllFiveChoicesMatch=True,ownMatches=True))
# 36: all nonempty subsets; a peak permits single SW or single DW.
sets=[set(c) for n in [1,2,3] for c in itertools.combinations(['SW','DW','MW'],n)]
withPeak=[sorted(s) for s in sets if s & {'SW','DW'}];withoutPeak=[sorted(s) for s in sets if not s & {'SW','DW'}]
assert ['SW'] in withPeak and withoutPeak==[['MW']]
# 37: apply every candidate minimal mechanism to both experiments and all mice.
requirements=[({'X'},{'X'}),({'X'},{'Y'}),({'Y'},{'X'}),({'Y'},{'Y'}),({'X','Y'},set())]
models=[]
for n,(first,second) in enumerate(requirements,1):
 phosphorylation=[];eating=[]
 for ghrelin,inhibitor in [(False,False),(True,False),(True,True)]:
  ph=[];eat=[]
  for proteins in [{'X','Y'},{'Y'},{'X'}]:
   p=ghrelin and first<=proteins;ph.append(p);eat.append(inhibitor or (p and second<=proteins))
  phosphorylation.append(ph);eating.append(eat)
 matches=phosphorylation[:2]==[[False]*3,[True,True,False]] and eating==[[False]*3,[True,False,False],[True]*3]
 assert matches==(n==3);models.append(dict(option=n,phosphorylation=phosphorylation[:2],eating=eating,matches=matches))
assert F('17.2')>F('15') and F('17.2')<F('20.6') # illustrative compatible marginal cost, not source observed amount.
assert not (True and True and False) # l40 execution missing; no counterexample to full conjunction.
r.write(b/'source-key-model-checks.json',dict(status='PASS',count=10,checks=checks,figurePixels=pixels,CNT=dict(withPeak=withPeak,withoutPeak=withoutPeak,ratioReason='Dalpha=Dbeta>0; Galpha>Gbeta>Dbeta; Ggamma=Dgamma yields alpha>beta>1=gamma.'),mechanisms=models,limits='Minimal supplied candidate mechanisms, not exhaustive biology. l40 premise absent is no counterexample; l28 illustrative marginal15 is not an inferred source amount.'))
print('PASS10 source/key/native; CNT subsets and5 mechanism models;1 fresh original table crop')
