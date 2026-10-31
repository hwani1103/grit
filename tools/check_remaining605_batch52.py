import re,unicodedata,pdfplumber,itertools
import review_remaining605 as r
b=r.folder(52)
def norm(s):return re.sub(r'\s','',unicodedata.normalize('NFKC',re.sub(r'[①②③④⑤]','',s).replace('ㆍ','·')))
ledger={x['id']:x for x in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/current900-evidence-ledger.json')['questions']}
for related in [False,True]:
 prefix='related295-' if related else '';rows=r.read(b/'related295-before.json') if related else [x['question'] for x in r.read(b/'revealed-current.json')]
 src={x['id']:x for x in r.read(b/('related295-source.json' if related else 'blind-source.json'))};own={x['id']:x for x in r.read(b/(prefix+'own-solves.json'))};checks=[]
 for q in rows:
  m=src[q['id']];s=re.sub(r'(?:가\s*)?책형\s*\d+쪽','',m['sourceText']);s=re.sub(r'^\s*\[39～40\] 다음 글을 읽고 물음에 답하시오[.]\s*','',s);s=re.sub(r'(?m)^\s*(?:문\s*)?'+str(q['number'])+r'[.]\s*','',s,count=1)
  if q['examDate']=='2024-03-02' and q['number'] in [39,40]:
   a=norm(s);assert a.count(norm(q['prompt']))==1;a=a.replace(norm(q['prompt']),'',1);e=norm(q['body']+''.join(q['choices']))
  else:a,e=norm(s),norm(q['prompt']+q['body']+''.join(q['choices']))
  if a!=e:
   j=next((j for j,(aa,ee) in enumerate(zip(a,e)) if aa!=ee),min(len(a),len(e)));raise AssertionError((q['id'],j,a[j:j+120],e[j:j+120]))
  key=ledger[q['id']]['officialKey']
  with pdfplumber.open(r.ROOT/key) as pdf:pi,t=next((j+1,p.extract_text()) for j,p in enumerate(pdf.pages) if '영역 언어논리' in (p.extract_text() or ''))
  assert q['examDate'][:4] in t and ('책형 '+q['book']) in t.replace('㉮','가').replace('㉯','나');ans={}
  for line in t.splitlines():
   if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):z=list(map(int,line.split()));ans.update(zip(z[::2],z[1::2]))
  assert ans[q['number']]==q['answer']==own[q['id']]['answer'];checks.append(dict(id=q['id'],source=m['source'],page=m['page'],key=key,keyPage=pi,nativeAndAllFiveChoicesMatch=True,ownMatches=True))
 r.write(b/(prefix+'source-key-checks.json'),dict(status='PASS',checks=checks))
 print(prefix or 'target',len(checks),'source/key/native PASS')
sources=r.read(b/'blind-source.json')+r.read(b/'related295-source.json');strokeChecks=[]
configs={
'kr-mpm-2024-03-02-psat-l-38':([[388.873,407.580]],['동일한 물질에 입사하는 빛의 파장이 짧을수록 전자의 전이시간이 더 길어진다']),
'kr-mpm-2021-07-10-psat-l-13':([[175.728,191.311],[273.781,289.363],[320.769,336.352],[367.758,383.341]],['당신은 나에게 10억 원을 지불한다','그는 당신에게 10만 원을 돌려주지 않는다','(1)은 참일 수밖에 없다','당신은 그에게 10억 원을 지불한다']),
'kr-mpm-2025-03-08-psat-l-07':([[145.693,164.399],[183.105,201.811],[295.342,314.048],[444.992],[519.817,538.523]],['유선 인터넷망이 설치되어 이를 통한 소통이 가능하게 되었을 때만 해도 이만큼의 파급력은 없었다','인터넷으로 메시지를 전하려면 적지 않은 시간과 비용이 필요했기 때문이다','우리는 틈만 나면 스마트폰을 확인하며 늘 어딘가와 연결되어 있다는 사실에 안도한다','스마트폰은 책상과 마찬가지로 사물이다','스마트폰을 타자로 인식하는 순간 나는 스마트폰에 예속된다'])}
for i,(groups,ranges) in configs.items():
 m=next(x for x in sources if x['id']==i);found=[];geometry=[]
 with pdfplumber.open(r.ROOT/m['source']) as pdf:
  p=pdf.pages[m['page']-1]
  for ys,expected in zip(groups,ranges):
   txt=''
   for y in ys:
    ls=[l for l in p.lines if abs(l['top']-y)<.002 and l['height']<.01 and l['x0']>=p.width/2*m['side'] and l['x1']<=p.width/2*(m['side']+1)];assert len(ls)==1
    l=ls[0];chars=[c for c in p.chars if l['x0']-.2<=(c['x0']+c['x1'])/2<=l['x1']+.2 and y-15<c['top']<y];txt+=''.join(c['text'] for c in chars)
    geometry.append({k:l[k] for k in ['x0','x1','top']})
   assert norm(txt)==norm(expected),(i,txt,expected);found.append(expected)
 strokeChecks.append(dict(id=i,source=m['source'],page=m['page'],sourceRanges=found,strokes=geometry,terminalPeriodsExcluded=True if i!=list(configs)[0] else None))
r.write(b/'underline-source-strokes.json',dict(status='PASS',checks=strokeChecks,method='PDF stroke endpoints and character midpoint; full original images inspected. Font overhang extends beyond underline by up to0.58pt; terminal dot midpoints remain beyond endpoint.'))
models=r.read(b/'pre-reveal-exact-models.json');assert models['status']=='PASS' and len(models['hiring32Worlds'])==11
for v in models['detectorAmbiguityExamples']:assert v['M1']==v['T1']+v['R1'] and v['M2']==v['T2']+v['R2'] and v['M1']>v['M2'] and v['R1']>v['R2']
logic=[]
for A,B in itertools.product([False,True],repeat=2):
 S=A or B
 if ((not S) or (not A)) and (S or A):logic.append((A,B))
assert logic==[(False,True)]
r.write(b/'exact-model-checks.json',dict(status='PASS',sourceOnlyModels='pre-reveal-exact-models.json',travelContractUniqueWorld=logic,pBoundary='.01<.04<.05; p=alpha excluded by source strict less-than.',inferenceScope='Strengthening not complete proof; no inference from p to hypothesis truth probability; B drug efficacy unspecified; same source variables and qualifiers verified for all options.'))
print('PASS 10 underline ranges from source strokes;11 hiring worlds;travel logic;detector counterexamples')
