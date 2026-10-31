import re,pdfplumber
from PIL import Image
import review_remaining605 as r
b=r.folder(53);old={x['question']['id']:x['question'] for x in r.read(b/'revealed-current.json')};related={q['id']:q for q in r.read(b/'related295-before.json')}
for n in ['host-before.log','related295-host-before.log']:assert 'All tests passed!' in (b/n).read_text(encoding='utf-8-sig')
for n in ['source-key-checks.json','related295-source-key-checks.json','exact-model-checks.json']:assert r.read(b/n)['status']=='PASS'
notes={26:'제조단계와온도/주로/지문밖추정불가대응정확.',28:'27배끝자리유일성과전체수검산/丙십자리정확.',29:'몰리의가격용적열등성으로대체가능증명/모든수량과어항하한정확.',30:'FIFO잔여금과월말만료/사용후적립정확. 날짜뒤조사에불필요한공백수정.',31:'분할집합배수와교집합고정/유일20및가능배치정확.',33:'지급일생일전후/20와35포함/3종숫자/홀수일정확.',34:'정답과5선지근거및경우표정확하나정석근거마지막문장은C5표사례를C항상4이상반례로붙여부적절. A/B선택C3표사례로교체.',36:'직전이현재제외인구간정의/3오답반례와ㄷ일반증명정확. 짧은도입포함원본표는확대지원유지.',37:'가격경계9억/천원단위/가점포함24.5정확. 긴가중치규칙과도입이이미지라기본화면과확대글자에서너무작음. 원본평가표만분리하고도입/규칙네이티브화.',38:'70점포함/참여기업별도제외/가중치와지원비율분리정확. 원본상황표주석보존.'}
fix={30,34,37};ratings=[dict(id=i,scoreBeforeFix=3 if q['number']==37 else 4 if q['number'] in fix else 5,assessment=notes[q['number']],needsChange=q['number'] in fix) for i,q in old.items()]
assert not (b/'ratings-before.json').exists();r.write(b/'ratings-before.json',dict(method='Source own10 frozen before current reveal; source/key/all options/exact enumeration and host checks.',ratings=ratings));r.write(b/'ratings-frozen.json',dict(frozenAt=r.now(),ratingsSha256=r.sha(b/'ratings-before.json'),total=46,count=10,beforeChanges=True))
hist={x['id']:x for x in r.read(r.PREP/'previously-scored295.json')['questions']}
r.write(b/'related295-assessment-before.json',[dict(id=i,historicalScorePreserved=hist[i]['scoreBeforeFix'],currentBeforeScore=5,assessment='직접풀이와공식키/5선지근거일치. 복권비율단계와단위공백현재정상; 달리기추월의시간조건과최종순서정확. 추가수정없음.',notReplacementOfHistoricalScore=True,changed=False) for i in related])
prefix='甲시는 전기차충전기 설치업체를 선정하려고 한다. 다음과 같은 <평가표>를 바탕으로 후보업체 5곳(A～E) 중 최종 점수가 가장 높은 곳을 선정한다.'
middle='○ 품질 점수에 대해서는 3배의 가중치를 부여하고 안전성 점수에 대해서는 2배의 가중치를 부여한 후, 항목별로 산출한 점수를 합하여 최종 점수를 산정한다. 단, 설치업체로 2회 이상 선정된 적이 있는 업체에 대해서는 2.5점의 가점을 부여하여 최종 점수를 산출한다.'
norm=lambda s:re.sub(r'\s','',s)
src=next(x for x in r.read(b/'blind-source.json') if x['originalNumber']==37)
with pdfplumber.open(r.ROOT/src['source']) as pdf:
 page=pdf.pages[src['page']-1];full=page.crop((26,73,358,469)).extract_text();table=page.crop((26,132,358,371)).extract_text();assert norm(full)==norm(prefix+table+middle)
changes=[];crops=[]
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  if q['id'] not in old or q['number'] not in fix:continue
  prev=old[q['id']];assert q==prev;n=q['number'];snap=r.OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();r.write(snap,prev)
  if n==30:
   for f in ['steps','optionReasons']:q[f]=[re.sub(r'(?<=\d[.]) (?=에|까지|과)', '',s) for s in q[f]]
  if n==34:
   a='C 선택이면 (3,2,5)이므로 C가 언제나 4표 이상 받는 것도 아니다.';assert a in q['steps'][3];q['steps'][3]=q['steps'][3].replace(a,'甲·乙이 A나 B를 선택하면 C는 3표이므로, C가 언제나 4표 이상 받는 것도 아니다.')
  if n==37:
   source=q['figures'][0]['asset'];asset='assets/psat/figures/2024grade5-s37-evaluation-review605.png';box=(0,236,1328,1192);assert not (r.ROOT/asset).exists()
   with Image.open(r.ROOT/source) as im:im.crop(box).save(r.ROOT/asset)
   q['figures'][0]=dict(asset=asset,width=1328,height=956,caption='평가항목·등급·점수 원본 표');q['bodyBeforeFigures']=prefix;q['body']=middle;q['bodyAfterFigureCount']=1
   crops.append(dict(id=q['id'],oldAsset=source,newAsset=asset,pixelBoxWithinOriginal=list(box),sourcePDFBox=[26,132,358,371],completeSourceProsePreserved=True,oldAssetPreserved=True,tableStrokesY=[152.528,366.690]))
  assert q['answer']==prev['answer'] and q['choices']==prev['choices']
  if n!=37:assert q['body']==prev['body'] and q['figures']==prev['figures']
  if n==30:
   for f in ['steps','optionReasons']:assert norm(''.join(q[f]))==norm(''.join(prev[f]))
  if n==34:assert q['optionReasons']==prev['optionReasons']
  if n==37:assert q['steps']==prev['steps'] and q['optionReasons']==prev['optionReasons']
  fields=sorted(k for k in q if q[k]!=prev.get(k));q['revision']+=1;touched=True;changes.append(dict(id=q['id'],file=p.relative_to(r.ROOT).as_posix(),oldRevision=prev['revision'],newRevision=q['revision'],changedFields=fields,beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason=notes[n],status='repaired_pending_reverification'))
 if touched:r.write(p,data)
assert len(changes)==3;r.write(r.OUT/'changes-batch53.json',changes)
r.write(b/'repair-semantic-checks.json',dict(status='PASS',targetChanged=3,relatedChanged=0,crops=crops,answersChoicesUnchanged=True,sourceProsePreserved=True,voteCounterexample='Aselected(5,2,3) or Bselected(3,4,3) implies C3<4; all shown by pre-reveal enumerations.'))
r.write(b/'after-sample.json',dict(sample=[dict(id=i) for i in list(old)+list(related)]))
print('46/50 frozen;3target repairs;2related unchanged5 each')
