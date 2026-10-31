from pathlib import Path
import json,re,hashlib,pdfplumber,itertools as it
from PIL import Image
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/verbal10';P=R/'assets/psat/verbal10.json';bank=json.loads((P if P.exists() else A/'authored-verbal10.json').read_text(encoding='utf-8'));tr=json.loads((A/'source-transcripts.json').read_text(encoding='utf-8'));proof={}
# Exhaust both row assignments, retaining actual facts before reading answer choices.
facts={'notice':['미완료','완료','미완료'],'similar':['있음','있음','없음']};assign=[(a,b) for a,b in [('notice','similar'),('similar','notice')]]
truth=[all(facts[b][0]==facts[b][2] for a,b in assign if a=='similar'),all(facts[a][0]==facts[a][2] for a,b in assign if b=='similar'),all(facts[a][0]==facts[a][1] for a,b in assign if facts[b][0]==facts[b][1])];assert truth==[True,True,False];proof['18']={'truth':truth,'allAssignments':assign,'facts':facts}
# q21: actual event 0/1, predicted low/high0/1. Both must be errors and the larger group rates align with summary.
opts=[(0,1,1,0),(0,1,1,1),(0,0,1,0),(1,1,0,0),(1,0,0,1)]
valid=[a!=b and c!=d and b==1 and d==0 for a,b,c,d in opts];assert valid==[True,False,False,False,False];proof['21']={'optionsValid':valid,'rateDenominator':'actual outcome;not prediction class'}
# q24: conjunctive common threshold remains under adding a list category.
parking=50;eligible=parking>=100;assert not eligible
support=[eligible,eligible,eligible,True,eligible];assert support==[False,False,False,True,False];proof['24']={'threshold':100,'parking':50,'supportAfterAmendment':support}
# q25: continuity is counted over actual intervening tenure, not total lifetime counts.
history=['C','C','D','C'];runs=[len(list(g)) for k,g in it.groupby(history) if k=='C'];assert max(runs)==2;proof['25']={'truth':[True,True,False],'tenure':history,'maxConsecutiveC':max(runs)}
assert 12000<1000000 and 12000*90>1000000 and 2000000>1000000 and 1000000<=1000000
proof['23']={'perRecipientFestival':12000,'firstCRefused':True,'repeatSameNotYet':True,'dutyIfRepeat':True,'optionTruth':[False,False,False,False,True]}
proof['16']={'manual':'retain website instructions + add mobile application;not replace;final agreement civilian course only','invalid':5}
proof['17']={'old':['기관','서류','필기','면접'],'new':['도','기관','필기','서류','면접'],'manual':'roles/sequence/content separately read;two charts directly inspected','answer':3}
proof['19']={'truth':[True,True,False],'manual':'population-normalized facilities;actual copay;age composition not absolute willing age50-64 counts'}
proof['22']={'truth':[False,False,True],'manual':'subgroup equal extreme risk does not strengthen bias;baseline vs accuracy compatible B;crime-type base group alone no racial-feedback evidence;not strengthened differs refuted'}
proof['special1']={'manual':'paragraph3directrecord+paragraph4officialsaccess;otherchoicesaddcountcomparison/accessban/neutrality','answer':4}
keys={}
for sp,folder,year,book in [(False,'3982','2021','나'),(True,'6001','2025','혁')]:
 with pdfplumber.open(next((R/'artifacts/psat600_20261028/sources'/folder).glob('*.pdf'))) as pdf:
  t=next(p.extract_text() for p in pdf.pages if '영역 언어논리' in p.extract_text());assert year in t and book in t;k={}
  for line in t.splitlines():
   if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
    v=list(map(int,line.split()));k.update(zip(v[::2],v[1::2]))
  assert len(k)==25;keys[sp]=k
norm=lambda s:re.sub(r'[\s□·․「」]+','',s)
for q in bank:
 n=q['number'];sp=q['examDate']=='2025-11-15';src=tr[q['id']]
 assert norm(q['prompt'])==norm(src['prompt']) and all(norm(x)==norm(y) for x,y in zip(q['choices'],src['choices'])),(n,'prompt/choice')
 if n==17:assert q['body']=='' and len(q['figures'])==2
 elif n==18:
  b=src['body'];pre,post=b.split('<표>',1);unused,post=post.split('<보 기>',1);assert norm(q['body'])==norm(pre+'<보기>'+post);assert q['tables'][0]['rows']==[['A','㉠','㉡','㉢'],['B','㉣','㉤','㉥']]
  assert all(c in src['body'] for c in ['(가)','(나)','(다)','A','B','㉠','㉡','㉢','㉣','㉤','㉥'])
 else:assert norm(q['body'])==norm(src['body']),(n,'body')
 assert q['answer']==keys[sp][n] and len(q['steps'])==len(q['optionReasons'])==5
 for s,prefix in zip(q['steps'],['착안점: ','실전 풀이: ','답 확정 기준: ','정석 근거: ','적용 한계: ']):assert s.startswith(prefix) and len(s)>40
 for u in q.get('underlines',[]):assert q['body'].count(u)==1,(n,u)
 assert not any('\ue000'<=c<='\uf8ff' or c in '\ufffd\u2060\u2024' for c in json.dumps(q,ensure_ascii=False))
assert bank[4]['body']==bank[5]['body'].split('\n\n<보기>')[0] and bank[6]['body'].endswith('□')
assert bank[4]['choiceNote']=='(가) → (나) → (다) → (라)'
for c in json.loads((A/'crop-manifest.json').read_text(encoding='utf-8')):
 source=R/c['source'];assert hashlib.sha256(source.read_bytes()).hexdigest()==c['sha256']
 with pdfplumber.open(source) as pdf:
  p=pdf.pages[c['page1based']-1];ref=p.crop(c['rect']).to_image(resolution=c['resolution'],antialias=True).original.convert('RGB');path=R/c['asset'] if P.exists() else A/'staged'/c['asset'];im=Image.open(path).convert('RGB');assert im.size==ref.size and im.tobytes()==ref.tobytes(),c['asset']
  if '/figures/' in c['asset']:
   x0,y0,x1,y1=c['rect']
   for w in p.extract_words():
    if w['x1']<=x0 or w['x0']>=x1 or w['bottom']<=y0 or w['top']>=y1:continue
    assert w['x0']>=x0-.5 and w['x1']<=x1+.5 and w['top']>=y0-.5 and w['bottom']<=y1+.5,(c['asset'],w)
seen=set();old=0
for path in (R/'assets/psat').glob('*.json'):
 if path.name in ['sets.json','verbal10.json']:continue
 obj=json.loads(path.read_text(encoding='utf-8'))
 if isinstance(obj,list):
  for q in obj:
   k=(q.get('examDate',q['source'][:10].replace('.','-')),q['subject'],q['number']);assert k not in seen;seen.add(k);old+=1
for q in bank:
 k=(q['examDate'],q['subject'],q['number']);assert k not in seen;seen.add(k)
for path,digest in json.loads((A/'before-verbal10-hashes.json').read_text(encoding='utf-8')).items():
 if path!='assets/psat/sets.json':assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
proof.update(status='PASS',count=10,officialFinalKeys=10,sourceComparison='allnativeprompt/body/options;sharedcomplete;table1;blankrestored;12pixelcomparisons;2figurewordboundaries',preservedExisting=old,held='2021l20unpublished',limitations='Same-author original/manual semantics plus algorithmic structured models;not independent expert review.')
(A/'content-checks.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PASS10source/key/original;models;preserved',old)
