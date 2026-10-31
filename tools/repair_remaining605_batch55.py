import review_remaining605 as r
b=r.folder(55);old={x['question']['id']:x['question'] for x in r.read(b/'revealed-current.json')};related={q['id']:q for q in r.read(b/'related295-before.json')}
for n in ['host-before.log','related295-host-before.log']:assert 'All tests passed!' in (b/n).read_text(encoding='utf-8-sig')
for n in ['source-key-checks.json','related295-source-key-checks.json','exact-model-checks.json','underline-source-strokes.json']:assert r.read(b/n)['status']=='PASS'
notes=['병렬정치심리요인/대표사례와최초발생구별/의식무의식모두정확.','한원인확인과다른원인배제구별/전칭반례/본문한정정확.','원사례반례/4M/N/경향과매회오차단조성구별정확.','물과전자의공통방향/다른연속성및3빈칸선택지유일성정확.','같은공간/보이는원천/배경음악4칸대응정확;원문선지머리보존.','책임유형경계/최적수정의제시문내한계정확. 원문밑줄에포함되지않은㉠~㉤기호제외.','물리적센서조건대우와사용목적별표상구분/다른규격E반례정확.','동의명칭과목적조건있는시간사슬/온도역추론배제정확.','24순열중기존2/추가후1배치와기존확정/최종확정구별정확.','공통부정/미언급과부정구별/직접속도설명과비교우열한계정확.']
fix='kr-mpm-2023-03-04-psat-l-10';ratings=[dict(id=i,scoreBeforeFix=4 if i==fix else 5,assessment=n,needsChange=i==fix) for i,n in zip(old,notes)]
assert not (b/'ratings-before.json').exists();r.write(b/'ratings-before.json',dict(method='Original current-pass own10 frozen before current reveal. All10 had historical key exposure, disclosed in solve receipt; not blind or independent.',ratings=ratings));r.write(b/'ratings-frozen.json',dict(frozenAt=r.now(),ratingsSha256=r.sha(b/'ratings-before.json'),total=49,count=10,beforeChanges=True))
hist={x['id']:x for x in r.read(r.PREP/'previously-scored295.json')['questions']}
r.write(b/'related295-assessment-before.json',[dict(id=i,historicalScorePreserved=hist[i]['scoreBeforeFix'],currentBeforeScore=4 if q['number']==22 else 5,assessment='강약화의대상A/방향정확. 원문밑줄선끝밖마침표만제외.' if q['number']==22 else '도와도의회/의결기관유사성/판단주체/사전시점및벡터법명괄호6쌍원문일치. 현재수정불필요.',notReplacementOfHistoricalScore=True,changed=q['number']==22) for i,q in related.items()])
proof={x['id']:x['sourceRanges'] for x in r.read(b/'underline-source-strokes.json')['checks']};changes=[]
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  i=q['id']
  if i not in proof:continue
  prev=(related if i in related else old)[i];assert q==prev;snap=r.OUT/f"before-changes/{i}-r{q['revision']}.json";assert not snap.exists();r.write(snap,prev)
  q['underlines']=proof[i]
  assert all(q[k]==prev[k] for k in prev if k!='underlines');q['revision']+=1;touched=True
  changes.append(dict(id=i,file=p.relative_to(r.ROOT).as_posix(),oldRevision=prev['revision'],newRevision=q['revision'],changedFields=['underlines'],beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason='PDF원문선끝일치:기호또는마침표밑줄에서제외;본문과풀이전체보존.',status='repaired_pending_reverification'))
 if touched:r.write(p,data)
assert len(changes)==2;r.write(r.OUT/'changes-batch55.json',changes)
r.write(b/'repair-semantic-checks.json',dict(status='PASS',targetChanged=1,relatedChanged=1,onlyUnderlineMetadataChanged=True,allTextAnswersChoicesFiguresUnchanged=True,sourceProof='underline-source-strokes.json',historicalScoresPreserved=True,shared21='Same passage in2023July-l21 remains on pending underline-period queue for separate associated review; not silently marked verified.'))
r.write(b/'after-sample.json',dict(sample=[dict(id=i) for i in list(old)+list(related)]))
print('49/50 frozen;1target+1related underline metadata repair')
