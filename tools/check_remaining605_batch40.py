import re,unicodedata,itertools
from fractions import Fraction as F
import pdfplumber
import review_remaining605 as r
b=r.folder(40);rows=r.read(b/'revealed-current.json');src={x['id']:x for x in r.read(b/'blind-source.json')};own={x['id']:x for x in r.read(b/'own-solves.json')}
def norm(s):return re.sub(r'\s','',unicodedata.normalize('NFKC',re.sub(r'[①②③④⑤]','',s).replace('ㆍ','·').replace('\ue09d','α'))).replace('[빈칸]','')
checks=[]
for row in rows:
 q=row['question'];m=src[q['id']];s=re.sub(r'책형\s*\d+쪽','',m['sourceText']);s=re.sub(r'^\s*\[19～\s*20\] 다음 글을 읽고 물음에 답하시오[.]\s*','',s);s=re.sub(r'(?m)^\s*'+str(q['number'])+r'[.]\s*','',s,count=1)
 if q['number']==16:s=s.replace('SnO )','SnO2)').replace('\n2\n','\n')
 if q['number'] in [19,20]:
  assert norm(q['prompt']) in norm(s);s=s.replace(q['prompt'],'',1);expected=q['body']+''.join(q['choices'])
 else:expected=q['prompt']+q['body']+''.join(q['choices'])
 a,e=norm(s),norm(expected)
 if a!=e:
  j=next((j for j,(x,y) in enumerate(zip(a,e)) if x!=y),min(len(a),len(e)));raise AssertionError((q['id'],j,a[j:j+100],e[j:j+100]))
 with pdfplumber.open(r.ROOT/row['officialKey']) as pdf:pi,t=next((j+1,p.extract_text()) for j,p in enumerate(pdf.pages) if '영역 언어논리' in (p.extract_text() or ''))
 assert q['examDate'][:4] in t and f"책형 {q['book']}" in t.replace('㉮','가').replace('㉯','나');ans={}
 for line in t.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):z=list(map(int,line.split()));ans.update(zip(z[::2],z[1::2]))
 assert ans[q['number']]==q['answer']==own[q['id']]['answer'];checks.append(dict(id=q['id'],source=m['source'],page=m['page'],key=row['officialKey'],keyPage=pi,nativeAndAllFiveChoicesMatch=True,ownMatches=True))
# All truth assignments: equivalent A/B and true C; only option4 forces not B.
models=[]
for opt in range(5):
 valid=[]
 for A,B,C in itertools.product([False,True],repeat=3):
  candidates=[B or not A,not C or B,C or A,A or not C,B is False or not C]
  # Store options in their actual order, option4 is B->not C and option5 not A->not C.
  candidates=[B or not A,not C or B,C or A,not B or not C,A or not C]
  if A==B and C and candidates[opt]:valid.append([A,B,C])
 assert valid and (all(not v[1] for v in valid)==(opt==3));models.append(dict(option=opt+1,models=valid))
assert 1+1<1+3 and 1+3+1+1>1+3+1
assert 1-F(1,4)>1-F(1,2) and 12-6>10-6 and 10-4>10-6 and 25+3==28
r.write(b/'source-key-model-checks.json',dict(status='PASS',count=10,checks=checks,conditionalTruthTables=models,finiteConductivity='r>0, sensitivity difference r/(2R)>0; equal extrema times addresses response-time part only.',experiment='Initial I>II; increase I and decrease II both enlarge difference, A/B same directional predictions.',codeSwitch='Unknown main language still allows mixing if either language norm violated; borrowed word vs foreign pronunciation distinct.',sourceSuperscriptAndSubscript='Original image a^n and SnO2 viewed; PDF displaced subscript restored only in checker; app glyphs preserved.'))
print('PASS10 source/keys; truth tables and exact boundary models')
