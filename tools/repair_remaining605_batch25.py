import shutil
import review_remaining605 as r
b=r.folder(25);before={x['question']['id']:x['question'] for x in r.read(b/'revealed-current.json')}
notes={4:'두 철학의 개선 가능성이라는 공통점과 관계 필요성의 차이를 분리한다. 근거 없는 사회적 지위 주장을 배제한다.',6:'세 분류 및 ㄱ만 참이라는 정답·해설은 정확하다. 원문은 전이 두 글자만 밑줄인데 현재 따옴표까지 포함하여 표시 범위를 수정한다.',9:'세 발언의 비교집단·조사 변수를 각각 대응하며 조사 적절성과 인과 확증을 구별한다. 자료 조사 밑줄도 원문과 일치한다.',10:'19/34/49세 경계와 거주지·중소기업 자격을 구별한다. 신청 자격을 이미 지급된 바우처의 사용 규정과 혼동하지 않는다.',11:'자연류·생식격리·동소분화의 필요조건 세 개를 정확히 방향화하고 H참 S거짓 반례로 충분조건의 역추론을 배제한다.',13:'A의 내적 상태 필요조건 주장과 B의 판단 유보를 구분한다. 유보를 부정이나 긍정으로 확대하지 않는다.',14:'파장 C>B>A, 에너지·주파수 A>B>C, 크기 A<B<C를 일관되게 연결한다. 보기 머리말과 최소 A/C가 정확하다.',19:'변수 고정 조건을 지켜 짧은 파장·큰 조리개·무거운 원자를 도출한다. X의 관찰을 모든 원인의 확정으로 확대하지 않는다.',20:'상대 종이 있는 때와 제거된 때의 생장률을 기준으로 P(+,-),Q(0,+),R(-,0)를 산출한다. 편리·편해 주체 방향과 세 보기 판단이 정확하다.',23:'원문 두 도식의 모든 기관·절차·순서가 네이티브 표와 대응한다. 서류평가와 심의를 구별하여 ㉢→㉠ 교부를 확정한다.'}
ratings=[dict(id=qid,scoreBeforeFix=4 if q['number']==6 else 5,assessment=notes[q['number']],deduction='원문 밑줄 범위 복원' if q['number']==6 else '발견 없음',needsChange=q['number']==6) for qid,q in before.items()]
assert not (b/'ratings-before.json').exists()
r.write(b/'ratings-before.json',dict(method='Same-author pre-edit original/own solve/key/5 steps/5 options/host review, not independent.',ratings=ratings))
r.write(b/'ratings-frozen.json',dict(frozenAt=r.now(),ratingsSha256=r.sha(b/'ratings-before.json'),total=49,count=10,beforeChanges=True))
changes=[]
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  if q['id']!='kr-mpm-2026-07-18-psat-l-06':continue
  old=before[q['id']];assert old==q
  snap=r.OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();r.write(snap,old)
  q['underlines']=['㉠ ‘전이’'];q['underlineLabelAnchors']=True;q['revision']+=1;touched=True
  changes.append(dict(id=q['id'],file=p.relative_to(r.ROOT).as_posix(),oldRevision=old['revision'],newRevision=q['revision'],changedFields=['underlines','underlineLabelAnchors'],beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason='Label-scoped quoted anchor excludes circled label and both quote marks; repeated unlabelled 전이 remains unmarked.',status='repaired_pending_reverification'))
 if touched:r.write(p,data)
assert len(changes)==1;r.write(r.OUT/'changes-batch25.json',changes)
source=r.ROOT/'lib/psat_text.dart';snap=b/'psat_text-before.dart';assert not snap.exists();shutil.copyfile(source,snap)
r.write(b/'renderer-before.json',dict(file='lib/psat_text.dart',beforeSha256=r.sha(source),beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason='Source-confirmed quote boundary on a labelled exact phrase; opt-in existing anchor flag. Vitamin code and all other baseline files stay byte-identical.'))
print('Frozen49/50. One target revision advanced; renderer BEFORE snapshot retained.')
