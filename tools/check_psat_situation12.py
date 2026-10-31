from pathlib import Path
import json,re,hashlib,itertools as it,pdfplumber
from fractions import Fraction as F
from PIL import Image
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/situation12';P=R/'assets/psat/situation12.json';bank=json.loads((P if P.exists() else A/'authored-situation12.json').read_text(encoding='utf-8'));tr=json.loads((A/'source-transcripts.json').read_text(encoding='utf-8'));proof={}
assert [q['number'] for q in bank]==list(range(11,21))
assert 10//2+1==6 and 6//2+1==4 and 12>=10
proof['11']={'truth':[False,False,True,False,False],'meeting10Needs':6,'attendees6NeedVotes':4,'qualification':'10years OR associate professor;secretaries not members'}
T,Rm,H=100,10,3
assert F(T,10)<=Rm<=F(3*T,10) and H>=F(3*Rm,10) and H<F(3*T,10)
proof['12']={'answer':1,'option5Counterexample':{'tuition':T,'totalRelief':Rm,'hardshipRelief':H},'denominator':'total relief,not total tuition'}
paid=[]
for year in range(2022,2025):
 for month in range(1,13):
  if (2022,2)<=(year,month)<=(2022,8) or (2024,2)<=(year,month)<=(2024,7):paid.append(f'{year}-{month:02}')
assert len(paid)==13 and len(paid)*5==65
proof['13']={'paidMonths':paid,'totalManWon':65,'boundary':'selection next month;leave stop next month;return same month;retire stop next month'}
proof['14']={'truth':[False,False,True,True],'exports':['silk','musk','cinnamon'],'imports':['glassware','wool'],'evidence':'settlement record;island depiction;no similar Chinese tomb statue'}
passwords=[''.join(c) for c in it.combinations('abcdefghijklmn',5) if c[0] in 'aei' and c[2] in 'aei' and c[1] not in 'aei' and c[4] not in 'aei']
assert passwords and 'abeij' in passwords and 'abijk' in passwords
truth=[not any(s[3]=='i' for s in passwords),any(s[4]=='f' for s in passwords),any(s[1]=='g' and s[3]=='i' for s in passwords),all(s[1]=='h' for s in passwords if s[2]=='i'),all(s[0]=='a' for s in passwords if s[4]=='j')]
assert truth==[False,False,False,False,True]
proof['15']={'validCount':len(passwords),'truth':truth,'counterexamples':['abeij','abijk'],'allEndingJ':[s for s in passwords if s[4]=='j']}
matches=[]
for x,y,z in it.product(range(25),repeat=3):
 if x>9:continue
 if len({25,y,z})!=2:continue
 if 25+y+z!=50+x+9:continue
 # Two equal B totals must be the two losses; 25 cannot equal either losing score.
 if y!=z:continue
 for lossPosition in [0,1]:
  a=[25,25];b=[y,z];a.insert(lossPosition,x);b.insert(lossPosition,25)
  assert sum(v==25 for v in a)==2 and not(a[0]==a[1]==25)
  matches.append({'A':a,'B':b,'totalB':sum(b)})
assert max(m['totalB'] for m in matches)==67
proof['16']={'allMatches':matches,'maxB':67,'witness':{'A':[8,25,25],'B':[25,21,21]}}
ages={}
for minAge in [0,1]:
 choices=[list(reversed(c)) for c in it.combinations(range(minAge,23),4) if sum(c)==22]
 assert max(c[2] for c in choices)==6
 ages[str(minAge)]={'count':len(choices),'maximumFirstSon':6,'witness':[8,7,6,1]}
proof['17']=ages
people=[(40,300,1,True),(25,80,2,False),(75,100,2,False),(45,70,1,False),(71,150,3,True)]
def income_score(x):return 12 if x<80 else 9 if x<140 else 6 if x<200 else 3 if x<300 else 0
scores=[income_score(m)+min(k,3)*2+int(a>=70)+int(r) for a,m,k,r in people]
assert scores==[3,13,14,14,14];winner=max(range(5),key=lambda i:(scores[i],-people[i][1]));assert winner==3
proof['18']={'scores':scores,'ties':['丙','丁','戊'],'tieIncomes':[100,70,150],'winner':'丁'}
fac={'A':(200,250,1800),'B':(250,300,2000),'C':(600,400,3600),'D':(450,350,2500),'E':(350,200,2000)};plans=[['C','C',3600]]
for ex,se in it.permutations(fac,2):
 if fac[ex][0]<300 or fac[se][1]<200:continue
 price=sum(fac[x][2] for x in [ex,se])
 if {ex,se}=={'A','D'}:price-=750
 if {ex,se}=={'B','E'}:price-=500
 plans.append([ex,se,price])
assert min(plans,key=lambda p:p[2])==['E','B',3500] and sum(p[2]==3500 for p in plans)==1
proof['19']={'validPlans':plans,'minimum':['E','B',3500],'choiceCosts':[None,3600,3550,4500,3500]}
cars=[[8,8,7,9],[7,7,10,8],[10,6,7,7],[8,7,10,7],[7,9,9,7]];tot=list(map(sum,cars));assert tot==[32,32,30,32,32]
assert max(range(5),key=lambda i:(tot[i],cars[i][0],cars[i][3]))==0
proof['20']={'scoresByCriterion':cars,'totals':tot,'firstTie':['A','B','D','E'],'manufacturerTie':['A','D'],'pricePoints':[9,7],'winner':'A'}
with pdfplumber.open(next((R/'artifacts/psat600_20261028/sources/6001').glob('*.pdf'))) as pdf:
 text=next(p.extract_text() for p in pdf.pages if '영역 상황판단' in p.extract_text());assert '2025' in text and '혁' in text;keys={}
 for line in text.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
   vals=list(map(int,line.split()));keys.update(zip(vals[::2],vals[1::2]))
 assert len(keys)==25
