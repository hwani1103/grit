"""Three prior295 source-confirmed raster-body readability repairs, no rerating."""
from pathlib import Path
import json,copy
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/psat_remaining605_20261030';B=OUT/'batch08'
read=lambda f:json.loads(f.read_text(encoding='utf-8-sig'))
def write(f,v):f.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
ids={x['id'] for x in read(B/'density-prior295-sample.json')['sample']};changes=read(OUT/'changes-batch08.json');assert not ids&{x['id'] for x in changes}
for f in (ROOT/'assets/psat').glob('*.json'):
 qs=read(f)
 if not isinstance(qs,list):continue
 dirty=False
 for q in qs:
  if q['id'] not in ids:continue
  old=copy.deepcopy(q);snap=OUT/'before-changes'/f"{q['id']}-r{q['revision']}.json";assert not snap.exists();write(snap,old)
  if q['id'].endswith('2025-03-08-psat-s-17'):
   q['body']='<민원처리 우수 공무원 선정 기준>\n\n○ 민원처리 점수에 가점 또는 감점을 하여 점수의 총합이 가장 높은 사람을 민원처리 우수 공무원으로 선정한다. 민원처리 점수의 산정 방식과 가점 및 감점 기준은 다음과 같다.\n\n민원처리 점수 = (민원만족도 × 0.8) + (민원처리 건수 × 0.2)\n－ 우수답변 선정 민원 1건당 1점 가점\n－ 미결재 민원 1건당 1점 감점\n－ 처리기간 초과 민원 1건당 1점 감점\n\n○ 민원만족도가 80점 미만이거나 민원처리 건수가 월 40건 미만인 사람은 민원처리 우수 공무원으로 선정될 수 없다.\n\n<상황>\n\n○ A부처는 8월의 민원처리 우수 공무원을 선정하려고 한다.\nA부처 공무원(甲～戊)의 8월 민원처리 현황은 다음과 같다.'
   q['tables']=[dict(caption='8월 민원처리 현황',columns=['구분','민원만족도','민원처리 건수','우수답변 선정 건수','미결재 건수','처리기간 초과 건수'],rows=[['甲','85점','50건','0건','1건','3건'],['乙','80점','40건','3건','0건','0건'],['丙','85점','40건','1건','0건','1건'],['丁','90점','35건','0건','2건','2건'],['戊','75점','55건','4건','1건','1건']],afterParagraph=5)]
  elif q['id'].endswith('2025-03-08-psat-s-18'):
   q['body']='○ 甲사무관은 내년도 예산편성을 위해 증액요청을 한 사업을 대상으로 올해 지출 내역을 정산하고자 한다.\n\n○ 甲사무관이 담당하고 있는 올해 사업(A～E)의 사업비 내역은 다음과 같다.\n\n○ 정산 순서에 대한 규칙은 다음과 같다.\n－ 총사업비 대비 보조금 총액 비율이 높은 사업부터 정산한다.\n－ 총사업비 대비 보조금 총액 비율이 동일한 경우, 보조금 총액이 큰 사업부터 정산한다.\n\n○ 위 규칙에도 불구하고 보조금 미집행액이 있는 사업을 우선하여 정산한다.'
   q['tables']=[dict(caption='사업비 내역 (단위: 천 원)',columns=['사업','총사업비','보조금 총액','보조금 집행액','증액요청 여부'],rows=[['A','250,000','200,000','200,000','○'],['B','30,000','27,000','27,000','○'],['C','125,000','120,000','120,000','×'],['D','90,000','81,000','81,000','○'],['E','82,000','65,600','64,600','○']],afterParagraph=1)]
  else:
   assert q['id']=='kr-mpm-2024-03-02-psat-s-27'
   q['body']='○ A시는 주민의 전기, 상수도, 도시가스 사용량 감축률에 따라 다음년도에 탄소중립포인트를 지급하는 온실가스 감축 제도를 운영하고 있다.\n\n○ 탄소중립포인트 지급기준은 다음과 같다.\n\n○ 감축률(%) = (직전년도 월평균 사용량 − 당해년도 월평균 사용량) / (직전년도 월평균 사용량) × 100\n\n<상황>\n\nA시 주민 甲의 2022년 및 2023년 전기, 상수도, 도시가스 월평균 사용량은 다음과 같다.'
   q['tables']=[dict(caption='탄소중립포인트 지급기준 (단위: 포인트)',columns=['감축률','전기','상수도','도시가스'],rows=[['5% 이상 10% 미만','600','75','300'],['10% 이상 15% 미만','750','150','600'],['15% 이상','1,000','200','800']],afterParagraph=1),dict(caption='2022년 및 2023년 월평균 사용량',columns=['연도','전기(kWh)','상수도(m³)','도시가스(m³)'],rows=[['2022','400','11','60'],['2023','350','10','51']],afterParagraph=4)]
  q['figures']=[]
  q['editNote']='공식 원문의 조건·표의 행과 열·단위·선택지를 유지했습니다. 본문·수식·표는 화면의 공통 글자 크기와 어절 줄바꿈으로 표시합니다. 공식 원문 보기에서 원형을 확인할 수 있습니다. 해설은 GRIT에서 별도로 작성했습니다.'
  fields=sorted(k for k in old.keys()|q.keys() if old.get(k)!=q.get(k));q['revision']+=1;dirty=True
  changes.append(dict(id=q['id'],cohort='prior295',file=f.relative_to(ROOT).as_posix(),oldRevision=old['revision'],newRevision=q['revision'],changedFields=fields,beforeSnapshot=snap.relative_to(ROOT).as_posix(),reason='R605-008연관:기본390화면에서본문까지한이미지에작게축소된다.공식조건·가감점/자격/정산예외/감축률식·모든표셀과단위를기존본문/표컴포넌트로전사한다.기존이미지·원문·과거스냅샷및기존개별점수는보존.',status='repaired_pending_source_host_reverification'))
 if dirty:write(f,qs)
assert ids<={c['id'] for c in changes};write(OUT/'changes-batch08.json',changes)
queue=read(OUT/'cross-candidates-situation-raster-body.json')
for x in queue:
 if x['id'] in ids:x.update(status='source_confirmed_repaired_pending_host_reverification',evidence='batch08/density-prior295-review.json',newRevision=x['revision']+1)
write(OUT/'cross-candidates-situation-raster-body.json',queue)
print('Native body/tables restored for3relatedprior295; no historical score change or lib change.')
