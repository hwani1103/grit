import re,pdfplumber,unicodedata
import review_remaining605 as r
b=r.folder(48);old={x['question']['id']:x['question'] for x in r.read(b/'revealed-current.json')};related={q['id']:q for q in r.read(b/'related295-before.json')}
for n in ['host-before.log','related295-host-before.log']:assert 'All tests passed!' in (b/n).read_text(encoding='utf-8-sig')
for n in ['source-native-pixel-checks.json','related295-source-native-pixel-checks.json','exact-model-checks.json','related295-underline-source-strokes.json']:assert r.read(b/n)['status']=='PASS'
notes={40:'가구상한과실제인원복원,독립기준변경정확.작은지급기준이미지를본문으로분리.',1:'추가분류ㄱㄴ및원표증가율정확.긴보고서이미지를본문으로옮겨분류별문단분리.',3:'누적막대구간반례1104→1048및5그래프/0시작수와비중경계정확.발견없음.',4:'5행4조건/성별방향/2배이상등호모두정확.발견없음.',5:'동기별증가4→1및20%/50%반례와실제⑤ㄱㄴㄹ에따른조기확정정확.발견없음.',6:'29%/28%분리및교집합범위2142~2355,반례연도정확.발견없음.',7:'5개연도×단위/분모별계산및2022여집합80%상한정확.그래프오류의도보존,발견없음.',8:'ㄹ의중복입직총계와ㄷ의고유이직정보구별정확.긴보고서이미지를본문으로분리.',10:'3기관모든빈칸복원/평가지표가중치/4배경계정확.발견없음.',15:'정비구역우선과길고짧은균열범례/연한등호를원본확대로확인.활용4/철거2정확.원형지도유지,발견없음.'}
fix={40,1,8};ratings=[dict(id=i,scoreBeforeFix=4 if q['number'] in fix else 5,assessment=notes[q['number']],needsChange=q['number'] in fix) for i,q in old.items()]
assert not (b/'ratings-before.json').exists();r.write(b/'ratings-before.json',dict(method='Own source-only solutions frozen,10answer matches but4own-record corrections preserved separately; exact models/source/key/fresh pixels and pre-edit host inspected.',ratings=ratings));r.write(b/'ratings-frozen.json',dict(frozenAt=r.now(),ratingsSha256=r.sha(b/'ratings-before.json'),total=47,count=10,beforeChanges=True))
hist={x['id']:x for x in r.read(r.PREP/'previously-scored295.json')['questions']}
r.write(b/'related295-assessment-before.json',[dict(id=i,historicalScorePreserved=hist[i]['scoreBeforeFix'],currentBeforeScore=4 if q['number']==2 else 5,assessment='全24대응중유일/차이1이하/1인당총량정확.조건이미지를본문으로분리.' if q['number']==2 else '원표등록/수출과5국교집합정확.5밑줄의마침표도원본선에포함되므로유지.',notReplacementOfHistoricalScore=True,changed=q['number']==2) for i,q in related.items()])
body40='<국민재난지원금 지급기준>\n\n○ (기준 1) 건강보험료가 226,880원 이하인 세대만 지급 대상으로 함.\n\n○ (기준 2) 세대원 1인당 10만 원을 지급함.\n\n○ (기준 3) 세대별 지급가능 상한액은 40만 원임.'
body1='<보고서>\n\n‘갑’지역 택배서비스 이용자의 코로나19 발생 전 월평균 이용건수는 6.2건이었으나 발생 후에는 9.7건으로 50% 이상 증가하였다. 코로나19 발생 전 대비 발생 후 택배서비스 월평균 이용건수 증가율은 여성이 남성보다 높았다.\n\n연령대별로 살펴보면, 코로나19 발생 전 대비 발생 후 택배서비스 월평균 이용건수 증가율은 20대가 가장 높게 나타났고, 70대 이상이 다음으로 높았다. 거주형태별로 살펴보면, 오피스텔 거주자의 코로나19 발생 전 대비 발생 후 택배서비스 월평균 이용건수 증가율이 약 70%로 가장 높게 나타났고, 아파트 거주자가 다음으로 높았다.\n\n유통채널별로 살펴보면, 코로나19 발생 전에는 온라인구매 비율이 61.0%로 가장 높았고, 다음으로 마트배송, 홈쇼핑, 기타 순으로 나타났다. 코로나19 발생 후 온라인구매 비율은 발생 전에 비해 3.3%p 증가하였다.\n\n수령방법별로 살펴보면, 코로나19 발생 전에는 대면 수령 비율과 비대면 수령 비율이 각각 50.2%, 49.8%로 비슷한 수준이었다. 코로나19 발생 후에는 대면 수령 비율이 19.4%로 감소하였고, 비대면 수령 비율은 80.6%로 증가하였다.'
body8='<보고서>\n\n‘갑’국 고용노동부는 2023년 7월 사업체노동력조사를 통해 종사자 및 입·이직자 현황을 파악하였다. 2023년 7월 상용근로자는 전년 동월 대비 27만 2천 명 증가하였으며, 임시일용근로자는 전년 동월 대비 12만 8천 명 증가하였다.\n\n사업체 규모별 종사자 수 동향을 살펴보면, 2023년 7월 300인 미만 사업체의 경우 전년 동월 대비 33만 3천 명 증가하였으며, 300인 이상 사업체는 전년 동월 대비 6만 9천 명 증가하였다.\n\n한편, 2023년 7월 입직자는 전년 동월 대비 2만 6천 명 증가하였고 전월 대비 5만 8천 명 증가하였다. 2023년 7월 이직자는 전년 동월 대비 약 4.0% 증가하였고 전월 대비 약 7.0% 증가하였다.\n\n또한, 2023년 7월 전체 입직자 중 채용을 통한 입직자는 전년 동월 대비 2만 5천 명 증가하였으며, 기타 입직자는 전년 동월 대비 1천 명 증가하였다.'
body2='<조 건>\n\n○ ‘갑’국은 온실가스 총배출량이 50백만 톤 CO₂eq. 이상이고, 1인당 온실가스 총배출량이 가장 적다.\n\n○ ‘을’국과 ‘병’국 간 1인당 온실가스 총배출량의 차이는 1.0톤 CO₂eq./명 이하이다.\n\n○ 온실가스 총배출량 대비 주거용 빌딩의 온실가스 배출량 비율은 ‘병’국이 ‘정’국보다 높다.\n\n○ 주거용 빌딩과 상업용 빌딩의 온실가스 배출량 합은 ‘을’국이 가장 적다.'
reg={x['newAsset']:x for x in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/native-image-repairs.json')['figures']}
norm=lambda s:re.sub(r'\s','',unicodedata.normalize('NFKC',s.replace('ㆍ','·')))
changes=[];checks=[]
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  isRelated=q['id'] in related
  if not ((q['id'] in old and q['number'] in fix) or (isRelated and q['number']==2)):continue
  prev=(related if isRelated else old)[q['id']];assert q==prev;n=q['number'];body={1:body1,8:body8,40:body40,2:body2}[n]
  removed=q['figures'].pop(2 if n in [40,2] else 1);v=reg[removed['asset']]
  with pdfplumber.open(r.ROOT/v['source']) as pdf:raw=pdf.pages[v['page1based']-1].crop(v['rect']).extract_text()
  if n==2:
   assert raw.endswith('A B C D');raw=raw[:-7]
   # Original subscript2 is extracted on its own next line; retain CO2 identity.
   assert raw.count('CO eq. 이상이고,\n2')==1 and raw.count('CO eq./명 이하이다.\n2')==1
   raw=raw.replace('CO eq. 이상이고,\n2','CO₂eq. 이상이고,').replace('CO eq./명 이하이다.\n2','CO₂eq./명 이하이다.')
   assert q['choiceNote']=='A → B → C → D'
  assert norm(raw)==norm(body),(n,raw,body)
  snap=r.OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();r.write(snap,prev)
  q['body']=body+('\n\n'+prev['body'] if n==40 else '')
  q['figuresAfterBody']=False
  if n in [1,8]:q['bodyAfterFigureCount']=1
  assert q['answer']==prev['answer'] and q['choices']==prev['choices'] and q['steps']==prev['steps'] and q['optionReasons']==prev['optionReasons']
  fields=sorted(k for k in q if q[k]!=prev.get(k));q['revision']+=1;touched=True
  changes.append(dict(id=q['id'],file=p.relative_to(r.ROOT).as_posix(),oldRevision=prev['revision'],newRevision=q['revision'],changedFields=fields,beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason='조건문장본문분리;CO2첨자보존;선지머리A/B/C/D는기존choiceNote로표시.' if isRelated else notes[n],status='repaired_pending_reverification'))
  checks.append(dict(id=q['id'],removedFigure=removed['asset'],originalAllCharactersPreserved=True,sourceSubscriptExtractionReordered=n==2,bodyBetweenMainAndOptionFigures=n in [1,8]))
 if touched:r.write(p,data)
assert len(changes)==4;r.write(r.OUT/'changes-batch48.json',changes)
r.write(b/'repair-semantic-checks.json',dict(status='PASS',targetCount=3,relatedCount=1,checks=checks,allAnswersChoicesExplanationsUnchanged=True,sourceTablesAndOriginalAssetsPreserved=True))
r.write(b/'after-sample.json',dict(sample=[dict(id=i) for i in list(old)+list(related)]))
print('Frozen47/50;3target+1related prose repairs;all original assets retained')
