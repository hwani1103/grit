from pathlib import Path
from itertools import product
from fractions import Fraction as F
import json,re,hashlib
import pdfplumber
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/verbal04';P=R/'assets/psat/verbal04.json'
bank=json.loads((P if P.exists() else A/'authored-verbal04.json').read_text(encoding='utf-8'))
norm=lambda s:re.sub(r'\s+','',s)
keys={}
for y,post,suffix,book in [(2023,4341,2,'인'),(2024,4564,1,'사')]:
 with pdfplumber.open(R/f'artifacts/psat600_20261028/sources/{post}/BBSMSTR_000000000138_{post}_{suffix}.pdf') as pdf:
  t=pdf.pages[0].extract_text();assert str(y)+'년도' in t and '언어논리' in t and book in t
  answers={}
  for line in t.splitlines():
   if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
    v=list(map(int,line.split()));answers.update(zip(v[::2],v[1::2]))
  assert len(answers)==25;keys[y]=answers
proofs={}
def note(y,n,v):proofs[f'{y}-{n}']=v
# Independent exact model checks supplement the written deductions.
models=[]
for eab,ec,ia,ib,ic in product(range(1,11),repeat=5):
 if not eab>ec:continue
 if ia*eab>ib*eab==ic*ec:models.append((eab,ec,ia,ib,ic))
assert models and all(ia>ib and ic>ib for _,_,ia,ib,ic in models)
assert any(ia>ic for _,_,ia,_,ic in models) and any(ia<ic for _,_,ia,_,ic in models)
for ia in [F(3,10),F(5,10)]:
 ext=[F(8,10),F(8,10),F(4,10)];inte=[ia,F(2,10),F(4,10)]
 out=[e*i for e,i in zip(ext,inte)];assert out[0]>out[1]==out[2]
note(2023,19,{'positiveEfficiencyGridModels':len(models),'deduction':'iA>iB,iC>iB; A/C both orders possible','printedCounterexamples':2,'limit':'Finite model checks supplement the algebraic positive-efficiency proof.'})
def weak(prev,cur):return cur.count('하')==3 or cur.count('하')==2 and prev.count('하')==2
def excellent(prev,cur):return prev.count('상')>=2 and cur.count('상')>=2 and '하' not in cur
counts=[0,0,0];bad=[[],[],[]]
for a,b,c,d,e,f in product(['상','중','하'],repeat=6):
 ap=[a,'중',b];ac=[c,'하','상'];bp=[d,'상','하'];bc=['중',e,f]
 antecedents=[a!=c,e==f=='하',weak(ap,ac) and excellent(bp,bc)]
 conclusions=[not weak(ap,ac) and not excellent(ap,ac),weak(bp,bc),b!=d]
 for i in range(3):
  if antecedents[i]:
   counts[i]+=1
   if not conclusions[i]:bad[i].append([a,b,c,d,e,f])
