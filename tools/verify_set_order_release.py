"""Verify the numbering-only release against the previous signed release."""
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/psat_set_order_20261031'
APK = ROOT / 'releases/GRIT-1.3.2-5002-PSAT900-ordered-arm64.apk'
OLD = ROOT / 'releases/GRIT-1.3.1-5001-PSAT900-reviewed605-arm64.apk'
PREFIX = 'assets/flutter_assets/assets/psat/'
with ZipFile(OLD) as old, ZipFile(APK) as new:
    entries = {n for n in old.namelist() if n.startswith(PREFIX)}
    assert entries == {n for n in new.namelist() if n.startswith(PREFIX)}
    for name in entries:
        if name == PREFIX + 'sets.json':
            assert new.read(name) == (ROOT / 'assets/psat/sets.json').read_bytes()
        else:
            assert old.read(name) == new.read(name), name
with APK.open('rb') as stream:
    digest = hashlib.file_digest(stream, 'sha256').hexdigest()
result = {
    'status': 'PASS',
    'apk': str(APK),
    'sha256': digest,
    'bytes': APK.stat().st_size,
    'verifiedPsatEntries': len(entries),
    'onlyChangedPsatAsset': 'sets.json',
}
(OUT / 'release-verification.json').write_text(
    json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8'
)
print(json.dumps(result, ensure_ascii=True))
