from pathlib import Path
from fractions import Fraction as F
import json,re,hashlib,pdfplumber
from PIL import Image
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/data08';P=R/'assets/psat/data08.json';bank=json.loads((P if P.exists() else A/'authored-data08.json').read_text(encoding='utf-8'));checks={}
def note(y,n,key,data):
 assert next(q for q in bank if q['examDate'].startswith(str(y)) and q['number']==n)['answer']==key;checks[f'{y}-{n}']=data
a=302589+160897+59184;d=38188-(326646-287502);e=20996-(177942-157368)
assert (a,d,e)==(522670,-956,422) and a==444870+18616+59184 and d+e==-534
note(2025,21,1,{'A':a,'D':d,'E':e})
aw=[5500,5600,5300,5400,5600];br=[12200,13500,11500,11400,12800]
sign=lambda x:(x>0)-(x<0)
assert [sign(aw[i]-aw[i-1]) for i in range(1,5)]==[1,-1,1,1]
assert [sign(br[i]-br[i-1]) for i in range(1,5)]==[1,-1,-1,1]
ratesA=[F(1500,7700),F(3000,16500)];ratesB=[F(600,11700),F(400,26700)];assert ratesA[0]>ratesA[1] and ratesB[0]>ratesB[1]
sums=[13000*5-(11600+11600+12100),14000*5-(15200+15700+13600)];assert sums==[29700,25500] and sums[0]>sums[1]
note(2025,22,5,{'truth':[False,True,True],'absoluteChangeRates':[list(map(str,ratesA)),list(map(str,ratesB))],'missingWeekSums':sums,'semanticReview':'change magnitude compared separately from signed growth rate;explicit in explanation'})
qty=[[4,4,2],[3,5,2],[5,3,2],[5,2,3],[5,1,4]];wholesale=[6700,14300,2300];retail=[14100,26400,6100]
assert [sum(a*b for a,b in zip(row,retail)) for row in qty]==[174200,186500,161900,141600,121300]
saved=[sum(a*(r-w) for a,r,w in zip(row,retail,wholesale)) for row in qty];assert saved==[85600,90300,80900,72600,64300]
assert all(sum(row)==10 for row in qty) and [saved[1]-saved[0],saved[0]-saved[2],saved[2]-saved[3],saved[3]-saved[4]]==[4700,4700,8300,8300]
note(2025,23,2,{'perKg':[r-w for r,w in zip(retail,wholesale)],'savings':saved})
def round1(x):return F((x*10+F(1,2)).numerator//(x*10+F(1,2)).denominator,10)
def score(raw,weights):return sum(round1(F(x,maximum)*weight) for x,maximum,weight in zip(raw,[767,4104,1000],weights))
assert 70>=2*(10+20)
g=score([112,105,700],[10,20,70]);fr=score([56,143,710],[10,20,70]);israel=score([14,117,760],[20,10,70]);taiwan=score([45,22,770],[20,10,70])
assert g==51 and fr==F('51.1') and israel==F('53.9') and taiwan==F('55.2')
note(2025,24,1,{'truth':[True,False,False],'germanyFrance':[str(g),str(fr)],'newIsraelTaiwan':[str(israel),str(taiwan)],'rounding':'half-up each transformed component'})
upper=[11,33,37,38,41,50,52,54,55,56];lower=[39,44,53,60,64,66,67,73,81,83];low=[104,110,117,121,127,128,129,130,131,132]
assert 10-sum(41<=x<=50 for x in upper+lower+low)==7
assert 133-110-sum(x>110 for x in low)==15
assert sum(x<53 for x in upper+lower)+1==10
note(2025,25,3,{'truth':[True,True,False,True],'highIncome41to50':7,'nonLowBelow110':15,'philippinesMergedRank':10})
traffic=[4380,4019,3973,3529];allacc=[31582,30944,29545,31111]
assert all(traffic[i]<traffic[i-1] for i in range(1,4)) and round1(F(traffic[2]-traffic[3],traffic[2])*100)==F('11.2')
assert allacc[0]>allacc[1]>allacc[2]<allacc[3] and 25+7==32 and 5+2==7
note(2021,1,2,{'usable':[True,False,True,False],'annualTrafficDrop':str(F(444,3973)),'exclusions':'2019 vs2015-2018 repeated grades;2019large vs2018total'})
periods=[(200304,200406),(200410,200712),(200603,200606),(200701,202105),(200705,200810),(200707,202105),(201203,202105),(201212,201307),(201312,201409)]
sizes=[3128,300,462,6000,350,6000,3350,1450,5961];active=[i for i,(a,b) in enumerate(periods) if a<=200710<=b]
dur=lambda z:(z[1]//100-z[0]//100)*12+z[1]%100-z[0]%100
assert active==[1,3,4,5] and sum(sizes)==27001 and sum(sizes[i] for i in [3,5,6])==15350
assert max(range(9),key=lambda i:dur(periods[i]))==3 and min(range(9),key=lambda i:dur(periods[i]))==2
note(2021,2,5,{'October2007activeIndices':active,'sum':27001,'current2021May':15350,'wrongStatement':'5missions actually4'})
total=list(map(F,['29.7','30.3','30.8','32.6','34.1','35.7','36.0']));deficit=list(map(F,['14.6','14.9','15.3','16.9','18.3','20.0','20.7']));gdp=[1323,1389,1440,1501,1563,1658,1741]
finance=[a-b for a,b in zip(total,deficit)];debts=[x*p/100 for x,p in zip(gdp,total)];defdebts=[x*p/100 for x,p in zip(gdp,deficit)]
assert debts[-1]>=F(3,2)*debts[0] and finance[5]<finance[4] and finance[3]<deficit[3]
assert [2014+i for i,x in enumerate(defdebts) if x>=300]==[2019,2020]
note(2021,3,2,{'truth':[True,False,True,False],'financeShares':list(map(str,finance)),'debtAmounts':list(map(str,debts)),'deficitAmounts':list(map(str,defdebts))})
matrix=[[15,10,5],[0,30,10],[5,10,15]];rows=list(map(sum,matrix));cols=[sum(row[i] for row in matrix) for i in range(3)];changed=100-sum(matrix[i][i] for i in range(3));up=sum(matrix[r][c] for r in range(3) for c in range(r));down=sum(matrix[r][c] for r in range(3) for c in range(r+1,3))
assert sum(rows)==100 and rows==[30,40,30] and cols==[20,50,30] and (changed,up,down)==(40,15,25)
note(2021,4,1,{'truth':[True,True,False,False],'matrix':matrix,'rows':rows,'columns':cols,'changed':changed,'larger':up,'smaller':down})
rework=1000*F(1,10);rubbish1=rework/2;assembly=900+rework/2;rubbish2=assembly*F(1,5);ship=assembly*F(4,5);assert (rubbish1,rubbish2,ship)==(50,190,760) and rubbish1+rubbish2+ship==1000
note(2021,5,4,{'reworkWaste':50,'inspectionInput':950,'inspectionWaste':190,'wasteTotal':240,'shipped':760})
keys={}
for y,post,book in [(2025,'5994','인'),(2021,'3982','나')]:
 with pdfplumber.open(next((R/f'artifacts/psat600_20261028/sources/{post}').glob('*.pdf'))) as pdf:
  t=next(p.extract_text() for p in pdf.pages if '영역 자료해석' in p.extract_text());assert f'{y}년도' in t and f'{book} 책형' in t;key={}
  for line in t.splitlines():
   if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
    v=list(map(int,line.split()));key.update(zip(v[::2],v[1::2]))
  assert len(key)==25;keys[y]=key
norm=lambda s:re.sub(r'[\s·]+','',s)
for q in bank:
 y=int(q['examDate'][:4]);n=q['number'];raw=(A/f'{y}-d{n}-source.txt').read_text(encoding='utf-8').split(f'{n}.',1)[1];prompt,tail=raw.split('?',1)
 assert norm(q['prompt'])==norm(prompt+'?')
 opts=re.split('[①②③④⑤]','①'+tail.split('①',1)[1])[1:];assert len(opts)==5 and all(norm(a)==norm(b) for a,b in zip(opts,q['choices'])),(y,n,'options')
 assert q['answer']==keys[y][n] and len(q['steps'])==len(q['optionReasons'])==5
 for s,prefix in zip(q['steps'],['착안점: ','실전 풀이: ','답 확정 기준: ','정석 근거: ','적용 한계: ']):assert s.startswith(prefix) and len(s)>40
 assert not any('\ue000'<=c<='\uf8ff' or c in '\ufffd\u2060' for c in json.dumps(q,ensure_ascii=False))
manifest=json.loads((A/'crop-manifest.json').read_text(encoding='utf-8'));assert len(manifest)==29
pdfs={}
for f in manifest:
 source=R/f['source'];assert hashlib.sha256(source.read_bytes()).hexdigest()==f['sha256']
 if str(source) not in pdfs:pdfs[str(source)]=pdfplumber.open(source)
 p=pdfs[str(source)].pages[f['page1based']-1];path=R/f['asset'] if P.exists() else A/'staged'/f['asset'];im=Image.open(path).convert('RGB');ref=p.crop(f['rect']).to_image(resolution=f['resolution'],antialias=f.get('antialias',False)).original.convert('RGB');assert im.size==ref.size and im.tobytes()==ref.tobytes(),f['asset']
 x0,y0,x1,y1=f['rect']
 for w in p.extract_words():
  if w['x1']<=x0 or w['x0']>=x1 or w['bottom']<=y0 or w['top']>=y1:continue
  assert w['x0']>=x0-.5 and w['x1']<=x1+.5 and w['top']>=y0-.5 and w['bottom']<=y1+.5,(f['asset'],w['text'],w)
seen=set();old=0
for path in (R/'assets/psat').glob('*.json'):
 if path.name in ['sets.json','data08.json']:continue
 obj=json.loads(path.read_text(encoding='utf-8'))
 if isinstance(obj,list):
  for q in obj:
   k=(q.get('examDate',q['source'][:10].replace('.','-')),q['subject'],q['number']);assert k not in seen;seen.add(k);old+=1
for q in bank:
 k=(q['examDate'],q['subject'],q['number']);assert k not in seen;seen.add(k)
for path,digest in json.loads((A/'before-data08-hashes.json').read_text(encoding='utf-8')).items():
 if path!='assets/psat/sets.json':assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
checks.update(status='PASS',count=10,officialFinalKeys=10,figures=29,preservedExisting=old,limitations='Same-author source/visual verification and separate exact computations;not independent expert certification.')
(A/'content-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PASS10keys29pixelcrops;sourcechoices;exactratios/halfup/rank/period/matrix/flow;preserved',old)
