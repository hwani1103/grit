import hashlib
import review_remaining605 as r
b=r.folder(22);old={x['question']['id']:x['question'] for x in r.read(b/'revealed-current.json')}
old['kr-mpm-2025-11-15-psat-l-22']=r.read(b/'related295-shared22-before.json')
assessments=[
('독립과등확률 구별 및 직전Y 동일조건 비교로ㄴ만참. 반례와 적용범위가 타당하다.','원문 밑줄은 A/B연쇄에만 있으므로 지시문자㉠㉡을 제외한다.',True),
('세 강화사례의 역할을 구분하고ㄴ에 없는 예후를 덧붙이지 않는다. 다만④는ㄴㄷ인데 선지해설이ㄱㄷ을 지목한다.','④의 선택조합을ㄴㄷ으로 바로잡고 빠진ㄱ을 명시한다. 본문의 진단 했지만 어절을 복원한다.',True),
('가능모형4개 모두 설악·지리 제외, 속리·소백 동시선택으로 최대2. 상한과 달성모형이 정확하다.','발견 없음. 역과대우 및 적어도하나의 범위가 정확하다.',False),
('32배치 중 나연·다솜·마현만 유효. 대우와 모순, 논리합 처리 및 모든조건 대입이 타당하다.','발견 없음. 선언문을 배타적선택으로 축소하지 않는다.',False),
('4!×4! 일정 중 화을B/수정C/목병A/금갑D가 유일. 서로다른기사·인접조건을 보존한다.','발견 없음. 정목요일 배제는 다른 선후·기사 조건을 함께 쓰면 타당하다.',False),
('실험별 갑/을 예측 A/B,A/A,B/A와 관찰비교로ㄱ만참. 통제·생존율·강약범위를 정확히 한정한다.','본문100 %의 수치와 백분율기호가 갈라지는 공백을 제거한다.',True),
('초기이론 시간선행 누락이②의 오류. 수정이론의 차폐를 초기이론에 잘못 추가하지 않는다.','표시된 밑줄에 지시문자가 함께 포함되어 원문처럼 지시문자를 제외한다.',True),
('두 열배치에서ㄱㄷ은모두참,ㄴ은전건참·후건거짓 반례가있다. 변화의 지역별기준과 전국수준기준을 구분한다.','발견 없음. 표의 머리글·6개 지시문자·위치가 원문과 맞는다.',False),
('숙종/새은병/활구만일치. 성종철전·원보초·공민왕실패·공양왕소멸의 주체·시점과강한범위가 정확하다.','발견 없음. 외부역사지식을추가하지않는 적용범위도 적절하다.',False),
('일반법칙+실제조건으로사건발생을설명한다는④가 결론과사례를포괄. 도입과핵심·설명과해결책을구분한다.','발견 없음. 과학전반에대한외부주장을추가하지않는다.',False)]
assert not (b/'ratings-before.json').exists()
targetIds=[x['id'] for x in r.read(b/'own-solves.json')]
ratings=[dict(id=qid,scoreBeforeFix=4 if change else 5,assessment=a,deduction=d,needsChange=change) for qid,(a,d,change) in zip(targetIds,assessments)]
r.write(b/'ratings-before.json',dict(method='Same-author pre-edit individual full original/choices/models/host-screen review. Related prior295 historical score preserved separately.',ratings=ratings))
r.write(b/'ratings-frozen.json',dict(frozenAt=r.now(),ratingsSha256=hashlib.sha256((b/'ratings-before.json').read_bytes()).hexdigest(),total=46,count=10,beforeChanges=True))
changes=[]
targets={14,15,19,21,22}
for path in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(path)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  if q['id'] not in old or q['number'] not in targets:continue
  before=old[q['id']];assert q==before
  snap=r.OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();r.write(snap,before)
  if q['number'] in [14,21,22]:q['underlineLabelAnchors']=True
  if q['number']==15:
   assert q['optionReasons'][3]=='ㄱ과 ㄷ은 맞지만 식단 변경 권고를 하고 인정받은 ㄴ도 글의 논거와 일치한다.'
   q['optionReasons'][3]='ㄴ과 ㄷ은 맞지만, 예후를 설명하지 못해 인정받지 못한 ㄱ도 글의 기준을 지지하므로 함께 포함해야 한다.'
   assert '진단 했지만' in q['body'];q['body']=q['body'].replace('진단 했지만','진단했지만')
  if q['number']==19:
   assert '100 %' in q['body'];q['body']=q['body'].replace('100 %','100%')
  q['revision']+=1;touched=True
  changes.append(dict(id=q['id'],file=path.relative_to(r.ROOT).as_posix(),oldRevision=before['revision'],newRevision=q['revision'],changedFields=sorted(k for k in q.keys()|before.keys() if k!='revision' and q.get(k)!=before.get(k)),beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason='원문 밑줄의 지시문자 제외, 선지④ 조합 대응 교정, 본문 단어·백분율 경계 복원. 정답·선지·공식 원문·기존 기록 보존.',status='repaired_pending_reverification'))
 if touched:r.write(path,data)
assert len(changes)==5
r.write(r.OUT/'changes-batch22.json',changes)
sample=[{'id':qid} for qid in targetIds]+[{'id':'kr-mpm-2025-11-15-psat-l-22'}]
r.write(b/'sample-after.json',{'sample':sample})
print('Frozen46/50; four targets and one related prior295 repaired; historical scores retained.')
