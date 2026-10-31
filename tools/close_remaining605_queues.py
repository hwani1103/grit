import collections
import review_remaining605 as r
out=r.OUT/'final';assert r.read(out/'current900-evidence-ledger.json')['status']=='PASS'
p=r.OUT/'cross-candidates-weighted-cancellation.json';v=r.read(p);assert r.read(r.folder(11)/'batch-verification.json')['status']=='verified'
for x in v['candidates']:assert x['id']=='kr-mpm-2025-07-19-psat-s-15';x.update(status='source_model_and_host_reverified',evidence='batch11/batch-verification.json')
r.write(p,v)
def statuses(v):
 if isinstance(v,dict):
  if 'status' in v:yield v
  for z in v.values():yield from statuses(z)
 elif isinstance(v,list):
  for z in v:yield from statuses(z)
queues=[]
for p in sorted(r.OUT.glob('cross-candidates*.json')):
 v=r.read(p);rows=list(statuses(v))
 for x in rows:
  assert not any(s in x['status'] for s in ['pending','candidate_not','open_']), (p.name,x)
  e=x.get('evidence')
  if e and ';' not in e:assert (r.OUT/e.split(':')[0]).exists(),(p.name,e)
 queues.append(dict(file=p.name,sha256=r.sha(p),statusCounts=dict(collections.Counter(x['status'] for x in rows)),rowCount=len(rows)))
v=r.read(r.OUT/'cross-validation.json');before=out/'cross-validation-before-closure.json';assert not before.exists();r.write(before,v)
mapping={1:['initial','word-boundaries31','numeric-word-boundaries18','fuel-word-boundaries20'],2:['initial'],3:['max-premise','structure-and-extrema','minimum-boundary31'],4:['structure-and-extrema'],5:['structure-and-extrema','law-quotes32'],6:['underline-label','underline-object34','underline-period46','underline-tail49'],7:['time-anchor'],8:['situation-raster-body'],9:['data-raster-prose'],10:['weighted-cancellation'],11:['bound-direction'],12:['inclusive-or-wording'],13:['word-unit-and-conditional-direction','choice-percent-boundaries24','unit-exponent29'],14:['minimum-boundary31','word-boundaries31'],15:['option-label-mapping22','option-single-label-mapping22'],16:['verdict-only-reasons28'],17:['structure-and-extrema','word-unit-and-conditional-direction'],18:['count-ratio40']}
for x in v['findings']:
 x['statusBeforeClosure']=x['status'];x['status']='closed_with_scope_evidence';x['closureEvidence']=[f'cross-candidates-{s}.json' for s in mapping[int(x['id'][-3:])]];x['closure']='Fixed605 individual source reviews complete; associated cause queues contain only verified or explicitly scoped non-defect screenings. Negative screening is not whole-item semantic re-review.'
 if 'pendingCandidateCount' in x:x['pendingCandidateCountAtDiscovery']=x['pendingCandidateCount'];x['pendingCandidateCount']=0
 if 'remainingCandidates' in x:x['remainingCandidatesAtDiscovery']=x['remainingCandidates'];x['remainingCandidates']='No unresolved entries in recorded cause queues.'
v['status']='cross_review_complete_pending_final_regression_and_release';v['closedAt']=r.now();v['queueClosureEvidence']='final/cross-queue-closure.json'
# Distinguish visual evidence from independence; all review here was performed by the same author.
for x in v['causeFamilies']:
 if x['id']=='source-render':x['check']=x['check'].replace('independent visual review','separate visual inspection (same author)')
r.write(r.OUT/'cross-validation.json',v)
related=v['relatedPrior295Reviews'];associated=v['associated605Reviews']
r.write(out/'cross-queue-closure.json',dict(status='PASS',checkedAt=r.now(),queues=queues,unresolvedCandidateEntries=0,closedCauseFamilies=18,relatedPrior295Unique=len({x['id'] for x in related}),associated605Unique=len({x['id'] for x in associated}),limitations='67 option-label rows were screened only for prefix/subset mismatch;6 header rows only for legitimate complete prose introduction. Neither counts as a new full semantic re-review. Original ratings unchanged. Same-author review.'))
print('Cause queues closed; unique related295',len({x['id'] for x in related}),'associated605',len({x['id'] for x in associated}))
