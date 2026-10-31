import itertools
from fractions import Fraction as F
import review_remaining605 as r
b=r.folder(39)
houses=[41979,31208,31466,22755,17244];private=[32472,27802,25726,19804,13057];households=[39492,30685,30225,19175,17365];owners=[23335,19740,17778,12298,10266];local=[26089,21092,20614,13106,10904];other=[6383,6710,5112,6698,2153]
assert sum(houses)==144652 and sum(private)==118861 and round(100*F(sum(private),sum(houses)),1)==F('82.2')
assert [round(100*F(a,c),1) for a,c in zip(owners,households)]==list(map(F,['59.1','64.3','58.8','64.1','59.1']))
assert [round(100*F(a,c),1) for a,c in zip(other,local)]==list(map(F,['24.5','31.8','24.8','51.1','19.7']))
# Enumerate all choices of5 direct-operated regions containing fixed D,F,H,
# and every possible report subject under all numeric and strict extrema.
parks=[154,107,53,44,27,21,14,13,11,3];bikes=[1700,1553,1600,458,424,267,568,130,514,493];rent=[964937,1580187,1227900,160133,213070,99606,47244,60117,62570,392633]
ops=[]
for extra in itertools.combinations([2,4,6,8,9],2):
 direct={3,5,7,*extra}
 for j in direct:
  rest=direct-{j}
  if F(rent[j],parks[j])>=5000 and F(rent[j],bikes[j])>=100 and all(bikes[j]>bikes[k] and parks[j]<parks[k] and F(rent[j],bikes[j])<F(rent[k],bikes[k]) for k in rest):ops.append(dict(direct=''.join(chr(65+k) for k in sorted(direct)),report=chr(65+j)))
assert ops==[dict(direct='DEFHI',report='I')]
# Manual transcription from original O/X grid, rows1..10, columns A..H.
fixed=[[1,1,0,1,0,1,1,1],[1,1,0,0,1,0,1,1],[0,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1],[0,1,0,1,1,1,1,1],[0,1,1,1,1,0,1,1],[1,1,0,1,0,1,0,0],[1,1,1,1,1,1,1,0],[0,1,0,1,1,0,0,0],[1,0,0,1,1,0,1,0]]
counts=[8,7,8,9,8,7,6,8,5,4];weight=[2]*5+[3]*5
scores=[sum(fixed[j][k]*weight[j] for j in range(10)) for k in range(8)];assert scores==[15,22,10,23,20,14,19,13]
assert sum(a*c for a,c in zip(counts,weight))==170
completions=[]
for assignments in itertools.product([0,1],repeat=4):
 unknown={2:assignments[0],3:assignments[1],5:assignments[2],7:assignments[3]};grid=[]
 for j,row in enumerate(fixed):
  if j in unknown:i=unknown[j];jj=1-i
  elif j in [0,1,4,6,8]:i=jj=1
  else:i=jj=0
  grid.append(row+[i,jj]);assert sum(grid[-1])==counts[j]
 total=[sum(grid[j][k]*weight[j] for j in range(10)) for k in range(10)]
 if len(set(total))<10:continue
 alltwo=[chr(65+k) for k in range(10) if all(grid[j][k] for j in range(5))]
 final=[total[k] for k in range(10) if grid[9][k]]
 assert max(total)-min(total)==13 and len(alltwo)==4 and F(sum(final),len(final))>total[6]
 completions.append(dict(scores=total,allTwoPointCorrect=alltwo,lastQuestionMean=str(F(sum(final),len(final)))))
assert len(completions)==2 and {tuple(x['scores'][8:]) for x in completions}=={(16,18),(18,16)}
# Weather figures as printed plus conservative +/-0.05 bounds on both
# displayed one-decimal deviation and one-decimal percentage.
def actual_bounds(delta,percent):
 d,p=F(delta),F(percent)/100;dd=F('0.05');dp=F('0.0005')
 return min((d+x)* (p+y)/(1-p-y) for x,y in itertools.product([-dd,dd],[-dp,dp])),max((d+x)*(p+y)/(1-p-y) for x,y in itertools.product([-dd,dd],[-dp,dp]))
