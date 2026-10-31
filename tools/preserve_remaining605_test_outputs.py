import re,shutil,sys
import review_remaining605 as r
f=r.OUT/'final';f.mkdir(exist_ok=True);backup=f/'previous-test-pngs';manifest=f/'previous-test-pngs.json'
if sys.argv[1]=='backup':
 assert not manifest.exists()
 dirs=set()
 for p in (r.ROOT/'test').glob('*.dart'):
  for value in re.findall(r"'(artifacts/[^']+?\.png)'",p.read_text(encoding='utf-8')):
   prefix=value.split('$')[0];directory=prefix.rsplit('/',1)[0]
   dirs.add(directory)
 files={p for d in dirs for p in (r.ROOT/d).rglob('*.png') if (r.ROOT/d).is_dir()}
 rows=[]
 for p in sorted(files):
  rel=p.relative_to(r.ROOT);dst=backup/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dst);rows.append(dict(path=rel.as_posix(),sha256=r.sha(p)))
 r.write(manifest,dict(files=rows,directories=sorted(dirs)))
 print('Backed up',len(rows),'existing screenshots before full regression')
elif sys.argv[1]=='restore':
 v=r.read(manifest);old={x['path']:x for x in v['files']};captured=[]
 for d in v['directories']:
  for p in (r.ROOT/d).rglob('*.png'):
   rel=p.relative_to(r.ROOT).as_posix()
   if rel not in old or r.sha(p)!=old[rel]['sha256']:
    dst=f/'regression-screens'/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dst);captured.append(rel)
 for rel,row in old.items():
  src=backup/rel;assert r.sha(src)==row['sha256'];shutil.copy2(src,r.ROOT/rel);assert r.sha(r.ROOT/rel)==row['sha256']
 r.write(f/'test-output-preservation.json',dict(status='PASS',oldScreenshotsRestoredByteForByte=len(old),newRunScreenshotsCaptured=sorted(set(captured)),newRunDirectory='regression-screens',method='Copy prior PNGs before tests, capture changed/new PNGs separately, restore prior PNG bytes; no deletions.'))
 print('Restored',len(old),'previous PNGs; captured',len(set(captured)),'new regression outputs')
