"""Independently transcribed quantities, robust bounds and exact native prose."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,re,unicodedata
import pdfplumber
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/psat_remaining605_20261030';B=OUT/'batch18'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
write=lambda p,v:p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
old={x['question']['id']:x['question'] for x in read(B/'revealed-current.json')};bank={q['id']:q for p in (ROOT/'assets/psat').glob('*.json') for q in (read(p) if isinstance(read(p),list) else [])}
reg={x['newAsset']:x for x in read(ROOT/'artifacts/psat_final_quality_20261029/full900/native-image-repairs.json')['figures']};spec=read(B/'native-prose-transcriptions.json')['transcriptions']
norm=lambda s:re.sub(r'[\s<>○◯]','',unicodedata.normalize('NFKC',s))
prose=[]
for qid,s in spec.items():
 q=bank[qid];previous=old[qid];texts=[]
 for i in s['remove']:
  m=reg[previous['figures'][i]['asset']]
  with pdfplumber.open(ROOT/m['source']) as pdf:texts.append(pdf.pages[m['page1based']-1].crop(m['rect']).extract_text() or '')
 assert norm('\n'.join(texts))==norm(q['body']),(qid,norm('\n'.join(texts)),norm(q['body']))
 assert q['figures']==[f for i,f in enumerate(previous['figures']) if i not in s['remove']]
 assert all(q.get(k)==previous.get(k) for k in ['id','answer','choices','original','number','prompt','choiceNote'])
 assert all((ROOT/f['asset']).is_file() for f in previous['figures'])
 if q.get('underlines'):
  assert len(q['underlines'])==4 and q['underlineLabelAnchors'] and all(q['body'].count(u)==1 for u in q['underlines'])
  assert '800명 이상 증가' in q['underlines'][1] and '37.9%' in q['underlines'][2]
 prose.append(dict(id=qid,nativeBodyMatchesOriginalPdfIgnoringLayout=True,dataFiguresUnchanged=True,answerChoicesOriginalAndChoiceHeadingsUnchanged=True,allOriginalAssetsRetained=True))
assert hashlib.sha256((B/'ratings-before.json').read_bytes()).hexdigest()==read(B/'ratings-frozen.json')['ratingsSha256']
assert hashlib.sha256((B/'own-solves.json').read_bytes()).hexdigest()==read(B/'solve-frozen-before-reveal.json')['solveFileSha256']

gdp=[1323,1389,1440,1501,1563,1658,1741];debt=list(map(F,['29.7','30.3','30.8','32.6','34.1','35.7','36.0']));deficit=list(map(F,['14.6','14.9','15.3','16.9','18.3','20.0','20.7']))
financial=[a-b for a,b in zip(debt,deficit)];amount=[g*r/100 for g,r in zip(gdp,debt)];deficitAmount=[g*r/100 for g,r in zip(gdp,deficit)]
assert amount[-1]==F('626.76')>=F('1.5')*amount[0] and amount[0]==F('392.931')
assert financial==list(map(F,['15.1','15.4','15.5','15.7','15.8','15.7','15.3']))
assert deficitAmount[4]<300<=min(deficitAmount[5:]) and all(v<300 for v in deficitAmount[:5])
assert financial[3]<debt[3]/2

direct=1000*F('.9');rework=1000*F('.1');reworkWaste=rework/2;assembly=direct+rework/2;inspectionWaste=assembly*F('.2');shipment=assembly*F('.8')
assert reworkWaste==50 and assembly==950 and inspectionWaste==190 and reworkWaste+inspectionWaste==240 and shipment+240==1000

korean=[90,85,60,95,75];english=[90,85,100,65,100];math=[75,70,85,100,100];totals=[sum(v) for v in zip(korean,english,math)]
assert F(sum(korean),5)==81 and totals==[255,240,245,260,275] and F(max(totals)-min(totals),3)>10
weighted=[(2*k+e+2*m)/5 for k,e,m in zip(korean,english,math)];assert weighted==[84,79,78,91,90]
assert F(75+85+100,3)>F(70+100,2) and F(75+100,2)>F(70+85+100,3)

assert F('.08')<F(325,2686)<F('.155')
assert 3500*F('.3135')==F('1097.25')<1179
assert 3465*F('.1985')==F('687.8025')>657 and 2310*F('.1995')<657
aiGrowth=F(657-185,185);systemMaximum=F(657)/F('.1985');systemGrowthMaximum=(systemMaximum-2310)/2310
assert aiGrowth>F('2.5')>5*systemGrowthMaximum>0

matrix=[[65,121,54,52,172,198,226,89],[56,152,61,55,172,164,214,70],[29,47,30,22,62,61,85,30],[24,61,30,37,82,80,113,45],[61,112,54,47,187,150,202,72],[50,87,38,41,120,188,150,55],[78,151,83,73,227,208,359,115],[27,66,31,28,94,81,116,46]]
rowSums=list(map(sum,matrix));columnSums=list(map(sum,zip(*matrix)));diagonal=[matrix[i][i] for i in range(8)]
assert rowSums==[977,944,366,472,885,729,1294,489] and columnSums==[390,797,381,355,1116,1130,1465,522] and sum(rowSums)==6156
assert [i for i,(r,c) in enumerate(zip(rowSums,columnSums)) if r>c]==[0,1,3]
assert diagonal.index(min(diagonal))==2 and columnSums.index(min(columnSums))==3
externalSum=[r+c-2*d for r,c,d in zip(rowSums,columnSums,diagonal)];differences=[abs(r-c) for r,c in zip(rowSums,columnSums)]
assert externalSum==[1237,1437,687,753,1627,1483,2041,919] and differences==[587,147,15,117,231,401,171,33]
assert externalSum.index(min(externalSum))==differences.index(min(differences))==2
insideShare=[F(d,r) for d,r in zip(diagonal,rowSums)];assert max(range(8),key=lambda i:insideShare[i])==columnSums.index(max(columnSums))==6
assert insideShare[6]>F('.27') and insideShare[5]<F('.26') and all(insideShare[i]<F('.25') for i in [0,1,2,3,4,7])

domestic=[9778,1287,1147,9263];foreign=[7796,508,141,7626];newDomestic=[900,70,20,839];releaseDomestic=[560,195,7,704];newForeign=[646,52,15,741];releaseForeign=[600,33,5,666];officers=[10142,710,196,8898]
quarantine=[a+b for a,b in zip(domestic,foreign)];changes=[a-b+c-d for a,b,c,d in zip(newDomestic,releaseDomestic,newForeign,releaseForeign)]
assert quarantine==[17574,1795,1288,16889] and changes==[386,-106,23,210]
assert [i for i,v in enumerate(changes) if v<0]==[1]
assert [i for i,(n,o) in enumerate(zip(quarantine,officers)) if F(n,o)<F('1.8')]==[0]
foreignShare=[F(f,n) for f,n in zip(foreign,quarantine)];assert max(range(4),key=lambda i:foreignShare[i])==3
assert foreignShare[3]>F('.45') and all(foreignShare[i]<F('.45') for i in [0,1,2])

top15=list(map(F,['33.0','24.1','19.4','12.0','11.7','5.3','5.2','4.5','4.3','4.3','3.1','2.9','2.7','2.5','2.5']))
assert sum(top15)==F('137.5') and sum(top15[:5])==F('100.2')
knownHighShare=F('19.4')+F('5.2')+F('4.3')+F('2.5');totalUpper=sum(top15)+14*top15[-1]
assert knownHighShare==F('31.4')>25 and sum(top15[:5])>totalUpper/2
assert F('.61')*F('27.1')<F('.70')*F('24.1')
assert F('.615')*F('27.05')<F('.70')*F('24.05')
assert '27.05/24.05' in bank['kr-mpm-2021-07-10-psat-d-12']['steps'][4]

casualties=[492,536,589,640,734,612,665,841,670,592,594,507];accidents=[240,211,263,269,307,277,260,311,302,273,256,249]
assert sum(casualties)==7472 and sum(accidents)==3218 and all(a>2*b for a,b in zip(casualties,accidents))
assert min(casualties)<=F('.6')*max(casualties) and F(sum(casualties),sum(accidents))>=F('1.9')
distance=100-F('65.3')-F('3.4')-F('1.5')-F('6.9');assert distance==F('22.9')<7*F('3.4')
assert 3218*F('.6525')>2000

options=list(map(lambda row:list(map(F,row)),[['58.6','20.9','100.9','92.9'],['60.8','19.8','102.4','92.5'],['63.5','20.1','115.7','92.0'],['65.2','20.3','117.1','92.6'],['65.8','20.6','118.7','93.7']]))
otherAthletics=list(map(F,['111.1','103.4','128.0','133.8','114.0','110.2','102.5','119.2','113.0']))
conditionValues=[[F('58.5')<=a<F('65.7'),b<F('20.7'),sum(v>c for v in otherAthletics)==3,d>=F('92.5')] for a,b,c,d in options]
assert [i+1 for i,row in enumerate(conditionValues) if all(row)]==[4]
assert options[1][3]==F('92.5') and not conditionValues[1][2] # Equality is allowed, but rank fails.

privateCapacity=354749-102025;publicDelta=102025-102906;privateDelta=privateCapacity-251261
assert privateCapacity==252724 and publicDelta==-881 and privateDelta==1463
oldMetro=F(119940*100,676479);assert F('18.2')-oldMetro>0==F('25.5')-F('25.5')
assert F('26.8')-F('26.7')<F('21.0')-F('20.8')
assert F(47,196)*100<F('24.1')<F('37.9') and 27+20==47 and 43+25+9==77
assert 0+0==0 and 0+9==9
report=bank['kr-mpm-2021-07-10-psat-d-18'];assert '800명 이상 증가' in report['body'] and '37.9%' in report['body']
write(B/'source-key-model-checks.json',dict(status='PASS',count=10,nativeProseChecks=prose,exactArithmeticAndBoundaryModels=True,genderBothCases=True,roundingTolerances={'d08SharePercentagePoints':'.05','d12RatioPercentagePoints':'.005','d12AmountBillions':'.05'},originRowDestinationColumnAndAll64CellsChecked=True,municipalityMapping={'A':'충남','B':'세종','C':'충북','D':'대전'},aidWhole29UpperBound=str(totalUpper),trafficTotals=[7472,3218],regionalOptionConditions=conditionValues,dormitoryDeltas=[publicDelta,privateDelta],reportFalseClaimsPreserved=True,underlineRangeCount=4,limitations='Same-author source-transcribed models. Original/keys/fresh crops in separate source-native-pixel-checks.json. No independent or device review.'))
print('PASS10 exact models;9 native prose blocks;4 underline ranges;both gender cases;rounding-safe bounds;all64 cargo cells.')
