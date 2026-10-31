import re
import review_remaining605 as r
out=r.OUT/'final';bank=r.bank();sets={s['id']:s for s in r.read(r.ROOT/'assets/psat/sets.json')['sets']}
assert r.read(out/'current900-evidence-ledger.json')['status']=='PASS'
dest=out/'test-updates';dest.mkdir(exist_ok=True);rows=[]
for n in range(2,31):
 p=r.ROOT/f'test/psat_data{n:02d}_test.dart';s=p.read_text(encoding='utf-8');before=s;qs=[bank[i] for i in sets[f'psat-data-{n:03d}']['questionIds']];counts=[len(q.get('figures',[])) for q in qs];unique=len({f['asset'] for q in qs for f in q.get('figures',[])})
 # Static expected counts are updated only against the source-verified final bank.
 s=re.sub(r"(expect\(\s*(?:added|qs)\.expand\(\(q\)\s*=>\s*q\.figures\)\.length,\s*)\d+",lambda m:m[1]+str(sum(counts)),s)
 s=re.sub(r"(expect\(\s*(?:added|qs)\.expand\(\(q\)\s*=>\s*q\.figures\)\.map\(\(f\)\s*=>\s*f\['asset'\]\)\.toSet\(\)\.length,\s*)\d+",lambda m:m[1]+str(unique),s)
 s=re.sub(r"(expect\(\s*(?:added|qs)\.map\(\(q\)\s*=>\s*q\.figures\.length\)(?:\.toList\(\))?,\s*)\[[\d,\s]+\]",lambda m:m[1]+str(counts),s)
 s=re.sub(r"(expect\((?:added|qs)\[(\d+)\]\.figures\.length,\s*)\d+",lambda m:m[1]+str(counts[int(m[2])]),s)
 s=re.sub(r'all \d+ (?:new )?figures fit',f'all {sum(counts)} current figures fit',s)
 if s!=before:
  (dest/p.name).write_text(s,encoding='utf-8');rows.append(dict(file=p.relative_to(r.ROOT).as_posix(),beforeSha256=r.sha(p),afterDraft=dest.relative_to(r.ROOT).as_posix()+'/'+p.name,verifiedFigureCounts=counts,sourceProof='final/current900-evidence-ledger.json',reason='Prose-only figures were source-verified and moved to native text. Keep exact remaining graphic counts, official answers, pixel dimensions, snapshot roundtrip, graph labels and widget assertions.'))
r.write(out/'test-update-plan.json',rows);print('Prepared',len(rows),'test count updates; originals not yet edited')
