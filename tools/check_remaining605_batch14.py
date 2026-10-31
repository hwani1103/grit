"""Batch14 original tables/keys and independent optimization/schedule models."""
from pathlib import Path
from itertools import product,permutations,combinations
from fractions import Fraction as F
import json,re
import pdfplumber
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/psat_remaining605_20261030/batch14'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
norm=lambda s:re.sub(r'[\s①②③④⑤ㆍ·․「」『』\uf000\uf001/]','',s)
expected={
16:[dict(columns=['과목','일반과정','속성과정'],rows=[['A','5,000','10,000'],['B','3,000','7,000'],['C','10,000','13,000']],after=1,native='취득점수 1점당 수강료(원) 과목 일반과정 속성과정 A 5,000 10,000 B 3,000 7,000 C 10,000 13,000')],
18:[dict(columns=['매물','지역','동ㆍ호수','입주 가능 시기','전세 보증금(억 원)','담보 대출','붙박이장'],rows=[['A','대한동','1011동 1601호','즉시','2.5','없음','있음'],['B','대한동','503동 1704호','즉시','2.3','있음','없음'],['C','민국동','301동 1504호','즉시','2.0','없음','없음'],['D','대한동','308동 1306호','2025. 8. 1. 이후','2.0','없음','있음'],['E','민국동','616동 806호','즉시','2.3','없음','없음']],after=5,native='입주 가능 전세 보증금 담보 매물 지역 동ㆍ호수 붙박이장 시기 (억 원) 대출 1011동 A 대한동 즉시 2.5 없음 있음 1601호 503동 B 대한동 즉시 2.3 있음 없음 1704호 301동 C 민국동 즉시 2.0 없음 없음 1504호 308동 2025. 8. 1. D 대한동 2.0 없음 있음 1306호 이후 616동 E 민국동 즉시 2.3 없음 없음 806호')],
19:[dict(columns=['지급기준','지원 한도액'],rows=[['장애, 질병 등으로 출퇴근에 어려움이 있는 자','35만 원'],['신규임용일로부터 3년이 지나지 않은 자','25만 원'],['그 이외의 자','20만 원']],after=2,native='지급기준 지원 한도액 장애, 질병 등으로 출퇴근에 어려움이 있는 자 35만 원 신규임용일로부터 3년이 지나지 않은 자 25만 원 그 이외의 자 20만 원'),dict(columns=['직원','거주지와 근무지 간 편도 거리','통근 시간','주택 소유 여부','월세'],rows=[['甲','50km','1시간 10분','○','45만 원'],['乙','45km','1시간','×','30만 원'],['丙','100km','1시간 30분','×','45만 원'],['丁','40km','50분','×','40만 원'],['戊','70km','1시간 40분','×','35만 원']],after=3,native='거주지와 근무지 간 주택 소유 직원 통근 시간 월세 편도 거리 여부 甲 50km 1시간 10분 ○ 45만 원 乙 45km 1시간 × 30만 원 丙 100km 1시간 30분 × 45만 원 丁 40km 50분 × 40만 원 戊 70km 1시간 40분 × 35만 원')],
20:[dict(columns=['기업','전년도 매출액(억 원)','최근 1년간 탈세 의심 민원(건)','전년도 부실 거래(건)','성실 납세 기업 선정 연도','최근 1년 내 세무조사 여부'],rows=[['A','1,700','5','7','2021년','×'],['B','480','10','4','2017년','×'],['C','6,250','6','2','2022년','○'],['D','3,000','7','5','2023년','×'],['E','5,000','3','3','2010년','×']],after=10,native='전년도 최근 1년간 전년도 성실 납세 최근 1년 내 기업 매출액 탈세 의심 부실 거래 기업 선정 세무조사 (억 원) 민원(건) (건) 연도 여부 A 1,700 5 7 2021년 × B 480 10 4 2017년 × C 6,250 6 2 2022년 ○ D 3,000 7 5 2023년 × E 5,000 3 3 2010년 ×')],
24:[dict(columns=['4월 1일','4월 2일','4월 3일','4월 4일','4월 5일','4월 6일','4월 7일'],rows=[['0','1','0','1','0','1','1']],after=5,native='4월 1일 4월 2일 4월 3일 4월 4일 4월 5일 4월 6일 4월 7일 0 1 0 1 0 1 1')]}
rows=read(OUT/'revealed-current.json');sources={x['id']:x for x in read(OUT/'blind-source.json')};solves={x['id']:x for x in read(OUT/'own-solves.json')};checks=[]
for row in rows:
 q=row['question'];m=sources[q['id']]
 native=norm(re.sub(r'^.*?\b'+str(q['number'])+r'[.]\s*','',m['sourceText'],count=1,flags=re.S))
 for i,t in enumerate(expected.get(q['number'],[])):
  actual=q['tables'][i];assert actual['columns']==t['columns'] and actual['rows']==t['rows'] and actual['afterParagraph']==t['after']
  assert native.count(norm(t['native']))==1,(q['id'],'table',i);native=native.replace(norm(t['native']),'',1)
 if q['number']==17:
  label=norm('甲 丙');assert native.count(label)==1;native=native.replace(label,'',1)
 a,b=native,norm(q['prompt']+q['body']+''.join(q['choices']))
 if a!=b:
  i=next((i for i,(x,y) in enumerate(zip(a,b)) if x!=y),min(len(a),len(b)))
  raise AssertionError((q['id'],i,a[max(0,i-20):i+120],b[max(0,i-20):i+120]))
 with pdfplumber.open(ROOT/row['officialKey']) as pdf:
  pi,t=next((i+1,p.extract_text()) for i,p in enumerate(pdf.pages) if '영역 상황판단' in (p.extract_text() or ''))
 assert q['examDate'][:4] in t and f"책형 {q['book']}" in t
 answers={}
 for line in t.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
   z=list(map(int,line.split()));answers.update(zip(z[::2],z[1::2]))
 assert answers[q['number']]==q['answer']==solves[q['id']]['answer']
 checks.append(dict(id=q['id'],source=m['source'],page=m['page'],nativeTextAndFiveChoicesMatch=True,tablesChecked=len(expected.get(q['number'],[])),key=row['officialKey'],keyPage=pi,answer=q['answer']))

