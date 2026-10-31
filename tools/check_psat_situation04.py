from pathlib import Path
from itertools import product,permutations,combinations
from fractions import Fraction as F
from datetime import date,timedelta
import json,re,hashlib
import pdfplumber
from PIL import Image
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/situation04';P=R/'assets/psat/situation04.json';bank=json.loads((P if P.exists() else A/'authored-situation04.json').read_text(encoding='utf-8'))
norm=lambda s:re.sub(r'\s+','',s)
proofs={}
def note(y,n,answer,evidence):
 q=next(q for q in bank if q['examDate'].startswith(str(y)) and q['number']==n);assert q['answer']==answer;proofs[f'{y}-{n}']=evidence
eligible=[700000,500000,300000,500000];ratio=F(1600000,sum(eligible));allocated=[a*ratio for a in eligible]
assert allocated==[560000,400000,240000,400000] and sum(allocated)==1600000
note(2023,17,2,{'allocation':list(map(int,allocated)),'ratio':str(ratio)})
marks=[[68,68,68,68,72],[65,73,62,65,65],[73,69,69,65,69],[75,70,65,65,75],[65,60,60,70,75]]
tech=[F(sum(sorted(m)[1:-1]),3) for m in marks];assert tech==[68,65,69,70,65]
price=[13,20,15,14,17];survivors=[(tech[i]+price[i],tech[i],i) for i in range(5) if tech[i]>=F(80*85,100)]
assert max(survivors)[2]==3
note(2023,18,4,{'technicalScores':list(map(str,tech)),'tie':'丙84/tech69,丁84/tech70','strictBelowThreshold':'68 survives'})
mins=lambda s:int(s[:2])*60+int(s[3:])
rows=[('08:55','20:00',0,180,False),('08:00','19:55',0,0,False),('09:00','21:30',30,90,False),('08:30','23:30',0,0,True),('07:00','21:30',0,0,False)]
totals=[]
for start,end,personal,sat,remote in rows:
 fri=0 if remote else min(240,max(0,540-mins(start))+max(0,mins(end)-1080)-personal)
 totals.append(fri+min(120,sat))
assert totals==[245,175,270,0,240]
note(2023,19,3,{'recognizedMinutes':totals})
scorecases=[s for s in product([70,30],[70,30],[60,40],[60,40],[80,20]) if sum(s)==300 and sum(x<50 for x in s)==2]
assert scorecases==[(70,70,40,40,80)]
note(2023,20,3,{'allPossibilities':32,'solutions':scorecases,'highTotal':340,'deductions':[40,40,20,20,60]})
calendar=[]
for day1 in range(7): # Monday0
 weekday=lambda d:(day1+d-1)%7
 for wed in range(12,15):
  if weekday(wed)!=2:continue
  sunday=max(d for d in range(1,31) if weekday(d)==6);days=[5,11,wed,15,sunday-1,sunday]
  if days==sorted(days) and len(set(map(weekday,days)))==6:calendar.append((weekday(5),days))
assert calendar==[(1,[5,11,13,15,23,24])]
note(2023,21,2,{'allMonthOffsets':7,'solution':calendar})
seats=[]
for arr in permutations('甲乙丙丁'): # frontleft,frontright,backleft,backright
 pos={v:i for i,v in enumerate(arr)}
 if pos['甲']<2 or pos['丁']<2 or pos['丙']>=2:continue
 absent2={arr[pos['甲']-2]}
 if '乙' in absent2:continue
 absent3={arr[pos['丙']+2]};present4={'丁',arr[pos['丁']-2]}
 presentcounts={v:2+int(v not in absent2)+int(v not in absent3)+int(v in present4) for v in arr}
 seats.append((arr,presentcounts))
assert len(seats)==2 and all({v for v,k in c.items() if k<4}=={'甲','丙'} for _,c in seats)
note(2024,21,3,{'permutationsChecked':24,'mirrorSeats':seats})
def matchings(nums):
 if not nums:yield [];return
 a=nums[0]
 for b in nums[1:]:
  for rest in matchings([v for v in nums if v not in [a,b]]):yield [(a,b)]+rest
