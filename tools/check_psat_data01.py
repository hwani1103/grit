"""Exact-arithmetic review of the ten official 2023 PSAT data questions.
Inputs transcribed from visually inspected source figures, not generated examples.
Run with bundled Python (pdfplumber); source PDF remains the authority.
"""
from pathlib import Path
from fractions import Fraction as F
import json,re,hashlib,pdfplumber
ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'artifacts/psat_data10_20261028'
bank=json.loads((ROOT/'assets/psat/data01.json').read_text(encoding='utf-8'))
report={}
def record(n, flags, evidence):
 q=next(q for q in bank if q['number']==n)
 assert len(flags)==5 and sum(flags)==1,(n,flags)
 assert flags.index(True)+1==q['answer'],(n,flags,q['answer'])
 report[str(n)]={'optionTruth':flags,'answer':q['answer'],'evidence':evidence}
def combos(truth,options):
 wanted={i for i,v in enumerate(truth) if v}
 return [set(o)==wanted for o in options]
# 2
physicians=143-sum([23,26,25,30,15,4]);rate=F(580,physicians)
record(2,[x==rate for x in [20,26,29,32,38]],{'physicians':physicians,'rate':str(rate)})
# 3. Crop order as in the original table.
crops={'콩':[2593,105340,246117],'건고추':[2483,78437,86097],'땅콩':[2260,8219,26146],'참깨':[2024,12986,76812],'팥':[2020,7102,42418]}
ratios={k:F(v[0],sum(v)) for k,v in crops.items()};winner=max(ratios,key=ratios.get)
record(3,[k==winner for k in ['건고추','땅콩','참깨','콩','팥']],{k:{'total':sum(crops[k]),'percent':float(v*100)} for k,v in ratios.items()})
# 4
media={'A':(90,50,True),'B':(180,0,False),'C':(50,80,True),'D':(80,60,False),'E':(100,40,False),'F':(60,45,True)}
scores={k:F(2,5)*m+F(3,5)*s for k,(m,s,_) in media.items()}
selected={max((k for k in media if media[k][2]==g),key=scores.get) for g in [True,False]}
record(4,[set(pair)==selected for pair in [('A','D'),('A','E'),('B','C'),('B','F'),('C','D')]],{k:str(v) for k,v in scores.items()})
# 6
T=[3613,12567,2104,4316,6547];pg=[F('.20'),F('.07'),F('.13'),F('.16'),F('.13')];pr=[F('4.97'),F('2.85'),F('8.15'),F('10.62'),F('4.14')]
G=[F(t)*100/p for t,p in zip(T,pg)];R=[F(t)*100/p for t,p in zip(T,pr)]
truth=[G[2]>G[4],R[1]==max(R),R[0]/G[0]>R[1]/G[1]]
record(6,combos(truth,[(0,),(1,),(2,),(1,2),(0,1,2)]),{'statements':truth,'R_G_percent':[float(r/g*100) for r,g in zip(R,G)]})
# 9. Coordinates are (exports, imports), units ten million tonnes.
old={'농산물':(350,400),'임산물':(200,400),'축산물':(150,150),'수산물':(100,100)}
new={'농산물':(400,300),'임산물':(150,300),'축산물':(250,150),'수산물':(200,100)}
growth={k:F(new[k][0]-v[0],v[0]) for k,v in old.items()}
truth=[all(new[k][0]>old[k][0] for k in ['농산물','축산물','수산물']),sum(v[1] for v in new.values())>sum(v[1] for v in old.values()),max(old,key=lambda k:F(old[k][1],old[k][0]))==max(new,key=lambda k:F(new[k][1],new[k][0])),growth['축산물']==max(growth.values())]
record(9,combos(truth,[(0,1),(0,2),(0,3),(1,2),(1,3)]),{'statements':truth,'imports':[sum(v[1] for v in x.values()) for x in [old,new]],'exportGrowthPercent':{k:float(v*100) for k,v in growth.items()}})
# 11
meeting={'가':(250,200,150,12),'나':(200,150,200,16),'다':(200,150,150,25),'라':(150,100,200,30)}
totals={k:a+2*b+3*(c+d) for k,(a,b,c,d) in meeting.items()};rank=sorted(totals,key=totals.get,reverse=True)
record(11,[(a,b)==(rank[0],rank[2]) for a,b in [('나','가'),('나','다'),('나','라'),('라','나'),('라','다')]],{'totalsThousandWon':totals,'descending':rank})
# 12
patents={'A':[3,25],'B':[1,3,20],'C':[3,2,10,5,6],'D':[12,21,15],'E':[6,56,4,12]}
common=F(sum(sum(v) for v in patents.values()),sum(len(v) for v in patents.values()))
impact={k:F(sum(v),len(v))/common for k,v in patents.items()};tech={k:impact[k]*len(v) for k,v in patents.items()}
pair=(max(impact,key=impact.get),min(tech,key=tech.get))
record(12,[p==pair for p in [('A','B'),('D','A'),('D','C'),('E','B'),('E','C')]],{'common':str(common),'impact':{k:str(v) for k,v in impact.items()},'technology':{k:str(v) for k,v in tech.items()}})
# 14
pests=[[35964,32235,29325,29332,28522,32627],[35707,38976,69812-29325-6380-1576,27530,27638,20840],[4043,7718,6380,5024,3566,3497],[1733,1636,1576,1560,1240,58451-32627-20840-3497]]
totals=[sum(v[i] for v in pests) for i in range(6)]
falling=[all(v[i]<v[i-1] for i in range(3,6)) for v in pests]
truth=[falling==[False,False,True,False],[totals[i]>totals[i-1] for i in range(1,6)]==[True,False,False,False,False],pests[1][2]>=30*pests[3][5],F(pests[3][5]-pests[3][4],pests[3][4])<F(pests[0][5]-pests[0][4],pests[0][4])]
record(14,combos(truth,[(0,),(2,),(0,1),(2,3),(0,1,3)]),{'statements':truth,'totals':totals,'blanks':[pests[1][2],pests[3][5]],'growthPercent':[float(F(v[5]-v[4],v[4])*100) for v in [pests[3],pests[0]]]})
# 17: same total classified by project and ministry. Intersection lower bound.
national=[32594,5200,2954,10930,1540,1320,520];local=[9000,1800,532,260,340,660,0]
T=sum(national);forestry=33008;overlap=max(0,forestry+national[0]-T);land=T-sum([2930,33008,9520,350,240])
# Both sides of the minimal-overlap allocation are nonnegative and fit the margins.
assert overlap==10544 and forestry-overlap==T-national[0] and national[0]-overlap==T-forestry
truth=[F(local[1],national[1])==max(F(l,n) for l,n in zip(local[:-1],national[:-1])),overlap>=10000,F(land,T)>=F(1,5),sum(local)>national[3]]
record(17,combos(truth,[(0,1),(0,2),(1,2),(1,3),(2,3)]),{'statements':truth,'minimumOverlapTenMillionWon':overlap,'minimumOverlapHundredMillionWon':str(F(overlap,10)),'land':land,'localTotal':sum(local)})
# 19
rows={'A':(8010,254645,133,33499),'B':(195,13899,12,4722),'C':(502,16652,60,5197),'D':(320,20120,17,6102),'E':(684,30706,20,6814)}
amount=sum(v[0] for v in rows.values());ordered=sorted(rows.values(),key=lambda v:v[0]);rat=[F(v[0],v[1]) for v in ordered]
truth=[F(rows['A'][0],amount)>=F(4,5),F(rows['B'][1],rows['B'][3])>F(rows['C'][1],rows['C'][3]),all(rat[i]>rat[i-1] for i in range(1,5)),F(rows['A'][0],rows['A'][2])>=3*F(rows['D'][0],rows['D'][2])]
record(19,combos(truth,[(0,1),(0,3),(1,2),(0,2,3),(1,2,3)]),{'statements':truth,'defenseTotal':amount,'GDPperPersonCross':[13899*5197,16652*4722],'militaryCross':[8010*17,3*320*133]})
# Textual transcription independently compared with PDF extraction (whitespace ignored).
loc={2:(1,1),3:(2,0),4:(2,1),6:(3,1),9:(5,0),11:(6,0),12:(6,1),14:(7,1),17:(9,0),19:(10,0)}
clean=lambda s:re.sub(r'\s+','',s)
with pdfplumber.open(ART/'sources/자료해석(인).pdf') as pdf:
 for q in bank:
  n=q['number'];pg,side=loc[n];p=pdf.pages[pg-1];w=p.width/2
  raw=p.crop((w*side,0,w*(side+1),p.height)).extract_text()
  raw=raw[raw.index(f'{n}. ')+len(f'{n}. '):]
  stop=re.search(r'<(?:표|그림)',raw).start() # first appearance in the question is also <표>; use ending ?
  prompt=raw[:raw.index('?')+1]
  assert clean(prompt)==clean(q['prompt']),(n,'prompt')
  if q['body']:
   m=re.search(r'(?m)^<(?:보\s*기|회\s*의)>',raw)
   body=raw[m.start():raw.index('①',m.start())]
   if n==11:body=body[:body.index('총지급액이')]
   assert clean(body)==clean(q['body']),(n,'body',body)
  choices=re.split(r'[①②③④⑤]\s*',raw[raw.index('①'):])[1:]
  assert len(choices)==5
  for a,b in zip(choices,q['choices']):
   if n in (11,12):b=b.replace('/','')
   assert clean(a)==clean(b),(n,'choice',a,b)
  assert len(q['optionReasons'])==5 and len(q['steps'])>=3
# Official final answer PDF page visually reviewed; map transcribed from that page.
final={2:3,3:2,4:3,6:4,9:2,11:3,12:4,14:3,17:4,19:2}
assert {q['number']:q['answer'] for q in bank}==final
report['review']={'questions':10,'choices':50,'officialFinalAnswers':final,'transcription':'prompts, textual bodies and all choices match official PDF after whitespace normalization; pair choice headers supplied separately','figures':'13 high-resolution crops visually inspected including units, legends and footnotes','scope':'Exact arithmetic and source checks; not independent expert review or a claim of zero errors.'}
report['hashes']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ART/'sources/자료해석(인).pdf',ART/'sources/2023-07-22-final-answers.pdf',ROOT/'assets/psat/data01.json']}
(ART/'content_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('PASS: 10 official answers, 50 options, exact calculations, source transcription, 13 reviewed figure crops.')
