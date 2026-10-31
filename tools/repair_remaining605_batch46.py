import re,pdfplumber
import review_remaining605 as r
b=r.folder(46);old={x['question']['id']:x['question'] for x in r.read(b/'revealed-current.json')};related={q['id']:q for q in r.read(b/'related295-before.json')}
for n in ['host-before.log','related295-host-before.log']:assert 'All tests passed!' in (b/n).read_text(encoding='utf-8-sig')
for n in ['source-key-model-checks.json','related295-source-key-model-checks.json']:assert r.read(b/n)['status']=='PASS'
notes={4:'관념과 제도·사례와 도입목적 및 현행제도 적용한계 구분 정확. 발견없음.',5:'대안 지표와 국가별 역상관 부재·시기별 감소 구분 정확. 발견없음.',6:'적정 수준과 무한 증가·필요조건/역할 연결 및 이식의 가능성 한정 정확. 발견없음.',7:'반박 대상과 결론·환경 관련성과 필연/정책처방 구분 정확. 발견없음.',11:'의도/변형의 필요조건, 예술과 창조의 범위 및 역방향 반례 정확. 발견없음.',13:'정답·전체 대진·모든 보기 정확. 병의 승리 가정 뒤 전적을 여러 번 추적하는 기존 경로를 우승자 후보 제거부터 시작하는 짧은 경로로 개선.',14:'갑 잔류와 을무 교환·독립 조건부 보기 정확.6개 완전 배치 전수 확인. 발견없음.',15:'비동일성과 부분중첩·빈도 정보 부재 정확. 원문 밑줄의 끝은 없다이며 마침표를 포함한 두 범위를 수정.',17:'조건부 허용과 전면 금지·비약화와 인과증명 구별 정확. 발견없음.',18:'항성 밝기·행성 크기·추가 행성의 존재 가설 약화 구분 정확. 발견없음.'}
fix={13,15};ratings=[dict(id=i,scoreBeforeFix=4 if q['number'] in fix else 5,assessment=notes[q['number']],needsChange=q['number'] in fix) for i,q in old.items()]
assert not (b/'ratings-before.json').exists();r.write(b/'ratings-before.json',dict(method='Same-author own solves frozen before reveal; all10 have historical key exposure; original native/key, exhaustive models and before-host images reviewed.',ratings=ratings));r.write(b/'ratings-frozen.json',dict(frozenAt=r.now(),ratingsSha256=r.sha(b/'ratings-before.json'),total=48,count=10,beforeChanges=True))
hist={x['id']:x for x in r.read(r.PREP/'previously-scored295.json')['questions']}
r.write(b/'related295-assessment-before.json',[dict(id=i,historicalScorePreserved=hist[i]['scoreBeforeFix'],currentBeforeScore=5,assessment='배치 전수/반례/상한과 조건방향 정확, 발견없음.' if q['number']==33 else '6개 밑줄 범위와 명제 대응, 필요조건 대우/추가전제 추론 정확, 발견없음.',notReplacementOfHistoricalScore=True,changed=False) for i,q in related.items()])
src=next(x for x in r.read(b/'blind-source.json') if x['id'].endswith('l-15'));strokes=[]
with pdfplumber.open(r.ROOT/src['source']) as pdf:
 p=pdf.pages[src['page']-1]
 for l in p.lines:
  if l['x1']<375 and l['x1']-l['x0']>15 and abs(l['top']-l['bottom'])<.1 and 90<l['top']<460:
   chars=[c for c in p.chars if l['top']-15<c['top']<l['top']-5 and l['x0']-.1<(c['x0']+c['x1'])/2<l['x1']+.1]
   strokes.append(dict(line={k:l[k] for k in ['x0','x1','top']},text=''.join(c['text'] for c in chars)))
q=next(q for q in old.values() if q['number']==15)
for parts,phrase in [(strokes[:2],q['underlines'][0]),(strokes[2:],q['underlines'][1])]:assert re.sub(r'\s','',''.join(x['text'] for x in parts))==re.sub(r'\s','',phrase.removesuffix('.'))
r.write(b/'underline-source-strokes.json',dict(source=src['source'],page=src['page'],strokes=strokes,terminalPeriodsOutsideUnderline=True,initialQuoteIncluded=True))
changes=[]
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  if q['id'] not in old or q['number'] not in fix:continue
  prev=old[q['id']];assert q==prev;snap=r.OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();r.write(snap,prev)
  if q['number']==15:q['underlines']=[s.removesuffix('.') for s in q['underlines']]
  else:
   q['steps'][0]='착안점: 두 번 이겨야 우승한다. 갑은 1승 1패, 을은 정에게 패했고, 병은 갑·을을 이길 수 없어 두 상대에게 승리할 수 없다. 따라서 우승자는 정이며 연구부다.'
   q['steps'][1]='실전 풀이: 병은 갑·을을 이긴 적이 없고 우승한 정에게도 이길 수 없으므로 2패, 즉 영업부 4위다. 연구부와 대결하지 않은 인사부는 결승 상대인 2위도 영업부 4위도 아니므로 3위다. 남은 자재부가 2위다.'
   q['steps'][2]='답 확정 기준: 정에게 진 을은 정과 대결하지 않은 인사부 3위일 수 없다. 을은 자재부 2위, 갑은 인사부 3위이므로 을·정이 결승에서 만난 ②가 맞다. 아래의 네 경기로 모든 조건을 검산하면 확정한다.'
  fields=sorted(k for k in q if q[k]!=prev.get(k));assert q['body']==prev['body'] and q['answer']==prev['answer'] and q['choices']==prev['choices'] and q['optionReasons']==prev['optionReasons'];q['revision']+=1;touched=True
  changes.append(dict(id=q['id'],file=p.relative_to(r.ROOT).as_posix(),oldRevision=prev['revision'],newRevision=q['revision'],changedFields=fields,beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason=notes[q['number']],status='repaired_pending_reverification'))
 if touched:r.write(p,data)
assert len(changes)==2;r.write(r.OUT/'changes-batch46.json',changes)
r.write(b/'repair-semantic-checks.json',dict(status='PASS',count=2,tournamentProof='source-key-model-checks.json: unique full bracket supports reordered reasoning; not a new answer.',underlines='underline-source-strokes.json: both terminal periods excluded, quote retained.',allBodiesAnswersChoicesOptionReasonsUnchanged=True))
r.write(b/'after-sample.json',dict(sample=[dict(id=i) for i in list(old)+list(related)]))
print('Frozen48/50;2target repairs;2related unchanged')