allpairs=list(matchings(list(range(1,11))));valid={}
for pairs in allpairs:
 ds={abs(a-b) for a,b in pairs}
 if len(ds)==1:valid.setdefault(ds.pop(),[]).append(pairs)
assert len(allpairs)==945 and sorted(valid)==[1,5]
note(2024,22,4,{'perfectMatchings':945,'commonDifferences':sorted(valid),'firstWitnessPerDifference':{str(d):m[0] for d,m in valid.items()},'difference':4})
dt=date(2024,3,1);water=0;history=[]
while True:
 before=water;added=min(900,10000-water);water+=added
 history.append((dt.isoformat(),before,water,added))
 if water==10000:break
 water-=300 if dt<=date(2024,3,5) else 500 if dt<=date(2024,3,10) else 700
 if dt==date(2024,3,15):water-=1000
 assert water>=0;dt+=timedelta(days=1)
assert dt==date(2024,4,6) and history[-2][2]==9900 and history[-1][1:]==(9200,10000,800)
note(2024,23,2,{'dayStepSimulation':history,'firstFull':dt.isoformat(),'lastFill':800})
base=[F(20,3),F(8,3),F(10,3),F(10,3)];cases=[]
for p5,p6 in product(list(combinations(range(4),2)),repeat=2):
 result=[base[i]+2*(i in p5)+2*(i in p6) for i in range(4)]
 assert sum(result)==24;cases.append((p5,p6,result))
assert max(c[2][0] for c in cases)==F(32,3)
witness=next(c for c in cases if c[0]==(1,2) and c[1]==(1,3))
assert all(v>=5 for v in witness[2])
note(2024,24,5,{'cases':36,'baseScores':list(map(str,base)),'printedAllPassCounterexample':[list(witness[0]),list(witness[1]),list(map(str,witness[2]))],'totalAllCases':24,'maximumA':'32/3'})
before=[7500,7000,6500,5000];after=[6000,7250,7500,7000];solutions=[]
for new in permutations([2000,1000,500,250]):
 old=tuple(before[i]+new[i]-after[i] for i in range(4))
 if any(v not in [0,250,500,1000,2000] for v in old):continue
 positives=[v for v in old if v];
 if len(set(positives))!=len(positives):continue
 solutions.append((old,new))
assert solutions==[((2000,0,0,0),(500,250,1000,2000))]
note(2024,25,1,{'currentOrderings':24,'solutions':solutions,'year2022ZerosMayRepeat':True})
# Identity and official final answers; page order differs between years.
keys={}
for y,post,suffix,book in [(2023,4341,2,'인'),(2024,4564,1,'사')]:
 with pdfplumber.open(R/f'artifacts/psat600_20261028/sources/{post}/BBSMSTR_000000000138_{post}_{suffix}.pdf') as pdf:
  texts=[p.extract_text() for p in pdf.pages];found=[t for t in texts if '영역 상황판단' in t];assert len(found)==1;t=found[0]
  assert str(y)+'년도' in t and book in t;ans={}
  for line in t.splitlines():
   if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
    v=list(map(int,line.split()));ans.update(zip(v[::2],v[1::2]))
  assert len(ans)==25;keys[y]=ans
