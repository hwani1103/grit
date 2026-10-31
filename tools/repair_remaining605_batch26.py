import review_remaining605 as r
b=r.folder(26);before={x['question']['id']:x['question'] for x in r.read(b/'revealed-current.json')}
notes={23:'양의 가중평균 사이값 성질로ㄱㄴ을 입증하고 ㄷ에는 기존 해설 b0/c1과 새 풀이 b3/c3.5의 두 반례가 있다. 과목수 동일 가정을 일반화하지 않는다.',24:'첫 출발·마지막 도착의 재고 상한을 구별하고 양의 서로 다른 이동량으로1+2를 확정한다. 행위자 본인 창고 제외까지 반영한16개 완전 경로와 실제 달성 예를 검산했다.',2:'기본계획과 구역지정의 서로 다른 절차, 수립주기5년과 계획기간10년, 준용 항의 고시·통지 범위를 정확히 구별한다.',3:'위원장·임명권자·설치단위·심의대상·통합 조례 요건을 모두 대조했다. 위원장=부단체장, 임명=단체장 구분이 명확하다.',4:'판사3인 합의부 구성과 기술심리관 참여, 대법원장 임명, 재판장 명·허가, 서면/구술·비공개 범위를 정확히 대응한다.',6:'1→7호봉의 세 번 증가, 이월상한5, 올해사용4.5를 분리하여18.5일. 0.5단위·월할계산 금지·전년도 사용 중복 차감 방지가 정확하다.',7:'화물별5천·5천·8천, 전체10%할인16200 계산과 모든 오답의 누락/올림 함정 설명은 정확하다. 본문10 %의 수치·기호 공백은 줄바꿈 경계가 되므로 연결한다.',8:'금요일 후속수업 불가, C의 희소성, 연속 마하하타 금지를 적용한 전체 가능 일정은3개. 다섯 선지의 가능/불가능·상한을 모두 확인했다.',10:'원문표의 빈 인증칸과 날짜를 모두 대응하고2019-07-01등록경계·기준일전인증·업종별매출·자산미만 조건을 대조했다. D만 전 조건 충족한다.',11:'제2호 양수인만 단서 적용, 결격상속인의 일단승계 후6개월양도,30일신고와 경미변경신고의 구분이 정확하다.'}
ratings=[dict(id=qid,scoreBeforeFix=4 if q['number']==7 else 5,assessment=notes[q['number']],deduction='백분율 수치·기호 경계 복원' if q['number']==7 else '발견 없음',needsChange=q['number']==7) for qid,q in before.items()]
assert not (b/'ratings-before.json').exists();r.write(b/'ratings-before.json',dict(method='Same-author pre-edit original/own solve/key/all options/models/host review, not independent.',ratings=ratings));r.write(b/'ratings-frozen.json',dict(frozenAt=r.now(),ratingsSha256=r.sha(b/'ratings-before.json'),total=49,count=10,beforeChanges=True))
changes=[]
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  if q['id']!='kr-mpm-2026-07-18-psat-s-07':continue
  old=before[q['id']];assert q==old and q['body'].count('10 %')==1
  snap=r.OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();r.write(snap,old)
  q['body']=q['body'].replace('10 %','10%');q['revision']+=1;touched=True
  changes.append(dict(id=q['id'],file=p.relative_to(r.ROOT).as_posix(),oldRevision=old['revision'],newRevision=q['revision'],changedFields=['body'],beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason='Prevent percentage number and sign from separating during word wrapping. Only one whitespace removed; all values and meanings preserved.',status='repaired_pending_reverification'))
 if touched:r.write(p,data)
assert len(changes)==1;r.write(r.OUT/'changes-batch26.json',changes);print('Frozen49/50; one target percent boundary repaired.')