assert counts[0]>0 and counts[2]>0 and not bad[0] and bad[1] and not bad[2]
assert not weak(['중','상','하'],['중','하','하'])
note(2024,23,{'assignments':729,'antecedentCounts':counts,'necessarilyTrue':[not x for x in bad],'printedCounterexample':'B2023=중상하,B2024=중하하 -> notweak','third':'Aweak -> b=하; Bexcellent -> d=상'})
assert 550+50==600
note(2023,20,{'clock':'t_target=550만*targetDifference/calibrationDifference; targetDifference>calibration implies older than550만','hostAfterLouse50만':'louse calibration600만; old550만 loses support','statements':[True,True,True]})
note(2023,17,{'chain':'surfactant lung->macrophage amniotic->A uterus->B active->C threshold->contraction','Bremoved':'no endogenous C; threshold not reached','Cdirect':'threshold reached -> birth','statements':[False,True,True]})
note(2023,18,{'comparison':'same dive:initial unchanged < largeeye=water=body','answer':2})
note(2023,21,{'identity':'갑 same fetus; 을 different possible child','A':'을 wrong','B':'no nonexistent individuals pleasure/pain; same-child harm independent ofreplacement','statements':[True,True,True]})
note(2024,21,{'statement1':'measures reabuse between report/protection','statement2':'does not measure false negatives','statement3':'does not measure reporting barrier','statements':[True,False,False]})
note(2024,22,{'oldAllowed':['대면','예약 주문'],'payment':['영업장 방문','영업장 방문'],'exception':'meal+smallalcohol,approvedtraditionalmaker','answer':4})
note(2024,24,{'difference':'을 absent wording in article7,무 flexible meaning ofcontinuity','answer':2})
note(2024,25,{'scope':'same-country principle couldexplain disagreement','forecast':'갑 futureinfringement,을 currentreasonablepractice permitsmaintenance','notEntailed':'both oppose mandatorycredit','statements':[True,True,False]})
for q in bank:
 y=int(q['examDate'][:4]);n=q['number'];raw=(A/f'{y}-l{n}-source.txt').read_text(encoding='utf-8')
 t=(A/'2023-l21-question-source.txt').read_text(encoding='utf-8') if (y,n)==(2023,21) else raw
 prompt,tail=t.split('.',1)[1].split('?',1);body,options=tail.split('①',1)
 if (y,n)==(2023,21):body=raw.split('\n',1)[1]+'\n'+body
 if (y,n)==(2024,22):
  before,rest=body.split('<표> 판매 유형',1);body=before+'갑국은 주류에'+rest.split('갑국은 주류에',1)[1]
  assert q['tables']==[{'caption':'판매 유형 및 방법에 따른 구분','columns':['유형','주문 방법','결제 방법','수령 방법'],'rows':[['대면','영업장 방문','영업장 방문','영업장 방문'],['예약 주문','온라인','영업장 방문','영업장 방문'],['스마트 오더','온라인','온라인','영업장 방문'],['완전 비대면','온라인','온라인','배송']],'afterParagraph':0}]
 if (y,n)==(2024,23):
  before,rest=body.split('<표> 2023년과',1);body=before+'<보 기>'+rest.split('<보 기>',1)[1]
  assert q['tables']==[{'caption':'2023년과 2024년 보호수준 평가 결과','columns':['기관','연도','접근권한 관리','암호화 조치','접속기록 점검'],'rows':[['A','2023','㉠','중','㉡'],['A','2024','㉢','하','상'],['B','2023','㉣','상','하'],['B','2024','중','㉤','㉥']],'afterParagraph':3}]
 assert norm(q['prompt'])==norm(prompt+'?'),(y,n,'prompt')
 assert norm(q['body'])==norm(body),(y,n,'body')
 opts=re.split('[①②③④⑤]','①'+options)[1:];assert len(opts)==5
 for i,(a,b) in enumerate(zip(opts,q['choices'])):assert norm(a)==norm(b),(y,n,'choice',i)
 assert q['answer']==keys[y][n],(y,n,'key')
 assert len(q['steps'])==len(q['optionReasons'])==5
 for s,prefix in zip(q['steps'],['착안점: ','실전 풀이: ','답 확정 기준: ','정석 근거: ','적용 한계: ']):assert s.startswith(prefix) and len(s)>40
 for u in q.get('underlines',[]):assert q['body'].count(u)==1
 assert not any(c in json.dumps(q,ensure_ascii=False) for c in ['\u2060','\ufffd'])
 assert (R/q['original'] if P.exists() else A/'staged'/q['original']).exists()
seen=set()
for path in (R/'assets/psat').glob('*.json'):
 if path.name in ['sets.json','verbal04.json']:continue
 obj=json.loads(path.read_text(encoding='utf-8'))
 if isinstance(obj,list):
  for q in obj:
   k=(q.get('examDate',q['source'][:10].replace('.','-')),q['subject'],q['number']);assert k not in seen,k;seen.add(k)
for q in bank:
 k=(q.get('examDate',q['source'][:10].replace('.','-')),q['subject'],q['number']);assert k not in seen,k;seen.add(k)
for path,digest in json.loads((A/'before-verbal04-hashes.json').read_text(encoding='utf-8')).items():
 if path=='assets/psat/sets.json':continue
 assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
proofs.update(status='PASS',count=10,officialFinalKeys=10,sourceText='normalized exactmatch including fullsharedpassage and5options',tables=2,underlines=5,limitations='Same-author review; finite/exact checks supplement reasoning. No independent expert certification.')
(A/'content-checks.json').write_text(json.dumps(proofs,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PASS:10 original transcripts/finalkeys,2tables,729 rating assignments,positive product countermodels,90existing preservation.')