expectedRows={
(2023,17):[[['甲','700,000','해당'],['乙','400,000','해당하지 않음'],['丙','500,000','해당'],['丁','300,000','해당'],['戊','500,000','해당']]],
(2023,18):[[['평가점수','13','20','15','14','17']],[['A위원','68','65','73','75','65'],['B위원','68','73','69','70','60'],['C위원','68','62','69','65','60'],['D위원','68','65','65','65','70'],['E위원','72','65','69','75','75']]],
(2023,19):[[['甲','08:55','20:00','－','10:30','13:30'],['乙','08:00','19:55','－','－','－'],['丙','09:00','21:30','개인용무시간 (19:00～19:30)','13:00','14:30'],['丁','08:30','23:30','재택근무','－','－'],['戊','07:00','21:30','－','－','－']]],
(2024,25):[[['우승','2000'],['준우승','1000'],['3위','500'],['4위','250']],[['1위','A','7500'],['2위','B','7000'],['3위','C','6500'],['4위','D','5000']],[['1위','C','7500'],['2위','B','7250'],['3위','D','7000'],['4위','A','6000']]]}
for q in bank:
 y=int(q['examDate'][:4]);n=q['number'];raw=(A/f'{y}-s{n}-source.txt').read_text(encoding='utf-8');prompt,tail=raw.split('.',1)[1].split('?',1);body,opts=tail.split('①',1)
 assert q['answer']==keys[y][n];assert norm(q['prompt'])==norm(prompt+'?')
 options=re.split('[①②③④⑤]','①'+opts)[1:];assert len(options)==5
 for a,b in zip(options,q['choices']):assert norm(a)==norm(b),(y,n,'option')
 if q.get('figures'):assert norm(q['sourceTranscript'])==norm(body)
 else:
  if (y,n)==(2023,17):body=body.split('구분 이전여비',1)[0]
  if (y,n)==(2023,18):
   before,rest=body.split('(단위: 점)',1);body=before+'○ 각 업체의 기술능력에'+rest.split('○ 각 업체의 기술능력에',1)[1].split('(단위: 점)',1)[0]
  if (y,n)==(2023,19):body=body.split('\n금요일 토요일',1)[0]
  if (y,n)==(2024,25):
   before,rest=body.split('챔피언십 대회 성적 점수',1);body=before+'○ 총점수에는'+rest.split('○ 총점수에는',1)[1]
  assert norm(q['body'])==norm(body),(y,n,'body')
 if (y,n) in expectedRows:assert [t['rows'] for t in q['tables']]==expectedRows[y,n]
 assert len(q['steps'])==len(q['optionReasons'])==5
 for s,prefix in zip(q['steps'],['착안점: ','실전 풀이: ','답 확정 기준: ','정석 근거: ','적용 한계: ']):assert s.startswith(prefix) and len(s)>40
 for f in [q['original']]+[f['asset'] for f in q.get('figures',[])]:assert (R/f if P.exists() else A/'staged'/f).exists()
for crop in json.loads((A/'crop-manifest.json').read_text(encoding='utf-8')):
 source=R/crop['source'];assert hashlib.sha256(source.read_bytes()).hexdigest()==crop['sha256']
 with pdfplumber.open(source) as pdf:
  im=pdf.pages[crop['page1based']-1].crop(tuple(crop['rect'])).to_image(resolution=crop['resolution']).original.convert('RGB')
  actual=Image.open(R/crop['asset'] if P.exists() else A/'staged'/crop['asset']).convert('RGB')
  assert im.size==actual.size and im.tobytes()==actual.tobytes()
seen=set()
for path in (R/'assets/psat').glob('*.json'):
 if path.name in ['sets.json','situation04.json']:continue
 obj=json.loads(path.read_text(encoding='utf-8'))
 if isinstance(obj,list):
  for q in obj:
   k=(q.get('examDate',q['source'][:10].replace('.','-')),q['subject'],q['number']);assert k not in seen;seen.add(k)
for q in bank:
 k=(q['examDate'],q['subject'],q['number']);assert k not in seen;seen.add(k)
for path,digest in json.loads((A/'before-situation04-hashes.json').read_text(encoding='utf-8')).items():
 if path=='assets/psat/sets.json':continue
 assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
proofs.update(status='PASS',count=10,officialFinalKeys=10,sourceTables=7,sourceFigures=4,limitations='Same-author source review and exact/enumerated proofs, not independent expert audit.')
(A/'content-checks.json').write_text(json.dumps(proofs,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PASS:10 officialkeys/source,7tables/4pixelmatchedcrops,945pairings,24seats,32scores,36examoutcomes,waterdaysteps,ranking24permutations.')
