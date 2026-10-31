from pathlib import Path
import json,re,hashlib,itertools as it,pdfplumber
from PIL import Image
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/verbal15';P=R/'assets/psat/verbal15.json'
bank=json.loads((P if P.exists() else A/'authored-verbal15.json').read_text(encoding='utf-8'));tr=json.loads((A/'source-transcripts.json').read_text(encoding='utf-8'))
assert [(q['examDate'],q['number']) for q in bank]==[('2026-07-18',n) for n in range(20,26)]+[('2026-03-07',n) for n in [13,14,33,34]]
proof={};certs=[]
for b,c in it.product(range(1,8),repeat=2):
 cs=[1,b,c,2,4]
 if [x.bit_count() for x in cs].count(2)!=1 or 1&b or c&b or c&(2|4):continue
 for selected in it.combinations(range(5),2):
  if sorted(cs[i].bit_count() for i in selected)!=[1,2]:continue
  if 0 in selected and 1 in selected:continue
  if 3 not in selected and 0 not in selected:continue
  certs.append(dict(cert=cs,selected=selected))
assert certs==[{'cert':[1,6,1,2,4],'selected':(1,3)}];proof['grade5_13']=certs
imp=lambda a,b:not a or b
allowed=[r for r in it.product([False,True],repeat=4) if imp(r[0],r[2]) and imp(r[1],not r[0])]
worlds=[]
for mask in range(1,1<<len(allowed)):
 rows=[r for i,r in enumerate(allowed) if mask>>i&1]
 if not(any(r[1] for r in rows) and any(not r[1] and r[2] for r in rows) and any(not r[0] and r[3] for r in rows)):continue
 claims=[any(r[0] and r[2] for r in rows),imp(not any(not r[2] and r[1] for r in rows),sum(r[2] for r in rows)>=2),imp(not any(r[3] and r[2] for r in rows),any(r[1] and r[3] for r in rows))]
 worlds.append(dict(rows=rows,claims=claims))
assert [all(w['claims'][i] for w in worlds) for i in range(3)]==[False,True,False]
proof['grade5_33']={'allowedTypes':allowed,'worldCount':len(worlds),'counterexamples':[next((w for w in worlds if not w['claims'][i]),None) for i in range(3)]}
models=[]
for matrix in it.product(range(16),repeat=4):
 received=[sum(bool(row>>i&1) for row in matrix) for i in range(4)];mx=max(received)
 if received.count(mx)!=1:continue
 leader=received.index(mx);team=matrix[leader]|(1<<leader)
 if team&1:continue
 preds=[[4 in received,not bool(team&1)],[15 in matrix,matrix[3]==1],[all(matrix),team==6],[not any(row>>i&1 for i,row in enumerate(matrix)),matrix[0]!=4]]
 if not all(a==b for a,b in preds) or sum(a for a,b in preds)!=2:continue
 claims=[not bool(matrix[0]&1),not bool(matrix[1]&4),bool(matrix[3]&4) and not bool(matrix[2]&8)]
 models.append(dict(rows=matrix,leader=leader,team=team,predictions=preds,claims=claims))
assert len(models)==49 and all(x['claims']==[True,False,True] and x['rows'][0]==4 and x['rows'][2]==6 and x['leader']==2 and x['team']==6 for x in models)
proof['grade5_34']={'modelCount':49,'models':models,'all65536MatricesChecked':True}

