import re,unicodedata,itertools,subprocess,shutil
from fractions import Fraction as F
from datetime import date
import pdfplumber
from PIL import Image
import review_remaining605 as r
b=r.folder(47);rows=r.read(b/'revealed-current.json');src={x['id']:x for x in r.read(b/'blind-source.json')};own={x['id']:x for x in r.read(b/'own-solves.json')}
norm=lambda s:re.sub(r'\s','',unicodedata.normalize('NFKC',re.sub(r'[①②③④⑤]','',s.replace('ㆍ','·')))).replace('−','-').replace('－','-')
reg={x['newAsset']:x for x in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/native-image-repairs.json')['figures']};checks=[];pixels=[]
for row in rows:
 q=row['question'];m=src[q['id']];s=re.sub(r'책형\s*\d+쪽','',m['sourceText']);s=re.sub(r'^\s*\[39～\s*40\] 다음 글을 읽고 물음에 답하시오[.]\s*','',s);s=re.sub(r'(?m)^\s*'+str(q['number'])+r'[.]\s*','',s,count=1)
 if q['number']==39:
  assert norm(q['prompt']) in norm(s);s=norm(s).replace(norm(q['prompt']),'',1);expected=q['body']+''.join(q['choices'])
 else:expected=q['prompt']+q['body']+''.join(q['choices'])
 if q['number']==8:assert '㉠ ㉡\n' in s;s=s.replace('㉠ ㉡\n','',1);assert q['choiceNote']=='㉠ → ㉡'
 if q['number']==9:
  rec=reg[q['figures'][0]['asset']]
  with pdfplumber.open(r.ROOT/rec['source']) as pdf:raw=pdf.pages[rec['page1based']-1].crop(rec['rect']).extract_text()
  assert norm(raw) in norm(s);s=norm(s).replace(norm(raw),'',1)
  # The original header belongs above the5 answer pairs, separately represented.
  pos=s.rfind('甲乙');assert pos>=0;s=s[:pos]+s[pos+2:];assert q['choiceNote']=='甲 → 乙'
  render=b/'fresh-s09';subprocess.run([shutil.which('pdftoppm'),'-r',str(rec['resolution']),'-f',str(rec['page1based']),'-l',str(rec['page1based']),'-singlefile','-png',str(r.ROOT/rec['source']),str(render)],check=True,capture_output=True)
  with Image.open(render.with_suffix('.png')) as im,Image.open(r.ROOT/q['figures'][0]['asset']) as actual:assert im.convert('RGB').crop(rec['pixelBox']).tobytes()==actual.convert('RGB').tobytes()
  pixels.append(dict(asset=q['figures'][0]['asset'],freshCropMatch=True,source=rec['source'],rect=rec['rect']))
 a,e=norm(s),norm(expected)
 if a!=e:
  j=next((j for j,(x,y) in enumerate(zip(a,e)) if x!=y),min(len(a),len(e)));raise AssertionError((q['id'],j,a[j:j+120],e[j:j+120]))
 with pdfplumber.open(r.ROOT/row['officialKey']) as pdf:pi,t=next((j+1,p.extract_text()) for j,p in enumerate(pdf.pages) if '영역 상황판단' in (p.extract_text() or ''))
 assert q['examDate'][:4] in t and f"책형 {q['book']}" in t.replace('㉮','가').replace('㉯','나');ans={}
 for line in t.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):z=list(map(int,line.split()));ans.update(zip(z[::2],z[1::2]))
 assert ans[q['number']]==q['answer']==own[q['id']]['answer'];checks.append(dict(id=q['id'],source=m['source'],page=m['page'],key=row['officialKey'],keyPage=pi,nativeAndFiveChoicesMatch=True,ownMatches=True))
solutions=[]
for a,c,d in itertools.product(range(10),repeat=3):
 v=(a,a,c,d)
 if sum(x%2 for x in v)==a and v.count(1)==c and v.count(2)==d:solutions.append(v)
assert solutions==[(0,0,0,0),(3,3,1,0)]
rates=[[F('4.2')+F('.5')+min(F('1.5'),F('1.0')),F('4.0')+F('.5')+F('1.5'),F('3.8')+F('.5')+F('.6')],[F('4.2')+F('1.0'),F('4.0')+F('.5'),F('3.8')+F('1.7')]]
assert rates==[[F('5.7'),F('6'),F('4.9')],[F('5.2'),F('4.5'),F('5.5')]]
x=15*F('1.6')/4;y=F(100,8);z=18
assert 120/x==20 and 4*4*(z-y)==88
assert F(60,120)/F(60,100)==F(5,6) and F(100,100)==1
assert date(2015,4,16)<=date(2021,6,30) and date(2020,6,28)<=date(2021,6,30)
terms='입춘 우수 경칩 춘분 청명 곡우 입하 소만 망종 하지 소서 대서 입추 처서 백로 추분 한로 상강 입동 소설 대설 동지 소한 대한'.split()
assert terms[1+12]=='처서'
for j in [3,9,15,21]:assert (j-3)%24 in [0,6,12,18] and (j+3)%24 in [0,6,12,18]
r.write(b/'source-key-model-checks.json',dict(status='PASS',count=10,checks=checks,figurePixels=pixels,selfReference=dict(candidates=1000,solutions=solutions,sums=[sum(v) for v in solutions]),interestRates=[[str(x) for x in row] for row in rates],fuel=dict(xKmPerL=str(x),yKmPerL=str(y),neededLitres=20,distanceDifferenceKm=88),humidityFactor='5/6; decrease1/6, not20%; constant numerator counterexample',solarTerms=terms,sourceOnlyLegalEvaluation=True))
print('PASS10 source/key/native, fresh table crop,1000 self-reference candidates,6 exact rates and unit conversions')
