import itertools,math
import review_remaining605 as r
b=r.folder(59)
rows=[(4,'5·6·7명조직수를a,b,c라두면a+b+c=10,5a+6b+7c=57이므로b+2c=7이다. 세규모가각각하나이상이라c=1,2,3에대응하여b=5,3,1이고a=4,5,6이다. 따라서5명조직최소4최대6으로④. c=0은7명조직필수조건위반, c=4면b음수라불가하므로다른극값은없다.', ['최소1은10개조직과총57명동시조건을만족하지못한다.','최소3은불가하고최대5도a6인경우를빠뜨린다.','최대6은맞지만최소는a4여서3이아니다.','a,b,c가4,5,1또는5,3,2또는6,1,3이므로경계4와6이다.','a7이면남은3개에22명을넣어야하는데7명상한에서도21명뿐이다.']),
(3,'甲착수금은기본120만원+종속2개7만원+도면3개4.5만원=131.5만원이다. 독립항1개와명세서14면은추가없으며등록결정사례금도동액이라합263만원이다. 乙은독립항초과4개40만원만더해도상한140만원을넘고거절되어사례금0이라합140만원이다. 차이123만원③이며착수금상한을최종보수전체상한으로적용하지않는다.', ['2만원은甲사례금이나추가항목을누락한값으로차액123만원과다르다.','8만5천원은착수금140와131.5차이일뿐甲사례금을빠뜨렸다.','甲263만원에서乙140만원을빼면123만원차이다.','129만5천원은甲항목의실제합계131.5및동액사례금과맞지않는다.','259만원은차이가아니며상한적용후甲263乙140을비교해야한다.']),
(4,'내부4명고정에외부e명이총수의1/3이상이려면3e≥4+e라e≥2,최소6명은남녀3대3으로실현가능하다. 내부여4일때외부남3으로총7명은양쪽성별이상대절반보다많아허용된다. 총8명이면회의출석최소6명이고찬성최소4명이므로3명가결④불가. 직접5+서면2출석7명은총수최대10의개의정족수7을충족하고찬성5명은7의2/3이상이라서면의견무관가결. 외부2년임기2회연임총6년도맞다.', ['최초2년과두번연임4년합계6년까지가능하다.','외부2명과내부4명총6명이최소이며남녀3대3구성이가능하다.','내부여4외부남3이면외부비율과양성별엄격한절반초과조건충족한다.','총8명출석최소6명이고찬성은최소4명이라3명만으로가결불가다.','서면2명도출석이라7명개의가능하고직접찬성5명은7명의2/3이상이다.'])]
src=r.read(b/'related295-source.json');assert not (b/'related295-own-solves.json').exists()
solutions=[(a,c,d) for a,c,d in itertools.product(range(1,11),repeat=3) if a+c+d==10 and 5*a+6*c+7*d==57];assert solutions==[(4,5,1),(5,3,2),(6,1,3)]
r.write(b/'related295-pre-reveal-models.json',dict(status='PASS',organizationSolutions=solutions,remuneration=[2630000,1400000,1230000],eightMemberQuorum=[math.ceil(8*2/3),math.ceil(6*2/3)],sevenPresentPass=5,allGenderCounts={str(n):[f for f in range(n+1) if 2*f>n-f and 2*(n-f)>f] for n in range(6,11)}))
r.write(b/'related295-own-solves.json',[dict(id=s['id'],answer=a,reasoning=x,optionReasons=o) for s,(a,x,o) in zip(src,rows)])
r.write(b/'related295-solve-frozen.json',dict(frozenAt=r.now(),sha256=r.sha(b/'related295-own-solves.json'),beforeCurrentKeyAndExplanationReveal=True))
bank=r.bank();r.write(b/'related295-before.json',[bank[s['id']] for s in src])
for s in src:
 q=bank[s['id']];print(q['id'],q['answer']);print('\n'.join(q['steps']));print('\n'.join(q['optionReasons']));print('body:',q['body'])
