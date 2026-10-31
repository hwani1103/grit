from pathlib import Path
from collections import Counter
from fractions import Fraction as F
from itertools import product
import json,re,hashlib,pdfplumber
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/situation06';P=R/'assets/psat/situation06.json'
bank=json.loads((P if P.exists() else A/'authored-situation06.json').read_text(encoding='utf-8'));norm=lambda s:re.sub(r'\s+','',s)
with pdfplumber.open(next((R/'artifacts/psat600_20261028/sources/5994').glob('*.pdf'))) as pdf:
 text=next(p.extract_text() for p in pdf.pages if '영역 상황판단' in p.extract_text());assert '2025년도' in text and '인 책형' in text
 key={}
 for line in text.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
   vs=list(map(int,line.split()));key.update(zip(vs[::2],vs[1::2]))
 assert len(key)==25
proof={'1':{'delegation':True,'requestIncludesBusinesses':True,'publicationCondition':'survey not mere data collection','fee':'may; provision cost not economicvalue'},'2':{'governmentOnly':True,'excluded':'greenclimatefundcontribution','selfReview':'agencyhead','submit':'March31 tocommittee','forward':'May31 tominfinance'},'3':{'panelSizes':[3,5],'majorities':[2,3],'directorCanChairImportant':True,'oralRequestException':'written sufficient','disclosureRule':'oralnotwritten'},'4':{'medical':'specialists AND (mutual OR insurance)','nonmedical':'guaranteeinsurance AND domesticOffice','renewal':'beforeexpiry3years'},'5':{'sourceReadingOnly':True,'saltfieldNaturalEvaporation':True,'Mapo':'distribution notproduction'}}
assert all(a for a,b in product([False,True],repeat=2) if (a or b) and not b)
solutions=[(x,x+2) for x in range(16) if 1000*(2*x+2)+3000==15000];assert solutions==[(5,7)]
proof['6']={'solutions':solutions,'choicePayments':[1000*(2*x+2)+3000 for x in [5,6,7,8,9]],'dumplingCharge':0}
base=Counter(dict(zip('ABCDE',[2,0,3,5,5])));options=['ABBCB','BABBC','BADBD','CBBBD','DBECA']
def valid(s):
 counts=base+Counter(s);tail='AA'+s
 return all(2<=counts[k]<=6 for k in 'ABCDE') and all(len(set(tail[i:i+3]))>1 for i in range(len(tail)-2))
validopts=[valid(s) for s in options];assert validopts==[False,True,False,False,False]
allvalid=[''.join(s) for s in product('ABCDE',repeat=5) if valid(''.join(s))]
assert 'BABBC' in allvalid
proof['7']={'testedAllTails':3125,'validTailCount':len(allvalid),'choiceValidity':validopts,'answerCounts':dict(base+Counter('BABBC')),'boundaryIncluded':True}
rows=bank[7]['tables'][0]['rows'];eligible=[]
for name,res,projector,seats,snack in rows:
 ok=(res=='없음' or res=='11:00～12:30') and projector=='○' and int(seats[:-1])>=43
 if ok:eligible.append(name)
