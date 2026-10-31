"""Freeze the remaining review inventory; does not solve, score or edit content."""
from pathlib import Path
from collections import Counter
import datetime
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/psat_remaining605_20261030/preparation'
assert not OUT.exists(), 'Frozen preparation already exists; do not overwrite.'
read = lambda p: json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
digest = lambda q: hashlib.sha256(json.dumps(q, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
phases = [
    ('initial15', 'artifacts/psat_quality_audit_20261029/ratings15.json'),
    ('extra30', 'artifacts/psat_quality_audit_20261029/extra30/ratings30-before.json'),
    *[(phase or 'first50', f'artifacts/psat_final_quality_20261029/{phase + "/" if phase else ""}ratings50-before.json')
      for phase in ['', 'followup50', 'holdout50', 'final50', 'acceptance50']],
]
prior = []
for phase, path in phases:
    for row in read(path)['ratings']:
        prior.append(dict(id=row['id'], subject=row['subject'], phase=phase,
                          scoreBeforeFix=row.get('score', row.get('scoreBeforeFix')),
                          evidence=path))
prior_ids = {r['id'] for r in prior}
assert len(prior) == len(prior_ids) == 295
assert dict(Counter(r['scoreBeforeFix'] for r in prior)) == {4: 85, 5: 206, 3: 4}
ledger = {r['id']: r for r in read('artifacts/psat_final_quality_20261029/full900/current900-evidence-ledger.json')['questions']}
bank, files = {}, {}
for p in (ROOT / 'assets/psat').glob('*.json'):
    value = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(value, list):
        continue
    for q in value:
        assert q['id'] not in bank
        bank[q['id']] = q
        files[q['id']] = p.relative_to(ROOT).as_posix()
assert len(bank) == 900 and set(bank) == set(ledger) and prior_ids <= set(bank)
for qid, q in bank.items():
    assert digest(q) == ledger[qid]['questionSha256'], qid
sets = read('assets/psat/sets.json')['sets']
membership = {qid: dict(setId=s['id'], setOrder=s['order'], setPosition=pos)
              for s in sets for pos, qid in enumerate(s['questionIds'], 1)}
assert len(membership) == 900
subjects = ['언어논리', '상황판단', '자료해석']
targets = {}
for subject in subjects:
    selected = [q for qid, q in bank.items() if qid not in prior_ids and q['subject'] == subject]
    selected.sort(key=lambda q: (membership[q['id']]['setOrder'], membership[q['id']]['setPosition']))
    targets[subject] = [dict(id=q['id'], subject=subject, **membership[q['id']],
                            revision=q['revision'], questionSha256=digest(q),
                            file=files[q['id']], officialSource=ledger[q['id']]['officialSource'],
                            originalNumber=q['number'], status='not_started') for q in selected]
assert [len(targets[s]) for s in subjects] == [202, 202, 201]
batches = []
for i in range(20):
    for subject in subjects:
        batches.append(dict(batch=len(batches)+1, questions=targets[subject][i*10:(i+1)*10]))
batches.append(dict(batch=61, questions=[q for s in subjects for q in targets[s][200:]]))
ordered = [q for b in batches for q in b['questions']]
assert len(ordered) == len({q['id'] for q in ordered}) == 605
assert not ({q['id'] for q in ordered} & prior_ids)
assert {q['id'] for q in ordered} | prior_ids == set(bank)
OUT.mkdir(parents=True)
write = lambda name, value: (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
meta = dict(preparedAt=datetime.datetime.now().astimezone().isoformat(), status='prepared_only_not_started',
            bankCount=900, previouslyScoredCount=295, remainingCount=605,
            remainingBySubject={s:len(targets[s]) for s in subjects},
            batchSizes=[len(b['questions']) for b in batches],
            completedInThisReview=0, scoredInThisReview=0,
            method='All remaining IDs, deterministic Set/position order, subjects alternate every10; final5 combined. No authored titles/answers/explanations in target list. Full snapshot is archival and must not be opened before blind solving.')
write('targets605.json', dict(**meta, batches=batches))
write('previously-scored295.json', dict(count=295, distributionBeforeFix=dict(Counter(r['scoreBeforeFix'] for r in prior)), questions=prior))
write('baseline900.json', dict(questionCount=900, questions=[bank[k] for k in sorted(bank)]))
write('preparation-checks.json', dict(**meta, current900HashesMatchLedger=True, priorAndRemainingDisjoint=True, unionCount=900, sourceBankEdited=False))
lines = ['605문항 재검수 대상 고정 목록 — 준비만 완료, 재풀이·평가0개',
         '언어논리202 / 상황판단202 / 자료해석201. 기존 개별 평가295개 제외.',
         '10개 묶음60회 + 마지막5개. 각 묶음 검수 완료 후 다음 묶음 진행.\n']
for batch in batches:
    lines.append(f"묶음 {batch['batch']:02d} ({len(batch['questions'])}개)")
    for q in batch['questions']:
        lines.append(f"  {q['subject']} Set {q['setOrder']:02d} · {q['setPosition']}번째 · 원문{q['originalNumber']}번 · {q['id']} · revision{q['revision']}")
    lines.append('')
(OUT/'605문항_대상목록.txt').write_text('\n'.join(lines)+'\n', encoding='utf-8')
print(json.dumps(meta, ensure_ascii=False))
