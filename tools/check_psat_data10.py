from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import json,re,itertools as it,hashlib,pdfplumber
from PIL import Image
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/data10';P=R/'assets/psat/data10.json';bank=json.loads((P if P.exists() else A/'authored-data10.json').read_text(encoding='utf-8'));proof={}
cas=[492,536,589,640,734,612,665,841,670,592,594,507];acc=[240,211,263,269,307,277,260,311,302,273,256,249]
assert (sum(cas),sum(acc))==(7472,3218) and all(c>2*a for c,a in zip(cas,acc)) and min(cas)<=F('.6')*max(cas)
rest=100-sum(map(F,['65.3','6.9','1.5','3.4']));assert rest==F('22.9') and rest<7*F('3.4') and F('.6525')*sum(acc)>2000
proof['16']={'truth':[True,True,False,False],'casualtyTotal':sum(cas),'accidentTotal':sum(acc),'annualRatio':str(F(sum(cas),sum(acc))),'remainingPercent':str(rest),'roundingLowerStillAbove2000':str(F('.6525')*sum(acc))}
opts=[[58.6,20.9,100.9,92.9],[60.8,19.8,102.4,92.5],[63.5,20.1,115.7,92.0],[65.2,20.3,117.1,92.6],[65.8,20.6,118.7,93.7]]
constraints=[[58.5<=g<65.7,n<20.7,114<d<119.2,r>=92.5] for g,n,d,r in opts];assert [all(x) for x in constraints]==[False,False,False,True,False];proof['17']={'constraintsPerOption':constraints}
priv=354749-102025;delta=[102025-102906,priv-251261];oldmetro=F(119940,676479)*100;card=F(47,196)*100
assert delta==[-881,1463] and F('17.65')<oldmetro<F('17.75') and F('23.95')<card<F('24.05') and 18.2>float(oldmetro)
proof['18']={'truth':[True,False,False,True],'privateCapacity':priv,'capacityChanges':delta,'oldMetroPercent':str(oldmetro),'cardPercent':str(card),'publicDormCashInstallment':'private9;publicuniversity0;card0'}
bonuses=[[12,6,3],[5,20,5],[6,3,6],[6,6,12],[F('4.5')]*3,[6,6,12]];rates=[F('.2'),F('.1'),F('.05')];candidates=[sorted(set(F(row[0])/r for r in rates).intersection(*(set(F(x)/r for r in rates) for x in row[1:]))) for row in bonuses];salary=[]
for vals in it.product(*candidates):
 if all(Counter(F(bonuses[i][y])/vals[i] for i in range(6))==Counter({F('.2'):1,F('.1'):2,F('.05'):3}) for y in range(3)):salary.append(vals)
assert len(salary)==2 and {sum(x) for x in salary}=={490} and all(v[:3]==(60,100,60) and v[4]==90 and v[3]+v[5]==180 for v in salary);proof['19']={'allSalaryVectors':[[str(x) for x in row] for row in salary],'total':490}
# Each entry directly transcribed from the 6x6 visual map: region,capacity symbol.
grid=[[(4,'L'),(4,'S'),(3,'M'),(3,'L'),(4,'M'),(4,'L')],[(4,'S'),(3,'L'),(3,'M'),(3,'M'),(3,'S'),(4,'S')],[(4,'L'),(2,'M'),(2,'S'),(2,'M'),(3,'L'),(3,'S')],[(2,'M'),(1,'L'),(1,'L'),(1,'M'),(1,'L'),(2,'M')],[(2,'L'),(2,'S'),(3,'S'),(2,'L'),(2,'M'),(2,'S')],[(3,'L'),(3,'M'),(3,'S'),(4,'L'),(4,'M'),(4,'L')]];flat=sum(grid,[]);size=Counter(s for g,s in flat);strict=sum(g in [1,2] and s=='L' for g,s in flat);grade2L=sum(g==2 and s=='L' for g,s in flat);tn=sum(s!='S' for g,s in flat)
assert size==Counter(L=14,M=12,S=10) and strict==5 and grade2L==2 and tn==26 and size['L']<F('1.5')*size['S'] and tn>=5*strict;proof['20']={'grid':grid,'sizeCount':dict(size),'strictBODCOD':strict,'grade2L':grade2L,'nitrogen20':tn,'truth':[True,False,True,True]}
fixed=[[91,87,None,89,95],[89,86,90,88,None],[68,76,None,74,78],[71,72,85,74,None],[71,72,79,85,None]];means=[89,89,None,77,78];valid=[]
for row,mean in zip(fixed,means):
 candidates=[]
 for x in range(1,101):
  v=[x if z is None else z for z in row]
  if len(set(v))<5:continue
  avg=F(sum(sorted(v)[1:-1]),3)
  if mean is None or avg==mean:candidates.append((v,avg,{i for i,z in enumerate(v) if z in [min(v),max(v)]}))
 valid.append(candidates)
