"""Verify a release APK against current assets and an existing release key."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
from zipfile import ZipFile


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apk', required=True, type=Path)
    parser.add_argument('--previous', required=True, type=Path)
    parser.add_argument('--build-tools', required=True, type=Path)
    parser.add_argument('--name', required=True)
    parser.add_argument('--code', required=True, type=int)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    args.output.mkdir(parents=True, exist_ok=True)

    def certificate(apk, log):
        result = subprocess.run(
            [str(args.build_tools / 'apksigner.bat'), 'verify', '--verbose',
             '--print-certs', str(apk.resolve())],
            check=True, capture_output=True, text=True,
        )
        (args.output / log).write_text(result.stdout, encoding='utf-8')
        return re.search(r'certificate SHA-256 digest: (\w+)', result.stdout).group(1)

    current_cert = certificate(args.apk, 'certificate.txt')
    previous_cert = certificate(args.previous, 'previous-certificate.txt')
    assert current_cert == previous_cert, 'Release signing certificate changed'
    result = subprocess.run(
        [str(args.build_tools / 'aapt.exe'), 'dump', 'badging',
         str(args.apk.resolve())],
        check=True, capture_output=True, text=True, encoding='utf-8',
    )
    (args.output / 'badging.txt').write_text(result.stdout, encoding='utf-8')
    for expected in ["name='com.gritpractice.grit'",
                     f"versionCode='{args.code}'", f"versionName='{args.name}'",
                     "native-code: 'arm64-v8a'"]:
        assert expected in result.stdout, expected

    questions = 0
    images = 0
    with ZipFile(args.apk) as archive:
        assert not any('.secrets/' in n or n.endswith(('.jks', '.keystore'))
                       for n in archive.namelist())
        for path in (root / 'assets/psat').rglob('*'):
            if not path.is_file():
                continue
            name = 'assets/flutter_assets/' + path.relative_to(root).as_posix()
            assert archive.read(name) == path.read_bytes(), name
            if path.suffix == '.png':
                images += 1
            elif path.suffix == '.json':
                data = json.loads(path.read_text(encoding='utf-8'))
                if isinstance(data, list):
                    questions += len(data)
    assert questions == 900
    manifest = json.loads((root / 'assets/psat/sets.json').read_text(encoding='utf-8'))
    ranks = {'기본': 0, '혼합': 1, '심화': 2, '고난도': 3}
    for subject in ['자료해석', '언어논리', '상황판단']:
        sets = sorted((s for s in manifest['sets'] if s['subject'] == subject),
                      key=lambda s: s['order'])
        assert [s['order'] for s in sets] == list(range(1, 31))
        difficulty = [ranks[s['difficulty']] for s in sets]
        assert difficulty == sorted(difficulty)
    report = {
        'status': 'PASS', 'apk': str(args.apk.resolve()),
        'bytes': args.apk.stat().st_size, 'sha256': digest(args.apk),
        'versionName': args.name, 'versionCode': args.code,
        'package': 'com.gritpractice.grit', 'abi': 'arm64-v8a',
        'certificateSha256': current_cert, 'matchesPreviousCertificate': True,
        'questionCount': questions, 'imageCount': images, 'setCount': 90,
        'allPackagedPsatAssetsMatchSource': True, 'difficultyOrderVerified': True,
        'previousApkSha256': digest(args.previous),
    }
    (args.output / 'release-verification.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8',
    )
    print(json.dumps(report, ensure_ascii=True))


if __name__ == '__main__':
    main()
