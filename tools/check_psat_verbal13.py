from pathlib import Path
import json,re,hashlib,itertools as it,pdfplumber
from PIL import Image
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/verbal13';P=R/'assets/psat/verbal13.json'
bank=json.loads((P if P.exists() else A/'authored-verbal13.json').read_text(encoding='utf-8'));tr=json.loads((A/'source-transcripts.json').read_text(encoding='utf-8'))
assert [(q['examDate'],q['number']) for q in bank]==[('2025-11-15',n) for n in [23,24,25]]+[('2026-07-18',n) for n in [1,3,4,6,7,8,9]]
proof={};models=[]
# True=high. Both regions share the national level/sex-gap benchmark.
for gl,gc,gg,nl,nc,ng in it.product([False,True],repeat=6):
 if not(not gl and not gc and gg):continue
 if not nl<=gl or not gg<=ng:continue # turnout_n < turnout_g; gap_n > gap_g
 if not nl and not nc and ng:continue
 for a in ['change','gap']:
  ga,gb=(gc,gg) if a=='change' else (gg,gc)
  na,nb=(nc,ng) if a=='change' else (ng,nc)
  models.append(dict(ga=[gl,ga,gb],na=[nl,na,nb],A=a,judgments=[gl==nl,not(ga!=na) or gb==nl,nl!=nb]))
assert len(models)==2 and all(x['judgments'][0] and x['judgments'][2] for x in models)
assert any(not x['judgments'][1] for x in models)
proof['special23']={'models':models,'universallyTrue':[True,False,True]}
proof['special24']={'truth':[False,False,True],'missingOrMisread':['prior quarters application and nonallocation','at least one dependent,not every dependent','evidenced uninhabitability exception and actual co-residence']}
assert 63-24==39 and max(24,39)<60
proof['special25']={'truth':[True,True,True],'grounds':['no residence','ownership segments24and39months each below60','residence ended6months before selection'],'limit':'Each proposed interpretation is evaluated separately;not advice on current law.'}
proof['regular1']={'correct':4,'mismatches':['issuer and period','ruler and metal plus unsupported exclusive tax','unproved recall and successful reissue','exclusive currency usage not stated']}
proof['regular3']={'correct':4,'structure':['general law','actual condition satisfied','event explained'],'distractor2':'why-question alone omits distinction of scientific explanation'}
proof['regular4']={'correct':5,'shared':'human improvement possible','difference':'interpersonal relation required vs individual capacity sufficient'}
def classify(mother,target,same):
 if not mother and target:return 'exclusive'
 if mother and target:return 'positive' if same else 'intrusive'
 raise AssertionError
assert [classify(True,True,True),classify(True,True,False),classify(False,True,False)]==['positive','intrusive','exclusive']
proof['regular6']={'actualTypes':['positive','intrusive','exclusive'],'truth':[True,False,False],'limit':'Evaluate stipulated linguistic cases,not all real lexical uses.'}
proof['regular7']={'correct':3,'direction':'experience reconstructed using existing cognitive scheme','intro':'common belief is intentionally contrasted,not author endorsement'}
proof['regular8']={'correct':4,'earlier':['less than meal','time unrestricted'],'later':['meal','midday'],'notInferred':['fixed quantity','place constraint']}
proof['regular9']={'truth':[True,True,True],'comparisons':['A/B other activity share','A/C practical course count','festival participant/nonparticipant completion'],'limit':'Relevant observational data do not alone establish causality.'}
keys={}
for post,date,year,book in [(6001,'2025-11-15','2025','혁'),(6016,'2026-07-18','2026','사')]:
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
 if q['examDate']=='2025-11-15' and n==23:
  before,tail=src['body'].split('<표> 투표율 분석 결과',1);table,after=tail.split('<보 기>',1)
  assert norm(q['body'])==norm(before+'<보기>'+after)
  assert norm(table)=='항목투표율수준AB지역(가)㉠㉡㉢(나)㉣㉤㉥'
  assert q['tables'][0]['columns']==['지역 / 항목','투표율 수준','A','B'] and q['tables'][0]['rows']==[['(가)','㉠','㉡','㉢'],['(나)','㉣','㉤','㉥']]
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
 if path.name in ['sets.json','verbal13.json']:continue
 obj=json.loads(path.read_text(encoding='utf-8'))
 if isinstance(obj,list):
  for q in obj:
   k=(q.get('examDate',q['source'][:10].replace('.','-')),q['subject'],q['number']);assert k not in seen;seen.add(k);old+=1
for q in bank:
 k=(q['examDate'],q['subject'],q['number']);assert k not in seen;seen.add(k)
for path,digest in json.loads((A/'before-verbal13-hashes.json').read_text(encoding='utf-8')).items():
 if path!='assets/psat/sets.json':assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
proof.update(status='PASS',count=10,officialFinalKeys=10,sourceComparison='native prompt/body/choices;table1/7underline ranges/10originalpixels',preservedExisting=old,limitations='Same-author semantic review with logical countermodels;not independent expert review.')
(A/'content-checks.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PASS10source/key/10pixels;models;preserved',old)
