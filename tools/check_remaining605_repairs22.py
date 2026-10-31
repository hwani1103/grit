import re,hashlib
import pdfplumber
import review_remaining605 as r
b=r.folder(22);old={x['question']['id']:x['question'] for x in r.read(b/'revealed-current.json')};related='kr-mpm-2025-11-15-psat-l-22';old[related]=r.read(b/'related295-shared22-before.json');current=r.bank()
norm=lambda s:re.sub(r'[\s①②③④⑤·ㆍ/]+','',s)
checks=[]
for qid in [x['id'] for x in r.read(r.OUT/'changes-batch22.json')]:
 before,after=old[qid],current[qid]
 assert norm(before['body'])==norm(after['body'])
 for k in ['answer','choices','prompt','steps','pitfall','transfer','original','source','underlines']:assert before.get(k)==after.get(k),(qid,k)
 if before['number']==15:
  assert before['choices'][3]=='ㄴ, ㄷ'
  assert after['optionReasons'][3]=='ㄴ과 ㄷ은 맞지만, 예후를 설명하지 못해 인정받지 못한 ㄱ도 글의 기준을 지지하므로 함께 포함해야 한다.'
  assert before['optionReasons'][:3]+before['optionReasons'][4:]==after['optionReasons'][:3]+after['optionReasons'][4:]
 else:assert before['optionReasons']==after['optionReasons']
 if before['number'] in [14,21,22]:assert after['underlineLabelAnchors'] is True
 checks.append(dict(id=qid,sourceTextAndAnswerChoicesPreserved=True,onlyDocumentedFieldsChanged=True))
m=next(v for v in r.read(b/'blind-source.json') if v['id'].endswith('-21'))
q=old[related];common,tail=q['body'].split('<상황>',1)
assert norm(common)==norm(old['kr-mpm-2025-11-15-psat-l-21']['body'])
with pdfplumber.open(r.ROOT/m['source']) as pdf:
 page=pdf.pages[m['page']-1];t=page.crop((page.width/2,30,page.width,page.height)).extract_text();native=t.split('22.',1)[1]
assert norm(native)==norm(q['prompt']+'<상황>'+tail+''.join(q['choices']))
row=next(x for x in r.read(b/'revealed-current.json') if x['question']['id'].endswith('-21'))
with pdfplumber.open(r.ROOT/row['officialKey']) as pdf:
 pi,t=next((i+1,p.extract_text()) for i,p in enumerate(pdf.pages) if '영역 언어논리' in (p.extract_text() or ''))
answers={}
for line in t.splitlines():
 if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
  z=list(map(int,line.split()));answers.update(zip(z[::2],z[1::2]))
assert answers[22]==q['answer']==r.read(b/'related295-shared22-own.json')['answer']==4
assert hashlib.sha256((b/'own-solves.json').read_bytes()).hexdigest()==r.read(b/'solve-frozen-before-reveal.json')['solveFileSha256']
assert hashlib.sha256((b/'related295-shared22-own.json').read_bytes()).hexdigest()==r.read(b/'related295-shared22-solve-frozen.json')['sha256']
assert hashlib.sha256((b/'ratings-before.json').read_bytes()).hexdigest()==r.read(b/'ratings-frozen.json')['ratingsSha256']
r.write(b/'related295-own-option-reading-correction.json',dict(status='corrected_after_bank_reveal_and_direct_PDF_text',id=related,scope='Related prior295 review, not one of ten fixed605 targets.',initialAnswer=4,correctedAnswer=4,initialOption2Reason='ㄴ은참이지만ㄷ의조건부공통원인도참이라누락이다.',sourceOption2='ㄷ',correctedOption2Reason='ㄷ은 참이지만 차폐에 관한 ㄴ도 참이어서 누락이다.',publishedOptionReasonAlreadyCorrect=True,firstOwnRecordRetained=True,methodRefinement='Read actual printed label of every option from PDF text as well as source image before freezing a related review; do not infer combination order.'))
r.write(b/'related295-shared22-review.json',dict(status='source_key_semantics_checked_host_pending',id=related,source=m['source'],page=m['page'],key=row['officialKey'],keyPage=pi,answer=4,fullNativeTextAndChoicesMatch=True,reasoning='D after O excludesㄱ. With noO, inducingD yields probability0 and cannot raise S, soㄴ. O precedesD/raisesD/no prior shielding event; if also causesS then common cause, soㄷ. Option2 isㄷ, notㄴ; own reason corrected separately, bank reason already correct.',oldRevision=2,newRevision=3,oldHistoricalScorePreserved=True,correction='related295-own-option-reading-correction.json'))
progress=r.read(r.OUT/'progress.json');progress['postRevealReasoningCorrections'][related]='batch22/related295-own-option-reading-correction.json';r.write(r.OUT/'progress.json',progress)
r.write(b/'repair-semantic-checks.json',dict(status='PASS',checks=checks,relatedSourceAndOfficialKey=True,frozenRecordsIntact=True,relatedOwnOptionReasonCorrection='related295-own-option-reading-correction.json'))
print('PASS five explicit repairs, related original/key and frozen records. Related own option2 label correction disclosed; answer4 unchanged.')