jeju=actual_bounds('26.3','50.7');inland=actual_bounds('29.6','54.0');assert jeju[1]<28<34<inland[0]
assert F('57.5')/F('132.6')>F('0.4') and F('35.3')/F('1.026')>F('35.8')/F('1.252')
assert 36217*13262<10248*52116 and 120*5543>103*5340
assert [51004-48225,13173-13093,5543-5527]==[2779,80,16]
assert F(1850,5579)>F('0.33') and F('20')-F('14.7')==F('5.3') and F('8.6')-F('8.5')==F('0.1')
ap=[4,3,5,16,32];bp=[14,26,15,3,5];aa=[156,30,97,248,702];ba=[229,358,201,19,42]
assert [sum(ap),sum(bp),sum(aa),sum(ba)]==[60,63,1233,849] and sum(aa)>F('1.2')*sum(ba)
assert sorted(range(5),key=lambda j:F(aa[j],ap[j]),reverse=True)==[0,4,2,3,1]
assert min(range(5),key=lambda j:F(ba[j],bp[j]))==3 and F(1233,60)>=20>F(849,63)
incoming=[4,4,9,8,2,5,2,3,2,3];out=[2,5,4,1,4,3,4,2,8,0];stocks=[40]
for j in range(1,10):stocks.append(stocks[-1]+incoming[j]-out[j])
assert stocks==[40,39,44,51,49,51,49,50,44,47] and 17<3*6 and F(7,44)>F(5,39) and F(5,51)<F(4,40)
national=list(map(F,['265.4','293.6','293.5','285.5','344.1']));localtax=list(map(F,['80.4','84.3','90.5','102','112.8']));tot=[a+c for a,c in zip(national,localtax)]
assert all(a<c for a,c in zip(tot,tot[1:])) and tot[-1]==F('456.9') and national[-1]>F('1.2')*national[-2]
growth=[(localtax[j]-localtax[j-1])/localtax[j-1] for j in range(1,5)];assert growth.index(max(growth))==2 and localtax[-1]/tot[-1]<localtax[-2]/tot[-2]
assert all(c/t>=F('.2') for c,t in zip(localtax,tot)) and max(a-c for a,c in zip(national,localtax))==F('231.3')
r.write(b/'exact-model-checks.json',dict(status='PASS',housingPersonalShare='118861/144652 =82.2% rounded; D/E swapped inㄴ; all five incorrect ratios inㄹ independently recomputed.',bikeAssignments=ops,scoreGridTranscription=fixed,scoreCompletions=completions,weatherActualConservativeBounds=dict(jeju=list(map(str,jeju)),inland=list(map(str,inland))),traffic='Exact cross-products, bus minimum each road and full report premises verified.',finance='All16 correct2023 bars and all9 funding-series labels visually matched; false welfare28%vs33.2,health-2.7vs+5.3,culture-.5vs+.1.',admissions='Exact five ratios each, full sums and all five report statements.',military='Sources1,2,4,5 map report figures; source3 candidate-count composition cannot give exam-frequency counts.',prisonStocks=stocks,taxGrowth=list(map(str,growth)),taxShareFall=True))
r.write(b/'post-reveal-reasoning-correction.json',dict(id='kr-mpm-2026-03-07-psat-d-38',answerBefore=3,answerAfter=5,issue='Own count omitted H, whose first five cells are all O. Original own answer3 and reasoning remain frozen. App and official answer5 already correct.',source='Original page19 right O/X grid, H column rows1–5 allO; exhaustive16 assignments with two admissible completions recorded in exact-model-checks.json.',corrected='All two-point questions correct: B,G,H plus one ofI/J =4. ㄴㄷㄹ all true; answer5.',notAnAppDefect=True))
p=r.read(r.OUT/'progress.json');p.setdefault('postRevealReasoningCorrections',{})['kr-mpm-2026-03-07-psat-d-38']='batch39/post-reveal-reasoning-correction.json';r.write(r.OUT/'progress.json',p)
r.write(b/'source-check-config.json',dict(removeSourceBlocks={'kr-mpm-2025-03-08-psat-d-02':['A B C']},imageChoices=['kr-mpm-2025-03-08-psat-d-05','kr-mpm-2025-03-08-psat-d-06','kr-mpm-2025-03-08-psat-d-08'],postRevealAnswerCorrections={'kr-mpm-2026-03-07-psat-d-38':'post-reveal-reasoning-correction.json'}))
print('PASS individual exact models; own omittedH correction3→5 recorded, original solve retained.')
