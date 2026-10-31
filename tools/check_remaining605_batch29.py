import re
from itertools import product,permutations
from fractions import Fraction as F
import pdfplumber
import review_remaining605 as r
b=r.folder(29);rows=r.read(b/'revealed-current.json');sources={x['id']:x for x in r.read(b/'blind-source.json')};own={x['id']:x for x in r.read(b/'own-solves.json')}
tables={
 ('2026-07-18',16):(['使用','使用'],[['게임','500'],['동영상 시청','200'],['동영상 촬영','120']],3,r'사용 내역 사용 전류\(mA\).*?동영상 촬영 120'),
 ('2026-07-18',17):(['제과점','집과 제과점의 거리(km)','쿠키 1개당 단백질 함량(g)','쿠키 1개당 가격(원)'],[['A','2.0','3.0','3,000'],['B','2.5','6.5','7,000'],['C','3.0','6.0','5,000'],['D','2.0','5.0','5,000'],['E','1.5','4.5','6,500']],6,r'집과 제과점의 쿠키 1개당 쿠키 1개당.*?E 1.5 4.5 6,500'),
 ('2026-07-18',18):(['구분','가중치','A회사','B회사','C회사','D회사','E회사'],[['근무시간','4','4점','2점','2점','5점','5점'],['급여','4','3점','4점','5점','3점','2점'],['복지혜택','3','4점','4점','3점','4점','3점'],['인지도','2','2점','5점','4점','3점','1점'],['재택근무','3','가능','가능','불가능','불가능','가능']],0,r'구분 가중치 A회사 B회사 C회사 D회사 E회사.*?재택근무 3 가능 가능 불가능 불가능 가능'),
 ('2026-07-18',20):(['구분','A','B','C'],[['통행료(만 달러)','700','350','900'],['항해기간(일)','30','10','30'],['쇄빙선 이용료(만 달러)','200','400','600']],5,r'구분 A B C\n통행료.*?쇄빙선 이용료\(만 달러\) 200 400 600'),
 ('2026-07-18',22):(['문서 종류','1건당 중요도(점)','1건당 크기(MB)','건수'],[['가','8','12','12'],['나','5','8','18'],['다','3','3','24'],['라','3','4','32']],1,r'문서 종류 1건당 중요도\(점\) 1건당 크기\(MB\) 건수.*?라 3 4 32'),
 ('2026-07-18',23):(['구분','A','B','C','D'],[['A','－','60','70','20'],['B','60','－','35','35'],['C','70','35','－','70'],['D','20','35','70','－']],2,r'\(단위: km\)\n구분 A B C D.*?D 20 35 70 －'),
 ('2026-03-07',13):(['의원실','사전질의 개수','의원실','사전질의 개수'],[['가','4','바','0'],['나','2','사','10'],['다','0','아','5'],['라','0','자','0'],['마','1','차','4']],1,r'의원실 사전질의 개수 의원실 사전질의 개수.*?마 1 차 4')}
tables[('2026-07-18',16)]=(['사용 내역','사용 전류(mA)'],*tables[('2026-07-18',16)][1:])
def norm(s):return re.sub(r'[\s①②③④⑤]','',s).replace('²','2')
checks=[]
for row in rows:
 q=row['question'];m=sources[q['id']];native=re.sub(r'책형 \d+쪽','',m['sourceText'])
 if q['number']==20:
  native=re.sub(r'^\[19.*?\]\s*다음 글을 읽고 물음에 답하시오\.','',native,flags=re.S)
  common,tail=re.split(r'20[.]\s+',native,maxsplit=1)
  prompt,situation=tail.split('<상 황>',1);native=prompt+common+'<상 황>'+situation
 else:native=re.sub(r'^.*?\b'+str(q['number'])+r'[.]\s*','',native,count=1,flags=re.S)
 k=(q['examDate'],q['number'])
 if k in tables:
  cols,trs,after,pattern=tables[k];assert len(q['tables'])==1
  t=q['tables'][0];assert (t['columns'],t['rows'],t['afterParagraph'])==(cols,trs,after)
  native,n=re.subn(pattern,'',native,count=1,flags=re.S);assert n==1
 a,z=norm(native),norm(q['prompt']+q['body']+''.join(q['choices']))
 if a!=z:
  i=next((i for i,(u,v) in enumerate(zip(a,z)) if u!=v),min(len(a),len(z)));raise AssertionError((q['id'],i,a[max(0,i-20):i+100],z[max(0,i-20):i+100]))
 with pdfplumber.open(r.ROOT/row['officialKey']) as pdf:
  pi,text=next((i+1,p.extract_text()) for i,p in enumerate(pdf.pages) if '영역 상황판단' in (p.extract_text() or ''))
 assert q['examDate'][:4] in text and f"책형 {q['book']}" in text.replace('㉯','나')
 answers={}
 for line in text.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
   v=list(map(int,line.split()));answers.update(zip(v[::2],v[1::2]))
 assert answers[q['number']]==q['answer']==own[q['id']]['answer']
 checks.append(dict(id=q['id'],nativeAndChoices=True,nativeTableChecked=k in tables,keyPage=pi,key=row['officialKey'],answer=q['answer']))

