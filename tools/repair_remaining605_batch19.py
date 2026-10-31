"""Freeze two target deductions; restore exact underline strokes and one old control."""
from pathlib import Path
import datetime,hashlib,json,re
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/psat_remaining605_20261030';B=OUT/'batch19'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
now=lambda:datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).isoformat()
old={x['question']['id']:x['question'] for x in read(B/'revealed-current.json')};related=read(B/'related295-shared21-before.json')
assert not (B/'ratings-before.json').exists() and not (OUT/'changes-batch19.json').exists()
assert 'All tests passed!' in (B/'host-before.log').read_text(encoding='utf-8') and 'All tests passed!' in (B/'host-related-before.log').read_text(encoding='utf-8')
assessments=[
(5,'시설/인구와 실제 자기 부담은 두 주장을 검토하지만50~64세 희망자 수는 전체 연령 구성비를 확인하지 못한다. 기존 해설의 분모·정확한 가설 대응은 타당하다. 제 초벌 답⑤는 정책 설계 일반의 유용성을 혼동한 오류로 별도 정정했다.','게시 결함 발견 없음. 최초 자체풀이와 정정 기록을 보존하고 기존 해설의 점수를 자체풀이 오류 때문에 낮추지 않는다.'),
(4,'㉠편파 평가·㉡비편파·㉢고착화의 술어와 방향을 분리해ㄷ만 참이다. 일부 집단 비율·예측 정확성·인종차별 고착을 동일 지표로 보지 않는 해설이 타당하다.','A/B 주장 앞 표지까지 밑줄이 그어지며 원문 마지막 마침표도 밑줄 밖이다. 표지를 위치 앵커로 사용하고 실제 원문 선의 문자 범위만 표시한다.'),
(5,'첫 거절과 동일 청탁 반복을 분리해⑤이며,1인당1만2천원을90명 전체액으로 합치지 않는다. 부정 청탁 아닌 식사·Y입찰·X용도변경의 사실과200만원 상한을 정확히 구분한다.','발견 없음. 실제 현행법 결론으로 일반화하지 않으며 다섯 선지별 판단 단위가 명확하다.'),
(5,'임기 존속과 위법 연임 산입의 해석 차이를 설명하고 C→C→D→C에서 연속성이 끊겨ㄷ을 배제한다. 잔여 임기라는 이유로D를 순서에서 지우지 않는다.','발견 없음. 현실 법률의 확정 해석 대신 선택지에 주어진 조건부 해석으로 판단한다.'),
(5,'주서의 직접 기록과 사헌부의 열람을 근거 문단으로 연결해④다. 승지6/주서3 구성비를 관서 간 총인원 비교로 확대하지 않고 각 업무 공간을 구분한다.','발견 없음. 열람 주체·기록 내용·부당한 왕명 출납 거부에 관한 원문 정보가 보존된다.'),
(5,'주관적 기준 일부를 인정하되 대부분의 객관적 유사성 기반이라는 결론을 대체로의 범위로 보존한④다. 양보와 주결론을 구분한다.','발견 없음. 예외를 모두 배제하거나 예외가 존재한다는 이유로 주관주의로 바꾸지 않는다.'),
(5,'개정 전 처의 부모라는 인척 반례 하나로⑤를 배제하고 두3촌·부계/모계8촌·이모 자녀 혈연을 확인했다. 주어진 목록과 정의만 적용한다.','발견 없음. 촌수의 세대 연결과 최초 도입이라는 전면 주장에 대한 반례가 구체적이다.'),
(4,'호혜성의 주기·받기·되갚기 의무와 혼인의 마찬가지로 연결해④다. 원문의 오류인 권리/자율은 문제 본문에서 유지해야 한다.','첫 밑줄의 원문은 이성적으로 통제할 수 있다까지인데 고까지 더 표시하고 있다. 원문 PDF 선과 문자 중심 좌표를 대조해 어미 고를 밑줄에서 제외한다.'),
(5,'민원/신고와 심사대상/심사관은 적합하고, 적합·부적합 외에 조건부/불심사 두 범주가 남아ㄷ을 검토할 수 없다. 동일 두 비율에서 조건부10%/40%인 반례가 정확하다.','발견 없음. 전체 분할의 누락 범주와 분모를 먼저 확인하는 풀이가 재현 가능하다.'),
(5,'위반한 첫째 인간 생명 원칙에 불가피한 구조 중 인명 피해의 용인을 연결해③이다. 명령 거부와 자기 파손은 이미 상위 원칙 예외로 처리됨을 구별한다.','발견 없음. 구조의 필요·피해의 불가피 조건과 실제 윤리 일반화의 한계가 보존된다.')]
ratings=[dict(id=qid,scoreBeforeFix=score,assessment=a,deduction=d,needsChange=score<5) for qid,(score,a,d) in zip(old,assessments)]
assert sum(r['scoreBeforeFix'] for r in ratings)==48
write(B/'ratings-before.json',dict(method='Same-author pre-edit individual assessment after source/stroke/option/model and host checks. Own l19 wrong answer separately disclosed; four prior key exposures.',ratings=ratings));write(B/'ratings-frozen.json',dict(frozenAt=now(),ratingsSha256=hashlib.sha256((B/'ratings-before.json').read_bytes()).hexdigest(),total=48,count=10,beforeChanges=True))
targets={r['id'] for r in ratings if r['needsChange']};allChanged=targets|{related['id']};changes=[]
for path in (ROOT/'assets/psat').glob('*.json'):
 data=read(path)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  if q['id'] not in allChanged:continue
  previous=related if q['id']==related['id'] else old[q['id']];assert q==previous
  snap=OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();write(snap,previous)
  if q['id']=='kr-mpm-2025-11-15-psat-l-07':
   assert q['underlines'][0]=='이성적으로 통제할 수 있다고';q['underlines'][0]='이성적으로 통제할 수 있다'
  else:
   q['underlines']=['㉠ A의 주장','㉡ B의 주장','㉢ X의 지속적인 사용은 미국 사회의 인종차별을 고착화한다'];q['underlineLabelAnchors']=True
   if q['id']==related['id']:
    assert len(re.findall(r'(?<=\d) %',q['body']))==8
    q['body']=re.sub(r'(?<=\d) %','%',q['body'])
  q['revision']+=1;touched=True
  changes.append(dict(id=q['id'],file=path.relative_to(ROOT).as_posix(),oldRevision=previous['revision'],newRevision=q['revision'],changedFields=sorted(k for k in q.keys()|previous.keys() if k!='revision' and q.get(k)!=previous.get(k)),beforeSnapshot=snap.relative_to(ROOT).as_posix(),reason='원문 밑줄 선의 표지 제외·어미/마침표 범위 복원. 기존21번은 숫자% 어절도 회복. 본문 의미·정답·선지·과거점수·기록 보존.',cohort='prior295' if q['id']==related['id'] else 'fixed605',status='repaired_pending_reverification'))
 if touched:write(path,data)
