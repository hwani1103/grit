import re,pdfplumber
from PIL import Image
import review_remaining605 as r
b=r.folder(59);old={x['question']['id']:x['question'] for x in r.read(b/'revealed-current.json')};related={q['id']:q for q in r.read(b/'related295-before.json')}
for n in ['host-before.log','related295-host-before.log']:assert 'All tests passed!' in (b/n).read_text(encoding='utf-8-sig')
for n in ['source-key-checks.json','related295-source-key-checks.json','pre-reveal-exact-models.json','related295-pre-reveal-models.json']:assert r.read(b/n)['status']=='PASS'
notes={15:'법조계/여성 최소와 예술계 최대의 교집합, 순서 없는 4쌍 소진 정확.',16:'서로 다른 네 품목/중복 한 개/필수 매장과 실제 20만원 배분 정확.',18:'95분 주행 상한과 피로도 선택/왕복 시간 정확. 이미지의 긴 요금·식사 조건이 기본 화면에서 작아 원문 표와 주석은 유지하고 조건을 네이티브 본문으로 분리.',21:'정가 기준 이중 상한과 예외 대상 정확. 해설의 항 번호를 선택지 번호와 혼동하지 않도록 제3항·제4항 등으로 표기.',22:'관할청/동의 예외와 사후 통보/재량과 의무 정확. 제3항 인용과 중간점 뒤 불필요 공백 개선.',24:'기준일/6개월/독립 결격과 임기 중 확정 정확. ③제 4호를 제3항제4호로 명확화하고 줄바꿈 유래 동대표자 공백 제거.',25:'심판 인용과 취소소송 인용 대상/기각 연쇄와 기간 정확. 특허 무효심판의 원문 줄바꿈 유래 공백 제거.',26:'9·7·14·14정/캡슐과10정 조건 교집합/총19920 정확.',27:'양의100원 단위 두 잔여 분할/동일가격 불가능/최대최소25배 정확.',29:'승점3+1과2+2 양쪽 극값 및 실제 종결 점수, 전체108·45 정확.'}
fix={18,21,22,24,25};ratings=[dict(id=i,scoreBeforeFix=3 if q['number']==18 else 4 if q['number'] in fix else 5,assessment=notes[q['number']],needsChange=q['number'] in fix) for i,q in old.items()]
assert not (b/'ratings-before.json').exists();r.write(b/'ratings-before.json',dict(method='Original own10 frozen before reveal, all source pages/5options/exact models/current host reviewed.',ratings=ratings));r.write(b/'ratings-frozen.json',dict(frozenAt=r.now(),ratingsSha256=r.sha(b/'ratings-before.json'),total=44,count=10,beforeChanges=True))
hist={x['id']:x for x in r.read(r.PREP/'previously-scored295.json')['questions']};r.write(b/'related295-assessment-before.json',[dict(id=i,historicalScorePreserved=hist[i]['scoreBeforeFix'],currentBeforeScore=5,assessment={5:'세 정수해 소진과 실제 경계4·6 정확.',13:'착수금 상한과 등록 사례금 구별/차123만원/표의 본문 삽입 위치 정확.',18:'재적→출석→찬성 올림/서면 출석/성별 엄격 경계와 실제6명 구성 정확.'}[q['number']],notReplacementOfHistoricalScore=True,changed=False) for i,q in related.items()])
tail='○ 甲사무관은 통행요금이 5,000원을 넘으면 해당 경로를 이용하지 않으며, 통행요금이 5,000원을 넘지 않으면 피로가 가장 덜한 경로를 선택한다.\n\n○ 甲사무관은 B연구소 주차장에 도착한 후, 도보 10분 거리의 음식점으로 걸어가 점심식사(30분 소요)를 마치고 다시 주차장까지 걸어온 뒤, 주차장에서 5분 걸려 회의 장소에 도착할 예정이다.'
norm=lambda s:re.sub(r'\s','',s)
src=next(x for x in r.read(b/'blind-source.json') if x['originalNumber']==18)
with pdfplumber.open(r.ROOT/src['source']) as pdf:
 page=pdf.pages[src['page']-1];full=page.crop((390,230,722,518)).extract_text();table=page.crop((390,230,722,378)).extract_text();assert norm(full)==norm(table+tail)
