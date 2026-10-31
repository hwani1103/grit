"""Audit native blocks moved to source images: the replacement must cover the removed text."""
from pathlib import Path
import json,pdfplumber
from psat_batch_tools import norm
R=Path(__file__).resolve().parents[1];root=R/'artifacts/psat600_20261028';questions={};proof=[]
for path in (R/'assets/psat').glob('*.json'):
 obj=json.loads(path.read_text(encoding='utf-8'))
 if isinstance(obj,list):questions.update({q['id']:q for q in obj})
for path in root.glob('*/source-transcripts.json'):
 for qid,tr in json.loads(path.read_text(encoding='utf-8')).items():
  q=questions.get(qid)
  if not q or not q.get('figures') or not tr.get('removedBlocks'):continue
  manifest=json.loads((path.parent/'crop-manifest.json').read_text(encoding='utf-8'))
  figures={f['asset'] for f in q['figures']};sourceTexts=[]
  for c in manifest:
   if c['asset'] not in figures:continue
   with pdfplumber.open(R/c['source']) as pdf:sourceTexts.append(pdf.pages[c['page1based']-1].crop(c['rect']).extract_text() or '')
  replacement=norm('\n'.join(sourceTexts))
  for block in tr['removedBlocks']:
   assert norm(block) in replacement,(path.parent.name,qid,'removed native content outside replacement image')
  proof.append({'batch':path.parent.name,'id':qid,'removedBlocks':len(tr['removedBlocks']),'status':'PASS'})
dest=root/'verbal23/image-replacement-scope-check.json'
dest.write_text(json.dumps({'scope':'Published image replacements declared in source-transcripts.json;native-table conversions separately covered by their batch checks. Not a whole-bank semantic review.','checks':proof},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PASS image replacement coverage',len(proof),'questions')
