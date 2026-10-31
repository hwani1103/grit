"""Evidence workflow for the fixed 605; never generates solves or ratings.

Run with the bundled Python. Frozen preparation is read-only. Every reveal
requires a separately written solve, and completion requires explicit evidence.
"""
from pathlib import Path
import argparse
import datetime
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/psat_remaining605_20261030'
PREP = OUT / 'preparation'


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def sha(path):
    return hashlib.file_digest(path.open('rb'), 'sha256').hexdigest()


def digest(q):
    return hashlib.sha256(json.dumps(q, ensure_ascii=False, sort_keys=True,
                                     separators=(',', ':')).encode()).hexdigest()


def now():
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).isoformat()


def bank():
    result = {}
    for path in (ROOT / 'assets/psat').glob('*.json'):
        value = read(path)
        if isinstance(value, list):
            for q in value:
                assert q['id'] not in result
                result[q['id']] = q
    return result


def batch(n):
    return read(PREP / 'targets605.json')['batches'][n-1]['questions']


def folder(n):
    return OUT / f'batch{n:02d}'


def init():
    assert not (OUT / 'progress.json').exists(), 'Keep existing review progress.'
    current = bank()
    target = read(PREP / 'targets605.json')
    rows = [q for b in target['batches'] for q in b['questions']]
    prior = read(PREP / 'previously-scored295.json')['questions']
    ids = {q['id'] for q in rows}
    prior_ids = {q['id'] for q in prior}
    ledger = {q['id']: q for q in read(ROOT / 'artifacts/psat_final_quality_20261029/full900/current900-evidence-ledger.json')['questions']}
    assert len(current) == 900 and len(ids) == 605 and len(prior_ids) == 295
    assert not ids & prior_ids and ids | prior_ids == set(current)
    assert all(digest(q) == ledger[qid]['questionSha256'] for qid, q in current.items())
    assert all(digest(current[q['id']]) == q['questionSha256'] for q in rows)
    paths = [p for name in ['lib', 'test', 'assets/psat', 'releases', 'artifacts/vitamin_ui_20261030']
             for p in (ROOT / name).rglob('*') if p.is_file()]
    paths += [ROOT / n for n in ['pubspec.yaml', 'README.md', 'VERIFICATION.md', '비타민_UI_개선보고_2026-10-30.txt']]
    write(OUT / 'preservation-at-start.json', {
        'capturedAt': now(), 'files': {p.relative_to(ROOT).as_posix(): sha(p) for p in paths},
        'questionHashes': {qid: digest(q) for qid, q in current.items()},
        'method': 'Read-only file hashing; no device/app-data access. Baseline snapshot not opened.'})
    write(OUT / 'progress.json', {
        'startedAt': now(), 'status': 'in_progress', 'targetCount': 605,
        'solvedCount': 0, 'scoredCount': 0, 'verifiedCount': 0, 'nextBatch': 1,
        'buildPolicy': 'No intermediate APK build/install/device operation.',
        'limitations': 'Same-author fresh re-solving; not independent expert review.',
        'answerExposureBeforeSolve': {
            '2023-07-22-l-03': 'Official answer visible while inspecting ledger schema before new solve.',
            '2023-07-22-l-04': 'Official answer visible while inspecting ledger schema before new solve.'}})
    write(OUT / 'cross-validation.json', {
        'status': 'in_progress',
        'method': 'Prior295 -> fixed605 and newly found causes -> all900. Candidate searches do not count as semantic clearance.',
        'causeFamilies': [
            {'id': 'source-boundary', 'check': 'Prompt boundary; repeated headings; omitted source blocks; replacement-image coverage.'},
            {'id': 'source-render', 'check': 'Full official page, glyph strokes, footnotes, legend, choice completion; independent visual review.'},
            {'id': 'logic-uniqueness', 'check': 'Necessary/sufficient; feasible counterexamples; exact unique combination among five choices.'},
            {'id': 'numerical-boundary', 'check': 'Denominator/unit; signed rate; rounding interval; separated upper/lower bounds.'},
            {'id': 'explanation-premise', 'check': 'Answer-free cue; reproducible short route; stopping proof; scope and exceptions.'},
            {'id': 'reading-layout', 'check': 'Default screen readability, underline occurrence, diagram empty positions, punctuation.'}],
        'findings': [], 'relatedPrior295Reviews': []})
    print('Initialized real review; 0 solved/scored/verified. Frozen preparation unchanged.')


