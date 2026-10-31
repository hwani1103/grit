import re,pdfplumber
import review_remaining605 as r
b=r.folder(45);old={x['question']['id']:x['question'] for x in r.read(b/'revealed-current.json')};related={q['id']:q for q in r.read(b/'related295-before.json')}
for name in ['source-native-pixel-checks.json','related295-source-native-pixel-checks.json','exact-model-checks.json']:assert r.read(b/name)['status']=='PASS'
for name in ['host-before.log','related295-host-before.log']:assert 'All tests passed!' in (b/name).read_text(encoding='utf-8-sig')
notes={24:'동일분자소거/가중대칭/순위반례와실제선지유일성정확.작은보기이미지를원문본문으로분리.',25:'20대합산/25세경계/직장인교집합최소239명/분모구분정확.발견없음.',27:'GDP5개/증가분4개및80%/100%경계검산정확.원표계층과그래프의의도된오류보존.발견없음.',28:'증가율4개/반올림범위내9.4%/병원5.9%/기관별비용미제공구분정확.발견없음.',30:'성별분모미제공과A/C근접반례,4품종비율및C연령값정확.공통29와모든정의교차검증.발견없음.',32:'올림5/34/5/4대와정확총시간/최대요금차/300초경계정확.긴조건이미지의문장을본문으로분리하고원본정보수식/표보존.',33:'정수해c4/k6유일,대소140개재고일치정확.규칙문장을원표1과원표2사이본문으로옮겨읽기개선.',35:'모니터가격대비주사율/UHD엄격초과/총예산/메모리순서및5개금액근거정확.작은대화이미지의전체7발언·화자·시각을네이티브본문으로옮김.',36:'4개날짜창과31일합2170/편차합0/품질보정후갑77.66>무77정확.정보표·달력원형유지,발견없음.',37:'Q●당유일과정당별잔여7건이7명에하나씩배정됨을확인.숫자만으로인원동일시하지않는적용한계정확.발견없음.'}
fix={24,32,33,35};ratings=[dict(id=i,scoreBeforeFix=4 if q['number'] in fix else 5,assessment=notes[q['number']],needsChange=q['number'] in fix,deduction='긴조건/보기/대화읽기크기' if q['number'] in fix else '발견없음') for i,q in old.items()]
assert not (b/'ratings-before.json').exists();r.write(b/'ratings-before.json',dict(method='Original-only solves frozen before reveal; exact models, direct source/key/fresh pixels and pre-edit host reviewed.',ratings=ratings));r.write(b/'ratings-frozen.json',dict(frozenAt=r.now(),ratingsSha256=r.sha(b/'ratings-before.json'),total=46,count=10,beforeChanges=True))
hist={x['id']:x for x in r.read(r.PREP/'previously-scored295.json')['questions']}
r.write(b/'related295-assessment-before.json',[dict(id=i,historicalScorePreserved=hist[i]['scoreBeforeFix'],currentBeforeScore=4 if q['number']==26 else 5,assessment='5개도시4조건의전수검산정확.작은보고서이미지의조건을본문으로옮김.' if q['number']==26 else '감염수와구성비/감염률분모구별및성별차이반올림상하한정확,발견없음.',notReplacementOfHistoricalScore=True,changed=q['number']==26) for i,q in related.items()])
body24='<보 기>\n\nㄱ. 고령인구 구성비가 높은 도시일수록 노년부양비도 높다.\n\nㄴ. 생산연령인구 구성비가 가장 낮은 도시는 A이다.\n\nㄷ. B도시와 E도시가 하나의 도시로 통합되면, 통합 도시의 고령인구 구성비는 15% 이하가 된다.'
body32='<조 건>\n\n○ A～D는 각각 ‘돌고래’, ‘무궁화’, ‘소나무’, ‘호랑이’ 중 하나이다.\n\n○ ‘소나무’는 출발점부터 도착점까지의 운행시간이 5분 이상이다.\n\n○ 200명의 승객이 출발점에서 도착점까지 이동하기 위한 운행대수를 최소화할 때, 총운행시간이 가장 짧은 케이블카는 ‘호랑이’이다.\n\n○ 대인 2명과 소인 2명의 케이블카 이용요금 총합은 ‘소나무’와 ‘돌고래’ 사이에서 차이가 가장 크다.'
body33='<규 칙>\n\n○ 보유한 사과 140개를 10개씩 나누어 14개 세트를 구성한다.\n\n○ 각 세트는 품질 구분 없이 같은 크기의 사과로만 구성한다.\n\n○ 각 세트는 ‘상’ 품질의 사과가 ‘중’ 품질의 사과보다 많도록 구성한다.'
body26='<보고서>\n\n‘갑’시의 2024년 일평균 미세먼지 노출시간에 따른 남녀 호흡기 질환 발병률을 분석한 결과는 다음과 같다. 첫째, 미세먼지 노출시간이 매 1시간 증가할 때, 남성과 여성 모두 호흡기 질환 발병률이 증가한다. 둘째, 남성과 여성의 호흡기 질환 발병률 차이는 미세먼지 노출시간이 3시간일 때가 1시간일 때의 1.5배 이상 2배 미만이다. 셋째, 미세먼지 노출시간이 매 1시간 증가할 때, 호흡기 질환 발병률의 증감폭은 여성이 남성보다 크다. 넷째, 호흡기 질환 발병률은 남성과 여성 모두 미세먼지 노출시간이 4시간일 때가 2시간일 때의 1.3배 이상이다.'
dialog=[('장 사무관','3:10 pm','조 사무관님, 소개해주신 ‘갑’～‘무’ 모니터와 ‘가’～‘바’ 그래픽카드의 사양 및 단가 자료 확인했습니다. 그런데, 금번 A 부서의 모니터, 그래픽카드 구매 예산과 제품별 구매 수량은 어떻게 되나요?'),('조 사무관','3:11 pm','네, 저희 A 부서는 총 3,000만 원 예산 범위 내에서 모니터 10개와 그래픽카드 32개를 2024년 3월 4일에 구매하였습니다.'),('장 사무관','3:13 pm','모니터 10개와 그래픽카드 32개를 각각 단일 제품으로 구매하셨나요?'),('조 사무관','3:16 pm','네, 그렇습니다. 소개해드린 자료에서 모니터는 30인치 이상 크기에 QHD 이상 해상도를 지원하는 제품을 선택하였고, 그래픽카드는 해당 모니터가 지원하는 가장 높은 해상도를 기준으로 그래픽카드 프레임속도 값이 모니터 주사율 값보다 큰 제품을 선택하였습니다.'),('장 사무관','3:17 pm','그러셨군요. 예산 제약 때문에 제품 선택이 어려우셨겠어요.'),('조 사무관','3:19 pm','네, 그렇습니다. 방금 말씀드린 사양을 만족하는 모니터와 그래픽카드 중 모니터는 단가 대비 주사율이 더 큰 제품을 선택하였고, 그래픽카드는 메모리 용량이 더 큰 제품을 선택하였습니다. 모든 구매는 예산 범위 내에서 제품별 단가대로 진행하였습니다.'),('장 사무관','3:20 pm','수고 많으셨네요. 덕분에 큰 도움이 되었습니다. 감사합니다.')]
body35='<대 화>\n\n'+'\n\n'.join(f'{speaker} ({time}): {speech}' for speaker,time,speech in dialog)
reg={x['newAsset']:x for x in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/native-image-repairs.json')['figures']};norm=lambda s:re.sub(r'\s','',s);checks=[];changes=[]
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  is_related=q['id'] in related
  if not((q['id'] in old and q['number'] in fix) or (is_related and q['number']==26)):continue
  prev=(related if is_related else old)[q['id']];assert q==prev;n=q['number'];snap=r.OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();r.write(snap,prev)
  if n==24:removed=q['figures'].pop();q['body']=body24
  elif n==32:removed=q['figures'].pop();q['body']=body32;assert q['choiceNote']=='A → B'
  elif n==33:removed=q['figures'].pop(1);q['body']=body33;q['bodyAfterFigureCount']=1
  elif n==35:removed=q['figures'].pop();q['body']=body35
  elif n==26:removed=q['figures'].pop();q['body']=body26
  q['figuresAfterBody']=False
  if n!=35:
   v=reg[removed['asset']]
   with pdfplumber.open(r.ROOT/v['source']) as pdf:raw=pdf.pages[v['page1based']-1].crop(v['rect']).extract_text()
   if n==32:assert raw.endswith('A B');raw=raw[:-3]
   assert norm(raw)==norm(q['body']),(n,'source prose mismatch')
   checks.append(dict(id=q['id'],removedFigure=removed['asset'],sourceProseExactIgnoringWhitespace=True,choiceHeaderRepresentedByChoiceNote=n==32))
  else:checks.append(dict(id=q['id'],removedFigure=removed['asset'],sourceRasterSha256=r.sha(r.ROOT/removed['asset']),manualTranscription=dialog,visualComparison='All7 balloons, speaker names,7 timestamps inspected from original raster. Decorative avatars omitted; all source utterances retained.'))
  for j,f in enumerate(q['figures']):
   if n==32:f['caption']=['케이블카 요금·거리·정원·속도 원본 표','운행 정보와 속도 정의'][j]
   if n==33:f['caption']=['사과 크기·품질별 개수·단가 원본 표','세트별 구성·개수·가격 원본 표와 주석'][j]
   if n==35:f['caption']=['모니터 제품별 사양·단가 원본 표','그래픽카드 제품별 사양·단가 원본 표'][j]
  assert q['answer']==prev['answer'] and q['choices']==prev['choices'] and q['steps']==prev['steps'] and q['optionReasons']==prev['optionReasons']
  fields=sorted(k for k in q if q[k]!=prev.get(k));q['revision']+=1;touched=True
  changes.append(dict(id=q['id'],file=p.relative_to(r.ROOT).as_posix(),oldRevision=prev['revision'],newRevision=q['revision'],changedFields=fields,beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason='보고서의4개조건을원문본문으로옮김.' if is_related else notes[n],status='repaired_pending_reverification'))
 if touched:r.write(p,data)
assert len(changes)==5;r.write(r.OUT/'changes-batch45.json',changes)
r.write(b/'repair-semantic-checks.json',dict(status='PASS',targetCount=4,relatedCount=1,proseChecks=checks,sourceTablesFormulasAndAllAssetsPreserved=True,allAnswersChoicesExplanationsUnchanged=True))
print('Frozen46/50;4target+1related prose repairs;all original assets retained')
