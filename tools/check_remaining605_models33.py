from fractions import Fraction as F
import review_remaining605 as r
out=[]
def add(n,**kw):out.append(dict(id=f'kr-mpm-2026-03-07-psat-d-{n:02}',**kw))
assert F('23.2')<59 and F('76.8')>3*F('23.2') and F('75.6')>3*F('24.4')
lo=F('75.6')+44-100;assert lo==F('19.6') and lo>=19
add(2,truth=[False,True,True],intersectionBounds=['19.6','44'],boundaryWitness={'youngFemale':'19.6','youngMale':'24.4','oldFemale':'56','oldMale':'0'},independenceNotAssumed=True)
founding=[1,169,952,1151,903,839,271,318,693,996];closed=[0,68,496,517,504,623,384,355,343,394]
assert founding[1:4]==[169,952,1151] and all(founding[i]>founding[i+1] for i in [3,4,5]) and all(founding[i]<founding[i+1] for i in [6,7,8])
assert closed[1]==68 and closed[5]==623 and closed[5]>closed[6]>closed[7]>closed[8]<closed[9]==394
assert abs(F(608,2609)*100-F('23.3'))<F(1,20)
add(4,choiceUsed=[False,True,True,True,True],sourceReportMapping=['서울 내부 권역은 없음; 서울 평균영업일과 다른 지표','세계194→263/국내2000→3000','경기608/2609≈23.3%','창업169/952/1151/996','폐업68/623/394'],founding=founding,closures=closed,notAllReportSentencesDerivableFromChoices=True)
travel23=[F('95.5'),296977,465391,37816];travel24=[F('95.4'),291825,448498,36800]
assert all(a>b for a,b in zip(travel23,travel24)) and travel24[1]*1000>290000000 and travel24[2]*1000>440000000 and travel24[3]>36000
stays=[4716,3976,2738,1978,658];assert stays==sorted(stays,reverse=True)
times23=list(map(F,['19.5','65.2','9.1','6.2']));times24=list(map(F,['19.4','64.6','7.9','8.1']))
rank=lambda xs:sorted(range(len(xs)),key=lambda i:xs[i],reverse=True)
assert rank(times23)==[1,0,2,3] and rank(times24)==[1,0,3,2]
assert F('60.1')>F('58.3') and rank(list(map(F,['60.1','29.2','8.6','2.1'])))==[0,1,2,3]
regions=list(map(F,['21.1','11.8','10.1','9.3','9.2','8.9']));assert rank(regions)==list(range(6))
add(5,choiceMatches=[True,True,False,True,True],timeRanks2023=rank(times23),timeRanks2024=rank(times24),lodging2024=stays)
exp23=list(map(F,['36.1','29.8','12.5','4.9','4.0','1.9','1.9','8.9']));exp24=list(map(F,['28.8','20.8','9.6','18.5','1.3','2.8','2.2','16.0']));exp25=list(map(F,['28.3','23.8','9.8','22.7','5.0','2.7','2.6','5.1']))
assert all(sum(x)==100 for x in [exp23,exp24,exp25])
increasing=[i for i,(a,b,c) in enumerate(zip(exp23,exp24,exp25)) if a<b<c];dif=[c-a for a,c in zip(exp23,exp25)]
assert increasing==[3,6] and [i for i,d in enumerate(dif[:-1]) if d>dif[4]]==[3]
army=[[F(v) for v in row] for row in [['28.4','23.9','10.0','22.8','4.5','2.6','2.3','5.5'],['28.2','24.6','9.0','22.8','5.3','2.7','3.1','4.3'],['27.8','22.9','9.1','27.0','4.5','2.1','2.0','4.6'],['28.7','23.5','10.9','17.6','6.6','3.6','3.5','5.6']]]
assert all(sum(a)==100 for a in army) and [rank(a)[:2] for a in army]==[[0,1],[0,1],[0,3],[0,1]]
add(7,blanks=['세탁',1,'공군'],increments=list(map(str,dif)),allYearIncreaseIndices=increasing)
# Columns: 신규,승진,재등록,재공개,퇴직,의무면제,정기변동.
people=[[15,18,1,0,23,1,0],[21,23,0,0,38,3,2],[17,24,2,2,59,1,1718],[37,21,2,4,35,5,0],[24,9,4,1,41,8,0],[21,10,0,3,148,1,2],[17,9,0,1,60,1,0],[15,7,0,0,27,0,6],[622,14,1,1,566,4,0],[25,19,0,0,19,4,0],[20,16,2,0,28,2,2],[18,11,0,0,20,0,0]]
total=list(map(sum,people));assert total==[58,87,1823,104,87,185,88,55,1208,67,70,49]
top=[i+1 for i in rank(total)[:5]];assert top==[3,9,6,4,7]
regular=[i+1 for i,p in enumerate(people) if p[6]];counter=[i for i in regular if total[i-1]<total[i-2]];assert counter==[8]
quarter=[sum(p[j] for p in people[9:]) for j in range(7)];assert quarter==[63,46,2,0,67,6,2] and sum(quarter)==186
assert F(25,19)>F(13,10)>F(11,10)>F(622,566)
add(8,truth=[True,False,True,False],topFiveMonths=top,regularMonths=regular,counterexampleMonths=counter,quarterTotals=quarter,crossProducts=[25*566,622*19])
tasks=[[115,148,146],[24,27,30],[88,107,122],[50,54,47],[31,40,45]];money=[[82197,77496,58344],[87039,88380,104201],[56793,67523,70960],[11623,12219,19786],[685,874,888]]
growth=[F(m[1]-m[0],m[0]) for m in money];assert growth.index(max(growth))==4
inc=[i for i,t in enumerate(tasks) if t[0]<t[1]<t[2]];assert inc==[1,2,4]
unit=[[F(m[j],t[j]) for j in [1,2]] for m,t in zip(money,tasks)];assert [i for i,u in enumerate(unit) if u[1]>u[0]]==[1,3] and F(88380*30,27)==98200
add(13,mapping={'A':'주거','B':'교육','C':'복지·문화','D':'참여·권리'},budgetGrowth=list(map(str,growth)),unitBudget=[[str(x) for x in u] for u in unit])
production=[[174,55,104,78],[166,52,75,74],[148,75,101,73],[154,103,106,78],[151,137,125,76],[127,98,99,92],[156,89,111,95],[144,68,130,91],[150,51,141,92],[146,37,155,91]]
selfs=[['101','23','32.1','4.1'],['104.7','24.6','24.6','3.7'],['103.4','26','22','3.3'],['97.3','32.1','25.3','3.3'],['92.1','47.7','29.2','3.5'],['92.9','38.2','30.4','3.6'],['84.6','33.3','23.7','4.1'],['104.8','29.8','28.6','4.3'],['99.1','25.4','35.7','4.5'],['100.2','24.9','35.7','4.6']]
consumption=[[F(p*100)/F(s) for p,s in zip(ps,ss)] for ps,ss in zip(production,selfs)]
assert all(rank(x)[0]==3 for x in consumption) and all(x[3]>1400 and max(x[:3])<1000 for x in consumption)
assert consumption[-1][0]<consumption[-2][0] and F(137,489)>F(1,4) and F(selfs[2][0])>100 and production[2][1]>=70 and F(selfs[6][2])<F(selfs[5][2]) and selfs[8][2]==selfs[9][2]
add(14,truth=[True,False,False,False,False],consumptionExact=[[str(x) for x in row] for row in consumption],publishedSafeBounds={'corn':'>1400','others':'<1000'},barley2019Total=sum(production[4]))
exports=[1277,769,1969,373];imports=[1968,694,1832,217];population=list(map(F,['310.4','126.5','1318.2','143']));percap=list(map(F,['41.6','31.6','7.7','16.6']));gdp=[p*c for p,c in zip(population,percap)];trade=[e+i for e,i in zip(exports,imports)];balance=[e-i for e,i in zip(exports,imports)];op=[t/g for t,g in zip(trade,gdp)]
assert exports[2]>=F(3,2)*exports[0] and op[1]>F(3,10)>op[3] and rank(trade)[0]==2 and F(balance[3])/gdp[3]>F(balance[2])/gdp[2] and op[0]>F(1,5)
assert gdp[0]<311*42 and trade[0]>F(311*42,5) and gdp[1]<127*32 and gdp[3]>140*16
add(16,truth=[True,True,True,True,False],gdp=list(map(str,gdp)),trade=trade,openness=list(map(str,op)),balance=balance)
matrix=[[0,0,0,0,0,0,0,0],[1,2,0,0,0,0,0,0],[8,45,2,0,0,0,4,0],[0,26,1,3,0,0,1,0],[2,5,0,0,0,0,0,0],[0,6,3,0,0,1,0,0],[1,41,6,2,0,0,7,0],[1,4,0,0,0,0,0,0]]
rs=list(map(sum,matrix));cs=[sum(row[j] for row in matrix) for j in range(8)];diag=sum(matrix[i][i] for i in range(8));union=rs[2]+cs[2]-matrix[2][2]
assert sum(rs)==sum(cs)==172 and rs==[0,3,59,31,7,10,57,5] and cs==[13,129,12,5,0,1,12,0] and diag==15 and union==69
assert cs[1]>=4*rs[3] and diag<F(172,10) and matrix[5][6]==matrix[6][5]==0 and union<70
add(17,truth=[True,False,True,False],completedMatrix=matrix,rowSums=rs,columnSums=cs,diagonal=diag,architectureUnion=union)
gender=F(28-17,38-28);region=F(36,22);remaining=F(32,36)
assert gender==F(11,10)<F(3,2) and region>=F(3,2) and 1-remaining>F(8,100)
add(18,truth=[False,True,True],maleToFemale=str(gender),regionMeanRatio=str(region),fixedTotalCountRatio=str(remaining),decline=str(1-remaining))
r.write(r.folder(33)/'exact-model-checks.json',dict(status='PASS',checks=out,limitations='Same-author exact arithmetic and original transcription, not independent review.'))
print('PASS10 original-based numerical and all-option models.')
