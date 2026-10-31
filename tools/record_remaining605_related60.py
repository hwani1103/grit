from fractions import Fraction as F
import review_remaining605 as r
b=r.folder(60)
rows=[(1,'2024개최소세종359다음대전1218이고고양이최소세종100다음대전337로두번째가같아①이다. 고양이27826은전국106824의25%26706보다커②거짓. 전국개는80393→80467→77304로마지막감소. 경기20946은전국20%21364.8미만. 개감소3163은고양이감소3063보다커⑤도거짓이다. 감소율대신감소폭이라는차이의개수를비교한다.', ['개와고양이둘다최저세종다음대전이두번째최소지역이다.','고양이27826은전국106824의4분의1인26706보다많다.','2023년80467에서2024년77304로줄어매년증가가아니다.','경기20946은전국20퍼센트21364.8보다적다.','개3163마리감소는고양이3063마리감소보다100마리더크다.']),
(3,'여성발의2559중반영522이고20%는511.8이므로522>511.8,20%이하라는③거짓이다. 정부383/12413은5%이하,의원계류9096/11573은80%이하,남성9014/11573은70%이상이다. 의원미반영기간은남149건79.4일과여39건80.6일가중평균으로같은80일경계에서부족149×.6이초과39×.6보다커80일미만이다. 평균둘을단순평균80으로처리하면안된다.', ['정부383은전체12413의5퍼센트620.65이하라맞다.','계류9096은11573의80퍼센트9258.4보다작다.','여성반영522는2559의20퍼센트511.8보다많아옳지않다.','남성9014는11573의70퍼센트8101.1보다커맞다.','79.4일149건이80.6일39건보다많아가중평균은80일미만이다.']),
(1,'전체회원85.2만명중장기저축744733명비중은약87.41%로85%초과하여①거짓이다. 장기자산27.3조원이전체64.5%라전체42.325조원으로40이상. 자산상위4제도가입수합872578명은전체852000명보다20578많으며1인최대2가입이라이네제도중2개가입자가최소20578명이다. 충청61850>장기총744733/15약49649,1인구좌장기449579295/744733은분할2829332/32411의약6.92배로5이상이다. 중복수를정확한값으로단정않고하한으로판정한다.', ['744733은852000의85퍼센트724200보다커85퍼센트이하가틀리다.','27.3조원이전체의64.5퍼센트이므로총액약42.33조원이다.','상위4가입합872578에서전체852000을뺀20578명이중복가입하한이다.','충청61850명은장기저축744733명의15지역평균약49649명보다많다.','장기약603.68구좌는분할약87.29구좌의5배보다많다.'])]
src=r.read(b/'related295-source.json');assert not (b/'related295-own-solves.json').exists()
assert sum([744733,55090,40344,32411])-852000==20578
r.write(b/'related295-pre-reveal-models.json',dict(status='PASS',animalDeclines=[80467-77304,30889-27826],femaleBillShare=str(F(522,2559)),unreflectedWeightedDays=str((149*F('79.4')+39*F('80.6'))/188),membershipOverlapLowerBound=20578,assetsTrillion=str(F('27.3')/F('.645')),longMembershipShare=str(F(744733,852000)),accountRatio=str(F(449579295*32411,744733*2829332)),overlapExplanation='At most two schemes per member. Four-scheme membership sum minus all members is a lower bound, not exact count.'))
r.write(b/'related295-own-solves.json',[dict(id=s['id'],answer=a,reasoning=x,optionReasons=o) for s,(a,x,o) in zip(src,rows)])
r.write(b/'related295-solve-frozen.json',dict(frozenAt=r.now(),sha256=r.sha(b/'related295-own-solves.json'),beforeCurrentKeyAndExplanationReveal=True))
bank=r.bank();r.write(b/'related295-before.json',[bank[s['id']] for s in src])
for s in src:
 q=bank[s['id']];print(q['id'],q['answer']);print('\n'.join(q['steps']));print('\n'.join(q['optionReasons']))
