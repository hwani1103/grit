import review_remaining605 as r
b=r.folder(56)
rows=[(2,'자체예산100억은공공50과기타50으로나눈다. 교부금20억은공공16과기타4로나눠내년공공66,기타54,합계120이다. 따라서기타가전년보다4억증가한②만맞다. 공공증가액16이고증가율16/50=32%이며전체예산증가율20%와구별한다. 같은총액이라도재원의종류별배분비율이다르므로60/60으로나눌수없다.', ['기타는자체50에교부금4를더해54억으로60억아니다.','기타50에서54로4억늘어나므로이선지가맞다.','공공은50에서66으로16억늘어나동일하지않다.','공공증가율16/50=32%이며50%가아니다.','공공증가액은20의80%인16억으로10억이아니다.']),
(1,'피인용횟수는5회마다1점이므로몫9,12,17,7,33이다. 실적/계획/특허를합산하면A68,B94,C77,D93,E79로순위B,D,E,A보다C순이나상위3중E79는80미만이라제외한다. B1위기본10+우수1=11억,D2위7−특허2건감액1=6억,총17억①. 3위E를선정하거나우수증액으로선정점수80을넘겼다고판단하면안되고선정과지급을순서대로적용한다.', ['B94와D93만80점이상이므로11+6=17억이다.','18억은D의특허3건미만감액1억을빠뜨린합계다.','총액은선정된B11과D6뿐이므로19억을구성할세번째팀이없다.','21억은80점미만인E를3위로선정해4억을더한결과다.','22억은탈락E를포함하거나D감액을누락한값으로허용되지않는다.'])]
src=r.read(b/'related295-source.json');assert not (b/'related295-own-solves.json').exists()
r.write(b/'related295-own-solves.json',[dict(id=s['id'],answer=a,reasoning=x,optionReasons=o) for s,(a,x,o) in zip(src,rows)])
r.write(b/'related295-solve-frozen.json',dict(frozenAt=r.now(),sha256=r.sha(b/'related295-own-solves.json'),beforeCurrentKeyAndExplanationReveal=True,historicalExposure='Prior reviews existed; not independent or blind.'))
scores=[15*x+y//5+z+3*w for x,y,z,w in [(2,45,20,3),(3,62,25,4),(2,88,15,5),(4,37,20,2),(1,165,25,2)]]
assert scores==[68,94,77,93,79]
r.write(b/'related295-pre-reveal-models.json',dict(status='PASS',scores=scores,selected=['B','D'],grants=[11,6],public=66,other=54))
bank=r.bank();r.write(b/'related295-before.json',[bank[s['id']] for s in src])
for s in src:
 q=bank[s['id']];print(q['id'],q['answer']);print(q['body']);print(q.get('figures'));print('\n'.join(q['steps']));print('\n'.join(q['optionReasons']))
