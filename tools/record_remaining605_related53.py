import review_remaining605 as r
b=r.folder(53);src=r.read(b/'related295-source.json')
rows=[(5,'일시금은1등당첨금의60%에서세금을빼므로원래1등당첨금보다적어⑤다. 60%는전체등위당첨금합계이고그절반30%가당회1등배정이다. 공공기금은25%여서과반아니고미당첨이월도전체판매액아니다. 20세기초합법복권은거의사라졌고메가는45개주로모든주가아니다. 본문규칙에따른비교이며외부복권제도를추가하지않는다.', ['공공기금은판매액25%로과반50%초과가아니다.','20세기초전국에서합법복권이거의사라졌다는흐름을뒤집었다.','이월대상은1등배정잔액이며판매액전부가아니다.','45개주는모든주가아니며유통영역을확대할수없다.','일시금은당첨금60%에서세금을뺀액수라원래당첨금보다작다.']),
(3,'乙은丙丁을추월하고다시추월당하지않아최종乙이두사람보다앞이다. 丁은丙에게따라잡힌적없으므로丁이丙앞이며丙앞에달린적있는사람도乙丁뿐이라甲戊는丙뒤다. 따라서乙1丁2丙3이고甲은1또는5중1이불가해5,戊4다. 동순위없음까지적용해乙丁丙戊甲유일순서이며정답③. 중간추월서술을최종전체순위로무조건바꾸지않고추월없음조건과결합한다.', ['甲은1또는5인데乙丁丙이앞이라5등이다.','乙은丙丁을추월한후누구에게도추월당하지않았고甲戊도丙뒤이므로1등이다.','乙丁만丙보다앞에설수있고둘다최종앞이어서丙3등이다.','丁은乙에게추월당했으나丙에게따라잡히지않아2등이다.','戊는丙보다뒤이며甲5등이므로4등이다.'])]
assert not (b/'related295-own-solves.json').exists();r.write(b/'related295-own-solves.json',[dict(id=s['id'],answer=a,reasoning=x,optionReasons=o) for s,(a,x,o) in zip(src,rows)])
r.write(b/'related295-solve-frozen.json',dict(frozenAt=r.now(),sha256=r.sha(b/'related295-own-solves.json'),beforeCurrentKeyAndExplanationReveal=True))
bank=r.bank();r.write(b/'related295-before.json',[bank[s['id']] for s in src])
for s in src:
 q=bank[s['id']];print(q['id'],q['answer']);print(q['body']);print('\n'.join(q['steps']));print('\n'.join(q['optionReasons']))