assert {v[2] for v,m,e in valid[0]}==set(range(1,87)) and {v[4] for v,m,e in valid[1]}==set(range(91,101)) and {v[4] for v,m,e in valid[3]}==set(range(86,101)) and {v[4] for v,m,e in valid[4]}=={83}
span=max(m for v,m,e in valid[2])-min(m for v,m,e in valid[2]);alwaysExcluded=[set.intersection(*(e for v,m,e in rows)) for rows in valid];assert span==F(10,3) and set.union(*alwaysExcluded)==set(range(5))
proof['21']={'truth':[True,False,False,True],'ByungMin':str(min(m for v,m,e in valid[2])),'ByungMax':str(max(m for v,m,e in valid[2])),'span':str(span),'alwaysExcludedByRow':[sorted(x) for x in alwaysExcluded]}
air=[[-2.5,1.6,-2.4,-4.5,-2.3],[-.3,3.2,-.5,-1.8,-.1],[5.2,7.4,4.5,4.2,5.1],[12.1,13.1,10.7,11.4,12.2],[17.4,17.6,15.9,16.8,17.2],[21.9,21.1,20.4,21.5,21.3],[25.9,25,24,24.5,24.4],[25.4,25.7,24.9,24.3,25],[20.8,21.2,20.7,18.9,19.7],[14.4,15.9,14.5,12.1,13],[6.9,9.6,7.2,4.8,6.1],[-.2,4,.6,-1.7,-.1]]
surface=[[-2.4,2.7,-1.2,-2.7,.3],[-.3,4.8,.8,-.7,2.8],[5.6,9.3,6.3,4.8,8.7],[13.4,15.7,13.4,12.6,16.3],[19.7,20.8,19.4,19.1,22],[24.8,24.2,24.5,24.4,25.9],[26.8,27.7,26.8,26.9,28.4],[27.4,28.5,27.5,27,29],[22.5,19.6,22.8,21.4,23.5],[14.8,17.9,15.8,13.5,16.9],[6.2,10.8,7.5,5.3,8.6],[-.1,4.7,1.1,-.7,2.1]];snow=list(map(F,['.5','.5','.7','.8','2']));wind=[30,45,35,30,40]
aMax=[max(range(12),key=lambda j:air[j][i])+1 for i in range(5)];sMax=[max(range(12),key=lambda j:surface[j][i])+1 for i in range(5)]
assert aMax==[7,8,8,7,8] and sMax==[8]*5 and [i for i in range(5) if air[1][i]<0<surface[1][i]]==[2,4] and surface[0].index(min(surface[0]))==3 and snow[3]<sum(snow)/5==F('.9') and sorted(range(5),key=lambda i:wind[i],reverse=True)[1]==4 and sorted(range(5),key=lambda i:air[7][i],reverse=True)[2]==4
proof['22']={'truth':[False,True,True,False],'airMaxMonth':aMax,'surfaceMaxMonth':sMax,'meanSnow':'.9'}
neg=[sum(air[j][i]<0 for j in range(12)) for i in range(5)];final=[max(1,snow[i]*F('1.5')*(F('1.4') if neg[i]>=3 else 1)*(F('.8') if wind[i]>=40 else 1)) for i in range(5)];growth=[x-s for x,s in zip(final,snow)];assert neg==[3,0,2,3,3] and final==list(map(F,['1.05','1','1.05','1.68','3.36'])) and sorted(range(5),key=lambda i:growth[i],reverse=True)==[4,3,0,1,2];proof['23']={'negativeMonths':neg,'final':list(map(str,final)),'absoluteIncrease':list(map(str,growth))}
traffic=[[7989,6957,18925,20052],[5991,6129,13344,13727],[4106,4457,3004,3610],[0,0,821,1717],[3006,3033,2515,2871],[4642,4676,5825,7266],[3738,3475,4859,5415],[2935,2873,3278,4128]];newCases=[153,106,23,44,57,98,85,72];delta=[13,-2,-6,7,16,-35,34,9];oldCases=[x-d for x,d in zip(newCases,delta)];assert oldCases==[140,108,29,37,41,133,51,63] and sum(oldCases)==602 and 486-7==479
national=[344,137,32,41,2,46];foreign=[235,133,33,32,9,37];assert sum(national)==602 and sum(foreign)==479
np=list(map(F,['57.14','22.76','5.32','6.81','.33','7.64']));fp=list(map(F,['49.06','27.77','6.89','6.68','1.88','7.72']))
assert all(abs(F(x,602)*100-p)<=F('.005') for x,p in zip(national,np)) and all(abs(F(x,479)*100-p)<=F('.005') for x,p in zip(foreign,fp))
wronggraph=list(map(F,['1.16','.82','.77','1.02','.18','.99']));assert all(abs(F(n,f)-g)>F('.02') for n,f,g in zip(national,foreign,wronggraph))
shares=[F(x,602)*100 for x in oldCases];shownShares=list(map(F,['23.3','17.9','4.8','6.1','6.8','22.1','8.5','10.5']));assert all(abs(x-y)<F('.05') for x,y in zip(shares,shownShares))
growths=[(F(r[1]+r[3],r[0]+r[2])-1)*100 for r in traffic[2:]];assert all(abs(x-y)<F('.05') for x,y in zip(growths,map(F,['13.5','109.1','6.9','14.1','3.4','12.7'])))
ratios=[[F(oldCases[i],traffic[i][0]+traffic[i][2])*1000,F(newCases[i],traffic[i][1]+traffic[i][3])*1000] for i in [0,1]];assert all(abs(x-y)<F('.05') for row,target in zip(ratios,[[F('5.2'),F('5.7')],[F('5.6'),F('5.3')]]) for x,y in zip(row,target))
proof['24']={'compatible':[False,True,True,True,True],'oldNational':602,'oldForeign':479,'wrongGraphActualRatios':list(map(str,[F(n,f) for n,f in zip(national,foreign)])),'oldByAirline':oldCases,'nationalByType':national,'growthPercent':list(map(str,growths)),'perMillion':[[str(x) for x in row] for row in ratios]}
fires=[277,197,296,492,623,391,692,496,653,620];assert sum(fires)==4737 and sum(fires)<=5000 and F(305,692)>F(73,197) and F(45,49)>F(6,9);rest=620-sum([49,65,75,9,1,54,150]);assert rest==217 and F(rest,620)==F('.35');proof['25']={'truth':[True,True,False,True],'decadeTotal':4737,'hikerFires':217,'counterexample':'9fires6caught vs49fires45caught'}
keys={}
with pdfplumber.open(next((R/'artifacts/psat600_20261028/sources/3982').glob('*.pdf'))) as pdf:
 t=next(p.extract_text() for p in pdf.pages if '영역 자료해석' in p.extract_text());assert '2021' in t and '나 책형' in t
 for line in t.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):v=list(map(int,line.split()));keys.update(zip(v[::2],v[1::2]))
