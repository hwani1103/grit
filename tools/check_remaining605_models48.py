from fractions import Fraction as F
from itertools import permutations
import review_remaining605 as r
b=r.folder(48);out={};Q=lambda x:F(str(x));rnd=lambda x:(x+F(1,2)).numerator//(x+F(1,2)).denominator
payments=[sum(c*n for c,n in zip(comp,[1,2,3,4]))*50 for comp in [[40,20,20,20]]*2+[[35,25,20,20]]]
assert payments==[11000,11000,11250] and sum(payments)==33250 and sum(payments)-1750==31500
large=[t-sum(c*n*50 for c,n in zip(comp,[1,2,3])) for t,comp in zip([11200,11200,11450],[[40,20,20],[40,20,20],[35,25,20]])]
assert large==[4200]*3 and F(sum(large),3000)*10==42
out['2025d40']=dict(cappedPersonEquivalents=payments,totalTenThousandWon=332500,modifiedTenThousandWon=315000,largeMembers=large,largeHouseholdMeanPeople='4.2',truth=[True]*3,optionCombinations=['ㄱ','ㄷ','ㄱㄴ','ㄴㄷ','ㄱㄴㄷ'])
ages=[[4.2,6.4],[5.4,9.5],[7.2,11.4],[7.4,11.7],[6.2,9.4],[6.1,9],[5,8.2]];growth=[Q(y)/Q(x)-1 for x,y in ages]
homes=[[6.3,10],[6.3,9],[5.7,9.7],[4.4,6.4]];hg=[Q(y)/Q(x)-1 for x,y in homes]
assert sorted(range(7),key=lambda i:growth[i],reverse=True)[:2]==[1,6]
assert sorted(range(4),key=lambda i:hg[i],reverse=True)==[2,0,3,1]
assert Q(9.7)/Q(6.2)>Q(1.5) and Q(3.5)/Q(5.7)>Q(3.5)/Q(6.8)
out['2024d01']=dict(ageGrowth=list(map(str,growth)),homeGrowth=list(map(str,hg)),needed=['channel','receiptMethod'],notNeeded='city/rural')
offline=[[1547,1904,2056],[431,674,827],[43,58,108]];online=[[45,150,504],[10,44,185],[0,10,54]]
ot=[sum(x) for x in zip(*offline)];nt=[sum(x) for x in zip(*online)];assert ot==[2021,2636,2991] and nt==[55,204,743]
assert all(F(nt[j+1]-nt[j],nt[j])>F(ot[j+1]-ot[j],ot[j]) for j in range(2))
assert all(x<y for row in offline+online for x,y in zip(row,row[1:])) and 1104>1048
out['2024d03']=dict(offline=ot,online=nt,mediumCity=[809,1104,1048],counterexample='2022->2023 decline',onlineShares=[[46,27,27],[32,46,22],[30,43,27]])
noise=[[7.2,6.9,8,6.6,3.6,3.3,4.1,3],[6.8,7.3,6.5,8.1,2.5,3,3.1,3.6],[8.3,7.9,7.8,7.6,4.4,4.1,3.5,3.4],[6.5,6.8,6.7,6.5,3.2,3.5,3.2,3.3],[7.7,8,7.9,7.9,3.7,4,3.9,3.6]]
checks=[]
for row in noise:
 a,b0,c,d,e,f,g,h=map(Q,row);checks.append([a-e==b0-f,(e-f)*(g-h)>0,a>=2*e and b0>=2*f,c>a and b0>d])
