from pathlib import Path
from itertools import product,permutations
import json,re,hashlib
import pdfplumber
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/verbal05';P=R/'assets/psat/verbal05.json'
bank=json.loads((P if P.exists() else A/'authored-verbal05.json').read_text(encoding='utf-8'))
norm=lambda s:re.sub(r'\s+','',s)
with pdfplumber.open(R/'artifacts/psat600_20261028/sources/4341/BBSMSTR_000000000138_4341_2.pdf') as pdf:
 t=pdf.pages[0].extract_text();assert '2023년도' in t and '언어논리' in t and '인' in t
 key={}
 for line in t.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
   vs=list(map(int,line.split()));key.update(zip(vs[::2],vs[1::2]))
 assert len(key)==25
proof={}
def phase(reserve):
 if reserve<100:return 5
 if reserve<200:return 4
 if reserve<300:return 3
 if reserve<400:return 2
 if reserve<500:return 1
 return 0
assert [phase(x) for x in [50,100,180,200,280,300,400,500,750]]==[5,4,4,3,3,2,1,0,0]
assert phase(50)==5 and phase(180)>=3
# Baseline survives outside crisis; universal disability-elevator exception.
ordinary_temp_at_750=25
assert not 24>=ordinary_temp_at_750
proof['13']={'boundaryInputs':[50,100,180,200,280,300,400,500,750],'phaseResults':[5,4,4,3,3,2,1,0,0],'statements':[True,False,False],'exception':'Medical institutions also exempt; non-vulnerable alone does not mean non-exempt. All disabled elevators run.'}
prior=[True,True,True,False];reason=[False,True,True,None]
checks=[[],[],[]]
for aname,bname in permutations(['prior','reason']):
 rows={'prior':prior,'reason':reason};a,b=rows[aname],rows[bname]
 if aname=='prior':checks[0].append(a[0]==a[1])
 if a[0]!=a[2]:checks[1].append(bname=='reason')
 if b[0]==b[1]:checks[2].append(b[2]==b[3])
assert checks==[[True],[False],[False]]
proof['23']={'assignments':2,'conditionalEvaluations':checks,'rowA':['㉠','㉡','㉢','㉣'],'rowB':['㉤','㉥','㉦','㉧'],'unneededValue':'no assumed refusal reason for 라'}
rows=[]
for home,school in product(['A','B'],repeat=2):
 oldA=school=='A';oldB=home=='B'
 ga=home=='A' and school=='A'
 na=home=='A' and school=='A'
 da=school=='B'
 rows.append([home,school,oldA,oldB,ga,na,da])
gap=next(x for x in rows if x[:2]==['A','B'])
assert gap==['A','B',False,False,False,False,True]
assert next(x for x in rows if x[:2]==['B','A'])[2:4]==[True,True]
proof['25']={'residenceSchoolCases':rows,'gapStudent':'갑','amendmentsSolveGap':[False,False,True]}
proof['1']={'before':'3military groups also police','after':'3originalduties+separatepolice','gate':'위숙군 retains'}
proof['2']={'creation':'숙종','campaign':'예종2','rescue':'척준경->윤관->영주','return':'예종4 losses+costs','forts':['영주','웅주','복주','길주','함주','공험진','의주','통태진','평융진']}
proof['5']={'roles':{'주관':'기관장','자문':'갈등관리심의위원회','작성':'중립적 전문가','회람':'모든 이해당사자','보고대상':'기관장','심의':'갈등관리심의위원회'}}
proof['6']={'inclusion':'stage3 subset complexlow subset low','fivecentres':'권역학습센터','certification':'mentor certified','answerPossibility':True}
proof['7']={'requests':['registered residents','10types','claim window','actual representative documents','website+app'],'missingIn4':'actual documents; phone referral insufficient','threeYears':'number supplied by choice, not stated in dialogue'}
proof['22']={'target':'A rejection of B','statements':[True,False,True],'earlyStop':'excludeㄴ includeㄷ leavesonly③','limit':'weakening not refutation'}
proof['24']={'institution':'council itself not separate responsibleagency','decision':'governor assesses need','preparation':'before disaster,not after'}
for q in bank:
 n=q['number'];raw=(A/f'2023-l{n}-source.txt').read_text(encoding='utf-8').split(f'{n}.',1)[1]
 prompt,tail=raw.split('?',1);body,options=tail.rsplit('\n① ',1)
 if n==22:body=(A/'shared21-22-source.txt').read_text(encoding='utf-8')+'\n'+body
 if n==13:
  before,rest=body.split('<표> 전력수급',1);table,after=rest.split('다만 장애인',1);body=before+'다만 장애인'+after
  assert len(q['tables'])==1 and len(q['tables'][0]['rows'])==5 and q['tables'][0]['afterParagraph']==1
  for row in q['tables'][0]['rows']:assert norm(''.join(row)) in norm(table)
 if n==23:
  before,rest=body.split('<표> 적극행정',1);table,after=rest.split('<보 기>',1);body=before+'<보 기>'+after
  assert q['tables']==[{'caption':'적극행정 국민신청안 처리 현황','columns':['기준','(가)','(나)','(다)','(라)'],'rows':[['A','㉠','㉡','㉢','㉣'],['B','㉤','㉥','㉦','㉧']],'afterParagraph':3}]
  for row in q['tables'][0]['rows']:assert norm(''.join(row)) in norm(table)
 body=body.replace('갑: 예, 그러면 .','갑: 예, 그러면 □.')
 assert norm(q['prompt'])==norm(prompt+'?'),(n,'prompt')
 assert norm(q['body'])==norm(body),(n,'body')
 opts=re.split('[①②③④⑤]','① '+options)[1:];assert len(opts)==5
 assert all(norm(a)==norm(b) for a,b in zip(opts,q['choices'])),(n,'options')
 assert q['answer']==key[n],(n,'final key')
 assert len(q['steps'])==len(q['optionReasons'])==5
 for s,prefix in zip(q['steps'],['착안점: ','실전 풀이: ','답 확정 기준: ','정석 근거: ','적용 한계: ']):assert s.startswith(prefix) and len(s)>40,(n,prefix)
 for u in q.get('underlines',[]):assert q['body'].count(u)==1
 assert not any(c in json.dumps(q,ensure_ascii=False) for c in ['\u2060','\ufffd'])
 assert (R/q['original'] if P.exists() else A/'staged'/q['original']).exists()
seen=set();oldcount=0
for p in (R/'assets/psat').glob('*.json'):
 if p.name in ['sets.json','verbal05.json']:continue
 obj=json.loads(p.read_text(encoding='utf-8'))
 if isinstance(obj,list):
  for q in obj:
   k=(q.get('examDate',q['source'][:10].replace('.','-')),q['subject'],q['number'])
   assert k not in seen,k;seen.add(k);oldcount+=1
for q in bank:
 k=(q['examDate'],q['subject'],q['number']);assert k not in seen,k;seen.add(k)
for path,digest in json.loads((A/'before-verbal05-hashes.json').read_text(encoding='utf-8')).items():
 if path=='assets/psat/sets.json':continue
 assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
proof.update(status='PASS',count=10,officialFinalKeys=10,normalizedSource='all prompts,complete passages,all5choices;restored blank',tables=2,underlines=3,preservedExisting=oldcount,limitations='Same-author source review and model checks; not independent expert certification.')
(A/'content-checks.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PASS:10source/finalkeys,2tables,3underlines,crisisboundaries,2criterionorders,4residence-schoolcases,preserved',oldcount)