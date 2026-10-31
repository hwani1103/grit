import re,pdfplumber
from PIL import Image
import review_remaining605 as r
b=r.folder(62);old={q['id']:q for q in r.read(b/'before.json')};reg={x['newAsset']:x for x in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/native-image-repairs.json')['figures']}
assert 'All tests passed!' in (b/'host-before.log').read_text(encoding='utf-8-sig');assert r.read(b/'terminal-period-check.json')['status']=='PASS'
body={5:'<보고서>\n\n‘갑’국의 주택 수는 2022년 1,813만 호에서 2023년 1,853만 호로 2.2% 증가하였다. 개인소유 주택 수는 2022년 1,569만 호에서 2023년 1,597만 호로 1.8% 증가하였다. 주택소유 가구 수는 2022년 1,146만 가구에서 2023년 1,173만 가구로 2.4% 증가하였지만, 가구 주택소유율은 2022년 56.3%에서 2023년 56.0%로 감소하였다. 2023년 지역별 가구 주택소유율을 살펴보면, 상위 3개 지역은 A(64.4%), B(63.0%), C(61.0%)로 나타났다.',
7:'<보고서>\n\n‘갑’국에서 배달대행과 퀵서비스 업종에 종사하는 운전자 실태를 조사한 결과는 다음과 같다. 두 업종 모두 이륜자동차를 이용하여 유사한 형태의 서비스를 제공하지만, 운전자 특성에는 큰 차이가 있었다. 우선, 운전자 평균 연령은 퀵서비스가 57.8세로 배달대행 33.2세보다 높았다. 이는 배달대행은 30대 이하 운전자 비중이 전체의 70% 이상이지만 퀵서비스는 50대 이상 운전자가 전체의 80% 이상을 차지하기 때문이다. 운전자의 이륜자동차 운전 경력의 평균과 서비스 제공 경력의 평균도 각각 퀵서비스가 배달대행에 비해 10년 이상 길었다. 한편, 운전자가 배달대행이나 퀵서비스 시장에 진입하기 위해서는 이륜자동차 구입 비용이 소요되는데, 신차와 중고차 구입 각각에서 배달대행이 퀵서비스보다 평균 구입 비용이 높았다. 또한, 운행시간과 운행 외 시간을 합한 일평균 근로시간은 배달대행이 퀵서비스보다 1.0시간 길었고, 월평균 근로일수도 배달대행이 퀵서비스보다 3일 이상 많은 것으로 나타났다.',
10:'<보고서>\n\n안전 체험 시설이 없는 지역으로 찾아가는 ‘어린이 안전 체험 교실’ 사업이 2017년부터 2023년까지 운영되었다. 해당 기간 동안 참여 자치 단체 수, 운영 횟수 등이 변화하였는데 그중 참여 자치 단체 수와 교육 참여 〔A〕 수의 전년 대비 증감 방향은 매년 같았다.\n\n2021년은 사업 기간 중 참여 자치 단체 수가 가장 많았던 해로 2020년보다 운영 횟수와 교육 참여 어린이 수가 늘었다. 운영 횟수당 교육 참여 어린이 수는 2021년이 2020년보다 〔B〕.\n\n본 사업에 자원봉사자도 꾸준히 참여하였다. 2019년에는 사업 기간 중 가장 많은 자원봉사자가 참여하였다. 자원봉사자당 교육 참여 어린이 수는 2019년이 2017년보다 〔C〕.',
16:'<보 기>\n\nㄱ. ‘전통공예시설’과 ‘한옥숙박시설’의 전년 대비 증감 방향은 매년 같다.\n\nㄴ. 전체 공공한옥시설 중 ‘문화전시시설’의 비율은 매년 20% 이상이다.\n\nㄷ. 2020년 대비 2022년 공공한옥시설의 유형별 증가율은 ‘주거체험시설’이 ‘주민이용시설’의 2배이다.\n\nㄹ. ‘한옥숙박시설’이 ‘주거체험시설’보다 많은 해는 2017년과 2018년뿐이다.'}
norm=lambda s:re.sub(r'\s','',s)
proof=[];plans={}
for n,txt in body.items():
 i=f'kr-mpm-2024-07-27-psat-d-{n:02d}';q=old[i];fi=0 if n in [5,10] else 1;f=q['figures'][fi];v=reg[f['asset']]
 with pdfplumber.open(r.ROOT/v['source']) as pdf:
  p=pdf.pages[v['page1based']-1];whole=p.crop(v['rect']).extract_text();cut=242 if n==5 else 318 if n==10 else None
  if cut:head=p.crop([v['rect'][0],v['rect'][1],v['rect'][2],cut]).extract_text();tail=whole[len(head):];assert norm(head+tail)==norm(whole)
  else:tail=whole
 expected=txt.replace('〔','').replace('〕','');assert norm(tail)==norm(expected),(n,tail,expected)
 plans[i]=(n,txt,fi,f,v,cut);proof.append(dict(id=i,source=v['source'],page=v['page1based'],replacedText=txt,normalizedWholeSourceExact=True,blankMarkerConvention='Source rectangle A/B/C represented by〔A〕/〔B〕/〔C〕; no completed answer inserted.' if n==10 else None))
assert not (b/'followup-assessment.json').exists();r.write(b/'followup-assessment.json',dict(scope='Four already-solved605 raster readability follow-ups plus six terminal-period controls. Original scores retained.',items=[dict(id=i,needsChange=i in plans,currentReadability=3 if i in plans else 5,reason='Long raster prose/choices converted to native; all original tables/formulas/charts retained.' if i in plans else 'All20 terminal dots covered by original strokes; no typography change.') for i in old]))
changes=[]
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  if q['id'] not in plans:continue
  n,txt,fi,f,v,cut=plans[q['id']];prev=old[q['id']];assert q==prev;snap=r.OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();r.write(snap,prev)
  if cut:
   asset=f'assets/psat/figures/2024-d{n:02d}-table-review605.png';height=int((cut-v['rect'][1])*v['resolution']/72)
   with Image.open(r.ROOT/f['asset']) as im:im.crop((0,0,im.width,height)).save(r.ROOT/asset)
   q['figures'][fi]=dict(asset=asset,width=f['width'],height=height,caption='원본 표·정보 수식' if n==5 else '원본 사업 운영 현황 표');proof[[x['id'] for x in proof].index(q['id'])]['newCrop']=dict(newAsset=asset,oldAsset=f['asset'],pixelBoxWithinOriginal=[0,0,f['width'],height],sourcePDFBox=[v['rect'][0],v['rect'][1],v['rect'][2],cut])
  else:q['figures'].pop(fi)
  q['body']=txt;q['bodyAfterFigureCount']=1
  fields=[k for k in q if q[k]!=prev.get(k)];q['revision']+=1;touched=True;changes.append(dict(id=q['id'],file=p.relative_to(r.ROOT).as_posix(),oldRevision=prev['revision'],newRevision=q['revision'],changedFields=fields,beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason='Raster prose readability follow-up; original semantics and graphics preserved.',status='repaired_pending_reverification'))
 if touched:r.write(p,data)
assert len(changes)==4;r.write(r.OUT/'changes-batch62.json',changes);r.write(b/'repair-semantic-checks.json',dict(status='PASS',checks=proof,originalScoresRetained=True,allAnswersExplanationsChoicesUnchanged=True,allOriginalAssetsPreserved=True));r.write(b/'after-sample.json',r.read(b/'sample.json'))
print('Four native prose improvements; six period controls unchanged; no score overwrite')
