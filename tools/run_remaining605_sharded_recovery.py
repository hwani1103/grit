import sys,subprocess,os,re
import review_remaining605 as r
out=r.OUT/'final';dest=out/'recovery';dest.mkdir(exist_ok=True);scopes=out/'recovery-scopes';scopes.mkdir(exist_ok=True)
base=['C:/tools/flutter/bin/cache/dart-sdk/bin/dart.exe','C:/tools/flutter/bin/cache/flutter_tools.snapshot','--no-version-check','--suppress-analytics','test','--no-pub','--concurrency=1']
env=os.environ.copy();env.update(FLUTTER_ALREADY_LOCKED='true',CI='true',FLUTTER_ROOT='C:/tools/flutter')
specs=[('dialogs','test/dialog_fold_test.dart',['all published leave dialogs stay centered through flat half-open cover and return']),('transitions','test/psat_explanation_revision_test.dart',['all published reviews stay reachable through open-cover-open transitions']),('explanations','test/psat_test.dart',['all published complete explanations remain reachable at (Size(752.0, 834.0), 1.0)','all published complete explanations remain reachable at (Size(840.0, 360.0), 1.0)'])]
runrows=[]
def run(tag,args):
 log=dest/(tag+'.log');exitfile=dest/(tag+'-exit.json')
 if exitfile.exists():
  old=r.read(exitfile);assert old['exitCode']==0;runrows.append(old);return
 assert not log.exists(),log
 r.write(dest/(tag+'-command.json'),dict(args=args,startedAt=r.now()))
 with log.open('w',encoding='utf-8') as f:ret=subprocess.run(args,cwd=r.ROOT,env=env,stdout=f,stderr=subprocess.STDOUT).returncode
 row=dict(tag=tag,exitCode=ret,finishedAt=r.now(),log=log.relative_to(r.ROOT).as_posix());r.write(exitfile,row);runrows.append(row)
 print(tag,'PASS' if ret==0 else 'FAILED',flush=True)
 if ret:sys.exit(ret)
for kind,file,titles in specs:
 pattern='^(?:'+'|'.join(map(re.escape,titles))+')$'
 for start in range(0,900,100):
  args=base+['--name',pattern,f'--dart-define=PSAT_RECOVERY_START={start}','--dart-define=PSAT_RECOVERY_COUNT=100',f'--dart-define=PSAT_RECOVERY_OUTPUT={scopes.relative_to(r.ROOT).as_posix()}',file]
  run(f'{kind}-{start:03d}',args)
 if kind=='explanations':tailpattern=r'^(?!all published complete explanations remain reachable at ).*'
 else:tailpattern='^(?!(?:'+'|'.join(map(re.escape,titles))+')$).*'
 run(kind+'-other',base+['--name',tailpattern,file])
r.write(out/'recovery-runs.json',dict(status='PASS',runs=runrows,method='Fresh single tester per disjoint100-question range. Default test coverage unchanged; successful IDs saved by tests. Two other900-screen cases passed in initial run.'))
print('All recovery ranges and remaining tests passed.',flush=True)
