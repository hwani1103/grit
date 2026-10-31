from pathlib import Path
from fractions import Fraction as F
import json,re,hashlib,pdfplumber
from PIL import Image
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/data07';P=R/'assets/psat/data07.json'
bank=json.loads((P if P.exists() else A/'authored-data07.json').read_text(encoding='utf-8'));checks={}
def note(n,key,data):
 assert next(q for q in bank if q['number']==n)['answer']==key;checks[str(n)]=data
world=[[247,114,76,19,19],[225,112,68,21,23],[158,88,47,17,24],[156,83,45,21,17],[131,73,39,14,20],[118,74,32,22,20],[110,67,31,17,19],[104,55,30,14,11],[88,59,25,13,21]]
assert all(r[1]==sum(r[2:]) for r in world)
assert [i+1 for i,r in enumerate(world[:8]) if 2*r[2]<=r[1]]==[6,7]
avg=[F(r[0],r[1]) for r in world];assert avg[5]<avg[6] and 118*67==7906<8140==110*74
assert F(21,112)<F(22,74)
note(11,1,{'truth':[True,False,False],'winRateLEhalfRanks':[6,7],'averages':list(map(str,avg)),'scope':'top8 excludesUruguay'})
private=[[6333,8771,73,15177],[9393,7537,6,16936],[0,399,8,407],[0,64,0,64],[4,68,0,72],[7,62,0,69]]
public=[[833,2104,61,2998],[1135,1486,20,2641],[1916,2366,109,4391],[3422,1307,136,4865],[682,2813,174,3669],[307,2939,95,3341]]
assert all(sum(r[:3])==r[3] for r in private+public)
assert [sum(r[i] for r in private) for i in range(4)]==[15737,16901,87,32725]
combined=[15737+307,16901+2939,87+95];ratios=[F(r[2],r[1]) for r in private]
assert max(range(3),key=lambda i:combined[i])==1 and max(range(6),key=lambda i:ratios[i])==2 and max(range(6),key=lambda i:public[i][0])==3
assert ratios[2]>F(2,100) and all(r<F(1,100) for i,r in enumerate(ratios) if i!=2)
note(12,2,{'blanks':[73,8],'combined':combined,'hydrogenPerElectric':list(map(str,ratios)),'hybridPeak':2022})
points={'A':(52,63),'B':(66,63),'C':(58,41),'D':(50,18),'E':(50,90),'F':(77,48),'G':(72,89),'H':(16,45),'I':(71,87),'J':(90,93)}
indices={k:3*x+2*y for k,(x,y) in points.items()};assert indices==dict(zip('ABCDEFGHIJ',[282,324,256,186,330,327,394,138,387,456]))
assert [k for k,v in indices.items() if 150<=v<300]==['A','C','D'];assert all(all(t>70 for t in points[k]) and indices[k]>350 for k in 'GIJ')
note(13,1,{'visualCoordinates':points,'indices':indices,'boundary':'150included300excluded'})
awards=[[[8,24,12,26,15,27],[25,112,27,132,28,141],[41,253,37,281,39,277]],[[8,21,12,25,9,27],[25,112,31,109,36,117],[44,253,43,281,45,297]],[[4,24,5,26,6,27],[25,112,27,132,30,141],[41,253,37,281,39,277]],[[8,21,9,25,9,27],[25,112,31,115,36,117],[44,281,43,253,45,257]],[[4,24,5,26,6,27],[25,129,31,132,36,141],[41,351,37,281,39,314]]]
valid=[]
for rows in awards:
 increasing=all(r[c]<r[c+2]<r[c+4] for r in rows[:2] for c in [0,1]);growth=F(rows[1][4]-rows[1][0],rows[1][0])>=F(1,5);rates=[F(r[5],r[4]) for r in rows];order=rates[2]>rates[1]>rates[0];valid.append([increasing,growth,order])
