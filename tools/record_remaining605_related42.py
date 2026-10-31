import review_remaining605 as r
b=r.folder(42)
rows=[(4,'2021년이후중학생남녀섭취율차는.4,.9,1.6,1.4%p로2024감소하여ㄱ거짓.ㄴ2024남중20.6<21.9,남고14.2<14.8,여중19.2<20.3,여고14.6<14.9로전부감소참.ㄷ동일섭취자수를가정하면2020조사대상=13827*.192/.25=10619.136명으로10000초과여서거짓.표시반올림±.05%p양끝에서도10569명초과라판정유지.ㄹ여중2년4610*.194=894.34명,남고2년4160*.141=586.56명,1.5배879.84보다커참.최악표시오차여중하한4610*.1935=892.035>남고상한4160*.1415*1.5=882.96로반올림에도참.ㄴㄹ④.', ['ㄴ은맞지만ㄱ은2024년차가1.6에서1.4로줄어거짓이다.','ㄱ차의매년증가와ㄷ조사대상10000이하가모두거짓이다.','ㄴ은맞지만ㄷ은2020조사대상약10619명으로10000초과여서틀리다.','네집단섭취율모두감소하며여중2년섭취자수는남고2년의1.5배이상이어서맞다.','ㄹ은맞지만ㄷ은섭취자수와조사대상수를분리해역산하면10000초과다.']),
(3,'A불량분류6개와정밀도1/3에서TB2,FB4로ㄱ참.재현율2/3에서실제불량전체3개다.B와C는재현율1이라실제불량은두불량분류집합교집합{1,5,7,10}안의3개이다.D불량집합{1,2,5,6,8}과정밀도2/5로TB2이므로후보중1,5가실제불량이다.나머지7/10중A불량에7만포함되고A의TB2에는1외한개필요해7로확정.실제불량{1,5,7},ㄷ참.D는TB2,FG1,FB3,TG4여서정확도6/10=3/5로ㄴ거짓.따라서ㄱㄷ③.모든1024실제불량부분집합도이세트하나로확인가능하다.', ['ㄱFB4는맞으나실제불량1,5,7인ㄷ도참이어서누락이다.','D정확도는진불량2와진양호4의합6/10이므로1/2아니다.','A위불량4개와실제불량1,5,7이모두맞고D정확도1/2는틀리다.','ㄷ은맞지만ㄴ정확도는2/5정밀도나1/2가아닌3/5다.','ㄱㄷ은맞으나ㄴD정확도1/2는계산6/10과불일치한다.'])]
src=r.read(b/'related295-source.json');assert not (b/'related295-own-solves.json').exists()
r.write(b/'related295-own-solves.json',[dict(id=s['id'],answer=a,reasoning=x,optionReasons=o) for s,(a,x,o) in zip(src,rows)])
r.write(b/'related295-solve-frozen.json',dict(frozenAt=r.now(),sha256=r.sha(b/'related295-own-solves.json'),beforeKeyAndExplanationReveal=True))
bank=r.bank();r.write(b/'related295-before.json',[bank[s['id']] for s in src])
for s in src:
 q=bank[s['id']];print(q['id'],q['answer']);print(q['body']);print('\n'.join(q['steps']));print('\n'.join(q['optionReasons']));print([(f['asset'],f['caption']) for f in q['figures']])
