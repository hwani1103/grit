import review_remaining605 as r
b=r.folder(52);src=r.read(b/'related295-source.json')
rows=[(5,'환급을A,10억원지불을B라하면(1)은A∨B다. (1)거짓가정에서드모르간으로¬A와¬B를얻는것이㉠이다. 추가조건은(1)거짓이면A여서A와¬A모순이고귀류법으로(1)참인㉡을얻는다. 참이면추가조건상¬A여서A∨B와¬A의선언지제거로B인㉢이다. 세원리모두정확해⑤이며현실계약효력판단이아니라주어진약속과고전논리분석이다.', ['ㄱ의선언거짓원리는맞지만ㄴㄷ도맞아빠졌다.','ㄷ의선언지제거는맞지만ㄱㄴ도포함해야한다.','ㄱㄴ뿐아니라참인선언에서거짓항을빼는ㄷ도맞다.','ㄴㄷ뿐아니라선언이거짓이면각항거짓인ㄱ도맞다.','드모르간과귀류법과선언지제거가각각㉠㉡㉢을정확히뒷받침한다.']),
(2,'뒤문장의이러한부동성문제를받으려면앞에는유선인터넷소통의장소제약이있어야한다. 시간비용보다는랜선연결된컴퓨터앞에서만가능이라는②가이동성스마트폰과맞는다. ①은새미디어파급력최대논지를뒤집고③은안도와타자착각설명에뜬금없는운동을추가한다. ④는사물인데타자로혼동한다는주장을실제타자라고바꾼다. ⑤는예속과위험을확장긍정으로뒤집어틀리다.', ['유선인터넷보다현재파급력이못하다는수정은첫문단최대파급력과모순이다.','랜선컴퓨터앞이라는장소제약이바로다음부동성문제의지시대상이다.','중독방지운동으로바꾸면연결안도에서타자착각으로가는흐름을끊는다.','스마트폰을실제타자로확정하면사물을타자로오인한다는비판과모순이다.','삶의확장이라는긍정은예속과도구지배를경고하는뒤문맥에어긋난다.'])]
assert not (b/'related295-own-solves.json').exists()
r.write(b/'related295-own-solves.json',[dict(id=s['id'],answer=a,reasoning=x,optionReasons=o) for s,(a,x,o) in zip(src,rows)])
r.write(b/'related295-solve-frozen.json',dict(frozenAt=r.now(),sha256=r.sha(b/'related295-own-solves.json'),beforeKeyAndExplanationReveal=True))
bank=r.bank();r.write(b/'related295-before.json',[bank[s['id']] for s in src])
for s in src:
 q=bank[s['id']];print(q['id'],q['answer']);print(q.get('underlines'));print('\n'.join(q['steps']));print('\n'.join(q['optionReasons']))
