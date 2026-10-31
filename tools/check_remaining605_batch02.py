"""Batch02: direct PDF keys/transcription, table rows, and independent arithmetic."""
from pathlib import Path
from itertools import product
import json
import re
import pdfplumber

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts/psat_remaining605_20261030/batch02'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
norm=lambda s:re.sub(r'[\s①②③④⑤·ㆍ․]','',s)
targets=read(ROOT/'artifacts/psat_remaining605_20261030/preparation/targets605.json')['batches'][1]['questions']
sources={q['id']:q['sourceText'] for q in read(OUT/'blind-source.json')}
revealed={q['question']['id']:q for q in read(OUT/'revealed-current.json')}
solves={q['id']:q for q in read(OUT/'own-solves.json')}
checks=[]
for row in targets:
 q=next(q for q in read(ROOT/row['file']) if q['id']==row['id'])
 src=re.sub(r'^책형\s*\d+쪽\s*','',sources[q['id']]);src=re.sub(r'^상황판단영역\s*','',src);src=re.sub(r'^\d+\.\s*','',src);src=norm(src)
 table_proof=[]
 for table in q.get('tables',[]):
  rows=table['rows'];rowtext=''.join(''.join(r) for r in rows)
  assert all(norm(''.join(r)) in src.replace(':','') for r in rows),q['id']
  if q['id']=='2023-07-22-s-08':
   block='직전과세년도소득최근금융소득군복무이름나이근로소득사업소득종합과세해당년도기간'+norm(rowtext)
   assert table['columns']==['이름','나이','근로소득','사업소득','최근 금융소득 종합과세 해당년도','군복무기간']
  elif q['id']=='2023-07-22-s-13':block='구분착한일횟수울음횟수'+norm(rowtext)
  elif q['id']=='kr-mpm-2024-07-27-psat-s-06':block=norm(''.join(r[0]+':'+r[1] for r in rows))
  else:raise AssertionError('Review new table mapping explicitly')
  assert src.count(block)==1,(q['id'],'whole source table block')
  src=src.replace(block,'',1)
  table_proof.append(dict(columns=table['columns'],rows=rows,sourceRowMatch=True))
 assert src==norm(q['prompt']+q['body']+''.join(q['choices'])),(q['id'],'source body/choice mismatch')
 key=revealed[q['id']]['officialKey']
 with pdfplumber.open(ROOT/key) as pdf:
  pg,text=next((i+1,p.extract_text()) for i,p in enumerate(pdf.pages) if f"영역 {q['subject']}" in (p.extract_text() or ''))
 assert ('2023' if q['id'].startswith('2023') else '2024') in text and f"책형 {q['book']}" in text
 answers={}
 for line in text.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
   v=list(map(int,line.split()));answers.update(zip(v[::2],v[1::2]))
 assert len(answers)==25 and answers[q['number']]==solves[q['id']]['answer']==q['answer']
 checks.append(dict(id=q['id'],keyPdf=key,keyPage=pg,answer=answers[q['number']],sourceTextMatch=True,tables=table_proof))

santa=[]
for x in range(1,16):
 points=[15-3*x,15-2*x,10-3*x,5,5-3*x]
 counts=[sum(p>=10 for p in points),sum(0<=p<10 for p in points),sum(p<0 for p in points)]
 santa.append(dict(x=x,points=points,counts=counts))
assert [v['x'] for v in santa if v['counts']==[1,3,1]]==[2]
assert santa[5]['points'][3]>santa[5]['points'][1]  # counterexample to old universal maximum claim
reports=[]
for p in range(1,1001):
 if 1000%p:continue
 remaining=1000//p
 for m in range(2,remaining+1):
  if remaining%m==0 and remaining//m>20:reports.append(dict(pages=p,days=remaining//m,executives=m))
assert max(x['pages'] for x in reports)==20
digits=[]
for a,b,c,d,e in product(range(10),repeat=5):
 numbers=[10000*a+5701,84098+100*b,83004+100*c+10*d,10000*e+6715]
 if sum(numbers)==199998:digits.append(dict(digits=[a,b,c,d,e],sum=a+b+c+d+e))
assert digits and {x['sum'] for x in digits}=={14}
eligibility=[]
for name,age,wage,business,finance,service in [('甲',20,0,0,None,0),('乙',36,0,5000,None,0),('丙',29,3500,1000,2022,2),('丁',35,4500,0,2020,2),('戊',27,4000,1500,2021,0)]:
 ok=19<=age-service<=34 and 0<wage+business<=5000 and finance not in [2021,2022]
 eligibility.append(dict(name=name,adjustedAge=age-service,income=wage+business,eligible=ok))
assert [x['name'] for x in eligibility if x['eligible']]==['丁']
result=dict(status='PASS',officialKeysAndSourceChecks=checks,santa=santa,
            santaCounterexampleToOldPremise={'x':6,'乙':3,'丁':5},
            santaBoundProof='For positive x,丙<10,丁=5,戊<10;only甲/乙 can reach A,乙>=甲,so A existence implies15-2x>=10. This is not a universal maximum among all5.',
            reportPossibilities=reports,erasedDigitsSolutions=digits,eligibility=eligibility,
            limitations='Source/table and arithmetic checks; legal-reading claims judged solely by exam text, not current external law.')
(OUT/'source-key-model-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PASS:10 direct PDF keys/texts,3 source tables,positive-coefficient classifications,integer report cases,100000 digit assignments and5 eligibility rows.')
