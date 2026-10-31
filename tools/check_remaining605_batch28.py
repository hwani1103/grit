import re
from itertools import product
import pdfplumber
import review_remaining605 as r
b=r.folder(28); rows=r.read(b/'revealed-current.json'); sources={x['id']:x for x in r.read(b/'blind-source.json')}; own={x['id']:x for x in r.read(b/'own-solves.json')}
def norm(s):
 return re.sub(r'[\s①②③④⑤\uf000『』]','',s).replace('m²','m2').replace('[빈칸]','')
checks=[]
for row in rows:
 q=row['question'];m=sources[q['id']];native=m['sourceText']
 native=re.sub(r'책형 \d+쪽','',native)
 if q['number']==20:
  native=re.sub(r'^\[19.*?\]\s*다음 글을 읽고 물음에 답하시오\.','',native,flags=re.S)
  head,tail=re.split(r'20[.]\s+',native,maxsplit=1)
  native=tail[:tail.index('①')]+head+tail[tail.index('①'):]
 else:native=re.sub(r'^.*?\b'+str(q['number'])+r'[.]\s*','',native,count=1,flags=re.S)
 if q['number']==17:
  native=native.replace('c ,…,c 으로\n1 n','c(1), …, c(n)으로').replace('c ,…,c 중 일부로 구성된 합산적 행위도 있다.\n1 n','c(1), …, c(n) 중 일부로 구성된 합산적 행위도 있다.')
 expected=q['prompt']+q['body']+''.join(q['choices']);a,z=norm(native),norm(expected)
 if a!=z:
  i=next((i for i,(u,v) in enumerate(zip(a,z)) if u!=v),min(len(a),len(z)));raise AssertionError((q['id'],i,a[max(0,i-20):i+100],z[max(0,i-20):i+100]))
 with pdfplumber.open(r.ROOT/row['officialKey']) as pdf:
  pi,text=next((i+1,p.extract_text()) for i,p in enumerate(pdf.pages) if '영역 언어논리' in (p.extract_text() or ''))
 assert q['examDate'][:4] in text and f"책형 {q['book']}" in text.replace('㉯','나')
 answers={}
 for line in text.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
   v=list(map(int,line.split()));answers.update(zip(v[::2],v[1::2]))
 assert answers[q['number']]==q['answer']==own[q['id']]['answer']
 checks.append(dict(id=q['id'],source=m['source'],page=m['page'],nativeAndFiveChoices=True,key=row['officialKey'],keyPage=pi,answer=q['answer'],ownMatches=True))

# Independent exhaustive relationship matrix, all 2^16 recommendation matrices.
valid=[]
for bits in range(1<<16):
 matrix=[[bool(bits&(1<<(4*i+j))) for j in range(4)] for i in range(4)]
 votes=[sum(matrix[i][j] for i in range(4)) for j in range(4)]
 if votes.count(max(votes))!=1:continue
 winner=votes.index(max(votes));team={winner}|{j for j in range(4) if matrix[winner][j]}
 if 0 in team:continue
 predictions=[(4 in votes,0 not in team),(any(all(x) for x in matrix),matrix[3]==[True,False,False,False]),(all(any(x) for x in matrix),team=={1,2}),(not any(matrix[i][i] for i in range(4)),matrix[0]!=[False,False,True,False])]
 if any(x!=y for x,y in predictions) or sum(x for x,y in predictions)!=2:continue
 truth=[not matrix[0][0],not matrix[1][2],matrix[3][2] and not matrix[2][3]]
 assert truth==[True,False,True]
 valid.append(dict(rows=[[int(x) for x in v] for v in matrix],votes=votes,winner=winner,team=sorted(team),truth=truth))
assert len(valid)==49

# All certificate assignments and all selection pairs, without assuming uniqueness.
credentials=[]
for B,C in product(range(1,8),repeat=2):
 certs=[1,B,C,2,4]
 if sum(x.bit_count()==2 for x in certs)!=1 or B&1 or B&C or C&(2|4):continue
 for hired in product([False,True],repeat=5):
  if sum(hired)!=2 or sum(hired[i] and certs[i].bit_count()==1 for i in range(5))!=1:continue
  if hired[0] and hired[1] or not hired[3] and not hired[0]:continue
  credentials.append(dict(certificates=certs,hired=[i for i in range(5) if hired[i]]))
assert credentials==[dict(certificates=[1,6,1,2,4],hired=[1,3])]
for E,H in [([10,3,3],[1,4,3]),([10,6,3],[1,3,2])]:
 S=[e+h for e,h in zip(E,H)];assert S[0]>S[1]>S[2] and H[0]<min(H[1:])
r.write(b/'source-key-model-checks.json',dict(status='PASS',count=10,checks=checks,recommendationMatrixCount=len(valid),recommendationMatrices=valid,certificateModels=credentials,models={'l14':'P,V true;D,W false single-object countermodel satisfies options2–5 separately but not conclusion. Option1 sends existing witness toW.','l33':'A empty; b:B only; s:Smart only; p:Precision only. All premises and Precision→notSmart hold; B∩Precision empty.','l15':'Necessary conditions: goal→I&V; goal→I; goal→V|M. I-only violatesA; M-only violatesA/B,compatibleC; V-only violatesB,compatibleC.','l16':{'counterexamples':[{'E':[10,3,3],'H':[1,4,3]},{'E':[10,6,3],'H':[1,3,2]}],'weakeningProof':'S_A>S_B>S_C and E_A<E_B<E_C imply H_A>H_B>H_C.'},'l17':'Responsibility→cause, not converse. Individual and aggregate groups remain distinct.','l20':'Challenge the stated human/reconstruction distinction; no claim of proving equal intelligence.','l26':'Intent/context matter; not unrestricted permission to exclude inconvenient data.'},limitations='Same-author formalization, not independent review. Original images manually read for all10.'))
print('PASS10 original/key/own;49 recommendation matrices;unique certificate and hire assignment.')