norm=lambda s:re.sub(r'[\s·]+','',s).replace('m²','m2')
for q in bank:
 n=q['number'];src=tr[q['id']]
 assert norm(q['prompt'])==norm(src['prompt'])
 if n==19:
  assert q['choices']==[' · '.join(c.split()) for c in src['choices']] and q['choiceNote']=='전시 → 세미나'
 else:assert all(norm(x)==norm(y) for x,y in zip(q['choices'],src['choices']))
 if n==18:
  pre,rest=src['body'].split('평가항목 세부 내용 점수',1);criteria,after=rest.split('<상 황>',1);context,tab=after.split('구분 甲 乙 丙 丁 戊',1)
  assert norm(q['body'])==norm(pre+'<상 황>'+context)
  assert q['tables'][0]['rows']==[['월 소득','80만 원 미만','12'],['월 소득','80만 원 이상 140만 원 미만','9'],['월 소득','140만 원 이상 200만 원 미만','6'],['월 소득','200만 원 이상 300만 원 미만','3'],['월 소득','300만 원 이상','0'],['최근 3년간 예술활동 수행실적','0건','0'],['최근 3년간 예술활동 수행실적','1건','2'],['최근 3년간 예술활동 수행실적','2건','4'],['최근 3년간 예술활동 수행실적','3건 이상','6']]
  assert q['tables'][1]['rows']==[['70세 이상','1'],['농어촌지역 거주','1']]
  assert q['tables'][2]['rows']==[['甲','40세','300','1건','거주'],['乙','25세','80','2건','비거주'],['丙','75세','100','2건','비거주'],['丁','45세','70','1건','비거주'],['戊','71세','150','3건','거주']]
  for line in ['연령40세25세75세45세71세','월소득(만원)3008010070150','1건2건2건1건3건']:assert line in norm(tab)
 elif n==19:
  assert norm(q['body'])==norm(src['body'].split('면적 정원 사용료',1)[0])
  rows=q['tables'][0]['rows']
  assert [r[:4] for r in rows]==[['A','200','250','1,800'],['B','250','300','2,000'],['C','600','400','3,600'],['D','450','350','2,500'],['E','350','200','2,000']]
  assert norm(rows[2][4]) in norm(src['body']).replace('C6004003,600','')
  assert norm(rows[3][4]) in norm(src['body']).replace('D4503502,500','')
  assert norm(rows[4][4]) in norm(src['body']).replace('E3502002,000','')
 elif n==20:
  pre,rest=src['body'].split('제조사 甲 乙 丙 丁',1);criteria,after=rest.split('<상 황>',1);context,tab=after.split('구분 제조사 크기 색상 가격(만 원)',1)
  assert norm(q['body'])==norm(pre+'<상 황>'+context)
  assert q['tables'][0]['rows']==[['甲','10'],['乙','8'],['丙','8'],['丁','7']]
  assert q['tables'][1]['rows']==[['대형','7'],['중형','8'],['준중형','9'],['소형','6']]
  assert q['tables'][2]['rows']==[['흰색','10'],['검은색','10'],['회색','7'],['파란색','9']]
  assert q['tables'][3]['rows']==[['1,000만 원 이상 2,500만 원 미만','9'],['2,500만 원 이상 4,000만 원 미만','8'],['4,000만 원 이상','7']]
  for row,line in zip(q['tables'][4]['rows'],tab.strip().splitlines()):assert norm(''.join(row))==norm(line)
 else:assert norm(q['body'])==norm(src['body']),(n,'body')
 assert q['answer']==keys[n] and len(q['steps'])==len(q['optionReasons'])==5,(n,q['answer'],keys[n])
 for s,prefix in zip(q['steps'],['착안점: ','실전 풀이: ','답 확정 기준: ','정석 근거: ','적용 한계: ']):assert s.startswith(prefix) and len(s)>40
 assert not any('\ue000'<=c<='\uf8ff' or c in '\ufffd\u2060\u2024' for c in json.dumps(q,ensure_ascii=False)),n
for c in json.loads((A/'crop-manifest.json').read_text(encoding='utf-8')):
 source=R/c['source'];assert hashlib.sha256(source.read_bytes()).hexdigest()==c['sha256']
 with pdfplumber.open(source) as pdf:
  ref=pdf.pages[c['page1based']-1].crop(c['rect']).to_image(resolution=c['resolution'],antialias=True).original.convert('RGB');path=R/c['asset'] if P.exists() else A/'staged'/c['asset'];im=Image.open(path).convert('RGB');assert im.size==ref.size and im.tobytes()==ref.tobytes(),c['asset']
seen=set();old=0
for path in (R/'assets/psat').glob('*.json'):
 if path.name in ['sets.json','situation12.json']:continue
 obj=json.loads(path.read_text(encoding='utf-8'))
 if isinstance(obj,list):
  for q in obj:
   k=(q.get('examDate',q['source'][:10].replace('.','-')),q['subject'],q['number']);assert k not in seen;seen.add(k);old+=1
for q in bank:
 k=(q['examDate'],q['subject'],q['number']);assert k not in seen;seen.add(k)
for path,digest in json.loads((A/'before-situation12-hashes.json').read_text(encoding='utf-8')).items():
 if path!='assets/psat/sets.json':assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
proof.update(status='PASS',count=10,officialFinalKeys=10,sourceComparison='native prompt/body/choices;9tables;10originalpixelcomparisons',preservedExisting=old,limitations='Same-author semantic review and exhaustive/exact models;not independent expert certification.')
(A/'content-checks.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PASS10source/key/original;models;preserved',old)
