from pathlib import Path
import json,re,hashlib,itertools as it,pdfplumber
from PIL import Image
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/verbal14';P=R/'assets/psat/verbal14.json'
bank=json.loads((P if P.exists() else A/'authored-verbal14.json').read_text(encoding='utf-8'));tr=json.loads((A/'source-transcripts.json').read_text(encoding='utf-8'))
assert [(q['examDate'],q['number']) for q in bank]==[('2026-07-18',n) for n in range(10,20)]
proof={}
imp=lambda a,b:not a or b
m16=[]
for S,V,H,B,Aval,N,D in it.product([False,True],repeat=7):
 if not(imp(S,V) and imp(V,H or B or Aval) and imp(V,not B) and imp(H,N or D)):continue
 added=[imp(S,not B) and imp(S,not D),imp(B,Aval) and imp(H,D),imp(V,not Aval) and imp(H,not D),imp(V,not Aval) and imp(H,not N),imp(V,Aval) and imp(H,not D)]
 m16.append(dict(state=[S,V,H,B,Aval,N,D],added=added,conclusion=imp(S,N)))
counters=[[x['state'] for x in m16 if x['added'][i] and not x['conclusion']] for i in range(5)]
assert [not x for x in counters]==[False,False,True,False,False]
assert all(any(x['added'][i] and x['state'][0] for x in m16) for i in range(5))
proof['q16']={'variables':['soldier','brave','selfSacrifice','blind','authoritarian','honorable','dogmatic'],'counterexamples':counters,'validOnly':3,'all128AssignmentsChecked':True}
m17=[]
for Rr,B,Ping,M,H,T in it.product([False,True],repeat=6):
 if not(imp(B or Ping,Rr) and (T== (not Rr)) and imp(M,H) and not(H and B)):continue
 claims=[imp(T,H),imp(Rr and M,B),imp(Ping and B,not M),imp(M,sum([B,Ping,M,H,T])>=3),imp(Rr and H and not Ping,M)]
 m17.append(dict(state=[Rr,B,Ping,M,H,T],claims=claims))
counters=[[x['state'] for x in m17 if not x['claims'][i]] for i in range(5)]
assert [not x for x in counters]==[False,False,True,False,False]
proof['q17']={'variables':['research','basketball','pingpong','marathon','hiking','tennis'],'counterexamples':counters,'validOnly':3,'all64AssignmentsChecked':True}
m18=[]
for Aval,B,C in it.product([False,True],repeat=3):
 claims=[imp(Aval,B),Aval or B,imp(not B,C and not Aval),imp(C,Aval),C and not B]
 if claims.count(False)==1:m18.append(dict(state=[Aval,B,C],claims=claims))
assert [x['state'] for x in m18]==[[False,True,False],[True,True,False],[True,True,True]] and all(x['claims']==[True]*4+[False] for x in m18)
proof['q18']={'models':m18,'uniqueFalsePerson':5,'all8AssignmentsChecked':True}
proof['q10']={'answer':5,'ineligible':'large-company employee is excluded from growth voucher despite proper use','ageBoundaries':[19,34,49]}
proof['q11']={'truth':[True,True,False],'arrows':['naturalKind -> qualitativeSimilarity','Mayr:reproductiveIsolation -> geographicalIsolation','Smith:sympatricSpeciation -> strongSelection'],'limit':'Different theorists are evaluated separately.'}
proof['q12']={'answer':5,'axes':['energy','electron','carbon'],'purpleNonSulfur':['photo-organo-hetero without oxygen','chemo-organo-hetero with oxygen'],'carbonUnchanged':True}
proof['q13']={'truth':[True,False,False],'B':'suspends judgment;does not affirm inner states or endorse A criterion'}
proof['q14']={'answer':2,'wavelength':'C>B>A','energy':'A>B>C','size':'A<B<C','sameMaterialRequired':True}
proof['q15']={'truth':[False,True,False],'reason':'two component proportions sum to one;stickiness tracks amylopectin;enzyme amount for Q not specified'}
proof['q19']={'answer':1,'terms':['shorter','larger','heavier'],'limit':'Experiment C supports a proposed explanation,not proof eliminating all alternatives.'}
keys={}
for post,date,year,book in [(6016,'2026-07-18','2026','사')]:
 with pdfplumber.open(next((R/f'artifacts/psat600_20261028/sources/{post}').glob('*.pdf'))) as pdf:
  t=next(p.extract_text() for p in pdf.pages if '영역 언어논리' in p.extract_text());assert year in t and book in t;k={}
  for line in t.splitlines():
   if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
    v=list(map(int,line.split()));k.update(zip(v[::2],v[1::2]))
  assert len(k)==25;keys[date]=k
