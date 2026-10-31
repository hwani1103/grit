"""Read-only source/key/pixel evidence for an already solved and revealed batch.

Does not produce solves, ratings, or semantic clearance. Adjacent question
boundaries follow real PDF margin headings, rather than a two-questions rule.
"""
from pathlib import Path
import argparse,hashlib,json,re,shutil,subprocess,unicodedata
import pdfplumber
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('batch',type=int);parser.add_argument('--related',action='store_true');args=parser.parse_args()
OUT=ROOT/f'artifacts/psat_remaining605_20261030/batch{args.batch:02d}'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
norm=lambda s:re.sub(r'[\s·ㆍ/]','',unicodedata.normalize('NFKC',re.sub(r'[①②③④⑤]','',s)))
prefix='related295-' if args.related else ''
if args.related:
 ledger={x['id']:x for x in read(ROOT/'artifacts/psat_final_quality_20261029/full900/current900-evidence-ledger.json')['questions']}
 rows=[dict(question=q,officialKey=ledger[q['id']]['officialKey']) for q in read(OUT/'related295-before.json')]
else:rows=read(OUT/'revealed-current.json')
solves={x['id']:x for x in read(OUT/f'{prefix}own-solves.json')};sources={x['id']:x for x in read(OUT/('related295-source.json' if args.related else 'blind-source.json'))}
config=read(OUT/f'{prefix}source-check-config.json') if (OUT/f'{prefix}source-check-config.json').exists() else {}
reg={x['newAsset']:x for x in read(ROOT/'artifacts/psat_final_quality_20261029/full900/native-image-repairs.json')['figures']}
pdfs={};renders={};checks=[];pixels=[]
try:
 for row in rows:
  q=row['question'];m=sources[q['id']];src=ROOT/m['source']
  if src not in pdfs:pdfs[src]=pdfplumber.open(src)
  page=pdfs[src].pages[m['page']-1];side=m['side'];left=side*page.width/2;right=(side+1)*page.width/2
  words=page.extract_words();heading=next(w for w in words if w['text']==str(q['number'])+'.' and left<=w['x0']<left+45)
  nextHeads=[w for w in words if re.fullmatch(r'\d+[.]',w['text']) and int(w['text'][:-1])>q['number'] and left<=w['x0']<left+45 and w['top']>heading['top']+5]
  bottom=min([w['top']-1 for w in nextHeads],default=page.height)
  rectangles=[reg[f['asset']]['rect'] for f in q.get('figures',[])]
  def keep(obj):
   if obj.get('object_type')!='char':return True
   x=(obj['x0']+obj['x1'])/2;y=(obj['top']+obj['bottom'])/2
   return not any(a<=x<=c and b<=y<=d for a,b,c,d in rectangles)
  filtered=page.filter(keep);native=filtered.crop((left,heading['top']-1,right,bottom)).extract_text() or ''
  if m.get('columnContinuation',False) or q['id'] in config.get('columnContinuation',[]):
   following=[w for w in words if re.fullmatch(r'\d+[.]',w['text']) and int(w['text'][:-1])>q['number'] and page.width/2<=w['x0']<page.width/2+45]
   stop=min([w['top']-1 for w in following],default=page.height)
   tail=filtered.crop((page.width/2,30,page.width,stop)).extract_text() or ''
   native+='\n'+re.sub(r'책형\s*\d+쪽','',tail)
  for before,after in config.get('sourceTextReplacements',{}).get(q['id'],[]):
   assert native.count(before)==1,(q['id'],'explicit PDF extraction replacement',before)
   native=native.replace(before,after,1)
  native=norm(re.sub(r'^(?:문\s*)?\d+[.]\s*','',native))
  for block in config.get('removeSourceBlocks',{}).get(q['id'],[]):
   block=norm(block);assert native.count(block)==1,(q['id'],'explicit heading',block);native=native.replace(block,'',1)
  choices='' if q['id'] in config.get('imageChoices',[]) else ''.join(q['choices'])
  expected=norm(q['prompt']+q['body']+choices)
  if native!=expected:
   i=next((i for i,(a,b) in enumerate(zip(native,expected)) if a!=b),min(len(native),len(expected)))
   raise AssertionError((q['id'],i,native[max(0,i-20):i+120],expected[max(0,i-20):i+120]))
  with pdfplumber.open(ROOT/row['officialKey']) as keypdf:
   pi,t=next((i+1,p.extract_text()) for i,p in enumerate(keypdf.pages) if '영역 자료해석' in (p.extract_text() or ''))
  assert q['examDate'][:4] in t and f"책형 {q['book']}" in t.replace('㉯','나').replace('㉮','가')
  answers={}
  for line in t.splitlines():
   if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
    z=list(map(int,line.split()));answers.update(zip(z[::2],z[1::2]))
  assert answers[q['number']]==q['answer']
  own=solves[q['id']];conditional=config.get('existingAppConditions',{}).get(q['id'])
  primaryMatches=own['answer']==answers[q['number']]
  if conditional:
   # Only an alternative explicitly recorded before reveal can match a
   # condition already present in the pre-edit app snapshot. Never replace
   # the first raw-source answer or add a new condition to force the key.
   frozen=read(OUT/'solve-frozen-before-reveal.json')
   assert hashlib.sha256((OUT/'own-solves.json').read_bytes()).hexdigest()==frozen['solveFileSha256']
   assert own['answer']==conditional['rawSourceAnswer'] and own['alternativeAnswerIfMagnitude']==answers[q['number']]
   assert own.get('uncertainty') and q.get('choiceNote')==conditional['choiceNote']
   assert '원문에 명시되지 않은' in q['editNote'] and '절댓값' in q['choiceNote']
  elif q['id'] in config.get('postRevealAnswerCorrections',{}):
   receipt=read(OUT/config['postRevealAnswerCorrections'][q['id']])
   frozen=read(OUT/'solve-frozen-before-reveal.json')
   assert hashlib.sha256((OUT/'own-solves.json').read_bytes()).hexdigest()==frozen['solveFileSha256']
   assert receipt['id']==q['id'] and receipt['answerBefore']==own['answer'] and receipt['answerAfter']==answers[q['number']] and receipt['issue'] and receipt['source']
  else:assert primaryMatches,(q['id'],'own primary answer differs')
  checks.append(dict(id=q['id'],source=m['source'],sourcePage=m['page'],side=side,questionTop=heading['top'],nextQuestionCutoff=bottom,nativeTextAndFiveChoicesOrImageChoicesMatch=True,key=row['officialKey'],keyPage=pi,answer=answers[q['number']],ownPrimaryAnswer=own['answer'],ownPrimaryMatchesOfficial=primaryMatches,prespecifiedAlternativeUnderExistingAppCondition=bool(conditional)))
  for f in q.get('figures',[]):
   record=reg[f['asset']];assert record['source']==m['source'] and hashlib.sha256(src.read_bytes()).hexdigest()==record['sha256']
   sig=(m['source'],record['page1based'],record['resolution'])
   if sig not in renders:
    d=OUT/'fresh-source-renders';d.mkdir(exist_ok=True);renderPrefix=d/f"{record['sha256'][:16]}-p{record['page1based']:02d}-r{record['resolution']}"
    subprocess.run([shutil.which('pdftoppm'),'-r',str(record['resolution']),'-f',str(record['page1based']),'-l',str(record['page1based']),'-singlefile','-png',str(src),str(renderPrefix)],check=True,capture_output=True)
    renders[sig]=Image.open(renderPrefix.with_suffix('.png')).convert('RGB')
   fresh=renders[sig].crop(record['pixelBox']);actual=Image.open(ROOT/f['asset']).convert('RGB')
   assert fresh.size==actual.size and fresh.tobytes()==actual.tobytes(),f['asset']
   pixels.append(dict(id=q['id'],asset=f['asset'],sourcePage=record['page1based'],pixelBox=record['pixelBox'],pixelMatch=True))
finally:
 for pdf in pdfs.values():pdf.close()
 for im in renders.values():im.close()
(OUT/f'{prefix}source-native-pixel-checks.json').write_text(json.dumps(dict(status='PASS',officialSourceKeyNative=checks,figurePixels=pixels,limitations='Source/key/pixel checks only; own semantic evaluation and host readability evidence are separate. No whole key pages printed.'),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PASS direct selected keys/native source and fresh figure crops:',len(checks),len(pixels))
