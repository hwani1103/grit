"""Shared mechanical gates; each batch supplies its own reviewed content/model proof."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import shutil
import pdfplumber
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def norm(text):
    for old,new in [('\ue09d','α'),('\ue09e','β'),('\ue09f','γ'),('\ue0a8','μ'),('\ue0fc','x')]:text=text.replace(old,new)
    text=text.replace('m^3','m3')
    text=text.replace('cm⁻¹','cm-1')
    for token in ['[빈칸]', '\uf000', '『', '』', '「', '」']:
        text = text.replace(token, '')
    return re.sub(r'[\s·ㆍ․]+', '', text)

def validate(batch, proof, selection, figure_count=0):
    folder = ROOT / 'artifacts/psat600_20261028' / batch
    published = ROOT / 'assets/psat' / f'{batch}.json'
    bank = read(published if published.exists() else folder / f'authored-{batch}.json')
    assert len(bank) == 10
    assert [(q['examDate'], q['number']) for q in bank] == selection
    transcripts = read(folder/'source-transcripts.json') if (folder/'source-transcripts.json').exists() else None
    keys = {}
    for q in bank:
        post = re.search(r'pstId=(\d+)', q['answerUrl'])[1]
        signature = (post, q['subject'])
        if signature not in keys:
            with pdfplumber.open(next((ROOT/f'artifacts/psat600_20261028/sources/{post}').glob('*.pdf'))) as pdf:
                matches = [p.extract_text() or '' for p in pdf.pages]
                text = next(t for t in matches if f"영역 {q['subject']}" in t)
                assert q['examDate'][:4] in text
                assert {'나':'㉯','가':'㉮','인':'인','사':'사'}.get(q['book'],q['book']) in text
                result={}
                for line in text.splitlines():
                    if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?', line):
                        values=list(map(int,line.split())); result.update(zip(values[::2],values[1::2]))
                assert len(result) in [25,40]
                keys[signature]=result
        assert q['answer'] == keys[signature][q['number']]
        assert len(q['choices']) == len(q['steps']) == len(q['optionReasons']) == 5
        assert all(x.strip() for x in q['choices']+q['optionReasons'])
        for s,prefix in zip(q['steps'],['착안점: ','실전 풀이: ','답 확정 기준: ','정석 근거: ','적용 한계: ']):
            assert s.startswith(prefix) and len(s)>40,(q['id'],prefix)
        assert not re.search(r'[\uE000-\uF8FF\uFFFD\u2060\u2024]',json.dumps(q,ensure_ascii=False)),q['id']
        for u in q.get('underlines',[]):assert q['body'].count(u)==1 and '\n' not in u
        if transcripts:
            src=transcripts[q['id']]
            assert norm(q['prompt'])==norm(src['prompt']),(q['id'],'prompt')
            source_body=norm(src['body'])
            for old_text,new_text in src.get('rewrites',[]):
                old_part,new_part=norm(old_text),norm(new_text)
                assert source_body.count(old_part)==1,(q['id'],'reviewed formula')
                source_body=source_body.replace(old_part,new_part,1)
            for block in src.get('removedBlocks',[]):
                fragment=norm(block)
                assert source_body.count(fragment)==1,(q['id'],'removed native block')
                source_body=source_body.replace(fragment,'',1)
            assert norm(q['body'])==source_body,(q['id'],'body')
            if src.get('choiceColumns'):
                columns=src['choiceColumns']
                assert 2<=len(columns)<=3 and norm(' '.join(columns)) in norm(src['body']),(q['id'],'original choice column headings')
                for actual,original in zip(q['choices'],src['choices']):
                    values=original.split()
                    assert len(values)==len(columns) and all(re.fullmatch(r'[－−-]?\d+(?:\.\d+)?',v) for v in values),(q['id'],'original numeric choice row')
                    expected='\n'.join(f'{column}: {value}' for column,value in zip(columns,values))
                    assert norm(actual)==norm(expected),(q['id'],'labeled choice columns')
            else:
                assert all(norm(a)==norm(b) for a,b in zip(q['choices'],src['choices'])),(q['id'],'choices')
    assert sum(len(q['figures']) for q in bank)==figure_count
    manifest=read(folder/'crop-manifest.json')
    if (folder/'original-manifest.json').exists():manifest+=read(folder/'original-manifest.json')
    source_cache={}
    try:
        for c in manifest:
            source=ROOT/c['source']
            assert hashlib.sha256(source.read_bytes()).hexdigest()==c['sha256']
            key=str(source)
            if key not in source_cache:source_cache[key]=pdfplumber.open(source)
            page=source_cache[key].pages[c['page1based']-1]
            ref=page.crop(c['rect']).to_image(resolution=c['resolution'],antialias=True).original.convert('RGB')
            path=ROOT/c['asset'] if published.exists() else folder/'staged'/c['asset']
            im=Image.open(path).convert('RGB')
            assert im.size==ref.size and im.tobytes()==ref.tobytes(),c['asset']
            if '/figures/' in c['asset']:
                x0,y0,x1,y1=c['rect']
                for w in page.extract_words()+page.images:
                    if w['x1']<=x0 or w['x0']>=x1 or w['bottom']<=y0 or w['top']>=y1:continue
                    assert w['x0']>=x0-.5 and w['x1']<=x1+.5 and w['top']>=y0-.5 and w['bottom']<=y1+.5,(c['asset'],'cut boundary',w)
        if transcripts:
            for q in bank:
                removed=transcripts[q['id']].get('removedBlocks',[])
                if not removed or not q.get('figures'):continue
                assets={f['asset'] for f in q['figures']}
                regions=[c for c in manifest if c['asset'] in assets]
                replacement=norm('\n'.join(source_cache[str(ROOT/c['source'])].pages[c['page1based']-1].crop(c['rect']).extract_text() or '' for c in regions))
                for block in removed:
                    assert norm(block) in replacement,(q['id'],'removed native text must be covered by replacement images')
        if (folder/'source-regions.json').exists():
            for number,regions in read(folder/'source-regions.json').items():
                q=next(q for q in bank if q['number']==int(number))
                assets={f['asset'] for f in q['figures']}
                crops=[c for c in manifest if c['asset'] in assets]
                for pg,side,top,bottom in regions:
                    page=source_cache[str(ROOT/crops[0]['source'])].pages[pg-1];mid=page.width/2
                    for w in page.extract_words():
                        if not(mid*side<=w['x0'] and w['x1']<=mid*(side+1) and top<=w['top'] and w['bottom']<=bottom):continue
                        assert any(c['page1based']==pg and c['rect'][0]-.5<=w['x0'] and w['x1']<=c['rect'][2]+.5 and c['rect'][1]-.5<=w['top'] and w['bottom']<=c['rect'][3]+.5 for c in crops),(number,'uncovered word',w)
    finally:
        for pdf in source_cache.values():pdf.close()
    seen=set();old=0
    for path in (ROOT/'assets/psat').glob('*.json'):
        if path.name in ['sets.json',batch+'.json']:continue
        obj=read(path)
        if not isinstance(obj,list):continue
        for q in obj:
            k=(q.get('examDate',q['source'][:10].replace('.','-')),q['subject'],q['number'])
            assert k not in seen,k
            seen.add(k);old+=1
    for q in bank:
        k=(q['examDate'],q['subject'],q['number']);assert k not in seen,k;seen.add(k)
    for path,digest in read(folder/f'before-{batch}-hashes.json').items():
        if path!='assets/psat/sets.json':assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,path
    proof.update(status='PASS',count=10,officialFinalKeys=10,originals=10,figures=figure_count,preservedExisting=old,
        limitations='Same-author original/semantic review with explicit calculations and counterexamples;not independent expert certification.')
    (folder/'content-checks.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'PASS {batch}:10 source/key,{len(manifest)} pixel assets;preserved{old}')

def publish(batch, after, difficulty):
    assert difficulty in ['기본', '심화', '고난도', '혼합'], 'Use an existing Set difficulty label'
    folder=ROOT/'artifacts/psat600_20261028'/batch
    assert read(folder/'content-checks.json')['status']=='PASS'
    progress=read(ROOT/'artifacts/psat600_20261028/progress.json')
    assert progress['uiPending'] is None
    bank=read(folder/f'authored-{batch}.json');subject=bank[0]['subject']
    assert progress['verifiedInApp'][subject]+len(bank)<=progress['goalPerSubject']
    assert progress['verifiedTotal']+len(bank)<=progress['targetTotal']
    order=int(re.search(r'\d+$',batch)[0]);kind=batch[:-len(str(order))]
    set_id=f'psat-{kind}-{order:03}'
    for name in ['lib/psat_model.dart','pubspec.yaml','assets/psat/sets.json']:
        dest=folder/('before-'+name.replace('/','_')+'.txt')
        if not dest.exists():shutil.copy2(ROOT/name,dest)
    assert not (ROOT/'assets/psat'/f'{batch}.json').exists()
    shutil.copy2(folder/f'authored-{batch}.json',ROOT/'assets/psat'/f'{batch}.json')
    for image in (folder/'staged').rglob('*.png'):
        dest=ROOT/image.relative_to(folder/'staged');dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(image,dest)
    for name,anchor,newline in [('lib/psat_model.dart',f"    'assets/psat/{after}.json',",f"    'assets/psat/{batch}.json',"),('pubspec.yaml',f'    - assets/psat/{after}.json',f'    - assets/psat/{batch}.json')]:
        path=ROOT/name;text=path.read_text(encoding='utf-8');assert anchor in text and newline not in text
        path.write_text(text.replace(anchor,anchor+'\n'+newline),encoding='utf-8')
    path=ROOT/'assets/psat/sets.json';sets=read(path)
    assert not any(s['id']==set_id for s in sets['sets'])
    sets['sets'].append(dict(id=set_id,subject=subject,order=order,difficulty=difficulty,questionIds=[q['id'] for q in bank]))
    path.write_text(json.dumps(sets,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    shutil.copy2(folder/f'psat_{batch}_test.dart.txt',ROOT/'test'/f'psat_{batch}_test.dart')
    progress.update(sourceTotalIncludingUiPending=progress['verifiedTotal']+10,uiPending=f'{batch} source/key/model PASS;host UI checks pending',nextBatch=f'{batch} display validation')
    (ROOT/'artifacts/psat600_20261028/progress.json').write_text(json.dumps(progress,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Published {batch};verified remains{progress["verifiedTotal"]}')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('batch');parser.add_argument('--after',required=True);parser.add_argument('--difficulty',required=True)
    args=parser.parse_args();publish(args.batch,args.after,args.difficulty)
