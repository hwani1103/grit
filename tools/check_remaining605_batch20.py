"""Source/keys, instruction figure pixels and complete calendar/history models."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,permutations
import hashlib,json,re,shutil,subprocess,unicodedata
import pdfplumber
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/psat_remaining605_20261030';B=OUT/'batch20'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
norm=lambda s:re.sub(r'[\s「」『』\uf000\uf001/]','',unicodedata.normalize('NFKC',re.sub(r'[①②③④⑤ㆍ·․]','',s)))
rows=read(B/'revealed-current.json');sources={x['id']:x for x in read(B/'blind-source.json')};solves={x['id']:x for x in read(B/'own-solves.json')};reg={x['newAsset']:x for x in read(ROOT/'artifacts/psat_final_quality_20261029/full900/native-image-repairs.json')['figures']};checks=[];pixels=[];renders={}
for row in rows:
 q=row['question'];m=sources[q['id']];native=m['sourceText']
 if m['sharedPassageRange']:
  common,question=re.split(r'\n(?:문\s*)?23[.]\s*',native,maxsplit=1)
  common=re.sub(r'^※\s*\[(?:문\s*)?23[.]?\s*[～~∼-]\s*(?:문\s*)?24[.]?\]\s*다음 글을 읽고 물음에 답하시오[.]\s*','',common)
  assert norm(common)==norm(q['body']),(q['id'],'full common source including formula')
  native=norm(question);expected=norm(q['prompt']+''.join(q['choices']))
 else:
  native=norm(re.sub(r'^.*?\b'+str(q['number'])+r'[.]\s*','',native,count=1,flags=re.S))
  for f in q.get('figures',[]):
   r=reg[f['asset']]
   with pdfplumber.open(ROOT/r['source']) as pdf:figtext=norm(pdf.pages[r['page1based']-1].crop(r['rect']).extract_text() or '')
   assert native.count(figtext)==1,(q['id'],'figure text',f['asset']);native=native.replace(figtext,'',1)
   assert hashlib.sha256((ROOT/r['source']).read_bytes()).hexdigest()==r['sha256']
   sig=(r['source'],r['page1based'],r['resolution'])
   if sig not in renders:
    d=B/'fresh-source-renders';d.mkdir(exist_ok=True);prefix=d/f"{r['sha256'][:16]}-p{r['page1based']:02d}"
    subprocess.run([shutil.which('pdftoppm'),'-r',str(r['resolution']),'-f',str(r['page1based']),'-l',str(r['page1based']),'-singlefile','-png',str(ROOT/r['source']),str(prefix)],check=True,capture_output=True)
    renders[sig]=Image.open(prefix.with_suffix('.png')).convert('RGB')
   a=renders[sig].crop(r['pixelBox'])
   with Image.open(ROOT/f['asset']) as im:b=im.convert('RGB');assert a.size==b.size and a.tobytes()==b.tobytes()
   pixels.append(dict(id=q['id'],asset=f['asset'],pixelMatch=True))
  if q['id']=='kr-mpm-2025-11-15-psat-s-04':
   table=q['tables'][0]
   assert table['columns']==['구분','소음대책지역','군용비행장 설치일','전입일','2024년 실제 거주기간']
   assert table['rows']==[['甲','제2종 구역','2010. 3. 29.','2015. 1. 7.','1. 1. ～ 12. 31.'],['乙','제1종 구역','2010. 3. 29.','2009. 1. 7.','1. 1. ～ 8. 31.']] and table['afterParagraph']==10
   block=norm('군용비행장 2024년 실제 구분 소음대책지역 전입일 설치일 거주기간 甲 제2종 구역 2010. 3. 29. 2015. 1. 7. 1. 1.～12. 31. 乙 제1종 구역 2010. 3. 29. 2009. 1. 7. 1. 1.～8. 31.')
   assert native.count(block)==1;native=native.replace(block,'',1)
  body=q['body']
  if q['id']=='kr-mpm-2021-07-10-psat-s-21':
   assert body.count('□')==1
   body=body.replace('□','') # Original answer blank is a drawn box.
  expected=norm(q['prompt']+body+''.join(q['choices']))
 if native!=expected:
  i=next((i for i,(a,b) in enumerate(zip(native,expected)) if a!=b),min(len(native),len(expected)))
  raise AssertionError((q['id'],i,native[max(0,i-25):i+120],expected[max(0,i-25):i+120]))
 with pdfplumber.open(ROOT/row['officialKey']) as pdf:
  pi,t=next((i+1,p.extract_text()) for i,p in enumerate(pdf.pages) if '영역 상황판단' in (p.extract_text() or ''))
 assert q['examDate'][:4] in t and f"책형 {q['book']}" in t
 answers={}
 for line in t.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
   z=list(map(int,line.split()));answers.update(zip(z[::2],z[1::2]))
 assert answers[q['number']]==q['answer']==solves[q['id']]['answer']
 checks.append(dict(id=q['id'],source=m['source'],sourcePage=m['page'],fullNativeTextAndFiveChoicesMatch=True,key=row['officialKey'],keyPage=pi,answer=q['answer']))
for im in renders.values():im.close()

def divisionAllowed(kind,prior,recent,satisfaction):
 thresholds={'general':(100,120),'discussion':(60,80),'english':(30,50),'practical':(20,None)}
 average,maximum=thresholds[kind];factor=F('.9') if satisfaction>=90 else F(1)
 return F(prior+recent,2)>=average*factor or (maximum is not None and max(prior,recent)>=maximum*factor)
assert not divisionAllowed('general',100,80,85)
assert all(not divisionAllowed('english',10,45,s) or s>=90 for s in range(101))
assert all(divisionAllowed('english',10,45,s) for s in range(90,101))
assert [n for n in range(31) if not divisionAllowed('practical',20,n,92)]==list(range(16))
assert divisionAllowed('practical',20,16,92)

# Six visit slots: Monday lunch/dinner through Wednesday lunch/dinner.
base=[];byOption=[[] for _ in range(5)]
for a,e,b in permutations(range(6),3):
 if e%2!=1 or b not in [2,4] or not(e<a):continue
 base.append((a,e,b))
 predicates=[b//2==e//2+1,a%2==0 and a<b,a>max(e,b),min(a,e,b)>=2,b>max(a,e)]
 for i,value in enumerate(predicates):
  if value:byOption[i].append((a,e,b))
assert len(base)==9 and list(map(len,byOption))==[4,1,7,3,2]
assert byOption[1]==[(2,1,4)]

histories=list(product([0,1],repeat=5));installed=[];first={3:[],4:[],5:[]}
for h in histories:
 days=[k for k in range(3,6) if all(h[k-3:k])]
 if days:installed.append(h);first[min(days)].append(h)
assert len(installed)==8 and [len(first[k]) for k in [3,4,5]]==[4,2,2]
assert 200000//32==6250 and len(installed)*6250==50000
assert (1,0,1,1,1) in first[5] and (0,0,1,1,1) in first[5]

# Source proposal retains total50 while making unauthorized subscore swaps.
currentI=[10,5,5];proposedI=[10,10,5];currentII=[5,5];proposedII=[5,5,5];currentIII=[7,3];proposedIII=[3,7]
assert sum(currentI)==20 and sum(proposedI)==25 and sum(currentII)==10 and sum(proposedII)==15
assert sum(currentIII)==sum(proposedIII)==10 and currentIII!=proposedIII
assert sum(proposedI+proposedII+proposedIII)==50
proposalMatches=[False,True,True,False,True]
assert 100000//50==2000>200

from datetime import date
installation=date(2010,3,29);aEntry=date(2015,1,7);eEntry=date(2009,1,7)
assert eEntry<installation<aEntry
compensation=[F(45000)*F('.5')*12,F(60000)*8];assert compensation==[270000,480000] and sum(compensation)==750000
fuel=[F(250000)*F('1.1'),F(200000)*F('1.3'),F(250000)];assert fuel==[275000,260000,250000] and fuel[0]>fuel[1]>fuel[2]

qualitative={'2021s16':'Complaint class fixed before per-stage exception: discomfort other; permit statutory. Transfer remains required; statutory repeated-case exclusion remains.', '2021s23':'Minister-required completed referendum substitutes for council opinion; all proposals via governor.2% signers2000; heads and councils nominate, no implied preproposal resolution.', '2025s01':'Minister writes list with foreign labor authority; jobagency receives domestic application and grants employer permit. Fee permission is not free duty.', '2025s03':'Compounding versus sale and location versus prescription exceptions separate. Volunteer compounding in pharmacy valid; general-drug sale with location approval valid; professional-drug patient sale without prescription invalid.'}
(B/'source-key-model-checks.json').write_text(json.dumps(dict(status='PASS',count=10,sourceKeyChecks=checks,figurePixels=pixels,nativeCompensationTableAndPlacement=True,divisionStrictThreshold16=True,restaurantBaseModels=base,restaurantOptionModelCounts=list(map(len,byOption)),restaurantUniqueWitness=[2,1,4],weatherAllHistories=32,weatherInstallHistories=installed,weatherFirstDayCounts={str(k):len(v)*6250 for k,v in first.items()},weatherInstallTotal=50000,proposalMatches=proposalMatches,compensation=list(map(str,compensation)),fuel=list(map(str,fuel)),qualitative=qualitative,limitations='Same-author original-source solving. Source figures checked against fresh crops. Qualitative regulations confined to given text; no current-law or medical guidance, no device/APK.'),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PASS10 source/key matches;3fresh crops/native table;all9restaurant models,32weather histories and strict threshold/cash witnesses.')
