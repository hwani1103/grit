import review_remaining605 as r
b=r.folder(55)
rows=[(3,'㉠은미래세대가다른구성원이되므로현세대책임을물을수없다는B결론을A가받아들이기어렵다는판단이다. ㄱ은구성원차이에도행복총량차이가있어총량을보는A를약화시키지않는다. ㄴ은미존재만으로도덕고려배제불합리라면B를비판하는A를오히려지지하므로약화라는판정거짓. ㄷ은직관이옳은지별도평가필요라하여A가일반직관을근거로B를거부하는연결을약화한다. ㄱㄷ③.', ['ㄱ은적절하지만직관권위의검토필요가약화한다는ㄷ도맞아빠졌다.','미래세대배제불합리는B비판A를지지하므로약화라는ㄴ틀리다.','총량변화가A를약화하지않는ㄱ과직관근거재평가로약화되는ㄷ이맞다.','ㄷ은맞지만ㄴ은A의B비판을지지하는방향이어서틀리다.','ㄱㄷ은맞으나ㄴ이강화방향을약화로뒤집어추가될수없다.']),
(5,'도의회는지방자치단체자체가아니라그기관이므로독립재난관리책임기관이아니다. 그러나재난중에도지속할핵심기능유무를해당자치단체장이판단하여관련계획필요여부를정한다. A도지사판단으로결정된다는⑤이다. 국회와의유사성으로사무처장에준용하지말라고명시했고자체수립이나의장책임을추론할수없다. 재난상황에대비한사전계획을발생후신속수립으로바꾼①도시점이다르다. 본문가상법관계만적용한다.', ['재난대비사전수립을재난발생하면신속수립으로바꾸어시점이맞지않는다.','핵심기능이있다고독자확정할수없고판단권자는도지사이며자체수립도아니다.','도의회자체는재난관리책임기관이아니라고직접명시되어전제가틀리다.','도의회도의결기관이지만국회에준하지말라는것이며계획불필요로확정못한다.','도의회의핵심기능지속필요성판단권한이도지사에게있어계획필요여부가따른다.'])]
src=r.read(b/'related295-source.json');assert not (b/'related295-own-solves.json').exists()
r.write(b/'related295-own-solves.json',[dict(id=s['id'],answer=a,reasoning=x,optionReasons=o) for s,(a,x,o) in zip(src,rows)])
r.write(b/'related295-solve-frozen.json',dict(frozenAt=r.now(),sha256=r.sha(b/'related295-own-solves.json'),beforeCurrentKeyAndExplanationReveal=True,historicalExposure='Earlier reviews existed; not independent/blind claim.'))
bank=r.bank();r.write(b/'related295-before.json',[bank[s['id']] for s in src])
for s in src:
 q=bank[s['id']];print(q['id'],q['answer']);print(q['body']);print('underlines',q.get('underlines'),q.get('underlineLabelAnchors'));print('\n'.join(q['steps']));print('\n'.join(q['optionReasons']))