# All-positive linear objective: reduce any excess above150 before optimization.
feesNormal=[5000,3000,10000];feesAccelerated=[10000,7000,13000];costs=[];witness=[]
for accelerated in range(3):
 fee=[feesAccelerated[i] if i==accelerated else feesNormal[i] for i in range(3)]
 candidates=[(sum(x*y for x,y in zip([a,b,150-a-b],fee)),[a,b,150-a-b]) for a in range(40,71) for b in range(40,71) if 40<=150-a-b<=100]
 best=min(candidates);costs.append(best[0]);witness.append(best[1])
assert costs==[1010000,1030000,930000] and witness[2]==[40,70,40]
assert 40*sum(feesNormal)+40*min(a-b for a,b in zip(feesAccelerated,feesNormal))+30*min(feesNormal)==930000
offices={'A':[(3,'국장'),(4,'과장'),(5,'팀장')],'B':[(4,'국장'),(5,'과장')],'C':[(5,'국장')]};postal=[]
for oa,ob,oc in permutations('ABC'):
 for pa,pb,pc in product(offices[oa],offices[ob],offices[oc]):
  if oa!='C' and oc!='A' and pa[0]==pb[0] and all(pc[0]<p[0] for p in offices[ob]):postal.append(((oa,pa),(ob,pb),(oc,pc)))
