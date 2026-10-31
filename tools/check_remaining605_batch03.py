"""Original PDF/figure fidelity and exact independent numeric models for batch03."""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import json
import re
import shutil
import subprocess
import pdfplumber
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts/psat_remaining605_20261030/batch03'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
norm=lambda s:re.sub(r'[\s①②③④⑤·ㆍ․/]','',s)
items=read(OUT/'revealed-current.json')
solves={x['id']:x for x in read(OUT/'own-solves.json')}
sources={x['id']:x for x in read(OUT/'blind-source.json')}
reg={x['newAsset']:x for x in read(ROOT/'artifacts/psat_final_quality_20261029/full900/native-image-repairs.json')['figures']}
checks=[];pixels=[];cache={};pdfcache={}
try:
 for item in items:
  q=item['question'];m=sources[q['id']];src=ROOT/m['source']
  if src not in pdfcache:pdfcache[src]=pdfplumber.open(src)
  page=pdfcache[src].pages[m['page']-1];left=page.width*m['side']/2;right=page.width*(m['side']+1)/2
  marker=next(w for w in page.extract_words() if w['text']==str(q['number'])+'.' and left<=w['x0']<left+45)
  rectangles=[reg[f['asset']]['rect'] for f in q['figures']]
  def keep(obj):
   if obj.get('object_type')!='char':return True
   x=(obj['x0']+obj['x1'])/2;y=(obj['top']+obj['bottom'])/2
   return not any(a<=x<=c and b<=y<=d for a,b,c,d in rectangles)
  native=page.crop((left,marker['top']-1,right,page.height)).filter(keep).extract_text() or ''
  native=norm(re.sub(r'^\d+[.]\s*','',native))
  headings={
   '2023-07-22-d-11':('총지급액이총지급액이가장큰회의세번째로큰회의','왼쪽: 총지급액이 가장 큰 회의 / 오른쪽: 세 번째로 큰 회의'),
   'kr-mpm-2024-07-27-psat-d-01':('가장높은도시가장낮은도시','가장 높은 도시 / 가장 낮은 도시')}
  if q['id'] in headings:
   heading,note=headings[q['id']];assert native.count(heading)==1;assert q['choiceNote']==note
   native=native.replace(heading,'',1)
  assert native==norm(q['prompt']+q['body']+''.join(q['choices'])),q['id']
  with pdfplumber.open(ROOT/item['officialKey']) as pdf:
   keypage,keytext=next((i+1,p.extract_text()) for i,p in enumerate(pdf.pages) if '영역 자료해석' in (p.extract_text() or ''))
  assert ('2023' if q['id'].startswith('2023') else '2024') in keytext and f"책형 {q['book']}" in keytext
  answers={}
  for line in keytext.splitlines():
   if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
    z=list(map(int,line.split()));answers.update(zip(z[::2],z[1::2]))
  assert len(answers)==25 and answers[q['number']]==q['answer']==solves[q['id']]['answer']
  checks.append(dict(id=q['id'],source=m['source'],sourcePage=m['page'],questionTop=marker['top'],
                     nativeTextAndFiveChoicesMatch=True,choiceHeaderMapping=headings.get(q['id']),
                     keyPdf=item['officialKey'],keyPage=keypage,answer=answers[q['number']]))
  for f in q['figures']:
   record=reg[f['asset']];assert record['source']==m['source']
   assert hashlib.sha256(src.read_bytes()).hexdigest()==record['sha256']
   signature=(m['source'],record['page1based'],record['resolution'])
   if signature not in cache:
    directory=OUT/'fresh-source-renders';directory.mkdir(exist_ok=True)
    prefix=directory/f"{record['sha256'][:16]}-p{record['page1based']:02d}-r{record['resolution']}"
    subprocess.run([shutil.which('pdftoppm'),'-r',str(record['resolution']),'-f',str(record['page1based']),
                    '-l',str(record['page1based']),'-singlefile','-png',str(src),str(prefix)],check=True,capture_output=True)
    cache[signature]=Image.open(prefix.with_suffix('.png')).convert('RGB')
   ref=cache[signature].crop(record['pixelBox']);actual=Image.open(ROOT/f['asset']).convert('RGB')
   assert actual.size==ref.size and actual.tobytes()==ref.tobytes(),f['asset']
   pixels.append(dict(id=q['id'],asset=f['asset'],source=record['source'],page=record['page1based'],
                      resolution=record['resolution'],pixelBox=record['pixelBox'],pixelMatch=True))
finally:
 for pdf in pdfcache.values():pdf.close()
 for im in cache.values():im.close()

