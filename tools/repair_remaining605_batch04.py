"""Reviewed, explicit batch04 fixes; never scores or supplies new solves."""
from pathlib import Path
import copy,json
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/psat_remaining605_20261030'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert (OUT/'batch04/ratings-frozen.json').exists()
assert not (OUT/'changes-batch04.json').exists()
primary='kr-mpm-2024-07-27-psat-l-'
related=['kr-mpm-2021-07-10-psat-l-13','kr-mpm-2021-07-10-psat-l-21',
         'kr-mpm-2024-03-02-psat-l-32','kr-mpm-2023-03-04-psat-l-11']
ids={primary+x for x in ['17','18','19','20']}|set(related);changes=[]
for p in (ROOT/'assets/psat').glob('*.json'):
 qs=read(p)
 if not isinstance(qs,list):continue
 changed=False
 for q in qs:
  if q['id'] not in ids:continue
  old=copy.deepcopy(q);n=q['id']
  if n==primary+'17':
   q['steps'][2]='답 확정 기준: (가)는 ‘약화하고’, (나)는 ‘강화한다’이므로 ⑤로 확정한다. 실험 1의 총 방출 전자량이 아니라 단위 면적당 양을 비교했는지 확인한다.'
   q['optionReasons'][4]='밀도 증가에도 단위 면적당 전자량이 같았던 실험 1은 H1을 약화하고, 같은 기판에서 증가 후 감소한 실험 2는 H2를 강화한다.'
   reason='두 빈칸의 완성 문구와 가설 지시어를 문장으로 분명히 구분한다. 밀도와 단위 면적당 양이라는 기존 수학적 의미는 유지한다.'
  elif n==primary+'18':
   assert '상한 초과' in q['steps'][1]
   q['steps'][0]=q['steps'][0].replace('주변의○','주변의 ○')
   q['steps'][1]=q['steps'][1].replace('상한 초과이므로','II의 광포화점 이상이므로')
   reason='광포화점과 같은 세기도 측정 불가다. 정석의 ≤와 일치하도록 실전 경계 표현을 이상으로 수정한다. 원문 조건과 정답은 유지한다.'
  else:
   assert not q.get('underlineLabelAnchors')
   q['underlineLabelAnchors']=True
   if n==primary+'19':
    for t in ['ㄱ','ㄴ','ㄷ']:q['steps'][1]=q['steps'][1].replace(t+':',t+': ')
   reason='공식 원문의 원문자 지시표는 밑줄 밖이다. 반복 문구를 특정하는 저장 앵커는 유지하고 기존 underlineLabelAnchors 표시 옵션으로 원문자를 밑줄 범위에서 제외한다.'
  fields=[k for k in q.keys()|old.keys() if q.get(k)!=old.get(k)]
  assert fields
  snapshot=OUT/'before-changes'/f"{n}-r{old['revision']}.json";assert not snapshot.exists()
  write(snapshot,old);q['revision']+=1;changed=True
  changes.append(dict(id=n,cohort='prior295' if n in related else 'fixed605',file=p.relative_to(ROOT).as_posix(),
       oldRevision=old['revision'],newRevision=q['revision'],changedFields=sorted(fields),
       beforeSnapshot=snapshot.relative_to(ROOT).as_posix(),reason=reason,status='repaired_pending_reverification'))
 if changed:write(p,qs)
assert {x['id'] for x in changes}==ids
write(OUT/'changes-batch04.json',changes)
write(OUT/'batch04/related295-sample.json',dict(sample=[dict(id=x) for x in related]))
print('Applied8 explicitly reviewed revisions,4 target and4 related prior295; old snapshots retained.')