assert postal==[(('A',(5,'팀장')),('C',(5,'국장')),('B',(4,'국장')))]
apartments={'A':(1601,True,F('2.5'),False,True,'대한'),'B':(1704,True,F('2.3'),True,False,'대한'),'C':(1504,True,F('2.0'),False,False,'민국'),'D':(1306,False,F('2.0'),False,True,'대한'),'E':(806,True,F('2.3'),False,False,'민국')}
eligible=[k for k,(room,july,deposit,loan,closet,region) in apartments.items() if room//100>=10 and july and not loan and deposit<=(F('2.5') if closet else F('2.3'))]
assert eligible==['A','C'] and [k for k in eligible if apartments[k][-1]=='대한']==['A']
staff=[(50,70,True,45,25),(45,60,False,30,35),(100,90,False,45,20),(40,50,False,40,20),(70,100,False,35,25)]
rent=[min(actual,cap) if not owns and (distance>=50 or minutes>=60) else 0 for distance,minutes,owns,actual,cap in staff]
assert rent==[0,30,20,0,25] and sum(rent)==75
firms={'A':(1700,5,7,2021,False),'B':(480,10,4,2017,False),'C':(6250,6,2,2022,True),'D':(3000,7,5,2023,False),'E':(5000,3,3,2010,False)}
score=lambda sales,complaints,bad,year,recent:(1 if sales<500 else 3 if sales<5000 else 5)+F(complaints,2)+F(3*bad,10)-(1 if year in range(2020,2026) else 0)
tax={k:score(*v) for k,v in firms.items()};assert tax==dict(A=F('6.6'),B=F('7.2'),C=F('7.6'),D=F(7),E=F('7.4'))
assert [k for k,v in firms.items() if tax[k]>7 and not v[-1]]==['B','E']
def laundry(n):
 clean=list(range(n));dirty=[];worn=None;jobs={};peak=None
 for day in range(84):
  if not clean:return False,day,peak
  if worn is not None:dirty.append(worn)
  worn=clean.pop(0)
  if day%7==0:
   jobs[day+7]=dirty;dirty=[]
   if day==14:peak=dict(clean=len(clean),worn=1,inLaundry=sum(map(len,jobs.values())))
   clean+=jobs.pop(day,[])
  partition=clean+dirty+([worn] if worn is not None else [])+[x for group in jobs.values() for x in group]
  assert len(partition)==len(set(partition))==n
 return True,None,peak
assert laundry(14)[0:2]==(False,14) and laundry(15)==(True,None,dict(clean=0,worn=1,inLaundry=14))
# Complete four-card directed relation, with every unlisted pair tied.
cards=['사자','불곰','얼룩말','하이에나'];wins={('사자','얼룩말'),('불곰','사자'),('얼룩말','하이에나'),('하이에나','사자')}
result=lambda a,b:1 if (a,b) in wins else -1 if (b,a) in wins else 0
cardModels=[v for v in permutations(cards) if result(v[0],v[3])==-1 and result(v[1],v[3])==1 and result(v[2],v[3])==0]
assert set(cardModels)=={('하이에나','사자','불곰','얼룩말'),('사자','얼룩말','불곰','하이에나')}
assert all(v[2]=='불곰' for v in cardModels) and ('불곰','사자') in wins and not any(b=='불곰' for a,b in wins)
# First satisfaction triggers germination the following day, no pre-plant weather.
weatherModels=[]
for weather in product([0,1],repeat=7): #0sun,1rain
 sprout={}
 for day in range(1,8):
  checksToday={'B':weather[day-1]==0,'A':day>=2 and weather[day-2:day]==(0,0),'D':day>=2 and weather[day-2:day]==(1,1),'C':sum(weather[:day])>=3}
  for seed,condition in checksToday.items():
   if condition and seed not in sprout:sprout[seed]=day+1
 if len(sprout)==4 and [sum(v==d for v in sprout.values()) for d in range(1,8)]==[0,1,0,1,0,1,1]:weatherModels.append((weather,sprout))
assert len(weatherModels)==2 and all([k for k,v in sorted(s.items(),key=lambda x:x[1])]==list('BDAC') for w,s in weatherModels)
# Quarter labels: 0甲,1乙,2丙,3丁,4戊. January cohort is forced by two exclusions.
def select(previousBad,last):
 chosen=set(previousBad)
 if len(chosen)<3:chosen.update(sorted(set(range(5))-chosen,key=lambda i:(last[i],i))[:3-len(chosen)])
 return chosen
quarterModels=[]
for lastC,lastD in [(-3,-2),(-2,-3)]:
 for bits in product([False,True],repeat=2):
  janBad={person for person,on in zip([0,4],bits) if on};last=[0,0,lastC,lastD,0]
  april=select(janBad,last)
  if 3 in april or 4 not in april:continue
  for i in april:last[i]=1
  for mask in product([False,True],repeat=len(april)):
   aprilBad={person for person,on in zip(sorted(april),mask) if on};july=select(aprilBad,last)
   if 3 in july or 4 not in july or len(july)!=3:continue
   # All three July assessed departments were excellent, so JulyBad is empty.
   quarterModels.append(dict(januaryBad=sorted(janBad),april=sorted(april),aprilBad=sorted(aprilBad),july=sorted(july),julyBad=[],total=len(janBad)+len(aprilBad)))
assert quarterModels and {m['total'] for m in quarterModels}=={5}
assert all(m['januaryBad']==[0,4] and m['aprilBad']==[0,2,4] for m in quarterModels)
proof=dict(status='PASS',officialSourceKeys=checks,nativeTablesChecked=6,costByAcceleratedSubject=costs,costWitnesses=witness,postalUniqueModel=postal,apartmentsEligible=eligible,rentPayments=rent,taxScores={k:str(v) for k,v in tax.items()},laundry15=laundry(15),laundry14= 'fails Monday morning day14 before evening return',cardModels=cardModels,bearExclusionReason='Bear beats lion but has no losing opponent;乙 cannot beat bear. Initial own-solve sentence corrected separately.',weatherModels=weatherModels,quarterModels=quarterModels,continuousCostProof='All rates positive; total150 lower bound with per-subject40,minimum acceleration surcharge120000 and residual lowerbound90000; attained at40/70/40 withCaccelerated.',qualitativeLegal='2021s01 applicantBdistrict head,not metropolitan mayor;committee decides but doesnot execute;prefix6andnextfirstdigit2unchanged;driverlicense requires own application;appeal30days tolocalhead.',limitations='Same-author source/model checks. Initial own-solve bear exclusion sentence was wrong and is preserved with separate correction; answer and feasible assignments unchanged. Not independent expert/device validation.')
(OUT/'source-key-model-checks.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PASS10 original/key checks,6native tables,linear cost bound,postal/card permutations,84-day laundry,128weather and quarterly schedules.')
