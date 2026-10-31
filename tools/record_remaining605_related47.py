import review_remaining605 as r
b=r.folder(47)
rows=[(4,'원문 배치순서는 입춘 우수 경칩 춘분 청명 곡우 입하 소만 망종 하지 소서 대서 입추 처서 백로 추분 한로 상강 입동 소설 대설 동지 소한 대한이다. 우수는 기준점0이고 그 뒤 경칩1부터 센다. 입추11 처서12이므로④. 네 계절마다6개라12개뒤는반대계절의같은유형순서로 봄교첫우수→가을교첫처서로도 확인된다. 우수를첫번째로포함해입추를고르지않는다.', ['곡우는 우수 뒤4번째이므로 요구한12번째보다 이르다.','망종은 우수 뒤7번째이며12번째는 처서다.','입추는 우수 뒤11번째로 기준 우수를 포함해 세면 생기는 오류다.','경칩부터1로 세면 처서가12번째이며 반대계절의 교 첫절기와도 맞는다.','상강은 우수 뒤16번째로12번째가 아니다.']),
(2,'1893년12전은1884년가격의60%이므로 원가격은12/0.6=20전이다. 설탕이 같은무게소고기의2.5배여서 소고기1근은20/2.5=8전이다. 예산52전에서설탕1근20전을빼면32전남아 소고기32/8=4근②다. 40%하락을12의40%를더하는방식으로복원하지않고,1884년설탕과소고기를같은시점에비교한다. 모든예산을쓰는지20+4×8=52로검산.', ['설탕20전에 소고기3근24전을 더하면44전으로8전이남아 전액사용조건과다르다.','1884년설탕20전과소고기4근32전을합하면52전전부사용한다.','소고기5근이면40전과설탕20전으로60전이되어예산을넘는다.','소고기6근48전과설탕20전은68전으로52전조건에맞지않는다.','소고기7근56전만으로도예산52전을넘어불가능하다.'])]
src=r.read(b/'related295-source.json');assert not (b/'related295-own-solves.json').exists()
r.write(b/'related295-own-solves.json',[dict(id=s['id'],answer=a,reasoning=x,optionReasons=o) for s,(a,x,o) in zip(src,rows)])
r.write(b/'related295-solve-frozen.json',dict(frozenAt=r.now(),sha256=r.sha(b/'related295-own-solves.json'),beforeKeyAndExplanationReveal=True))
bank=r.bank();r.write(b/'related295-before.json',[bank[s['id']] for s in src])
for s in src:
 q=bank[s['id']];print(q['id'],q['answer']);print('\n'.join(q['steps']));print('\n'.join(q['optionReasons']))
