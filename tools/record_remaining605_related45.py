import review_remaining605 as r
b=r.folder(45)
rows=[(3,'성별감염수차이는감염총수×성별구성비차이다.A3047×.36=1096.92,B2415×.50=1207.5,C5554×.10=555.4,D3621×.14=506.94로D최소여서③맞다.①A24~36개월은약850으로D36~48개월약815보다커틀림.②C48개월감염률44.4<24~36개월49.3으로틀림.④36~48개월은C약1194가B약725보다커틀림.⑤D연령별최저는12~24개월4.0%로48개월이상4.8%보다작다.반올림±.05%p로도성별차D최소순위유지.', ['A해당감염수약850은D약815보다많으므로적다는설명이틀렸다.','C의48개월이상감염률44.4는24~36개월49.3보다낮다.','성별감염수차A1096.92,B1207.5,C555.4,D506.94로D가최소다.','36~48개월감염수는C가약1194로B약725보다많다.','D감염개체중12~24개월비중4.0이48개월이상4.8보다작다.']),
(5,'E는남3.3,4.1,6.4,7.2와여4.6,5.5,8.4,9.7모두증가한다.성별차는1시간1.3,3시간2.0으로비율20/13이1.5이상2미만이다.남성증분.8,2.3,.8보다여성.9,2.9,1.3이각각크고4시간/2시간남7.2/4.1,여9.7/5.5모두1.3이상이다.A는여성증분이작고B는차이비1.7/.3>2,C는여성이2→3시간감소,D는차이비4.0/2.8<1.5이므로나머지모두탈락해⑤.', ['A는남성증분.8,1.3,2.9가여성.7,.6,2.4보다커셋째조건불충족이다.','B성별차의3시간/1시간비율1.7/.3은2이상으로둘째조건위반이다.','C여성발병률이2시간5.8에서3시간5.3으로감소하여첫조건위반이다.','D성별차4.0/2.8은약1.429로둘째조건하한1.5미만이다.','E는전구간증가와차이비/증분우위/4시간대2시간1.3배네조건모두충족한다.'])]
src=r.read(b/'related295-source.json');assert not (b/'related295-own-solves.json').exists()
r.write(b/'related295-own-solves.json',[dict(id=s['id'],answer=a,reasoning=x,optionReasons=o) for s,(a,x,o) in zip(src,rows)])
r.write(b/'related295-solve-frozen.json',dict(frozenAt=r.now(),sha256=r.sha(b/'related295-own-solves.json'),beforeKeyAndExplanationReveal=True))
bank=r.bank();r.write(b/'related295-before.json',[bank[s['id']] for s in src])
for s in src:
 q=bank[s['id']];print(q['id'],q['answer']);print(q['body']);print('\n'.join(q['steps']));print('\n'.join(q['optionReasons']))