changes=[];crops=[]
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  if q['id'] not in old or q['number'] not in fix:continue
  prev=old[q['id']];assert q==prev;n=q['number'];snap=r.OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();r.write(snap,prev)
  if n==18:
   asset='assets/psat/figures/2023grade5-s18-route-table-review605.png';source=q['figures'][0]['asset'];assert not (r.ROOT/asset).exists()
   with Image.open(r.ROOT/source) as im:im.crop((0,0,1328,592)).save(r.ROOT/asset)
   q['bodyBeforeFigures']=q['body'];q['body']=tail;q['bodyAfterFigureCount']=1;q['figures']=[dict(asset=asset,width=1328,height=592,caption='경로별 거리·시간·통행요금·피로도 원본 표와 주석')]
   crops.append(dict(id=q['id'],oldAsset=source,newAsset=asset,pixelBoxWithinOriginal=[0,0,1328,592],sourcePDFBox=[390,230,722,378],allTableAndFootnotePreserved=True,oldAssetPreserved=True))
  if n==21:
   for f in ['steps','optionReasons']:q[f]=[s.replace('③·④항','제3항·제4항').replace('⑥항','제6항').replace('①항','제1항') for s in q[f]]
  if n==22:q['steps']=[s.replace('건강검사 등 ③항','건강검사 등 제3항') for s in q['steps']];q['body']=q['body'].replace('산업대학· 교육대학','산업대학·교육대학')
  if n==24:q['steps']=[s.replace('③제 4호','제3항제4호').replace('임기 중 ④의','임기 중 제4항의') for s in q['steps']];q['choices']=[s.replace('A동 대표자','A동대표자').replace('B동 대표자','B동대표자') for s in q['choices']]
  if n==25:q['body']=q['body'].replace('특허 무효심판','특허무효심판')
  assert q['answer']==prev['answer'] and norm(''.join(q['choices']))==norm(''.join(prev['choices']))
  if n!=18:assert norm(q['body'])==norm(prev['body']) and q['figures']==prev['figures']
  fields=sorted(k for k in q if q[k]!=prev.get(k));q['revision']+=1;touched=True;changes.append(dict(id=q['id'],file=p.relative_to(r.ROOT).as_posix(),oldRevision=prev['revision'],newRevision=q['revision'],changedFields=fields,beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason=notes[n],status='repaired_pending_reverification'))
 if touched:r.write(p,data)
assert len(changes)==5;r.write(r.OUT/'changes-batch59.json',changes)
r.write(b/'repair-semantic-checks.json',dict(status='PASS',targetChanged=5,relatedChanged=0,crops=crops,allAnswersUnchanged=True,sourceTextPreserved=True,scoreModel='pre-reveal-exact-models.json',relatedModels='related295-pre-reveal-models.json'))
r.write(b/'after-sample.json',dict(sample=[dict(id=i) for i in list(old)+list(related)]))
p=r.ROOT/'test/psat_remaining605_prefix_order_test.dart';s=p.read_text(encoding='utf-8');s=s.replace("      'kr-mpm-2024-03-02-psat-d-39',","      'kr-mpm-2024-03-02-psat-d-39',\n      'kr-mpm-2023-03-04-psat-s-18',")
s=s.replace("for (final n in [13, 25, 37]) {\n      final q = catalog.questions['kr-mpm-2024-03-02-psat-s-$n']!;","for (final id in ['kr-mpm-2024-03-02-psat-s-13', 'kr-mpm-2024-03-02-psat-s-25', 'kr-mpm-2024-03-02-psat-s-37', 'kr-mpm-2023-03-04-psat-s-18']) {\n      final q = catalog.questions[id]!;\n      final n = q.number;")
p.write_text(s,encoding='utf-8');print('44/50 frozen;5 repairs,3 related unchanged')
