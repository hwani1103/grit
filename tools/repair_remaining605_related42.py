import re,unicodedata
from fractions import Fraction as F
from itertools import combinations
import pdfplumber
import review_remaining605 as r
b=r.folder(42);old={q['id']:q for q in r.read(b/'related295-before.json')}
assert 'All tests passed!' in (b/'related295-host-before.log').read_text(encoding='utf-8-sig') and r.read(b/'related295-source-native-pixel-checks.json')['status']=='PASS'
assert [F('24.2')-F('23.8'),F('22')-F('21.1'),F('21.9')-F('20.3'),F('20.6')-F('19.2')]==list(map(F,['.4','.9','1.6','1.4']))
assert all(a<c for a,c in zip([20.6,14.2,19.2,14.6],[21.9,14.8,20.3,14.9]))
assert 13827*F('.1915')/F('.2505')>10000 and 4610*F('.1935')>F('1.5')*4160*F('.1415')
pred=[{1,3,4,7,8,9},{1,2,5,7,8,9,10},{1,4,5,7,10},{1,2,5,6,8}];precision=[F(1,3),F(3,7),F(3,5),F(2,5)];recall=[F(2,3),F(1),F(1),F(2,3)]
valid=[]
for k in range(1,11):
 for tup in combinations(range(1,11),k):
  actual=set(tup)
  if all(F(len(p&actual),len(p))==pr and F(len(p&actual),len(actual))==re for p,pr,re in zip(pred,precision,recall)):valid.append(tup)
assert valid==[(1,5,7)]
actual=set(valid[0]);confusion=[dict(TB=len(p&actual),FB=len(p-actual),FG=len(actual-p),TG=len(set(range(1,11))-p-actual)) for p in pred]
assert confusion[0]['FB']==4 and confusion[3]==dict(TB=2,FB=3,FG=1,TG=4)
hist={q['id']:q for q in r.read(r.PREP/'previously-scored295.json')['questions']}
assert not (b/'related295-assessment-before.json').exists()
r.write(b/'related295-assessment-before.json',[dict(id=i,historicalScorePreserved=hist[i]['scoreBeforeFix'],currentBeforeScore=4 if q['number']==21 else 5,assessment='각집단분모·2024차감소·정수아닌예상인원·반올림양끝검산;작은보기본문전환.' if q['number']==21 else '1023비어있지않은실제불량부분집합을모두열거해1,5,7유일성확인.네칸과분모·전체10검산;기존본문·해설유지.',notReplacementOfHistoricalScore=True) for i,q in old.items()])
body='<보기>\n\nㄱ. 2021년 이후 남자 중학생과 여자 중학생의 과일섭취율 차이는 매년 증가하였다.\n\nㄴ. 2024년 과일섭취율은 남자 중학생, 남자 고등학생, 여자 중학생, 여자 고등학생 모두 2023년보다 감소하였다.\n\nㄷ. 2020년과 2024년의 여자 중학생 과일섭취자 수가 같다면, 2020년 여자 중학생 조사대상자 수는 10,000명 이하이다.\n\nㄹ. 2024년 과일섭취자 수는 2학년 여자 중학생이 2학년 남자 고등학생의 1.5배 이상이다.'
reg={x['newAsset']:x for x in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/native-image-repairs.json')['figures']};changes=r.read(r.OUT/'changes-batch42.json')
norm=lambda s:re.sub(r'\s','',unicodedata.normalize('NFKC',s))
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  if q['id'] not in old or q['number']!=21:continue
  prev=old[q['id']];assert q==prev;rec=reg[q['figures'][-1]['asset']]
  with pdfplumber.open(r.ROOT/rec['source']) as pdf:raw=pdf.pages[rec['page1based']-1].crop(rec['rect']).extract_text()
  assert norm(raw)==norm(body)
  snap=r.OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();r.write(snap,prev)
  q['body']=body;q['figures']=q['figures'][:-1];q['revision']+=1;touched=True
  changes.append(dict(id=q['id'],file=p.relative_to(r.ROOT).as_posix(),oldRevision=prev['revision'],newRevision=q['revision'],changedFields=['body','figures'],beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason='원문보기본문전환;비율분모/모든선지와반올림경계검산.',cohort='prior295',status='repaired_pending_reverification'))
 if touched:r.write(p,data)
assert len(changes)==8;r.write(r.OUT/'changes-batch42.json',changes)
r.write(b/'related295-repair-model-checks.json',dict(status='PASS',count=2,source='related295-source-native-pixel-checks.json',fruitRoundingBounds=dict(equalEatersMin2020Sample=float(13827*F('.1915')/F('.2505')),femaleGrade2Lower=float(4610*F('.1935')),maleGrade2Times1_5Upper=float(F('1.5')*4160*F('.1415'))),uniqueActualDefects=valid,confusion=confusion,nativeProseExact=True,oldScoresAssetsAnswersPreserved=True,changedCount=1,unchangedCount=1))
print('2 related rechecks;1 native prose repair;1023 classifier worlds/fruit interval models PASS')
