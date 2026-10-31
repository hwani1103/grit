import review_remaining605 as r
b=r.folder(44)
rows=[(1,'丙은5마리라최소50점이며점수서로다른10점단위순위로乙은최소60점,甲은최소70점이다.甲이A없으면3마리최대60점이라모순으로ㄱ참이다.乙80점이라도A2/C2/B0이가능하고甲A3=90,丙C5=50과양립해ㄴ거짓이다.丙이C없으면5마리최소100점으로甲최대90보다높아져3위불가이므로오히려C필수라ㄷ거짓이다.ㄱ①.', ['甲은최소70점인데A없는3마리최대60이므로A를잡았다는ㄱ만참이다.','乙A2마리C2마리면80점으로B없이2위가능하여ㄴ거짓이다.','ㄱ참이지만丙은C없으면최소100점이라3위불가여서ㄷ거짓이다.','乙80점B필수도丙C없음도각각반례/최소점으로부정된다.','ㄱ만참이고ㄴㄷ이거짓이므로셋모두는아니다.']),
(4,'복용8일을AA일x,BB일y,AB일z로두면x+y+z=8이고A총량=2x+z,B총량=2y+z다.ㄱ잔여2/2이면총8/8이라x=y=4,z=0의모든날오복용반례가있다.ㄴ잔여1/3이면A9,B7을먹어z는홀수이므로최소1일이있다.ㄷ잔여4/0이면A6,B10이라z는짝수이고0/2/4/6일가능하여5일불가능하다.잔량의총합만으로매일조합을확정하지않고홀짝으로가능날짜경계를판정한다.', ['총량8/8은AA4일BB4일도가능해매일제대로라는ㄱ거짓이다.','ㄴ은맞지만A6정의짝수성으로5일불가인ㄷ도참이라누락이다.','ㄷ은맞아도잔여2/2에서올바른날0인반례로ㄱ거짓이다.','A9정이면AB홀수최소1일, A6정이면AB짝수라5일불가로ㄴㄷ참이다.','ㄴㄷ이참이어도매일복용상태를총잔량에서확정하는ㄱ은거짓이다.'])]
src=r.read(b/'related295-source.json');assert not (b/'related295-own-solves.json').exists()
r.write(b/'related295-own-solves.json',[dict(id=s['id'],answer=a,reasoning=x,optionReasons=o) for s,(a,x,o) in zip(src,rows)])
r.write(b/'related295-solve-frozen.json',dict(frozenAt=r.now(),sha256=r.sha(b/'related295-own-solves.json'),beforeKeyAndExplanationReveal=True))
bank=r.bank();r.write(b/'related295-before.json',[bank[s['id']] for s in src])
for s in src:
 q=bank[s['id']];print(q['id'],q['answer']);print(q['body']);print('\n'.join(q['steps']));print('\n'.join(q['optionReasons']))
