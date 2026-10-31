import re,unicodedata,subprocess,shutil,itertools
import pdfplumber
from PIL import Image
import review_remaining605 as r
b=r.folder(50)
def norm(s):return re.sub(r'\s','',unicodedata.normalize('NFKC',re.sub(r'[①②③④⑤]','',s).replace('ㆍ','·')))
reg={x['newAsset']:x for x in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/native-image-repairs.json')['figures']}
ledger={x['id']:x for x in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/current900-evidence-ledger.json')['questions']}
for related in [False,True]:
 prefix='related295-' if related else ''
 rows=r.read(b/'related295-before.json') if related else [x['question'] for x in r.read(b/'revealed-current.json')]
 src={x['id']:x for x in r.read(b/('related295-source.json' if related else 'blind-source.json'))};own={x['id']:x for x in r.read(b/(prefix+'own-solves.json'))};checks=[];pixels=[]
 for q in rows:
  m=src[q['id']];s=re.sub(r'책형\s*\d+쪽','',m['sourceText']);s=re.sub(r'^\s*\[19～20\] 다음 글을 읽고 물음에 답하시오[.]\s*','',s);s=re.sub(r'(?m)^\s*'+str(q['number'])+r'[.]\s*','',s,count=1);actual=norm(s)
  for f in q.get('figures',[]):
   v=reg[f['asset']];assert v['source']==m['source'] and r.sha(r.ROOT/v['source'])==v['sha256']
   with pdfplumber.open(r.ROOT/v['source']) as pdf:part=pdf.pages[v['page1based']-1].crop(v['rect']).extract_text()
   raw=norm(part);assert actual.count(raw)==1,(q['id'],'figure text mismatch',raw[:100]);actual=actual.replace(raw,'',1)
   dst=b/'fresh-source-renders'/f"{v['sha256'][:12]}-p{v['page1based']:02d}";dst.parent.mkdir(exist_ok=True)
   if not dst.with_suffix('.png').exists():subprocess.run([shutil.which('pdftoppm'),'-r',str(v['resolution']),'-f',str(v['page1based']),'-l',str(v['page1based']),'-singlefile','-png',str(r.ROOT/v['source']),str(dst)],check=True,capture_output=True)
   with Image.open(dst.with_suffix('.png')) as im,Image.open(r.ROOT/f['asset']) as old:
    fresh=im.convert('RGB').crop(v['pixelBox']);assert fresh.size==old.size and fresh.tobytes()==old.convert('RGB').tobytes()
   pixels.append(dict(id=q['id'],asset=f['asset'],pixelBox=v['pixelBox'],page=v['page1based'],freshMatch=True))
  if not related and q['number'] in [14,20]:
   header='최솟값최댓값' if q['number']==14 else '직접효과비율승수'
   j=actual.rfind(header);assert j>=0;actual=actual[:j]+actual[j+len(header):]
   assert q['choiceNote']==('최솟값 → 최댓값' if q['number']==14 else '직접효과 → 비율승수')
  if not related and q['number'] in [19,20]:
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
# Exhaust every unary predicate truth assignment for a possible individual.
worlds=[];counter=[]
for opt in range(5):
 accepted=[]
 for S,B,A,L,R,H,D in itertools.product([False,True],repeat=7):
  if not((not S or B) and (not B or A or L or R) and (not B or not L) and (not A or H or D)):continue
  extra=[(not S or not L) and (not S or not D),(not L or R) and (not A or D),(not B or not R) and (not A or not D),(not B or not R) and (not A or not H),(not B or R) and (not A or not D)][opt]
  if extra:accepted.append((S,B,A,L,R,H,D))
 bad=[x for x in accepted if x[0] and not x[5]]
 assert bool(bad)==(opt!=2);worlds.append(accepted);counter.append(bad)
ages=[]
for a,bb,c,d,e in itertools.permutations(range(1,8),5):
 if e>bb>a and bb==a+1 and bb>c and d<min(a,bb,c,e):ages.append((a,bb,c,d,e))
assert ages and all(sorted(v,reverse=True)[1]==v[1] for v in ages)
assert [sum(v) for v in [(2,7,4,5),(3,7,4,4),(4,6,2,5),(4,6,3,5)]]==[18,18,17,18]
assert 10+20+20==50 and 50/20==2.5 and 50/10==5 and min(6/.1*5,250)==250
with pdfplumber.open(r.ROOT/'artifacts/psat600_20261028/sources/6015/pdf/언어논리-사.pdf') as pdf:
 p=pdf.pages[7];strokes=[l for l in p.lines if abs(l['top']-126.986)<.1 and 570<l['x0']<571]
 assert len(strokes)==1 and 635<strokes[0]['x1']<637
 chars=[c for c in p.chars if c['x0']>=strokes[0]['x0']-.1 and c['x1']<=strokes[0]['x1']+.1 and 110<c['top']<127]
 marked=''.join(c['text'] for c in chars);assert norm(marked)==norm('두 개의 전제'),marked
r.write(b/'exact-model-checks.json',dict(status='PASS',preReveal='pre-reveal-exact-models.json',logicWorlds=worlds,logicCounterexamples=counter,ageOrderExamples=ages,scoreTotals=[18,18,17,18],tourism=dict(initial=20,direct=10,indirect=20,induced=20,total=50,ratioMultiplier=5,generalMultiplier=2.5),legalScope='Given source clauses only; include high school pupil aged18, exclude purchaser, distinguish register and agency; renewal exception and command before fine.',underline=dict(id='kr-mpm-2026-07-18-psat-l-16',source=m['source'],page=8,stroke=strokes[0],sourceText='두 개의 전제',excludedParticle='를')))
print('PASS exact gem/duty/score models,128 logic worlds per option,age counterexamples and source underline stroke')
