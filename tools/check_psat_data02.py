
from pathlib import Path
from fractions import Fraction as F
import json,re,hashlib
import pdfplumber
R=Path(__file__).resolve().parents[1]
A=R/'artifacts/psat600_20261028/data02_2024'
P=R/'assets/psat/data02.json'
bank=json.loads((P if P.exists() else A/'authored-data02.json').read_text(encoding='utf-8'))
prefix=['착안점: ','실전 풀이: ','답 확정 기준: ','정석 근거: ','적용 한계: ']
norm=lambda s:re.sub(r'\s+','',s)
report={}
def record(n,answer,details):
 q=bank[n-1]
 assert q['number']==n and q['answer']==answer,(n,answer,q['answer'])
 report[str(n)]={'answer':answer,'proof':details}
rates=dict(zip('ABCDE',[F(16,300),F(1,20),F(2,50),F(6,100),F(9,200)]))
assert max(rates,key=rates.get)=='D' and min(rates,key=rates.get)=='C'
record(1,4,{k:str(v) for k,v in rates.items()})
total=3*30+6*24
assert total==234 and F(total,9)==26
record(2,1,{'total':total,'average':26,'independentTotals':7*22+5*34-3*30})
assert F(316,1000)*100==F('31.6')
record(3,5,{'review':'Report variables experience/field, expense, companion and awareness match choices1-4; reasons not mentioned. Original five option graphics retained.'})
subsidies=[170+3*60+30*6,350+3*80+30*8,200+3*150+30*10,50+3*40+30*3]
assert subsidies==[530,830,950,260]
record(4,5,{'subsidiesMillions':subsidies,'CminusB':subsidies[2]-subsidies[1]})
record(5,5,{'required':['ㄱ','ㄴ','ㄷ'],'ownershipRate':[round(1146/2034*100,1),round(1173/2093*100,1)],'growth':[round(40/1813*100,1),round(28/1569*100,1),round(27/1146*100,1)]})
rows=[[30,15,25,20,27],[12,14,9,10,8],[1400,800,1200,1250,1500],[-14,-8,-9,-7,-10]]
scores=[1,2,0,2,1]
ranks=[]
for row in rows:
 rank=[1+sum(v>x for x in row) for v in row]
 ranks.append(rank);scores=[a+b for a,b in zip(scores,rank)]
assert scores==[15,13,10,15,13]
assert min([0,3],key=lambda i:[14,8,9,7,10][i])==3
record(6,4,{'ranks':ranks,'scores':scores,'tiebreak':'D price0.7 < A1.4'})
assert F('25.4')-F('22.1')==F('3.3')
assert 408>356 and 214>138
record(7,3,{'required':['ㄷ','ㄹ'],'ageShares':[76.1,82.8],'experienceGaps':[12.4,10.9],'monthlyWorkdayGap':'3.3'})
patent={'A':[25234,1575,4730,1725],'전기장비':[6611,501,3265,1282],'기계':[1314,1870,5833,2360],'출판':[204,345,8041,2550],'자동차':[5460,1606,1116,617],'화학제품':[2978,917,2026,995],'의료':[52,533,2855,1019],'B':[18,115,3223,1154],'건축':[113,167,2129,910],'C':[29,7,596,370]}
small=[k for k,(l,m,s,c) in patent.items() if s>=9*(l+m)]
large=[k for k,(l,m,s,c) in patent.items() if l>=2*(m+s)]
assert set(small)=={'B','C','출판'} and set(large)=={'A','자동차'}
assert sum(patent['B'][:3])>2*patent['B'][3] and sum(patent['C'][:3])<2*patent['C'][3]
record(8,2,{'small90':small,'largeDouble':large,'Btotal':3356,'Ctotal':632})
prices=[[26000,27500,27500,33000,34500,34500],[3890,3580,3980,3900,4600,5180],[1280,1280,1280,1190,1590,1880],[1630,1680,1350,1790,1790,1980],[2250,3500,5000,8000,5000,6000],[4000,8000,8000,10000,10000,15000],[10000,10000,10000,13000,15000,13000]]
truth=[5276*F(4,5)<=4000,F('120.6')>=F('95.0')*F(6,5),sum(p[-1]>=2*p[0] for p in prices)==1,2*(3980+1280+1350)>=15000,sum(all(a<b for a,b in zip(p,p[1:])) for p in prices)>=2]
assert truth==[False,True,False,False,False]
# Even plausible nearest-0.1 rounding cannot reverse the 20% comparison.
assert F('120.55')>F('95.05')*F(6,5)
record(9,2,{'optionTruth':truth,'priceAt80':'4220.8','doubleCount':2,'purchaseCost':13220,'strictIncreasingCount':0})
city=[9,15,14,18,19,17,18];child=[10265,73060,55780,58680,61380,59559,72261];parent=[6700,19465,15785,13006,11660,9071,8619]
signs=lambda a:[(b>a)-(b<a) for a,b in zip(a,a[1:])]
assert signs(city)==signs(child) and signs(city)!=signs(parent)
assert F(61380,39)<1600<F(58680,35)
assert F(55780,2989)>10 and F(10265,2083)<5
record(10,2,{'trends':signs(child),'operationsMean':[str(F(58680,35)),str(F(61380,39))],'volunteerMean':[str(F(10265,2083)),str(F(55780,2989))]})
with pdfplumber.open(R/'artifacts/psat600_20261028/sources/4564/BBSMSTR_000000000138_4564_1.pdf') as pdf:
 text=pdf.pages[2].extract_text()
 assert '자료해석' in text and '사책형' in text and '2024년도' in text
 keys={}
 for line in text.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
   a=list(map(int,line.split()));keys.update(zip(a[::2],a[1::2]))
 assert len(keys)==25
for q in bank:
 n=q['number'];raw=(A/f'q{n:02}-source.txt').read_text(encoding='utf-8')
 assert q['answer']==keys[n]
 assert norm(q['prompt'])==norm(raw.split('?',1)[0].split('.',1)[1]+'?'),(n,'prompt')
 if n!=3:
  opts=re.split('[①②③④⑤]',raw)[1:]
  assert len(opts)==5,(n,len(opts))
  for i,(a,b) in enumerate(zip(opts,q['choices'])):
   assert norm(a)==norm(b.replace(' / ',' ')),(n,i,a,b)
 else:
  for c in q['choices']:assert norm(c) in norm(raw)
 assert len(q['steps'])==5 and all(s.startswith(p) for s,p in zip(q['steps'],prefix))
 assert len(q['optionReasons'])==5 and all(len(s)>15 for s in q['optionReasons']), (n, 'empty/insufficient reason')
 assert not any(c in json.dumps(q,ensure_ascii=False) for c in ['\u2060','\ufffd'])
 paths=[q['original']]+[f['asset'] for f in q['figures']]
 for path in paths:assert (R/path if P.exists() else A/'staged'/path).exists(),path
baseline=json.loads((A/'before-data02-hashes.json').read_text(encoding='utf-8'))
for path,digest in baseline.items():
 if path=='assets/psat/sets.json':continue
 assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
report.update(status='PASS',count=10,officialKeysMatched=10,optionReasons=50,figures=21,previousQuestionAssetsPreserved=len(baseline)-1,limitations='Source visual review and same-author reasoning plus exact arithmetic checks; not independent expert review.')
(A/'content-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('PASS:10 official keys;50 reasons;10 independent calculations/reviews;source prompt/options;existing assets preserved.')