assert [keys[n] for n in range(16,26)]==[1,4,3,3,4,2,2,5,1,5]
norm=lambda s:re.sub(r'[\s·]+','',s)
for q in bank:
 n=q['number'];raw=(A/f'2021-d{n}-source.txt').read_text(encoding='utf-8').split(f'{n}.',1)[1];prompt,tail=raw.split('?',1);assert norm(q['prompt'])==norm(prompt+'?')
 if n!=24:
  choices=re.split('[①②③④⑤]','①'+tail.split('①',1)[1])[1:];assert len(choices)==5 and all(norm(x)==norm(y) for x,y in zip(q['choices'],choices)),n
 else:assert q['choices']==[f'자료 {i}' for i in range(1,6)] and [f['caption'] for f in q['figures'][3:]]==[f'선택지 {c}' for c in '①②③④⑤']
 assert q['answer']==keys[n] and len(q['steps'])==len(q['optionReasons'])==5
 for s,prefix in zip(q['steps'],['착안점: ','실전 풀이: ','답 확정 기준: ','정석 근거: ','적용 한계: ']):assert s.startswith(prefix) and len(s)>40
 assert not any('\ue000'<=c<='\uf8ff' or c in '\ufffd\u2060\u2024' for c in json.dumps(q,ensure_ascii=False))
