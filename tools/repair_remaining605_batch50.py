import re,shutil
from PIL import Image
import review_remaining605 as r
b=r.folder(50);old={x['question']['id']:x['question'] for x in r.read(b/'revealed-current.json')};related={q['id']:q for q in r.read(b/'related295-before.json')}
for n in ['source-key-checks.json','related295-source-key-checks.json','exact-model-checks.json']:assert r.read(b/n)['status']=='PASS'
for n in ['host-before.log','related295-host-before.log']:assert 'All tests passed!' in (b/n).read_text(encoding='utf-8-sig')
notes={12:'정수해 전수열거의 유일905만원과 각 선지별 최고값/손실 상한 증명 일치. 발견없음.',14:'전체 유효일정4개와丙3~4일, 양끝 실현/전역 한계 정확. 발견없음.',16:'A280/C270/B최대270 및A중등급0또는2, 동점최대2개 정확. 발견없음.',17:'점수18/18/17/18, 초급제외와 실제13건 타이브레이크 및 경계 포함 정확. 표 원형 및 확대 확인, 발견없음.',18:'기준일과 경영주등록/직접영농/예정자, 연령만 병역차감 정확. 발견없음.',19:'분자/분모와 세 효과의 구분 정확. 공통지문의 관광사업자 어절 연결 및 간접/유발 문단 분리.',20:'일반2.5/비율5와 직접10억 역대입 정확. 공통19와 동일한 어절 및 문단 개선.',21:'18세 고교생포함, 벌금가능/상한, 등록주체/직권말소/판매자/1000명 조건 정확. 발견없음.',23:'두 등록부/기관/선후와 변경1개월 정확. 국제선박등록부 어절 연결.',25:'최초/반복/예외/명령/강제금 상한250 및4년 반례 정확. 표를제2항 뒤 원문 위치에 배치하고 수산동식물/어장규모 어절 연결.'}
fix={19,20,23,25};ratings=[dict(id=i,scoreBeforeFix=4 if q['number'] in fix else 5,assessment=notes[q['number']],needsChange=q['number'] in fix) for i,q in old.items()]
assert not (b/'ratings-before.json').exists();r.write(b/'ratings-before.json',dict(method='Original-only solves frozen before reveal; exact models and original/native/key/pixels/host pre-edit assessment.',ratings=ratings));r.write(b/'ratings-frozen.json',dict(frozenAt=r.now(),ratingsSha256=r.sha(b/'ratings-before.json'),total=46,count=10,beforeChanges=True))
hist={x['id']:x for x in r.read(r.PREP/'previously-scored295.json')['questions']}
r.write(b/'related295-assessment-before.json',[dict(id=i,historicalScorePreserved=hist[i]['scoreBeforeFix'],currentBeforeScore=4,assessment='부분순서와 호칭 성별/나이반례 정확. 작은 이미지의 나이인지규칙을 네이티브로 옮기고 표/대화 순서 유지.' if q['number']==13 else '7개 술어128상태와 각 선지 반례 정확. 원문 밑줄은 전제까지로 를 제외.',notReplacementOfHistoricalScore=True,changed=True) for i,q in related.items()])
norm=lambda s:re.sub(r'\s','',s);changes=[];crops=[]
prefix='A마을에 사는 5명(甲～戊)은 서로 나이가 다르다. 이들은 자신보다 연상인 사람의 나이는 모르지만, 연하인 사람의 나이는 알고 있다.\n\nA마을 사람들은 연상인 사람에 대해서는 아래 표에 따라 칭하는 말을 붙인다.'
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  ir=q['id'] in related
  if not(ir or (q['id'] in old and q['number'] in fix)):continue
  prev=(related if ir else old)[q['id']];assert q==prev;n=q['number'];snap=r.OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();r.write(snap,prev)
  if ir and n==16:
   assert q['underlines']==['두 개의 전제를'];q['underlines']=['두 개의 전제'];assert q['body'].count('두 개의 전제를')==1;reason='원문 선끝은 전제까지; 를은 본문에 유지하고 밑줄에서 제외.'
  elif ir:
   source=prev['figures'][0]['asset'];asset='assets/psat/figures/2024grade5-s13-table-review605.png';box=(0,372,1328,704)
   assert not (r.ROOT/asset).exists()
   with Image.open(r.ROOT/source) as im:im.crop(box).save(r.ROOT/asset)
   q['figures']=[dict(asset=asset,width=1328,height=332,caption='성별 호칭 원본 표')];q['bodyBeforeFigures']=prefix
   sourceRow=next(x for x in r.read(b/'related295-source.json') if x['id']==q['id']);part=sourceRow['sourceText'].split('칭하는 대상')[0].split('옳은 것은?')[1];assert norm(part)==norm(prefix)
   crops.append(dict(id=q['id'],originalAsset=source,newAsset=asset,pixelBoxWithinOriginal=list(box),sourceProseExactIgnoringWhitespace=True,oldAssetPreserved=True));reason='나이 인지 규칙을 기본 글꼴 본문으로 표시하고 원본 호칭표와 대화의 순서 유지.'
  else:
   reason=notes[n]
   if n in [19,20]:q['body']=q['body'].replace('관광 사업자','관광사업자').replace('간접효과이다. 직접효과와','간접효과이다.\n\n직접효과와')
   if n==23:q['body']=q['body'].replace('국제선박 등록부','국제선박등록부')
   if n==25:
    text=q['body'].replace('수산 동식물','수산동식물').replace('어장 규모','어장규모');cut=text.index('③ 제1항에도')
    q['bodyBeforeFigures']=text[:cut].rstrip();q['body']=text[cut:];q['figuresAfterBody']=False
   assert norm(q.get('bodyBeforeFigures','')+q['body'])==norm(prev['body'])
  assert q['answer']==prev['answer'] and q['choices']==prev['choices'] and q['steps']==prev['steps'] and q['optionReasons']==prev['optionReasons']
  fields=sorted(k for k in q if q[k]!=prev.get(k));q['revision']+=1;touched=True
  changes.append(dict(id=q['id'],file=p.relative_to(r.ROOT).as_posix(),oldRevision=prev['revision'],newRevision=q['revision'],changedFields=fields,beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason=reason,status='repaired_pending_reverification'))
 if touched:r.write(p,data)
assert len(changes)==6;r.write(r.OUT/'changes-batch50.json',changes)
r.write(b/'repair-semantic-checks.json',dict(status='PASS',targetChanged=4,relatedChanged=2,crops=crops,allAnswersChoicesStepsReasonsUnchanged=True,bodyCharactersPreserved=True,requiredRenderer='bodyBeforeFigures optional prefix; old snapshots lack the field and retain original order.',sourceUnderline='exact-model-checks.json'))
r.write(b/'after-sample.json',dict(sample=[dict(id=i) for i in list(old)+list(related)]))
source=r.ROOT/'lib/psat.dart';snap=b/'psat-before.dart';assert not snap.exists();shutil.copyfile(source,snap)
r.write(b/'reader-before.json',dict(file='lib/psat.dart',beforeSha256=r.sha(source),beforeSnapshot=snap.relative_to(r.ROOT).as_posix()))
print('Frozen46/50;4target+2related repairs; prefix reader support pending')
