import re,itertools,datetime,unicodedata,copy
from fractions import Fraction as F
import pdfplumber
import review_remaining605 as r
b=r.folder(39);old={q['id']:q for q in r.read(b/'related295-before.json')};assert 'All tests passed!' in (b/'related295-host-before.log').read_text(encoding='utf-8-sig');assert r.read(b/'related295-source-native-pixel-checks.json')['status']=='PASS'
pred=[{1,3,4,7,8,9},{1,2,5,7,8,9,10},{1,4,5,7,10},{1,2,5,6,8}];prec=[F(1,3),F(3,7),F(3,5),F(2,5)];recall=[F(2,3),F(1),F(1),F(2,3)];solutions=[]
for k in range(1,11):
 for tup in itertools.combinations(range(1,11),k):
  actual=set(tup)
  if all(F(len(actual&p),len(p))==pr and F(len(actual&p),k)==rc for p,pr,rc in zip(pred,prec,recall)):solutions.append(tup)
assert solutions==[(1,5,7)] and len(pred[0]-set(solutions[0]))==4
actual=set(solutions[0]);D=pred[3];assert F(len(actual&D)+len(set(range(1,11))-actual-D),10)==F(3,5)
date=datetime.date;day=datetime.timedelta
assert date(2014,7,2)+day(days=27)==date(2014,7,29) and date(2017,7,29)-day(days=28)==date(2017,7,1)
assert date(2015,6,25)+day(days=34)==date(2015,6,24)+day(days=35)==date(2015,7,29)
north=[26,19,49,28,35,37,29,16,34,54,17,33,31,29];south=[31,30,46,28,36,29,32,14,35,38,17,34,33,36];assert max(north)==54 and max(south)==46 and sum(a>=40 and c>=40 for a,c in zip(north,south))==1
assert F('3.06')<F('5.68')<F('6.98') and F('24.5')>F('19.36')>F('13.89') and sum(map(F,['4.21','11.89','22.87','44.36']))==F('83.33')
assert max([4.2,3.5,3.3,4.1,2.9])==4.2 and sorted([3.7,4.2,2.8,1.5,3.3],reverse=True)[1]==3.7
bodies={39:'<보기>\n\nㄱ. 분류기 A를 사용했을 때, ‘위불량(FB)’은 4개다.\n\nㄴ. 분류기 D의 ‘정확도’는 1/2이다.\n\nㄷ. 실제 불량품은 상품 1, 상품 5, 상품 7이다.',4:'<보기>\n\nㄱ. 장마 기간이 가장 길었던 해는 중부 지방과 남부 지방 모두 2020년이다.\n\nㄴ. 같은 해에 중부 지방과 남부 지방의 장마 기간이 각각 40일 이상이었던 해는 한 번뿐이다.\n\nㄷ. 2014년과 2017년 중부 지방의 장마 종료일이 같다면, 2017년 중부 지방의 장마는 6월에 시작되었다.\n\nㄹ. 2015년 장마 종료일은 중부 지방과 남부 지방이 같다.',1:'<보고서>\n\n2024년 공용자전거 A의 이용용도별 비중은 ‘여가·오락·운동’이 가장 크게 나타났고, 그다음으로 ‘통근’, ‘친교’의 순이었다. ‘여가·오락·운동’과 ‘친교’의 비중은 2023년 대비 각각 증가했으나 ‘통근’의 비중은 오히려 감소했다. 또한, 2024년에는 ‘기타’를 제외하고 ‘학원’의 이용용도 비중이 가장 작았고, 그다음으로 ‘업무’, ‘쇼핑’의 순이었다. 그러나 2023년에는 ‘기타’를 제외하고 ‘쇼핑’의 비중이 가장 작았다.\n\n공용자전거 A의 평균 이용시간은 ‘30분 이상 1시간 미만’의 비중이 44.36%로 가장 컸고, 1시간 미만으로 이용하는 비중은 80% 이상이었다.\n\n공용자전거 A의 이용 시 불편사항으로는 ‘무거운 자전거’가 가장 많았으며 그다음으로는 ‘기타’를 제외하고 ‘대여소간 연계성 부족’, ‘잦은 고장’의 순이었다. 이를 개선하기 위해 자전거 경량화 및 지속적인 자전거 품질 개선 등의 조치가 필요할 것으로 보인다. 이외에도 ‘신속대여 어려움’이나 ‘임시거치 불편’ 등도 불편사항으로 꼽혔다. 따라서 이용자 편의를 위해서 향후 새로운 대책이 강구되어야 할 것이다.\n\n다른 공용자전거와의 비교에서는 공용자전거 A ～ E 중 A가 만족도는 4.2점으로 가장 높았으며, 인지도는 3.7점으로 2위를 차지하였다.'}
hist={q['id']:q for q in r.read(r.PREP/'previously-scored295.json')['questions']};assess=[dict(id=i,historicalScorePreserved=hist[i]['scoreBeforeFix'],currentBeforeScore=4,historicalEvidence=hist[i]['evidence'],assessment={39:'1023개비공집합실제불량후보를검사해1,5,7유일,네분류지표모두일치.원문보기와1/2분수를본문으로옮기고해설공백정리.',4:'양끝포함일수·최대연도·동시40일·2015동일종료일을검증.작은보기이미지를원문본문으로복원하고포함규칙어절정리.',1:'보고서상하위순서와기타제외조건,83.33%,만족/인지순위를전부대조했다.긴보고서본문을원문그대로읽기쉽게옮긴다.'}[q['number']],notReplacementOfHistoricalScore=True) for i,q in old.items()]
if (b/'related295-assessment-before.json').exists():assert r.read(b/'related295-assessment-before.json')==assess
else:r.write(b/'related295-assessment-before.json',assess)
reg={x['newAsset']:x for x in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/native-image-repairs.json')['figures']};norm=lambda s:re.sub(r'\s','',unicodedata.normalize('NFKC',s.replace('ㆍ','·')))
changes=r.read(r.OUT/'changes-batch39.json');checks=[]
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  if q['id'] not in old:continue
  prev=old[q['id']];observed=copy.deepcopy(q);q.clear();q.update(copy.deepcopy(prev));n=q['number'];index=0 if n==1 else len(q['figures'])-1;record=reg[q['figures'][index]['asset']]
  with pdfplumber.open(r.ROOT/record['source']) as pdf:raw=pdf.pages[record['page1based']-1].crop(record['rect']).extract_text()
  transformed=raw
  if n==39:
   assert '\n1\nㄴ.' in raw and '\n2\nㄷ.' in raw;transformed=raw.replace('\n1\nㄴ.','\nㄴ.').replace('정확도’는 이다.\n2\n','정확도’는 1/2이다.\n')
  assert norm(transformed)==norm(bodies[n]),(n,raw,bodies[n])
  snap=r.OUT/f"before-changes/{q['id']}-r{q['revision']}.json"
  if snap.exists():assert r.read(snap)==prev
  else:r.write(snap,prev)
  q['body']=bodies[n];q['figures']=[f for j,f in enumerate(q['figures']) if j!=index]
  if n==1:q['bodyAfterFigureCount']=0
  if n==39:q['steps']=[s.replace('교집합{','교집합 {') for s in q['steps']];q['optionReasons']=[s.replace('정확도는(','정확도는 (') for s in q['optionReasons']]
  if n==4:q['steps']=[s.replace('이번의−','이번의 −') for s in q['steps']]
  fields=sorted(k for k in q.keys()|prev.keys() if q.get(k)!=prev.get(k));assert fields;q['revision']+=1;touched=True
  assert observed==prev or observed==q,'Resume only an identical previously applied repair'
  assert q['answer']==prev['answer'] and q['choices']==prev['choices']
  changes.append(dict(id=q['id'],file=p.relative_to(r.ROOT).as_posix(),oldRevision=prev['revision'],newRevision=q['revision'],changedFields=fields,beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),cohort='prior295',reason='Direct original/key/finite models; native prose with fraction/report order preserved; old assets retained.',status='repaired_pending_reverification'))
  checks.append(dict(id=q['id'],source=record['source'],page=record['page1based'],rawProse=raw,nativeProseMatchesIgnoringWhitespace=True,fraction1over2Recovered=n==39))
 if touched:r.write(p,data)
r.write(r.OUT/'changes-batch39.json',changes)
assert r.sha(b/'related295-own-solves.json')==r.read(b/'related295-solve-frozen.json')['sha256']
r.write(b/'related295-repair-model-checks.json',dict(status='PASS',checks=checks,classifierCandidatesTested=1023,classifierUniqueTruth=solutions,classifierDAccuracy='6/10=3/5',rain='Inclusive dates;2017Jul1,2015bothJul29;only2013both>=40',bike='Lower-order shopping5.68<work6.98, inconvenience breakdown19.36>connectivity13.89; time83.33%, A satisfaction1st/awareness2nd.',originalAssetsAndHistoricalScoresPreserved=True))
print('3 prior295 repairs; native/finite/temporal models PASS')
