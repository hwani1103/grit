import review_remaining605 as r
b=r.folder(46);dst=b/'related295-originals';dst.mkdir(exist_ok=True)
ids=['kr-mpm-2024-03-02-psat-l-33','kr-mpm-2024-03-02-psat-l-16']
prior={x['id'] for x in r.read(r.PREP/'previously-scored295.json')['questions']};assert set(ids)<=prior
ledger={x['id']:x for x in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/current900-evidence-ledger.json')['questions']};bank=r.bank()
r.batch=lambda n:[dict(id=i,officialSource=ledger[i]['officialSource'],questionSha256=r.digest(bank[i])) for i in ids]
r.folder=lambda n:dst
r.blind(46)
r.write(b/'related295-source.json',r.read(dst/'blind-source.json'))
r.write(b/'related295-sample.json',dict(sample=[dict(id=i) for i in ids]))
