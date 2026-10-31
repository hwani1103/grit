from fractions import Fraction as F
import review_remaining605 as r
b=r.folder(57)
rows=[(4,'제조비중증가최대A가채소이고모든6분야폐기량이늘어난D가어육이다. 2021소비4행합은A546.6,B204.1,C425,D302.7로최소B가과일이고남은C곡류다. ㄱ어육302.7>300참,ㄴ2016유통채소29.5>과일22.2로동일일수연간도참. ㄷ가정B40.7→33.8감소반례,ㄹ채소숙박113→97.3감소참. ㄱㄴㄹ④. 연간비교는동일연도라일수를곱해도순위보존된다.', ['ㄱ은맞지만채소유통연간더많은ㄴ과숙박감소ㄹ도참이다.','ㄹ은맞지만가정과일류가감소하여모두증가ㄷ은틀리다.','ㄱㄴ맞지만가정B감소반례로ㄷ은거짓이며ㄹ이빠졌다.','어육302.7톤/채소유통더많음/채소숙박감소가모두성립한다.','ㄴㄹ맞지만가정B감소로ㄷ거짓이고참인ㄱ도빠졌다.']),
(5,'심야운행96/100=.96이다른네종류운행비율보다높아ㄱ참. 광역예비/노선18/10=1.8이고지선196/223의2배392/223약1.758보다높아2배이하ㄴ거짓. 상위4개는201이상구간4개이다. 나머지61개구간하한합5×1+8×41+28×81+10×121+10×161=5421,전체7393에서남기는상위4최대1972라평균493이하이다. 500이하ㄷ참이며ㄱㄷ⑤. 최고구간에상한없어도전체합과하위하한이상한을만든다.', ['심야비중최대ㄱ맞지만상위4평균최대493인ㄷ도참이라누락이다.','광역1.8은지선196/223의2배보다커이하라는ㄴ틀리다.','ㄷ은맞지만심야운행비중96%최대인ㄱ도참이어서빠졌다.','ㄱ맞지만18×223=4014가2×196×10=3920보다커ㄴ거짓이다.','ㄱ의96%최대와ㄷ의평균상한493이모두맞고ㄴ만거짓이다.'])]
src=r.read(b/'related295-source.json');assert not (b/'related295-own-solves.json').exists()
r.write(b/'related295-own-solves.json',[dict(id=s['id'],answer=a,reasoning=x,optionReasons=o) for s,(a,x,o) in zip(src,rows)])
r.write(b/'related295-solve-frozen.json',dict(frozenAt=r.now(),sha256=r.sha(b/'related295-own-solves.json'),beforeCurrentKeyAndExplanationReveal=True,historicalExposure='Prior reviews existed; same author, not blind or independent.'))
lower=5+8*41+28*81+10*121+10*161;assert lower==5421 and F(7393-lower,4)==493
old=[F('12.7'),F('5.6'),F('24.3'),F('4.6')];new=[F('16.9'),F('5.1'),F('10.9'),F('5.8')]
assert max(range(4),key=lambda i:new[i]/F('44.7')-old[i]/F('54.7'))==0
assert max(range(4),key=lambda i:new[i]/sum(new)-old[i]/sum(old))==0
r.write(b/'related295-pre-reveal-models.json',dict(status='PASS',lower61=lower,topFourMax=1972,topFourAverageMax=493,manufacturingShareMax='A with full or nonother denominator',consumerTotals=['546.6','204.1','425.0','302.7']))
bank=r.bank();r.write(b/'related295-before.json',[bank[s['id']] for s in src])
for s in src:
 q=bank[s['id']];print(q['id'],q['answer']);print('\n'.join(q['steps']));print('\n'.join(q['optionReasons']));print('figures',q.get('figures'))
