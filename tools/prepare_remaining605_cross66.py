import review_remaining605 as r
b=r.folder(66);b.mkdir(exist_ok=True);dst=b/'originals';dst.mkdir(exist_ok=True)
ids=['kr-mpm-2026-07-18-psat-d-'+n for n in ['05','13']]+['kr-mpm-2026-03-07-psat-d-'+n for n in ['03','06','09','12','22','25']]+['kr-mpm-2025-03-08-psat-d-'+n for n in ['09','11']]
ledger={x['id']:x for x in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/current900-evidence-ledger.json')['questions']};bank=r.bank()
assert not (b/'before.json').exists();r.write(b/'before.json',[bank[i] for i in ids]);r.write(b/'sample.json',dict(sample=[dict(id=i) for i in ids]))
r.batch=lambda n:[dict(id=i,officialSource=ledger[i]['officialSource'],questionSha256=r.digest(bank[i])) for i in ids];r.folder=lambda n:dst;r.blind(66)
r.write(b/'source.json',r.read(dst/'blind-source.json'))
