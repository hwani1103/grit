"""Exact arithmetic and bounded graph readings independently recomputed from source."""
from fractions import Fraction as F
from itertools import product
import review_remaining605 as r

b=r.folder(21); checks=[]
def save(qid, answer, **evidence):
    own=next(x for x in r.read(b/'own-solves.json') if x['id']==qid)
    assert own['answer']==answer
    checks.append(dict(id=qid,answer=answer,**evidence))
q=lambda year,n:f'kr-mpm-{year}-psat-d-{n:02}'
bonuses=[[12,6,3],[5,20,5],[6,3,6],[6,6,12],[F(9,2)]*3,[6,6,12]]
rates=[F(1,5),F(1,10),F(1,20)]
candidates=[sorted(set(row[0]/v for v in rates if all(z/(row[0]/v) in rates for z in row))) for row in bonuses]
models=[]
for base in product(*candidates):
    grades=[[bonuses[i][t]/base[i] for i in range(6)] for t in range(3)]
    if all([g.count(v) for v in rates]==[1,2,3] for g in grades):models.append(base)
assert len(models)==2 and {sum(m) for m in models}=={490}
save(q('2021-07-10',19),3,feasibleAnnualSalaries=[[str(v) for v in m] for m in models],total=490)
size=['LSMLML','SLMMSS','LMSMLS','MLLMLM','LSSLMS','LMSLML']
region=['443344','433334','422233','211112','223222','333444']
plants=list(zip(''.join(size),''.join(region)))
assert len(plants)==36
counts={s:sum(x==s for x,_ in plants) for s in 'LMS'}
assert counts=={'L':14,'M':12,'S':10}
tight=sum(s=='L' and reg in '12' for s,reg in plants)
ii=sum(s=='L' and reg=='2' for s,reg in plants)
truth=[tight==5,counts['L']>=F(3,2)*counts['S'],ii*500>=1000,36-counts['S']>=5*tight]
assert truth==[True,False,True,True]
save(q('2021-07-10',20),4,sizeRows=size,regionRows=region,counts=counts,truth=truth,regionIIL=ii)
initial=list(map(F,['.5','.5','.7','.8','2']))
neg=[3,0,2,3,3];wind=[30,45,35,30,40]
final=[max(F(1),v*F(3,2)*(F(7,5) if n>=3 else 1)*(F(4,5) if w>=40 else 1)) for v,n,w in zip(initial,neg,wind)]
delta=[x-y for x,y in zip(final,initial)]
assert sorted(range(5),key=lambda i:delta[i],reverse=True)==[4,3,0,1,2]
save(q('2021-07-10',23),5,final=list(map(str,final)),increase=list(map(str,delta)),comparison='D second, C smallest')
pass17=[26914,19335,7110,821,5521,10467,8597,6213]
pass18=[27009,19856,8067,1717,5904,11942,8890,7001]
case18=[153,106,23,44,57,98,85,72];change=[13,-2,-6,7,16,-35,34,9]
case17=[a-d for a,d in zip(case18,change)]
assert sum(case17)==602
shares=[round(100*x/602,1) for x in case17]
assert shares==[23.3,17.9,4.8,6.1,6.8,22.1,8.5,10.5]
types=[round(F(602)*F(p)/100) for p in ['57.14','22.76','5.32','6.81','.33','7.64']]
assert types==[344,137,32,41,2,46]
growth=[round(100*(a-d)/d,1) for d,a in zip(pass17[2:],pass18[2:])]
assert growth==[13.5,109.1,6.9,14.1,3.4,12.7]
perMillion=[[round(1000*c/p,1) for c,p in zip(case17[:2],pass17[:2])],[round(1000*c/p,1) for c,p in zip(case18[:2],pass18[:2])]]
assert perMillion==[[5.2,5.6],[5.7,5.3]]
lo=F(602)*F('57.135')/(F(479)*F('49.065'))
hi=F(602)*F('57.145')/(F(479)*F('49.055'))
assert lo>F('1.46') and hi<F('1.47')
save(q('2021-07-10',24),1,counts2017=case17,shares=shares,typeCounts=types,growth=growth,perMillion=perMillion,cancelRatioBounds=list(map(str,[lo,hi])),roundingCannotReach116=True)
fire=[277,197,296,492,623,391,692,496,653,620]
assert sum(fire)==4737 and F(305,692)>F(73,197)
hiker=620-sum([49,65,75,9,1,54,150]);trash=246-sum([32,45,17,6,1,33,52])
assert hiker==217 and F(hiker,620)==F(35,100) and F(trash,65)>F(45,49)
save(q('2021-07-10',25),5,truth=[True,True,False,True],fireTotal=sum(fire),hiker=hiker,trashArrests=trash)
assert 3231>=2*1487 and F(1126,1239)>F(837,1311) and 916<950<976
assert 1927>max(1744,1126,837,617,88,-79,-298,976-916,976-1128)
save(q('2025-11-15',1),2,istanbulIncreasingCounterexample=950,omittedUpperBound=976,maxGrowth=1927)
teachers=[446,189,337,143,257];students=[874,459,715,277,682]
debt=[756,2700,1637,1020,3469];cadavers=[188,114,142,159,304]
scores=[]
for t,s,d,c in zip(teachers,students,debt,cadavers):
    scores.append([3 if s<2*t else 2 if s<4*t else 1,3 if d<1000 else 2 if d<2000 else 1,1 if c<120 else 2 if c<200 else 3])
