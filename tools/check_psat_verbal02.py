"""Audit the 2024 verbal Set against official source files.
Text equivalence is mechanical; semantic review and source visual checks are
separately documented, never inferred from a passing script.
"""
from pathlib import Path
from fractions import Fraction as F
import json,re,hashlib,itertools
import pdfplumber
ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'artifacts/psat600_20261028/verbal02'
SOURCE=ROOT/'artifacts/psat600_20261028/sources/4555/pdf/언어논리(사).pdf'
KEY=ROOT/'artifacts/psat600_20261028/sources/4564/BBSMSTR_000000000138_4564_1.pdf'
PUBLISHED=ROOT/'assets/psat/verbal02.json'
BANK=PUBLISHED if PUBLISHED.exists() else ART/'authored-verbal02.json'
bank=json.loads(BANK.read_text(encoding='utf-8'))
def norm(s):
 # PDF font maps both book-quote glyphs to the same private-use code point.
 return re.sub(r'\s+','',s.replace('『','\uf000').replace('』','\uf000'))
checks=[]
with pdfplumber.open(SOURCE) as pdf:
 for q in bank:
  n=q['number'];p=pdf.pages[(n-1)//2];side=(n-1)%2
  text=p.crop((side*p.width/2,43,(side+1)*p.width/2,p.height-15)).extract_text()
  text=text[text.index(str(n)+'.')+len(str(n))+1:].strip()
  prompt,tail=text.split('?',1);body,options=tail.split('①',1)
  assert norm(prompt+'?')==norm(q['prompt']),(n,'prompt')
  # Only the two visually confirmed empty boxes are represented with □.
  body_in_app=q['body'].replace('□','') if n in [9,10] else q['body']
  assert norm(body)==norm(body_in_app),(n,'body')
  choices=re.split(r'[①②③④⑤]\s*','①'+options)[1:]
  assert len(choices)==len(q['choices'])==5
  for i,(a,b) in enumerate(zip(choices,q['choices']),1):
   assert norm(a)==norm(b),(n,'choice',i)
  assert len(q['optionReasons'])==5 and len(q['steps'])>=3
  assert all(len(x)>20 for x in q['optionReasons'])
  assert '\u2060' not in json.dumps(q,ensure_ascii=False)
  assert '\uf000' not in json.dumps(q,ensure_ascii=False)
  for phrase in q.get('underlines',[]):assert q['body'].count(phrase)==1
  checks.append({'number':n,'promptExactIgnoringLayout':True,'bodyExactIgnoringLayoutAndBlankGlyph':True,'choicesCompared':5})
with pdfplumber.open(KEY) as pdf:
 text=pdf.pages[0].extract_text()
 assert '언어논리' in text and '사책형' in text and '2024년도' in text
 answers={int(m[1]):int(m[2]) for m in re.finditer(r'(?m)^(\d+) ([1-5])(?: \d+ [1-5])?$',text)}
 for q in bank:assert q['answer']==answers[q['number']],q['number']
pre=json.loads((ART/'pre-answer-review.json').read_text(encoding='utf-8'))
# Enumerate four disjoint atoms A∩B, A\B, B\A, neither with exact arithmetic.
# Include zero intersections and zero complements; division by zero rejects a candidate.
valid=[True]*5;cases={'sameEvents':0,'strictIntersection':0};counterexamples={}
for total in range(2,13):
 for a in range(total+1):
  for b in range(total-a+1):
   for c in range(total-a-b+1):
    d=total-a-b-c;I=F(a,total);U=F(a+b+c,total);H=1-I
    if U==0:continue
    if b==c==0:kind='sameEvents';expected=lambda v:v==1
    else:kind='strictIntersection';expected=lambda v:v is not None and 0<=v<1
    cases[kind]+=1
    ratios=[(U,I),(I,U),(H,I),(I,H),(H,U)]
    for index,(num,den) in enumerate(ratios):
     value=num/den if den else None
     okay=value is not None and expected(value)
     if not okay:
      valid[index]=False
      counterexamples.setdefault(str(index+1),{'case':kind,'atoms':[a,b,c,d],'denominator':total,'ratio':str(value)})
assert valid==[False,True,False,False,False],valid
before=json.loads((ROOT/'artifacts/psat_sets_20261028/content-before.json').read_text(encoding='utf-8'))
from psat_legacy_guard import verify_legacy_assets
legacy_review=verify_legacy_assets(ROOT,before)
report={'status':'PASS','bank':str(BANK.relative_to(ROOT)),'questionCount':len(bank),'transcription':checks,'officialFinalAnswersCompared':len(bank),'sourceSha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'finalKeySha256':hashlib.sha256(KEY.read_bytes()).hexdigest(),'probabilityQuestion10':{'survivingOption':2,'cases':cases,'counterexamples':counterexamples},'legacyPreservation':legacy_review,'limits':'Mechanical verification plus recorded self-review; not independent expert approval or a zero-error guarantee.'}
(ART/'content-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ['transcription']},ensure_ascii=False,indent=2))
