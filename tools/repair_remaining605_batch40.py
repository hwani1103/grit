import re
import review_remaining605 as r
b=r.folder(40);old={x['question']['id']:x['question'] for x in r.read(b/'revealed-current.json')}
assert 'All tests passed!' in (b/'host-before.log').read_text(encoding='utf-8-sig') and r.read(b/'source-key-model-checks.json')['status']=='PASS'
notes={11:'양수반례와잔기직접측정불가·최대흡기합을정확히설명. 원문줄갈이의흡식예비용량·호식예비용량을연결한다.',12:'5조건문진리표에서④만C참으로¬B강제. 대우/전건부정/동치연결과모든오답근거정확. 발견없음.',16:'유한최대전도도의양의최소저항,감도비율차,반응시간부분강화와선택도구분정확. 실제선지③④⑤중ㄴ제외시④유일. 발견없음.',18:'I>II초기조건,양처리차이증가,두가설동일예측및가능성범위정확. 발견없음.',19:'두빈칸의주축확정/규범조건과나머지5선지대응정확. 공통지문빈칸뒤조사를붙인다.',20:'주축미확정만으로뒤섞기불가일반화기각및차용어·발음·단일언어사회각근거정확. 공통지문빈칸뒤조사를붙인다.',22:'모임종류·참여기간·폐지시점·화가·부친기록의범위를개별대조했다. 발견없음.',23:'25+3합,문자도입후꾸러미,실색과토큰분류구별정확.8000년경부터조사연결.',24:'동력→교류→발전의한요인및면역·저지대·문자부재·시계열미제시정확. 발견없음.',26:'문제중심규범초월과전문성존속양립,학제내수용성/규범준수환원의오류정확. 발견없음.'}
changed=[11,19,20,23]
ratings=[dict(id=i,scoreBeforeFix=4 if q['number'] in changed else 5,assessment=notes[q['number']],needsChange=q['number'] in changed,deduction='원문줄갈이에서분리된어절' if q['number'] in changed else '발견없음') for i,q in old.items()]
assert not (b/'ratings-before.json').exists();r.write(b/'ratings-before.json',dict(method='Original-only own solve frozen before key/current reveal; source/native/keys/exact models and host before reviewed individually.',ratings=ratings));r.write(b/'ratings-frozen.json',dict(frozenAt=r.now(),ratingsSha256=r.sha(b/'ratings-before.json'),total=46,count=10,beforeChanges=True))
changes=[]
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  if q['id'] not in old or q['number'] not in changed:continue
  prev=old[q['id']];assert q==prev;snap=r.OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();r.write(snap,prev)
  q['body']=q['body'].replace('흡식 예비용량','흡식예비용량').replace('호식 예비용량','호식예비용량').replace('[빈칸] 로','[빈칸]로').replace('8000년경 부터','8000년경부터')
  assert q!=prev and re.sub(r'\s','',q['body'])==re.sub(r'\s','',prev['body']);q['revision']+=1;touched=True
  changes.append(dict(id=q['id'],file=p.relative_to(r.ROOT).as_posix(),oldRevision=prev['revision'],newRevision=q['revision'],changedFields=['body'],beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason=notes[q['number']],status='repaired_pending_reverification'))
 if touched:r.write(p,data)
assert len(changes)==4;r.write(r.OUT/'changes-batch40.json',changes)
bank=r.bank();assert bank['kr-mpm-2025-03-08-psat-l-19']['body']==bank['kr-mpm-2025-03-08-psat-l-20']['body']
r.write(b/'repair-semantic-checks.json',dict(status='PASS',count=4,onlyWhitespaceChanged=True,sharedPassagePreserved=True,allAnswersOptionsStepsUnchanged=True))
print('Frozen46/50;4 whitespace repairs; source words/answers preserved')
