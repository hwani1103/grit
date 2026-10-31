from pathlib import Path
from fractions import Fraction as F
import json,re,hashlib,pdfplumber
from PIL import Image
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/data09';P=R/'assets/psat/data09.json';bank=json.loads((P if P.exists() else A/'authored-data09.json').read_text(encoding='utf-8'));proof={}
names=['A','B','C','D','미국','E','F','G','영국','H','이탈리아','러시아'];rain=[1277,1690,627,1083,715,537,534,1732,1220,867,832,460];available=[1553,3232,2130,1647,10075,89081,23965,78986,2429,3326,3249,31469];annual=[2629,4993,4530,3091,22741,164595,201364,112077,4907,7794,4270,54915]
assert [names[i] for i in range(12) if rain[i]>=807*2]==['B','G']
large=[i for i in range(12) if annual[i]>=16427*5];assert [names[i] for i in sorted(large,key=lambda i:-rain[i])]==['G','E','F']
assert min((i for i in range(12) if rain[i]>807),key=lambda i:available[i])==0
assert [names[i] for i in range(12) if available[i]<2429 and annual[i]>=F(16427,4)]==['C']
assert names[sorted(range(12),key=lambda i:-available[i])[5]]=='H';proof['6']={'mapping':{'A':'대한민국','B':'일본','C':'중국','D':None,'E':'캐나다','F':'호주','G':'뉴질랜드','H':'프랑스'}}
scores=[[90,90,75],[85,85,70],[60,100,85],[95,65,100],[75,100,100]];totals=list(map(sum,scores));weighted=[F(2*k+e+2*m,5) for k,e,m in scores]
assert sum(x[0] for x in scores)==405 and max(totals)-min(totals)==35 and weighted==[84,79,78,91,90]
sexCases=[(F(260,3),F(170,2)),(F(175,2),F(255,3))];assert all(m>f for m,f in sexCases)
assert '84·79·78' in bank[1]['steps'][1];proof['7']={'truth':[True,False,True,True],'totals':totals,'weighted':list(map(str,weighted)),'sexCases':[[str(v) for v in row] for row in sexCases]}
assert F(8,100)<F(325,2686)<F('0.155') and F(1179)/F('.313')>3500
aiGrowth=F(657,185)-1;system2025=F(657)/F('.199');sysGrowth=system2025/2310-1
assert aiGrowth>F('2.5') and 0<sysGrowth<F('.5') and aiGrowth>5*sysGrowth
# optional +/-0.05percentage-point rounding still leaves the stated bounds strict.
assert F(1179)/F('.3135')>3500 and F(657)/F('.1985')<3465 and F(657)/F('.1995')>2310
proof['8']={'truth':[True,True,True],'aiGrowth':str(aiGrowth),'systemGrowth':str(sysGrowth),'roundingSensitivity':'all bounds survive +/-0.05percentage point'}
matrix=[[65,121,54,52,172,198,226,89],[56,152,61,55,172,164,214,70],[29,47,30,22,62,61,85,30],[24,61,30,37,82,80,113,45],[61,112,54,47,187,150,202,72],[50,87,38,41,120,188,150,55],[78,151,83,73,227,208,359,115],[27,66,31,28,94,81,116,46]];rows=list(map(sum,matrix));cols=[sum(r[i] for r in matrix) for i in range(8)];diag=[matrix[i][i] for i in range(8)];sums=[r+c-2*d for r,c,d in zip(rows,cols,diag)];diff=[abs(r-c) for r,c in zip(rows,cols)];shares=[F(d,r) for d,r in zip(diag,rows)]
assert rows==[977,944,366,472,885,729,1294,489] and cols==[390,797,381,355,1116,1130,1465,522]
assert [i for i in range(8) if rows[i]>cols[i]]==[0,1,3] and diag.index(min(diag))==2 and cols.index(min(cols))==3
assert sums==[1237,1437,687,753,1627,1483,2041,919] and diff==[587,147,15,117,231,401,171,33] and shares.index(max(shares))==cols.index(max(cols))==6
assert shares[6]>F('.27') and shares[5]<F('.26') and all(shares[i]<F('.25') for i in [0,1,2,3,4,7]);proof['9']={'truth':[True,False,True,True],'sums':sums,'absoluteDifferences':diff,'shares':list(map(str,shares))}
local=[9778,1287,1147,9263];foreign=[7796,508,141,7626];total=[a+b for a,b in zip(local,foreign)];staff=[10142,710,196,8898];inc=[900+646-560-600,70+52-195-33,20+15-7-5,839+741-704-666]
assert inc==[386,-106,23,210] and [F(t,s)>=F('1.8') for t,s in zip(total,staff)]==[False,True,True,True] and [F(f,t)>F('.45') for f,t in zip(foreign,total)]==[False,False,False,True]
proof['10']={'increase':inc,'total':total,'mapping':['충남','세종','충북','대전']}
fairs=[3200,2300,1800];walk=[800,1000,600];base=[450,350,250];extra=[200,0,100];count=[15,22,22];bills=[(f-(b+e)*F(min(w,800),800))*n for f,b,e,w,n in zip(fairs,base,extra,walk,count)];assert bills==[38250,42900,33825];proof['11']={'monthlyCost':list(map(str,bills)),'order':[1,0,2]}
known=F('19.4')+F('5.2')+F('4.3')+F('2.5');top5=sum(map(F,['33','24.1','19.4','12','11.7']));bound=F('137.5')+14*F('2.5');newRate=F('.61')*F('27.1')/F('24.1')
assert known==F('31.4') and known>=25 and top5==F('100.2') and bound==F('172.5') and top5>bound/2 and newRate<F('.7');proof['12']={'truth':[True,True,False],'knownBillion':str(known),'top5':str(top5),'allUpper':str(bound),'newGermanyPercent':str(newRate)}
duck=1327*F('.9442');agri=50052*F('1.0077');pig=7119*F('.9609');cropGrowth=F('1.015')*F('.9958')-1;liveGrowth=F('.9966')*F('1.007')-1
assert duck==F('1252.9534') and duck>=1200 and pig<agri*F('.15') and 7119<50052*F('.15')
r22=list(map(F,['.53','.20','-2.10','3.78','1.12','5.27']));r23=list(map(F,['3.51','1.79','2.82','3.93','.88','3.34']));assert [i for i in range(6) if r23[i]<r22[i]]==[4,5] and cropGrowth==F('.010737') and liveGrowth==F('.0035762') and 30270*cropGrowth>19782*liveGrowth>0
proof['13']={'truth':[True,False,True,True],'duck':str(duck),'cropChange':str(30270*cropGrowth),'livestockChange':str(19782*liveGrowth)}
member=852000;long=744733;four=744733+40344+55090+32411;assert long>member*F('.85') and F('27.3')/F('.645')>40 and four-member==20578 and 61850*15==927750>long
assert F(449579295,744733)>600 and F(2829332,32411)<100;proof['14']={'optionTruth':[False,True,True,True,True],'share':str(F(long,member)),'fourMemberships':four,'duplicateLowerBound':four-member}
assert F(573-498,1270)>F('.05') and F(1270-1108,1108)>=F('.14')
assert 110362+61757==172119 and abs(F(110362,172119)*100-F('64.1'))<F('.05')
assert 21671+14735==36406 and 21008+17796==38804 and F(38804,36406)>F('1.06') and F(17796,14735)>F('1.2')
old=[64050,20102,31535,7374,27335,13737];new=[66239,20434,33267,8057,31953,12169];assert sum(old)==164133 and sum(new)==172119 and F(172119,164133)>F('1.045') and F(172119,7256)>F(164133,7234)
growth=[F(n,o)-1 for n,o in zip(new,old)];assert F(66239,172119)>F('.38') and growth[4]>F('.16') and all(growth[i]<F('.1') for i in [0,1,2,3,5]) and sum([40266,38804,19700,11592])==110362
proof['15']={'compatible':[True,True,False,True,True],'pplGapPercentPoints':str(F(75,1270)*100),'industryGrowth':list(map(str,growth))}
keys={}
with pdfplumber.open(next((R/'artifacts/psat600_20261028/sources/3982').glob('*.pdf'))) as pdf:
 t=next(p.extract_text() for p in pdf.pages if '영역 자료해석' in p.extract_text());assert '2021년도' in t and '나 책형' in t
 for line in t.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
   v=list(map(int,line.split()));keys.update(zip(v[::2],v[1::2]))
