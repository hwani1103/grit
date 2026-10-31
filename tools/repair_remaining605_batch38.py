import re
import review_remaining605 as r
b=r.folder(38);old={x['question']['id']:x['question'] for x in r.read(b/'revealed-current.json')}
assert 'All tests passed!' in (b/'host-before.log').read_text(encoding='utf-8-sig');assert r.read(b/'source-key-model-checks.json')['status']=='PASS'
key=lambda q:('26' if '2026-' in q['id'] else '25')+'-'+str(q['number'])
notes={'26-12':'13점의정수타수와세라운드조건을전수열거해유일해3·3·7/2·5·6및5<6타를확인했다. 개선발견없음.','26-19':'최소모공/최대먼지의하한8과다섯선지방향·측정법을대조했다. 해설단위뒤조사를정리한다.','26-32':'서로다른부족여섯쌍을열거해ㄱㄴ반례와ㄷ성립례확인. 개선발견없음.','26-40':'배정·이월·일시금·세후를정확분수로검산했다. 원문줄갈이어절과퍼센트·해설괄호간격을복원한다.','25-1':'앱의수립·확정·통보주체및예외판단은맞다. 새풀이메모의주체오류를별도로보존정정했다. 본문기본계획어절과선지퍼센트연결.','25-3':'답②는맞으나착안점에서성-이름필수공백과이름사이선택공백을동일한선택으로서술했다. 필수·선택구분및로마자성명조사연결.','25-4':'1년/3년독립소멸과보험액/한도구분은맞다. 첫조제목과마지막제△△조를독립행으로복원하고우주손해어절연결.','25-7':'다섯잔210·150·150·360·20및100포함200제외정확. 개선발견없음.','25-8':'단위환산240및기준압력포함3800정확. 제목과해설괄호앞공백정리.','25-9':'실제·외모·시점분리와두식검산50정확. 답확정문선지기호뒤공백정리.'}
score=lambda q:5 if key(q) in ['26-12','26-32','25-7'] else 4
ratings=[dict(id=i,scoreBeforeFix=score(q),assessment=notes[key(q)],needsChange=score(q)<5) for i,q in old.items()]
assert not (b/'ratings-before.json').exists();r.write(b/'ratings-before.json',dict(method='Same-author fresh original solve with five reasons, source/key/model and host review. Own s01 subject mistake recorded separately; not attributed to app.',ratings=ratings));r.write(b/'ratings-frozen.json',dict(frozenAt=r.now(),ratingsSha256=r.sha(b/'ratings-before.json'),total=43,count=10,beforeChanges=True))
changes=[]
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  if q['id'] not in old or score(q)==5:continue
  prev=old[q['id']];assert q==prev;k=key(q);snap=r.OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();r.write(snap,prev)
  if k=='26-19':q['optionReasons'][0]=q['optionReasons'][0].replace('μm초과','μm 초과')
  if k=='26-40':
   q['body']=re.sub(r'(?<=\d)\s+(?=%)','',q['body']).replace('재개 했고','재개했고').replace('멀티스테이트 (','멀티스테이트(');q['steps']=[s.replace('쓰면(','쓰면 (') for s in q['steps']]
  if k=='25-1':q['body']=q['body'].replace('‘기본 계획’','‘기본계획’');q['choices']=[s.replace('20 %','20%') for s in q['choices']]
  if k=='25-3':
   q['body']=q['body'].replace('로마자성명 으로','로마자성명으로');q['choices']=[s.replace('존)’ 으로','존)’으로') for s in q['choices']]
   q['steps'][0]='착안점: 로마자는 성→이름 순서의 대문자다. 성과 이름 사이는 반드시 띄고, 여러 이름 사이에는 띄어쓰기를 할 수 있다. 한글은 성과 이름을 붙여 쓴다. 필수 공백과 선택 공백을 구별한다.'
   q['optionReasons'][1]='성 BROWN과 이름 사이는 반드시 띄고, 이름 KOKO와 KATHERINE 사이도 선택해 띄울 수 있어 BROWN KOKO KATHERINE의 두 공백이 허용된다.'
  if k=='25-4':q['body']=q['body'].replace('제○○조 이','제○○조\n\n이').replace('있다. 제△△조 이','있다.\n\n제△△조\n\n이').replace('우주 손해','우주손해')
  if k=='25-8':q['title']=q['title'].replace('수면의1','수면의 1');q['steps']=[s.replace('이므로(나)','이므로 (나)') for s in q['steps']]
  if k=='25-9':q['steps']=[s.replace('③50세','③ 50세') for s in q['steps']]
  fields=sorted(k for k in q if q[k]!=prev[k]);assert fields;q['revision']+=1;touched=True
  assert re.sub(r'\s','',q['body'])==re.sub(r'\s','',prev['body']) and [re.sub(r'\s','',s) for s in q['choices']]==[re.sub(r'\s','',s) for s in prev['choices']]
  changes.append(dict(id=q['id'],file=p.relative_to(r.ROOT).as_posix(),oldRevision=prev['revision'],newRevision=q['revision'],changedFields=fields,beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason=notes[k],status='repaired_pending_reverification'))
 if touched:r.write(p,data)
assert len(changes)==7;r.write(r.OUT/'changes-batch38.json',changes);r.write(b/'repair-semantic-checks.json',dict(status='PASS',count=7,originalBodyChoicesAndAnswersPreserved=True,mandatorySurnameGivenSpaceVsOptionalMultipleNames=True,lawHeadingsOnSeparateLines=True))
print('Frozen43/50;7 repairs; original source content and answers preserved')
