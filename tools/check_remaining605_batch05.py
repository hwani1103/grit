"""Exact batch05 source/key/table comparisons and finite constraint checks."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,combinations
import re,json,math
import pdfplumber
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/psat_remaining605_20261030/batch05'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def norm(s):
 s=s.translate(str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹','0123456789'))
 return re.sub(r'[\s①②③④⑤ㆍ·~～^－−—-]','',s)
items=read(OUT/'revealed-current.json');source={x['id']:x for x in read(OUT/'blind-source.json')};solves={x['id']:x for x in read(OUT/'own-solves.json')};checks=[]
tables={
 'kr-mpm-2024-07-27-psat-s-07':(['색','무게(g)','개수'],[['빨강','30','3'],['노랑','40','2'],['파랑','50','2']]),
 'kr-mpm-2024-07-27-psat-s-12':(['종류','유형','쪽수','중요도'],[['A','보도자료','2','상'],['B','보도자료','34','중'],['C','보도자료','5','하'],['D','설명자료','3','상']]),
 'kr-mpm-2024-07-27-psat-s-20':(['단체','인원(명)','사업분야','운영비(억 원)','사업비(억 원)'],[['A','30','공연','1.8','5.5'],['B','28','교육','2.0','4.0'],['C','27','공연','3.0','3.0'],['D','33','교육','0.8','5.0']])}
for row in items:
 q=row['question'];m=source[q['id']];native=m['sourceText'];mapping=None
 if q['id'] in tables:
  cols,rows=tables[q['id']];assert q['tables'][0]['columns']==cols and q['tables'][0]['rows']==rows
  block=norm(''.join(cols)+''.join(''.join(r) for r in rows));native=norm(native)
  assert native.count(block)==1,(q['id'],block);native=native.replace(block,'',1);mapping='exact independently transcribed rows/headers'
 if q['id']=='kr-mpm-2023-07-22-psat-s-19':
  assert q['tables'][0]['columns']==['구분','금요일 출근시각','금요일 퇴근시각','금요일 비고','토요일 출근시각','토요일 퇴근시각']
  assert q['tables'][0]['rows']==[['甲','08:55','20:00','－','10:30','13:30'],['乙','08:00','19:55','－','－','－'],['丙','09:00','21:30','개인용무시간 (19:00～19:30)','13:00','14:30'],['丁','08:30','23:30','재택근무','－','－'],['戊','07:00','21:30','－','－','－']]
  before,tail=native.split('금요일 토요일',1);table,choices=tail.split('①',1)
  # Native merged two-level header/row text is kept as explicit evidence below.
  assert all(x in norm(table) for x in ['08:55','20:00','19:55','21:30','23:30','19:0019:30','재택근무'])
  native=before+'①'+choices;mapping=table
 if q['number']==9:
  prefix,question=re.split(r'\n9[.]\s*',native,maxsplit=1)
  prefix=re.sub(r'^\[9\s*～\s*10\]\s*다음 글을 읽고 물음에 답하시오[.]\s*','',prefix)
  prefix=re.sub(r'책형\s*5쪽','',prefix)
  stored_prefix,look=q['body'].split('<보기>',1)
  assert norm(prefix)==norm(stored_prefix),(q['id'],'shared passage including2^8 and2^100')
  a,b=norm(question),norm(q['prompt']+'<보기>'+look+''.join(q['choices']))
 else:
  native=re.sub(r'^.*?'+str(q['number'])+r'[.]\s*','',native,count=1,flags=re.S)
  a,b=norm(native),norm(q['prompt']+q['body']+''.join(q['choices']))
 if a!=b:
  i=next((i for i,(x,y) in enumerate(zip(a,b)) if x!=y),min(len(a),len(b)))
  raise AssertionError((q['id'],i,a[max(0,i-30):i+90],b[max(0,i-30):i+90]))
 with pdfplumber.open(ROOT/row['officialKey']) as pdf:
  pi,t=next((i+1,p.extract_text()) for i,p in enumerate(pdf.pages) if '영역 상황판단' in (p.extract_text() or ''))
 assert str(q['examDate'][:4]) in t and any(x in t for x in [f"책형 {q['book']}",'책형 ㉧' if q['book']=='인' else f"책형 {q['book']}"])
 answers={}
 for line in t.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
   z=list(map(int,line.split()));answers.update(zip(z[::2],z[1::2]))
 assert answers[q['number']]==q['answer']==solves[q['id']]['answer']
 checks.append(dict(id=q['id'],source=m['source'],sourcePage=m['page'],key=row['officialKey'],keyPage=pi,answer=answers[q['number']],nativeAndChoicesMatch=True,tableMapping=mapping))

balls=[('R',30)]*3+[('Y',40)]*2+[('B',50)]*2;arrangements=set()
for where in product(range(3),repeat=7):
 groups=[[balls[i] for i,w in enumerate(where) if w==j] for j in range(3)]
 if all(len({c for c,w in group})>=2 and sum(w for c,w in group)<=100 for group in groups):
  arrangements.add(tuple(sorted(tuple(sorted(c for c,w in group)) for group in groups)))
assert arrangements=={(('B','R'),('B','Y'),('R','R','Y'))}
rankings=[]
for c in combinations([1,3,4,6,7,9,10],3):
 a=sorted(set([1,3,4,6,7,9,10])-set(c))
 if max(c)<min(a):rankings.append(dict(A=a,B=[2,5,8],C=c))
assert len(rankings)==1 and rankings[0]['A']==[6,7,9,10]
menu=[]
# True = can access; enumerate all16 bits without assuming unmentioned menu.
for flat in product([False,True],repeat=16):
 a,b,c,d=[flat[i:i+4] for i in range(0,16,4)]
 if all(not all(row) for row in [a,b,c,d]) and sum(not x for x in a)==2 and not a[2] and all(all(row[i] for row in [b,c,d]) for i in range(4) if not a[i]) and all((c[i] and d[i]) or not b[i] for i in range(4)) and c[3] and not d[1] and c[1]:menu.append([a,b,c,d])
assert len(menu)==2
for a,b,c,d in menu:assert a==(True,True,False,False) and b==(False,False,True,True) and c==(False,True,True,True) and d[2] and d[3]
docs=[('보도자료',2,'상'),('보도자료',34,'중'),('보도자료',5,'하'),('설명자료',3,'상')]
sheets=[math.ceil(pages/((1 if kind=='보도자료' and imp=='상' else 2)*(2 if imp=='하' else 1))) for kind,pages,imp in docs]
assert sheets==[2,17,2,2] and sum(sheets)==23
groups={'A':(30,'공연',F('1.8'),F('5.5')),'B':(28,'교육',F('2.0'),F('4.0')),'C':(27,'공연',F('3.0'),F('3.0')),'D':(33,'교육',F('.8'),F('5.0'))}
eligible=sorted([k for k,(n,t,o,b) in groups.items() if n<30 or o<1],key=lambda k:groups[k][0],reverse=True);assert eligible==['D','B','C']
remaining=F(4);paid={}
for k in eligible:
 n,t,o,b=groups[k];requested=o*(F('.2') if t=='공연' else F('.5'))+b*(F('.5') if t=='공연' else F('.2'))
 paid[k]=min(remaining,requested);remaining-=paid[k]
assert paid=={'D':F('1.4'),'B':F('1.8'),'C':F('.8')} and max(paid,key=paid.get)=='B'
overtime={'甲':min(5+120,240)+min(180,120),'乙':min(60+115,240),'丙':min(210-30,240)+min(90,120),'丁':0,'戊':min(120+210,240)}
assert overtime=={'甲':245,'乙':175,'丙':270,'丁':0,'戊':240}
assert (240+220)/2==230 and 230+180-170==240 and 230+170-180==220
result=dict(status='PASS',sourceAndKeys=checks,ballUniqueUnlabelledArrangement=[list(map(list,a)) for a in arrangements],rankings=rankings,menuAllSolutions=menu,requiredSheets=sheets,budgetPayments={k:str(v) for k,v in paid.items()},overtimeMinutes=overtime,
 qualitativeChecks={'s09':'Definitions:ㄱtrueㄴfalseㄷfalseㄹtrue, not current security advice. Source exponents8/100 visually confirmed.', 's11':'firstarticle4proviso+1mandatory revoke; thirdarticle2promote; institute facilities; state-only establish vs state/local support; private persons included.', 's13':'Jon beforeThor;grandfather first name not patronym;sex suffix differs;no patronym-only address.'},
 limitations='Same-author source comparisons and models, not independent expertise or real-device validation.')
(OUT/'source-key-model-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PASS10 direct source/key checks;4native tables;2187 ball,65536menu,35ranking cases;rounding/budget/time models.')
