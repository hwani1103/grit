from pathlib import Path
import json,re,hashlib,pdfplumber,itertools as it
from fractions import Fraction as F
from PIL import Image
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/situation11';P=R/'assets/psat/situation11.json';bank=json.loads((P if P.exists() else A/'authored-situation11.json').read_text(encoding='utf-8'));tr=json.loads((A/'source-transcripts.json').read_text(encoding='utf-8'));proof={}
proof['1']={'roles':{'domesticApplication':'job agency','list':'minister + sending-country labour official','recommendPermit':'agency head -> employer'},'truth':[False,True,False,False,False]}
assert 9*F(2,3)==6;proof['2']={'planDeadline':'April end','resultDeadline':'March end','privateMinOf9':6,'answer':3}
proof['3']={'truth':[False,True,True],'checks':['prescription-required professional-drug patient sale','volunteer preparation exception + pharmacy location','ordinary drug + mayor-approved outside location']}
payA=F(45,10)*12*F(1,2);payB=6*8;assert payA==27 and payB==48 and payA+payB==75
proof['4']={'A':int(payA),'B':payB,'total':int(payA+payB),'BException':'2009 arrival precedes 2010 airfield -> no reduction','period':'actual residence2024'}
vals=[25*F(11,10),20*F(13,10),F(25)];assert vals[0]>vals[1]>vals[2];proof['5']={'payments':list(map(str,vals)),'order':['甲','乙','丙']}
proof['6']=json.loads((A/'cube-proof.json').read_text(encoding='utf-8'));assert proof['6']['minimum']==24 and proof['6']['counts'][-1]==162913
# Enumerate every possible distinct first four moves, then apply copy/period constraints and state transition.
moves=['scissors','rock','paper','thumb'];wins={('rock','scissors'),('paper','rock'),('thumb','paper'),('scissors','thumb')};solutions=[]
for first in it.permutations(moves):
 B=list(first)+list(first[:2]);G=['scissors']+B[:-1]
 if G[2]!='thumb' or G[5]!='paper' or B[3]!='scissors':continue
 state='draw';history=[]
 for a,b in zip(G,B):
  if a==b:state='draw'
  elif (a,b) in wins:state='A'
  elif (b,a) in wins:state='B'
  history.append(state)
 solutions.append(dict(A=G,B=B,winners=history,Bwins=history.count('B')))
assert len(solutions)==1 and solutions[0]['winners']==['draw','B','B','A','A','B'];proof['7']=solutions[0]
people=[('A',76,True,None),('B',63,False,'hepatitis'),('C',66,True,'diabetes'),('D',68,False,'asthma'),('E',78,False,'hypertension')]
paid={name:F(20 if age>=75 else 10,2 if prior else 1) for name,age,prior,disease in people if age>=65 and disease not in ['asthma','hypertension']};assert paid=={'A':10,'C':5};proof['8']={'recipients':list(paid),'payments':{k:int(v) for k,v in paid.items()},'total':int(sum(paid.values()))}
proof['9']={'truth':[False,False,False,False,True],'scope':'textual trend;not individual diagnostic or universal causal guarantee'}
f90=500*F(1,5)*F(1,2);total00=f90*4;assert f90==50 and total00==200 and total00/F(2,5)==500
proof['10']={'commonFemaleExperienced':int(f90),'all2000Experienced':int(total00),'all2000PopulationNotAsked':500,'unit':'10thousand people'}
with pdfplumber.open(next((R/'artifacts/psat600_20261028/sources/6001').glob('*.pdf'))) as pdf:
 t=next(p.extract_text() for p in pdf.pages if '영역 상황판단' in p.extract_text());assert '2025' in t and '혁' in t;keys={}
 for line in t.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
   v=list(map(int,line.split()));keys.update(zip(v[::2],v[1::2]))
 assert len(keys)==25