assert len(keys)==25 and [keys[n] for n in range(6,16)]==[3,4,5,5,2,3,3,4,1,3]
norm=lambda s:re.sub(r'[\s·]+','',s)
for q in bank:
 n=q['number'];raw=(A/f'2021-d{n}-source.txt').read_text(encoding='utf-8').split(f'{n}.',1)[1];prompt,tail=raw.split('?',1);assert norm(q['prompt'])==norm(prompt+'?')
 if n!=15:
  choices=re.split('[①②③④⑤]','①'+tail.split('①',1)[1])[1:];assert len(choices)==5 and all(norm(a)==norm(b) for a,b in zip(q['choices'],choices)),n
 else:assert q['choices']==[f'자료 {i}' for i in range(1,6)] and [f['caption'] for f in q['figures'][1:]]==[f'선택지 {c}' for c in '①②③④⑤']
 assert q['answer']==keys[n] and len(q['steps'])==len(q['optionReasons'])==5
 for s,prefix in zip(q['steps'],['착안점: ','실전 풀이: ','답 확정 기준: ','정석 근거: ','적용 한계: ']):assert s.startswith(prefix) and len(s)>40
 assert not any('\ue000'<=c<='\uf8ff' or c in '\ufffd\u2060\u2024' for c in json.dumps(q,ensure_ascii=False))
