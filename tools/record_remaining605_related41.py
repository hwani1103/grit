import review_remaining605 as r
b=r.folder(41)
rows=[(1,'2024년12월1일현재납세판정한다.ㄱ철거명령은다음2025년1월1일이므로기준일현재해당없어과세.ㄴ지자체공공용무료사용2023년1월부터라1년이상비과세.ㄷ임시건축물2024년4월19일건축이라기준일현재1년미만비과세이며이후사용예정기간은별개.ㄹ재해구조선박비과세는국가1년무료사용조건과별도호이므로10개월사용이어도비과세.따라서ㄱ만과세①.현행세법자문아닌제시규정기준독해이다.', ['ㄱ의철거명령은기준일뒤라과세하고나머지는각각별도비과세요건을충족한다.','ㄱ과세는맞지만ㄷ임시건축물은기준일현재건축1년미만이라비과세다.','ㄴ은지자체1년이상공공무료사용,ㄹ은재해구조선박으로각각비과세다.','ㄱ만과세이고ㄷ건축1년미만과ㄹ재해구조선박을과세에넣을수없다.','ㄴㄷㄹ은각각제시조항에따른비과세이고과세ㄱ을빠뜨렸다.']),
(4,'보조금은기본차량가액에화물만20%더하고경유는승용30또는그외50을더한다.甲160,乙240+30=270,丙250*1.2+50=350,丁280,戊300*1.2=360.내림차순戊360丙350丁280乙270甲160으로세번째丁④다.20%는경유추가금까지합한금액이아닌차량가액기준이고승합휘발유丁에는화물/경유가산없다.동률없어순위확정된다.', ['甲은160만원으로5위이며세번째금액280만원과다르다.','乙은승용경유예외30만원더해270만원으로4위다.','丙은화물가산50만원과경유50만원더해350만원으로2위다.','丁280만원은戊360丙350뒤이고乙270앞이므로3위다.','戊는300만원의20%가산으로360만원이며최고1위다.'])]
src=r.read(b/'related295-source.json');assert not (b/'related295-own-solves.json').exists()
r.write(b/'related295-own-solves.json',[dict(id=s['id'],answer=a,reasoning=x,optionReasons=o) for s,(a,x,o) in zip(src,rows)])
r.write(b/'related295-solve-frozen.json',dict(frozenAt=r.now(),sha256=r.sha(b/'related295-own-solves.json'),beforeKeyAndExplanationReveal=True))
bank=r.bank();r.write(b/'related295-before.json',[bank[s['id']] for s in src])
for s in src:
 q=bank[s['id']];print(q['id'],q['answer']);print(q['body']);print(q.get('tables'));print('\n'.join(q['steps']));print('\n'.join(q['optionReasons']))
