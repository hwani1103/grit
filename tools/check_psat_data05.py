from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import json,re,hashlib
import pdfplumber
from PIL import Image
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/data05';P=R/'assets/psat/data05.json'
bank=json.loads((P if P.exists() else A/'authored-data05.json').read_text(encoding='utf-8'));checks={}
def note(n,answer,e):
 assert next(q for q in bank if q['number']==n)['answer']==answer
 checks[str(n)]=e
note(1,1,{'visualConditions':'A within6km/8km,whitepricezone,above100m; Boutside8km; Cbelow100m; D/E>=300000','noInventedCoordinates':True})
dom=[287,368,385,458,514,481,555,441,189,77];abroad=[34,17,9,26,21,13,21,16,2,3]
tot=[a+b for a,b in zip(dom,abroad)]
assert tot==[321,385,394,484,535,494,576,457,191,80]
assert all(a<b for a,b in zip(tot[:4],tot[1:5])) and all(a>b for a,b in zip(tot[6:9],tot[7:10]))
us=[26,15,8,18,20,11,16,15,2,3]
others=[[1,1,1,0,0,0,0,0,0,0],[0,1,0,2,0,0,1,1,0,0],[0,0,0,5,1,1,0,0,0,0],[7,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,3,0,0,0],[0,0,0,1,0,1,1,0,0,0]]
assert all(us[i]>max(x[i] for x in others) for i in range(10))
assert all(us[i]+sum(x[i] for x in others)==abroad[i] for i in range(10))
note(5,5,{'totalsDerived':tot,'USannualMaximum':True,'needed':['countrybreakdown','trademark','utilitymodel'],'utilityYears':[2016,2018,2020,2022]})
whole=list(map(F,['180.1','175.9','171.5','173.0','169.1','167.9','164.4','162.1','159.6','158.1']))
zone=list(map(F,['91.5','81.5','80.7','80.9','81.1','81.0','78.0','77.7','77.8','77.6']))
field=list(map(F,['14.6','9.9','9.7','9.7','9.7','9.7','10.1','9.8','9.6','8.9']))
assert all(2*z<w for z,w in zip(zone[1:],whole[1:]))
assert zone[3]>zone[2] and field[0]>zone[0]*F(15,100)
note(7,1,{'truth':[True,False,False],'range1':'2014-2022','counterexamples':['2016increase','2013field>15%']})
candidates=[
[[1118,12280,2968,98932,395,6109],[266,3030,2035,67832,199,1827]],
[[1118,12320,2968,98932,395,6109],[266,3180,2035,67832,199,1827]],
[[1118,12280,2968,98932,395,6309],[266,3030,2035,67832,199,1290]],
[[1118,12320,2968,96932,395,6309],[266,3180,2035,70069,199,1290]],
[[1118,12280,2968,96932,395,6109],[266,3030,2035,70069,199,1827]]]
valid=[]
for old,new in candidates:
 rates=[F(n,o) for n,o in zip(new,old)]
 tests=[rates[0]<=F(1,4),rates[1]<=F(1,4),rates[2]<=F(7,10),rates[3]<=F(7,10),rates[0]<rates[4]<1,rates[1]<rates[5]<1]
 valid.append(tests)
