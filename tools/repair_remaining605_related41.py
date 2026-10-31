import re
from datetime import date
import review_remaining605 as r
b=r.folder(41);old={q['id']:q for q in r.read(b/'related295-before.json')}
assert 'All tests passed!' in (b/'related295-host-before.log').read_text(encoding='utf-8-sig') and r.read(b/'related295-source-key-checks.json')['status']=='PASS'
hist={q['id']:q for q in r.read(r.PREP/'previously-scored295.json')['questions']}
notes={24:'기준일뒤철거명령불소급·임시건축기산일·지자체무상기간·선박별도비과세경로정확. 산림보호법뒤조사와과세기준일어절및상황표제분리정리.',16:'기준丁280보다상하각2명으로중간값확정및전체160/270/350/280/360검산정확.20%의어절만연결한다.'}
assert not (b/'related295-assessment-before.json').exists();r.write(b/'related295-assessment-before.json',[dict(id=i,historicalScorePreserved=hist[i]['scoreBeforeFix'],currentBeforeScore=4,assessment=notes[q['number']],notReplacementOfHistoricalScore=True) for i,q in old.items()])
changes=r.read(r.OUT/'changes-batch41.json')
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  if q['id'] not in old:continue
  prev=old[q['id']];assert q==prev;snap=r.OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();r.write(snap,prev)
  q['body']=q['body'].replace('「산림보호법」 에','「산림보호법」에').replace('재산세 과세 기준일','재산세 과세기준일').replace('<상 황> 사업자','<상 황>\n\n사업자').replace('20 %','20%')
  assert q!=prev and re.sub(r'\s','',q['body'])==re.sub(r'\s','',prev['body']);q['revision']+=1;touched=True
  changes.append(dict(id=q['id'],file=p.relative_to(r.ROOT).as_posix(),oldRevision=prev['revision'],newRevision=q['revision'],changedFields=['body'],beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason=notes[q['number']],cohort='prior295',status='repaired_pending_reverification'))
 if touched:r.write(p,data)
r.write(r.OUT/'changes-batch41.json',changes)
assert len(changes)==8 and date(2025,1,1)>date(2024,12,1) and (date(2024,12,1)-date(2024,4,19)).days<365 and (date(2024,12,1)-date(2023,1,1)).days>365
assert sorted([160,240+30,250+50+50,280,300+60],reverse=True)==[360,350,280,270,160]
r.write(b/'related295-repair-model-checks.json',dict(status='PASS',count=2,source='related295-source-key-checks.json',dateBoundary='2024-12-01 cutoff; demolition2025-01-01 after; temporary construction2024-04-19 less than1year; free public use since2023-01-01 over1year; rescue vessel independent exemption.',subsidies=[160,270,350,280,360],onlyWhitespaceChanged=True,oldScoresTablesAnswersPreserved=True))
print('2related minor repairs; exact source/date/subsidy checks PASS')