packs=[];best=-1
for a,c0,c,d in product(range(1,13),range(1,19),range(1,25),range(1,33)):
 volume=12*a+8*c0+3*c+4*d;value=8*a+5*c0+3*c+3*d
 if volume>100:continue
 if value>best:best=value;packs=[]
 if value==best:packs.append([a,c0,c,d])
assert best==91 and packs==[[1,1,24,2]]
distance=[[0,60,70,20],[60,0,35,35],[70,35,0,70],[20,35,70,0]];routes=[]
for seq in permutations([1,2,3]):
 path=(0,)+seq+(0,);split=path.index(2);segments=[sum(distance[path[i]][path[i+1]] for i in range(split)),sum(distance[path[i]][path[i+1]] for i in range(split,4))]
 routes.append(dict(path=''.join('ABCD'[i] for i in path),segments=segments,valid=max(segments)<=90))
assert [x['path'] for x in routes if x['valid']]==['ACBDA','ADBCA']
scoreModels=[]
for z in range(1,15):
 for y in range(z+1,16):
  x=17-y-z
  if x<=y:continue
  for rounds in product(list(permutations([x,y,z])),repeat=3):
   if rounds[-1][1]!=x or [sum(t[i] for t in rounds) for i in range(3)]!=[20,16,15]:continue
   scoreModels.append(dict(X=x,Y=y,Z=z,rounds=rounds))
assert len(scoreModels)==1 and scoreModels[0]['rounds'][1][1]==4
def compositions(n):
 if n==0:yield ();return
 for first in range(1,n+1):
  for tail in compositions(n-first):yield (first,)+tail
def traits(v):return (len(v)>0 and v[0]>=2,len(v)>1 and v[1]>=2,len(v)>=4,len(v)>=3,any(x>=3 for x in v))
scopes=[]
for count in [4,2,1,10,5,4]:
 scope={}
 for v in compositions(count):scope.setdefault(traits(v),v)
 scopes.append(scope)
max12=max41=0;witness=None;valid31count=0
for combo in product(*[list(s) for s in scopes]):
 max12=max(max12,sum(x[0] for x in combo))
 if sum(x[1] for x in combo)==2 and sum(x[2] for x in combo)>max41:
  max41=sum(x[2] for x in combo);witness=[scopes[i][v] for i,v in enumerate(combo)]
 if sum(x[3] for x in combo)==1:
  valid31count+=1;assert any(x[4] for x in combo)
assert max12==5 and max41==4 and valid31count>0
assert (500*2+120*F(50,60)+200*F(7,2))/2000==F(9,10)
assert [sum(w*s for w,s in zip([4,4,3,2,3],v)) for v in [[4,3,4,2,2],[2,4,4,5,2],[2,5,3,4,0],[5,3,4,3,0],[5,2,3,1,2]]]==[50,52,45,50,45]
r.write(b/'source-key-model-checks.json',dict(status='PASS',count=10,checks=checks,knapsack=dict(maximum=best,uniqueComposition=packs[0],count=28),allSixRoutes=routes,allScoreModels=scoreModels,questionNumbering=dict(max12=max12,max41WithExactlyTwo22=max41,witnessByOfficeGaNaMaSaAaCha=witness,threeTopicSingleOfficeImpliesBack3=True),flags=[['K','A','B','C'],['C','A','K','B','D']],battery='1800/2000=0.9',cookieTotals={'B':'19.5','C':'18','D':'20','E':'13.5'},companyTotals=[50,52,45,50,45],routeCosts=[910,870,1860],postDelivery=dict(minimumPositions=[5,10,15,20,25],maximumPositions=[5,-10,15,-20,25],distanceRange=[25,125],hoursDifference=4),limitations='Same-author source/model check, not independent review.'))
print('PASS10source/key/native+7tables;knapsack unique91;6routes;unique score model;all numbering trait combinations.')
