from psat_batch_tools import ROOT,read,validate,norm
from pathlib import Path
from itertools import product
from fractions import Fraction as F
import runpy,pdfplumber
A=ROOT/'artifacts/psat600_20261028/situation21';raw=runpy.run_path(str(A/'solve_before_key.py'))
bank=read(A/'authored-situation21.json');by={q['number']:q for q in bank};own=read(A/'own-solve-before-key.json')
assert all(q['answer']==own[str(q['number'])]['answer'] for q in bank)
assert raw['q12']==[True,False,True]
assert len(raw['after_f'])==1 and raw['own'](raw['after_f'][0],5)==(1,0)
# Show why all non-S possibilities for 丁 leave the interchangeable 甲/乙 histories unresolved.
ambiguous_d={}
for info,worlds in raw['groups'].items():
 abc={(v[0][:3],v[1][:3]) for v in worlds}
 if info[1]!=2:
  assert len(abc)>1
  witness=next(w for w in worlds if w[1][0]==2 or w[1][1]==2)
  flipped=(tuple([witness[0][1],witness[0][0],*witness[0][2:]]),tuple([witness[1][1],witness[1][0],*witness[1][2:]]))
  assert flipped in worlds and flipped!=witness
  ambiguous_d[str(info)]=[witness,flipped]
# Reading rates are positive integers. Enumerate all rates consistent with the observed intervals.
reading=[]
for mon,tue,wed,thu,fri in product(range(1,15),repeat=5):
 if mon+2*tue+wed+thu+fri!=17 or wed+thu!=6 or fri+mon+tue!=8:continue
 rates=[mon,tue,wed,thu,fri,0,0];day=1;pages=0
 while pages<74:pages+=rates[day%7];day+=1
 assert (day-1)%7==2
 reading.append([mon,tue,wed,thu,fri])
assert reading and {sum(r) for r in reading}=={14} and {r[1] for r in reading}=={3}
assert raw['wallet_candidates']==[{'initial':3100,'afterStationery':2250,'afterFlower':1250,'afterConvenience':450,'optimalWallets':[(3,0,1,0)]}]
# Actual tender/change path, with minimum-cost wallets at every stage.
wallets=raw['wallets'];path=[(62,(3,0,1,0)),(45,(2,0,2,1)),(25,(1,0,2,1)),(9,(0,0,4,1))]
assert all(w in wallets(v)[1] for v,w in path)
assert 3100-850==2250 and 2250-1000==1250 and 1250-800==450
assert wallets(45)[0]==9 and sum(path[2][1][2:])==3
# Native tables are compared cell by cell against an independent fresh PDF table extraction.
source=ROOT/'artifacts/psat600_20261028/sources/4681/pdf/상황판단(가).pdf'
table_evidence={};transcribed=read(A/'source-tables.json')
with pdfplumber.open(source) as pdf:
 for n in [12,16,17,18]:
  p=pdf.pages[(n-1)//2];side=(n-1)%2;p=p.crop((p.width/2*side,43,p.width/2*(side+1),1016))
  tables=p.find_tables();assert len(tables)==1
  expected=tables[0].extract();record=transcribed[str(n)]
  assert record['cells']==expected
  assert by[n]['body']=='' and by[n]['tables']==[] and len(by[n]['figures'])==1
  table_evidence[str(n)]=dict(rows=len(expected),columns=len(expected[0]),cellsPreserved=True,display='Source image body with original row/column geometry')
def table(n):
 cells=transcribed[str(n)]['cells'];return dict(columns=cells[0],rows=cells[1:])
t=table(16); candidates=[]
for i,name in enumerate(t['columns'][1:],1):
 price=int(t['rows'][0][i].replace(',','').replace('원',''))
 date=int(t['rows'][1][i].split()[1].replace('일',''));loc=t['rows'][2][i];disc=t['rows'][3][i]=='○'
 if '바이올린' in name or date<9 or loc.startswith('B'):continue
 candidates.append([name.replace('\n',' '),F(price)*F(4,5) if disc else F(price)])
assert sorted(candidates,key=lambda x:x[1])[0]==['피아노 협주',F(96000)]
scores={};eligible=[]
for row in table(17)['rows']:
 name=row[0];a,b,c,d,e=[int(s[:-1]) for s in row[1:]]
 scores[name]=F(4,5)*a+F(1,5)*b+c-d-e
 if a>=80 and b>=40:eligible.append(name)
assert max(eligible,key=lambda name:scores[name])=='丙'
assert [scores[n] for n in '甲乙丙']==[74,75,76]
projects=[]
for row in table(18)['rows']:
 name,total,sub,used,request=row
 if request!='○':continue
 total,sub,used=[int(x.replace(',','')) for x in (total,sub,used)]
 projects.append((name,sub>used,F(sub,total),sub))
order=[p[0] for p in sorted(projects,key=lambda p:(p[1],p[2],p[3]),reverse=True)]
assert order==['E','D','B','A']
assert F(1,2)*2*30==30 and 1000*4*30//250==480 and F(500000)/F(5,2)==200000
assert [i+1 for i,c in enumerate(by[19]['choices']) if 'ㄱ' not in c and 'ㄷ' not in c]==[2]
assert by[21]['body'].startswith('제00조(수출입규제폐기물의 수출허가)\n\n①')
proof=dict(ownAnswers=[own[str(q['number'])]['answer'] for q in bank],codeWorlds=len(raw['worlds']),
 knowledgeModel=dict(public=len(raw['public']),afterD=len(raw['after_d']),afterE=len(raw['after_e']),afterF=len(raw['after_f']),nonS_DCounterexamples=ambiguous_d,unique=raw['after_f']),
 readingSchedules=reading,walletPath=path,walletBoundary='Final change positive, optimized coin-only final wallet <500; 800 after flower rejected because last change impossible.',
 sourceTableChecks=table_evidence,eligibleScores={n:str(scores[n]) for n in eligible},projectOrder=order,
 semanticReview={str(q['number']):own[str(q['number'])]['proof'] for q in bank},
 unitsNote='Original kW/MW wording retained; explanation distinguishes accumulated electrical energy in kWh/MWh; no source correction.',
 sourceVisualReview='All ten source columns/common page inspected, including exact show-column mapping and law hierarchy.')
validate('situation21',proof,[('2025-03-08',n) for n in range(12,22)],figure_count=4)
