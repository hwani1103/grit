import zipfile,re,hashlib
import review_remaining605 as r
out=r.OUT/'final';apk=r.ROOT/'releases/GRIT-1.3.1-5001-PSAT900-reviewed605-arm64.apk';old=r.ROOT/'releases/GRIT-1.3.0-5000-PSAT900-arm64.apk'
assert r.read(out/'current900-evidence-ledger.json')['status']=='PASS'
cert=(out/'release-certificate.txt').read_text(encoding='utf-8-sig');oldcert=(out/'previous-release-certificate.txt').read_text(encoding='utf-8-sig');getcert=lambda s:re.search(r'certificate SHA-256 digest: (\w+)',s).group(1)
assert getcert(cert)==getcert(oldcert)=='726a4e0da6d5a53471385f606b79b2a52058c032e4578edb3d451a37fa00cda5'
badge=(out/'release-badging.txt').read_text(encoding='utf-8-sig');assert all(x in badge for x in ["name='com.gritpractice.grit'","versionCode='5001'","versionName='1.3.1'","native-code: 'arm64-v8a'"])
bank=r.bank();ledger={x['id']:x for x in r.read(out/'current900-evidence-ledger.json')['questions']};assert all(r.digest(q)==ledger[i]['questionSha256'] for i,q in bank.items())
assets={p.relative_to(r.ROOT).as_posix() for folder in ['figures','originals'] for p in (r.ROOT/'assets/psat'/folder).glob('*.png')}
with zipfile.ZipFile(apk) as z:
 assert not any('.secrets' in n or n.endswith('.jks') for n in z.namelist())
 count=0
 for p in (r.ROOT/'assets/psat').glob('*.json'):
  assert z.read('assets/flutter_assets/'+p.relative_to(r.ROOT).as_posix())==p.read_bytes()
  v=r.read(p)
  if isinstance(v,list):count+=len(v)
 assert count==900
 for a in sorted(assets):assert z.read('assets/flutter_assets/'+a)==(r.ROOT/a).read_bytes(),a
start=r.read(r.OUT/'preservation-at-start.json');assert r.sha(old)==start['files'][old.relative_to(r.ROOT).as_posix()]
report=dict(status='PASS',verifiedAt=r.now(),apk=str(apk),bytes=apk.stat().st_size,sha256=r.sha(apk),package='com.gritpractice.grit',versionName='1.3.1',versionCode=5001,abi='arm64-v8a',certificateSha256=getcert(cert),matchesPreviousReleaseCertificate=True,packagedQuestionCount=count,currentAndHistoricalImageBytesVerified=len(assets),allQuestionJsonAndSetsBytesMatchSource=True,oldReleasePreserved=True,installed=False,deviceOperations=0)
r.write(out/'release-verification.json',report);print(report)