proof['grade5_14']={'answer':1,'witness':'old map and valuable heritage exists;valuable->recorded sends it to conclusion','countermodelFor2to5':{'oldMap':True,'valuable':True,'reviewTarget':False,'recorded':False},'universalDoesNotImplyExistence':True}
imp=lambda a,b:not a or b
oldMap,valuable,reviewTarget,recorded=True,True,False,False
assert imp(oldMap,not reviewTarget) and (oldMap and valuable) and imp(recorded,valuable)
assert [imp(valuable,recorded),oldMap and not recorded,imp(reviewTarget,not recorded),imp(recorded,reviewTarget),imp(oldMap,valuable)]==[False,True,True,True,True]
proof['regular20']={'interactionEffects':[['+','-'],['0','+'],['-','0']],'truth':[True,True,True],'comparison':'coexistence growth minus alone growth'}
proof['regular21']={'answer':4,'countercase':{'pastUnrefuted':True,'nearFutureUnrefuted':False,'stable':False},'limits':['usage is not stability','success is not truth','suspicion is not scientific refutation','near future is not forever']}
proof['regular22']={'truth':[False,True,False],'乙':'vagueness is irrelevant,not necessarily absent','病':'rejects correlation and rejects stability criterion'}
proof['regular23']={'answer':2,'mapping':{'㉠':'지자체','㉡':'○○청','㉢':'○○청','㉣':'서류 평가','㉤':'심의','㉥':'A 위원회','㉦':'심의'}}
proof['regular24']={'answer':1,'tablet':'exempt and used;still needs safety approval','vase':'nonexempt;needs duty payment','limit':'stipulated fictional country rules only'}
proof['regular25']={'truth':[True,False,True],'grounds':['marked walking area included;6minutes parking','free shuttle excluded by proposed paid-route definition','no passenger means not operating under proposed interpretation'],'eachInterpretationIndependent':True}
keys={}
for post,date,year,book in [(6016,'2026-07-18','2026','사'),(5982,'2026-03-07','2026','㉯')]:
 with pdfplumber.open(next((R/f'artifacts/psat600_20261028/sources/{post}').glob('*.pdf'))) as pdf:
  t=next(p.extract_text() for p in pdf.pages if '영역 언어논리' in p.extract_text());assert year in t and book in t;k={}
  for line in t.splitlines():
   if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
    v=list(map(int,line.split()));k.update(zip(v[::2],v[1::2]))
  assert len(k)==(40 if post==5982 else 25);keys[date]=k
def norm(s):
 s=re.sub(r'\uf000([^\uf000]+)\uf000',r'『\1』',s).replace('','α').replace('','β')
 return re.sub(r'[\s·․]+','',s.replace('\uf000','『').replace('\uf001','』'))
for q in bank:
 n=q['number'];src=tr[q['id']]
 assert norm(q['prompt'])==norm(src['prompt']),(n,'prompt')
 assert len(q['choices'])==5 and all(norm(x)==norm(y) for x,y in zip(q['choices'],src['choices'])),(n,'choices')
 if q['examDate']=='2026-07-18' and n==23:
  assert norm(q['body'])==norm(src['body'].split('<일반 지원 프로그램>',1)[0])
  assert len(q['tables'])==2
  assert q['tables'][0]['columns']==q['tables'][1]['columns']==['순서','담당 기관','절차']
  assert q['tables'][0]['rows']==[['1','지자체','신청 접수'],['2','㉠','현장 평가'],['3','㉡','㉣'],['4','A 위원회','㉤'],['5','㉢','사업비 교부'],['6','지자체','사업 추진']]
  assert q['tables'][1]['rows']==[['1','A 위원회','신청 접수'],['2','㉥','㉦'],['3','○○청','사업비 교부'],['4','지자체','사업 추진']]
  assert all(t['afterParagraph']==len(q['body'].split('\n\n'))-1 for t in q['tables'])
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
 if path.name in ['sets.json','verbal15.json']:continue
 obj=json.loads(path.read_text(encoding='utf-8'))
 if isinstance(obj,list):
  for q in obj:
   k=(q.get('examDate',q['source'][:10].replace('.','-')),q['subject'],q['number']);assert k not in seen;seen.add(k);old+=1
for q in bank:
 k=(q['examDate'],q['subject'],q['number']);assert k not in seen;seen.add(k)
for path,digest in json.loads((A/'before-verbal15-hashes.json').read_text(encoding='utf-8')).items():
 if path!='assets/psat/sets.json':assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
assert norm(bank[1]['body']) in norm(bank[2]['body'])
proof.update(status='PASS',count=10,officialFinalKeys=10,sourceComparison='native prompt/body/choices;2flowtables/1underline/shared passage/10originalpixels',preservedExisting=old,limitations='Same-author semantic review with logical countermodels;not independent expert review.')
(A/'content-checks.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PASS10source/key/10pixels;models;preserved',old)
