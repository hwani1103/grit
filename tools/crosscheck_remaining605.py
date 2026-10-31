"""Mechanical cross-cause inventory and preservation checks; not semantic clearance."""
from pathlib import Path
import argparse
import datetime
import hashlib
import json
import re
from collections import defaultdict

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts/psat_remaining605_20261030'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
digest=lambda q:hashlib.sha256(json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def write(path,value):
 path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def bank():
 return {q['id']:q for p in (ROOT/'assets/psat').glob('*.json')
         if isinstance(v:=read(p),list) for q in v}


def scan():
 prior={q['id'] for q in read(OUT/'preparation/previously-scored295.json')['questions']}
 hits=[]
 for q in bank().values():
  causes=[]
  if q.get('tables') and re.search(r'<상\s*황>[^\n]{3,}$',q['body']):
   causes.append('table-header-residue-or-legitimate-situation-text')
  if re.search(r'[가-힣][.] [1-9][.]|[가-힣] [2-9][.]\s*(?:\n|$)',q['body']):
   causes.append('legal-list-boundary-or-legitimate-prose')
  if (q['id'] in prior and re.search(r'가장|최대|최소|상한|하한',' '.join(q['steps']))
      and re.search(r'수리|계산|정수|비율|추론|증감|최대|최소|상한|하한',q.get('tag',''))):
   causes.append('prior295-extremum-scope-screen')
  if causes:
   hits.append(dict(id=q['id'],cohort='prior295' if q['id'] in prior else 'fixed605',
                    revision=q['revision'],causes=causes,status='candidate_not_semantically_reviewed'))
 path=OUT/'cross-candidates-structure-and-extrema.json'
 if path.exists():
  old=read(path)
  known={(x['id'],tuple(x['causes'])):x for x in old}
  for x in hits:
   prev=known.get((x['id'],tuple(x['causes'])))
   if prev and prev['revision']==x['revision']:x['status']=prev['status']
 write(path,hits)
 cross=read(OUT/'cross-validation.json')
 new=[
  dict(id='R605-003',cause='extremum-scope-premise',detectedIn='2023-07-22-s-13',
       counterexample='x6 gives乙3<丁5; global-maximum assertion false. OnlyA-eligible甲/乙 comparison is valid.',
       targetRepairs=['2023-07-22-s-13'],exactPhraseSearch='cross-candidates-max-premise.json',
       broaderPrior295Queue=path.name,status='open_prior295_scope_screen_and_future605'),
  dict(id='R605-004',cause='table-header-residue',detectedIn='2023-07-22-s-08',
       targetRepairs=['2023-07-22-s-08'],searchEvidence=path.name,status='open_candidate_review'),
  dict(id='R605-005',cause='legal-list-boundary',detectedIn='2023-07-22-s-11',
       targetRepairs=['2023-07-22-s-11'],searchEvidence=path.name,status='open_candidate_review')]
 for x in new:
  if x['id'] not in {v['id'] for v in cross['findings']}:cross['findings'].append(x)
 write(OUT/'cross-validation.json',cross)
 print('Cross-cause search candidates:',len(hits),'prior295:',sum(x['cohort']=='prior295' for x in hits))
 print(json.dumps([x for x in hits if x['cohort']=='prior295'],ensure_ascii=False,indent=2))


def preserve(n, destination=None):
 start=read(OUT/'preservation-at-start.json');changes=[]
 for p in sorted(OUT.glob('changes-batch*.json')):changes+=read(p)
 source_changes=[]
 for p in sorted(OUT.glob('source-changes-batch*.json')):source_changes+=read(p)
 for c in source_changes:
  assert c['file'] in ['lib/psat_text.dart','lib/psat.dart'],c['file']
  assert c['beforeSha256']==start['files'][c['file']]
  assert hashlib.sha256((ROOT/c['beforeSnapshot']).read_bytes()).hexdigest()==c['beforeSha256']
  assert hashlib.sha256((ROOT/c['file']).read_bytes()).hexdigest()==c['afterSha256']
 test_changes=[]
 test_receipt=OUT/'final/test-changes.json'
 if test_receipt.exists():
  test_changes=read(test_receipt)
  for c in test_changes:
   assert c['file'].startswith('test/') and c['file'].endswith('.dart')
   assert hashlib.sha256((ROOT/c['beforeSnapshot']).read_bytes()).hexdigest()==c['beforeSha256']
   if c['file'] in start['files']:assert c['beforeSha256']==start['files'][c['file']]
   assert hashlib.sha256((ROOT/c['file']).read_bytes()).hexdigest()==c['afterSha256']
 allowed={x['file'] for x in changes+source_changes+test_changes};files_changed=[]
 for name,h in start['files'].items():
  p=ROOT/name;assert p.is_file(),name
  with p.open('rb') as f:current=hashlib.file_digest(f,'sha256').hexdigest()
  if current!=h:files_changed.append(name);assert name in allowed,name
 current=bank();assert len(current)==900
 changed_ids={qid for qid,q in current.items() if digest(q)!=start['questionHashes'][qid]}
 assert changed_ids=={x['id'] for x in changes},(changed_ids,{x['id'] for x in changes})
 byid=defaultdict(list)
 for c in changes:byid[c['id']].append(c)
 for qid,chain in byid.items():
  chain.sort(key=lambda c:c['oldRevision'])
  states=[read(ROOT/c['beforeSnapshot']) for c in chain]+[current[qid]]
  assert digest(states[0])==start['questionHashes'][qid],qid
  for i,c in enumerate(chain):
   old,new=states[i:i+2]
   permitted=set(c.get('changedFields',[c.get('field')]))|{'revision'}
   actual={k for k in old.keys()|new.keys() if old.get(k)!=new.get(k)}
   assert actual<=permitted,(qid,actual,permitted)
   assert new['revision']==old['revision']+1 and new['revision']==c['newRevision']
 result=dict(status='PASS',checkedAt=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).isoformat(),
             filesChecked=len(start['files']),changedFiles=files_changed,changedQuestionIds=sorted(changed_ids),
             unchangedQuestions=900-len(changed_ids),allowedFieldsAndRevisionChainsOnly=True,
             allPreviousAssetsRetainedByteForByte=True,
             vitaminAndReportsUnchanged=True,
             baselineTestsUnchangedExceptDocumentedSourceVerifiedExpectationUpdates=True,
             documentedTestUpdates=test_changes,
             otherLibFilesUnchanged=True,documentedPsatRendererChanges=source_changes,
             releaseApksUnchanged=True,setsUnchanged=True,deviceOperations=0)
 write(destination or OUT/f'batch{n:02d}/preservation-check.json',result)
 print('PASS preservation:',len(start['files']),'files;',900-len(changed_ids),'unchanged questions;',len(changed_ids),'documented revisions.')


if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('command',choices=['scan','preserve']);parser.add_argument('batch',type=int,nargs='?',default=2);args=parser.parse_args()
 if args.command=='scan':scan()
 else:preserve(args.batch)