def blind(n):
    import pdfplumber
    from PIL import Image
    current = bank()
    dst = folder(n)
    records = []
    cache = {}
    try:
        for row in batch(n):
            q = current[row['id']]
            assert digest(q) == row['questionSha256'], f"Baseline changed: {row['id']}"
            src = ROOT / row['officialSource']
            if src not in cache:
                cache[src] = pdfplumber.open(src)
            page_number = q.get('page')
            if page_number is None:
                match = re.search(r'-p(\d+)\.', q['original'])
                assert match, (q['id'], 'Find original page manually')
                page_number = int(match[1])
            page = cache[src].pages[page_number-1]
            side = q.get('side')
            if side is None:
                # Data PDFs sometimes have an extra page or more than two
                # questions per page. Infer from the actual margin heading,
                # never the question's odd/even parity.
                markers = [w for w in page.extract_words()
                           if w['text'] == str(q['number'])+'.'
                           and (w['x0'] < 45 or page.width/2 <= w['x0'] < page.width/2+45)]
                assert len(markers)==1,(q['id'],'Inspect original margin heading manually')
                side = int(markers[0]['x0'] >= page.width/2)
            bounds = (page.width*side/2, 30, page.width*(side+1)/2, page.height)
            text = page.crop(bounds).extract_text() or ''
            shared_range = None
            column_continuation = False
            columns = [page.crop((page.width*s/2,30,page.width*(s+1)/2,page.height)).extract_text() or '' for s in [0,1]]
            combined = '\n'.join(columns)
            shared = re.search(r'\[(?:문\s*)?(\d+)[.]?\s*[～~∼-]\s*(?:문\s*)?(\d+)[.]?\]\s*다음',combined)
            if shared and int(shared[1]) <= q['number'] <= int(shared[2]):
                # Both prose and data use shared sources. The common tables can
                # be on the opposite column even when choices fit this column.
                shared_range = [int(shared[1]),int(shared[2])]
                matches = {n:list(re.finditer(rf'(?m)^(?:문\s*)?{n}[.]\s+',combined))
                           for n in range(shared_range[0],shared_range[1]+1)}
                assert all(len(v)==1 for v in matches.values()),(q['id'],'Inspect shared-source question headings manually')
                starts = {n:v[0] for n,v in matches.items()}
                begin = starts[q['number']].start()
                end = starts[q['number']+1].start() if q['number'] < shared_range[1] else len(combined)
                text = combined[:starts[shared_range[0]].start()] + '\n' + combined[begin:end]
            elif side==0 and '⑤' not in text and '⑤' in columns[1]:
                # Confirmed two-column overflow: choices/report continue at
                # right top, before the next question (or entire right column).
                following = re.search(r'(?m)^\d+[.]\s+(?:다음|위 글|윗글|위 <)',columns[1])
                continuation = columns[1][:following.start()] if following else columns[1]
                assert '⑤' in continuation,(q['id'],'Inspect continuation choices manually')
                text += '\n'+continuation
                column_continuation = True
            assert f"{q['number']}." in text, (q['id'], 'Inspect question boundary manually')
            original = ROOT / q['original']
            with Image.open(original) as im:
                if q['subject'] == '자료해석' or shared_range or column_continuation:
                    # Preserve the whole source page for data: wrapped headers
                    # and common tables cannot be inferred from extracted order.
                    im.save(dst / f"{q['id']}-source.png")
                else:
                    im.crop((im.width*side//2, 0, im.width*(side+1)//2, im.height)).save(dst / f"{q['id']}-source.png")
            records.append(dict(id=q['id'], source=row['officialSource'], page=page_number, side=side,
                                originalNumber=q['number'], sourceText=text,
                                sharedPassageRange=shared_range,
                                columnContinuation=column_continuation,
                                image=f"{q['id']}-source.png"))
    finally:
        for pdf in cache.values():
            pdf.close()
    write(dst / 'blind-source.json', records)
    (dst / 'blind-source.txt').write_text('\n\n'.join(f"=== {r['id']} | original {r['originalNumber']} ===\n{r['sourceText']}" for r in records), encoding='utf-8')
    print((dst / 'blind-source.txt').read_text(encoding='utf-8'))


def reveal(n):
    current = bank()
    solves = read(folder(n) / 'own-solves.json')
    assert {s['id'] for s in solves} == {q['id'] for q in batch(n)}
    for s in solves:
        assert isinstance(s['answer'], int) and 1 <= s['answer'] <= 5
        assert len(s['optionReasons']) == 5 and len(s['reasoning']) > 80
        assert all(len(x) > 12 for x in s['optionReasons'])
    receipt = folder(n) / 'solve-frozen-before-reveal.json'
    if not receipt.exists():
        write(receipt, {'frozenAt': now(), 'solveFileSha256': sha(folder(n) / 'own-solves.json'),
                        'answersExposedPreviously': [qid for qid in read(OUT/'progress.json')['answerExposureBeforeSolve'] if qid in {s['id'] for s in solves}]})
    assert read(receipt)['solveFileSha256'] == sha(folder(n) / 'own-solves.json')
    ledger = {q['id']: q for q in read(ROOT / 'artifacts/psat_final_quality_20261029/full900/current900-evidence-ledger.json')['questions']}
    reviewed = []
    for row in batch(n):
        q = current[row['id']]
        reviewed.append(dict(question=q, officialKey=ledger[q['id']]['officialKey'],
                             officialAnswer=ledger[q['id']]['officialAnswer']))
    write(folder(n) / 'revealed-current.json', reviewed)
    for item in reviewed:
        q = item['question']
        print(json.dumps({k:q.get(k) for k in ['id','revision','answer','title','tag','steps','optionReasons','pitfall','transfer']},ensure_ascii=False,indent=2))
        print('Official answer:',item['officialAnswer'],'key:',item['officialKey'])


def refresh():
    progress = read(OUT / 'progress.json')
    solved, scored, verified = [], [], []
    verified_batches = []
    for n in range(1,62):
        dst = folder(n)
        if (dst/'own-solves.json').exists():
            solved += [q['id'] for q in read(dst/'own-solves.json')]
        if (dst/'ratings-before.json').exists():
            scored += [q['id'] for q in read(dst/'ratings-before.json')['ratings']]
        if (dst/'batch-verification.json').exists():
            proof = read(dst/'batch-verification.json')
            if proof['status'] == 'verified':
                verified += [q['id'] for q in batch(n)]
                verified_batches.append(n)
    assert len(solved) == len(set(solved))
    assert len(scored) == len(set(scored))
    assert len(verified) == len(set(verified))
    progress.update(updatedAt=now(), solvedCount=len(solved), scoredCount=len(scored),
                    verifiedCount=len(verified),
                    remainingCount=progress['targetCount']-len(verified),
                    lastVerifiedBatch=max(verified_batches, default=0),
                    nextBatch=next((n for n in range(1,62) if n not in verified_batches), None))
    write(OUT/'progress.json',progress)
    print(json.dumps(progress,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['init', 'blind', 'reveal', 'refresh'])
    parser.add_argument('batch', type=int, nargs='?', default=1)
    args = parser.parse_args()
    if args.command in ['init', 'refresh']:
        {'init': init, 'refresh': refresh}[args.command]()
    else:
        folder(args.batch).mkdir(parents=True, exist_ok=True)
        {'blind': blind, 'reveal': reveal}[args.command](args.batch)