def norm(s):
 s=re.sub(r'\uf000([^\uf000]+)\uf000',r'『\1』',s)
 return re.sub(r'[\s·․]+','',s.replace('\uf000','『').replace('\uf001','』'))
for q in bank:
 n=q['number'];src=tr[q['id']]
 assert norm(q['prompt'])==norm(src['prompt']),(n,'prompt')
 assert len(q['choices'])==5 and all(norm(x)==norm(y) for x,y in zip(q['choices'],src['choices'])),(n,'choices')
 if n==10:
  before,tail=src['body'].split('유형 연령 취업 여부',1);table,after=tail.split('지원 신청 자격',1)
  assert norm(q['body'])==norm(before+'지원 신청 자격'+after)
  assert norm(table)=='준비형19세이상34세미만미취업성장형19세이상34세미만취업전환형34세이상49세이하상관없음'
  assert q['tables'][0]['columns']==['유형','연령','취업 여부'] and q['tables'][0]['rows']==[['준비형','19세 이상 34세 미만','미취업'],['성장형','19세 이상 34세 미만','취업'],['전환형','34세 이상 49세 이하','상관 없음']]
 elif n in [14,19]:
  header='(가) (나)' if n==14 else '(가) (나) (다)'
  assert norm(q['body'])==norm(src['body'].rsplit(header,1)[0])
  assert q['choiceNote']==' → '.join(header.split())
 else:assert norm(q['body'])==norm(src['body']),(n,'body')
 assert q['body'].count('『')==q['body'].count('』') and not re.search(r'『[^』]*『',q['body'])
 assert q['answer']==keys[q['examDate']][n] and len(q['steps'])==len(q['optionReasons'])==5
 assert all(q['body'].count(u)==1 and '\n' not in u for u in q.get('underlines',[])),(n,'underline',q.get('underlines'))
 assert not any('\ue000'<=c<='\uf8ff' or c in '\ufffd\u2060\u2024' for c in json.dumps(q,ensure_ascii=False)),n
 assert not re.search(r'\d{4}\.\s*\n\s*\n\s*\d{1,2}\.',q['body'])
for c in json.loads((A/'crop-manifest.json').read_text(encoding='utf-8')):
 source=R/c['source'];assert hashlib.sha256(source.read_bytes()).hexdigest()==c['sha256']
 with pdfplumber.open(source) as pdf:
  ref=pdf.pages[c['page1based']-1].crop(c['rect']).to_image(resolution=c['resolution'],antialias=True).original.convert('RGB');path=R/c['asset'] if P.exists() else A/'staged'/c['asset'];im=Image.open(path).convert('RGB');assert im.size==ref.size and im.tobytes()==ref.tobytes(),c['asset']
seen=set();old=0
for path in (R/'assets/psat').glob('*.json'):
 if path.name in ['sets.json','verbal14.json']:continue
 obj=json.loads(path.read_text(encoding='utf-8'))
 if isinstance(obj,list):
  for q in obj:
   k=(q.get('examDate',q['source'][:10].replace('.','-')),q['subject'],q['number']);assert k not in seen;seen.add(k);old+=1
for q in bank:
 k=(q['examDate'],q['subject'],q['number']);assert k not in seen;seen.add(k)
for path,digest in json.loads((A/'before-verbal14-hashes.json').read_text(encoding='utf-8')).items():
 if path!='assets/psat/sets.json':assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
proof.update(status='PASS',count=10,officialFinalKeys=10,sourceComparison='native prompt/body/choices;table1/2underline ranges/10originalpixels',preservedExisting=old,limitations='Same-author semantic review with logical countermodels;not independent expert review.')
(A/'content-checks.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PASS10source/key/10pixels;models;preserved',old)
