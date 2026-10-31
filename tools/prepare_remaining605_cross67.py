import review_remaining605 as r
b=r.folder(67);b.mkdir(exist_ok=True);dst=b/'originals';dst.mkdir(exist_ok=True)
ids=['kr-mpm-2025-03-08-psat-d-23','kr-mpm-2021-07-10-psat-d-11','kr-mpm-2026-03-07-psat-d-26','kr-mpm-2025-03-08-psat-d-38','kr-mpm-2024-03-02-psat-d-14','kr-mpm-2024-03-02-psat-d-32','kr-mpm-2025-11-15-psat-d-20']+['kr-mpm-2026-07-18-psat-d-'+n for n in ['04','10','14']]
ledger={x['id']:x for x in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/current900-evidence-ledger.json')['questions']};bank=r.bank()
assert not (b/'before.json').exists();r.write(b/'before.json',[bank[i] for i in ids]);r.write(b/'sample.json',dict(sample=[dict(id=i) for i in ids]))
r.batch=lambda n:[dict(id=i,officialSource=ledger[i]['officialSource'],questionSha256=r.digest(bank[i])) for i in ids];r.folder=lambda n:dst;r.blind(67)
r.write(b/'source.json',r.read(dst/'blind-source.json'))