doctor=143-sum([23,26,25,30,15,4]);assert doctor==20 and F(580,doctor)==29
imports={'콩':[2593,105340,246117],'건고추':[2483,78437,86097],'땅콩':[2260,8219,26146],'참깨':[2024,12986,76812],'팥':[2020,7102,42418]}
import_ratios={k:F(v[0],sum(v)) for k,v in imports.items()};assert max(import_ratios,key=import_ratios.get)=='땅콩'
assert import_ratios['땅콩']>F(1,20) and all(v<F(1,20) for k,v in import_ratios.items() if k!='땅콩')
promotion={'A':(90,50,True),'B':(180,0,False),'C':(50,80,True),'D':(80,60,False),'E':(100,40,False),'F':(60,45,True)}
promotion_scores={k:2*m+3*s for k,(m,s,_) in promotion.items()}
assert [max((k for k,v in promotion.items() if v[2]==experienced),key=promotion_scores.get) for experienced in [True,False]]==['C','B']
research={'A':(3613,F('0.20'),F('4.97')),'B':(12567,F('0.07'),F('2.85')),'C':(2104,F('0.13'),F('8.15')),'D':(4316,F('0.16'),F('10.62')),'E':(6547,F('0.13'),F('4.14'))}
gdp={k:F(t)*100/g for k,(t,g,rr) in research.items()};spending={k:F(t)*100/rr for k,(t,g,rr) in research.items()};share={k:g/rr for k,(t,g,rr) in research.items()}
assert [gdp['C']>gdp['E'],max(spending,key=spending.get)=='B',share['A']>share['B']]==[False,True,True]
assert F(2104)*100/F('.125')<F(6547)*100/F('.135')
assert F('.195')/F('4.975')>F('.075')/F('2.845')
trade2020={'농':(350,400),'임':(200,400),'축':(150,150),'수':(100,100)}
trade2021={'농':(400,300),'임':(150,300),'축':(250,150),'수':(200,100)}
growth={k:F(trade2021[k][0]-v[0],v[0]) for k,v in trade2020.items()}
trade_truth=[all(trade2021[k][0]>trade2020[k][0] for k in ['농','축','수']),sum(v[1] for v in trade2021.values())>sum(v[1] for v in trade2020.values()),max(trade2020,key=lambda k:F(trade2020[k][1],trade2020[k][0]))==max(trade2021,key=lambda k:F(trade2021[k][1],trade2021[k][0])),max(growth,key=growth.get)=='축'];assert trade_truth==[True,False,True,False]
meetings={'가':(250,200,150,12),'나':(200,150,200,16),'다':(200,150,150,25),'라':(150,100,200,30)}
costs={k:chair+member*2+(attendance+travel)*3 for k,(chair,member,attendance,travel) in meetings.items()};assert sorted(costs,key=costs.get,reverse=True)==['나','가','라','다']
pests={'흰':[35964,32235,29325,29332,28522,32627],'솔':[35707,38976,None,27530,27638,20840],'깍':[4043,7718,6380,5024,3566,3497],'참':[1733,1636,1576,1560,1240,None]}
totals=[77447,None,69812,63446,60966,58451];totals[1]=sum(v[1] for v in pests.values());pests['솔'][2]=totals[2]-sum(pests[k][2] for k in ['흰','깍','참']);pests['참'][5]=totals[5]-sum(pests[k][5] for k in ['흰','솔','깍'])
pest_rates={k:F(v[5]-v[4],v[4]) for k,v in pests.items()}
pest_truth=[[k for k,v in pests.items() if all(v[i+1]<v[i] for i in range(2,5))]==['깍'],[i for i in range(1,6) if totals[i]>totals[i-1]]==[1],pests['솔'][2]>=30*pests['참'][5],pest_rates['참']<pest_rates['흰']];assert pest_truth==[True,True,False,False]
assert pest_rates['참']>F(1,6)>pest_rates['흰']
sectors=[32594,5200,2954,10930,1540,1320,520];local=[9000,1800,532,260,340,660,0];ministries=[2930,33008,9010,9520,350,240];T=sum(sectors)
assert T==55058==sum(ministries);lower=max(0,sectors[0]+ministries[1]-T)
matrix=[[2930,lower,9010,9520,350,240]]+[[0,x,0,0,0,0] for x in sectors[1:]]
assert [sum(row) for row in matrix]==sectors and [sum(row[j] for row in matrix) for j in range(6)]==ministries
support_truth=[max(range(6),key=lambda i:F(local[i],sectors[i]))==1,F(lower,10)>=1000,F(ministries[2],T)>=F(1,5),sum(local)>sectors[3]];assert support_truth==[False,True,False,True]
fatal={'A':F(16,300),'B':F(1,20),'C':F(2,50),'D':F(6,100),'E':F(9,200)};assert max(fatal,key=fatal.get)=='D' and min(fatal,key=fatal.get)=='C'
construction=dict(A=3*30,AB=7*22,AC=5*34,BC=6*24);B=construction['AB']-construction['A'];C=construction['AC']-construction['A'];assert B+C==construction['BC'] and F(construction['A']+construction['BC'],9)==26
result=dict(status='PASS',officialKeysAndNativeSource=checks,figurePixels=pixels,
            sourceVisualScope='All10 complete original columns visually inspected; d14 previous-question material excluded at actual14 heading. Pixel equality alone is not semantic/visual proof.',
            doctor=dict(count=doctor,perDoctor=str(F(580,doctor))),imports={k:str(v) for k,v in import_ratios.items()},promotionScoresTimes5=promotion_scores,
            research=dict(gdp={k:str(v) for k,v in gdp.items()},spending={k:str(v) for k,v in spending.items()},researchToGdp={k:str(v) for k,v in share.items()},roundingBoundaryStillSeparated=True),
            trade=dict(truth=trade_truth,growth={k:str(v) for k,v in growth.items()}),meetingCosts=costs,
            pests=dict(totals=totals,rows=pests,truth=pest_truth,rates={k:str(v) for k,v in pest_rates.items()}),
            support=dict(truth=support_truth,lowerBound=lower,feasibleMatrixAtLowerBound=matrix,localTotal=sum(local),transportMinistry=ministries[2]),
            fatality={k:str(v) for k,v in fatal.items()},construction=dict(totals=construction,B=B,C=C,overallAverage=26),
            limitations='Same-author independent input transcription and models; no expert independence or real-device verification.')
(OUT/'source-key-model-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PASS:10 direct PDF keys/native texts,12 newly rendered figure pixel comparisons,10 exact numeric models with rounding/boundary/feasibility checks.')