assert list(map(sum,scores))==[8,4,6,7,6]
save(q('2025-11-15',5),1,scoreRows=scores,sums=list(map(sum,scores)),boundaries='Student2->2pts;4->1pt;debt1000->2;2000->1;cadaver30->2;50->3')
ports=[['15.6','33.5','5.5','15.1','1.5','3.6'],['29.5','25.3','14.3','13.2','2.1','1.9'],['38.5','54.3','17.7','50.2','2.8','4.5'],['34.4','37.5','30.3','12.3','1.8','3.5'],['8.5','17.7','2.1','4.8','1.1','1.4']]
portTruth=[]
for vals in ports:
    a,z,oldTrans,y,c,x=map(F,vals);portTruth.append([z>a,x>=c*F(3,2),y/z>oldTrans/a,z/x*100>1000])
assert [all(v) for v in portTruth]==[False,False,True,False,False]
save(q('2025-11-15',7),3,conditions=portTruth,unitFactor=100)
assert F('.52')-F('.34')>F('.45')-F('.28')
# Conservative intervals read from original scatter axes, not exact claimed data.
cRatioUpper=F('8.5')/36
otherRatioLower=[F('7.5')/25,F('8.5')/28,F(11)/25,F('11.5')/35,F(11)/29,F('17.5')/28]
assert cRatioUpper<min(otherRatioLower)
save(q('2025-11-15',8),1,truth=[True,False,True,False],cGiniDifferenceLower='.18',bGiniDifferenceUpper='.17',cPovertyRatioUpper=str(cRatioUpper),otherPovertyRatioLower=list(map(str,otherRatioLower)),visualControls='G highest y in both; D left of A and above A. Approximate interval readings only.')
prices=[[4520,6620,9920],[5520,6930,9920],[4520,6930,9920],[4980,6930,9920],[4520,7620,10920]]
priceTruth=[[m<=5000,z<=10000,z-low<3000,2*m<z] for m,low,z in prices]
assert [all(v) for v in priceTruth]==[False,False,True,False,False]
save(q('2025-11-15',9),3,conditions=priceTruth,boundaries='3000 equality fails; half equality fails;5000/10000 equality permitted')
assert len(checks)==10
r.write(b/'source-key-model-checks.json',dict(status='PASS',count=10,models=checks,sourceKeysAndPixels='source-native-pixel-checks.json',limitation='Same-author source arithmetic; separate direct-key, native, fresh-pixel and host checks required.'))
print('PASS: ten exact or explicitly bounded source models.')
