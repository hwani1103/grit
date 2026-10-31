import review_remaining605 as r
b=r.folder(50)
rows=[(5,'戊우후는甲과戊가여자이며戊>甲이라는뜻이다. 乙은戊나이를모르므로戊>乙이고乙=甲+1세이다. 丙이乙이히라고하므로丙乙남자이며乙>丙이다. 丁이戊이후라고하여丁남자,모두丁나이를알므로丁이가장어리다. 결국戊가최연장이고乙이그다음이다. 女甲戊2명/男乙丙丁3명이며丁이丙에게는이히다. 戊50乙40甲39丙30丁20반례에서①과③도안된다.⑤.', ['甲보다丙이연상이라는보장이없다. 戊50乙40甲39丙30丁20이면甲은丙에게호칭을안붙인다.','丁도丙도남자이므로연상丙에게붙이는말은이히이며이후가아니다.','나이간격상한은없어戊50丙30같은20살차반례도조건을만족한다.','甲戊가여자2명이고乙丙丁이남자3명으로여자가더적다.','戊>乙이고乙은甲丙보다연상이며丁은최연소이므로乙이두번째다.']),
(3,'군인S→용감B, B→자기희생A∨맹목L∨권위R이고B→¬L이다. 권위R을배제하면군인→자기희생A가되고A→명예H∨독선D에서독선D도배제하면S→H가된다. ③의B→¬R와A→¬D가두갈림길을제거한다. ①은권위적인비희생군인이남고②는독선군인이남고④는오히려자기희생자의명예를금지하며⑤는권위군인이남는다. 답3이전노출을명시하며새논리모형으로재확인한다.', ['군인권위참/자기희생거짓/명예거짓의반례가남아결론을보장못한다.','자기희생과독선참/명예거짓군인이전제와추가조건을모두충족가능하다.','맹목과권위를제외해자기희생,그뒤독선을제외해명예가필연이된다.','명예가없고자기희생과독선이있는군인반례를배제하지못한다.','권위적인군인이자기희생하지않으면명예가거짓이어도전제들이참이다.'])]
src=r.read(b/'related295-source.json');assert not (b/'related295-own-solves.json').exists()
r.write(b/'related295-own-solves.json',[dict(id=s['id'],answer=a,reasoning=x,optionReasons=o,answerExposureBeforeSolve=s['id'].endswith('l-16')) for s,(a,x,o) in zip(src,rows)])
r.write(b/'related295-solve-frozen.json',dict(frozenAt=r.now(),sha256=r.sha(b/'related295-own-solves.json'),beforeCurrentExplanationReveal=True,knownAnswerBeforeSolve=['kr-mpm-2026-07-18-psat-l-16']))
bank=r.bank();r.write(b/'related295-before.json',[bank[s['id']] for s in src])
for s in src:
 q=bank[s['id']];print(q['id'],q['answer']);print(q['body']);print(q.get('underlines'));print('\n'.join(q['steps']));print('\n'.join(q['optionReasons']))
