from pathlib import Path
from fractions import Fraction as F
from itertools import permutations
import json,re,hashlib,pdfplumber
from PIL import Image
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/data06';P=R/'assets/psat/data06.json'
bank=json.loads((P if P.exists() else A/'authored-data06.json').read_text(encoding='utf-8'));checks={}
def note(n,answer,e):
 assert next(q for q in bank if q['number']==n)['answer']==answer
 checks[str(n)]=e
cells=[[1,2,2,0],[0,2,0,2],[2,0,1,2],[2,2,1,1],[1,1,1,2]];scores=[sum(a*b for a,b in zip(row,[10,15,15,20])) for row in cells]
assert scores==[70,70,75,85,80];note(1,4,{'scores':scores,'grayCellsByPlayer':cells,'halfWeights':[10,15,15,20]})
assert 42324>3095*10 and (430>427)!=(42324>44009)
assert 34777<F(44009)*F(4,5) and 44009-34777==9232>F(44009,5)
note(2,4,{'truth':[True,False,True],'children80percent':str(F(44009)*F(4,5)),'decrease':9232})
old=[10639,9163,9464,9939,10879,10597,11064,11186,11222,11516,11324,9873];new=[9834,9595,12025,11417,12365,12422,13961,14281,13393,12890,11991,11771]
assert sum(old)==126866 and sum(new)==145945 and F(sum(new)-sum(old),sum(old))>F(15,100)
assert new.index(max(new))==7 and [i for i,(a,b) in enumerate(zip(old,new)) if b<a]==[0]
shares=[F(s) for s in ['62.1','7.1','6.9','3.8','3.1','2.2','2.0','1.4','1.2','1.2','1.1','1.1','6.8']]
assert sum(shares)==100 and sum(shares[:3])==F('76.1')
pop=[287824,112231,122100,62045,60976];cases=[60433,35904,26852,12399,10357];rates=[F(c*100,p) for c,p in zip(cases,pop)]
assert sum(cases)==sum(new) and F(cases[0],sum(new))>F(2,5) and rates.index(max(rates))==1 and rates[1]>=30
note(3,5,{'sourceMappings':{'1':'population denominator','2':'field shares','3':'keywords','4':'regionalcounts','5':'notused:fieldyearonyearchanges'},'annualTotals':[sum(old),sum(new)],'per100':list(map(str,rates))})
awareness=list(map(F,['72.9','47.5','69.8','70.5','83.8']));assert all(a<b for a,b in zip(awareness[1:],awareness[2:]))
approval=[[F(s) for s in row] for row in [['15.0','62.8','16.8','5.4'],['18.3','55.6','19.2','6.9'],['11.5','70.6','14.1','3.8']]]
assert all(sum(x)==100 for x in approval) and [sum(x[:2]) for x in approval]==list(map(F,['77.8','73.9','82.1']))
assert F('48.0')+F('31.2')+F('20.8')==100
note(4,4,{'approval':[str(sum(x[:2])) for x in approval],'unused':'preferrededucationroute differsfromactualexposure','educationNeedDoesNotRequirePreference':True})
actual=[4000,26000-4000-6000-9000,6000,9000];maximum=[5000,9000,35000-5000-9000-12000,12000];util=[F(a,b) for a,b in zip(actual,maximum)]
assert actual[1]==7000 and maximum[2]==9000 and sorted(range(4),key=lambda i:util[i],reverse=True)==[0,1,3,2]
note(5,2,{'actual':actual,'maximum':maximum,'utilization':list(map(str,util)),'crossProducts':[[36,35],[28,27],[9,8]]})
coffee=[[4,2,3,2,4],[4,2,5,2,4],[4,2,3,2,3],[4,5,3,2,4],[5,4,4,3,4],[5,5,3,2,3],[5,4,3,3,4],[2,4,3,2,1],[4,3,3,2,2],[5,4,4,3,4],[4,5,3,3,4],[2,3,3,3,4],[4,5,4,4,4],[4,5,3,3,4]]
with pdfplumber.open(next((R/'artifacts/psat600_20261028/sources/6008/pdf').glob('*자료해석*'))) as pdf:
 im=pdf.pages[3].crop((35,95,360,420)).to_image(resolution=216).original.convert('L');sampled=[]
 for r in range(14):
  row=[];cy=155+60*r
  for c in range(5):
   count=0
   for k in range(5):
    cx=373+121*c+20*k;patch=im.crop((cx-8,cy-10,cx+8,cy+10));count+=sum(v<100 for v in patch.tobytes())>15
   row.append(count)
  sampled.append(row)
 assert sampled==coffee,'350icon pixel recount differs from visual transcription'