assert [all(x) for x in valid]==[True,False,False,False,False]
note(8,1,{'sixConditionsByChoice':valid,'thresholds':'retention<=.25/.7;fusionretention greaterthanvillage'})
rain=[1,0,13,18,27,21,14,4,7,14,11,8,20,21,18,11,9,17];hail=[8,3,3,4,9,3,3,3,8,6,6,6,1,3,2,2,4,2]
totals=[39,41,57,29,74,59,49,23,43,58,44,38,52,58,57,40,46,39]
assert sum(rain)==234==846-sum([83,96,38,56,76,43,52,64,37,57,10])
assert sorted(totals)[-2:]==[59,74] and sorted(totals)[:2]==[23,29]
assert 59+74<3*(23+29)
assert rain.index(max(rain))==hail.index(max(hail))==4
fog02=41-sum([3,0,5,3,1,3,5,0,2,2,2]);fog08=23-sum([0,4,3,1,1,3,1,0,3,0,0])
assert fog02==15>5 and fog08==7>4
sums={'천둥번개':83,'큰 비':234,'벼락':96,'폭설':38,'큰 바람':56,'우박':76,'한파':43,'서리':52,'짙은 안개':64,'황충':37,'가뭄':57,'지진':10}
assert set(sorted(sums,key=sums.get,reverse=True)[:5])=={'천둥번개','큰 비','벼락','우박','짙은 안개'}
note(10,5,{'truth':[False,True,True,True],'missing':[15,21,7,234],'topBottom':[133,52]})
computer=[61,119,200,285,558];cipher=[102,209,314,395,754];comm=[110,192,289,358,723];sensor=[77,106,125,124,209];year=[350,626,928,1162,2244]
assert [sum(x) for x in zip(computer,cipher,comm,sensor)]==year and sum(year)==5310
close=lambda xs,ss:all(abs(x-F(str(s)))<F(1,20) for x,s in zip(xs,ss))
assert close([F(100*(b-a),a) for a,b in zip(comm,comm[1:])],[74.5,50.5,23.9,102.0])
assert close([F(sum(x)*100,5310) for x in [computer,cipher,comm,sensor]],[23.0,33.4,31.5,12.1])
assert close([F(a*100,b) for a,b in zip(sensor,cipher)],[75.5,50.7,39.8,31.4,27.7])
assert close([F(61*100,350)],[17.4]) and abs(F(61*100,350)-F(249,10))>7
note(13,5,{'graphs1to4':'exactnumbers and roundingerror<.05percentagepoint','wrong5':'2018computer17.4% not24.9%'})
h0=[296,250,266,320,324,276,306,237];h1=[335,276,289,353,346,306,324,262];w0=[70,56,48,68,79,62,95,58];w1=[75,52,51,82,95,85,107,72]
b0=[F(100*w,h) for w,h in zip(w0,h0)];b1=[F(100*w,h) for w,h in zip(w1,h1)]
assert all(17<v<34 for v in b1)
assert sum(v<20 for v in b0)==1 and sum(v<20 for v in b1)==2
assert [i for i in range(8) if 20<=b0[i]<25 and 20<=b1[i]<25]==[0,3]
assert sum(w0)==536 and sum(w1)==619 and 10*(619-536)>536
assert b1.index(max(b1))==6 and b1.index(min(b1))==2 and max(b1)<2*min(b1)
bounds=[]
for x,y in zip(h0,h1):
 lx=isqrt(x*10000);ly=isqrt(y*10000)
 assert F(lx,1000)**2<=F(x,100)<F(lx+1,1000)**2
 assert F(ly,1000)**2<=F(y,100)<F(ly+1,1000)**2
 bounds.append((F(ly-lx-1,1000),F(ly+1-lx,1000)))
assert bounds[0][0]>max(b[1] for b in bounds[1:])
note(15,5,{'BMI2022Bounds':'strictly17to34 -> max/min<2','underweight':[1,2],'bothNormal':['A','D'],'weights':[536,619],'heightDiffSafeIntervals':[[str(a),str(b)] for a,b in bounds]})
funds=[34463,34098,46221,63493,61455,72138,90332];counts=[214,301,321,608,632,713,792]
data=[3520,4583,8021,10603,11677,16581,18226];auto=[27082,19975,23046,25377,22949,24330,31383];fusion=[3861,9540,15154,27513,26829,31227,40723]
assert F(funds[0],counts[0])>160 and all(F(f,c)<150 for f,c in zip(funds[1:],counts[1:]))
assert [sum(x) for x in [data,auto,fusion]]==[73211,174142,154847]
assert F(63493-46221,46221)>F(37,100) and F(90332-72138,72138)<F(26,100)
assert F(data[-1]-data[3],data[3])>F(7,10)
assert F(auto[-1]-auto[3],auto[3])<F(1,4) and F(fusion[-1]-fusion[3],fusion[3])<F(1,2)
note(16,4,{'truth':[True,True,False,True],'fieldTotals':[73211,174142,154847],'growthBounds':['data>.7','auto<.25','fusion<.5']})
assert 29507-1316==28191>F(56330,2)==28165
assert 56330-28191==28139 and 71976-29507==42469<29507*2
assert 44012>F(71976)*F(3,5)
assert F(15346,24388)<F(2,3)<F(26289,39312)
assert F(4,50)<F(1,5)
note(18,4,{'maleApplicants':[28191,28139],'halfMaleTotal':28165,'commonPassRateBound':'2/3'})
assert 1300*F(14,10)*F(11,10)==2002>1849
assert 1710*F(11,10)==1881<1885 and 1100*F(165,100)==1815>1806
cTax=F(1885)/F(11,10)-F(1806)/F(165,100)
assert cTax==F(6810,11)>610>600
dtax=F(1827)/F(33,10);dcost=F(2024)/F(11,10)-dtax
assert dtax==F(6090,11) and dcost==F(14150,11) and dtax<dcost/2
note(25,2,{'truth':[False,True,False],'safeMayCTaxLowerBound':610,'exactMayCTax':str(cTax),'JuneDfixedTax':str(dtax),'JuneDcost':str(dcost)})
with pdfplumber.open(R/'artifacts/psat600_20261028/sources/4341/BBSMSTR_000000000138_4341_2.pdf') as pdf:
 t=pdf.pages[1].extract_text();assert '자료해석' in t
 key={}
 for line in t.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
   v=list(map(int,line.split()));key.update(zip(v[::2],v[1::2]))
 assert len(key)==25
