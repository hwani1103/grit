import review_remaining605 as r
b=r.folder(51)
rows=[(1,'원표1은양육자성별/양육자연령이고보고서의자녀연령은별도분류다. 자녀0~2/3~6/7~9세의스트레스36.3/35.1/34.5와고위험58.3/52.4/50.7순위에는ㄱ이필요하다. 소득200미만40.5점최고및고위험86.6가다른구간최대57.5보다29.1%p높다는진술에는ㄴ이필요하다. 경제활동ㄷ과자녀수ㄹ은보고서에없다. 나머지정신건강은원표2로확인되므로ㄱㄴ①.', ['원표에없는자녀연령별과소득구간별결과ㄱㄴ을더하면보고서근거가충족된다.','자녀연령ㄱ은필요하나경제활동ㄷ은불필요하고소득ㄴ이빠졌다.','경제활동과자녀수는보고서에없어둘다추가자료가아니다.','ㄱㄴ은필요하지만보고서에없는자녀수ㄹ까지추가할필요는없다.','소득ㄴ은필요하나ㄷㄹ은불필요하며자녀연령ㄱ을누락했다.']),
(3,'ㄱ의두계열부주의340/391/411/322/426/342와조석114/100/105/83/90/72는전연도일치한다. ㄴ음주비중은13.0/14.2/11.0/14.8/11.0/12.5%로원표를나눠반올림하면모두일치한다. ㄷ2021원인별18/426/21/13/79/90/70을717로나누면2.5/59.4/2.9/1.8/11.0/12.6/9.8로전부맞다. ㄹ조석2020(83−105)/105=−21.0%,2021=8.4%,2022=−20.0%로그림−21.7/32.3/−37.1과다르다. 안전2022도−53.8%인데−19.7이라거짓,ㄱㄴㄷ③.', ['ㄱㄴ은맞지만2021원인구성비ㄷ도맞아누락됐다.','ㄱㄷ은맞지만6개연도음주비중ㄴ도모두맞다.','건수ㄱ/비중ㄴ/구성비ㄷ은모두일치하고증가율ㄹ만틀린다.','ㄹ은조석3개연도및안전2022증가율이원표와어긋난다.','ㄴㄷ은맞지만ㄹ이틀리고원표와맞는ㄱ도빠졌다.'])]
src=r.read(b/'related295-source.json');assert not (b/'related295-own-solves.json').exists()
r.write(b/'related295-own-solves.json',[dict(id=s['id'],answer=a,reasoning=x,optionReasons=o) for s,(a,x,o) in zip(src,rows)])
r.write(b/'related295-solve-frozen.json',dict(frozenAt=r.now(),sha256=r.sha(b/'related295-own-solves.json'),beforeKeyAndExplanationReveal=True))
bank=r.bank();r.write(b/'related295-before.json',[bank[s['id']] for s in src])
for s in src:
 q=bank[s['id']];print(q['id'],q['answer']);print(q['body']);print(q.get('bodyAfterFigureCount'));print('\n'.join(q['steps']));print('\n'.join(q['optionReasons']))
