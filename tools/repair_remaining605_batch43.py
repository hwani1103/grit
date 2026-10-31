import re
import pdfplumber
import review_remaining605 as r
b=r.folder(43);old={x['question']['id']:x['question'] for x in r.read(b/'revealed-current.json')}
assert 'All tests passed!' in (b/'host-before.log').read_text(encoding='utf-8-sig') and r.read(b/'source-key-model-checks.json')['status']=='PASS'
notes={27:'이해가능성vs미적우열,대중적→젊음필요조건,두빈칸유일성정확.빈칸뒤마침표분리공백제거.',28:'총누적비용/추가비용과적자감소·흑자전환구별정확.빈칸뒤조사이/과연결.',29:'시간·면적당최대수분과지구력/속도/효율및내용의한계정확.발견없음.',30:'실물자원변경vs회계선택과ㄱㄷ③정확.원본밑줄은이익조정네글자만이며현재따옴표를포함하여범위수정.',35:'환경대응/경쟁완화의공통전제와강화약화방향정확.줄갈이유성생식/무성생식어절연결.',36:'G/D순서와포괄적또는·세종완전분류및단일SW반례정확.집합7개대조;발견없음.',37:'두실험15개O/X를원본과대조하고5후보경로별모델③만일치.강한생물학적일반화안함;발견없음.',40:'세조건중실행누락은정의밖,믿음인식적한정과도덕이유반례,결정론진위무관정확;발견없음.',1:'사은숙배/사조/하직숙배순서와기관및파면가능성한정정확;발견없음.',3:'비공개노력의주체·인권시대구별·승리자관리비·가족비판가능성정확;발견없음.'}
changed=[27,28,30,35]
ratings=[dict(id=i,scoreBeforeFix=4 if q['number'] in changed else 5,assessment=notes[q['number']],needsChange=q['number'] in changed) for i,q in old.items()]
if not (b/'ratings-before.json').exists():
 r.write(b/'ratings-before.json',dict(method='Same-author original solves,10 native/source/key checks,5 explicit mechanism models and7 CNT subsets, original and host-before images. Two2024 keys previously exposed; not blind.',ratings=ratings));r.write(b/'ratings-frozen.json',dict(frozenAt=r.now(),ratingsSha256=r.sha(b/'ratings-before.json'),total=46,count=10,beforeChanges=True))
else:
 assert r.read(b/'ratings-before.json')['ratings']==ratings and r.sha(b/'ratings-before.json')==r.read(b/'ratings-frozen.json')['ratingsSha256']
src=next(x for x in r.read(b/'blind-source.json') if x['id'].endswith('l-30'))
with pdfplumber.open(r.ROOT/src['source']) as pdf:
 p=pdf.pages[src['page']-1];line=next(l for l in p.lines if abs(l['top']-220.517)<.01 and abs(l['x0']-420.66)<.01)
 chars=[c for c in p.chars if 208<c['top']<210 and line['x0']<(c['x0']+c['x1'])/2<line['x1']];word=''.join(c['text'] for c in chars)
 assert word=='이익조정';assert abs(chars[0]['x0']-line['x0'])<.5 and abs(chars[-1]['x1']-line['x1'])<.5
 r.write(b/'underline-source-stroke.json',dict(source=src['source'],page=src['page'],text=word,line={k:line[k] for k in ['x0','x1','top']},quoteCharactersExcluded=True))
changes=[]
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  if q['id'] not in old or q['number'] not in changed:continue
  prev=old[q['id']];assert prev==q;snap=r.OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();r.write(snap,prev)
  q['body']=q['body'].replace('[빈칸] .','[빈칸].').replace('[빈칸] 이','[빈칸]이').replace('[빈칸] 과','[빈칸]과').replace('무성 생식','무성생식').replace('유성 생식','유성생식')
  if q['number']==30:q['underlines']=['㉠‘이익조정’'];q['underlineLabelAnchors']=True
  assert q!=prev and re.sub(r'\s','',q['body'])==re.sub(r'\s','',prev['body'])
  fields=sorted(k for k in q.keys()|prev.keys() if q.get(k)!=prev.get(k));q['revision']+=1;touched=True
  changes.append(dict(id=q['id'],file=p.relative_to(r.ROOT).as_posix(),oldRevision=prev['revision'],newRevision=q['revision'],changedFields=fields,beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason=notes[q['number']],status='repaired_pending_reverification'))
 if touched:r.write(p,data)
assert len(changes)==4;r.write(r.OUT/'changes-batch43.json',changes);r.write(b/'repair-semantic-checks.json',dict(status='PASS',count=4,bodyChangesWhitespaceOnly=True,underlineSource='underline-source-stroke.json',allAnswersOptionsStepsUnchanged=True))
print('4 repairs;46/50 frozen;source underline stroke matched exact4chars')
