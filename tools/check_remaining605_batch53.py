import re,unicodedata,subprocess,shutil,itertools
import pdfplumber
from PIL import Image
import review_remaining605 as r
b=r.folder(53)
def norm(s):return re.sub(r'\s','',unicodedata.normalize('NFKC',re.sub(r'[①②③④⑤]','',s).replace('ㆍ','·')))
reg={x['newAsset']:x for x in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/native-image-repairs.json')['figures']}
ledger={x['id']:x for x in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/current900-evidence-ledger.json')['questions']}
for related in [False,True]:
 prefix='related295-' if related else ''
 rows=r.read(b/'related295-before.json') if related else [x['question'] for x in r.read(b/'revealed-current.json')]
 src={x['id']:x for x in r.read(b/('related295-source.json' if related else 'blind-source.json'))};own={x['id']:x for x in r.read(b/(prefix+'own-solves.json'))};checks=[];pixels=[]
 for q in rows:
  m=src[q['id']];s=re.sub(r'책형\s*\d+쪽','',m['sourceText']);s=re.sub(r'^\s*\[39～\s*40\] 다음 글을 읽고 물음에 답하시오[.]\s*','',s);s=re.sub(r'(?m)^\s*'+str(q['number'])+r'[.]\s*','',s,count=1);actual=norm(s)
  for f in q.get('figures',[]):
   v=reg[f['asset']];assert v['source']==m['source'] and r.sha(r.ROOT/v['source'])==v['sha256']
   with pdfplumber.open(r.ROOT/v['source']) as pdf:part=pdf.pages[v['page1based']-1].crop(v['rect']).extract_text()
   raw=norm(part);assert actual.count(raw)==1,(q['id'],'figure text mismatch',raw[:100]);actual=actual.replace(raw,'',1)
   dst=b/'fresh-source-renders'/f"{v['sha256'][:12]}-p{v['page1based']:02d}";dst.parent.mkdir(exist_ok=True)
   if not dst.with_suffix('.png').exists():subprocess.run([shutil.which('pdftoppm'),'-r',str(v['resolution']),'-f',str(v['page1based']),'-l',str(v['page1based']),'-singlefile','-png',str(r.ROOT/v['source']),str(dst)],check=True,capture_output=True)
   with Image.open(dst.with_suffix('.png')) as im,Image.open(r.ROOT/f['asset']) as old:
    fresh=im.convert('RGB').crop(v['pixelBox']);assert fresh.size==old.size and fresh.tobytes()==old.convert('RGB').tobytes()
   pixels.append(dict(id=q['id'],asset=f['asset'],pixelBox=v['pixelBox'],page=v['page1based'],freshMatch=True))
  if related and q['number']==39:
   assert actual.count(norm(q['prompt']))==1;actual=actual.replace(norm(q['prompt']),'',1);expected=norm(q['body']+''.join(q['choices']))
  else:expected=norm(q['prompt']+q['body']+''.join(q['choices']))
  if actual!=expected:
   j=next((j for j,(a,e) in enumerate(zip(actual,expected)) if a!=e),min(len(actual),len(expected)));raise AssertionError((q['id'],j,actual[j:j+100],expected[j:j+100]))
  key=ledger[q['id']]['officialKey']
  with pdfplumber.open(r.ROOT/key) as pdf:pi,t=next((j+1,p.extract_text()) for j,p in enumerate(pdf.pages) if '영역 '+q['subject'] in (p.extract_text() or ''))
  assert q['examDate'][:4] in t and f"책형 {q['book']}" in t.replace('㉮','가').replace('㉯','나');ans={}
  for line in t.splitlines():
   if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):z=list(map(int,line.split()));ans.update(zip(z[::2],z[1::2]))
  assert ans[q['number']]==q['answer']==own[q['id']]['answer'];checks.append(dict(id=q['id'],source=m['source'],page=m['page'],key=key,keyPage=pi,nativeAndAllFiveChoicesMatch=True,ownMatches=True))
 r.write(b/(prefix+'source-key-checks.json'),dict(status='PASS',checks=checks,figurePixels=pixels,originalVisualReview='All respective original images inspected; shared19/20 full source page.'))
 print(prefix or 'target',len(checks),'source/key/native PASS;',len(pixels),'fresh crops')
from datetime import date
from calendar import monthrange
events=[(date(2022,1,5),50000,5,0),(date(2022,9,20),22000,2,2000),(date(2023,1,9),25000,2,0),(date(2023,3,27),50300,4,300),(date(2024,1,5),10500,5,500)]
lots=[];history=[]
for dt,amount,rate,use in events:
 expired=[v for v in lots if v['expiry']<dt];lots=[v for v in lots if v['expiry']>=dt]
 spend=use
 for v in lots:
  n=min(spend,v['balance']);v['balance']-=n;spend-=n
 assert spend==0
 earned=(amount-use)*rate//100;expiry=date(dt.year+1,dt.month,monthrange(dt.year+1,dt.month)[1]);lots.append(dict(earned=dt,balance=earned,expiry=expiry))
 history.append(dict(date=str(dt),expired=[dict(balance=v['balance'],expiry=str(v['expiry'])) for v in expired],used=use,earned=earned,balance=sum(v['balance'] for v in lots)))
assert sum(v['balance'] for v in lots if v['expiry']>=date(2024,1,10))==2500
dates=['920202','931118','000610','010411','031103'];births=[date(1992,2,2),date(1993,11,18),date(2000,6,10),date(2001,4,11),date(2003,11,3)];elig=[]
for txt,born in zip(dates,births):
 ages=[year-born.year-((4,10)<(born.month,born.day)) for year in [2022,2023,2028]]
 checks=[all(20<=a<=35 for a in ages),born.day%2==1,len(set(txt))==3,any(a==bb for a,bb in zip(txt,txt[1:]))];elig.append(dict(candidate=txt,ages=ages,conditions=checks))
assert [x['candidate'] for x in elig if all(x['conditions'])]==['010411']
orders=[p for p in itertools.permutations('ABCDE') if p.index('B')<p.index('D')<p.index('C') and p.index('C')<p.index('A') and p.index('C')<p.index('E') and p.index('A') in [0,4]]
assert orders==[tuple('BDCEA')]
models=r.read(b/'pre-reveal-exact-models.json');assert models['status']=='PASS'
r.write(b/'exact-model-checks.json',dict(status='PASS',sourceOnly='pre-reveal-exact-models.json',pointLedger=history,finalPoints=2500,birthdayChecks=elig,raceOrders=orders,lottery='Separate sales60%,first-prize30%,and first-prize lump60%; tax reduces further. No real-world law assumptions.',votingExplanationDefect='Existing step4 final sentence uses C-selected (3,2,5) to refute C>=4, which does not work. Replace by A/B-selected giving C3; other steps/option reasons and answer3 already correct.'))
print('PASS FIFO expiries, birth-date boundaries, all120 race orders and exact pre-reveal models')
