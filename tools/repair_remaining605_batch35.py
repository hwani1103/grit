import re
import review_remaining605 as r
b=r.folder(35);old={x['question']['id']:x['question'] for x in r.read(b/'revealed-current.json')}
assert 'All tests passed!' in (b/'host-before.log').read_text(encoding='utf-8-sig')
notes={2:'소유자·일시불·지하범위·위험조건·사후통보를 정확히 대조했다. 도시철도건설사업과 지하부분의 원문 줄갈이 어절을 복원한다.',3:'요건의 결합, 부정지정의 의무취소와 청문, 부정지원의 재량취소를 구별했다. 행정안전부장관의 줄갈이 공백을 복원한다. 법률명 따옴표는 이미 맞다.',4:'임의신청·의무신청·대체신청·후속신고가 모두 정확하다. 도난미신청만으로 직권말소하지 않는다는 적용 범위도 명시되어 있다.',5:'기산일·납부능력·집행주체·공개권자·즉시석방을 정확히 대응했다. 경찰서장 어절을 복원하고 조문 밖 주석을 별도 문단으로 분리한다.',6:'진수시2억과 누적8억을 구별하고 지급·매출 기준도 정확하다. 본문과 보기의20 %/5 % 경계를 정리한다.',7:'유물27·궁궐54·유적지67·디지털52의 합계와 모든 차이를 검산했다. 본문 사업과 괄호 사이의 줄갈이 공백을 정리한다.',8:'상한을 포함해0~120 모든 정수 인원을 열거하고42불가능·43가능 및 단조성으로 최소를 검증했다. 설명과 다섯 선지 모두 타당하다.',9:'분수시각의 구간별 실제 궤적을 교차하여 각 쌍2회와甲丙각4회를 확인했다. 출발·끝점·같은방향 제외, 선택지 열 제목이 정확하다.',10:'구매날1·5·13·24·30과 가격·같은색제외·5월경계를 검산하고 표 모든 셀 및 배치 위치를 대조했다. 함정 문구의 구매를하루 띄어쓰기를 고친다.',11:'세번 복원구성과ㄴ/ㄹ한번반례 및5040배열의6번이하 복원을 확인했다. 정석 설명의 배열 표기 앞 공백 두 곳을 보완한다.'}
fix={2,3,5,6,7,10,11};ratings=[dict(id=i,scoreBeforeFix=4 if q['number'] in fix else 5,assessment=notes[q['number']],needsChange=q['number'] in fix,deduction='어절·문장 경계와 주석 표시 개선' if q['number'] in fix else '발견 없음') for i,q in old.items()]
assert not (b/'ratings-before.json').exists();r.write(b/'ratings-before.json',dict(method='Same-author original-only solve then direct source/key/exhaustive models/host before-edit inspection.',ratings=ratings));r.write(b/'ratings-frozen.json',dict(frozenAt=r.now(),ratingsSha256=r.sha(b/'ratings-before.json'),total=43,count=10,beforeChanges=True))
changes=[]
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  if q['id'] not in old or q['number'] not in fix:continue
  prev=old[q['id']];assert prev==q;snap=r.OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();r.write(snap,prev)
  if q['number']==2:q['body']=q['body'].replace('도시 철도건설사업','도시철도건설사업').replace('지하 부분','지하부분')
  if q['number']==3:q['body']=q['body'].replace('행정안전부 장관','행정안전부장관')
  if q['number']==5:
   q['body']=q['body'].replace('한다. ※','한다.\n\n※');q['choices']=[s.replace('경찰 서장','경찰서장') for s in q['choices']]
  if q['number']==6:q['body']=re.sub(r'(20|5) %',r'\1%',q['body'])
  if q['number']==7:q['body']=q['body'].replace('사업 (','사업(')
  if q['number']==10:q['pitfall']=q['pitfall'].replace('구매를하루','구매를 하루')
  if q['number']==11:q['steps']=[s.replace('ㄱ은[','ㄱ은 [').replace('부분열[','부분열 [') for s in q['steps']]
  fields=[k for k in q if prev[k]!=q[k]];assert fields;q['revision']+=1;touched=True
  assert re.sub(r'\s','',q['body'])==re.sub(r'\s','',prev['body']) and [re.sub(r'\s','',s) for s in q['choices']]==[re.sub(r'\s','',s) for s in prev['choices']]
  changes.append(dict(id=q['id'],file=p.relative_to(r.ROOT).as_posix(),oldRevision=prev['revision'],newRevision=q['revision'],changedFields=fields,beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason=notes[q['number']],status='repaired_pending_reverification'))
 if touched:r.write(p,data)
assert len(changes)==7;r.write(r.OUT/'changes-batch35.json',changes)
r.write(b/'repair-semantic-checks.json',dict(status='PASS',changedCount=7,originalWordsAndChoicesPreserved=True,allAnswerAndNumericModelsPreserved=True,tableUnchanged=True,choiceColumnHeader='甲 → 丙',notes=notes))
print('Frozen43/50;7 target revisions;source words/answers/table preserved')