assert bank[6]['figures'][:4]==bank[7]['figures'][:4]
manifest=json.loads((A/'crop-manifest.json').read_text(encoding='utf-8'));originals=json.loads((A/'original-manifest.json').read_text(encoding='utf-8'));assert len(manifest)==33 and len(originals)==10
source=next((R/'artifacts/psat600_20261028/sources/3977/pdf').glob('*자료*'));digest=hashlib.sha256(source.read_bytes()).hexdigest()
with pdfplumber.open(source) as pdf:
 for c in manifest+originals:
  assert digest==c['sha256'];p=pdf.pages[c['page1based']-1];ref=p.crop(c['rect']).to_image(resolution=c['resolution'],antialias=True).original.convert('RGB');path=R/c['asset'] if P.exists() else A/'staged'/c['asset'];im=Image.open(path).convert('RGB');assert im.size==ref.size and im.tobytes()==ref.tobytes(),c['asset']
  if '/figures/' in c['asset']:
   x0,y0,x1,y1=c['rect']
   for w in p.extract_words():
    if w['x1']<=x0 or w['x0']>=x1 or w['bottom']<=y0 or w['top']>=y1:continue
    assert w['x0']>=x0-.5 and w['x1']<=x1+.5 and w['top']>=y0-.5 and w['bottom']<=y1+.5,(c['asset'],w)
seen=set();old=0
for path in (R/'assets/psat').glob('*.json'):
 if path.name in ['sets.json','data10.json']:continue
 obj=json.loads(path.read_text(encoding='utf-8'))
 if isinstance(obj,list):
  for q in obj:
   k=(q.get('examDate',q['source'][:10].replace('.','-')),q['subject'],q['number']);assert k not in seen;seen.add(k);old+=1
for q in bank:
 k=(q['examDate'],q['subject'],q['number']);assert k not in seen;seen.add(k)
for path,digest in json.loads((A/'before-data10-hashes.json').read_text(encoding='utf-8')).items():
 if path!='assets/psat/sets.json':assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
proof.update(status='PASS',count=10,officialFinalKeys=10,figures=33,originals=10,preservedExisting=old,limitations='Same-author source/map review plus exact arithmetic/exhaustive independent-form models;not independent expert certification.')
(A/'content-checks.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PASS10source/key/33figures/10originals;exactmodels;preserved',old)
