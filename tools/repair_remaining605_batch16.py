"""Freeze individual ratings, clarify a sufficient condition, restore word units."""
from pathlib import Path
import datetime,hashlib,json,re
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/psat_remaining605_20261030';B=OUT/'batch16'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
now=lambda:datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).isoformat()
old={x['question']['id']:x['question'] for x in read(B/'revealed-current.json')}
assert not (B/'ratings-before.json').exists() and not (OUT/'changes-batch16.json').exists()
assessments=[
(4,'미등록이면 의무휴업 미적용이라는 대화 후반과 미등록 영업의 별도 고발을 연결한다. 대규모점포·사용승인·등록·휴업 제재를 구분한 해설과 다섯 선지 근거가 정확하다.','본문의 법명 뒤 조사 앞에 삽입된 공백 두 곳을 제거하여 법명과 조사가 따로 줄바꿈되지 않게 한다.'),
(5,'대항력의 제삼자 범위·우선배당의 확정일자 의미·임차인 선택 존중이라는 세 조건부 해석을 별개로 대조하여 ㄱㄴㄷ을 확인했다. 가상법 해석을 현행법으로 일반화하지 않는다.','발견 없음. 조문 제목·항 번호·쟁점별 본문 구획도 원문과 일치한다.'),
(4,'현재 10=제정7+예고2+계류0+미예고1로 ①, 현재70%와 연말 미정치를 분리한다. 예고만으로 완료에 넣지 않고 분모 증가도 고려하는 풀이가 타당하다.','본문의 A 시·60 % 같은 어절 내부 공백을 원문의 A시·60%로 복원해 줄바꿈 단위를 바로잡는다.'),
(4,'갑의 지휘자 자격과 세대 포괄성으로 대표가 된 뒤 A 참가를 도출하는 ①은 정확하다. 제삼자 대표를 포함한 유한 모형에서 다른 네 보기의 반례도 얻었다.','착안점의 A 참가를 보이려면 갑 또는 을의 대표 사실이 필요하다는 표현을 충분조건을 확보하는 풀이 경로로 명확히 고친다. 대표 여부가 A 참가의 논리적 필요조건이라는 역방향은 주어지지 않았다.'),
(5,'학습군 시냅스/운동군 모세혈관의 세포당 변화와 처치를 대응해 ②다. 세포 총수·효과 크기·내부 인과·수행 능력의 미측정 범위를 각 오답과 정확히 연결한다.','발견 없음. 일반화 한계와 실험 결과의 각 수치·변화 부위를 보존한다.'),
(5,'방2의 A 공격/B 미공격과 방2·3의 소리 종류별 차이로 ㄱㄴ이 강화된다. 방1·3 B 정상 탐지는 초음파 사용을 특별히 지지하지 않는다. 강화와 유일 원인 증명을 구분한다.','발견 없음. 유의미하지 않은 0.1초로 우열을 만들거나 방3 초음파 미사용을 단정하지 않는다.'),
(4,'어느 하나 실패→폐기→심리학 연구의 사슬과 중간결론의 두 역할이 정확하다. 추가 목표의 성공 여부를 자유롭게 둔 진리표에서도 기존 결론이 유지된다.','보기 ㄴ 한 문장의 마지막 (6)이 별도 문단으로 떨어져 있다. PDF의 같은 보기 문장으로 합쳐 문장 구조를 회복한다.'),
(5,'㉠ 철학과 ㉡ 모든 지적 작업의 밑줄 범위를 원문에서 확인했다. 필수 귀추만 전면 불필요를 반박하며 경험적 가설을 쓴 연역이 가능하다는 반례로 ㄷ을 배제한다.','발견 없음. 귀납 사용 여부와 필요성의 명제 강도, 철학과 과학의 범위를 구분한다.'),
(5,'기존 산하기관 전 절차와 개선 도 공고·접수·필기/기관 서류·면접·발표를 매핑했다. ㉡=㉧ 서류 심사이고 원문 도표의 기관 상자 범위·빈칸과 픽셀이 일치한다.','발견 없음. 필기 명칭 같아도 평가 능력이 달라지는 점과 면접 담당 보존이 정확하다.'),
(4,'완료 배열 미/완/미와 유사 배열 있/있/없을 두 행에 교환 배치하면 ㄱㄴ 참·ㄷ 거짓이다. 본문 표의 열·밑글자 여섯 개·삽입 위치까지 대조했다.','신청안들을 신청 안들로 분리한 어절을 원문대로 붙여 신청안의 의미와 줄바꿈 단위를 회복한다.')]
ratings=[dict(id=qid,scoreBeforeFix=score,assessment=a,deduction=d,needsChange=score<5) for qid,(score,a,d) in zip(old,assessments)]
assert sum(r['scoreBeforeFix'] for r in ratings)==45
write(B/'ratings-before.json',dict(method='Same-author pre-edit source/option/model and host assessment; eight previously key-exposed solves acknowledged.',ratings=ratings))
write(B/'ratings-frozen.json',dict(frozenAt=now(),ratingsSha256=hashlib.sha256((B/'ratings-before.json').read_bytes()).hexdigest(),total=45,count=10,beforeChanges=True))
changes=[];targets={r['id'] for r in ratings if r['needsChange']}
for path in (ROOT/'assets/psat').glob('*.json'):
 data=read(path)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  if q['id'] not in targets:continue
  previous=old[q['id']];assert q==previous
  snap=OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();write(snap,previous)
  if q['id']=='kr-mpm-2025-07-19-psat-l-24':
   assert q['body'].count('법」 ')==3
   q['body']=q['body'].replace('법」 에','법」에').replace('법」 을','법」을')
  elif q['number']==2:
   assert 'A 시' in q['body'] and '60 %' in q['body']
   q['body']=q['body'].replace('A 시','A시').replace('60 %','60%')
  elif q['number']==6:
   q['steps'][0]='착안점: 주어진 조건문에서 갑 또는 을이 대표라는 사실은 A 참가의 충분조건이다. 이 조건을 확보하기 위해 대표 자격을 ‘직업 조건과 세대 포괄성’의 결합으로 압축하고, 자격을 갖춘 사람은 모두 대표가 된다는 문장을 확인한다.'
   q['steps'][3]='정석 근거: 대표이면 비관료이면서 지휘자 또는 제작자이고 세대 포괄성도 갖춰야 한다. 그 조건을 모두 갖추면 대표라는 역방향도 본문이 명시한다. ②는 세대 포괄성, ③은 직업, ④는 을의 실제 자격, ⑤는 갑·을의 직업이 빠져 있다. 갑 또는 을이 대표라는 것은 A 참가의 충분조건이며, A가 참가하는 다른 경로까지 배제한 필요조건은 아니다.'
  elif q['number']==12:
   assert q['body'].count('위 논증에서\n\n(6)')==1
   q['body']=q['body'].replace('위 논증에서\n\n(6)','위 논증에서 (6)')
  elif q['number']==18:
   assert q['body'].count('신청 안들')==1;q['body']=q['body'].replace('신청 안들','신청안들')
  q['revision']+=1;touched=True
  changes.append(dict(id=q['id'],file=path.relative_to(ROOT).as_posix(),oldRevision=previous['revision'],newRevision=q['revision'],changedFields=sorted(k for k in q.keys()|previous.keys() if k!='revision' and q.get(k)!=previous.get(k)),beforeSnapshot=snap.relative_to(ROOT).as_posix(),reason='충분조건의 방향 명료화 또는 원문 어절·보기 문장 경계 회복. 정답·선지·원문·표·그림·기록 보존.',status='repaired_pending_reverification'))
 if touched:write(path,data)
