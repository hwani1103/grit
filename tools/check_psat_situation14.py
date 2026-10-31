from pathlib import Path
import json,re,hashlib,itertools as it,pdfplumber
from PIL import Image
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/situation14';P=R/'assets/psat/situation14.json'
bank=json.loads((P if P.exists() else A/'authored-situation14.json').read_text(encoding='utf-8'));tr=json.loads((A/'source-transcripts.json').read_text(encoding='utf-8'))
assert [(q['examDate'],q['number']) for q in bank]==[('2026-07-18',n) for n in range(7,17)]
proof={}
from fractions import Fraction as F
from math import ceil
from datetime import date
fees=[3000+max(ceil(w)-2,0)*1000+extra for w,extra in [(F(15,10),2000),(F(32,10),0),(F(8,10),5000)]]
assert fees==[5000,5000,8000] and sum(fees)*F(9,10)==16200
proof['q7']={'fees':fees,'afterDiscount':16200}
# Each cell: class, instructor, period. Friday period3 is explicitly unavailable.
days=[[('M','A',1),('M','B',2),('S','A',3)],[('V','C',1),('S','B',2),('T','B',3)],[('M','A',1),('S','B',2),('T','A',3)],[('T','A',1),('V','C',2),('M','A',3)],[('V','A',1),('M','B',2)]]
schedules=[]
for row in it.product(*days):
 if set(x[1] for x in row)!={'A','B','C'}:continue
 if any(x[0]=='V' and (i==4 or row[i+1][0]!='T') for i,x in enumerate(row)):continue
 if any(row[i][0]==row[i+1][0]=='M' for i in range(4)):continue
 schedules.append(row)
assert len(schedules)==3 and all(list(row[1:])==[('V','C',1),('T','A',3),('T','A',1),('M','B',2)] for row in schedules)
truth=[not any(any(x[0]=='S' for x in row) for row in schedules),any(sum(x[0]=='M' for x in row)==3 for row in schedules),any(sum(x[2]==2 for x in row)==3 for row in schedules),any(row[2][0]=='M' for row in schedules),any(sum(x[1]=='A' for x in row)==3 for row in schedules)]
assert truth==[False]*4+[True]
proof['q8']={'schedules':schedules,'optionTruth':truth,'all162SchedulesChecked':True}
dispose=lambda years,approved:((not approved) and years<5) or years<=1
assert [dispose(y,a) for y,a in [(3,True),(1,True),(2,False),(6,False)]]==[False,True,True,False]
proof['q9']={'disposed':['B','C'],'boundary5Protected':not dispose(5,False),'boundary1Disposed':dispose(1,True)}
companies=[('A',date(2022,5,13),'반도체',47,490,date(2026,7,6)),('B',date(2019,11,27),'태양광',53,560,date(2023,2,21)),('C',date(2025,10,23),'조선',73,480,None),('D',date(2020,2,7),'AI',59,450,date(2024,5,14)),('E',date(2019,3,29),'태양광',66,430,date(2023,6,7))]
checks={name:[date(2019,7,1)<=reg<=date(2026,7,1),field in ['반도체','태양광','AI'],sales>=(60 if field=='반도체' else 40),assets<500,cert is not None and cert<=date(2026,7,1)] for name,reg,field,sales,assets,cert in companies}
assert [name for name,flags in checks.items() if all(flags)]==['D']
proof['q10']={'allConditions':checks,'eligible':'D'}
proof['q11']={'answer':1,'rule':'disqualified assignee excluded;disqualified heir succeeds then transfers within6months;all succession reports within30days'}
assert 30+5*2==40
proof['q12']={'answer':3,'explorationTotalMax':10,'extractionTotalMax':40,'limit':'extensions require permission'}
proof['q13']={'answer':5,'criteria':['plenary','unjustified','at least2consecutive days'],'leave':'advance permission ends on return','absenceReport':'after absence;justified report exempts reduction'}
flags1=['K','A','B','C'];flags2=['C','A','K','B','D']
assert [flags1.index('K')==0,flags2.index('B')>flags2.index('K'),flags1.index('A')==flags2.index('A')==1]==[True]*3
proof['q14']={'layouts':[flags1,flags2],'truth':[True,True,True]}
credits=[max((350-300)*F(20,100),350*F(2,100)),24*F(25,100)]
assert credits==[10,6] and sum(credits)==16
proof['q15']={'credits':[int(x) for x in credits],'sum':16,'excluded乙Increment':11}
consumed=[500*2,120*F(50,60),200*F(7,2)]
assert consumed==[1000,100,700] and sum(consumed)/2000==F(9,10)
proof['q16']={'consumption':[int(x) for x in consumed],'capacity':1800,'performance':'9/10'}
keys={}
for post,date,year,book in [(6016,'2026-07-18','2026','사')]:
 with pdfplumber.open(next((R/f'artifacts/psat600_20261028/sources/{post}').glob('*.pdf'))) as pdf:
  t=next(p.extract_text() for p in pdf.pages if '영역 상황판단' in p.extract_text());assert year in t and book in t;k={}
  for line in t.splitlines():
   if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
    v=list(map(int,line.split()));k.update(zip(v[::2],v[1::2]))
  assert len(k)==25;keys[date]=k
def norm(s):
 s=re.sub(r'\uf000([^\uf000]+)\uf000',r'『\1』',s)
 return re.sub(r'[\s·․]+','',s.replace('\uf000','『').replace('\uf001','』'))
