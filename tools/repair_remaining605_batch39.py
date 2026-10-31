import re,unicodedata
import pdfplumber
import review_remaining605 as r
b=r.folder(39);old={x['question']['id']:x['question'] for x in r.read(b/'revealed-current.json')}
assert 'All tests passed!' in (b/'host-before.log').read_text(encoding='utf-8-sig');assert r.read(b/'exact-model-checks.json')['status']==r.read(b/'source-native-pixel-checks.json')['status']=='PASS'
key=lambda q:('26' if '2026-' in q['id'] else '25')+'-'+str(q['number'])
bodies={
'26-37':('<보고서>\n\n공영자전거를 직영으로 운영하는 ‘갑’지역은 2025년 주차장 1개소당 대여 실적이 5,000건 이상이었다. 운영 방식이 직영인 지역 중, ‘갑’지역은 공영자전거 수가 가장 많았지만 주차장 수는 가장 적었다. 한편, ‘갑’지역은 공영자전거 1대당 대여 실적이 100건 이상이었지만 운영 방식이 직영인 지역 중 가장 낮았다.',1),
'26-38':('<보기>\n\nㄱ. 학생 A의 점수는 ‘갑’반 학생 점수의 평균보다 높다.\n\nㄴ. 최고점을 받은 학생과 최저점을 받은 학생의 점수 차이는 13점이다.\n\nㄷ. 배점 2점인 문항을 모두 맞힌 학생은 4명이다.\n\nㄹ. 문항 10을 맞힌 학생 점수의 평균은 학생 G의 점수보다 높다.',2),
'25-2':('<보고서>\n\n2023년 모든 도로종류에서 전년에 비해 교통량이 증가하였으며 그중 고속국도의 증가폭이 가장 컸다. 2023년 차량유형별 교통량은 모든 도로종류에서 (A) [빈칸]가 가장 적었다.\n\n2024년 교통량을 보면, 전체 교통량은 전년에 비해 증가하였으며, 도로종류별 교통량 중 승용차의 비중은 고속국도가 일반국도보다 (B) [빈칸]. 한편, 2024년 지방도 교통량 중 버스의 비중은 전년 대비 (C) [빈칸]하였다.',1),
'25-5':('<보고서>\n\n2024년 A, B대학교 ‘갑’전공의 모집인원 및 지원자 수를 조사하였다. ①모집인원은 B대학교가 A대학교보다 3명 많은 것으로 나타났으며, ②지원자 수는 A대학교가 B대학교의 1.2배 이상인 것으로 확인되었다. 한편, 두 대학교에서 ‘갑’전공의 입학전형은 ‘가’, ‘나’, ‘다’, ‘라’, ‘마’전형으로만 구성되는데, ③A, B대학교는 각각 모집인원이 가장 많은 전형이 지원자 수도 가장 많은 것으로 조사되었다.\n\n④‘갑’전공 전체 경쟁률의 경우, A대학교는 지원자 수가 모집인원의 20배 이상으로 B대학교보다 높은 경쟁률을 보였다. 그러나 대학별로 지원자에게 유리한 전형은 다르게 나타났다. ⑤‘마’전형의 경우, A대학교에서는 경쟁률이 두 번째로 높았으나, B대학교에서는 경쟁률이 가장 낮은 것으로 나타났다.',2),
'25-6':('<보고서>\n\n조선 중기 이후 세제와 군역에 대한 개혁이 진행되어 군사조직이 효율적으로 변하기는 했지만, 여전히 무과는 자주 시행되었고, 실제 필요한 무관보다 많은 급제자를 양산하는 문제점이 나타나기 시작하였다. 무과제도가 존재했던 1402년부터 1894년까지 천 명 이상의 무과급제자를 배출한 연도수는 14개였고, 그중 10개 연도가 1618년부터 1894년 사이였다. 특히 1676년에는 17,652명의 무과급제자가 배출되었다.\n\n조선은 다양한 시험을 통해 무과급제자를 선발하였는데 급제자 수를 늘리기 위해 시험 시행 간격을 짧게 하였다. 예를 들어, 조선 초기에 15년이나 16년에 한 번씩 시행했던 증광시는 조선 중기 이후 5년이나 6년에 한 번씩 시행하였으며, 별시의 시행도 잦았다. 특히 정시와 알성시, 외방별시는 조선 초기보다 후기에 더욱 많이 시행되었는데, 1608년부터 1894년 사이에 정시 194회, 알성시 56회, 외방별시 32회가 시행되었다.\n\n1608 ～ 1894년 동안 무과급제자의 주요 성관 비중을 살펴보면, 김해 김씨 5.1%, 전주 이씨 4.7%, 밀양 박씨 4.0%, 경주 김씨 2.2% 등이었다. 또한, 광해군 이후 무과급제자의 출신지역 비중을 살펴보면 철종 재위 기간까지 출신지역 비중이 가장 컸던 지역은 한양 또는 경기였고, 전라 출신 무과급제자의 비중은 효종 재위 기간에는 19.6%였으나 이후 감소하다 헌종 재위 기간부터 다시 증가한 것이 특징이다.\n\n한편, 이 시기 무과급제 자체는 관직 임용을 보장해주지 않았다. 실제로 무관이 된 무과급제자는 한양과 그 주변에 기반을 둔 저명 무인 가문 출신이 대부분이었다. 이러한 무과급제자는 점차 주요 고위관직의 문관으로 예상외의 승진을 하기도 하였고, 반대로 군영의 장군직을 문과급제자가 수행하기도 하였는데, 고종 재위 기간에는 신임 군영 장군 33명 중 문과급제자 출신이 8명이었다.',0),
'25-8':('<보고서>\n\n①2020 ～ 2024년 ‘갑’국의 조세수입은 매년 증가하여, 2024년 총 456.9조 원 수준이다. 2023년 국세 수입은 전년 대비 소폭 감소하였으나, 이후 법인 영업실적 개선과 자산시장 호조 등의 영향으로 ②2024년에는 국세 수입이 전년 대비 20% 이상 증가하였다.\n\n같은 기간 지방세 수입은 지속해서 증가해왔는데, ③전년 대비 지방세 수입 증가율은 2023년에 가장 높았다. ‘갑’국의 조세수입 중 지방세 수입이 차지하는 비중은 매년 20% 이상을 유지해왔다. 재정분권 등에 따라 ④2021년 이후 조세수입 중 지방세 수입의 비중이 매년 증가해 왔으나, ⑤국세 수입과 지방세 수입의 격차는 2024년이 가장 컸다.',1)}
under={
'25-5':['모집인원은 B대학교가 A대학교보다 3명 많은 것으로 나타났으며,','지원자 수는 A대학교가 B대학교의 1.2배 이상인 것으로 확인되었다.','A, B대학교는 각각 모집인원이 가장 많은 전형이 지원자 수도 가장 많은 것으로 조사되었다.','‘갑’전공 전체 경쟁률의 경우, A대학교는 지원자 수가 모집인원의 20배 이상으로 B대학교보다 높은 경쟁률을 보였다.','‘마’전형의 경우, A대학교에서는 경쟁률이 두 번째로 높았으나, B대학교에서는 경쟁률이 가장 낮은 것으로 나타났다.'],
'25-8':['2020 ～ 2024년 ‘갑’국의 조세수입은 매년 증가하여,','2024년에는 국세 수입이 전년 대비 20% 이상 증가하였다.','전년 대비 지방세 수입 증가율은 2023년에 가장 높았다.','2021년 이후 조세수입 중 지방세 수입의 비중이 매년 증가해 왔으나,','국세 수입과 지방세 수입의 격차는 2024년이 가장 컸다.']}
notes={'26-36':'15막대값·지역별소유율·합계비중과타지역/해당지역분모를전부대조했다.공통도입문복원및붙은해설어절과ㄹ의실제분모오류를구체화한다.','26-37':'직영5곳과모든보고서조건을만족하는집합DEFHI/갑I가유일함을열거했다.보고서이미지를원문본문으로옮긴다.','26-38':'원문채점표와16가지빈칸배치에서2개가능배치·점수16/18·2점전부정답4명을확인했다.새풀이H누락오류는별도보존정정하며앱정답은맞다.보기네이티브및붙은어절수정.','26-40':'편차/대비율역산과네오답을정확분수로확인하고±0.05표시오차양끝으로도제주<28/영남내륙>34임을보였다.선지퍼센트·해설어절및구체적오차근거보완.','25-2':'모든최소값·승용비중교차곱·지방도버스분자증가분모감소와보고서다른전제를확인했다.보고서원문·빈칸을네이티브로복원.','25-3':'16개2023막대와9개재원값이일치,사회복지비중과보건·문화의증감오류를확인했다.해설부호앞공백과문화반례추가.','25-5':'두대학모집지원합과모든전형경쟁률을비교했다.보고서를밑줄전체보존본문으로복원하고해설어절정리.','25-6':'자료별직접대응문장을확인하고급제자비중과시행횟수의단위를구별했다.긴보고서가독성을본문으로개선하며원래보고서→자료순서보존.','25-7':'누적재고전체와집행연도증가·감형17<18·증가율·확정비중을검산했다.붙은선지기호와설명공백정리.','25-8':'연간합·국세20%경계·지방세증가율·비중하락·격차최대를전부검산했다.보고서다섯밑줄을완전한네이티브문구로보존한다.'}
ratings=[dict(id=i,scoreBeforeFix=4,assessment=notes[key(q)],needsChange=True) for i,q in old.items()]
assert not (b/'ratings-before.json').exists();r.write(b/'ratings-before.json',dict(method='Same-author fresh solves, original graph/grid, direct selected keys and32 fresh crops, exact models and host pre-edit. Own H omission corrected separately; nine first answers match, original answer3 retained.',ratings=ratings));r.write(b/'ratings-frozen.json',dict(frozenAt=r.now(),ratingsSha256=r.sha(b/'ratings-before.json'),total=40,count=10,beforeChanges=True))
reg={x['newAsset']:x for x in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/native-image-repairs.json')['figures']}
norm=lambda s:re.sub(r'\s','',unicodedata.normalize('NFKC',s)).replace('∼','~')
changes=[];checks=[]
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  if q['id'] not in old:continue
  prev=old[q['id']];assert prev==q;k=key(q)
  # Validate proposed prose before any mutation or immutable before snapshot.
  if k in bodies:
   body,index=bodies[k];rec=reg[q['figures'][index]['asset']]
   with pdfplumber.open(r.ROOT/rec['source']) as pdf:
    page=pdf.pages[rec['page1based']-1].crop(rec['rect']);raw=page.extract_text()
    lines=[dict(x0=l['x0'],x1=l['x1'],top=l['top']) for l in page.lines if abs(l['top']-l['bottom'])<.2]
   expected=body
   if k=='25-2':
    assert raw.rstrip().endswith('A B C');raw=raw.rstrip()[:-5]
    expected=expected.replace('(A) [빈칸]','A').replace('(B) [빈칸]','B').replace('(C) [빈칸]','C')
   assert norm(raw)==norm(expected),(k,raw,expected)
   checks.append(dict(id=q['id'],originalText=raw,source=rec['source'],page=rec['page1based'],rect=rec['rect'],nativeProseExact=True,sourceHorizontalLines=lines if k in under else []))
  snap=r.OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();r.write(snap,prev)
  if k in bodies:
   q['body'],index=bodies[k];q['figures']=[f for j,f in enumerate(q['figures']) if j!=index]
   if k=='25-6':q['bodyAfterFigureCount']=0
  if k in under:
   q['underlines']=under[k]
   assert all(q['body'].count(s)==1 for s in q['underlines'])
  if k=='26-36':
   intro='다음 <표>는 ‘갑’국 A ～ E지역의 주택 보급 및 소유 현황에 관한 자료이다. 다음 물음에 답하시오.';q['prompt']=intro+'\n\n'+q['prompt'];assert norm(intro) in norm(next(x['sourceText'] for x in r.read(b/'blind-source.json') if x['id']==q['id']))
   q['steps']=[s.replace('호로약','호로 약').replace('ㄷ은지역별','ㄷ은 지역별') for s in q['steps']]
   q['optionReasons'][3]='ㄱ·ㄷ은 맞지만 ㄹ의 A는 타지역 6,383/해당지역 26,089≈24.5%로 그림의 27.4%와 다르다. 27.4%는 주택소유가구수 23,335를 분모로 잘못 쓴 값이다.'
  if k=='26-38':q['steps']=[s.replace('40,3점','40, 3점').replace('H와그','H와 그') for s in q['steps']];q['optionReasons']=[s.replace('13,2점','13, 2점') for s in q['optionReasons']]
  if k=='26-40':
   q['choices']=[s.replace('40 %','40%') for s in q['choices']];q['steps']=[s.replace('보다제주','보다 제주') for s in q['steps']]
   q['steps'][2]='답 확정 기준: 표시된 편차와 대비율을 각각 ±0.05시간·±0.05%p 범위로 넓혀도 복원한 제주 일조시간은 28시간 미만, 영남내륙은 34시간 초과다. 따라서 반올림 오차에도 제주가 짧다. 나머지 선택지는 부호 개수·기준값·지표 대응·비율의 비로 반박해 ⑤를 확정한다.'
  if k=='25-3':q['steps']=[s.replace('그림은−','그림은 −').replace('ㄹ의−','ㄹ의 −').replace('과+','과 +') for s in q['steps']];q['steps'][3]+=' 문화 및 관광도 8.6−8.5=+0.1인데 그림은 −0.5로, 2022년 9.1을 뺀 값이다.'
  if k=='25-5':
   q['steps']=[s.replace('최대는마','최대는 마').replace('최대는나','최대는 나') for s in q['steps']];q['optionReasons']=[s.replace('A는마','A는 마').replace('최저 경쟁률은라','최저 경쟁률은 라') for s in q['optionReasons']]
  if k=='25-6':q['steps']=[s.replace('⑤는고종','⑤는 고종').replace('비중은효종','비중은 효종').replace('에서순조','에서 순조') for s in q['steps']]
  if k=='25-7':q['steps']=[s.replace('②2016','② 2016').replace('⑤2020','⑤ 2020') for s in q['steps']];q['optionReasons']=[s.replace('명은집행','명은 집행') for s in q['optionReasons']]
  fields=sorted(k for k in q.keys()|prev.keys() if q.get(k)!=prev.get(k));assert fields;q['revision']+=1;touched=True
  assert q['answer']==prev['answer'] and [norm(s) for s in q['choices']]==[norm(s) for s in prev['choices']]
  changes.append(dict(id=q['id'],file=p.relative_to(r.ROOT).as_posix(),oldRevision=prev['revision'],newRevision=q['revision'],changedFields=fields,beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason=notes[k],status='repaired_pending_reverification'))
 if touched:r.write(p,data)
assert len(changes)==10;r.write(r.OUT/'changes-batch39.json',changes);r.write(b/'repair-semantic-checks.json',dict(status='PASS',count=10,nativeProseCount=6,checks=checks,originalAssetsPreserved=True,sourceAnswersUnchanged=True,originalUnderlinesVerifiedAgainstPdfStrokes=True))
print('Frozen40/50;10 repairs;6 native report/보기 blocks; originals/answers preserved')
