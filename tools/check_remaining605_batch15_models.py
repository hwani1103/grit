"""Exact arithmetic and source-text checks, separate from authored answers."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D,ROUND_HALF_UP
import hashlib,json,re,unicodedata
import pdfplumber
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/psat_remaining605_20261030';B=OUT/'batch15'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
write=lambda p,v:p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
old={x['question']['id']:x['question'] for x in read(B/'revealed-current.json')}
bank={q['id']:q for p in (ROOT/'assets/psat').glob('*.json') for q in (read(p) if isinstance(read(p),list) else [])}
reg={x['newAsset']:x for x in read(ROOT/'artifacts/psat_final_quality_20261029/full900/native-image-repairs.json')['figures']}
spec=read(B/'native-prose-transcriptions.json')['transcriptions'];prose=[]
norm=lambda s:re.sub(r'[\s<>○◯]','',unicodedata.normalize('NFKC',s))
for qid,s in spec.items():
 previous=old[qid];q=bank[qid];source=[]
 for i in s['remove']:
  m=reg[previous['figures'][i]['asset']]
  with pdfplumber.open(ROOT/m['source']) as pdf:source.append(pdf.pages[m['page1based']-1].crop(m['rect']).extract_text() or '')
 assert norm('\n'.join(source))==norm(q['body']),(qid,norm('\n'.join(source)),norm(q['body']))
 assert q['figures']==[f for i,f in enumerate(previous['figures']) if i not in s['remove']]
 assert all(q.get(k)==previous.get(k) for k in ['answer','choices','original','choiceNote','prompt','id','number'])
 assert all((ROOT/f['asset']).is_file() for f in previous['figures'])
 assert q['revision']==previous['revision']+1
 if q.get('underlines'):
  assert len(q['underlines'])==5 and q['underlineLabelAnchors']
  assert all(q['body'].count(u)==1 for u in q['underlines'])
  assert q['underlines'][2].endswith('이상이며,')
  assert '현재 활동 중인' not in q['underlines'][2]
 prose.append(dict(id=qid,pdfTextEqualsNativeBodyIgnoringLayout=True,retainedDataFiguresExactlyEqual=True,answerChoicesOriginalAndExistingConditionUnchanged=True,oldAssetsRetained=True,proseBeforeData=bool(s.get('afterBody'))))
assert hashlib.sha256((B/'ratings-before.json').read_bytes()).hexdigest()==read(B/'ratings-frozen.json')['ratingsSha256']
assert hashlib.sha256((B/'own-solves.json').read_bytes()).hexdigest()==read(B/'solve-frozen-before-reveal.json')['solveFileSha256']

# d18: correct visual column order: space/ad/billboard/decoration/other.
sleep=[2014,2096,1490,1107,885];life=[217,294,388,354,502];glare=[177,167,264,333,390];anxiety=[5,20,26,50,57];totals=[2413,2577,2168,1844,1834]
space=[1792,1768,1176,829,827];ad=[353,464,626,560,522];bill=[53,82,41,44,90];decor=[75,55,107,120,101];other=[140,208,218,291,294]
assert [sum(x) for x in zip(sleep,life,glare,anxiety)]==totals==[sum(x) for x in zip(space,ad,bill,decor,other)]
minimum=max(0,space[3]+sleep[3]-totals[3]);assert minimum==92
assert [92+737,1015]==[space[3],totals[3]-space[3]] and 92+1015==sleep[3]
assert decor[2]>decor[1] and bill[2]<bill[1]
assert sleep[1]<F(totals[1])*F('.85') and F(97,167)>F(57,333)
assert decor[0]>bill[0] and bill[1]>decor[1]

# d19: unknown March/April values only constrained by their sum.
avg=F(3461,12);known={1:273,2:229,5:282,6:280,7:287,8:285,9:307,10:300,11:312,12:320}
assert sum(known.values())+586==3461 and 288<avg<289
assert 2222-1650-287==285<287 and F(320-273,273)>F('.15')
assert [m for m,v in known.items() if v>avg]==[9,10,11,12] and F(586,2)>avg
assert sum(v>avg for v in list(known.values())+[293,293])==6
assert sum(v>avg for v in list(known.values())+[280,306])==5

# d20: exact and conservative bounds including rounded share intervals.
sharesB=list(map(F,['8.5','10.1','12.6','14.4','16.5','18.5']))
assert all(b-a>=1 for a,b in zip(sharesB,sharesB[1:]))
assert 1129-135-80-260==654<3*260
assert all(F(p,p+e)>=F('.6') for p,e in [(139,70),(160,88),(135,80)])
c21=902*F('33.4')/F('26.1');c22=1079*F('30.5')/F('24.8')
assert c21<F('1172.6')<F('1294.8')<c22
assert 902*F('33.45')/F('26.05')<1079*F('30.45')/F('24.85')

# d21: totals, group differences and independent consistency equations.
present=302589+160897;absent=59184;applications=present+absent
assert present==444870+18616==463486 and applications==522670
oldAbsent=326646-287502;studentDelta=38188-oldAbsent;otherDelta=20996-(177942-157368)
assert oldAbsent==39144 and studentDelta==-956 and otherDelta==422
assert studentDelta+otherDelta==-534 and applications-504588==18082

# d22/23: signed original reading and prior explicit app interpretation separated.
aFrozen=[5500,5600,5300,5400,5600];bFrozen=[12200,13500,11500,11400,12800]
assert aFrozen[3]>aFrozen[2] and bFrozen[3]<bFrozen[2]
aRate=[F(6200-7700,7700),F(13500-16500,16500)]
bRate=[F(12300-11700,11700),F(26300-26700,26700)]
assert aRate.index(max(aRate))==1 and bRate.index(max(bRate))==0
assert list(map(abs,aRate)).index(max(map(abs,aRate)))==0==list(map(abs,bRate)).index(max(map(abs,bRate)))
aLast=13000*5-sum([11600,11600,12100]);bLast=14000*5-sum([15200,15700,13600])
assert aLast==29700>bLast==25500
differences=[14100-6700,26400-14300,6100-2300];assert differences==[7400,12100,3800]
quantities=[(4,4,2),(3,5,2),(5,3,2),(5,2,3),(5,1,4)]
savings=[sum(a*b for a,b in zip(q,differences)) for q in quantities]
assert all(sum(q)==10 for q in quantities) and savings==[85600,90300,80900,72600,64300]
assert sorted(range(5),key=lambda i:savings[i],reverse=True)==[1,0,2,3,4]

# d24: decimal half-up per-component rounding, not binary/banker's rounding.
raw=[[511,4104,1000],[767,431,850],[153,248,835],[138,167,760],[45,22,770],[14,117,760],[47,430,725],[56,143,710],[62,105,700],[73,85,680]]
def transformed(row,weights):return [(D(v)*D(w)/D(m)).quantize(D('.1'),rounding=ROUND_HALF_UP) for v,w,m in zip(row,weights,[767,4104,1000])]
scores=[sum(transformed(row,[10,20,70])) for row in raw]
assert scores==list(map(D,['96.7','71.6','61.7','55.8','54.6','54.0','53.5','51.1','50.3','49.0']))
assert 70>=2*(10+20) and sum(transformed([112,105,700],[10,20,70]))==D('51.0')<scores[7]
assert sum(transformed(raw[4],[20,10,70]))==D('55.2')>sum(transformed(raw[5],[20,10,70]))==D('53.9')

# d25: no tied ranks and four groups cover the universe.
high=list(range(1,11));upper=[11,33,37,38,41,50,52,54,55,56];lower=[39,44,53,60,64,66,67,73,81,83];low=[104,110,117,121,127,128,129,130,131,132]
assert sum([51,34,38,10])==133 and set(range(2,11))<=set(high)
assert len(set(range(41,51))-set(upper)-set(lower)-set(low))==7
assert len(set(range(111,134))-set(low))==15
assert sum(r<53 for r in upper+lower)+1==10

# 2021 d01: datum year/class mismatches cannot be repaired by guessing.
assert 25+7==32 and 5+2==7 and 32+7+434==473
traffic=[4380,4019,3973,3529];deaths=[31582,30944,29545,31111]
assert all(b<a for a,b in zip(traffic,traffic[1:])) and round(F(444,3973)*100,1)==F('11.2')
assert deaths[0]>deaths[1]>deaths[2]<deaths[3]

# 2021 d02: month intervals and original report's false statement preserved.
missions=[('Burundi',200304,200406,3128),('Sudan',200410,200712,300),('ComorosElection',200603,200606,462),('Somalia',200701,202105,6000),('ComorosSecurity',200705,200810,350),('Darfur',200707,202105,6000),('Uganda',201203,202105,3350),('Mali',201212,201307,1450),('CentralAfrica',201312,201409,5961)]
assert sum(x[3] for x in missions)==27001 and sum(x[3] for x in missions if x[2]==202105)==15350
assert [x[0] for x in missions if x[1]<=200710<=x[2]]==['Sudan','Somalia','ComorosSecurity','Darfur']
duration=lambda x:(x[2]//100-x[1]//100)*12+x[2]%100-x[1]%100
assert max(missions,key=duration)[0]=='Somalia' and min(missions,key=duration)[0]=='ComorosElection'
q=bank['kr-mpm-2021-07-10-psat-d-02'];assert '5개였다.' in q['body'] and '4개' in q['steps'][1]

write(B/'source-key-model-checks.json',dict(status='PASS',count=10,exactArithmeticAndBoundaryChecks=True,proseChecks=prose,rawSourceSignedAnswer22=2,existingAppConditionAnswer22=5,prespecifiedAlternativeBeforeReveal=True,ownHeaderMisreading18CorrectedSeparately=True,limitations='Same-author transcribed models; no independent reviewer. Original signed reading differs from existing explicit app condition. No device/APK.'))
print('PASS: 10 arithmetic/logic models, 8 exact PDF prose transcriptions, 5 underline ranges, immutable solves/ratings and existing condition.')
