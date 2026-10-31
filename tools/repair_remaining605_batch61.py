import re
from PIL import Image
import review_remaining605 as r
b=r.folder(61);old={x['question']['id']:x['question'] for x in r.read(b/'revealed-current.json')}
assert 'All tests passed!' in (b/'host-before.log').read_text(encoding='utf-8-sig')
assert r.read(b/'source-key-checks.json')['status']=='PASS'
notes={'l-33':'충돌 발언으로 유일 거짓을 확정하고 을의 비환경부 반례를 구성. 가능한4개 범주 배치 전수와 일치.', 'l-34':'전칭과 두 존재 증인의 분리/대우/공집합 가능성까지 정확.', 's-30':'곱의24/25 배율과 오차1/25 역산 정확. 긴 원문 이미지의 작은 글씨를 네이티브 본문으로 전환하고 곱 공식 원형은 별도 이미지로 보존.', 's-32':'대칭수 유일성/총상한/연도별 실현 예시 정확.', 'd-36':'다섯 그래프의 값·분모 검증 정확. 증감폭 부호 해석에 의존하지 않는 두 증가업종의 수치 교환을 확정 근거로 제시.'}
ratings=[dict(id=i,scoreBeforeFix=3 if i.endswith('s-30') else 5,assessment=notes[i[-4:]],needsChange=i.endswith('s-30')) for i in old]
if (b/'ratings-before.json').exists():
 assert r.read(b/'ratings-before.json')['ratings']==ratings and r.sha(b/'ratings-before.json')==r.read(b/'ratings-frozen.json')['ratingsSha256']
else:
 r.write(b/'ratings-before.json',dict(method='All5 original regions and own models/current5-stage explanations/options and host starts reviewed.',ratings=ratings));r.write(b/'ratings-frozen.json',dict(frozenAt=r.now(),ratingsSha256=r.sha(b/'ratings-before.json'),total=23,count=5,beforeChanges=True))
correction=dict(id='kr-mpm-2023-03-04-psat-d-36',issue='Own solve treated positive depiction of decreases as sufficient error under 증감폭. That term can denote magnitude; use the unambiguous online-advertising/information-industry swapped1717/1988, independently calculated before reveal, as decisive proof.',answerUnchanged=2,publishedExplanationAlreadyCorrect=True,originalOwnSolvePreserved=True,correctedAfterReveal=True)
r.write(b/'post-reveal-reasoning-correction.json',correction);progress=r.read(r.OUT/'progress.json');progress['postRevealReasoningCorrections'][correction['id']]='batch61/post-reveal-reasoning-correction.json';r.write(r.OUT/'progress.json',progress)
prefix='甲, 乙, 丙은 함께 밭을 일구었다. 이들은 하루 동안 한 일의 양을 산정하기 위해 다음과 같은 ‘일 지수’를 만들었다.'
tail='甲은 3월 3일의 일 지수를 계산할 때, 자신이 실제로 한 일의 양의 1/5을 늘려서 계산했다. 甲은 계산된 일 지수가 잘못된 것을 깨닫고, 앞에서 계산했던 방식에서 乙이 한 일의 양의 1/5을 줄이고 그 외는 동일하게 계산했다. 甲이 이렇게 계산한 이유는 자신이 실제로 한 일과 乙이 실제로 한 일의 양이 같았기 때문이다. 하지만 이렇게 계산한 일 지수는 옳게 계산한 일 지수보다 3이 작았다.'
source=next(x for x in r.read(b/'blind-source.json') if x['id'].endswith('s-30'))['sourceText']
def norm(s):return re.sub(r'\s','',s).replace('＝','=')
raw=source[source.index('甲,'):source.index('①')];raw=re.sub(r'\s*\s*양의\s*을\s*늘려서\s*계산했다[.]\s*甲은\s*계산된\s*일\s*지수가\s*잘못된\s*\s*', '양의1/5을 늘려서 계산했다. 甲은 계산된 일 지수가 잘못된',raw)
raw=re.sub(r'\s*을\s*줄이고\s*그\s*외는\s*동일하게\s*계산했다[.]\s*甲이\s*이렇게\s*계산한\s*\s*','1/5을 줄이고 그 외는 동일하게 계산했다. 甲이 이렇게 계산한',raw)
assert norm(raw)==norm(prefix+'일 지수＝[甲이 한 일의 양]×[乙이 한 일의 양]×[丙이 한 일의 양]'+tail),(norm(raw),norm(prefix+tail))
changes=[]
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  if q['id']!='kr-mpm-2023-03-04-psat-s-30':continue
  prev=old[q['id']];assert q==prev;snap=r.OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();r.write(snap,prev)
  asset='assets/psat/figures/2023grade5-s30-formula-review605.png';assert not (r.ROOT/asset).exists()
  with Image.open(r.ROOT/q['figures'][0]['asset']) as im:im.crop((0,180,1328,280)).save(r.ROOT/asset)
  q['bodyBeforeFigures']=prefix;q['body']=tail;q['bodyAfterFigureCount']=1;q['figures']=[dict(asset=asset,width=1328,height=100,caption='일 지수 정의 원본 수식')]
  fields=[k for k in q if q[k]!=prev.get(k)];q['revision']+=1;touched=True;changes.append(dict(id=q['id'],file=p.relative_to(r.ROOT).as_posix(),oldRevision=prev['revision'],newRevision=q['revision'],changedFields=fields,beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason=notes['s-30'],status='repaired_pending_reverification'))
 if touched:r.write(p,data)
r.write(r.OUT/'changes-batch61.json',changes);r.write(b/'after-sample.json',dict(sample=[dict(id=i) for i in old]))
r.write(b/'repair-semantic-checks.json',dict(status='PASS',targetChanged=1,allAnswersUnchanged=True,sourceTextEquality='Only two visually checked1/5 fraction extraction-order substitutions; entire native prefix+formula+tail matches original.',crop=dict(oldAsset=old['kr-mpm-2023-03-04-psat-s-30']['figures'][0]['asset'],newAsset=asset,pixelBoxWithinOriginal=[0,180,1328,280],sourcePDFBox=[390,139,722,164],oldAssetPreserved=True)))
p=r.ROOT/'test/psat_remaining605_prefix_order_test.dart';s=p.read_text(encoding='utf-8');s=s.replace("      'kr-mpm-2023-03-04-psat-s-18',","      'kr-mpm-2023-03-04-psat-s-18',\n      'kr-mpm-2023-03-04-psat-s-30',").replace("'kr-mpm-2023-03-04-psat-s-18'])", "'kr-mpm-2023-03-04-psat-s-18', 'kr-mpm-2023-03-04-psat-s-30'])");p.write_text(s,encoding='utf-8')
print('23/25 frozen; source30 native prefix/formula/native tail; original asset kept')
