import itertools
import review_remaining605 as r
b=r.folder(58)
rows=[(5,'A는일반직관으로갑과을모두도덕적잘못이라하므로ㄱ참이다. 갑은이미임신한동일한태아의건강을약으로개선가능해대체논제를수용하든거부하든불필요한고통을준행위로평가하여ㄴ참이다. B는존재하지않는대상의쾌락고통을도덕판단근거에서배제하므로을판단때잉태되지않은다른아이를고려하면안된다는ㄷ참. 따라서세개모두⑤이며동일인치료와다른인물로대체의구조차이가핵심이다.', ['A의을비판ㄱ은맞지만갑의동일인판정ㄴ과B의배제ㄷ도참이다.','B의비존재고려배제ㄷ맞지만ㄱㄴ도모두맞아누락이다.','ㄱㄴ맞지만B가비존재자의쾌락고통을배제하는ㄷ도참이다.','ㄴㄷ맞지만A는을도잘못이라고명시하여ㄱ도포함해야한다.','동일인갑/상이인을/비존재자배제세분석이모두본문에맞다.']),
(3,'정당화J,의무O,자유선택F라두면㉠J↔O,㉡¬F,㉢¬F→¬O,㉣¬J다. ㉠㉢만으로는F=J=O=true인반례가있어ㄱ참. ㉡부정F로㉢부정¬F∧O를끌어낼수없고오히려F일때조건문은참이므로ㄴ거짓. ㄷ은비의지¬F와㉢의전건긍정으로¬O바로도출되어참. ㄱㄷ③이고의무없음은믿지말라는의무가아니다.', ['ㄱ참이지만비의지와㉢으로의무없음도출하는ㄷ도참이다.','자유선택F만으로비의지이면서의무인조건문반례를도출할수없다.','F=J=O참반례로ㄱ참이며비의지조건적용ㄷ참,ㄴ만거짓이다.','ㄷ맞지만㉡부정은㉢부정을함의하지않아ㄴ틀리다.','ㄱㄷ맞으나조건문부정을잘못도출한ㄴ을포함할수없다.']),
(3,'A는비의지와자유주의를받고의무론을거부하므로자유선택가능F는그전제¬F를약화해ㄱ참. B는의무론J↔O와비의지를받고자유주의를거부하니O→J가참이면그가수용한의무론한방향을뒷받침하여ㄴ참. 비의지여도O가있다는ㄷ자료는A의자유주의를약화하지만B가명시한가능성을지지하여B약화는거짓이다. ㄱㄴ③이며한사례가두입장에같은방향으로작용한다고하지않는다.', ['ㄱ맞지만B의의무론O→J를지지하는ㄴ도적절하다.','비의지인데도의무가있음은B를지지하므로둘다약화ㄷ틀리다.','A전제비의지반박ㄱ과B의의무론일부지지ㄴ이적절하다.','ㄴ맞지만ㄷ은B를강화하는자료라둘다약화가아니다.','ㄱㄴ맞으나A만약화하고B를지지하는ㄷ평가는거짓이다.']),
(5,'본문마지막에서이방원이왕이된직후절제사휘하모든군인지휘권을의흥삼군부로넘겼다고하여⑤다. 왕자와공신절제사는왕자의난이전에이미있었으며①시점반대. 주현군은고려무신이후사라져8위배속언급없고②아니다. 삼군도총제부창설은공민왕아닌회군후이성계이며③아니다. 의흥친군위는조선건국뒤자기사병으로만들었고당시8위이지2군6위도아니라④틀리다. 창설자·개편명칭·취소된명령·실제이관을구별한다.', ['왕자공신절제사는이성계재위중이미있어왕자의난뒤대체된것아니다.','주현군은무신집권이후사라졌으며그군인의조선초8위배속근거없다.','삼군도총제부는위화도회군후이성계가만들어공민왕창설아니다.','의흥친군위창설과8위지휘권이관은건국후이고2군6위표기도시기다르다.','이방원즉위직후절제사휘하모든군인지휘권이의흥삼군부로넘어갔다.'])]
src=r.read(b/'related295-source.json');assert not (b/'related295-own-solves.json').exists()
r.write(b/'related295-own-solves.json',[dict(id=s['id'],answer=a,reasoning=x,optionReasons=o) for s,(a,x,o) in zip(src,rows)])
r.write(b/'related295-solve-frozen.json',dict(frozenAt=r.now(),sha256=r.sha(b/'related295-own-solves.json'),beforeCurrentKeyAndExplanationReveal=True,historicalExposure='Three are previously reviewed fixed605 associated crosschecks; final one prior295. Earlier scores and previous own solves preserved.'))
worlds=[dict(J=J,O=O,F=F) for J,O,F in itertools.product([False,True],repeat=3) if (J==O) and (F or not O)]
assert dict(J=True,O=True,F=True) in worlds
r.write(b/'related295-pre-reveal-models.json',dict(status='PASS',dutyAndLiberalWorlds=worlds,negatingAntecedent='F does not imply not(F or not O)',reviewKinds={s['id']:'prior295' if j==3 else 'associated605' for j,s in enumerate(src)}))
bank=r.bank();r.write(b/'related295-before.json',[bank[s['id']] for s in src])
for s in src:
 q=bank[s['id']];print(q['id'],q['answer'],'underlines',q.get('underlines'));print('\n'.join(q['steps']));print('\n'.join(q['optionReasons']))
