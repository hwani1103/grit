import review_remaining605 as r
b=r.folder(68);b.mkdir(exist_ok=True);dst=b/'originals';dst.mkdir(exist_ok=True)
ids=['kr-mpm-2024-07-27-psat-s-08','kr-mpm-2024-07-27-psat-s-10','kr-mpm-2024-07-27-psat-s-15','kr-mpm-2023-07-22-psat-s-10','kr-mpm-2025-07-19-psat-s-23','kr-mpm-2025-11-15-psat-s-02','kr-mpm-2025-11-15-psat-s-22','kr-mpm-2026-07-18-psat-s-12','kr-mpm-2025-03-08-psat-s-17','kr-mpm-2024-03-02-psat-s-15']
ledger={x['id']:x for x in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/current900-evidence-ledger.json')['questions']};bank=r.bank()
assert not (b/'before.json').exists();r.write(b/'before.json',[bank[i] for i in ids]);r.write(b/'sample.json',dict(sample=[dict(id=i) for i in ids]))
r.batch=lambda n:[dict(id=i,officialSource=ledger[i]['officialSource'],questionSha256=r.digest(bank[i])) for i in ids];r.folder=lambda n:dst;r.blind(68)
r.write(b/'source.json',r.read(dst/'blind-source.json'))
