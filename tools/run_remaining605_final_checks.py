import sys,re,subprocess,os
import review_remaining605 as r
out=r.OUT/'final';mode=sys.argv[1];plan=r.read(out/'test-update-plan.json');files=[x['file'] for x in plan]
env=os.environ.copy();env.update(FLUTTER_ALREADY_LOCKED='true',CI='true',FLUTTER_ROOT='C:/tools/flutter')
base=['C:/tools/flutter/bin/cache/dart-sdk/bin/dart.exe','C:/tools/flutter/bin/cache/flutter_tools.snapshot','--no-version-check','--suppress-analytics']
if mode=='unit':
 titles=r.read(out/'updated-unit-test-titles.json');args=base+['test','--no-pub','--concurrency=1','--name','^(?:'+'|'.join(map(re.escape,titles))+')$']+files
elif mode=='widget':
 titles=['all nine native situation tables fit cover and open widths','situation Set10 special text fits cover and opened fold','verbal Set11 special text fits cover and opened fold','verbal Set19 special text fits cover and opened fold']
 args=base+['test','--no-pub','--concurrency=1','--name','^(?:'+'|'.join(map(re.escape,titles))+')$','test/psat_situation04_test.dart','test/psat_situation10_test.dart','test/psat_verbal11_test.dart','test/psat_verbal19_test.dart']
elif mode.startswith('recover'):
 index=int(mode[-1]);file=['test/dialog_fold_test.dart','test/psat_explanation_revision_test.dart','test/psat_test.dart'][index-1]
 args=base+['test','--no-pub','--concurrency=1',file]
 if index==3:
  completed=['all published complete explanations remain reachable at (Size(320.0, 640.0), 1.4)','all published complete explanations remain reachable at (Size(390.0, 844.0), 1.0)']
  args+=['--name','^(?!(?:'+'|'.join(map(re.escape,completed))+')$).*']
elif mode=='analyze':args=base+['analyze','--no-pub','lib','test']
else:raise ValueError(mode)
tag=sys.argv[2] if len(sys.argv)>2 else mode
log=out/(tag+'.log');assert not log.exists(),log
r.write(out/(tag+'-command.json'),dict(startedAt=r.now(),args=args,scope='Executable lib/test only; artifacts contain intentionally archived historical source snapshots.' if mode=='analyze' else 'Source-grounded updated tests; initial full regression log preserved.'))
with log.open('w',encoding='utf-8') as f:ret=subprocess.run(args,cwd=r.ROOT,env=env,stdout=f,stderr=subprocess.STDOUT).returncode
r.write(out/(tag+'-exit.json'),dict(exitCode=ret,finishedAt=r.now(),log=log.name));print(mode,'exit',ret);sys.exit(ret)
