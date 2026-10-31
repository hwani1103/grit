import review_remaining605 as r
b=r.folder(43)
rows=[(1,'A의정당화↔심각피해+내부보고무조치+증거+피해방지충분이유이다.B는소속부서업무+심각잘못믿음+증거+미폭로시계속가담믿음이다.ㄱ심각피해없는데정당사례는A필요조건에반례여서약화참.ㄴ증거없어서부정당은B필요조건미충족시부정당이라는예측일치라약화아님.ㄷ내부보고안했는데정당사례는A둘째필요조건위반이라A강화아니며둘다강화연언은즉시거짓.B도가담회피대안있다는내용이지만믿음판정세부를추가가정할필요없다.ㄱ①.', ['심각피해없는정당사례는A의정당→심각피해필요조건을깨므로ㄱ맞다.','ㄷ은내부에보고하지않은정당사례로A를강화할수없어둘다강화거짓이다.','ㄱ은맞지만ㄴ은증거없음에정당불인정이라B의예측에맞아약화아니다.','ㄴ은예측일치이고ㄷ은A조건위반이어서둘다적절하지않다.','ㄱ만맞고ㄴ과ㄷ의약화/강화평가가성립하지않는다.']),
(1,'A는이유반응적행위가가능하고그러한행위라면자유라고하지모든행위가이유반응적이라고하지않는다.을의칩강제절도는실제행위지만이유모름이라는명시반례라알수없는①이다.②최면정은이유없는불결믿음③결정된행위도갑처럼자유/책임가능④B는믿음자체비난불가⑤B는인식적증거가주어지면믿음선택불가가각직접본문근거다.행위가결정되었다는사실과자유불가를동치로두지않고믿음과그로인한행위책임을분리한다.', ['A의일부가능을모든행위필연으로강화했으며을의무이유절도가반례다.','정은믿음이유없이최면에걸린것도모른다고하여이유제시못함을알수있다.','결정론아래에서도갑의이유반응적절도에는도덕적책임을물을수있다는예시다.','B는믿음에서생긴행위와달리믿음자체도덕평가는터무니없다고한다.','B는인식적이유가있으면무엇을믿을지선택할수없다고명시한다.'])]
src=r.read(b/'related295-source.json');assert not (b/'related295-own-solves.json').exists()
r.write(b/'related295-own-solves.json',[dict(id=s['id'],answer=a,reasoning=x,optionReasons=o) for s,(a,x,o) in zip(src,rows)])
r.write(b/'related295-solve-frozen.json',dict(frozenAt=r.now(),sha256=r.sha(b/'related295-own-solves.json'),beforeKeyAndExplanationReveal=True))
bank=r.bank();r.write(b/'related295-before.json',[bank[s['id']] for s in src])
for s in src:
 q=bank[s['id']];print(q['id'],q['answer']);print(q['body']);print('\n'.join(q['steps']));print('\n'.join(q['optionReasons']))