assert eligible==['C','E'] and next(r for r in rows if r[0]=='E')[-1]=='○'
proof['8']={'mandatorySurvivors':eligible,'priorityWinner':'E','overlapA':'14:00-15:00'}
truth=[False,True,True,False];assert [i+1 for i,c in enumerate([[0,1],[0,3],[1,2],[1,3],[2,3]]) if set(c)=={i for i,t in enumerate(truth) if t}]==[3]
proof['9']={'truth':truth,'specialcash':'inability AND equivalentfamilyservice','lowincome':'costexemption notsoleeligibility'}
amounts={'甲':(70000*10+300000)*F(15,100),'乙':0,'丙':70000*11*F(20,100)};assert amounts=={'甲':150000,'乙':0,'丙':154000};assert sorted(amounts,key=amounts.get,reverse=True)==['丙','甲','乙']
proof['10']={'amounts':{k:int(v) for k,v in amounts.items()},'difference':4000,'exemptBillUnnecessary':1010000}
for q in bank:
 n=q['number'];raw=(A/f'2025-s{n}-source.txt').read_text(encoding='utf-8').split(f'{n}.',1)[1];prompt,tail=raw.split('?',1);body,opts=tail.rsplit('\n① ',1)
 if n in [9,10]:body=(A/'shared9-10-source.txt').read_text(encoding='utf-8')+'\n'+body
 tables=q['tables']
 if n==7:
  body,table=body.split('\n정답 A B C D E',1)
  assert '문항개수20355' in norm(table) and tables[0]['columns']==['정답','A','B','C','D','E'] and tables[0]['rows']==[['문항 개수','2','0','3','5','5']]
  assert tables[0]['afterParagraph']==3 and '16번17번18번19번20번' in norm(table)
 if n==8:
  body,table=body.split('\n세미나 당일 프로젝터',1)
  for row in tables[0]['rows']:assert norm(''.join(row)) in norm(table),row
  assert tables[0]['afterParagraph']==4
 if n==10:
  before,rest=body.split('\n급여 유형 급여 내용 급여비용',1);t1,middle=rest.split('○ 노인장기요양보험제도 수급자',1);middle,t2=middle.split('\n수급자 수급 내역 비고',1);body=before+'\n○ 노인장기요양보험제도 수급자'+middle
  assert len(tables)==2 and [t['afterParagraph'] for t in tables]==[5,6]
  for row in tables[0]['rows']:assert norm(''.join(row[1:])) in norm(t1),row
  assert [r[0] for r in tables[0]['rows']]==['재가급여']*4+['시설급여']+['복지용구급여']*2
  assert tables[1]['rows']==[['甲','방문목욕 10회, 복지용구(전동침대) 구입','전동침대 구입비 30만 원'],['乙','주ㆍ야간보호 45시간, 방문요양 28시간','국민기초생활보장대상자'],['丙','노인요양시설 보호 11일','－']]
  assert re.findall(r'\d+',t2)==['10','30','45','28','11']
 assert norm(q['prompt'])==norm(prompt+'?'),(n,'prompt')
 assert norm(q['body'])==norm(body),(n,'body')
 options=re.split('[①②③④⑤]','① '+opts)[1:];assert len(options)==5 and all(norm(a)==norm(b) for a,b in zip(options,q['choices'])),(n,'choices')
 assert q['answer']==key[n] and len(q['steps'])==len(q['optionReasons'])==5
 for s,prefix in zip(q['steps'],['착안점: ','실전 풀이: ','답 확정 기준: ','정석 근거: ','적용 한계: ']):assert s.startswith(prefix) and len(s)>40
 assert not any(c in json.dumps(q,ensure_ascii=False) for c in ['\u2060','\ufffd'])
 assert (R/q['original'] if P.exists() else A/'staged'/q['original']).exists()
seen=set();old=0
for p in (R/'assets/psat').glob('*.json'):
 if p.name in ['sets.json','situation06.json']:continue
 obj=json.loads(p.read_text(encoding='utf-8'))
 if isinstance(obj,list):
  for q in obj:
   k=(q.get('examDate',q['source'][:10].replace('.','-')),q['subject'],q['number']);assert k not in seen;seen.add(k);old+=1
for q in bank:
 k=(q['examDate'],q['subject'],q['number']);assert k not in seen;seen.add(k)
for path,digest in json.loads((A/'before-situation06-hashes.json').read_text(encoding='utf-8')).items():
 if path!='assets/psat/sets.json':assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
proof.update(status='PASS',count=10,officialFinalKeys=10,source='complete passages,5choices,4tables,shared9-10',preservedExisting=old,limitations='Same-author review; not independent expert certification.')
(A/'content-checks.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PASS10,4tables,3125tails,feeexactmodel,preserved',old)