sums=[sum(row) for row in coffee];assert [max(sums[:5]),max(sums[5:10]),max(sums[10:])]==[20,20,21]
assert max(row[2] for row in coffee)==5==coffee[1][2]
assert coffee[11][0]<coffee[11][2] and coffee[12][0]==coffee[12][2]
assert min(range(5,10),key=lambda i:coffee[i][4])==min(range(5,10),key=lambda i:coffee[i][0])==7
assert max(range(5),key=lambda i:coffee[i][1])==3 and sums[3]==18<20==sums[4]
note(6,3,{'visualMatrixAnd350IconPixelRecount':coffee,'totals':sums,'regionalMax':[20,20,21],'sourceName':'도미니카 AA'})
rows=[[4,10,6,14,32,10],[8,6,10,12,24,8],[6,4,8,16,34,2],[8,6,4,20,36,8],[10,6,10,16,28,6]];tests=[]
for r in rows:tests.append([sum(r[:2])>=14,sum(r[2:4])>=20,abs(r[2]-r[3])<10,2*sum(r[4:])>=sum(r)])
assert [all(x) for x in tests]==[True,False,False,False,False]
note(7,1,{'conditionsByCompany':tests,'totals':list(map(sum,rows)),'dialogueThresholds':[14,20,10,50]})
data={'A':[190,F('4.2'),F('4.1'),F('4.3')],'B':[120,F('3.9'),F('4.0'),F('3.8')],'C':[180,F('4.6'),F('4.8'),F('4.1')],'D':[150,F('3.8'),F('3.6'),F('3.9')]};solutions=[]
for perm in permutations('ABCD'):
 culture,invention,tax,info=perm
 if {k for k,r in data.items() if r[3]>r[1]}!={invention,tax}:continue
 if data[info][2]>data[tax][2] and data[culture][0]>data[info][0]:solutions.append(perm)
assert solutions==[('C','A','D','B')]
note(8,3,{'testedMappings':24,'uniqueCultureInventionTaxInfo':solutions})
assert F('214.8')<F('547.9')*F(2,5)
assert F('33.9')>F('17.3')*F(3,2) and F('144.4')<F('214.8')*F(3,4)
assert 2*(F('222.0')+F('80.3'))>F('594.7')
assert F('114.1')<F('92.9')*F(3,2)
note(9,3,{'truth':[False,True,True,False],'doubleRatioBounds':'A>150%,capital<75%','generationDoubleSum':'604.6','B150percentThreshold':'139.35'})
inv=[[F(s) for s in r] for r in [['102.9','80.0','89.9','91.8'],['106.6','91.4','93.8','90.0'],['112.2','98.9','96.4','95.9'],['95.0','97.7','97.5','94.9']]]
ship=[[F(s) for s in r] for r in [['96.2','102.8','116.7','108.5'],['92.2','107.1','111.6','107.3'],['93.4','106.0','106.4','104.7'],['93.8','104.6','105.9','103.7']]]
directions=[]
for c in range(4):
 seq=[F(100)]+[row[c] for row in ship];directions.append([(b>a)-(b<a) for a,b in zip(seq,seq[1:])])
