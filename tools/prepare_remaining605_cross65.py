import review_remaining605 as r
b=r.folder(65);b.mkdir(exist_ok=True);dst=b/'originals';dst.mkdir(exist_ok=True)
ids=['kr-mpm-2021-07-10-psat-d-'+n for n in ['13','21','22']]+['kr-mpm-2025-11-15-psat-d-'+n for n in ['03','04','06','16','19','24']]+['kr-mpm-2026-07-18-psat-d-03']
ledger={x['id']:x for x in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/current900-evidence-ledger.json')['questions']};bank=r.bank()
assert not (b/'before.json').exists();r.write(b/'before.json',[bank[i] for i in ids]);r.write(b/'sample.json',dict(sample=[dict(id=i) for i in ids]))
r.batch=lambda n:[dict(id=i,officialSource=ledger[i]['officialSource'],questionSha256=r.digest(bank[i])) for i in ids];r.folder=lambda n:dst;r.blind(65)
r.write(b/'source.json',r.read(dst/'blind-source.json'))
