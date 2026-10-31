"""Freeze source-specific assessments and correct one strict-boundary phrase."""
from pathlib import Path
import datetime,hashlib,json,re
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/psat_remaining605_20261030';B=OUT/'batch17'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
now=lambda:datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).isoformat()
old={x['question']['id']:x['question'] for x in read(B/'revealed-current.json')}
assert not (B/'ratings-before.json').exists() and not (OUT/'changes-batch17.json').exists()
assessments=[
(5,'명령 없는 출납 금지와 관리관→출납/계약담당의 명령·청구, 출납→관리관의 보고를 대조해①이다. 타 관서 위임과 외부 보관 판단 주체도 구별한다.','발견 없음. 이름이 비슷한 직책의 권한을 섞지 않으며 조문 제목·항 번호도 원문과 일치한다.'),
(5,'불법검열의 징역·자격정지 병과 범위와 단말기번호의 별도 벌칙·정당한 개통 예외를 확인했다. 자기 참여 대화 판단을 모든 법률의 증거능력 보장으로 넓히지 않는다.','발견 없음. 다섯 선지의 행위와 제재 조합을 개별로 설명한다.'),
(5,'500미만 자격/GED 우선/F선순위와 개별한도·반액·잔액의 최솟값을 각각 적용해F1.6억이다. G2억과100이하 경계도 원문 표28셀과 일치한다.','발견 없음. 전체를 곱 하나로 정렬하지 않고 우선집단과 잔액 규칙을 보존한다.'),
(5,'240+3x>440으로x≥67 하한을 잡고 20/13/0/67로 총100 달성을 확인했다. 전체 노력 정수배분 열거에서도 최소67이다. 나머지 노력 분산을 생략하지 않는다.','발견 없음. 66의 불가능 근거와67의 실제 역량420/439/440/441을 함께 제시한다.'),
(5,'양끝 두 합의 차4와 중간합 홀짝으로B24/C20이다. 양의 정수 네 수 전수열거에서30/24/20/15 유일이며 비정수 대안도 모든 합을 만족해 정수 조건의 필요성을 확인한다.','발견 없음. 가운데 두 합의 순서를 임의로 고정하지 않는다.'),
(5,'첫 종 정각에서6회5간격→11회10간격의 비로12초를 구한다. 일정 간격과 첫 사건이 시작점이라는 가정을 분리하며 종 지속시간을 추가하지 않는다.','발견 없음. 최단 풀이와1.2초 정석 검산이 일치한다.'),
(5,'공통6단위로甲1/乙2/丙4/丁5/戊2를 구해丙2위다. 완료·잔여 보존식과 독립 분수 검산이 일치하고 乙·戊 동점을 두 번째로 오인하지 않는다.','발견 없음. 전체 일이 같은 조건과 잔여의 절반을 명시한다.'),
(4,'乙>甲>丙>丁=4에서최소합3x+7≤30과실제배분8/11/7/4로丙최대7이다. 자연수 분배 전수열거도 일치한다.','정답 선지 근거의8이상은최소합31을넘는다는 문구는8에서정확히31인경계를잘못표현한다. 최소합이31이상으로총점30을넘는다고 바로잡는다.'),
(5,'면적6/3/2와변동비9/6/3만·고정비0/20/5만을 분리한다. 여섯재료배치 중 지푸라기/나무/벽돌의23/38/18만원만 둘째최대이며 원문 가격·개수 표와 일치한다.','발견 없음. 고정 지지대 비용을 면적에 곱하지 않으며 둘째벽돌 후보를 최선배치에서도 배제한다.'),
(4,'결과와빈도 이중조건으로A/D/E만통과한다. 일반세균 월완화 제외와10%이하 이력의 필요성을 정확히 구별하고 더빈번한 검사도허용한다. 표두개의 모든값과주석을대조했다.','각각월1회의붙은어절을각각 월1회로고쳐주기 비교문장의단어경계를회복한다. 규정·수치·정답 변경은없다.')]
ratings=[dict(id=qid,scoreBeforeFix=score,assessment=a,deduction=d,needsChange=score<5) for qid,(score,a,d) in zip(old,assessments)]
assert sum(x['scoreBeforeFix'] for x in ratings)==48
write(B/'ratings-before.json',dict(method='Same-author pre-edit original source, all options, exhaustive numeric witnesses and host review.',ratings=ratings));write(B/'ratings-frozen.json',dict(frozenAt=now(),ratingsSha256=hashlib.sha256((B/'ratings-before.json').read_bytes()).hexdigest(),total=48,count=10,beforeChanges=True))
targets={x['id'] for x in ratings if x['needsChange']};changes=[]
for path in (ROOT/'assets/psat').glob('*.json'):
 data=read(path)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  if q['id'] not in targets:continue
  previous=old[q['id']];assert q==previous
  snap=OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();write(snap,previous)
  if q['number']==11:
   assert '최소합 31을 넘으므로' in q['optionReasons'][1]
   q['optionReasons'][1]=q['optionReasons'][1].replace('최소합 31을 넘으므로','최소합이 31 이상으로 총점 30을 넘으므로')
  else:
   assert '각각월' in q['steps'][1];q['steps'][1]=q['steps'][1].replace('각각월','각각 월')
  q['revision']+=1;touched=True
  changes.append(dict(id=q['id'],file=path.relative_to(ROOT).as_posix(),oldRevision=previous['revision'],newRevision=q['revision'],changedFields=['optionReasons'] if q['number']==11 else ['steps'],beforeSnapshot=snap.relative_to(ROOT).as_posix(),reason='x=8에서최소합31은정확한경계이며초과대상은총점30임을명확히함.각각 월의단어경계수정.정답·원문·선지·표·기록보존.',status='repaired_pending_reverification'))
 if touched:write(path,data)
assert len(changes)==2;write(OUT/'changes-batch17.json',changes)
prior={q['id'] for q in read(OUT/'preparation/previously-scored295.json')['questions']};hits=[]
for path in (ROOT/'assets/psat').glob('*.json'):
 data=read(path)
 if not isinstance(data,list):continue
 for q in data:
  value=old[q['id']] if q['id'] in targets else q;text='\n'.join(value.get('steps',[])+value.get('optionReasons',[]))
  patterns=[p for p in [r'최소합\s*31을\s*넘',r'각각월'] if re.search(p,text)]
  if patterns:hits.append(dict(id=q['id'],cohort='prior295' if q['id'] in prior else 'fixed605',patterns=patterns,status='batch17_repaired_pending_verification' if q['id'] in targets else 'pending_source_and_semantic_review'))
write(OUT/'cross-candidates-minimum-boundary31.json',dict(cause='R605-014',method='All900 exact two selected patterns only; broader bound reasoning remains separate.',candidates=hits))
cross=read(OUT/'cross-validation.json');cross['findings'].append(dict(id='R605-014',batch=17,cause='Exact minimal sum31 atx8 must be compared against budget30, not described as strictly exceeding31; one word boundary.',targets=sorted(targets),scopeFile='cross-candidates-minimum-boundary31.json',candidateCount=len(hits),prior295Candidates=sum(h['cohort']=='prior295' for h in hits),status='targets_repaired_pending_verification'));write(OUT/'cross-validation.json',cross)
print('Frozen48/50; two revisions. Exact-pattern candidates',len(hits),'prior295',sum(h['cohort']=='prior295' for h in hits))
