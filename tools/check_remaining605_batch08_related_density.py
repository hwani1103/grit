"""Prior295 density fixes: direct source cells, key, exact models, preservation."""
from pathlib import Path
from fractions import Fraction as F
import json,re,hashlib
import pdfplumber
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/psat_remaining605_20261030';B=OUT/'batch08'
read=lambda f:json.loads(f.read_text(encoding='utf-8-sig'))
def write(f,v):f.write_text(json.dumps(v,ensure_ascii=False,indent=2,default=str)+'\n',encoding='utf-8')
norm=lambda s:re.sub(r'\s','',s.translate(str.maketrans('³','3')))
bank={q['id']:q for f in (ROOT/'assets/psat').glob('*.json') if isinstance(v:=read(f),list) for q in v}
ledger={q['id']:q for q in read(ROOT/'artifacts/psat_final_quality_20261029/full900/current900-evidence-ledger.json')['questions']}
expected={'kr-mpm-2025-03-08-psat-s-17':3,'kr-mpm-2025-03-08-psat-s-18':2,'kr-mpm-2024-03-02-psat-s-27':2}
columns={
 'kr-mpm-2025-03-08-psat-s-17':[['구분','민원만족도','민원처리 건수','우수답변 선정 건수','미결재 건수','처리기간 초과 건수']],
 'kr-mpm-2025-03-08-psat-s-18':[['사업','총사업비','보조금 총액','보조금 집행액','증액요청 여부']],
 'kr-mpm-2024-03-02-psat-s-27':[['감축률','전기','상수도','도시가스'],['연도','전기(kWh)','상수도(m³)','도시가스(m³)']]}
rows={
 'kr-mpm-2025-03-08-psat-s-17':[[['甲','85점','50건','0건','1건','3건'],['乙','80점','40건','3건','0건','0건'],['丙','85점','40건','1건','0건','1건'],['丁','90점','35건','0건','2건','2건'],['戊','75점','55건','4건','1건','1건']]],
 'kr-mpm-2025-03-08-psat-s-18':[[['A','250,000','200,000','200,000','○'],['B','30,000','27,000','27,000','○'],['C','125,000','120,000','120,000','×'],['D','90,000','81,000','81,000','○'],['E','82,000','65,600','64,600','○']]],
 'kr-mpm-2024-03-02-psat-s-27':[[['5% 이상 10% 미만','600','75','300'],['10% 이상 15% 미만','750','150','600'],['15% 이상','1,000','200','800']],[['2022','400','11','60'],['2023','350','10','51']]]}
officialRows=rows
staff={'甲':(85,50,0,1,3),'乙':(80,40,3,0,0),'丙':(85,40,1,0,1),'丁':(90,35,0,2,2),'戊':(75,55,4,1,1)}
eligible={k:F(s)*F('.8')+n*F('.2')+p-u-l for k,(s,n,p,u,l) in staff.items() if s>=80 and n>=40}
assert eligible=={'甲':74,'乙':75,'丙':76} and max(eligible,key=eligible.get)=='丙'
projects={'A':(250000,200000,200000,True),'B':(30000,27000,27000,True),'C':(125000,120000,120000,False),'D':(90000,81000,81000,True),'E':(82000,65600,64600,True)}
order=sorted([k for k,v in projects.items() if v[3]],key=lambda k:(projects[k][1]>projects[k][2],F(projects[k][1],projects[k][0]),projects[k][1]),reverse=True)
assert order==['E','D','B','A']
reductions=[F(50,400),F(1,11),F(9,60)];assert F('.10')<=reductions[0]<F('.15') and F('.05')<=reductions[1]<F('.10') and reductions[2]==F('.15');assert 750+75+800==1625
for log in ['host-density-prior295.log','host-density-prior295-after.log']:
 assert 'All tests passed!' in (B/log).read_text(encoding='utf-8-sig')
changes=read(OUT/'changes-batch08.json');reviews=[]
for id,answer in expected.items():
 c=next(x for x in changes if x['id']==id);old=read(ROOT/c['beforeSnapshot']);q=bank[id];native=(B/f'density-{id}-source.txt').read_text(encoding='utf-8');e=ledger[id]
 assert q['figures']==[] and len(q['tables'])==len(rows[id])
 for i,table in enumerate(q['tables']):
  assert table['columns']==columns[id][i] and table['rows']==rows[id][i]
  assert all(norm(''.join(row)) in norm(native) for row in table['rows'])
 for k in ['steps','optionReasons','answer','choices','id','original','title','tag','pitfall','transfer','examId','examDate','subject','book','source','sourceUrl','answerUrl']:
  assert q[k]==old[k],(id,k)
 for image in old['figures']:
  f=ROOT/image['asset'];assert hashlib.sha256(f.read_bytes()).hexdigest()==read(OUT/'preservation-at-start.json')['files'][image['asset']]
 with pdfplumber.open(ROOT/e['officialKey']) as pdf:
  pi,t=next((i+1,page.extract_text()) for i,page in enumerate(pdf.pages) if '영역 상황판단' in (page.extract_text() or ''))
 answers={}
 for line in t.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
   v=list(map(int,line.split()));answers.update(zip(v[::2],v[1::2]))
 assert q['answer']==answers[q['number']]==answer
 notes={'kr-mpm-2025-03-08-psat-s-17':'적격甲乙丙74/75/76. 미결재는감점이고미만또는조건은두자격하한을모두충족해야함.비율식·가감점·25개셀·자격OR·8월조건을원문과대조했다.',
        'kr-mpm-2025-03-08-psat-s-18':'증액요청없는C제외,E미집행1000천원우선,D/B90%동률은보조금81000>27000. EDBA순서.모든표셀·천원단위·우선예외와동률기준을대조했다.',
        'kr-mpm-2024-03-02-psat-s-27':'감축률분모2022.전기12.5%,수도1/11,가스15%정확경계로750+75+800=1625.3개지급구간의포함/배제·다음연도2024·m³/kWh단위·두표모든셀을대조했다.'}
 reviews.append(dict(id=id,oldRevision=old['revision'],newRevision=q['revision'],status='source_key_semantics_and_host_reverified',source=e['officialSource'],key=e['officialKey'],keyPage=pi,answer=answer,evaluation=notes[id],nativeTableCellsExactlyMatchSource=True,sourceParagraphFormulaAndUnitsManuallyCompared=True,oldFiguresOriginalAndSnapshotRetained=True,oldHistoricalScoreUntouched=True))
 c['status']='source_key_semantics_and_host_reverified'
write(B/'density-prior295-review.json',dict(status='PASS',reviews=reviews,models=dict(staffScores=eligible,projectOrder=order,reductions=reductions,points=1625),beforeHost='host-density-prior295.log',afterHost='host-density-prior295-after.log',limitations='Same-author source/bounds/readability review,not independent rerating or realdevice validation.'))
write(OUT/'changes-batch08.json',changes)
queue=read(OUT/'cross-candidates-situation-raster-body.json')
for x in queue:
 if x['id'] in expected:x['status']='source_key_semantics_and_host_reverified'
write(OUT/'cross-candidates-situation-raster-body.json',queue)
cross=read(OUT/'cross-validation.json');finding=next(x for x in cross['findings'] if x['id']=='R605-008');finding['related295Repairs']=list(expected)
known={x['id'] for x in cross['relatedPrior295Reviews']}
cross['relatedPrior295Reviews'] += [x for x in reviews if x['id'] not in known]
write(OUT/'cross-validation.json',cross)
print('PASS3prior295source/native cells/officialkeys/exactmodels;4oldfigures retained,12host checks;historical scores untouched.')
