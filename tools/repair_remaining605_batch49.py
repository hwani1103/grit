import re
import review_remaining605 as r
b=r.folder(49);old={x['question']['id']:x['question'] for x in r.read(b/'revealed-current.json')};related={q['id']:q for q in r.read(b/'related295-before.json')}
for n in ['host-before.log','related295-host-before.log']:assert 'All tests passed!' in (b/n).read_text(encoding='utf-8-sig')
for n in ['source-key-model-checks.json','related295-source-key-model-checks.json','related295-underline-source-strokes.json']:assert r.read(b/n)['status']=='PASS'
notes={19:'통제필요/인식결여및보호와위임분리정확.공통밑줄원문범위도일치,발견없음.',20:'유추의인간관리자/AI구성원대응과강화약화방향정확.발견없음.',21:'외손자2세대와성골한정/진골최초통념교정정확.줄갈이의물려주기로어절연결.',22:'매수자선택적입안/100일/소지초사처분과입지차이정확.발견없음.',23:'실질심사와최종승인구별/국가범위/법사위비판주체정확.체계·자구심사어절2곳연결.',24:'가중치모두양수합1반례와일반증명/0경계정확.발견없음.',25:'0포함5상태/지수3점4조합/확정행동공집합/척도간비교불가정확.발견없음.',27:'문맥상정답과5밑줄범위정확.①근거의흔히는아포토시스라는명명관행을수식하므로빈도근거로쓰지않고명시적일상성과형성필수근거로교체.',28:'활성화참인지참경험거짓반례와④대우/확인불가와부재구별정확.발견없음.',30:'인간대상범위와문헌조사의근거없음/면제확정구별정확.기관생명윤리위원회고유명어절연결.'}
fix={21,23,27,30};ratings=[dict(id=i,scoreBeforeFix=4 if q['number'] in fix else 5,assessment=notes[q['number']],needsChange=q['number'] in fix) for i,q in old.items()]
assert not (b/'ratings-before.json').exists();r.write(b/'ratings-before.json',dict(method='Original source solutions frozen before present reveal; all10 had historical key exposure. Direct source/key/model/host assessment, no answer or reasoning correction in own49.',ratings=ratings));r.write(b/'ratings-frozen.json',dict(frozenAt=r.now(),ratingsSha256=r.sha(b/'ratings-before.json'),total=46,count=10,beforeChanges=True))
hist={x['id']:x for x in r.read(r.PREP/'previously-scored295.json')['questions']}
r.write(b/'related295-assessment-before.json',[dict(id=i,historicalScorePreserved=hist[i]['scoreBeforeFix'],currentBeforeScore=4 if q['number']==8 else 5,assessment='직업개념대응과5수정대입의의미는정확.㉠고/㉡㉢마침표/㉣를이원문밑줄밖이라4범위수정.' if q['number']==8 else '가열중결빙과전환온도−11<T<−8및양전하촉진/중성대조정확.발견없음.',notReplacementOfHistoricalScore=True,changed=q['number']==8) for i,q in related.items()])
changes=[];checks=[]
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  isRelated=q['id'] in related
  if not((q['id'] in old and q['number'] in fix) or (isRelated and q['number']==8)):continue
  prev=(related if isRelated else old)[q['id']];assert q==prev;n=q['number'];snap=r.OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();r.write(snap,prev)
  if isRelated:
   proof=r.read(b/'related295-underline-source-strokes.json');q['underlines']=proof['sourceRanges'];assert q['body']==prev['body']
   # Keep particles and punctuation outside substitute spans, exactly as source.
   for ix,tail in [(0,'고'),(1,'.'),(2,'.'),(3,'를')]:assert q['body'].count(q['underlines'][ix]+tail)==1
   assert q['underlines'][4]==prev['underlines'][4]
  elif n==21:
   assert q['body'].count('물려 주기로')==1;q['body']=q['body'].replace('물려 주기로','물려주기로')
  elif n==23:
   assert q['body'].count('체계· 자구심사')==1 and q['body'].count('체계·자구 심사')==1
   q['body']=q['body'].replace('체계· 자구심사','체계·자구심사').replace('체계·자구 심사','체계·자구심사')
  elif n==30:
   assert q['body'].count('기관생명윤리 위원회')==1;q['body']=q['body'].replace('기관생명윤리 위원회','기관생명윤리위원회')
  elif n==27:
   q['optionReasons'][0]='‘드문 현상’으로 고치면 세포자살을 탄생·분열만큼 일상적인 현상이라고 한 설명과 어긋난다. 뒤의 유기체 형성에 필수라는 설명과 수송망·시각 형성 사례도 일상적 기능을 뒷받침한다. 첫 문장의 ‘흔히’는 아포토시스라는 명칭에 붙은 말이므로 그것만으로 발생 빈도를 판단하지 않는다.'
  assert re.sub(r'\s','',q['body'])==re.sub(r'\s','',prev['body']) and q['answer']==prev['answer'] and q['choices']==prev['choices'] and q['steps']==prev['steps']
  if n!=27:assert q['optionReasons']==prev['optionReasons']
  fields=sorted(k for k in q if q[k]!=prev.get(k));q['revision']+=1;touched=True
  changes.append(dict(id=q['id'],file=p.relative_to(r.ROOT).as_posix(),oldRevision=prev['revision'],newRevision=q['revision'],changedFields=fields,beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason='원문선끝기준4밑줄범위수정;밖의조사고/를와마침표유지.' if isRelated else notes[n],status='repaired_pending_reverification'))
  checks.append(dict(id=q['id'],changedFields=fields,bodyCharactersUnchanged=True,answersChoicesStepsUnchanged=True))
 if touched:r.write(p,data)
assert len(changes)==5;r.write(r.OUT/'changes-batch49.json',changes)
r.write(b/'repair-semantic-checks.json',dict(status='PASS',count=5,checks=checks,originalAllCharactersAndAssetsPreserved=True,underlineSourceEvidence='related295-underline-source-strokes.json',explanation27='Explicit everyday/essential statement supports rejection; naming-frequency modifier no longer treated as event-frequency evidence.'))
r.write(b/'after-sample.json',dict(sample=[dict(id=i) for i in list(old)+list(related)]))
print('Frozen46/50;4target+1related repaired;4underline ranges corrected')