assert [all(x) for x in checks]==[True,False,False,False,False]
out['2024d04']=dict(fourConditionsByAtoE=checks,sourceTerms='저소음/고소음, 주의력/공간지각력 점수; not disorder incidence')
sales=[[127540,128435,132634,128913,128048],[138313,132807,131728,120954,119370],[129583,124145,132160,126701,116864],[83774,84170,85303,85266,79024],[20937,28876,24699,24393,21786],[95392,89461,90937,107322,112410]]
assert [sum(x) for x in zip(*sales)]==[595539,587894,597461,593549,577502]
assert sum(row[0]*5>=595539 for row in sales)==3
decrease=[F(row[1]-row[3],row[1]) for row in sales];assert decrease.index(max(decrease))==4
assert sum(row[2]>row[0] for row in sales)==4 and sum(row[4]>row[2] for row in sales)==1 and 2*(307+22534+17482)>79024
out['2024d05']=dict(truth=[True,True,False,False],decrease=list(map(str,decrease)),options=['ㄱㄴ','ㄱㄹ','ㄴㄷ','ㄷㄹ','ㄱㄴㄹ'])
claims=[1046,1231,1419,1493,1785,3097,2951,3484,4006,5708];full=[446,550,572,522,529,837,1004,1296,1497,2355];transfer=[44,46,77,104,207,511,379,161,170,188]
ratio=[F(a,b0) for a,b0 in zip(full,claims)];assert ratio.index(min(ratio))==transfer.index(max(transfer))==5 and all(x>F(29,100) for j,x in enumerate(ratio) if j!=5) and ratio[5]<F(28,100)
assert claims[6]<claims[5] and 215+134<claims[4]/5 and 2355+5495-5708==2142>=2100
out['2024d06']=dict(fullRatios=list(map(str,ratio)),intersection=[2142,2355],truth=[False,True,False,True])
total=[9315,10020,10397,10811,10147];individual=[6352,6739,7410,7458,7175];group=[2963,3281,2987,3353,2972]
assert [a+b0 for a,b0 in zip(individual,group)]==total
expense=[18760,18710,20953,19060,19392];assert [rnd(F(a*100,b0)) for a,b0 in zip(expense,total)]==[201,187,202,176,191]
assert [rnd(F(a*100,b0)) for a,b0 in zip([2774,2585,2284,2317,1682],individual)]==[44,38,31,31,23]
assert [rnd(F(a*100,b0)) for a,b0 in zip([106,161,82,72,86],group)]==[4,5,3,2,3]
assert [rnd(F(a*100,b0)) for a,b0 in zip([99,64,58,56,31],[125,114,104,80,50])]==[79,56,56,70,62]
shares=[F((t-high)*100,t) for t,high in zip(total,[1648,1777,1597,2367,1965])];assert list(map(rnd,shares))==[82,82,85,78,81]
out['2024d07']=dict(threeOrFewerShares=list(map(str,shares)),graphShares=[82,80,83,85,81],truth=[True,True,True,True,False])
assert 16675-16403==272 and 2020-1892==128 and 16549-16216==333 and 3333-3264==69
assert 1027-1001==26 and 1027-969==58 and rnd(F(39,973)*100)==4 and rnd(F(66,946)*100)==7 and 917-892==25 and 110-109==1
out['2024d08']=dict(required=['ㄱ','ㄷ','ㄹ'],uniqueInformation=['firmSize','leavers','entrantType'],duplicateTotalEntrants=['ㄷ','ㄹ'],unneeded='industry')
assert 2000*F(1,2)==1000 and 400/F(1000)==F(2,5) and F(1,2)+2*F(2,5)==F(13,10)
assert 4000*F(15,100)==600 and 4000/F(8,10)==5000 and F(8,10)+2*F(15,100)==F(11,10)
assert F(15,10)-2*F(1,2)==F(1,2) and 6000*F(1,2)*F(1,2)==1500<4*400
out['2024d10']=dict(sales=[1000,4000,3000],profits=[400,600,1500],assets=[2000,5000,6000],scores=['1.3','1.1','1.5'])
# Icon intervals are read from the original legend, including long crack at 라.
zone=[False,True,True,True,True,False,False,True,True];vacancy=[3,14,6,14,3,11,21,8,6];ageIntervals=[(0,10),(10,20),(20,30),(30,None),(0,10),(20,30),(20,30),(10,20),(30,None)];life=[20,20,40,30,40,40,30,30,20]
demolish=[];reuse=[]
for j,(general,v,age,l) in enumerate(zip(zone,vacancy,ageIntervals,life)):
 lower,upper=age;usable=general and v<=20 and upper is not None and upper<=l
 demolition=general and (v>20 or lower>=l)
 assert not(usable and demolition)
 if usable:reuse.append('가나다라마바사아자'[j])
 if demolition:demolish.append('가나다라마바사아자'[j])
assert reuse==['나','다','마','아'] and demolish==['라','자'];out['2024d15']=dict(reuse=reuse,demolition=demolish,bothForbidden=['가','바','사'],equalityIncluded=True)
# Prior295 independent recalculations, all24 bijections.
totals=list(map(Q,[51.7,64,17.3,10.8]));pop=list(map(Q,[9.7,2.9,2.4,1.5]));cap=[a/b0 for a,b0 in zip(totals,pop)];res=list(map(Q,[14,4.5,3.5,2]));build=list(map(Q,[31,9,7,4.8]));worlds=[]
for ga,eul,byeong,jeong in permutations(range(4)):
 if totals[ga]>=50 and cap[ga]==min(cap) and abs(cap[eul]-cap[byeong])<=1 and res[byeong]/totals[byeong]>res[jeong]/totals[jeong] and build[eul]==min(build):worlds.append([ga,eul,byeong,jeong])
