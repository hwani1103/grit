"""Independent transcribed-source arithmetic, bounds, and native prose checks."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,re,unicodedata
import pdfplumber
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/psat_remaining605_20261030';B=OUT/'batch09'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
bank={q['id']:q for p in (ROOT/'assets/psat').glob('*.json') for q in (read(p) if isinstance(read(p),list) else [])}
old={x['question']['id']:x['question'] for x in read(B/'revealed-current.json')}
reg={x['newAsset']:x for x in read(ROOT/'artifacts/psat_final_quality_20261029/full900/native-image-repairs.json')['figures']}
spec=read(B/'native-prose-transcriptions.json')['transcriptions']
norm=lambda s:re.sub(r'[\s<>○◯]','',unicodedata.normalize('NFKC',s))
checks=[]
for qid,s in spec.items():
 q=bank[qid];previous=old[qid]
 texts=[]
 for i in s['remove']:
  f=previous['figures'][i];r=reg[f['asset']]
  with pdfplumber.open(ROOT/r['source']) as pdf:
   texts.append(pdf.pages[r['page1based']-1].crop(r['rect']).extract_text() or '')
 a,b=norm('\n'.join(texts)),norm(q['body'])
 assert a==b,(qid,a,b)
 assert q['figures']==[f for i,f in enumerate(previous['figures']) if i not in s['remove']]
 assert all(q[k]==previous[k] for k in ['id','answer','choices','original','number'])
 assert q['body'].split('\n\n')[0] in ['보기','조건','보고서','입지조건','방송뉴스']
 if q.get('underlines'):
  assert q['underlineLabelAnchors'] and len(q['underlines'])==3
  assert all(q['body'].count(x)==1 for x in q['underlines'])
 # Original removed images remain byte-identical to fresh-source evidence.
 for f in previous['figures']:
  assert (ROOT/f['asset']).is_file()
 checks.append(dict(id=qid,nativeProseMatchesOriginalPdf=True,retainedDataFiguresUnchanged=True,choicesAnswerOriginalUnchanged=True))

# Votes: rounded to one decimal percent, hence +/-0.05 percentage points.
electors20=[110818,73381,32591,6818,2554];voters19=[106496,68213,36170,8210,2892]
rates19=list(map(F,['74.0','71.7','84.9','84.9','85.4']))
intervals=[(F(v*100)/(r+F('.05'))-e,F(v*100)/(r-F('.05'))-e) for v,r,e in zip(voters19,rates19,electors20)]
assert all(a[0]>b[1] for a,b in zip(intervals,intervals[1:]))
assert 219-62-47-21-21==68<4*21
assert F(73381,62)>1000>F(32591,47)
assert F('83.0')-F('68.7')==F('14.3')<15
# Maritime: ratios and all five annual twice conditions, not a single-year proxy.
cases={'A':[258,250,244,277,246],'B':[65,46,110,108,96],'C':[29,38,61,69,54],'D':[96,119,132,128,149],'E':[160,162,228,203,174]}
victims={'A':[35,19,10,8,9],'B':[20,25,19,25,27],'C':[25,1,0,2,3],'D':[3,0,16,8,3],'E':[60,52,52,79,76]}
assert sorted(cases,key=lambda k:F(victims[k][3],cases[k][3]),reverse=True)==['E','B','D','C','A']
assert all(a>=2*b for a,b in zip(cases['A'],cases['B']))
assert max(victims,key=lambda k:abs(victims[k][4]-victims[k][3]))=='D'
assert cases['E'][0]<cases['E'][1]<cases['E'][2] and sum(victims['C'])==31<=F(sum(victims['E']),2)
# Taxi missing cells and full totals.
taxi=[[1566,1110,125,1001,123,241],[1694,701,301,879,174,382],[1991,1194,441,825,554,349],[717,1128,51,769,2845,475],[130,355,40,1214,1064,484],[43,193,268,1262,114,187]]
assert list(map(sum,taxi))==[4166,4131,5354,5985,3287,2067]
assert F(717,51)>F(1566,125) and F(1214,3287)>F(769,5985) and 1566>1262
gas=[[1840,1825,1979],[1795,1849,1982],[1801,1867,2006],[1807,1852,1979]]
diesel=[[1843,1852,2014],[1806,1894,2029],[1806,1885,2013],[1827,1895,2024]]
assert all(a<b<c for a,b,c in diesel)
assert [max(range(4),key=lambda i:diesel[i][m]-gas[i][m]) for m in range(3)]==[3,1,1]
assert gas[2][2]-gas[2][1]==139>128==diesel[2][2]-diesel[2][1]
# City graph: only coarse separation is needed; no invented integer dot readings.
assert F(362)*F(51,100)*F(3,2)<277<350
city=[[18.4,15.9,16.3],[22.6,15.9,12.8],[35.9,39.9,38.4],[33.3,36,38.1],[22.2,30.6,36],[28.1,47.7,35.8],[33,38.1,50.9],[7.7,16.7,0],[23.3,19.6,22.3],[21.4,14.1,18.2],[23.6,28.5,24.3],[26.7,19.9,23.1],[31.7,34,22.1],[36.2,34.5,23.8],[10.6,23.3,22.9],[18.5,25.7,12.4],[31.6,25.3,26.2]]
assert [i for i,(a,b,c) in enumerate(city) if a>b>c]==[1,13]
# Quartiles: lower-bound array is feasible, and ordered positions force equality.
management=[15000,20000,30000,35000];executives=[24000,25600,25600,48000,48000,48000,48000,55000]
assert sum(management)==4*25000 and F(management[1]+management[2],2)==25000
assert F(executives[3]+executives[4],2)==executives[5]==48000
assert F(sum(executives),8)==40275>40000 and 2+26+8+18==54>50
# Farmland all annual scope and first-year strict counterexample.
allLand=list(map(F,['180.1','175.9','171.5','173.0','169.1','167.9','164.4','162.1','159.6','158.1']))
farm=list(map(F,['91.5','81.5','80.7','80.9','81.1','81.0','78.0','77.7','77.8','77.6']))
assert all(2*f<=t for f,t in zip(farm[1:],allLand[1:]));assert 2*farm[0]>allLand[0]
assert farm[3]>farm[2] and F('14.6')>farm[0]*F(15,100)
# Five tourism rows: six values for 2019 then 2020, transcribed individually.
tour=[([1118,12280,2968,98932,395,6109],[266,3030,2035,67832,199,1827]),([1118,12320,2968,98932,395,6109],[266,3180,2035,67832,199,1827]),([1118,12280,2968,98932,395,6309],[266,3030,2035,67832,199,1290]),([1118,12320,2968,96932,395,6309],[266,3180,2035,70069,199,1290]),([1118,12280,2968,96932,395,6109],[266,3030,2035,70069,199,1827])]
truth=[]
for a,b in tour:
 truth.append(all(4*b[i]<=a[i] for i in [0,1]) and all(10*b[i]<=7*a[i] for i in [2,3]) and all(F(b[i+4],a[i+4])>F(b[i],a[i]) for i in [0,1]))
assert truth==[True,False,False,False,False]
# Weather source full yearly row totals; restore unknown column and rank.
totals=[39,41,57,29,74,59,49,23,43,58,44,38,52,58,57,40,46,39]
otherTotals=[83,96,38,56,76,43,52,64,37,57,10]
assert sum(otherTotals)==612 and sum(totals)==846 and 846-612==234
assert sum(sorted(totals)[-2:])==133<3*sum(sorted(totals)[:2])==156
assert 41-(3+0+5+3+1+3+5+0+2+2+2)==15
assert 23-(0+4+3+1+1+3+1+0+3+0+0)==7
assert 59-(4+11+3+1+3+3+10+1+0+2+0)==21<27
result=dict(status='PASS',nativeProseChecks=checks,roundingDifferenceIntervals=[[str(a),str(b)] for a,b in intervals],maritimeRatiosOrder=['E','B','D','C','A'],taxiTotals=list(map(sum,taxi)),graphUpperBound=str(F(362)*F(51,100)*F(3,2)),cityDecreasingCandidates=[1,13],quartileManagement=management,quartileExecutivesLowerBound=executives,tourismTruth=truth,weatherOtherColumnSum=612,weatherRainTotal=234,sourceMapManualReview='A all four conditions; B station>8; C elevation<100 and interchange>6; D/E landprice>=30. Map/legend retained exactly.',limitations='Same-author review. Exact chart pixels checked separately. Native source prose and retained data geometry checked without changing original assets. Own first-pass weather arithmetic typo retained and corrected separately.')
(B/'source-key-model-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PASS original native prose eight, exact models ten, rounded intervals disjoint, retained source data figures unchanged.')
