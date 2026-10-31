"""Inspection aid only: screenshots retain native390px resolution."""
import argparse
from PIL import Image,ImageDraw
import review_remaining605 as r
p=argparse.ArgumentParser();p.add_argument('batch',type=int);p.add_argument('phase');p.add_argument('--details',nargs='*',default=[]);a=p.parse_args();b=r.folder(a.batch)
paths=sorted((b/f'screens-{a.phase}').glob('*390-start.png'))
if a.details:paths=sorted(x for x in (b/f'screens-{a.phase}').glob('*390-page*.png') if any(i in x.name for i in a.details))
label=f'{a.phase}-'+('details' if a.details else 'starts')
for n in range(0,len(paths),4):
 canvas=Image.new('RGB',(1560,874),'#eeeeee');d=ImageDraw.Draw(canvas)
 for j,path in enumerate(paths[n:n+4]):
  with Image.open(path) as im:assert im.size==(390,844);canvas.paste(im,(390*j,30))
  d.text((390*j+4,6),path.name,fill='black')
 dest=b/f'{label}{n//4+1}.png';canvas.save(dest);print(dest)