assert len(changes)==3;write(OUT/'changes-batch19.json',changes)
write(B/'sample-after.json',dict(sample=[dict(id=qid) for qid in old]+[dict(id=related['id'])]))
write(B/'related295-shared21-review.json',dict(status='repaired_pending_host',id=related['id'],oldRevision=related['revision'],newRevision=related['revision']+1,ownSolve='related295-shared21-own.json',officialAnswer=1,previousLabelExclusionAlreadyCorrect=True,furtherChanges='Exact final underline period boundary and eight number-percent word units.',oldScorePreserved=True,notCountedToward605=True,sharedSource='source-underline-boundaries.json'))
scope=read(OUT/'cross-candidates-underline-label.json')
for c in scope:
 if c['id']=='kr-mpm-2021-07-10-psat-l-22':c.update(status='batch19_repaired_pending_host',newRevision=4)
 if c['id']==related['id']:c['followupBatch19']=dict(status='pending_host',newRevision=5,previousLabelFixPreserved=True)
write(OUT/'cross-candidates-underline-label.json',scope)
scope=read(OUT/'cross-candidates-word-unit-and-conditional-direction.json')
for c in scope['candidates']:
 if c['id']==related['id']:c.update(status='batch19_repaired_pending_host',verification='batch19/related295-shared21-review.json')
write(OUT/'cross-candidates-word-unit-and-conditional-direction.json',scope)
cross=read(OUT/'cross-validation.json')
for f in cross['findings']:
 if f['id']=='R605-006':f.setdefault('additionalScopes',[]).append('batch19/source-underline-boundaries.json')
cross['relatedPrior295Reviews'].append(dict(id=related['id'],batch=19,causeFamilies=['R605-006','R605-013'],evidence='batch19/related295-shared21-review.json',status='repaired_pending_host',scorePreserved=True));write(OUT/'cross-validation.json',cross)
write(B/'review-method-refinement.json',dict(trigger='Own l19 answer5→3 correction',rule='For required-data questions, identify the exact speaker hypothesis, variable and denominator before judging each proposed dataset. General usefulness for policy design is insufficient to verify a specific claim.',originalSolveAndScorePreserved=True,notAPublishedContentError=True))
print('Frozen48/50; two target underline repairs + one shared prior295 control refinement. Original own answer error preserved.')