assert len(changes)==5;write(OUT/'changes-batch16.json',changes)

# Exact wording scope only: keep all other semantics pending until source review.
prior={q['id'] for q in read(OUT/'preparation/previously-scored295.json')['questions']}
fixed={q['id']:i+1 for i,b in enumerate(read(OUT/'preparation/targets605.json')['batches']) for q in b['questions']};candidates=[]
patterns={'law-particle':r'법」 [에을]','city-unit':r'A 시','percent-unit':r'\d %','proposal-word':r'신청 안들','split-option-reference':r'위 논증에서\n\n\(6\)','participation-necessity':r'참가를 보이려면.*필요하다'}
for path in (ROOT/'assets/psat').glob('*.json'):
 data=read(path)
 if not isinstance(data,list):continue
 for q in data:
  # Use frozen target snapshots so repaired members remain in the explicit scope.
  value=old[q['id']] if q['id'] in targets else q
  text=value.get('body','')+'\n'+'\n'.join(value.get('steps',[]))
  hits=[name for name,pattern in patterns.items() if re.search(pattern,text)]
  if hits:candidates.append(dict(id=q['id'],cohort='prior295' if q['id'] in prior else 'fixed605',batch=fixed.get(q['id']),patterns=hits,status='batch16_repaired_pending_verification' if q['id'] in targets else 'pending_source_and_semantic_review'))
write(OUT/'cross-candidates-word-unit-and-conditional-direction.json',dict(cause='R605-013',method='All900 exact selected patterns only; no global necessity/word-spacing clearance.',candidates=candidates))
cross=read(OUT/'cross-validation.json');cross['findings'].append(dict(id='R605-013',batch=16,cause='Sufficient proof route expressed as necessary condition; word-internal spaces and one fragmented option sentence.',targets=sorted(targets),scopeFile='cross-candidates-word-unit-and-conditional-direction.json',candidateCount=len(candidates),prior295Candidates=sum(c['cohort']=='prior295' for c in candidates),status='targets_repaired_pending_verification'));write(OUT/'cross-validation.json',cross)
print('Frozen45/50; clarified l06 and repaired four word/paragraph boundaries. Exact scope candidates:',len(candidates),'prior295:',sum(c['cohort']=='prior295' for c in candidates))
