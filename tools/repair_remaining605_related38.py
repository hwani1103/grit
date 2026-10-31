import re
from fractions import Fraction as F
import pdfplumber
import review_remaining605 as r
b=r.folder(38);old={q['id']:q for q in r.read(b/'related295-before.json')};src={x['id']:x for x in r.read(b/'related295-source.json')};own={x['id']:x for x in r.read(b/'related295-own-solves.json')}
assert 'All tests passed!' in (b/'related295-host-before.log').read_text(encoding='utf-8-sig')
ledger={x['id']:x for x in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/current900-evidence-ledger.json')['questions']}
norm=lambda s:re.sub(r'[\s①②③④⑤「」^]','',s).replace('[빈칸]','').replace('ㆍ','·').replace('\ue0a8','μ').replace('\ue09e','β').replace('\ue0fc','x').replace('∼','～')
checks=[]
for i,q in old.items():
 m=src[i];s=re.sub(r'책형\s*\d+쪽','',m['sourceText']);s=re.sub(r'^\s*\[\d+～\s*\d+\] 다음 글을 읽고 물음에 답하시오[.]\s*','',s);s=re.sub(r'(?m)^\s*(?:문\s*)?'+str(q['number'])+r'[.]\s*','',s,count=1)
 if q['subject']=='상황판단':
  prompt=re.search(r'윗글.*?\?',s,re.S).group();assert norm(prompt)==norm(q['prompt']);s=s.replace(prompt,'',1);expected=q['body']+''.join(q['choices'])
 else:
  a=s.index('특징 상호');z=s.index('A는 의회의',a);table=s[a:z]
  assert norm(table)==norm('특징 상호 외부 참여 합의 지속성 모형 의존성 가능성 효율성 A 높음 낮음 높음 높음 B 보통 보통 보통 보통 C 낮음 높음 낮음 낮음')
  assert q['tables'][0]['columns']==['모형','상호 의존성','외부 참여 가능성','합의 효율성','지속성'] and q['tables'][0]['rows']==[['A','높음','낮음','높음','높음'],['B','보통','보통','보통','보통'],['C','낮음','높음','낮음','낮음']] and q['tables'][0]['afterParagraph']==0
  s=s[:a]+s[z:];expected=q['prompt']+q['body']+''.join(q['choices'])
 assert norm(s)==norm(expected),(i,'source native mismatch')
 with pdfplumber.open(r.ROOT/ledger[i]['officialKey']) as pdf:pi,t=next((j+1,p.extract_text()) for j,p in enumerate(pdf.pages) if '영역 '+q['subject'] in (p.extract_text() or ''))
 assert q['examDate'][:4] in t and f"책형 {q['book']}" in t.replace('㉯','나').replace('㉮','가');answers={}
 for line in t.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):z=list(map(int,line.split()));answers.update(zip(z[::2],z[1::2]))
 assert answers[q['number']]==q['answer']==own[i]['answer'];checks.append(dict(id=i,source=m['source'],page=m['page'],directKey=ledger[i]['officialKey'],keyPage=pi,sourceAndAllFiveChoicesMatch=True,ownAnswerMatches=True))
assert F(20,1)/F(80,64)==16 and F(20,100)==F(16,16+64)
assert F(60,100)<1 and F(25,100)<F(1,2)
hist={q['id']:q for q in r.read(r.PREP/'previously-scored295.json')['questions']}
assess=[dict(id=i,historicalScorePreserved=hist[i]['scoreBeforeFix'],currentBeforeScore=4 if q['number']==39 else 5,historicalEvidence=hist[i]['evidence'],assessment={20:'같은공기부피의PM농도포함관계와밀도같음·지름세제곱·질량/개수비를모두정확히구분한다. 새풀이16:1및모든오답대조. 개선발견없음.',39:'판매배분과1등일시금비율및시대/지역범위의해설은맞다.공유지문의퍼센트와재개했고·멀티스테이트괄호어절을연결한다.',3:'표의C특성및본문매칭정확.합의효율최고A가목표달성최고라는추론은B반례로기각하고참여집단영향력미비교·C지속성범위설명도정확.개선발견없음.'}[q['number']],notReplacementOfHistoricalScore=True) for i,q in old.items()]
assert not (b/'related295-assessment-before.json').exists();r.write(b/'related295-assessment-before.json',assess)
changes=r.read(r.OUT/'changes-batch38.json')
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  if q['id'] not in old or q['number']!=39:continue
  prev=old[q['id']];assert q==prev;snap=r.OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();r.write(snap,prev)
  q['body']=re.sub(r'(?<=\d)\s+(?=%)','',q['body']).replace('재개 했고','재개했고').replace('멀티스테이트 (','멀티스테이트(')
  fields=sorted(k for k in q if q[k]!=prev[k]);assert fields;q['revision']+=1;touched=True
  assert norm(q['body'])==norm(prev['body']) and q['choices']==prev['choices'] and q['answer']==prev['answer']
  changes.append(dict(id=q['id'],file=p.relative_to(r.ROOT).as_posix(),oldRevision=prev['revision'],newRevision=q['revision'],changedFields=fields,beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason='Same common passage as target40; repair source line-wrap word boundaries.',cohort='prior295',status='repaired_pending_reverification'))
 if touched:r.write(p,data)
r.write(r.OUT/'changes-batch38.json',changes)
bank=r.bank();assert bank['kr-mpm-2026-03-07-psat-s-40']['body'].split('\n\n<상 황>')[0]==bank['kr-mpm-2026-03-07-psat-s-39']['body']
assert r.sha(b/'related295-own-solves.json')==r.read(b/'related295-solve-frozen.json')['sha256']
r.write(b/'related295-source-key-model-checks.json',dict(status='PASS',checks=checks,particleCount='A-only20,B80; unit masses1:64; count16:1; same volume cancels.',lottery='25%<50%; lump60%<100%; current passage only, no real-world tax inference.',network='High consensus efficiency=A, but B can achieve goals more effectively; no unjustified maximum or individual-group power comparison.',historicalScoresAndFrozenSolvesPreserved=True))
print('3 prior295 checked;1 repaired; source/key/models PASS')
