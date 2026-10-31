import re,unicodedata
from fractions import Fraction as F
import pdfplumber
import review_remaining605 as r
b=r.folder(33);old={q['id']:q for q in r.read(b/'related295-before.json')};hist={q['id']:q for q in r.read(r.PREP/'previously-scored295.json')['questions']};checks=[]
assert 'All tests passed!' in (b/'related295-host-before.log').read_text(encoding='utf-8-sig')
assert r.read(b/'related295-source-native-pixel-checks.json')['status']=='PASS'
expense=[9680,2350,1203,860,811,744,717,640,530,439];assert sum(expense[1:])==8294<expense[0]
assert F(640)/F('1.067')<600<F(860)/F('1.35') and F(530)/F('1.3')/(F(717)/F('6.5'))==F(2650,717)<4
population=[105077,292837,217032,431587,416012];staff=[197,267,200,337,334];dispatch=[2590,3759,2712,5634,6793];missing=[442,651,455,747,1621];rescued=[482,702,426,611,676]
action=[a-bb for a,bb in zip(dispatch,missing)];dens=[F(s,p)*1000 for s,p in zip(staff,population)];calls=[F(d,s) for d,s in zip(dispatch,staff)];rates=[F(a,d) for a,d in zip(action,dispatch)];rescue=[F(z,a) for z,a in zip(rescued,action)]
assert dens[0]>1>max(dens[1:]) and sorted(range(5),key=lambda i:calls[i],reverse=True)==[4,3,1,2,0]
intervals=[[F(13),F('13.5')],[F(14),F(15)],[F('13.5'),F(14)],[F(16),F(17)],[F(20),F(21)]]
assert all(lo<v<hi for v,(lo,hi) in zip(calls,intervals)) and rates[3]>F(86,100)>F(84,100)>rates[2] and rescue[3]<F(13,100)<rescue[4]
assess=[]
for qid,q in old.items():
 assert hist[qid]['scoreBeforeFix']==5
 assess.append(dict(id=qid,historicalScorePreserved=5,currentBeforeScore=4,historicalEvidence=hist[qid]['evidence'],assessment='원문·답·직접 풀이 일치. 작은 보기 이미지와 일부 판정형 선지 해설을 보완한다.'+('공무원당 출동 순위를 보장할 상한도 명시한다.' if q['number']==23 else ''),notReplacementOfHistoricalScore=True))
assert not (b/'related295-assessment-before.json').exists();r.write(b/'related295-assessment-before.json',assess)
bodies={17:'<보기>\n\nㄱ. 2023년 국방비지출액은 프랑스가 독일보다 크다.\n\nㄴ. 2024년 상위 10개국 국방비지출액의 합에서 미국이 차지하는 비중은 50% 이상이다.\n\nㄷ. 2024년 GDP는 일본이 사우디아라비아의 4배 이상이다.',23:'<보기>\n\nㄱ. 인구 천 명당 소방직 공무원 수는 A구가 가장 많다.\n\nㄴ. 소방직 공무원 1인당 출동 건수는 B구가 세 번째로 많다.\n\nㄷ. 조치 비율은 C구가 가장 높다.\n\nㄹ. 조치 1건당 구조 인원수는 D구가 E구보다 많다.'}
reasons={17:['프랑스의 전년액은 640/1.067로 600 미만이고, 독일은 860/1.35로 600 초과다. 따라서 ㄱ은 틀리다.','미국 9,680억 달러가 나머지 아홉 나라 합 8,294억 달러보다 크므로 상위 10개국 합의 절반을 넘는다. ㄴ만 옳다.','일본/사우디 GDP 비는 2,650/717이다. 2,650<717×4=2,868이므로 ㄷ의 4배 이상은 틀리다.','프랑스의 전년액은 독일보다 작고, 일본 GDP는 사우디의 4배 미만이다. ㄱ·ㄷ 모두 틀리다.','미국 비중이 절반 이상인 ㄴ은 맞지만, 일본/사우디 GDP 비가 2,650/717<4여서 ㄷ은 틀리다.'],23:['인구 천 명당 공무원 수는 A만 1명을 넘고, 공무원당 출동은 E>D>B>C>A여서 B가 세 번째다. ㄱ·ㄴ만 옳다.','A의 인구당 공무원 수가 가장 많아 ㄱ은 맞다. 그러나 조치 비율은 D가 86% 초과, C가 84% 미만이므로 ㄷ은 틀리다.','D의 조치 비율은 C보다 높아 ㄷ이 틀리다. 조치당 구조는 D가 13% 미만, E가 13% 초과이므로 ㄹ도 틀리다.','ㄱ·ㄴ은 맞지만 D의 611/4,887은 13% 미만, E의 676/5,172는 13% 초과다. D가 더 많다는 ㄹ을 추가할 수 없다.','B가 공무원당 출동 3위인 ㄴ은 맞다. 그러나 조치 비율 D>C, 조치당 구조 D<E로 ㄷ·ㄹ이 틀리며, 참인 ㄱ도 빠졌다.']}
reg={x['newAsset']:x for x in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/native-image-repairs.json')['figures']};norm=lambda s:re.sub(r'\s','',unicodedata.normalize('NFKC',s))
changes=r.read(r.OUT/'changes-batch33.json')
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  if q['id'] not in old:continue
  before=old[q['id']];assert q==before;n=q['number'];snap=r.OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();r.write(snap,before)
  q['body']=bodies[n];q['figures']=q['figures'][:1];q['optionReasons']=reasons[n]
  if n==23:q['steps'][1]=q['steps'][1].replace('E 20 초과, D 16 초과, B 14 초과, C 13.5 초과·14 미만, A 13.5 미만','E 20 초과·21 미만, D 16 초과·17 미만, B 14 초과·15 미만, C 13.5 초과·14 미만, A 13 초과·13.5 미만')
  q['revision']+=1;touched=True;rec=reg[before['figures'][1]['asset']]
  with pdfplumber.open(r.ROOT/rec['source']) as pdf:raw=pdf.pages[rec['page1based']-1].crop(rec['rect']).extract_text()
  assert norm(raw)==norm(q['body']) and q['answer']==before['answer'] and q['choices']==before['choices'] and (r.ROOT/before['figures'][1]['asset']).is_file()
  changes.append(dict(id=q['id'],file=p.relative_to(r.ROOT).as_posix(),oldRevision=before['revision'],newRevision=q['revision'],changedFields=sorted(k for k in q if k!='revision' and q[k]!=before[k]),beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason='Original prose native readability, substantive individual reasons, and explicit separating ratio intervals for d23.',cohort='prior295',status='repaired_pending_reverification'))
  checks.append(dict(id=q['id'],exactOriginalProse=True,originalFigureRetained=True,answersAndChoicesUnchanged=True))
 if touched:r.write(p,data)
assert len(changes)==12;r.write(r.OUT/'changes-batch33.json',changes)
assert r.sha(b/'related295-own-solves.json')==r.read(b/'related295-solve-frozen.json')['sha256']
r.write(b/'related295-repair-model-checks.json',dict(status='PASS',checks=checks,defense={'sumOthers':8294,'us':9680,'gdpRatio':'2650/717<4','previousFrance':'640/1.067<600','previousGermany':'860/1.35>600'},fire={'actions':action,'density':list(map(str,dens)),'calls':list(map(str,calls)),'separatingCallIntervals':[[str(x) for x in pair] for pair in intervals],'actionRates':list(map(str,rates)),'rescuesPerAction':list(map(str,rescue))},historicalScoresAndFrozenSolvesPreserved=True))
print('Two prior295 repaired; exact source prose/ratio models/frozen solves PASS.')
