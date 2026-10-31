from fractions import Fraction as F
import review_remaining605 as r
b=r.folder(54)
room=[]
for n in range(1,9):
 opts=[168000+max(n-5,0)*15000+17000*n]
 if n<=4:opts += [91000+max(n-2,0)*15000+17000*n,120000+max(n-2,0)*32000,360000+17000*n]
 room.append(min(opts))
dp=[0]+[10**9]*8
for n in range(1,9):dp[n]=min(dp[n-j]+room[j-1] for j in range(1,n+1))
assert dp[8]==349000 and 2*(120000+2*32000)==368000
human=[F(a,t) for a,t in zip([206,533,198,252,317],[523,1574,2755,5668,5890])]
growth=[F(y-x,x) for x,y in zip([1574,2896,5268,7541],[2896,5268,7541,9942])]
recogn=[F(a,t) for a,t in zip([57,93,105,98,121],[523,1574,2755,5668,5890])]
staff=[F(a,t) for a,t in zip([1574,2896,5268,7541,9942],[20,20,30,40,50])]
assert human[-1]>human[-2] and min(growth)==growth[-1] and min(recogn)==recogn[-2] and all(x<y for x,y in zip(staff,staff[1:]))
rows=[(4,'금요일단풍3명은기본패키지116000에초과1명숙박15000와관광15000을더해146000원이라ㄱ맞다. 나루8명소담4명씩2객실패키지는각184000합368000이지만버금1객실168000+초과3명45000+관광8명136000=349000으로더싸ㄴ거짓. 모든객실별가능인원과객실조합을동적계획으로검산해최저349000. 일요일소담회원2명70000+동굴16000=86000으로ㄷ맞아④.', ['ㄱ은맞지만일요일70000+16000인ㄷ도맞아빠졌다.','패키지368000보다버금8명349000이저렴하므로ㄴ틀리다.','ㄷ은맞지만패키지초과비용30000을더한ㄱ도맞다.','ㄱ146000과ㄷ86000이맞고ㄴ의최저비용주장은반례가있다.','ㄱㄷ은참이나ㄴ은최저가349000으로368000주장틀리다.']),
(1,'인도적체류비중은2019의252/5668약4.45%에서2020의317/5890약5.38%로증가하여매년감소라는①이틀리다. 신규신청증가율84.0/81.9/43.1/31.8%는2020최저. 인정률10.90/5.91/3.81/1.73/2.05%는2019최저. 신청과철회모두2020최대이고인력당신청78.7/144.8/175.6/188.525/198.84로모든연도증가. 전구간을분수로검산하여①확정.', ['2019약4.45%에서2020약5.38%로증가하는반례가있어옳지않다.','증가율은2017부터약84.0,81.9,43.1,31.8%로2020최저맞다.','98/5668이최소라2019인정률이가장낮다는설명은맞다.','신규9942명과철회1117명모두2020에가장많다.','인력당신청78.7,144.8,175.6,188.525,198.84로매년증가맞다.'])]
src=r.read(b/'related295-source.json');assert not (b/'related295-own-solves.json').exists()
r.write(b/'related295-own-solves.json',[dict(id=s['id'],answer=a,reasoning=x,optionReasons=o) for s,(a,x,o) in zip(src,rows)])
r.write(b/'related295-solve-frozen.json',dict(frozenAt=r.now(),sha256=r.sha(b/'related295-own-solves.json'),beforeKeyAndExplanationReveal=True))
r.write(b/'related295-pre-reveal-models.json',dict(status='PASS',roomCostByOccupancy=room,allRoomCombinationsMinimumByPeople=dp,humanitarianRatio=list(map(str,human)),applicantGrowth=list(map(str,growth)),recognitionRatio=list(map(str,recogn)),applicantsPerStaff=list(map(str,staff)),sourceReadingNote='Initial unrecorded draft used Mon-Thu room column. Original source image inspection corrected Friday column to91000/168000 before freeze/reveal; answer4 unchanged.'))
bank=r.bank();r.write(b/'related295-before.json',[bank[s['id']] for s in src])
for s in src:
 q=bank[s['id']];print(q['id'],q['answer']);print(q['body']);print('underlines',q.get('underlines'));print('\n'.join(q['steps']));print('\n'.join(q['optionReasons']))
