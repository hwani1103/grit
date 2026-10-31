from pathlib import Path
import json,subprocess,sys,pdfplumber
from psat_batch_tools import validate,norm
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/data28'
subprocess.run([sys.executable,str(A/'solve.py')],check=True,stdout=subprocess.DEVNULL)
bank=json.loads((A/'authored-data28.json').read_text(encoding='utf-8'));proof=json.loads((A/'model-proof.json').read_text(encoding='utf-8'))
assert [q['answer'] for q in bank]==[5,3,5,2,2,5,2,3,2,2]
for q in bank:assert q['answer']==proof[str(q['number'])]['answer']
tr=json.loads((A/'source-transcripts.json').read_text(encoding='utf-8'));manifest=json.loads((A/'crop-manifest.json').read_text(encoding='utf-8'))
q=next(q for q in bank if q['number']==13);regions=[c for c in manifest if c['asset'] in {f['asset'] for f in q['figures']}]
with pdfplumber.open(R/regions[0]['source']) as pdf:
 for source,crop in zip(tr[q['id']]['fullSourceChoiceTextCoveredByFigures'],regions):
  actual=pdf.pages[crop['page1based']-1].crop(crop['rect']).extract_text() or ''
  assert norm(source) in norm(actual),(source,actual)
validate('data28',{'directModelProof':proof,'manualSourceReview':'All10 originals visually read;21figures retain tables/chartchoices/units/footnotes. Exact ratios/rank bounds/tier sums/5graph comparisons/120sea assignments/fund weights.2023D14 held due unexplained99.9% vs6042/6044;notpublished.'},[('2023-03-04',n) for n in [6,7,8,9,10,11,12,13,15,16]],21)
