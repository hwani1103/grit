"""Record only a batch whose source and host UI checks have actually passed."""
from pathlib import Path
import argparse
import json
import re

parser = argparse.ArgumentParser()
parser.add_argument('batch')
parser.add_argument('--note', required=True)
parser.add_argument('--visual', action='append', required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
folder = root / 'artifacts/psat600_20261028' / args.batch
proof = json.loads((folder / 'content-checks.json').read_text(encoding='utf-8'))
assert proof['status'] == 'PASS'
log = (folder / 'flutter-final.log').read_text(encoding='utf-8-sig')
assert 'All tests passed!' in log and '[E]' not in log
for path in args.visual:
    assert (root / path).is_file(), path
bank = json.loads((root / 'assets/psat' / (args.batch + '.json')).read_text(encoding='utf-8'))
assert len(bank) == 10 and len({q['subject'] for q in bank}) == 1
progress_path = root / 'artifacts/psat600_20261028/progress.json'
progress = json.loads(progress_path.read_text(encoding='utf-8'))
completed = folder / 'completion.txt'
assert not completed.exists(), 'Do not count the same batch twice'
subject = bank[0]['subject']
progress['verifiedInApp'][subject] += 10
progress['verifiedTotal'] = sum(progress['verifiedInApp'].values())
assert progress['verifiedInApp'][subject] <= progress['goalPerSubject']
assert progress['verifiedTotal'] <= progress['targetTotal']
kind, number = re.fullmatch(r'(verbal|situation|data)(\d+)', args.batch).groups()
following = {'verbal': f'situation{number}', 'situation': f'data{number}', 'data': f'verbal{int(number)+1}'}[kind]
production_done = progress['verifiedTotal'] == progress['targetTotal']
progress.update(uiPending=None, sourceTotalIncludingUiPending=progress['verifiedTotal'],
    nextBatch='최종 품질검증: 새50문항 사전고정·평균4.8목표·필요시 나머지 전수검토·개선' if production_done else following + ': 원본·정답·해설 검토',
    currentTaskStatus='제작 수량 완료;최종 품질검증·개선 진행 필요;목표 완료 아님' if production_done else f"10문항씩 검수 진행;과목별{progress['goalPerSubject']}/총{progress['targetTotal']} 목표;품질 원칙과 중간 표본 점검 유지",
    lastVerification=args.batch + ': ' + args.note,
    currentVersion=f"Installed APK1.2.1+2006 unchanged;current host source{progress['verifiedTotal']}questions;no new build/install")
prepared = progress.get('preparedUnpublished', {})
prepared.pop(args.batch, None)
note = (f"2026-10-29 {args.batch} 검증 완료: {args.note}. "
        f"호스트 검증 합계{progress['verifiedTotal']}({progress['verifiedInApp']}). "
        f"기존 UI/기능 유지;APK 빌드·설치·기기 조작 없음. 과목별{progress['goalPerSubject']}/총{progress['targetTotal']} 목표.\n")
completed.write_text(note, encoding='utf-8')
(folder / 'visual-review.json').write_text(json.dumps({
    'reviewedHostScreens': args.visual, 'deviceValidation': False,
    'reviewNote': args.note}, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
progress_path.write_text(json.dumps(progress, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
for name in ['PSAT_CONTENT_REVIEW.md', 'VERIFICATION.md', '다음세션_600문항_제작_인수인계_2026-10-28.txt']:
    with (root / name).open('a', encoding='utf-8') as out:
        out.write('\n\n'+note)
print(f"Verified {progress['verifiedTotal']}: {args.batch}")
