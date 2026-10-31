"""Audit the 600-question milestone without changing published content."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'artifacts/psat600_20261028'
OUT = ART / 'final600'
OUT.mkdir(exist_ok=True)
read = lambda p: json.loads(p.read_text(encoding='utf-8'))
bank = []
for path in (ROOT / 'assets/psat').glob('*.json'):
    value = read(path)
    if isinstance(value, list):
        bank.extend(value)
counts = Counter(q['subject'] for q in bank)
assert len(bank) == 600 and set(counts.values()) == {200}, counts
ids = {q['id'] for q in bank}
assert len(ids) == 600
sets = read(ROOT / 'assets/psat/sets.json')['sets']
assert len(sets) == 60 and set(Counter(s['subject'] for s in sets).values()) == {20}
members = [qid for s in sets for qid in s['questionIds']]
assert len(members) == len(set(members)) == 600 and set(members) == ids
assert all(len(s['questionIds']) == 10 for s in sets)
old_sets = read(ART / 'verbal16/before-assets_psat_sets.json.txt')['sets']
current_sets = {s['id']: s for s in sets}
assert len(old_sets) == 45
assert all(current_sets[s['id']] == s for s in old_sets)
baseline = read(ART / 'verbal16/before-verbal16-hashes.json')
preserved = 0
for name, digest in baseline.items():
    if name == 'assets/psat/sets.json':
        continue
    assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, name
    preserved += 1
batches = [f'{subject}{n}' for n in range(16, 21) for subject in ('verbal', 'situation', 'data')]
staged_count = 0
for batch in batches:
    folder = ART / batch
    assert (folder / 'completion.txt').is_file(), batch
    assert read(folder / 'content-checks.json')['status'] == 'PASS'
    assert (ROOT / f'assets/psat/{batch}.json').read_bytes() == (folder / f'authored-{batch}.json').read_bytes(), batch
    for staged in (folder / 'staged/assets').rglob('*'):
        if staged.is_file():
            target = ROOT / staged.relative_to(folder / 'staged')
            assert target.read_bytes() == staged.read_bytes(), str(target)
            staged_count += 1
    assert read(folder / 'visual-review.json')['deviceValidation'] is False
for filename in ('lib/psat_model.dart', 'pubspec.yaml'):
    before = (ART / 'verbal16' / ('before-' + filename.replace('/', '_') + '.txt')).read_text(encoding='utf-8')
    current = (ROOT / filename).read_text(encoding='utf-8')
    stripped = ''.join(line for line in current.splitlines(keepends=True)
                       if not re.search(r'assets/psat/(?:verbal|situation|data)(?:1[6-9]|20)\.json', line))
    assert before == stripped, filename
progress = read(ART / 'progress.json')
assert progress['verifiedTotal'] == 600 and progress['uiPending'] is None
result = dict(status='PASS', questions=600, perSubject=dict(counts), sets=60,
              preservedOldSets=45, preservedBaselineAssets=preserved,
              authoredBatchesMatchPublished=15, stagedFilesMatchPublished=staged_count,
              modelAndPubspecChanges='Only the 15 added JSON registrations',
              deviceValidation=False)
(OUT / 'integrity.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result, ensure_ascii=False))
