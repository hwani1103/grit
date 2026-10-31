import re
from itertools import product,permutations
from fractions import Fraction as F
import pdfplumber
import review_remaining605 as r
b=r.folder(22);rows=r.read(b/'revealed-current.json');sources={x['id']:x for x in r.read(b/'blind-source.json')};own={x['id']:x for x in r.read(b/'own-solves.json')}
norm=lambda s:re.sub(r'[\s①②③④⑤·ㆍ․/\uf000\uf001]','',s)
checks=[]
for row in rows:
 q=row['question'];m=sources[q['id']];native=m['sourceText'];table=None
 if m['sharedPassageRange']:
  common,native=re.split(r'\n21[.]\s*',native,maxsplit=1)
  common=re.sub(r'^\[21\s*[～~] ?22\]\s*다음 글을 읽고 물음에 답하시오[.]\s*','',common)
  common=re.sub(r'책형\s*\d+쪽\s*','',common)
  assert norm(common)==norm(q['body']),(q['id'],'shared source')
  expected=q['prompt']+''.join(q['choices'])
 else:
  native=re.sub(r'^.*?\b'+str(q['number'])+r'[.]\s*','',native,count=1,flags=re.S)
  if q['number']==23:
   native,n=re.subn(r'<표> 투표율 분석 결과.*?(?=<보 기>)','',native,count=1,flags=re.S);assert n==1
   table=q['tables'][0]
   assert table==dict(caption='투표율 분석 결과',columns=['지역 / 항목','투표율 수준','A','B'],rows=[['(가)','㉠','㉡','㉢'],['(나)','㉣','㉤','㉥']],afterParagraph=3)
  expected=q['prompt']+q['body']+''.join(q['choices'])
 a,z=norm(native),norm(expected)
 if a!=z:
  i=next((i for i,(u,v) in enumerate(zip(a,z)) if u!=v),min(len(a),len(z)))
  raise AssertionError((q['id'],i,a[max(0,i-20):i+100],z[max(0,i-20):i+100]))
 with pdfplumber.open(r.ROOT/row['officialKey']) as pdf:
  pi,text=next((i+1,p.extract_text()) for i,p in enumerate(pdf.pages) if '영역 언어논리' in (p.extract_text() or ''))
 assert q['examDate'][:4] in text and f"책형 {q['book']}" in text
 answers={}
 for line in text.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
   v=list(map(int,line.split()));answers.update(zip(v[::2],v[1::2]))
 assert answers[q['number']]==q['answer']==own[q['id']]['answer']
 checks.append(dict(id=q['id'],source=m['source'],sourcePage=m['page'],fullNativeAndFiveChoicesMatch=True,table=table,key=row['officialKey'],keyPage=pi,answer=q['answer'],ownAnswerMatches=True))

def underlines(qid,ys):
 m=sources[qid];out=[]
 with pdfplumber.open(r.ROOT/m['source']) as pdf:
  page=pdf.pages[m['page']-1]
  for y in ys:
   lines=[ln for ln in page.lines if abs(ln['top']-y)<.01 and abs(ln['top']-ln['bottom'])<.1];assert len(lines)==1
   ln=lines[0]
   out.append(''.join(c['text'] for c in page.chars if ln['x0']<=(c['x0']+c['x1'])/2<=ln['x1'] and ln['top']-10<c['bottom']<ln['top']+2))
 return out
chain=underlines('kr-mpm-2025-11-15-psat-l-14',[314.048,613.348])
assert list(map(norm,chain))==['A－연쇄','B－연쇄']
causal=underlines('kr-mpm-2025-11-15-psat-l-21',[108.28,126.986,370.167,837.822])
assert norm(''.join(causal[:2]))==norm('원인은 그것이 없었다면 발생하지 않았을 사건인 결과를 발생하게 한다')
assert list(map(norm,causal[2:]))==list(map(norm,['초기 확률 인과 이론','수정된 확률 인과 이론']))
r.write(b/'source-underline-boundaries.json',dict(status='source_confirmed',chain=chain,causal=causal,correction='l14 circled labels excluded; l21 existing three spans already exact. Original PDF stroke/glyph centers and page images checked.'))
mountains=[]
for s,j,k,bb in product([False,True],repeat=4):
 if (not s or j) and (not j or bb) and not(j and bb) and (not k or not s):mountains.append([s,j,k,bb])
assert len(mountains)==4 and max(map(sum,mountains))==2
trips=[]
for g,n,d,l,m in product([False,True],repeat=5):
 if (g!=n) and (g or d or l) and (n or d) and (not d or not g) and (not l or not m) and m:trips.append([g,n,d,l,m])
assert trips==[[False,True,True,False,True]]
interviews=[]
for people in permutations('갑을병정'):
 if people.index('갑')<=people.index('병'):continue
 for films in permutations('ABCD'):
  if films.index('A')!=people.index('정')+1 or films.index('B')>=films.index('C'):continue
  if len({0,people.index('병'),people.index('정'),films.index('D')})!=4:continue
  interviews.append(dict(people=list(people),films=list(films)))
assert interviews==[dict(people=list('을정병갑'),films=list('BCAD'))]
election=[dict(ga=['저','저','고'],na=['저','고','고'],A='변화'),dict(ga=['저','고','저'],na=['저','고','고'],A='성차')]
truth=[]
for v in election:
 ga,na=v['ga'],v['na'];truth.append([ga[0]==na[0],not(ga[1]!=na[1]) or ga[2]==na[0],na[0]!=na[2]])
assert truth==[[True,False,True],[True,True,True]]
assert F(1,5)!=1-F(1,5)
r.write(b/'source-key-model-checks.json',dict(status='PASS',count=10,officialSourceKeys=checks,ownFirstPassMatches=10,mountainModels=mountains,tripModels=trips,interviewModels=interviews,electionModels=election,electionTruthByModel=truth,qualitative={'l14':'A independence permits .2/.8; B depends on common lastY so same nextY probability.','l15':'All support conclusion; do not invent prognosis for B. Published option4 reason mistakenly names ㄱㄷ instead of selected ㄴㄷ; repair required.','l19':{'predictionsByExperiment':[['A','B'],['A','A'],['B','A']],'observations':['B','B','A'],'truth':[True,False,False]},'l21':'Positive correlation plus time precedence for initial theory; no shielding only in revised theory.','2026l01':'Sukjong silver flask; issuer Yuan under Chungnyeol; reform failure vs actual issuance.','2026l03':'Law plus actual antecedent implies event; why-question alone omits distinguishing structure.'},limitations='Same-author review; separate host, repair and preservation evidence required.'))
print('PASS10 original/key/own solves; 4 mountain models, unique trip/interview, two election layouts, exact underline strokes.')
