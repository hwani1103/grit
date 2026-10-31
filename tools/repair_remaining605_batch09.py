"""Explicit source transcription of prose only; keep data tables/graphs intact."""
from pathlib import Path
import json, hashlib
from datetime import datetime
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/psat_remaining605_20261030';B=OUT/'batch09'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert not (OUT/'changes-batch09.json').exists()
assert hashlib.sha256((B/'ratings-before.json').read_bytes()).hexdigest()==read(B/'ratings-frozen.json')['ratingsSha256']
spec={
'kr-mpm-2023-07-22-psat-d-21':dict(remove=[1],body='보기\n\nㄱ. 제20대 선거에서 투표소 수는 ‘아주’가 ‘중동’의 4배 이상이다.\n\nㄴ. 제20대 선거에서 투표율이 가장 높은 지역과 가장 낮은 지역의 투표율 차이는 15%p 이상이다.\n\nㄷ. 제20대 선거에서 투표소당 선거인 수는 ‘미주’가 ‘유럽’보다 많다.\n\nㄹ. 제20대 선거와 제19대 선거의 선거인 수 차이가 큰 지역부터 순서대로 나열하면 ‘아주’, ‘미주’, ‘유럽’, ‘중동’, ‘아프리카’ 순이다.'),
'kr-mpm-2023-07-22-psat-d-22':dict(remove=[2],body='조건\n\n○ 2017～2019년 동안 ‘안전사고’ 발생 건수는 매년 증가한다.\n\n○ 2020년 해양사고 발생 건수 대비 인명피해 인원의 비율이 두 번째로 높은 유형은 ‘전복’이다.\n\n○ 해양사고 발생 건수는 매년 ‘충돌’이 ‘전복’의 2배 이상이다.\n\n○ 2017～2021년 동안의 해양사고 인명피해 인원 합은 ‘침몰’이 ‘안전사고’의 50% 이하이다.\n\n○ 2020년과 2021년의 해양사고 인명피해 인원 차이가 가장 큰 유형은 ‘화재폭발’이다.'),
'kr-mpm-2024-07-27-psat-d-24':dict(remove=[2],body='보고서\n\n2023년 우리나라 시도 행정심판위원회 처리 건수 상위 5개 시도는 경기, 서울, 경남, 경북, 부산이었다. 2022년에는 인천이 처리 건수 362건으로 상위 5개 시도에 속했으나, 2023년 부산에 자리를 넘겨주었다. 또한, ㉠2023년 처리 건수 상위 5개 시도의 처리 건수는 각각 전년 대비 증가하였다. 인용 건수를 살펴보면, ㉡2023년 처리 건수가 가장 많은 시도의 2023년 인용 건수는 2022년 인용률이 가장 높은 시도의 2022년 인용 건수의 1.5배 이상이다. 인용률을 살펴보면, ㉢2020년부터 2023년까지 인용률이 매년 감소한 시도는 3개이다.',underlines=['㉠2023년 처리 건수 상위 5개 시도의 처리 건수는 각각 전년 대비 증가하였다.','㉡2023년 처리 건수가 가장 많은 시도의 2023년 인용 건수는 2022년 인용률이 가장 높은 시도의 2022년 인용 건수의 1.5배 이상이다.','㉢2020년부터 2023년까지 인용률이 매년 감소한 시도는 3개이다.']),
'kr-mpm-2024-07-27-psat-d-25':dict(remove=[1],body='보기\n\nㄱ. 공장 관리직의 ‘시간당 임금’ 최고액은 35,000원이다.\n\nㄴ. ‘시간당 임금’이 같은 본사 임원은 3명 이상이다.\n\nㄷ. 본사 임원의 ‘시간당 임금’ 평균은 40,000원 이상이다.\n\nㄹ. ‘시간당 임금’이 23,000원 이상인 임직원은 50명 미만이다.'),
'kr-mpm-2023-07-22-psat-d-01':dict(remove=[1],body='입지조건\n\n○ 나들목에서부터 거리가 6km 이내인 장소\n\n○ 역에서부터 거리가 8km 이내인 장소\n\n○ 지가가 30만 원/m² 미만인 장소\n\n○ 해발고도가 100m 이상인 장소'),
'kr-mpm-2023-07-22-psat-d-07':dict(remove=[1],body='보고서\n\n‘갑’국은 우량농지를 보전하고 농지이용률을 높인다는 취지로 농업진흥지역을 지정하고 있다. 그러나, ㉠2014년부터 2022년까지 매년 농업진흥지역 면적은 전체 농지 면적의 50% 이하에 그치고 있다. 또한, ㉡같은 기간 농업진흥지역 면적은 매년 감소하여, 농업기반이 취약해지는 것으로 분석된다.\n\n농업진흥지역 면적은 2013년 91.5만ha에서 2022년 77.6만ha로 15% 이상 감소했으며, 이는 같은 기간 전체 농지 면적의 감소율보다 크다. 한편, ㉢농업진흥지역 면적에서 밭 면적이 차지하는 비중은 2013년 이후 매년 15% 이하이다.',underlines=['㉠2014년부터 2022년까지 매년 농업진흥지역 면적은 전체 농지 면적의 50% 이하에 그치고 있다.','㉡같은 기간 농업진흥지역 면적은 매년 감소하여,','㉢농업진흥지역 면적에서 밭 면적이 차지하는 비중은 2013년 이후 매년 15% 이하이다.']),
'kr-mpm-2023-07-22-psat-d-08':dict(remove=[0],afterBody=True,body='방송뉴스\n\n앵커: 농촌경제 활성화를 위하여 ○○부가 추진해오고 있는 농촌관광 사업이 있습니다. 최근 감염병으로 인해 농촌관광 사업도 큰 어려움을 겪고 있다고 합니다. □□□기자가 어려움을 겪고 있는 농촌관광 사업에 대해 보도합니다.\n\n기자: …(중략)… ‘갑’군은 농촌의 소득 다변화를 위하여 다양한 농촌관광 사업을 추진했습니다. 하지만 감염병 확산으로 2020년 ‘갑’군의 농촌관광 방문객 수와 매출액이 크게 줄었습니다. 농촌체험마을은 2020년 방문객 수와 매출액이 2019년에 비해 75% 이상 감소하였습니다. 농촌민박도 2020년 방문객 수와 매출액이 전년과 비교하여 30% 이상 줄어들었습니다. 다만, 농촌융복합사업장은 2020년 방문객 수와 매출액이 전년과 비교해 줄어든 비율이 농촌체험마을보다는 작았습니다.'),
'kr-mpm-2023-07-22-psat-d-10':dict(remove=[1],body='보기\n\nㄱ. 연도별 전체 발생 건수 상위 2개 연도의 발생 건수 합은 하위 2개 연도의 발생 건수 합의 3배 이상이다.\n\nㄴ. ‘큰 비’가 가장 많이 발생한 해에는 ‘우박’도 가장 많이 발생했다.\n\nㄷ. 1401～1418년 동안의 발생 건수 합 상위 5개 유형은 ‘천둥번개’, ‘큰 비’, ‘벼락’, ‘우박’, ‘짙은 안개’이다.\n\nㄹ. 1402년에 가장 많이 발생한 유형은 1408년에도 가장 많이 발생했다.')}
changes=[]
for path in (ROOT/'assets/psat').glob('*.json'):
 data=read(path)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  if q['id'] not in spec:continue
  old=json.loads(json.dumps(q,ensure_ascii=False));s=spec[q['id']]
  snapshot=OUT/f"before-changes/{q['id']}-r{q['revision']}.json"
  assert not snapshot.exists();write(snapshot,old)
  q['body']=s['body'];q['figures']=[f for i,f in enumerate(old['figures']) if i not in s['remove']]
  if s.get('afterBody'):q['figuresAfterBody']=True
  if 'underlines' in s:q['underlines']=s['underlines'];q['underlineLabelAnchors']=True
  if q['id']=='kr-mpm-2024-07-27-psat-d-24':
   assert '2023년은가로' in q['steps'][3];q['steps'][3]=q['steps'][3].replace('2023년은가로','2023년은 가로')
  if q['id']=='kr-mpm-2024-07-27-psat-d-25':
   assert '이고(x4' in q['steps'][1];q['steps'][1]=q['steps'][1].replace('이고(x4','이고 (x4')
  q['editNote']=old['editNote']+' 보기·조건·보고서의 문장은 원문과 대조하여 본문 글자로 표시한다. 표·그래프·지도와 그 주석·범례의 원형은 유지하며, 원문 화면에서 전체 배치를 확인할 수 있다.'
  q['revision']+=1
  fields=sorted(k for k in old.keys()|q.keys() if old.get(k)!=q.get(k) and k!='revision')
  changes.append(dict(id=q['id'],file=path.relative_to(ROOT).as_posix(),oldRevision=old['revision'],newRevision=q['revision'],changedFields=fields,beforeSnapshot=snapshot.relative_to(ROOT).as_posix(),reason='R605-009: 표·그래프·지도는 원형 보존하고 축소된 긴 문장만 기존 본문으로 옮긴다. 밑줄/기호/수치/조건/자료 순서 보존. 기존 자산·스냅샷 삭제 없음.',status='repaired_pending_reverification'))
  touched=True
 if touched:write(path,data)
assert len(changes)==8
write(OUT/'changes-batch09.json',changes)
write(B/'native-prose-transcriptions.json',dict(status='implemented_pending_verification',transcriptions=spec,originalAssetsRetained=True,dataFiguresNeverRearranged=True,uiCodeChanged=False))
print('Revised eight source prose blocks; original tables/graphs/maps and assets preserved.')
