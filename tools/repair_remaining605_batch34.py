import re
import review_remaining605 as r
b=r.folder(34);before={x['question']['id']:x['question'] for x in r.read(b/'revealed-current.json')}
assert 'All tests passed!' in (b/'host-before.log').read_text(encoding='utf-8-sig')
notes={3:'반원형 객석·무대의 이중 지위와 마지막 문단의 문화적 의미를 정확히 대응하며 다른 건축물·지형으로의 범위 확장을 배제한다.',5:'대체어 길이 차이와 암호 방향·포로 반례·사전 목적이 정확하다. 심지어 뒤에서 문장이 두 문단으로 끊긴 부분을 원문 단락으로 복원한다.',6:'세 주체와 시대·이론화 단계를 분리하고 성상 비판 논리의 재적용을 정확히 찾는다. 의미 확장과 대체, 명명과 신앙 수용을 혼동하지 않는다.',7:'의도된 투사 방향 오류와 다섯 수정안을 올바르게 판단했다. 다만 ㉤ 밑줄이 것을에서 끊겨 원문의 막아 준다까지 복원하고 첫 방어기제의 줄갈이 공백을 정리한다.',8:'필요조건과 충분조건의 방향 및 두 사상가의 공적 영역에 대한 태도 차이는 정확하다. 제목의 충분한은 내면 역량만으로 충분하다는 오해를 줄 수 있어 삭제하고 붙은 괄호 앞 띄어쓰기를 개선한다.',9:'이미 과학적 합의가 있는 상황의 기계적 동등 비중 보도를 반례로 삼는다. 규범 폐지나 판단 유보·보도 금지로 확대하지 않은 해설이 타당하다.',10:'쟁기·생산성·공동체 사육 및 같은 농지의1/2와2/3 경작비율을 정확히 대조한다. 원문 줄갈이에서 생긴38 % 분리를 복원한다.',11:'숙주 분비→균류 공생과 스트리가 신호 이용, 파종 전 제거 및 비용 한계를 정확히 구별한다. 화학물질의 줄갈이 공백을 복원한다.',12:'실력 안정성과 낮은 행운 반복의 문맥상 보완은 맞다. 다만 낮은 성공 확률 상한 자체에는 실력 안정성 전제가 필수이지 않으므로 개별 이유의 필요한 표현과 적용 한계를 정교화한다.',22:'성명 공통 허가와 성의 추가 제한을 분리한다. 본과 혈통, 양계·윗세대 글자 증가, 악용 거부 가능성의 근거가 맞으며 현실 법률 안내로 확대하지 않는다.'}
fix={5,7,8,10,11,12}
ratings=[dict(id=i,scoreBeforeFix=4 if q['number'] in fix else 5,assessment=notes[q['number']],needsChange=q['number'] in fix,deduction='문단·어절·밑줄 원형 또는 설명의 전제 범위 보완' if q['number'] in fix else '발견 없음') for i,q in before.items()]
assert not (b/'ratings-before.json').exists();r.write(b/'ratings-before.json',dict(method='Same-author original-only solve then source/key/models and host before-edit review.',ratings=ratings));r.write(b/'ratings-frozen.json',dict(frozenAt=r.now(),ratingsSha256=r.sha(b/'ratings-before.json'),total=44,count=10,beforeChanges=True))
changes=[]
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  if q['id'] not in before or q['number'] not in fix:continue
  old=before[q['id']];assert q==old;snap=r.OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();r.write(snap,old)
  if q['number']==5:q['body']=q['body'].replace('심지어\n\n일본군은','심지어 일본군은')
  if q['number']==7:
   q['body']=q['body'].replace('‘방어 기제’','‘방어기제’');q['underlines'][-1]='회복 불가능할 정도로 망가지는 것을 막아 준다'
  if q['number']==8:
   q['title']='필수 자원과 내면적 역량의 구별'
   for field in ['steps','optionReasons']:q[field]=[re.sub(r'(?<=[가-힣])(?=\([가나]\))',' ',s) for s in q[field]]
  if q['number']==10:q['body']=q['body'].replace('38 %','38%')
  if q['number']==11:q['body']=q['body'].replace('화학 물질','화학물질')
  if q['number']==12:
   q['optionReasons'][0]='선수 사이 운의 동등성은 한 선수의 실력과 운을 나누어 설명하는 문맥에서 남은 실력 항을 보완하지 못한다.'
   q['steps'][4]='적용 한계: ⑤는 실력 저하 없이도 현상을 설명하는 문맥에 가장 적절하다. 다만 0≤실력 확률≤1이므로 제시된 곱은 운의 확률 이하이며, 낮은 성공 확률이라는 상한 자체에 ⑤가 필수인 것은 아니다. 곱셈 관계는 지문이 부여한 모형이며 현실의 실력·행운이 항상 독립이라는 법칙이나 성공이 반드시 감소한다는 단정으로 확대하지 않는다.'
  fields=[k for k in q if q[k]!=old[k]];assert fields;q['revision']+=1;touched=True
  changes.append(dict(id=q['id'],file=p.relative_to(r.ROOT).as_posix(),oldRevision=old['revision'],newRevision=q['revision'],changedFields=fields,beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason=notes[q['number']],status='repaired_pending_reverification'))
 if touched:r.write(p,data)
assert len(changes)==6;r.write(r.OUT/'changes-batch34.json',changes)
bank=r.bank()
for i,q in before.items():
 after=bank[i];assert after['answer']==q['answer'] and after['choices']==q['choices'];assert re.sub(r'\s','',after['body'])==re.sub(r'\s','',q['body'])
assert bank['kr-mpm-2026-03-07-psat-l-07']['underlines'][-1].endswith('막아 준다')
r.write(b/'repair-semantic-checks.json',dict(status='PASS',sixRepairs=changes,sourceAllWordsAndChoicesPreserved=True,underlineSourceStroke=dict(sourcePage=4,x0=63.555,x1=286.955,y=744.291,lastCharEnd=286.840,periodEnd=289.905,conclusion='Stroke includes 막아 준다 and excludes period.'),probabilityModel='source-key-model-checks.json'))
print('Frozen44/50;6 revisions;source words/choices/answers preserved')
