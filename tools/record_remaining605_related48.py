import review_remaining605 as r
b=r.folder(48)
rows=[(3,'총배출A51.7,B64,C17.3,D10.8이고1인당A약5.33,B22.07,C7.208,D7.2이다.갑은50이상과1인당최소인A.주거+상업합A31/B9/C7/D4.8로을은D이며D와1인당차1이하인병은C뿐이다.C주거17.3−4−3.5−6.3=3.5,비중3.5/17.3약20.2%로정B4.5/64약7%보다높다.A갑B정C병D을③.', ['A갑D을은맞지만B병은D와1인당차1을훨씬넘어틀리다.','A갑B정은맞지만을은건물합최소D이므로C을은틀리다.','A갑B정C병D을로총량/1인당/비중/건물합네조건모두맞다.','갑은1인당최소A인데B로배정하여틀리고을도최소건물합D가아니다.','C병D을은맞지만B는1인당최소가아니므로갑이될수없다.']),
(4,'등록전체461733→600648→820329→1159087→1589985는매년1.3배초과①참.2018대비2022등록증가량하이브리드758476최대,증가율수소29623/893−1약32.17최대②참.수출합은195361/258669/271327/404897/553722로매년증가③참.유형수출하이브리드150474→124503,플러그인31399→26065는2020감소,수소1119→361은2022감소라매년증가는전기만④거짓.상위10세집합교집합일본독일벨기에영국한국5국⑤참.', ['전체등록대수의네전년비모두1.3이상으로매년30%증가가맞다.','수소등록대수29623/893약33.17배로다른유형의배율보다크다.','네유형수출을해마다합하면195361에서553722까지매년증가한다.','수소수출은2021년1119대에서2022년361대로감소해매년증가가아니다.','세유형상위10교집합은일본독일벨기에영국한국의정확히5개국이다.'])]
src=r.read(b/'related295-source.json');assert not (b/'related295-own-solves.json').exists()
r.write(b/'related295-own-solves.json',[dict(id=s['id'],answer=a,reasoning=x,optionReasons=o) for s,(a,x,o) in zip(src,rows)])
r.write(b/'related295-solve-frozen.json',dict(frozenAt=r.now(),sha256=r.sha(b/'related295-own-solves.json'),beforeKeyAndExplanationReveal=True))
bank=r.bank();r.write(b/'related295-before.json',[bank[s['id']] for s in src])
for s in src:
 q=bank[s['id']];print(q['id'],q['answer']);print(q['body']);print(q.get('underlinedPhrases'));print('\n'.join(q['steps']));print('\n'.join(q['optionReasons']))
