import re,unicodedata,subprocess,shutil
from fractions import Fraction as F
import pdfplumber
from PIL import Image
import review_remaining605 as r
b=r.folder(51)
def norm(s):return re.sub(r'\s','',unicodedata.normalize('NFKC',re.sub(r'[①②③④⑤]','',s).replace('ㆍ','·'))).replace('\x00','')
reg={x['newAsset']:x for x in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/native-image-repairs.json')['figures']}
ledger={x['id']:x for x in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/current900-evidence-ledger.json')['questions']}
for related in [False,True]:
 prefix='related295-' if related else '';rows=r.read(b/'related295-before.json') if related else [x['question'] for x in r.read(b/'revealed-current.json')]
 src={x['id']:x for x in r.read(b/('related295-source.json' if related else 'blind-source.json'))};own={x['id']:x for x in r.read(b/(prefix+'own-solves.json'))};checks=[];pixels=[]
 for q in rows:
  m=src[q['id']];s=re.sub(r'책형\s*\d+쪽','',m['sourceText']);shared=q['number'] in [22,23,29]
  if shared:s=s[s.index('<표 1>'):];s=re.sub(r'(?m)^\s*'+str(q['number'])+r'[.]\s*','',s,count=1)
  else:s=re.split(r'(?m)^\s*'+str(q['number'])+r'[.]\s*',s,maxsplit=1)[1]
  if q['number']==19:s=re.split(r'(?m)^20[.]',s,maxsplit=1)[0]
  actual=norm(s)
  for f in q.get('figures',[]):
   v=reg[f['asset']];assert v['source']==m['source'] and r.sha(r.ROOT/v['source'])==v['sha256']
   with pdfplumber.open(r.ROOT/v['source']) as pdf:part=pdf.pages[v['page1based']-1].crop(v['rect']).extract_text()
   raw=norm(part);assert actual.count(raw)==1,(q['id'],'figure text mismatch',raw[:100]);actual=actual.replace(raw,'',1)
   dst=b/'fresh-source-renders'/f"{v['sha256'][:12]}-p{v['page1based']:02d}";dst.parent.mkdir(exist_ok=True)
   if not dst.with_suffix('.png').exists():subprocess.run([shutil.which('pdftoppm'),'-r',str(v['resolution']),'-f',str(v['page1based']),'-l',str(v['page1based']),'-singlefile','-png',str(r.ROOT/v['source']),str(dst)],check=True,capture_output=True)
   with Image.open(dst.with_suffix('.png')) as im,Image.open(r.ROOT/f['asset']) as old:
    fresh=im.convert('RGB').crop(v['pixelBox']);assert fresh.size==old.size and fresh.tobytes()==old.convert('RGB').tobytes()
   pixels.append(dict(id=q['id'],asset=f['asset'],pixelBox=v['pixelBox'],page=v['page1based'],freshMatch=True))
  if q['number'] in [17,21,22]:
   header='BC' if q['number']==22 else 'ABC';j=actual.rfind(header);assert j>=0;actual=actual[:j]+actual[j+len(header):]
   assert q['choiceNote']==('B → C' if q['number']==22 else 'A → B → C')
  assert actual.count(norm(q['prompt']))==1,(q['id'],actual[:200],norm(q['prompt']));actual=actual.replace(norm(q['prompt']),'',1);expected=norm(q['body']+''.join(q['choices']))
  if q['number'] in [23,26,29] and '<보기>' in actual:
   assert actual.count('<보기>')==1;actual=actual.replace('<보기>','',1)
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
# Verify every year/series claimed correct, not just the falsifying year.
apple=[F(a)/F(h) for a,h in zip([489,368,460,583,422],['29.1','26.9','31','31.6','31.6'])]
assert [round(float(x),1) for x in apple]==[16.8,13.7,14.8,18.4,13.4]
pie=[F(x,4159)*100 for x in [1448,637,456,586,426,224,382]];assert [round(float(x),1) for x in pie]==[34.8,15.3,11.0,14.1,10.2,5.4,9.2]
drunk=[F(a,t)*100 for a,t in zip([91,108,79,89,79,72],[698,759,721,602,717,575])];assert [round(float(x),1) for x in drunk]==[13,14.2,11,14.8,11,12.5]
causes=[18,426,21,13,79,90,70];assert sum(causes)==717 and [round(x/717*100,1) for x in causes]==[2.5,59.4,2.9,1.8,11,12.6,9.8]
late=[F(y-x,x)*100 for x,y in zip([105,83,90],[83,90,72])];safety=[F(y-x,x)*100 for x,y in zip([28,20,13],[20,13,6])]
assert [round(float(x),1) for x in late]==[-21,8.4,-20] and [round(float(x),1) for x in safety]==[-28.6,-35,-53.8]
assert F('86.6')-max(map(F,['55.1','49.5','53.5','49.4','57.5']))==F('29.1')>25
assert F('39')/F('9.6')<5 and F('29.3')/F('4.2')>5 and F('30.3')/F('8.1')<5 and F('16.5')/F('3.1')>5
assert F('20.05')/11<F('1.9') and F('8.4')+F('20.05')>F('8.5')
r.write(b/'exact-model-checks.json',dict(status='PASS',preReveal='pre-reveal-models.json',appleYield=list(map(str,apple)),pie2022=list(map(str,pie)),drunkShares=list(map(str,drunk)),accidentComposition=causes,accidentLateRates=list(map(str,late)),accidentSafetyRates=list(map(str,safety)),reportNeeded=['child age','income bracket'],reportIncomeMinimumGap='29.1%p',dramaCounterexample='All11 omitted dramas20.05/11% each and all폭풍; satisfies ranking and reverses complete producer totals.',mentalHealthMapping=dict(A='우울',B='불안',C='불면증',D='섭식문제')))
print('PASS full-series graphs, report axes, exact mental-health ratios and complete omitted-rank counterexample')