assert [all(x) for x in valid]==[False,False,True,False,False]
assert F(28-25,25)==F(12,100) and F(141,36)<4<F(27,6)
note(14,3,{'threeConditionsByChoice':valid,'choice3rates':['27/6','141/30','277/39']})
affiliations=[[23,59,503],[22,60,540],[21,61,554],[19,62,534],[18,58,514]];meet=[69,88,78,55,62,101,59,78];budget=[336,71,90,60,27,6]
assert F(40,590)*100<7<F('7.3')
assert sum(affiliations[-1])==590 and all(r[2]>4*sum(r[:2]) for r in affiliations)
assert sum(meet)==590 and sum(meet[4:])==300>F(590,2)
assert sum(budget)==590 and sum(budget[3:])==93<590*F(1,5) and budget[0]>590*F(55,100)
note(15,5,{'truth':[False,True,False,True],'affiliations':affiliations,'meetings4plus':300,'budget50plus':93,'unbudgeted':336,'actualAdminShare':str(F(4000,590))})
exports=[('리비아',150087,54826),('이집트',58534,37197),('튀르키예',48501,21689),('요르단',30865,40762),('키르기스스탄',30734,13741),('아제르바이잔',17584,7675),('아랍에미리트연합',16777,7137),('타지키스탄',15758,12000),('알바니아',13752,1811),('몽골',10735,5491)]
tests={n:[F(y23,502028)<=F(1,10),F(y23,502028)>F(y22,303416),F(y22,1)/F(6,5)>=12000] for n,y23,y22 in exports};assert [n for n,cs in tests.items() if all(cs)]==['튀르키예']
assert 48501>2*21689 and 502028<2*303416
note(16,5,{'conditionsAll10':tests,'year2022LowerBound':14400})
length=[323,330,442,257];areas=list(map(F,['3.43','3.20','5.80','2.35']));urban=[F('11.79'),F('13.85'),areas[2]/F('.222'),areas[3]/F('.239')]
truth=[areas[0]/323>areas[3]/257,F(330,sum(length))>=F(1,4),urban[2]==max(urban),urban[3]<=10,sum(urban)>=50];assert truth==[True,False,True,True,True]
assert sum(length)==1352 and sum(length)/4==338
assert areas[0]/323>F(1,100)>areas[3]/257 and urban[2]>25 and 9<urban[3]<10 and sum(urban)>F('59.64')
note(17,2,{'choiceTruth':truth,'urbanAreas':list(map(str,urban)),'totalLength':sum(length),'quarter':338})
harm=[[2014,217,177,5,2413],[2096,294,167,20,2577],[1490,388,264,26,2168],[1107,354,333,50,1844],[885,502,390,57,1834]]
light=[[1792,353,53,75,140,2413],[1768,464,82,55,208,2577],[1176,626,41,107,218,2168],[829,560,44,120,291,1844],[827,522,90,101,294,1834]]
assert all(sum(r[:-1])==r[-1] for r in harm+light)
assert [sum(r[c] for r in harm) for c in range(5)]==[7592,1755,1331,158,10836]
assert [sum(r[c] for r in light) for c in range(6)]==[6392,2525,310,458,1151,10836]
assert 829+1107-1844==92
assert light[2][3]>light[1][3] and light[2][2]<light[1][2]
assert F(2096,2577)<F(85,100)
growth=[F(harm[i][2]-harm[i-1][2],harm[i-1][2]) for i in range(1,5)];assert growth[1]>F(1,2) and growth[-1]<F(1,5)
assert light[0][3]>light[0][2] and light[1][3]<light[1][2]
note(18,2,{'choiceTruth':[False,True,False,False,False],'intersectionLower':92,'eyeGrowth':list(map(str,growth)),'scope':'same2023complaintuniverse'})
aug=2222-1650-287;dec=3461-3141;pair=1370-273-229-282;mean=F(3461,12);assert aug==285<287 and dec==320 and dec-273>273*F(15,100)
assert 288<mean<289 and pair==586 and F(pair,2)>mean
possibleCounts=set()
for march in range(pair+1):
 months=[273,229,march,pair-march,282,280,287,aug,307,300,312,dec];assert sum(months)==3461;possibleCounts.add(sum(v>mean for v in months))
