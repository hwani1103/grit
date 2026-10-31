"""Source/answer/finite-case audit. Semantic and visual reviews are separate evidence."""
from pathlib import Path
from itertools import product
import json,re,hashlib
import pdfplumber
R=Path(__file__).resolve().parents[1]
A=R/'artifacts/psat600_20261028/situation02_2024'
S=R/'artifacts/psat600_20261028/sources/4555/pdf/상황판단(사).pdf'
K=R/'artifacts/psat600_20261028/sources/4564/BBSMSTR_000000000138_4564_1.pdf'
B=R/'assets/psat/situation02.json'
if not B.exists():B=A/'authored-situation02.json'
bank=json.loads(B.read_text(encoding='utf-8'))
def norm(s):return re.sub(r'\s+','',s.translate(str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹','0123456789')))
def eq(a,b,label):assert norm(a)==norm(b),(label,norm(a)[:120],norm(b)[:120])
checks=[]
with pdfplumber.open(S) as pdf:
 shared=pdf.pages[4].crop((0,43,364,1016)).extract_text().split('\n',1)[1]
 right=pdf.pages[4].crop((364,43,728,1016)).extract_text()
 for q in bank:
  n=q['number']
  if n<=8:
   p=pdf.pages[(n-1)//2];side=(n-1)%2
   raw=p.crop((364*side,43,364*(side+1),1016)).extract_text()
   raw=raw[raw.index(str(n)+'.')+len(str(n))+1:]
  else:
   raw=right.split('\n10.')[0][2:] if n==9 else right.split('\n10.')[1]
  prompt,tail=raw.split('?',1);cut=tail.rindex('\n① ')
  body,choices=tail[:cut],re.split('[①②③④⑤] ',tail[cut:])[1:]
  eq(prompt+'?',q['prompt'],(n,'prompt'))
  if n==4:
   body=body[:body.index('종전 대법원 판례 최근 대법원 판례')]
   choices=['종전: '+c.split()[0]+' / 최근: '+c.split()[1] for c in choices]
  if n==6:
   body=body[:body.index('甲:')]
   rawrows=re.findall(r'([甲乙丙丁]): ([^\n]+)',tail[:cut])
   assert len(rawrows)==4
   for (name,digits),row in zip(rawrows,q['tables'][0]['rows']):eq(name+digits,''.join(row),(n,'digits'))
  if n==7:
   body=body[:body.index('色')] if '色' in body else body
   body=body[:body.index('색 무게(g)')]+body[body.index('<조 건>'):]
  if n==8:
   # Remove precisely the two source table regions. Text outside remains in order.
   p=pdf.pages[3]
   region=p.crop((364,43,728,1016))
   boxes=[t.bbox for t in p.find_tables() if t.bbox[0]>400]
   region=region.filter(lambda o:not any(x0<=o.get('x0',-1) and o.get('x1',9999)<=x1 and y0<=o.get('top',-1) and o.get('bottom',9999)<=y1 for x0,y0,x1,y1 in boxes))
   rt=region.extract_text();body=rt.split('?',1)[1].split('\n① ',1)[0]
  if n>=9:body=shared+'\n\n'+body
  eq(body,q['body'],(n,'full-body-excluding-separately-compared-tables'))
  assert len(choices)==5
  for i,(x,y) in enumerate(zip(choices,q['choices']),1):eq(x,y,(n,'choice',i))
  assert len(q['steps'])>=3 and len(q['optionReasons'])==5
  assert all(len(s)>20 for s in q['optionReasons'])
  assert not any(c in json.dumps(q,ensure_ascii=False) for c in ['\u2060','\uf000'])
  checks.append({'number':n,'promptBodyAndFiveChoicesCompared':True})
 tables=[t.extract() for t in pdf.pages[3].find_tables() if t.bbox[1]>40]
 for source,app in [(tables[0],bank[6]['tables'][0]),(tables[2],bank[7]['tables'][1])]:
  eq(''.join(source[0]),''.join(app['columns']),'table headings')
  for row,out in zip(source[1:],app['rows']):eq(''.join(row),''.join(out),'table cells')
 source=tables[1];out=bank[7]['tables'][0]
 eq(''.join(x or '' for x in source[0]).replace('현황',''),''.join(out['columns']),'work headings')
 for row,outrow in zip(source[1:],out['rows']):
  eq(''.join(row),''.join(outrow).replace(', ',''),'work data')
with pdfplumber.open(K) as pdf:
 text=pdf.pages[1].extract_text()
 assert '상황판단' in text and '사책형' in text and '2024년도' in text
 key={int(m[1]):int(m[2]) for m in re.finditer(r'(?m)^(\d+) ([1-5])(?: \d+ [1-5])?$',text)}
 for q in bank:assert q['answer']==key[q['number']],q['number']
pre=json.loads((A/'pre-answer-review.json').read_text(encoding='utf-8'))
assert pre['proposedAnswers']==[q['answer'] for q in bank]
# All decimal assignments, including zero in leading blank; both conventions give same sum.
solutions=[]
for a,b,c,d,e in product(range(10),repeat=5):
 if 10000*a+5701+84098+100*b+83004+100*c+10*d+10000*e+6715==199998:
  solutions.append((a,b,c,d,e))
assert solutions and {sum(x) for x in solutions}=={14}
assert {sum(x) for x in solutions if x[0]>0 and x[4]>0}=={14}
# Enumerate color-count triples for each labeled box, enforcing inventory and all constraints.
possible=[x for x in product(range(4),range(3),range(3)) if sum(v>0 for v in x)>=2 and sum(v*w for v,w in zip(x,[30,40,50]))<=100]
arrangements=[]
for boxes in product(possible,repeat=3):
 if tuple(map(sum,zip(*boxes)))!=(3,2,2):continue
 weights=[sum(v*w for v,w in zip(x,[30,40,50])) for x in boxes]
 statements=[all(x[0]<=1 for x in boxes),len(set(weights))==3,all(not(x[0] and x[2]) for x in boxes),all(x[2]>0 for x,w in zip(boxes,weights) if w==min(weights))]
 assert statements==[False,True,False,True]
 arrangements.append(boxes)
assert len(arrangements)==6
# Score from source-verified table cells, using the actual year to find latest work.
scores={}
for name,base,staff,genre,history in bank[7]['tables'][0]['rows']:
 works=re.findall(r'(성공|실패)\((\d{4})\)',history);assert len(works)==2
 latest=max(works,key=lambda x:int(x[1]))[0]
 scores[name]=int(base)-10*(int(staff)<50)+10*(genre=='판타지')+10*all(v=='성공' for v,y in works)-10*(latest=='실패')
assert scores=={'성묘':70,'서울의 겨울':65,'만날 결심':75,'빅 포레스트':75}
assert [k for k,v in scores.items() if v>=75]==bank[7]['choices'][3].split(', ')
# Bit boundary: the previous upgrade is insufficient, the chosen upgrade meets exactly.
assert 2**56*2**3 < 2**60 == 2**56*2**4
assert 1000000+4*100000==int(bank[9]['choices'][2].replace(',',''))
for n in [8,9]:assert '2⁸' in bank[n]['body'] and '2¹⁰⁰' in bank[n]['body']
assert '2⁵⁶개의 키' in bank[9]['body']
legacy=json.loads((R/'artifacts/psat_sets_20261028/content-before.json').read_text(encoding='utf-8'))
from psat_legacy_guard import verify_legacy_assets
legacy_review=verify_legacy_assets(R,legacy)
report={'status':'PASS','bank':str(B.relative_to(R)),'questions':checks,'officialFinalAnswersMatched':10,'preKeySolveMatched':10,'tableCellsCompared':True,'q6AllAssignments':len(solutions),'q6PositiveLeadingAssignments':sum(x[0]>0 and x[4]>0 for x in solutions),'q7FeasibleLabeledArrangements':len(arrangements),'q8Scores':scores,'q10MinimumPrice':1400000,'sourceSha256':hashlib.sha256(S.read_bytes()).hexdigest(),'finalKeySha256':hashlib.sha256(K.read_bytes()).hexdigest(),'legacyPreservation':legacy_review,'limits':'Includes visual review and self-review; not independent expert approval or a zero-error guarantee.'}
(A/'content-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='questions'},ensure_ascii=False,indent=2))
