import re
from PIL import Image
import review_remaining605 as r
b=r.folder(44);old={x['question']['id']:x['question'] for x in r.read(b/'revealed-current.json')};related={q['id']:q for q in r.read(b/'related295-before.json')};src={x['id']:x for x in r.read(b/'blind-source.json')}
for name in ['source-key-checks.json','related295-source-key-checks.json','exact-model-checks.json']:assert r.read(b/name)['status']=='PASS'
for name in ['host-before.log','related295-host-before.log']:assert 'All tests passed!' in (b/name).read_text(encoding='utf-8-sig')
notes={28:'밤당일까지포함한560g손실/210일과남은65일검산정확.분수포함긴이미지본문을원문그대로네이티브로옮겨기본읽기크기개선.',29:'999의가능성과9/99배제로최소성증명정확.원문줄바꿈에서분리된달라지는지를연결.',30:'각팀6명및교차분류실현예시정확.모든이동을재계산해조건성립확인,발견없음.',32:'문자합집합및o와짝p유일성을전글자쌍열거로검증.영단어6개목록과주변문단경계를명확히분리.',33:'120배치중2개만가능하고A/C교환돼도합7유일.이상조건과파워0통과경계정확,발견없음.',34:'층배치전수검산으로戊2만유일,다른네명복수값및실제배치반례정확.발견없음.',35:'종료전네회25이상및마지막25미만,홀짝/3배수/서로다른탈락수전수검증정확.발견없음.',36:'별표5개후보/결격7초과/접근성다음경관순서정확.긴선정기준을본문으로분리하고체력소모도와/경관은/경관이조사오류수정.',37:'200원=.2천원,초과량하한0,E포함서비스와C최저130정확.표원형보존하며추가요금/상황긴조건을네이티브로분리.',38:'최저제외는예선만,최종6점수와면접합동점기준정확.채용후보자괄호앞어절공백정리.'}
fix={28,29,32,36,37,38};ratings=[dict(id=i,scoreBeforeFix=4 if q['number'] in fix else 5,assessment=notes[q['number']],needsChange=q['number'] in fix,deduction='읽기크기/문단/어절/조사' if q['number'] in fix else '발견없음') for i,q in old.items()]
assert not (b/'ratings-before.json').exists();r.write(b/'ratings-before.json',dict(method='Original-only solves frozen before reveal; exact models, source/key/pixels and pre-edit host reviewed.',ratings=ratings));r.write(b/'ratings-frozen.json',dict(frozenAt=r.now(),ratingsSha256=r.sha(b/'ratings-before.json'),total=44,count=10,beforeChanges=True))
hist={x['id']:x for x in r.read(r.PREP/'previously-scored295.json')['questions']}
r.write(b/'related295-assessment-before.json',[dict(id=i,historicalScorePreserved=hist[i],currentBeforeScore=4 if q['number']==11 else 5,assessment='하한/반례및전수어획배치정확.제목잡고1위인띄어쓰기정리.' if q['number']==11 else '홀짝과세잔량별가능AB일수전수검산정확.발견없음.',notReplacementOfHistoricalScore=True,changed=q['number']==11) for i,q in related.items()])
body28='개미는 매일 6g의 먹이를 먹는다. 1년(365일) 중 마지막 90일은 개미의 겨울이라서 이 기간에는 먹이를 구할 수 없다. 따라서 개미는 겨울을 제외한 기간에는 매일 아침 10g의 먹이를 수집하여 6g을 먹고, 남은 4g을 즉시 비축한다. 그런데 어느 날 밤 홍수가 나서, 그때까지 개미가 비축한 먹이 중 2/3가 휩쓸려 사라졌다. 그럼에도 개미는 이전과 같이 먹이 수집과 비축을 계속하여, 모자라거나 남는 먹이 없이 겨울을 무사히 보낼 수 있었다.'
body36='○ △△산악회가 산을 선택하는 기준은 다음과 같다.\n\n－ 최종점수가 가장 높은 산을 선택하며, 최종점수는 아래와 같이 산정한다. 단, 체력소모도 점수와 위험도 점수의 합이 7을 초과하면 선택하지 않는다.\n\n최종점수＝2×(경관 점수＋접근성 점수)－(체력소모도 점수＋위험도 점수)\n\n－ 최종점수가 동점일 경우, 접근성, 경관, 위험도의 순서대로 해당 항목의 점수를 비교하여 선호도가 높은 산을 선택한다.'
body37='○ 데이터 제공량을 초과하여 사용하는 경우, 추가로 사용한 데이터 1GB당 200원의 추가 요금이 발생한다.\n\n○ OTT 콘텐츠를 구독하는 경우, 월 2만 원의 추가요금이 부과된다. 단, E통신사의 기본요금에는 OTT 콘텐츠 구독료가 포함되어 있다.\n\n<상 황>\n\n甲은 월 요금 총액이 가장 저렴할 것으로 예상되는 통신사를 2월에 이용하려고 한다. 다만 甲은 데이터 전송 속도가 200Mbps 미만인 통신사는 이용하지 않는다. 甲의 1월 데이터 사용량은 400GB이고, 2월에도 같은 양의 데이터를 사용하려 한다. 그리고 1월까지 구독하지 않았던 OTT 콘텐츠를 구독하려 한다.'
norm=lambda s:re.sub(r'\s','',s);changes=[];crops=[]
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  is_related=q['id'] in related
  if not((q['id'] in old and q['number'] in fix) or (is_related and q['number']==11)):continue
  prev=(related if is_related else old)[q['id']];assert q==prev;n=q['number'];snap=r.OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();r.write(snap,prev)
  if is_related:q['title']=q['title'].replace('잡고1위인','잡고 1위인');reason='제목의수사앞어절공백복원;내용/정답/해설불변.'
  else:
   reason=notes[n]
   if n==28:
    raw=src[q['id']]['sourceText'];part=raw[raw.index('개미는 매일'):raw.index('①')]
    part=part.replace('2\n가 휩쓸려 사라졌다. 그럼에도 개미는 이전과 같이 먹이\n3','2/3가 휩쓸려 사라졌다. 그럼에도 개미는 이전과 같이 먹이')
    assert norm(part)==norm(body28);q['body']=body28;q['figures']=[]
   if n==29:q['body']=q['body'].replace('달라 지는지를','달라지는지를')
   if n==32:q['body']=q['body'].replace('송신하였다. apple','송신하였다.\n\napple').replace('peach 6개의','peach\n\n6개의')
   if n in [36,37]:
    original=q['figures'][0]['asset'];box=(0,0,1320,824 if n==36 else 712);asset=f'assets/psat/figures/2025grade5-s{n}-table-review605.png';assert not (r.ROOT/asset).exists()
    with Image.open(r.ROOT/original) as im:cropped=im.crop(box);cropped.save(r.ROOT/asset);size=cropped.size
    q['figures']=[dict(asset=asset,caption='등산 후보지 별점·범례 원본 표' if n==36 else '데이터 제공량·전송 속도·기본요금 원본 표',width=size[0],height=size[1])];q['figuresAfterBody']=False;q['body']=body36 if n==36 else body37
    raw=src[q['id']]['sourceText'];marker='○ △△산악회가 산을 선택하는' if n==36 else '○ 데이터 제공량을 초과하여';part=raw[raw.index(marker):raw.index('①')];assert norm(part)==norm(q['body'])
    with Image.open(r.ROOT/asset) as new,Image.open(r.ROOT/original) as im:assert new.tobytes()==im.crop(box).tobytes()
    crops.append(dict(id=q['id'],originalAsset=original,newAsset=asset,pixelBoxWithinOriginal=list(box),source=src[q['id']]['source'],page=src[q['id']]['page'],sourceProseExactIgnoringWhitespace=True,sourceGeometryUnchanged=True,oldAssetPreserved=True))
   if n==36:
    for field in ['steps','optionReasons']:q[field]=[s.replace('체력 소모도 과 위험','체력소모도와 위험').replace('경관는','경관은').replace('경관가','경관이') for s in q[field]]
   if n==38:q['body']=q['body'].replace('채용후보자 (A','채용후보자(A')
  assert q!=prev and q['answer']==prev['answer'] and q['choices']==prev['choices'];fields=sorted(k for k in q if q[k]!=prev.get(k));q['revision']+=1;touched=True
  changes.append(dict(id=q['id'],file=p.relative_to(r.ROOT).as_posix(),oldRevision=prev['revision'],newRevision=q['revision'],changedFields=fields,beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason=reason,status='repaired_pending_reverification'))
 if touched:r.write(p,data)
assert len(changes)==7;r.write(r.OUT/'changes-batch44.json',changes)
r.write(b/'repair-semantic-checks.json',dict(status='PASS',targetCount=6,relatedCount=1,crops=crops,sourceFraction='28 original stacked2/3 transcribed as2/3; all remaining source prose exact ignoring whitespace.',allAnswersChoicesUnchanged=True))
print('Frozen44/50;6target repairs and1related title;all original assets retained')
