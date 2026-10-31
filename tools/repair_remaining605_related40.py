import re
from fractions import Fraction as F
import review_remaining605 as r
b=r.folder(40);old={q['id']:q for q in r.read(b/'related295-before.json')}
assert 'All tests passed!' in (b/'related295-host-before.log').read_text(encoding='utf-8-sig') and r.read(b/'related295-source-key-checks.json')['status']=='PASS'
hist={q['id']:q for q in r.read(r.PREP/'previously-scored295.json')['questions']}
notes={16:'최종합의·홈페이지유지와앱추가·대상확대범위정확. A시의고유도시표기어절을연결한다.',24:'100구획공통전제와지원자격/우선순위/금액을정확히구분. 원본밑줄은조례제9조를개정까지인데하였고까지확장되어있어범위를복원한다. A시/B카페/15km·조례괄호와목록공백도정리.',6:'정답④와발병률/환자내수용체분포구별은맞다. 하지만⑤해설이전체미국여성환자비율증가를관찰한것처럼적었다. 원문전체는수용체보유환자숫자증가이며비율증가율비교는1960년대출생흑인집단이다. 관측의모집단과수/비율을분리하고퍼센트어절을복원한다.'}
assess=[dict(id=i,historicalScorePreserved=hist[i]['scoreBeforeFix'],currentBeforeScore=3 if q['number']==6 else 4,assessment=notes[q['number']],notReplacementOfHistoricalScore=True) for i,q in old.items()]
assert not (b/'related295-assessment-before.json').exists();r.write(b/'related295-assessment-before.json',assess)
changes=r.read(r.OUT/'changes-batch40.json')
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  if q['id'] not in old:continue
  prev=old[q['id']];assert q==prev;n=q['number'];snap=r.OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();r.write(snap,prev)
  if n in [16,24]:
   for k in ['body','pitfall','transfer']:
    if k in q:q[k]=q[k].replace('A 시','A시').replace('B 카페','B카페').replace('15 km','15km').replace('조례」 (','조례」(').replace('휴게· 문화시설','휴게·문화시설')
   for k in ['choices','steps','optionReasons']:q[k]=[s.replace('A 시','A시').replace('B 카페','B카페') for s in q[k]]
  if n==24:
   assert q['underlines']==['조례 제9조를 개정하였고'];q['underlines']=['조례 제9조를 개정']
  if n==6:
   q['body']=re.sub(r'(?<=\d)\s+(?=%)','',q['body'])
   q['steps'][3]='정석 근거: 전체 미국 여성 유방암 환자에 관한 문단은 수용체를 가진 환자의 숫자가 늘었다고 한다. 그다음 문단은 1960년대 출생 흑인 여성 환자 집단으로 범위를 좁혀 수용체 보유 비율의 증가율을 법의 존재 지역별로 비교한다. 이 사회 환경의 차이와 생물학적 특성의 관련 가능성을 일반화한 것이 ④다.'
   q['optionReasons'][4]='전체 미국 여성 환자에 대해서는 수용체 보유 환자의 숫자 증가만 제시되었다. 비율의 증가율을 비교한 대상은 1960년대 출생 흑인 여성 환자 집단이므로 이를 전체의 비율 증가로 확대할 수 없다. 사회 환경을 포함한 일반화된 결론도 아니다.'
   q['transfer']='수의 증가와 비율의 증가를 구분하고, 자료마다 분모와 조사 집단을 적는다. 특정 하위 집단의 비율 변화를 전체 집단의 추세로 확대하지 않는다.'
  fields=sorted(k for k in q if q[k]!=prev[k]);assert fields and q['answer']==prev['answer'];q['revision']+=1;touched=True
  assert re.sub(r'\s','',q['body'])==re.sub(r'\s','',prev['body']) and [re.sub(r'\s','',s) for s in q['choices']]==[re.sub(r'\s','',s) for s in prev['choices']]
  changes.append(dict(id=q['id'],file=p.relative_to(r.ROOT).as_posix(),oldRevision=prev['revision'],newRevision=q['revision'],changedFields=fields,beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason=notes[n],cohort='prior295',status='repaired_pending_reverification'))
 if touched:r.write(p,data)
r.write(r.OUT/'changes-batch40.json',changes)
assert len(changes)==7 and 50<100 and 60>50 and F(60,200)<F(50,100) and 60>50
r.write(b/'related295-repair-model-checks.json',dict(status='PASS',count=3,source='related295-source-key-checks.json',website='Preserve website instructions plus add app; replacement violates requirement.',qualification='50<100; adding facility types cannot remove parent100 threshold; recommendation support reaches nonmandatory facilities.',numberRatioCounterexample='50/100 ->60/200: count rises50to60 while ratio falls50%to30%. Hypothetical logical model, not empirical cancer data.',populationScope='AllUS patient count differs from1960s-born black patient subgroup proportion; no incidence claim.',underline24='source-underline24.png shows underline ends at 개정; 하였고 excluded.',historicalScoresPreserved=True))
print('3prior rechecked and repaired; current4/4/3 frozen; original scores preserved')