assert directions==[[-1,-1,1,1],[1,1,-1,-1],[1,-1,-1,-1],[1,-1,-1,-1]]
assert inv[0][1]/inv[-1][1]*100<100
assert [all(inv[y][c]>=ship[y][c] for y in range(4)) for c in range(4)]==[True,False,False,False]
note(10,3,{'truth':[True,False,True],'directionsIncluding2020':directions,'rebasedCounterexample':str(inv[0][1]/inv[-1][1]*100)})
with pdfplumber.open(next((R/'artifacts/psat600_20261028/sources/5994').glob('*.pdf'))) as pdf:
 t=next(p.extract_text() for p in pdf.pages if '영역 자료해석' in p.extract_text());assert '2025년도' in t and '인 책형' in t
 key={}
 for line in t.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
   v=list(map(int,line.split()));key.update(zip(v[::2],v[1::2]))
 assert len(key)==25
norm=lambda s:re.sub(r'\s+','',s)
for q in bank:
 n=q['number'];raw=(A/f'2025-d{n}-source.txt').read_text(encoding='utf-8').split(f'{n}.',1)[1];prompt,tail=raw.split('?',1)
 assert norm(q['prompt'])==norm(prompt+'?')
 assert q['answer']==key[n]
 if n in [3,4]:
  assert q['choices']==[f'자료 {i}' for i in range(1,6)]
  assert [f['caption'] for f in q['figures'][2 if n==3 else 1:]]==[f'선택지 {i}' for i in '①②③④⑤']
 else:
  opts=re.split('[①②③④⑤]','①'+tail.split('①',1)[1])[1:]
  assert len(opts)==5 and all(norm(a)==norm(b) for a,b in zip(opts,q['choices']))
 assert len(q['steps'])==len(q['optionReasons'])==5
 for st,prefix in zip(q['steps'],['착안점: ','실전 풀이: ','답 확정 기준: ','정석 근거: ','적용 한계: ']):assert st.startswith(prefix) and len(st)>40
 assert not any(c in json.dumps(q,ensure_ascii=False) for c in ['\u2060','\ufffd'])
# Every figure is a deterministic crop of the official PDF, with text boundaries intact.
manifest=json.loads((A/'crop-manifest.json').read_text(encoding='utf-8'));assert len(manifest)==27
with pdfplumber.open(R/manifest[0]['source']) as pdf:
 for f in manifest:
  assert hashlib.sha256((R/f['source']).read_bytes()).hexdigest()==f['sha256']
  path=R/f['asset'] if P.exists() else A/'staged'/f['asset']
  im=Image.open(path).convert('RGB');ref=pdf.pages[f['page1based']-1].crop(f['rect']).to_image(resolution=f['resolution']).original.convert('RGB')
  assert im.size==ref.size and im.tobytes()==ref.tobytes(),f['asset']
  x0,y0,x1,y1=f['rect']
  for w in pdf.pages[f['page1based']-1].extract_words():
   if w['x1']<=x0 or w['x0']>=x1 or w['bottom']<=y0 or w['top']>=y1:continue
   assert w['x0']>=x0-.5 and w['x1']<=x1+.5 and w['top']>=y0-.5 and w['bottom']<=y1+.5,(f['asset'],w['text'])
seen=set();old=0
for path in (R/'assets/psat').glob('*.json'):
 if path.name in ['sets.json','data06.json']:continue
 obj=json.loads(path.read_text(encoding='utf-8'))
 if isinstance(obj,list):
  for q in obj:
   k=(q.get('examDate',q['source'][:10].replace('.','-')),q['subject'],q['number']);assert k not in seen;seen.add(k);old+=1
for q in bank:
 k=(q['examDate'],q['subject'],q['number']);assert k not in seen;seen.add(k)
for path,digest in json.loads((A/'before-data06-hashes.json').read_text(encoding='utf-8')).items():
 if path=='assets/psat/sets.json':continue
 assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
checks.update(status='PASS',count=10,officialFinalKeys=10,figures=27,preservedExisting=old,limitations='Same-author visual/source review with exact rational comparisons, 24 mappings and 350 icon pixel recount; not independent expert certification.')
(A/'content-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PASS:10keys,27pixelmatchedfigures,all source text/choice mappings,ratios/mappings/iconrecount,existing',old)