assert worlds==[[0,3,2,1]];out['related02']=dict(worlds=worlds,perCapita=list(map(str,cap)))
registered=[461733,600648,820329,1159087,1589985];assert all(10*y>=13*x for x,y in zip(registered,registered[1:]))
regBegin=[399464,5620,55756,893];regEnd=[1157940,12567,389855,29623];gains=[y-x for x,y in zip(regBegin,regEnd)];regGrowth=[F(y-x,x) for x,y in zip(regBegin,regEnd)]
assert gains.index(max(gains))==0 and regGrowth.index(max(regGrowth))==3
exports=[[138216,150474,124503,211807,284598],[18395,31399,26065,37957,45140],[38523,76008,119718,154014,223623],[227,788,1041,1119,361]];et=[sum(x) for x in zip(*exports)];assert et==[195361,258669,271327,404897,553722] and all(x<y for x,y in zip(et,et[1:]))
assert [all(x<y for x,y in zip(row,row[1:])) for row in exports]==[False,False,True,False]
sets=[set('일본 독일 벨기에 터키 영국 한국 슬로바키아 캐나다 프랑스 스웨덴'.split()),set('독일 일본 스웨덴 미국 한국 영국 중국 슬로바키아 스페인 벨기에'.split()),set('미국 벨기에 독일 한국 오스트리아 프랑스 영국 네덜란드 중국 일본'.split())]
assert set.intersection(*sets)==set('한국 일본 독일 벨기에 영국'.split());out['related11']=dict(exportTotals=et,registrationGrowth=list(map(str,regGrowth)),intersection=sorted(set.intersection(*sets)),truth=[True,True,True,False,True])
r.write(b/'exact-model-checks.json',dict(status='PASS',checks=out))
corrections=[dict(id='kr-mpm-2025-03-08-psat-d-40',issue='Own optionReasons②/③ transposed combination labels: actual②ㄷ and③ㄱㄴ. All three propositions and answer⑤ unchanged.',correctedOptionReasons={'2':'ㄷ은참이나ㄱㄴ도참이라누락이다.','3':'ㄱㄴ은참이나ㄷ도참이라누락이다.'}),dict(id='kr-mpm-2024-03-02-psat-d-01',issue='Own ancillary age/house labels drifted; source ages start10대이하, not20대. Highest post count40대11.7;lowest10대이하6.4;growth maximum20대 then70대. Housing오피스텔>아파트>기타>주택. Needed자료ㄱㄴandanswer② unchanged.',correctedSourceMapping='Original page1 and exact-model-checks.json ageGrowth/homeGrowth.'),dict(id='kr-mpm-2024-03-02-psat-d-04',issue='Own prose called 주의력/공간지각력 scores disorders and low/high noise just low/high. Original is ability scores in noise environments. Numerical inequalities, four-condition validation and answer① unchanged.',correctedTerms='저소음/고소음;주의력점수/공간지각력점수'),dict(id='kr-mpm-2024-03-02-psat-d-05',issue='Own optionReason⑤ describedㄱㄴㄷ; actual⑤ㄱㄴㄹ. All4truthvalues and answer① unchanged.',correctedOptionReason='ㄱㄴ은참이나ㄹ은D의40323>39512반례로거짓이다.')]
assert r.sha(b/'own-solves.json')==r.read(b/'solve-frozen-before-reveal.json')['solveFileSha256']
if not (b/'post-reveal-reasoning-corrections.json').exists():r.write(b/'post-reveal-reasoning-corrections.json',dict(beforeAnswersPreserved=True,publishedAnswersAndReasoningAlreadyCorrect=True,corrections=corrections,originalOwnFileUnmodified=True,evidence='Original pages were reread and calculations rechecked, not scores inferred from answer equality.'))
p=r.read(r.OUT/'progress.json')
for x in corrections:p['postRevealReasoningCorrections'][x['id']]='batch48/post-reveal-reasoning-corrections.json'
r.write(r.OUT/'progress.json',p)
print('PASS 10 target +2 related exact models;4 own-record corrections preserved separately')
