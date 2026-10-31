"""Explicit prose-only transcriptions and one bound-terminology correction."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/psat_remaining605_20261030';B=OUT/'batch12'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert not (OUT/'changes-batch12.json').exists()
assert hashlib.sha256((B/'ratings-before.json').read_bytes()).hexdigest()==read(B/'ratings-frozen.json')['ratingsSha256']
spec={
'kr-mpm-2025-07-19-psat-d-02':dict(remove=[1],body='보기\n\nㄱ. 2018년 교원 1인당 원아수는 10명 이상이다.\n\nㄴ. 전년 대비 증감 방향은 유치원수와 원아수가 매년 동일하다.\n\nㄷ. 2017년 대비 2023년 원아수는 20% 이상 감소한다.'),
'kr-mpm-2025-07-19-psat-d-03':dict(remove=[1],afterBody=True,body='보고서\n\n2023년 ‘갑’시의 전체 민원건수는 145,945건으로 전년 126,866건 대비 15% 이상 증가하였다. 2023년 월별 민원건수는 8월에 가장 많았고, 1월을 제외하고 매월 전년 동월 대비 증가하였다.\n\n2023년 분야별로는 ‘교통’ 분야의 민원건수가 가장 많았고, 다음으로 ‘도로’, ‘행정’ 분야 순으로 많았다. 특히, 민원건수 상위 3개 분야가 전체 민원건수의 75% 이상을 차지하였다.\n\n2023년 지역별로는 A지역의 민원건수가 60,433건으로 ‘갑’시 전체 민원건수의 40% 이상을 차지하였으며, B지역의 민원건수는 35,904건으로 그 뒤를 따랐다. B지역의 인구 100명당 민원건수는 30건 이상으로 ‘갑’시에 속한 A～E지역 중 가장 많았다.\n\n2023년 ‘갑’시 민원의 상위 10대 키워드에는 ‘불법주정차’, ‘어린이 보호구역’ 등 교통법규 관련 키워드와 ‘철도역 신설’, ‘버스노선 신설’ 등 교통환경 관련 키워드, 그리고 ‘소음’, ‘악취’ 등 주거환경 관련 키워드가 포함되었다.'),
'kr-mpm-2025-07-19-psat-d-08':dict(remove=[1],body='조건\n\n○ ‘강사 만족도’가 ‘교육환경 만족도’보다 높은 기관은 발명청과 세무청이다.\n\n○ ‘내용 만족도’는 자료청이 세무청보다 높다.\n\n○ ‘참여자’는 문화청이 자료청보다 많다.'),
'kr-mpm-2025-07-19-psat-d-10':dict(remove=[1],body='보기\n\nㄱ. 2020년 이후 출하지수의 연도별 증감 방향이 ‘저위기술산업군’과 동일한 산업군은 ‘중저위기술산업군’뿐이다.\n\nㄴ. 기준연도를 2024년으로 변경한다면, 모든 산업군별 재고지수는 매년 각각 100 이상이 된다.\n\nㄷ. 재고율이 매년 100% 이상인 산업군은 ‘고위기술산업군’뿐이다.'),
'kr-mpm-2025-07-19-psat-d-12':dict(remove=[2],body='보고서\n\n‘갑’국에서는 에너지 절감을 위한 ‘환경친화적 자동차 구매목표제’를 2019년부터 시행하고 있다. 2024년 민간부문과 공공부문 구매실적의 합이 가장 큰 차종은 (가) 였다.\n\n2024년 민간부문의 업종구분별 구매실적을 보면, 자동차대여사업자는 하이브리드차를 가장 많이 구매하였고 그 외의 업종구분에서는 전기차를 가장 많이 구매하였다. 한편, 전기차 구매실적 대비 수소차 구매실적 비율이 가장 높은 업종구분은 (나) (으)로 나타났다.\n\n2019～2024년 공공부문 구매실적을 보면, 하이브리드차의 공공부문 구매실적은 정책 시행 시작연도인 2019년부터 매년 증가하여 (다) 년에 최대가 되었다가 이후 매년 감소하였다.')}
changes=[]
for path in (ROOT/'assets/psat').glob('*.json'):
 data=read(path)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  if q['id'] not in spec and q['id']!='kr-mpm-2025-07-19-psat-d-13':continue
  old=json.loads(json.dumps(q,ensure_ascii=False));snapshot=OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snapshot.exists();write(snapshot,old)
  if q['id'] in spec:
   s=spec[q['id']];q['body']=s['body'];q['figures']=[f for i,f in enumerate(old['figures']) if i not in s['remove']]
   if s.get('afterBody'):q['figuresAfterBody']=True
   q['editNote']+=' 보기·조건·보고서는 읽기 편한 본문 글자로 표시하고, 표·그래프와 주석·범례는 원형으로 유지한다. 원문 보기에서 전체 배치를 확인할 수 있다.'
  if q['id']=='kr-mpm-2025-07-19-psat-d-02':
   q['optionReasons']=['ㄱ은 42,324>3,095×10으로 참이지만, ㄷ의 원아 감소 9,232>8,801.8도 참이므로 누락이다.','2018년 유치원 수는 427→430으로 증가하고 원아 수는 44,009→42,324로 감소하여 ㄴ은 거짓이다.','ㄷ은 34,777<44,009×0.8로 참이지만, 교원당 원아가 10명 이상인 ㄱ도 참이므로 누락이다.','ㄱ은 42,324>30,950, ㄷ은 감소 9,232>8,801.8로 참이다. ㄴ은 2018년 증감 방향이 달라 거짓이다.','ㄱ·ㄷ은 참이지만 유치원 증가·원아 감소인 2018년 반례가 있는 ㄴ을 포함하여 틀리다.']
  if q['id']=='kr-mpm-2025-07-19-psat-d-10':
   q['optionReasons']=['ㄱ의 증감 방향 일치는 참이지만 고위기술만 매년 재고지수>출하지수인 ㄷ도 참이므로 누락이다.','2021년 중고위기술 재고지수는 새 기준에서 80.0/97.7×100<100이므로 ㄴ은 거짓이다.','ㄱ은 2020년 100을 포함한 증가→감소→감소→감소가 같아 참이고, ㄷ도 고위기술의 매년 재고>출하로 참이다. ㄴ은 80.0/97.7 반례로 거짓이다.','ㄷ은 고위기술의 매년 재고>출하로 참이지만, ㄴ은 2021년 중고위기술의 새 지수가 100 미만이어서 거짓이다.','ㄱ·ㄷ은 참이지만 80.0/97.7×100<100인 ㄴ까지 포함하여 틀리다.']
  if q['id']=='kr-mpm-2025-07-19-psat-d-13':
   assert '상한 소거' in q['steps'][4]
   q['steps'][4]=q['steps'][4].replace('두 좌표 모두 70 초과라는 상한 소거는 가중치가 양수일 때 성립한다.','두 좌표가 모두 70을 넘으면 양의 가중치에서 3×온도＋2×습도>3×70＋2×70=350이다. 이 하한으로 주의 구간 밖임을 확인할 수 있다.')
  q['revision']+=1
  fields=sorted(k for k in old.keys()|q.keys() if old.get(k)!=q.get(k) and k!='revision')
  changes.append(dict(id=q['id'],file=path.relative_to(ROOT).as_posix(),oldRevision=old['revision'],newRevision=q['revision'],changedFields=fields,beforeSnapshot=snapshot.relative_to(ROOT).as_posix(),reason='보고서/보기/조건의 본문 글자 표시 및 선지 근거 보강. d13은 양의 가중합>350이 상한 아닌 하한임을 명시. 표·그래프·선지·정답·기존 이미지와 기록 보존.',status='repaired_pending_reverification'))
  touched=True
 if touched:write(path,data)
assert len(changes)==6;write(OUT/'changes-batch12.json',changes)
write(B/'native-prose-transcriptions.json',dict(status='implemented_pending_verification',transcriptions=spec,dataFiguresRelativeOrderPreserved=True,report03DisplayedBeforeDataForReadability=True,allOriginalAssetsRetained=True,uiCodeChanged=False))
x=read(OUT/'cross-candidates-data-raster-prose.json');x['repairedInBatch12']=list(spec)
for hit in x['candidates']:
 if hit['id'] in spec:hit['status']='batch12_repaired_pending_source_and_host_reverification'
write(OUT/'cross-candidates-data-raster-prose.json',x)
# Exact terminology scope, using the unchanged pre-edit snapshot for the target.
prior={q['id'] for q in read(OUT/'preparation/previously-scored295.json')['questions']};hits=[]
for path in (ROOT/'assets/psat').glob('*.json'):
 data=read(path)
 if not isinstance(data,list):continue
 for q in data:
  if any('상한소거' in ''.join(s.split()) for s in q['steps']):hits.append({'id':q['id'],'cohort':'prior295' if q['id'] in prior else 'fixed605','status':'pending_semantic_review'})
write(OUT/'cross-candidates-bound-direction.json',dict(cause='R605-011',repairedTarget='kr-mpm-2025-07-19-psat-d-13',method='All900 exact phrase 상한 소거 after target correction; candidate searches do not validate all bound arguments.',otherCandidates=hits,prior295Hits=sum(h['cohort']=='prior295' for h in hits)))
x=read(OUT/'cross-validation.json');x['findings'].append(dict(id='R605-011',batch=12,cause='Positive coordinate lower bounds imply a lower bound on the weighted sum; incorrect upper-bound terminology corrected.',target='kr-mpm-2025-07-19-psat-d-13',scopeFile='cross-candidates-bound-direction.json',otherExactPhraseHits=len(hits),prior295ExactPhraseHits=sum(h['cohort']=='prior295' for h in hits),status='target_repaired_pending_verification'));write(OUT/'cross-validation.json',x)
print('Revised five prose blocks and one bound direction; data figures unchanged; other exact-bound-term hits',len(hits))
