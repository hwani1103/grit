import re
import pdfplumber
from PIL import Image
import review_remaining605 as r
b=r.folder(41);old={x['question']['id']:x['question'] for x in r.read(b/'revealed-current.json')};src={x['id']:x for x in r.read(b/'blind-source.json')}
assert 'All tests passed!' in (b/'host-before.log').read_text(encoding='utf-8-sig') and r.read(b/'source-key-model-checks.json')['status']=='PASS'
notes={10:'양의정수유일해(1,3,5,6,9),a홀수와a≥3합39초과,절댓값두분기정확. 절댓값앞해설공백을보완한다.',12:'필수2코드포함15조합과B단독최다DD포함반례,제외끝자리합2논증정확. 작은이미지에포함된처리조건/보기를본문크기로분리하고원본도입/표는보존한다.',14:'정보집합3600→84→3→1로모든발언과유일A→B확인.교환대칭/화자자기정보제약을정확히설명한다.발견없음.',16:'민서조건·시험변경·개별공연할인표및최저96000정확.작은대화이미지를네이티브본문으로옮기고표는원형유지.②88000을할인액이라쓴표현을할인후가격으로명확히한다.',19:'각도상대·위도방향·유지비·.5×2×30과원문MW/물리MWh구분이미정확.메가와트괄호앞어절을연결한다.',20:'480/200000두단위계산과독립기간·두빈칸유일성정확.공통지문의MW괄호연결.',22:'한정대상·발신방향·철인무색·한글표기·중앙상단모두원문일치.발견없음.',25:'등록대상건물·연월환산·지역한도동일포함·각선지계산정확.주석도조항밖표시확인.발견없음.',26:'제조온도와냉각·흡착/연료용도·민간믿음과효능구별모두정확.발견없음.',27:'128온스의이동/소비/잔량보존및5컵32테이블스푼정확.5ml어절과상황표제의명시적문단경계정리.'}
fix={10,12,16,19,20,27};ratings=[dict(id=i,scoreBeforeFix=4 if q['number'] in fix else 5,assessment=notes[q['number']],needsChange=q['number'] in fix,deduction='본문이미지읽기/용어/어절정리' if q['number'] in fix else '발견없음') for i,q in old.items()]
assert not (b/'ratings-before.json').exists();r.write(b/'ratings-before.json',dict(method='Original-only solving and exact enumeration frozen before reveal; source/key/pixels and pre-edit host reviewed.',ratings=ratings));r.write(b/'ratings-frozen.json',dict(frozenAt=r.now(),ratingsSha256=r.sha(b/'ratings-before.json'),total=44,count=10,beforeChanges=True))
body12='甲은 오늘 ‘휴폐업신고서 관리’, ‘신고서 목록 관리’를 포함하여 업무코드가 서로 다른 6건의 업무를 처리했다.\n\n<보 기>\n\nㄱ. ‘A’를 1번만 입력했다면, ‘D’는 3번 입력했다.\n\nㄴ. 가장 많이 입력한 알파벳이 ‘B’라면, ‘전자계산서 발급 조회’를 처리하지 않았다.\n\nㄷ. 입력한 업무코드 네 번째 자리의 숫자 총합이 21이라면, ‘신고자내역 조회’를 처리했다.'
body16='다음은 인영과 민서가 아래 <표>를 보면서 나눈 <대화>이다.\n\n<대 화>\n\n인영: 이번에 좋은 공연이 많던데, 나는 뮤지컬 공연을 보고 싶어.\n\n민서: 나는 지난달에 바이올린 협주 공연을 보고 와서 이번엔 다른 공연에 가려고 해.\n\n인영: 그런데 티켓 가격이 조금 부담스럽지 않아? 너는 학생할인을 받을 수 있어서 조금 더 저렴하게 공연을 볼 수 있겠다.\n\n민서: 맞아. 그래서 결제할 금액이 제일 저렴한 공연을 볼 생각이야.\n\n인영: 그렇구나. 시험이 10월 11일이라 그 전에는 가기 어렵겠어.\n\n민서: 아니야. 시험일정이 10월 9일로 바뀌어서 그 전만 아니면 괜찮을 거야. 그보다 B시는 우리집에서 너무 멀어서 안 가려고.'
norm=lambda s:re.sub(r'\s','',s)
changes=[];crops=[]
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  if q['id'] not in old or q['number'] not in fix:continue
  prev=old[q['id']];assert q==prev;n=q['number'];snap=r.OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();r.write(snap,prev)
  if n==10:q['steps']=[s.replace('丁은|','丁은 |').replace('24와|','24와 |') for s in q['steps']]
  if n in [12,16]:
   original=q['figures'][0]['asset'];box=(0,0,1340,656) if n==12 else (0,1024,1340,1742);asset=f'assets/psat/figures/2025grade5-s{n}-table-review605.png';assert not (r.ROOT/asset).exists()
   with Image.open(r.ROOT/original) as im:cropped=im.crop(box);cropped.save(r.ROOT/asset);size=cropped.size
   q['figures']=[dict(asset=asset,caption='업무코드 정의와 원본 표' if n==12 else '공연 가격·일정·장소·학생할인 원본 표',width=size[0],height=size[1])]
   q['body']=body12 if n==12 else body16
   if n==16:q['figuresAfterBody']=True;q['optionReasons'][1]=q['optionReasons'][1].replace('오케스트라의 할인액','오케스트라의 할인 후 가격')
   s=src[q['id']]['sourceText'];part=s[s.index('甲은 오늘'):s.index('①')] if n==12 else s[s.index('다음은 인영'):s.index('<표>\n')]
   assert norm(part)==norm(q['body'])
   with Image.open(r.ROOT/asset) as new,Image.open(r.ROOT/original) as im:assert new.tobytes()==im.crop(box).tobytes()
   crops.append(dict(id=q['id'],originalAsset=original,newAsset=asset,pixelBoxWithinOriginal=list(box),source=src[q['id']]['source'],page=src[q['id']]['page'],sourceProseExactIgnoringWhitespace=True,sourceGeometryUnchanged=True,oldAssetPreserved=True))
  if n in [19,20]:q['body']=q['body'].replace('MW (메가와트)','MW(메가와트)')
  if n==27:q['body']=q['body'].replace('5 ml','5ml').replace('<상 황> 처음에','<상 황>\n\n처음에')
  assert q!=prev and q['answer']==prev['answer'] and q['choices']==prev['choices'];fields=sorted(k for k in q if q[k]!=prev.get(k));q['revision']+=1;touched=True
  changes.append(dict(id=q['id'],file=p.relative_to(r.ROOT).as_posix(),oldRevision=prev['revision'],newRevision=q['revision'],changedFields=fields,beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason=notes[n],status='repaired_pending_reverification'))
 if touched:r.write(p,data)
assert len(changes)==6;r.write(r.OUT/'changes-batch41.json',changes)
r.write(b/'repair-semantic-checks.json',dict(status='PASS',count=6,crops=crops,sourceProseAndGeometryPreserved=True,sourceMWNotationAndPhysicalUnitCaveatPreserved=True,allAnswersChoicesUnchanged=True))
print('Frozen44/50;6repairs;2native prose promotions with original table crops')