tableSources=json.loads((A/'table-source-text.json').read_text(encoding='utf-8'))
rawTables={
8:['<시간표> 구분 월 화 수 목 금 마하하타 빈야사 마하하타 테라피 빈야사 1교시 (A) (C) (A) (A) (A) 마하하타 아쉬탕가 아쉬탕가 빈야사 마하하타 2교시 (B) (B) (B) (C) (B) 아쉬탕가 테라피 테라피 마하하타 3교시 (A) (B) (A) (A)'],
10:['구분 A B C D E 사업자 2022. 2019. 2025. 2020. 2019. 등록일 5. 13. 11. 27. 10. 23. 2. 7. 3. 29. 사업분야 반도체 태양광 조선 AI 태양광 매출액(원) 47억 53억 73억 59억 66억 자산총액(원) 490억 560억 480억 450억 430억 우수기업 2026. 2023. 2024. 2023. 없음 인증 취득일 7. 6. 2. 21. 5. 14. 6. 7.'],
15:['<공제율> 계산 방식 증가분 방식 당기분 방식 기업 규모 중소기업 50 % 25 % 대기업 20 % 2 %','연구개발비 기업 설립연도 기업 규모 전기 당기 甲 2010년 대기업 300억 원 350억 원 乙 2022년 중소기업 2억 원 24억 원'],
16:['사용 내역 사용 전류(mA) 게임 500 동영상 시청 200 동영상 촬영 120']}
expectedTables={
8:[(['구분','월','화','수','목','금'],[['1교시','마하하타 (A)','빈야사 (C)','마하하타 (A)','테라피 (A)','빈야사 (A)'],['2교시','마하하타 (B)','아쉬탕가 (B)','아쉬탕가 (B)','빈야사 (C)','마하하타 (B)'],['3교시','아쉬탕가 (A)','테라피 (B)','테라피 (A)','마하하타 (A)','수업 없음']])],
10:[(['구분','A','B','C','D','E'],[['사업자 등록일','2022. 5. 13.','2019. 11. 27.','2025. 10. 23.','2020. 2. 7.','2019. 3. 29.'],['사업분야','반도체','태양광','조선','AI','태양광'],['매출액(원)','47억','53억','73억','59억','66억'],['자산총액(원)','490억','560억','480억','450억','430억'],['우수기업인증 취득일','2026. 7. 6.','2023. 2. 21.','없음','2024. 5. 14.','2023. 6. 7.']])],
15:[(['기업 규모','증가분 방식','당기분 방식'],[['중소기업','50%','25%'],['대기업','20%','2%']]),(['기업','설립연도','기업 규모','전기 연구개발비','당기 연구개발비'],[['甲','2010년','대기업','300억 원','350억 원'],['乙','2022년','중소기업','2억 원','24억 원']])],
16:[(['사용 내역','사용 전류(mA)'],[['게임','500'],['동영상 시청','200'],['동영상 촬영','120']])]}
for q in bank:
 n=q['number'];src=tr[q['id']]
 assert norm(q['prompt'])==norm(src['prompt']),(n,'prompt')
 assert len(q['choices'])==5 and all(norm(x)==norm(y) for x,y in zip(q['choices'],src['choices'])),(n,'choices')
 originalBody=norm(src['body'])
 if n in rawTables:
  assert len(q['tables'])==len(rawTables[n])
  for i,raw in enumerate(rawTables[n]):
   assert norm(tableSources[str(n)][i])==norm(raw),(n,'source table')
   assert originalBody.count(norm(raw))==1;originalBody=originalBody.replace(norm(raw),'',1)
   table=q['tables'][i];columns,rows=expectedTables[n][i];assert table['columns']==columns and table['rows']==rows,(n,'table cells')
   assert 0<=table['afterParagraph']<len(q['body'].split('\n\n'))
 assert norm(q['body'])==originalBody,(n,'body')
 assert q['answer']==keys[q['examDate']][n] and len(q['steps'])==len(q['optionReasons'])==5
 assert not any('\ue000'<=c<='\uf8ff' or c in '\ufffd\u2060\u2024' for c in json.dumps(q,ensure_ascii=False)),n
 assert not re.search(r'\d{4}\.\s*\n\s*\n\s*\d{1,2}\.',q['body'])
for c in json.loads((A/'crop-manifest.json').read_text(encoding='utf-8')):
 source=R/c['source'];assert hashlib.sha256(source.read_bytes()).hexdigest()==c['sha256']
 with pdfplumber.open(source) as pdf:
  ref=pdf.pages[c['page1based']-1].crop(c['rect']).to_image(resolution=c['resolution'],antialias=True).original.convert('RGB');path=R/c['asset'] if P.exists() else A/'staged'/c['asset'];im=Image.open(path).convert('RGB');assert im.size==ref.size and im.tobytes()==ref.tobytes(),c['asset']
seen=set();old=0
for path in (R/'assets/psat').glob('*.json'):
 if path.name in ['sets.json','situation14.json']:continue
 obj=json.loads(path.read_text(encoding='utf-8'))
 if isinstance(obj,list):
  for q in obj:
   k=(q.get('examDate',q['source'][:10].replace('.','-')),q['subject'],q['number']);assert k not in seen;seen.add(k);old+=1
for q in bank:
 k=(q['examDate'],q['subject'],q['number']);assert k not in seen;seen.add(k)
for path,digest in json.loads((A/'before-situation14-hashes.json').read_text(encoding='utf-8')).items():
 if path!='assets/psat/sets.json':assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
proof.update(status='PASS',count=10,officialFinalKeys=10,sourceComparison='native prompt/body/choices;5native tables/10originalpixels',preservedExisting=old,limitations='Same-author semantic review with logical countermodels;not independent expert review.')
(A/'content-checks.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PASS10source/key/10pixels;models;preserved',old)