norm=lambda s:re.sub(r'\s+','',s)
for q in bank:
 n=q['number'];raw=(A/f'2023-d{n}-source.txt').read_text(encoding='utf-8').split(f'{n}.',1)[1];prompt,tail=raw.split('?',1)
 assert norm(q['prompt'])==norm(prompt+'?')
 assert q['answer']==key[n]
 if n in [8,13]:
  assert q['choices']==[f'자료 {i}' for i in range(1,6)]
  assert [f['caption'] for f in q['figures'][1:]]==[f'선택지 {i}' for i in '①②③④⑤']
 else:
  opts=re.split('[①②③④⑤]','①'+tail.split('①',1)[1])[1:]
  assert len(opts)==5 and all(norm(a)==norm(b) for a,b in zip(opts,q['choices']))
 assert len(q['steps'])==len(q['optionReasons'])==5
 for st,prefix in zip(q['steps'],['착안점: ','실전 풀이: ','답 확정 기준: ','정석 근거: ','적용 한계: ']):assert st.startswith(prefix) and len(st)>40
 assert not any(c in json.dumps(q,ensure_ascii=False) for c in ['\u2060','\ufffd'])
# Every figure is a deterministic crop of the official PDF, with text boundaries intact.
manifest=json.loads((A/'crop-manifest.json').read_text(encoding='utf-8'));assert len(manifest)==33
with pdfplumber.open(R/manifest[0]['source']) as pdf:
 for f in manifest:
  assert hashlib.sha256((R/f['source']).read_bytes()).hexdigest()==f['sha256']
  path=R/f['asset'] if P.exists() else A/'staged'/f['asset']
  im=Image.open(path).convert('RGB');ref=pdf.pages[f['page1based']-1].crop(f['rect']).to_image(resolution=f['resolution']).original.convert('RGB')
  assert im.size==ref.size and im.tobytes()==ref.tobytes(),f['asset']
  x0,y0,x1,y1=f['rect']
  for w in pdf.pages[f['page1based']-1].extract_words():
   if w['x1']<=x0 or w['x0']>=x1 or w['bottom']<=y0 or w['top']>=y1:continue
   assert w['x0']>=x0-.5 and w['x1']<=x1+.5 and w['top']>=y0-.5 and w['bottom']<=y1+.5,(f['asset'],w['text'])
seen=set();old=0
for path in (R/'assets/psat').glob('*.json'):
 if path.name in ['sets.json','data05.json']:continue
 obj=json.loads(path.read_text(encoding='utf-8'))
 if isinstance(obj,list):
  for q in obj:
   k=(q.get('examDate',q['source'][:10].replace('.','-')),q['subject'],q['number']);assert k not in seen;seen.add(k);old+=1
for q in bank:
 k=(q['examDate'],q['subject'],q['number']);assert k not in seen;seen.add(k)
for path,digest in json.loads((A/'before-data05-hashes.json').read_text(encoding='utf-8')).items():
 if path=='assets/psat/sets.json':continue
 assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
checks.update(status='PASS',count=10,officialFinalKeys=10,figures=33,preservedExisting=old,limitations='Same-author visual/source review with exact rational and square-root bounds; not independent expert certification.')
(A/'content-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PASS:10keys,33pixelmatchedfigures,all source text/choice mappings,exactratio/rootbounds,existing',old)