manifest=json.loads((A/'crop-manifest.json').read_text(encoding='utf-8'));assert len(manifest)==27
source=next((R/'artifacts/psat600_20261028/sources/3977/pdf').glob('*자료*'))
with pdfplumber.open(source) as pdf:
 for c in manifest:
  assert hashlib.sha256(source.read_bytes()).hexdigest()==c['sha256'];p=pdf.pages[c['page1based']-1];ref=p.crop(c['rect']).to_image(resolution=c['resolution'],antialias=True).original.convert('RGB');path=R/c['asset'] if P.exists() else A/'staged'/c['asset'];im=Image.open(path).convert('RGB');assert im.size==ref.size and im.tobytes()==ref.tobytes(),c['asset']
  x0,y0,x1,y1=c['rect']
  for w in p.extract_words():
   if w['x1']<=x0 or w['x0']>=x1 or w['bottom']<=y0 or w['top']>=y1:continue
   assert w['x0']>=x0-.5 and w['x1']<=x1+.5 and w['top']>=y0-.5 and w['bottom']<=y1+.5,(c['asset'],w)
seen=set();old=0
for path in (R/'assets/psat').glob('*.json'):
 if path.name in ['sets.json','data09.json']:continue
 obj=json.loads(path.read_text(encoding='utf-8'))
 if isinstance(obj,list):
  for q in obj:
   k=(q.get('examDate',q['source'][:10].replace('.','-')),q['subject'],q['number']);assert k not in seen;seen.add(k);old+=1
for q in bank:
 k=(q['examDate'],q['subject'],q['number']);assert k not in seen;seen.add(k)
for path,digest in json.loads((A/'before-data09-hashes.json').read_text(encoding='utf-8')).items():
 if path!='assets/psat/sets.json':assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
proof.update(status='PASS',count=10,officialFinalKeys=10,figures=27,preservedExisting=old,limitations='Same-author original/visual review and exact arithmetic models;not independent expert certification.')
(A/'content-checks.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PASS10source/key/27pixelcrops;exactmodels;preserved',old)
