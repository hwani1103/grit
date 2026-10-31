import re,unicodedata
import pdfplumber
import review_remaining605 as r
b=r.folder(42);old={x['question']['id']:x['question'] for x in r.read(b/'revealed-current.json')}
assert 'All tests passed!' in (b/'host-before.log').read_text(encoding='utf-8-sig')
assert r.read(b/'exact-model-checks.json')['status']==r.read(b/'source-native-pixel-checks.json')['status']=='PASS'
bodies={
12:'<보기>\n\nㄱ. 농촌 치매안심센터 중 담당면적이 500km² 이상인 센터의 비중은 도시 치매안심센터 중 담당면적이 100km² 미만인 센터의 비중보다 크다.\n\nㄴ. 전체 치매안심센터 중 농촌 치매안심센터의 비중은 담당면적이 100km² 이상 200km² 미만인 치매안심센터 중 농촌 치매안심센터의 비중보다 크다.\n\nㄷ. 치매안심센터에 종사하는 간호사 수는 도시가 농촌의 4배 이상이다.\n\nㄹ. 종사자 수 변동없이 농촌 치매안심센터만 14개소 추가되면, 농촌 치매안심센터 1개소당 사회복지사는 2명 이하가 된다.',
13:'<보기>\n\nㄱ. 조정중재성립 건수가 가장 많은 연도는 2019년이다.\n\nㄴ. 조정중재성립률은 2020년이 가장 높다.\n\nㄷ. 매년 조정중재성립 건수가 가장 많은 기관유형은 ‘병원’이다.\n\nㄹ. ‘상급종합병원’과 ‘의원’은 건당 성립금액의 전년 대비 증감방향이 매년 같다.',
15:'<보고서>\n\n2024년 ‘갑’기관은 업무 개편에 따른 직급 정원 조정의 필요성을 검토하기 위해 ‘위탁집행형 준정부기관’, ‘유사업무 수행 공공기관’ 및 ‘유사업무 수행 민간기관’의 직급 정원 구성비를 조사하였다.\n\n조사결과, 2024년 ‘상급’ 직급 정원 비중은 ‘갑’기관이 ‘위탁집행형 준정부기관’보다 컸다. 한편, ‘갑’기관의 ‘중급’ 직급 정원 비중은 40% 이상이지만, ‘유사업무 수행 공공기관’의 ‘중급’ 직급 정원 비중보다는 작았다. 또한, ‘갑’기관의 ‘하급’ 직급 정원 비중과 ‘유사업무 수행 민간기관’의 ‘하급’ 직급 정원 비중의 차이는 30%p 이상이었다.',
16:'<보기>\n\nㄱ. 여성이 남성보다 많은 읍·면은 3개이다.\n\nㄴ. C ～ E면은 인구가 많은 면일수록 여성 대비 남성의 비율이 높다.\n\nㄷ. ‘갑’군 여성 중 읍 지역 여성 비중과 ‘갑’군 남성 중 면 지역 남성 비중의 차이는 10%p 이하이다.',
17:'<보기>\n\nㄱ. 기술이전 건수는 매년 대학이 공공연구소보다 많다.\n\nㄴ. 2022년 기술도입자가 중소기업인 기술이전 건수 중 ‘유상기술실시’의 비중은 50% 이상이다.\n\nㄷ. 전체 기술이전 건수 중 ‘유상양도’와 ‘무상양도’의 합이 차지하는 비중이 25% 이상인 연도는 5개이다.',
18:'<보기>\n\nㄱ. 2024년 ‘국방비 비율’이 가장 높은 국가는 2014년 대비 2024년 ‘국방비 비율’ 증가폭도 가장 컸다.\n\nㄴ. 2024년 ‘장비비 비율’이 가장 낮은 국가는 2014년 대비 2024년 ‘장비비 비율’ 증가폭도 가장 작았다.\n\nㄷ. 미국의 GDP 대비 장비비는 2024년이 2014년보다 낮았다.',
20:'<보기>\n\nㄱ. 부서인원수가 많은 부서일수록 퇴사율이 높다.\n\nㄴ. 입사자수는 E가 A의 2배 이상이다.\n\nㄷ. 전체 퇴사자수 대비 C의 퇴사자수 비율은 10% 이상이다.'}
notes={12:'평균·센터수·반올림양끝의경계를검증했다.작은보기본문전환과담당면적캡션을원문에맞춘다.',13:'전체기관은생략기관합상한146/119/157/166/143까지포함해검증했다.새풀이누락별도정정;기존해설의상한논증은올바르다.보기본문가독성개선.',14:'7개원본크롭과5그래프의범주/단위/분모/반올림값을전부대조했다.오류그래프①원형유지하며나머지반례근거충분.',15:'각5기관의상급/중급/하급세조건과절대차의음수가지제외를정확분수로검산했다.긴보고서를본문으로전환.',16:'남녀분모와면지역성비순서·10p구간경계를검산했다.보기본문전환.',17:'중소유상교집합하한4829와양도25%이상5개연도를전부확인했다.보기본문전환.',18:'10국가비중증가폭및가까운두국가차.03p의오차하한.01p를검산했다.보기본문전환.',19:'증가율최대/1점포평균최대/상위3합/두해15%/단조반례/전체평균모두검산했다.기존본문과해설충분.',20:'정의식역산과A/E정수인원이표시오차에서도유일함을열거했다.보기본문전환.',22:'연도범례·7지역합·증감·비중과평균초과4곳을전부검산했다.기존본문과5개별이유충분.'}
ratings=[dict(id=i,scoreBeforeFix=4 if q['number'] in bodies else 5,assessment=notes[q['number']],needsChange=q['number'] in bodies) for i,q in old.items()]
assert not (b/'ratings-before.json').exists();r.write(b/'ratings-before.json',dict(method='Same-author original solves, all original images, direct keys/native/28 fresh crops,10 exact models and host-before inspection. Own d13 incomplete scope reasoning separately preserved and corrected; app already correct.',ratings=ratings));r.write(b/'ratings-frozen.json',dict(frozenAt=r.now(),ratingsSha256=r.sha(b/'ratings-before.json'),total=43,count=10,beforeChanges=True))
reg={x['newAsset']:x for x in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/native-image-repairs.json')['figures']}
norm=lambda s:re.sub(r'\s','',unicodedata.normalize('NFKC',s.replace('ㆍ','·')))
checks=[];changes=[]
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  if q['id'] not in old or q['number'] not in bodies:continue
  prev=old[q['id']];assert prev==q;n=q['number'];body=bodies[n];rec=reg[q['figures'][-1]['asset']]
  with pdfplumber.open(r.ROOT/rec['source']) as pdf:raw=pdf.pages[rec['page1based']-1].crop(rec['rect']).extract_text()
  assert norm(raw)==norm(body),(n,raw,body)
  snap=r.OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();r.write(snap,prev)
  q['body']=body;q['figures']=q['figures'][:-1]
  if n==12:q['figures'][0]['caption']='담당면적별 농촌 및 도시 치매안심센터 수'
  fields=sorted(k for k in q.keys()|prev.keys() if q.get(k)!=prev.get(k));q['revision']+=1;touched=True
  changes.append(dict(id=q['id'],file=p.relative_to(r.ROOT).as_posix(),oldRevision=prev['revision'],newRevision=q['revision'],changedFields=fields,beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason=notes[n],status='repaired_pending_reverification'))
  checks.append(dict(id=q['id'],nativeProseExact=True,originalText=raw,source=rec['source'],page=rec['page1based'],rect=rec['rect'],answersAndFiveReasonsUnchanged=q['answer']==prev['answer'] and q['optionReasons']==prev['optionReasons']))
 if touched:r.write(p,data)
assert len(changes)==7;r.write(r.OUT/'changes-batch42.json',changes);r.write(b/'repair-semantic-checks.json',dict(status='PASS',checks=checks,originalAssetsPreserved=True,newAssets=0))
print('7 native prose repairs; ratings43/50 frozen')
