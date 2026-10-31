import re,unicodedata,subprocess,shutil
import pdfplumber
from PIL import Image
import review_remaining605 as r
b=r.folder(41);rows=r.read(b/'revealed-current.json');src={x['id']:x for x in r.read(b/'blind-source.json')};own={x['id']:x for x in r.read(b/'own-solves.json')}
def norm(s):return re.sub(r'\s','',unicodedata.normalize('NFKC',re.sub(r'[①②③④⑤]','',s).replace('ㆍ','·'))).replace('[빈칸]','')
reg={x['newAsset']:x for x in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/native-image-repairs.json')['figures']};checks=[];pixels=[]
for row in rows:
 q=row['question'];m=src[q['id']];s=re.sub(r'책형\s*\d+쪽','',m['sourceText']);s=re.sub(r'^\s*\[19～\s*20\] 다음 글을 읽고 물음에 답하시오[.]\s*','',s);s=re.sub(r'(?m)^\s*'+str(q['number'])+r'[.]\s*','',s,count=1)
 if q['number']==14:s=s.replace('작년 올해','');assert q['choiceNote']=='작년 → 올해'
 if q['number'] in [20,27]:s=s.replace('(가) (나)','');assert q['choiceNote']=='(가) → (나)'
 if q['number'] in [19,20]:
  prompt=re.search(r'윗글.*?\?',s,re.S).group();assert norm(prompt)==norm(q['prompt']);s=s.replace(prompt,'',1);expected=q['body']+''.join(q['choices'])
 else:expected=q['prompt']+q['body']+''.join(q['choices'])
 if q['figures']:
  assert norm(s).startswith(norm(q['prompt']));s=q['prompt']+s[s.index('①'):]
 assert norm(s)==norm(expected),(q['id'],'native mismatch')
 with pdfplumber.open(r.ROOT/row['officialKey']) as pdf:pi,t=next((j+1,p.extract_text()) for j,p in enumerate(pdf.pages) if '영역 상황판단' in (p.extract_text() or ''))
 assert q['examDate'][:4] in t and f"책형 {q['book']}" in t.replace('㉮','가').replace('㉯','나');ans={}
 for line in t.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):z=list(map(int,line.split()));ans.update(zip(z[::2],z[1::2]))
 assert ans[q['number']]==q['answer']==own[q['id']]['answer'];checks.append(dict(id=q['id'],source=m['source'],page=m['page'],key=row['officialKey'],keyPage=pi,nativeAndAllFiveChoicesMatch=True,ownMatches=True))
 for f in q['figures']:
  v=reg[f['asset']];assert v['source']==m['source'] and r.sha(r.ROOT/v['source'])==v['sha256'];dst=b/'fresh-source-renders'/f"p{v['page1based']:02d}";dst.parent.mkdir(exist_ok=True)
  subprocess.run([shutil.which('pdftoppm'),'-r',str(v['resolution']),'-f',str(v['page1based']),'-l',str(v['page1based']),'-singlefile','-png',str(r.ROOT/v['source']),str(dst)],check=True,capture_output=True)
  with Image.open(dst.with_suffix('.png')) as im,Image.open(r.ROOT/f['asset']) as old:
   fresh=im.convert('RGB').crop(v['pixelBox']);assert fresh.size==old.size and fresh.tobytes()==old.convert('RGB').tobytes()
  pixels.append(dict(id=q['id'],asset=f['asset'],pixelBox=v['pixelBox'],page=v['page1based'],freshMatch=True))
assert r.read(b/'blind-exact-models.json')['status']=='PASS'
r.write(b/'source-key-model-checks.json',dict(status='PASS',checks=checks,figurePixels=pixels,exactModels='blind-exact-models.json',originalVisualReview='All10 original images inspected, including full shared19/20, code8x2table and all5performance columns.'))
print('PASS10 sources keys native;2fresh figure crops; pre-reveal exact models')