assert possibleCounts=={5,6}
note(19,5,{'truth':[False,True,True],'August':aug,'December':dec,'mean':str(mean),'MarchAprilSum':pair,'all587allocationsCounts':sorted(possibleCounts)})
shares=[[F(s) for s in row] for row in [['20.6','8.5','42.5','28.4'],['30.5','10.1','38.2','21.2'],['34.2','12.6','30.2','23.0'],['26.1','14.4','33.4','26.1'],['24.8','16.5','30.5','28.2'],['22.6','18.5','37.8','21.1']]]
# 2020 shares round to 100.0; data values are used as published.
assert all(sum(row)==100 for row in shares)
bdiff=[shares[i][1]-shares[i-1][1] for i in range(1,6)];assert all(x>=1 for x in bdiff)
wages=[139,160,135];expenses=[70,88,80];assert all(F(w,w+e)>=F(3,5) and w>F(3,2)*e for w,e in zip(wages,expenses))
project=1129-135-80-260;assert project==654<3*260
c21=902*shares[3][2]/shares[3][0];c22=1079*shares[4][2]/shares[4][0]
assert c22>1079*F(12,10)>902*F(13,10)>c21
note(20,4,{'truth':[True,False,True,True],'BshareIncrements':list(map(str,bdiff)),'project2023':project,'Camounts':[str(c21),str(c22)],'bounds':['2022>1294.8','2021<1172.6']})
with pdfplumber.open(next((R/'artifacts/psat600_20261028/sources/5994').glob('*.pdf'))) as pdf:
 t=next(p.extract_text() for p in pdf.pages if '영역 자료해석' in p.extract_text());assert '2025년도' in t and '인 책형' in t
 key={}
 for line in t.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
   v=list(map(int,line.split()));key.update(zip(v[::2],v[1::2]))
 assert len(key)==25
norm=lambda s:re.sub(r'[\s·]+','',s.replace('²','2'))
for q in bank:
 n=q['number'];raw=(A/f'2025-d{n}-source.txt').read_text(encoding='utf-8').split(f'{n}.',1)[1];prompt,tail=raw.split('?',1)
 assert norm(q['prompt'])==norm(prompt+'?')
 assert q['answer']==key[n]
 if n==14:
  assert q['choices']==[f'자료 {i}' for i in range(1,6)]
  assert [f['caption'] for f in q['figures'][1:]]==[f'선택지 {i}' for i in '①②③④⑤']
 else:
  opts=re.split('[①②③④⑤]','①'+tail.split('①',1)[1])[1:]
  assert len(opts)==5 and all(norm(a)==norm(b) for a,b in zip(opts,q['choices']))
 assert len(q['steps'])==len(q['optionReasons'])==5
 for st,prefix in zip(q['steps'],['착안점: ','실전 풀이: ','답 확정 기준: ','정석 근거: ','적용 한계: ']):assert st.startswith(prefix) and len(st)>40
 assert not any(c in json.dumps(q,ensure_ascii=False) for c in ['\u2060','\ufffd'])
# Every figure is a deterministic crop of the official PDF, with text boundaries intact.
manifest=json.loads((A/'crop-manifest.json').read_text(encoding='utf-8'));assert len(manifest)==28
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
 if path.name in ['sets.json','data07.json']:continue
 obj=json.loads(path.read_text(encoding='utf-8'))
 if isinstance(obj,list):
  for q in obj:
   k=(q.get('examDate',q['source'][:10].replace('.','-')),q['subject'],q['number']);assert k not in seen;seen.add(k);old+=1
for q in bank:
 k=(q['examDate'],q['subject'],q['number']);assert k not in seen;seen.add(k)
for path,digest in json.loads((A/'before-data07-hashes.json').read_text(encoding='utf-8')).items():
 if path=='assets/psat/sets.json':continue
 assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
checks.update(status='PASS',count=10,officialFinalKeys=10,figures=28,preservedExisting=old,limitations='Same-author visual/source review with exact rational comparisons and 587 missing-value allocations; not independent expert certification.')
(A/'content-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PASS:10keys,28pixelmatchedfigures,all source text/choice mappings,ratios/587allocations/counterexamples,existing',old)