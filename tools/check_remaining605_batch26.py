import re
from fractions import Fraction as F
from itertools import product
from functools import lru_cache
import pdfplumber
import review_remaining605 as r
b=r.folder(26);rows=r.read(b/'revealed-current.json');sources={x['id']:x for x in r.read(b/'blind-source.json')};own={x['id']:x for x in r.read(b/'own-solves.json')}
norm=lambda s:re.sub(r'[\s①②③④⑤·ㆍ․/]','',s)
checks=[]
tables={
 '2025-11-15-23':dict(caption='최근 세 학기의 평균 평점',columns=['구분','2학년 2학기','3학년 1학기','3학년 2학기'],rows=[['학기 평균 평점','a','b','c'],['누적 평균 평점','4.0','d','e']],afterParagraph=0),
 '2026-07-18-08':dict(caption='요가 특강 시간표',columns=['구분','월','화','수','목','금'],rows=[['1교시','마하하타 (A)','빈야사 (C)','마하하타 (A)','테라피 (A)','빈야사 (A)'],['2교시','마하하타 (B)','아쉬탕가 (B)','아쉬탕가 (B)','빈야사 (C)','마하하타 (B)'],['3교시','아쉬탕가 (A)','테라피 (B)','테라피 (A)','마하하타 (A)','수업 없음']],afterParagraph=4),
 '2026-07-18-10':dict(caption='지원 기업 정보',columns=['구분','A','B','C','D','E'],rows=[['사업자 등록일','2022. 5. 13.','2019. 11. 27.','2025. 10. 23.','2020. 2. 7.','2019. 3. 29.'],['사업분야','반도체','태양광','조선','AI','태양광'],['매출액(원)','47억','53억','73억','59억','66억'],['자산총액(원)','490억','560억','480억','450억','430억'],['우수기업인증 취득일','2026. 7. 6.','2023. 2. 21.','없음','2024. 5. 14.','2023. 6. 7.']],afterParagraph=6)}
for row in rows:
 q=row['question'];m=sources[q['id']];native=re.sub(r'^.*?\b'+str(q['number'])+r'[.]\s*','',m['sourceText'],count=1,flags=re.S)
 k=q['examDate']+f"-{q['number']:02}"
 if k in tables:
  assert q['tables']==[tables[k]]
  pattern=r'구분 2학년 2학기.*?누적 평균 평점 4.0 d e' if q['number']==23 else r'<시간표>\n구분 월 화 수 목 금.*?(?=①)' if q['number']==8 else r'구분 A B C D E.*?(?=①)'
  native,n=re.subn(pattern,'',native,count=1,flags=re.S);assert n==1
 expected=q['prompt']+q['body']+''.join(q['choices']);a,z=norm(native),norm(expected)
 if a!=z:
  i=next((i for i,(u,v) in enumerate(zip(a,z)) if u!=v),min(len(a),len(z)));raise AssertionError((q['id'],i,a[max(0,i-20):i+80],z[max(0,i-20):i+80]))
 with pdfplumber.open(r.ROOT/row['officialKey']) as pdf:
  pi,text=next((i+1,p.extract_text()) for i,p in enumerate(pdf.pages) if '영역 상황판단' in (p.extract_text() or ''))
 assert q['examDate'][:4] in text and f"책형 {q['book']}" in text
 answers={}
 for line in text.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
   v=list(map(int,line.split()));answers.update(zip(v[::2],v[1::2]))
 assert answers[q['number']]==q['answer']==own[q['id']]['answer']
 checks.append(dict(id=q['id'],source=m['source'],page=m['page'],nativeAndFiveChoices=True,nativeTable=tables.get(k),key=row['officialKey'],keyPage=pi,answer=q['answer'],ownMatches=True))

# Enumerate all permitted schedules, including the absent Friday third period.
days=[[('M','A',1),('M','B',2),('S','A',3)],[('V','C',1),('S','B',2),('T','B',3)],[('M','A',1),('S','B',2),('T','A',3)],[('T','A',1),('V','C',2),('M','A',3)],[('V','A',1),('M','B',2)]]
schedules=[]
for v in product(*days):
 if set(x[1] for x in v)!=set('ABC'):continue
 if any(x[0]=='V' and (i==4 or v[i+1][0]!='T') for i,x in enumerate(v)):continue
 if any(v[i][0]==v[i+1][0]=='M' for i in range(4)):continue
 schedules.append(v)
assert len(schedules)==3
assert [any(any(x[0]=='S' for x in v) for v in schedules),max(sum(x[0]=='M' for x in v) for v in schedules),max(sum(x[2]==2 for x in v) for v in schedules),any(v[2][0]=='M' for v in schedules),max(sum(x[1]=='A' for x in v) for v in schedules)]==[True,2,2,False,3]

@lru_cache(None)
def acorns(i,state,used):
 if i==5:return int(state==(2,2,2,2,2))
 count=0
 for src,dst in product(range(5),repeat=2):
  if src==dst or i in (src,dst):continue
  for amount in range(1,6):
   if used & (1<<amount) or state[src]<amount:continue
   v=list(state);v[src]-=amount;v[dst]+=amount
   count+=acorns(i+1,tuple(v),used|(1<<amount))
 return count
total=acorns(0,(2,2,2,2,2),0);assert total>0
state=(2,2,2,2,2);used=0;witness=[]
for i in range(5):
 found=False
 for src,dst,amount in product(range(5),range(5),range(1,6)):
  if src==dst or i in (src,dst) or used&(1<<amount) or state[src]<amount:continue
  v=list(state);v[src]-=amount;v[dst]+=amount
  if acorns(i+1,tuple(v),used|(1<<amount)):
   witness.append(dict(actor=i+1,source=src+1,destination=dst+1,amount=amount,after=v));state=tuple(v);used|=1<<amount;found=True;break
 assert found
assert witness[0]['amount']+witness[-1]['amount']==3
assert F(19,5)>F(45,12) and 3<F(7,2)
assert F(16,5)>F(17,6) and 0<1
assert 15+6//2+min(17-F(19,2),5)-F(9,2)==F(37,2)
assert (5000+5000+8000)*F(9,10)==16200
r.write(b/'source-key-model-checks.json',dict(status='PASS',count=10,checks=checks,schedules=schedules,acornAllValidTraceCount=total,acornWitness=witness,acornProof='First source starts2; last destination ends2. Positive distinct amounts force endpoints1and2 irrespective of middle trace.',weightedMeanCounterexamples=[dict(previous4Terms='4 each',b=3,c=3.5,d='19/5',e='15/4'),dict(previous4Terms='4 each',b=0,c=1,d='16/5',e='17/6')],holiday='18+5−4.5=18.5',shipping=[5000,5000,8000,16200],companyReasons={'A':['revenue47<60','certification2026-07-06 after reference'], 'B':['assets560>=500'],'C':['shipbuilding excluded','no certification'],'D':['all5 satisfied'],'E':['registration2019-03-29 before2019-07-01']},limitations='Same-author review; legal questions use supplied exam text, not advice about current law.'))
print('PASS10 original/key/own;3 complete schedules;',total,'valid acorn traces, witness',witness)
