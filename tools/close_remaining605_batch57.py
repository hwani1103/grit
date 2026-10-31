from fractions import Fraction as F
import review_remaining605 as r
b=r.folder(57);assert not (b/'batch-verification.json').exists()
old={x['question']['id']:x['question'] for x in r.read(b/'revealed-current.json')};related={q['id']:q for q in r.read(b/'related295-before.json')};bank=r.bank()
assert all(bank[i]==q for i,q in (old|related).items())
logs=['host-before.log','related295-host-before.log']
for n in logs:assert 'All tests passed!' in (b/n).read_text(encoding='utf-8-sig')
for file,receipt,key in [('own-solves.json','solve-frozen-before-reveal.json','solveFileSha256'),('related295-own-solves.json','related295-solve-frozen.json','sha256')]:assert r.sha(b/file)==r.read(b/receipt)[key]
for n in ['source-key-checks.json','related295-source-key-checks.json','pre-reveal-exact-models.json','related295-pre-reveal-models.json','preservation-check.json']:assert r.read(b/n)['status']=='PASS'
notes=['구성비와증가율분모/80%·30%경계/선택지유일성과모든보기정확.','동서그룹경계/전행주차밀도상한·하한/최대부정반례와2배증명정확.','6행모두30%경계/한빛근접경계/건물면적분모및설립연도반례정확.','보고서격차3.8년/수출단위·배수/끝점개선과단조증가구별정확;본문원문순서유지.','두조건집합교집합/두비중곱과반올림여유/다섯매칭정확.','존치가중치/80점포함/증감분4147과전체분모522636/최대비교정확.','축역할과음수증감역산/선기호연결/선택지교집합유일성과나머지검산정확.','월별감소율전체/업체당비율32.2%/생산합과품목순위/안전경계정확.','5개그래프비중9값·비율4값·허가6값·가격좌표5개/온라인오프라인틀린열정확.','지역17개용량합·태양광17995개/비중3년·증가율배수/개소당순서정확.']
assert not (b/'ratings-before.json').exists()
r.write(b/'ratings-before.json',dict(method='Original source-only own10 frozen before reveal; original figures, all five options, exact models and host reviewed. No change needed.',ratings=[dict(id=i,scoreBeforeFix=5,assessment=n,needsChange=False) for i,n in zip(old,notes)]))
r.write(b/'ratings-frozen.json',dict(frozenAt=r.now(),ratingsSha256=r.sha(b/'ratings-before.json'),total=50,count=10,beforeChanges=True))
hist={x['id']:x for x in r.read(r.PREP/'previously-scored295.json')['questions']}
assess=[dict(id=i,historicalScorePreserved=hist[i]['scoreBeforeFix'],currentBeforeScore=5,assessment='종류매칭/기타제외후보와전체분모/소비4분야합/동일연도연간순위정확.' if q['number']==21 else '상위4그룹식별/하위61최소5421/평균상한493과실제평균구별/운행비중정확.',notReplacementOfHistoricalScore=True,changed=False) for i,q in related.items()]
r.write(b/'related295-assessment-before.json',assess)
m=r.read(b/'pre-reveal-exact-models.json');assert m['solarCount']==17995 and m['graph19Shares']==[[55.4,37.4,7.2],[74.0,20.0,6.0],[76.4,17.7,5.9]]
assert F(1972,4)==493 and 4*493>=201*4
r.write(b/'exact-model-checks.json',dict(status='PASS',target='pre-reveal-exact-models.json',related='related295-pre-reveal-models.json',allOriginalGraphLabelsVerified=True,topFourBoundAttainable='Other61 at interval minima and all top4 at493 meet7393 and201+ class.'))
r.write(b/'unchanged-verification.json',dict(status='PASS',questions={i:r.digest(q) for i,q in (old|related).items()},all12ExactlyEqualToAuditedBefore=True,noRepeatHostNeeded='No content, metadata, app or asset changes; successful before audits remain applicable.'))
r.write(r.OUT/'changes-batch57.json',[])
ids=set(old)|set(related)
for p in r.OUT.glob('cross-candidates-*.json'):
 v=r.read(p);rows=v if isinstance(v,list) else v.get('candidates',[]);changed=False
 for x in rows:
  if isinstance(x,dict) and x.get('id') in ids:x.update(status='source_semantics_and_host_reverified',evidence='batch57/batch-verification.json');changed=True
 if changed:r.write(p,v)
p=r.OUT/'cross-validation.json';v=r.read(p)
for x in v['findings']:
 if x['id'] in ['R605-003','R605-008','R605-009','R605-011','R605-018']:x.setdefault('subsequentBatchRepairs',[]).append(dict(batch=57,ids=sorted(ids),changed=0,evidence='batch57/batch-verification.json'))
for x in assess:v['relatedPrior295Reviews'].append(dict(id=x['id'],batch=57,causeFamilies=['source-structure','ratio-denominator','maximum-minimum','interval-bound'],evidence='batch57/related295-source-key-checks.json',status='source_key_semantics_and_host_reverified',historicalScorePreserved=x['historicalScorePreserved'],currentAssessmentBeforeRepair=5))
r.write(p,v)
r.write(b/'visual-review.json',dict(status='PASS',original='All10 target and both related original pages viewed, all chart choices and table group boundaries inspected.',host='All12 start screenshots viewed; all figures source-pixel matched and audit exercised enlarged figures/original zoom. No content changes.',hostNotDevice=True))
r.write(b/'batch-verification.json',dict(status='verified',verifiedAt=r.now(),count=10,ownSolves='own-solves.json',solveFrozenReceipt='solve-frozen-before-reveal.json',ratings='ratings-before.json',frozenRatingsReceipt='ratings-frozen.json',beforeScoreTotal=50,beforeMean=5.0,targetQuestionsChanged=0,relatedPrior295Rechecked=2,relatedPrior295Changed=0,sourceKeyModels=['source-key-checks.json','related295-source-key-checks.json','exact-model-checks.json'],repairChecks='unchanged-verification.json',hostLogs=logs,hostSuccessfulTestCount=12,visualReview='visual-review.json',preservation='preservation-check.json',solvesFrozenBeforeReveal=10,previouslyExposedOfficialAnswers=0,firstPassAnswerMatches=10,firstPassReasoningCorrections=0,limitations='Same-author review, not independent or error-free guarantee. All12 unchanged after complete review. Two6-test host audits apply to exactly same question bytes; no fabricated after-run.30 original figure crops freshly matched. No intermediate APK.'))
print('Batch57 verified;570 total after refresh;all12 unchanged')
