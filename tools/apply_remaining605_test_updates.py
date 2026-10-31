import shutil,re
import review_remaining605 as r
out=r.OUT/'final';plan=r.read(out/'test-update-plan.json');receipt=out/'test-changes.json'
assert not receipt.exists();assert len({x['file'] for x in plan})==len(plan)
rows=[]
for row in plan:
 p=r.ROOT/row['file'];assert r.sha(p)==row['beforeSha256'],str(p)
 d=r.ROOT/row['afterDraft'];assert d.exists()
for row in plan:
 p=r.ROOT/row['file'];snap=out/'test-before'/p.name;snap.parent.mkdir(exist_ok=True);assert not snap.exists();shutil.copy2(p,snap);shutil.copy2(r.ROOT/row['afterDraft'],p)
 rows.append({**row,'beforeSnapshot':snap.relative_to(r.ROOT).as_posix(),'afterSha256':r.sha(p)})
r.write(receipt,rows)
# Select only ordinary tests from the changed files first; widget cases have separate runs.
titles=[]
for row in plan:
 s=(r.ROOT/row['file']).read_text(encoding='utf-8')
 titles.extend(re.findall(r"(?<![A-Za-z])test\(\s*'([^']+)'",s))
r.write(out/'updated-unit-test-titles.json',titles)
print('Applied',len(rows),'source-grounded test updates; backed up originals;',len(titles),'ordinary tests selected')
