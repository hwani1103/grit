from pathlib import Path
import json,re,hashlib,itertools as it,pdfplumber
from PIL import Image
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/situation15';P=R/'assets/psat/situation15.json'
bank=json.loads((P if P.exists() else A/'authored-situation15.json').read_text(encoding='utf-8'));tr=json.loads((A/'source-transcripts.json').read_text(encoding='utf-8'))
assert [(q['examDate'],q['number']) for q in bank]==[('2026-07-18',n) for n in range(17,26)]+[('2026-03-07',13)]
from itertools import product,permutations
from pathlib import Path
import json
out={}
out['cookies']={n:(int((22000-(3000 if 2*d>5 else 0))//p),round(int((22000-(3000 if 2*d>5 else 0))//p)*g,1)) for n,d,g,p in zip('BCDE',[2.5,3,2,1.5],[6.5,6,5,4.5],[7000,5000,5000,6500])}
out['companies']=[sum(a*b for a,b in zip(v,[4,4,3,2,3])) for v in [(4,3,4,2,2),(2,4,4,5,2),(2,5,3,4,0),(5,3,4,3,0),(5,2,3,1,2)]]
states={tuple('ABCDEF')}
for _ in range(5):
 nxt=set()
 for s in states:
  for i in range(5):
   v=list(s);v[i],v[i+1]=v[i+1],v[i];nxt.add(tuple(v))
 states=nxt
out['race5']=[''.join(v) for v in states if v[1]=='D' and v.index('C')<v.index('B') and v.index('A')>=3]
rows=[]
for a,b,c,d in product(range(1,13),range(1,19),range(1,25),range(1,33)):
 if 12*a+8*b+3*c+4*d<=100:rows.append((8*a+5*b+3*c+3*d,a,b,c,d))
m=max(v[0] for v in rows);out['storage']={'max':m,'solutions':[v for v in rows if v[0]==m],'maxByCount':{n:max(v[0] for v in rows if sum(v[1:])==n) for n in range(24,29)}}
dist={tuple(sorted(k)):v for k,v in [('AB',60),('AC',70),('AD',20),('BC',35),('BD',35),('CD',70)]}
routes=[]
for perm in permutations('BCD'):
 r=('A',)+perm+('A',);at=r.index('C');legs=[sum(dist[tuple(sorted((r[i],r[i+1])))] for i in range(x,y)) for x,y in [(0,at),(at,4)]];routes.append((''.join(r),legs,max(legs)<=90))
out['routes']=routes
machines=[]
for a in range(6):
 for b in range(6-a):
  c=5-a-b;need=[max(0,n-a-(b if i<5 else 0)) for i,n in enumerate([3,4,5,5,4,2,1])]
  if max(need)<=c:machines.append((2100*a+2000*b+600*sum(need),a,b,c,need))
out['machines']=sorted(machines)
# All ordered positive compositions of each office's total; signatures contain query labels.
def comps(n):
 if not n:yield ();return
 for x in range(1,n+1):
  for tail in comps(n-x):yield (x,)+tail
flags={n:set((bool(v and v[0]>=2),len(v)>=2 and v[1]>=2,len(v)>=4,len(v)>=3,any(x>=3 for x in v)) for v in comps(n)) for n in [4,2,1,10,5]}
worlds=list(product(*(flags[n] for n in [4,2,1,10,5,4])))
out['grade5s13']={'a_max':max(sum(v[0] for v in w) for w in worlds),'b_max':max(sum(v[2] for v in w) for w in worlds if sum(v[1] for v in w)==2),'c_all':all(any(v[4] for v in w) for w in worlds if sum(v[3] for v in w)==1),'worlds':len(worlds)}

assert out['cookies']=={'B':(3,19.5),'C':(3,18),'D':(4,20),'E':(3,13.5)}
assert out['companies']==[50,52,45,50,45]
assert out['race5']==['CDBAEF']
assert out['storage']['max']==91 and out['storage']['solutions']==[(91,1,1,24,2)]
assert [v[0] for v in out['routes'] if v[2]]==['ACBDA','ADBCA']
assert out['machines'][0][:4]==(9400,2,2,1)
assert out['grade5s13']=={'a_max':5,'b_max':4,'c_all':True,'worlds':17640}
from fractions import Fraction
from math import gcd
assert Fraction(7000,22000)>Fraction(1,4)
assert [350+30*12+200,350+10*12+400,900+30*12+600]==[910,870,1860]
assert [n for n in range(11,16) if n%2==0 and gcd(n,3)==1]==[14]
proof=out
keys={}
for post,date,year,book in [(6016,'2026-07-18','2026','사'),(5982,'2026-03-07','2026','㉯')]:
 with pdfplumber.open(next((R/f'artifacts/psat600_20261028/sources/{post}').glob('*.pdf'))) as pdf:
  t=next(p.extract_text() for p in pdf.pages if '영역 상황판단' in p.extract_text());assert year in t and book in t;k={}
  for line in t.splitlines():
   if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
    v=list(map(int,line.split()));k.update(zip(v[::2],v[1::2]))
  assert len(k)==(40 if post==5982 else 25);keys[date]=k
def norm(s):
 s=re.sub(r'\uf000([^\uf000]+)\uf000',r'『\1』',s)
 return re.sub(r'[\s·․]+','',s.replace('\uf000','『').replace('\uf001','』'))
tableSources=json.loads((A/'table-source-text.json').read_text(encoding='utf-8'))

rawTables={int(k):v for k,v in tableSources.items()}
expectedTables={
17:[(['제과점','집과 제과점의 거리(km)','쿠키 1개당 단백질 함량(g)','쿠키 1개당 가격(원)'],[['A','2.0','3.0','3,000'],['B','2.5','6.5','7,000'],['C','3.0','6.0','5,000'],['D','2.0','5.0','5,000'],['E','1.5','4.5','6,500']])],
18:[(['구분','가중치','A회사','B회사','C회사','D회사','E회사'],[['근무시간','4','4점','2점','2점','5점','5점'],['급여','4','3점','4점','5점','3점','2점'],['복지혜택','3','4점','4점','3점','4점','3점'],['인지도','2','2점','5점','4점','3점','1점'],['재택근무','3','가능','가능','불가능','불가능','가능']])],
20:[(['구분','A','B','C'],[['통행료(만 달러)','700','350','900'],['항해기간(일)','30','10','30'],['쇄빙선 이용료(만 달러)','200','400','600']])],
22:[(['문서 종류','1건당 중요도(점)','1건당 크기(MB)','건수'],[['가','8','12','12'],['나','5','8','18'],['다','3','3','24'],['라','3','4','32']])],
23:[(['구분','A','B','C','D'],[['A','－','60','70','20'],['B','60','－','35','35'],['C','70','35','－','70'],['D','20','35','70','－']])],
25:[(['요일','월','화','수','목','금','토','일'],[['기계(대)','3','4','5','5','4','2','1']])],
13:[(['의원실','사전질의 개수','의원실','사전질의 개수'],[['가','4','바','0'],['나','2','사','10'],['다','0','아','5'],['라','0','자','0'],['마','1','차','4']])]}
for q in bank:
 n=q['number'];src=tr[q['id']]
 assert norm(q['prompt'])==norm(src['prompt']),(n,'prompt')
 assert len(q['choices'])==5 and all(norm(x)==norm(y) for x,y in zip(q['choices'],src['choices'])),(n,'choices')
 originalBody=norm(src['body'])
 if n==21:assert originalBody.endswith(norm('최종 순위 선수'));originalBody=originalBody.removesuffix(norm('최종 순위 선수'));assert q['choiceNote']=='최종 순위 → 선수'
 if n==25:assert originalBody.endswith('ABC');originalBody=originalBody.removesuffix('ABC');assert q['choiceNote']=='A → B → C'
 if n in rawTables:
  assert len(q['tables'])==len(rawTables[n])
  for i,raw in enumerate(rawTables[n]):
   assert norm(tableSources[str(n)][i])==norm(raw),(n,'source table')
   assert originalBody.count(norm(raw))==1;originalBody=originalBody.replace(norm(raw),'',1)
   table=q['tables'][i];columns,rows=expectedTables[n][i];assert table['columns']==columns and table['rows']==rows,(n,'table cells')
   assert 0<=table['afterParagraph']<len(q['body'].split('\n\n'))
 assert norm(q['body'])==originalBody,(n,'body')
 assert q['answer']==keys[q['examDate']][n] and len(q['steps'])==len(q['optionReasons'])==5
 assert not any('\ue000'<=c<='\uf8ff' or c in '\ufffd\u2060\u2024' for c in json.dumps(q,ensure_ascii=False)),n
 assert not re.search(r'\d{4}\.\s*\n\s*\n\s*\d{1,2}\.',q['body'])
for c in json.loads((A/'crop-manifest.json').read_text(encoding='utf-8')):
 source=R/c['source'];assert hashlib.sha256(source.read_bytes()).hexdigest()==c['sha256']
 with pdfplumber.open(source) as pdf:
  ref=pdf.pages[c['page1based']-1].crop(c['rect']).to_image(resolution=c['resolution'],antialias=True).original.convert('RGB');path=R/c['asset'] if P.exists() else A/'staged'/c['asset'];im=Image.open(path).convert('RGB');assert im.size==ref.size and im.tobytes()==ref.tobytes(),c['asset']
seen=set();old=0
for path in (R/'assets/psat').glob('*.json'):
 if path.name in ['sets.json','situation15.json']:continue
 obj=json.loads(path.read_text(encoding='utf-8'))
 if isinstance(obj,list):
  for q in obj:
   k=(q.get('examDate',q['source'][:10].replace('.','-')),q['subject'],q['number']);assert k not in seen;seen.add(k);old+=1
for q in bank:
 k=(q['examDate'],q['subject'],q['number']);assert k not in seen;seen.add(k)
for path,digest in json.loads((A/'before-situation15-hashes.json').read_text(encoding='utf-8')).items():
 if path!='assets/psat/sets.json':assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
proof.update(status='PASS',count=10,officialFinalKeys=10,sourceComparison='native prompt/body/choices;7native tables/complete shared passage/10originalpixels',preservedExisting=old,limitations='Same-author semantic review with logical countermodels;not independent expert review.')
(A/'content-checks.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PASS10source/key/10pixels;models;preserved',old)
