import review_remaining605 as r
b=r.folder(60);dst=b/'related295-originals';dst.mkdir(exist_ok=True)
ids=['kr-mpm-2026-03-07-psat-d-19','kr-mpm-2025-03-08-psat-d-10','kr-mpm-2021-07-10-psat-d-14']
prior={x['id'] for x in r.read(r.PREP/'previously-scored295.json')['questions']};assert set(ids)<=prior
ledger={x['id']:x for x in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/current900-evidence-ledger.json')['questions']};bank=r.bank()
r.batch=lambda n:[dict(id=i,officialSource=ledger[i]['officialSource'],questionSha256=r.digest(bank[i])) for i in ids]
r.folder=lambda n:dst
r.blind(60)
r.write(b/'related295-source.json',r.read(dst/'blind-source.json'))
r.write(b/'related295-sample.json',dict(sample=[dict(id=i) for i in ids]))