norm=lambda s:re.sub(r'[\s·]+','',s)
for q in bank:
 n=q['number'];src=tr[q['id']];assert norm(q['prompt'])==norm(src['prompt']) and all(norm(x)==norm(y) for x,y in zip(q['choices'],src['choices'])),(n,'prompt/choices')
 if n==4:
  assert norm(q['body'])==norm(src['body'].split('군용비행장 2024년 실제',1)[0]);assert q['tables'][0]['rows']==[['甲','제2종 구역','2010. 3. 29.','2015. 1. 7.','1. 1. ～ 12. 31.'],['乙','제1종 구역','2010. 3. 29.','2009. 1. 7.','1. 1. ～ 8. 31.']]
 elif n==7:
  pre,rest=src['body'].split('구분 1회차',1);unused,post=rest.split('○ 甲은',1);assert norm(q['body'])==norm(pre+'○ 甲은'+post);assert q['tables'][0]['rows']==[['甲','가위','?','엄지척','?','?','보'],['乙','?','?','?','가위','?','?']]
 elif n==8:
  pre,rest=src['body'].split('연령 지원금액',1);unused,post=rest.split('※ 단,',1);post=post.split('구분 A B C D E',1)[0];assert norm(q['body'])==norm(pre+'※ 단,'+post)
  assert q['tables'][0]['rows']==[['65세 이상 75세 미만','접종비용 반액'],['75세 이상','접종비용 전액']]
  assert q['tables'][1]['rows']==[['A','76세','있음','－'],['B','63세','없음','간염'],['C','66세','있음','당뇨'],['D','68세','없음','천식'],['E','78세','없음','고혈압']]
 else:assert norm(q['body'])==norm(src['body']),(n,'body')
 assert q['answer']==keys[n] and len(q['steps'])==len(q['optionReasons'])==5,(n,q['answer'],keys[n])
 for s,prefix in zip(q['steps'],['착안점: ','실전 풀이: ','답 확정 기준: ','정석 근거: ','적용 한계: ']):assert s.startswith(prefix) and len(s)>40
 assert not any('\ue000'<=c<='\uf8ff' or c in '\ufffd\u2060\u2024' for c in json.dumps(q,ensure_ascii=False)),n
assert bank[8]['body']==bank[9]['body'].split('\n\n<상황>')[0]
for c in json.loads((A/'crop-manifest.json').read_text(encoding='utf-8')):
 source=R/c['source'];assert hashlib.sha256(source.read_bytes()).hexdigest()==c['sha256']
 with pdfplumber.open(source) as pdf:
  ref=pdf.pages[c['page1based']-1].crop(c['rect']).to_image(resolution=c['resolution'],antialias=True).original.convert('RGB');path=R/c['asset'] if P.exists() else A/'staged'/c['asset'];im=Image.open(path).convert('RGB');assert im.size==ref.size and im.tobytes()==ref.tobytes(),c['asset']
seen=set();old=0
for path in (R/'assets/psat').glob('*.json'):
 if path.name in ['sets.json','situation11.json']:continue
 obj=json.loads(path.read_text(encoding='utf-8'))
 if isinstance(obj,list):
  for q in obj:
   k=(q.get('examDate',q['source'][:10].replace('.','-')),q['subject'],q['number']);assert k not in seen;seen.add(k);old+=1
for q in bank:
 k=(q['examDate'],q['subject'],q['number']);assert k not in seen;seen.add(k)
for path,digest in json.loads((A/'before-situation11-hashes.json').read_text(encoding='utf-8')).items():
 if path!='assets/psat/sets.json':assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
proof.update(status='PASS',count=10,officialFinalKeys=10,sourceComparison='nativeprompt/body/choices;4tables;completecommonpassage;10originalpixelcomparisons',preservedExisting=old,limitations='Same-author semantic review and exhaustive/exact models;not independent expert certification.')
(A/'content-checks.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PASS10source/key/original;models;preserved',old)
