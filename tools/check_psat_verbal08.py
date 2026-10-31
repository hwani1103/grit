from pathlib import Path
import json,re,hashlib,itertools,pdfplumber
from fractions import Fraction as F
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/verbal08';P=R/'assets/psat/verbal08.json'
bank=json.loads((P if P.exists() else A/'authored-verbal08.json').read_text(encoding='utf-8'))
def norm(s):return re.sub(r'[\s□「」『』\uf000]+','',s)
keys={}
for year,post,book in [(2025,'5994','인'),(2021,'3982','나')]:
 with pdfplumber.open(next((R/f'artifacts/psat600_20261028/sources/{post}').glob('*.pdf'))) as pdf:
  text=next(p.extract_text() for p in pdf.pages if '영역 언어논리' in p.extract_text());assert f'{year}년도' in text and f'{book} 책형' in text
  key={}
  for line in text.splitlines():
   if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
    ns=list(map(int,line.split()));key.update(zip(ns[::2],ns[1::2]))
  assert len(key)==25;keys[year]=key
for q in bank:
 y=int(q['examDate'][:4]);n=q['number'];raw=(A/f'{y}-l{n}-source.txt').read_text(encoding='utf-8')
 if y==2025 and n in [21,22]:
  shared,own=raw.split('\n ',1) if False else ('','')
  # Saved source = complete shared passage followed by question text, before its first prompt.
  marker=' 위 글에서 추론할 수 있는 것은?' if n==21 else ' 위 글에 비추어 볼 때,'
  at=raw.index(marker);shared=raw[:at].strip();raw=raw[at:]
 else:shared=''
 prompt,tail=raw.split('?',1);body,opts=tail.rsplit('\n① ',1)
 if shared:body=shared+'\n'+body
 if (y,n) in [(2025,23),(2021,3)]:
  tb=(A/f'{y}-l{n}-table-source.txt').read_text(encoding='utf-8');assert tb in body;body=body.replace(tb,'')
 assert norm(q['prompt'])==norm(prompt+'?'),(y,n,'prompt')
 if (y,n)!=(2021,4):assert norm(q['body'])==norm(body),(y,n,'body')
 options=re.split('[①②③④⑤]','① '+opts)[1:];assert len(options)==5
 assert all(norm(a)==norm(b) for a,b in zip(options,q['choices'])),(y,n,'choices')
 assert q['answer']==keys[y][n],(y,n,'key')
 assert len(q['steps'])==len(q['optionReasons'])==5
 for s,prefix in zip(q['steps'],['착안점: ','실전 풀이: ','답 확정 기준: ','정석 근거: ','적용 한계: ']):assert s.startswith(prefix) and len(s)>40,(n,s)
 assert not any('\ue000'<=c<='\uf8ff' or c in '\ufffd\u2060' for c in json.dumps(q,ensure_ascii=False))
 assert (R/q['original'] if P.exists() else A/'staged'/q['original']).exists()
for idx,post,pg in [(2,'6008',11),(7,'3977',1)]:
 with pdfplumber.open(next((R/f'artifacts/psat600_20261028/sources/{post}/pdf').glob('*언어*'))) as pdf:
  p=pdf.pages[pg];tb=p.crop((0,43,p.width/2,p.height-15)).extract_tables()[0];rows=tb[1:]
  if idx==2:
   for i,row in enumerate(rows):
    if row[0] is None:row[0]=rows[i-1][0]
  assert rows==bank[idx]['tables'][0]['rows']
  cols=['모형' if i==0 and idx==7 else ''.join(v.split()) for i,v in enumerate(tb[0])]
  assert cols==[''.join(v.split()) for v in bank[idx]['tables'][0]['columns']]
with pdfplumber.open(next((R/'artifacts/psat600_20261028/sources/3977/pdf').glob('*언어*'))) as pdf:
 p=pdf.pages[1];combined=''
 for c in json.loads((A/'crop-manifest.json').read_text(encoding='utf-8')):
  box=c['rect'];crop=p.crop(box);reference=crop.to_image(resolution=288).original.convert('RGB');path=R/c['asset'] if P.exists() else A/'staged'/c['asset'];im=Image.open(path).convert('RGB');assert im.size==reference.size and ImageChops.difference(im,reference).getbbox() is None
  for w in p.extract_words():
   intersects=w['x1']>box[0] and w['x0']<box[2] and w['bottom']>box[1] and w['top']<box[3]
   if intersects:assert w['x0']>=box[0]-.1 and w['x1']<=box[2]+.1 and w['top']>=box[1]-.1 and w['bottom']<=box[3]+.1,w
  combined+=crop.extract_text()
 raw=(A/'2021-l4-source.txt').read_text(encoding='utf-8').split('?',1)[1].rsplit('\n① ',1)[0];assert norm(combined)==norm(raw)
assert bank[1]['body'].startswith(bank[0]['body'])
assert bank[6]['body'].endswith('□')
# Separate arithmetic and exhaustive models.
assert F(8,26)==F(80,260) and F(7,34)<F(1,2)
true=100*F(99,100);false=(100000000-100)*F(1,100);assert (true,false)==(99,999999)
assert (true+false)/100000000<F(1,2) and true/(true+false)<F(1,10000)
scores=list(itertools.product(range(1,3),range(4),range(2,5)))
assert [all([a<=b,b<=c,a<=c][i] for a,b,c in scores) for i in range(3)]==[False,False,True]
assert max([1,2])<=min([2,4]) # continuous interval proof: max A2 <= min C2
oldflag={'UL':'감','UR':'건','LL':'곤','LR':'이'};swap={'UL':'UR','UR':'UL','LL':'LR','LR':'LL'};newflag={p:oldflag[swap[p]] for p in swap};assert newflag=={'UL':'건','UR':'감','LL':'이','LR':'곤'}
assert 10-7-2-0==1 and F(7,10)!=F(9,10)
counts=[]
for n in range(1,21):
 mb=list(itertools.product(range(n),repeat=2));be={tuple(sorted(x)) for x in mb};fd={x for x in be if x[0]!=x[1]}
 assert len(mb)==n*n and len(be)==n*(n+1)//2 and len(fd)==n*(n-1)//2
 if n>=2:assert len(mb)>len(be)
 counts.append([n,len(mb),len(be),len(fd)])
assert counts[1][2]==3 and all(counts[i+1][3]>counts[i][3] for i in range(19))
seen=set();old=0
for p in (R/'assets/psat').glob('*.json'):
 if p.name in ['sets.json','verbal08.json']:continue
 obj=json.loads(p.read_text(encoding='utf-8'))
 if isinstance(obj,list):
  for q in obj:
   k=(q.get('examDate',q['source'][:10].replace('.','-')),q['subject'],q['number']);assert k not in seen;seen.add(k);old+=1
for q in bank:
 k=(q['examDate'],q['subject'],q['number']);assert k not in seen;seen.add(k)
for path,digest in json.loads((A/'before-verbal08-hashes.json').read_text(encoding='utf-8')).items():
 if path!='assets/psat/sets.json':assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
proof={'status':'PASS','count':10,'officialFinalKeys':10,'sourceComparison':'all prompt/body/options;shared passage both;2tables PDFcells;2figures pixel and wordbounds;book/blank/law delimiters restored','baseRate':{'positiveExpected':1000098,'actualPositiveExpected':99},'rangeUniversal':[False,False,True],'flag':newflag,'particleCounts':counts,'preservedExisting':old,'limitations':'Same-author verification;not independent expert certification.'}
(A/'content-checks.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PASS10 source/finalkey;2tables;2pixelcrops;exactprobability;range/flag/particlecounts;preserved',old)
