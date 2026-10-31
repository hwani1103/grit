"""Verify native replacements against the original PDF and preserved objects."""
from pathlib import Path
from fractions import Fraction as F
import json,re,hashlib
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/psat_remaining605_20261030';B=OUT/'batch08'
read=lambda f:json.loads(f.read_text(encoding='utf-8-sig'))
def write(f,v):f.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
bank={q['id']:q for f in (ROOT/'assets/psat').glob('*.json') if isinstance(v:=read(f),list) for q in v}
before={r['question']['id']:r['question'] for r in read(B/'revealed-current.json')}
sources={r['id']:r['sourceText'] for r in read(B/'blind-source.json')}
norm=lambda s:re.sub(r'[\s①②③④⑤·ㆍ:]','',s)
symbolId='kr-mpm-2023-07-22-psat-s-20';scoreId='kr-mpm-2024-07-27-psat-s-24'
q=bank[symbolId];table=q['tables'][0]
assert q['figures']==[] and table['afterParagraph']==1
assert table['columns']==['과목']+[str(i)+'번' for i in range(1,11)]
symbols={
 'A':['○','○','×','○','×','○','×','○','○','○'],
 'B':['V','×','V','V','V','×','V','×','V','V'],
 'C':['/','○','○','○','○','/','/','○','/','○'],
 'D':['○','○','V','V','V','○','○','V','V','V'],
 'E':['/','/','/','/','×','×','/','/','/','/']}
assert table['rows']==[[k]+v for k,v in symbols.items()]
native=sources[symbolId];start=native.index('○○국제교육과정');body= native[start:native.index('문항\n과목')]
assert norm(body)==norm('\n\n'.join(q['body'].split('\n\n')[:2]))
for k,v in symbols.items():assert norm(k+''.join(v)) in norm(native)
assert '※ 모든 과목은 각 10문항이며, 각 문항별 배점은 10점이다.' in q['body']
assert 'ㄱ. A: 70점\nㄴ. B: 30점\nㄷ. C: 60점\nㄹ. D: 40점\nㅁ. E: 80점' in q['body']

q=bank[scoreId];table=q['tables'][0]
assert q['figures']==[] and table['afterParagraph']==4
assert table['columns']==['구분','1번','2번','3번','4번','5번','6번']
known=[['甲','○','×','○','○'],['乙','○','×','○','×'],['丙','○','○','×','×'],['丁','×','○','○','×']]
assert table['rows']==[row+['미상','미상'] for row in known]+[['정답률(%)','75','50','75','25','50','50']]
native=sources[scoreId]
for row in known:assert norm(''.join(row)) in norm(native)
assert '정답률(%)755075255050' in norm(native)
assert '5번과 6번 문제의 결과는 찢어져 알 수가 없다.' in q['body']
assert '추가점수 = (해당 문제를 틀린 사람의 수) / (해당 문제를 맞힌 사람의 수)' in q['body']
assert '32/3점이다.' in q['body'] and F(32,3)==F(20,3)+4
nativeHeader=re.split(r'\(○:\s*정답',native,1)[0]
nativeHeader=re.sub(r'^.*?24[.]\s*','',nativeHeader,flags=re.S).replace(q['prompt'],'',1)
sourceFormula='해당 문제를 틀린 사람의 수\n추가점수＝\n해당 문제를 맞힌 사람의 수'
assert sourceFormula in nativeHeader
nativeHeader=nativeHeader.replace(sourceFormula,'추가점수 = (해당 문제를 틀린 사람의 수) / (해당 문제를 맞힌 사람의 수)')
appHeader=q['body'].split('\n(○: 정답',1)[0]
assert norm(nativeHeader)==norm(appHeader)

oldAssetHashes={}
for id in [symbolId,scoreId]:
 old=before[id];now=bank[id]
 for k in ['id','answer','choices','original','number','subject','book','examId','examDate','source','sourceUrl','answerUrl','title','tag','pitfall','transfer']:
  assert old[k]==now[k],(id,k)
 for f in old['figures']:
  file=ROOT/f['asset'];assert file.is_file();oldAssetHashes[f['asset']]=hashlib.sha256(file.read_bytes()).hexdigest()
assert read(OUT/'preservation-at-start.json')['files'].items() >= oldAssetHashes.items()
write(B/'native-after-source-checks.json',dict(status='PASS',nativeBodiesFromOriginal=True,symbolTable50CellsExact=True,grade16KnownAnd8UnknownCellsExact=True,all6CorrectRatesExact=True,unknownNotMappedToFalseOrZero=True,scoreFractionExact=True,tableInsertionParagraphs=[1,4],fiveChoicesKeyIdsAndOriginalsUnchanged=True,oldFigureAssetHashes=oldAssetHashes,
 scope='Existing reader components only; no lib/UI code change. Original table geometry and torn source still available in untouched original page and prior snapshots. Native tables keep all cell labels/values with adaptive cards.'))
prior={x['id'] for x in read(OUT/'preparation/previously-scored295.json')['questions']}
candidates=[dict(id=q['id'],cohort='prior295' if q['id'] in prior else 'fixed605',revision=q['revision'],figureCount=len(q.get('figures',[])),status='candidate_source_and_basic_screen_density_review_pending') for q in bank.values() if q['subject']=='상황판단' and not q['body'] and q.get('figures')]
path=OUT/'cross-candidates-situation-raster-body.json'
if path.exists():
 existing=read(path);known={x['id']:x for x in existing}
 for x in candidates:
  if x['id'] in known and x['revision']==known[x['id']]['revision']:x.update(known[x['id']])
 candidates += [x for x in existing if x['id'] not in {v['id'] for v in candidates}]
write(path,candidates)
cross=read(OUT/'cross-validation.json')
if not any(x['id']=='R605-008' for x in cross['findings']):
 cross['findings'].append(dict(id='R605-008',cause='dense-rasterized-situation-body',detectedIn=[symbolId,scoreId],targetRepairs=[symbolId,scoreId],searchEvidence='cross-candidates-situation-raster-body.json',status='open_prior295_and_future605_density_review',scope='Candidate only: empty native body+figures does not itself prove unreadability. Review actual source/basic viewport before any repair. All source files/assets retained.'))
write(OUT/'cross-validation.json',cross)
print('PASSnative source checks and4oldfigure hashes. Density candidates:',len(candidates),'prior295:',sum(x['cohort']=='prior295' for x in candidates))
