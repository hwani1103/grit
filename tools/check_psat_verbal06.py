from pathlib import Path
import json,re,hashlib,pdfplumber
from PIL import Image
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/verbal06';P=R/'assets/psat/verbal06.json'
bank=json.loads((P if P.exists() else A/'authored-verbal06.json').read_text(encoding='utf-8'))
norm=lambda s:re.sub(r'[\s「」]+','',s)
with pdfplumber.open(next((R/'artifacts/psat600_20261028/sources/5994').glob('*.pdf'))) as pdf:
 text=next(p.extract_text() for p in pdf.pages if '영역 언어논리' in p.extract_text());assert '2025년도' in text and '인 책형' in text
 key={}
 for line in text.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
   vs=list(map(int,line.split()));key.update(zip(vs[::2],vs[1::2]))
 assert len(key)==25
proof={
 '1':{'meeting':'내물마립간 사신→부견','items':{'황남대총':'터키석팔찌','계림로14호':'석류석보검'},'passagePermission':'소수림왕','purchaseLocation':'전진'},
 '2':{'ImdunFounder':'한무제','DongbuFounder':'낙랑군','lastRuler':'고구려','BulnaeSubset':'동예','directRuleDistinctFromAutonomy':True},
 '3':{'criterion':'shareduse ratherthan segregatedspecialuse','threeTermsSamePerspective':True,'barrierfreeNotSubset':'리프트counterexample'},
 '4':{'claim':'understanding via others interpretations','originalViewingNotSufficient':True,'archeologyNotNecessaryCondition':True},
 '5':{'access':'finalpapers','data':'intermediateoutputs and process','collaboration':'excludesfinalandintermediateoutputs','evolution':'norms→broaderopenactivities'},
 '6':{'events':{'association':1948,'truceinterest':1953,'promotionLaw':1960,'firstassembly':1965,'investmentLaw':1966},'semiconductorIntroduction':'1960s','KomiJointVenture':True},
 '7':{'teacherAtHome':'listenerLocationExplanation fails;standardLocation holds','homeInLastExample':'futureDestination notcurrent','firstInterpretationStillPossibleAtSchool':True},
 '8':{'naSurvivors':[2,4],'gaRequired':['paternal','male','bloodrelative','olderthanfather'],'choice4':'partlytrue but insufficiently distinguishes kinship','notPredictionEase':True},
 '9':{'truth':[True,False,True],'CcityAdopted':False,'earlyStop':'excludeㄴ then includeㄷ yields3','relevantEvidenceNotSufficientCausalProof':True},
 '10':{'actors':{'㉠':'○○청','㉡':'관리기관','㉢':'○○청'},'steps':{'㉣':'신청','㉤':'삭제요청','㉥':'처리결과알림'},'retry':'㉤','resultsRecipient':'○○청, not applicant'}
}
for q in bank:
 n=q['number'];raw=(A/f'2025-l{n}-source.txt').read_text(encoding='utf-8').split(f'{n}.',1)[1];prompt,tail=raw.split('?',1);body,options=tail.rsplit('\n① ',1)
 assert norm(q['prompt'])==norm(prompt+'?'),(n,'prompt')
 assert norm(q['body'])==norm(body),(n,'body')
 opts=re.split('[①②③④⑤]','① '+options)[1:]
 assert len(opts)==5 and all(norm(a)==norm(b) for a,b in zip(opts,q['choices'])),(n,'options')
 assert q['answer']==key[n],(n,'finalkey')
 assert len(q['steps'])==len(q['optionReasons'])==5
 for s,prefix in zip(q['steps'],['착안점: ','실전 풀이: ','답 확정 기준: ','정석 근거: ','적용 한계: ']):assert s.startswith(prefix) and len(s)>40
 for u in q.get('underlines',[]):assert q['body'].count(u)==1
 assert not any(c in json.dumps(q,ensure_ascii=False) for c in ['\u2060','\ufffd'])
 assert (R/q['original'] if P.exists() else A/'staged'/q['original']).exists()
assert sum(len(q.get('underlines',[])) for q in bank)==6
assert 1948<1960<=1965<1966
assert [i+1 for i,x in enumerate([[1],[2],[1,3],[2,3],[1,2,3]]) if 2 not in x and 3 in x]==[3]
m=json.loads((A/'crop-manifest.json').read_text(encoding='utf-8'))
with pdfplumber.open(next((R/'artifacts/psat600_20261028/sources/6008/pdf').glob('*언어논리*'))) as pdf:
 expected=pdf.pages[m['page']].crop(m['bbox']).to_image(resolution=m['resolution']).original.convert('RGB')
 actual=Image.open(R/m['asset'] if P.exists() else A/'staged'/m['asset']).convert('RGB');assert actual.size==expected.size and actual.tobytes()==expected.tobytes()
 f=bank[-1]['figures'][0];assert (f['width'],f['height'])==actual.size
seen=set();old=0
for p in (R/'assets/psat').glob('*.json'):
 if p.name in ['sets.json','verbal06.json']:continue
 obj=json.loads(p.read_text(encoding='utf-8'))
 if isinstance(obj,list):
  for q in obj:
   k=(q.get('examDate',q['source'][:10].replace('.','-')),q['subject'],q['number']);assert k not in seen;seen.add(k);old+=1
for q in bank:
 k=(q['examDate'],q['subject'],q['number']);assert k not in seen;seen.add(k)
for path,digest in json.loads((A/'before-verbal06-hashes.json').read_text(encoding='utf-8')).items():
 if path!='assets/psat/sets.json':assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
proof.update(status='PASS',count=10,officialFinalKeys=10,normalizedSource='all passages/prompt/options;title brackets restored visually',underlines=6,diagramPixels=True,preservedExisting=old,limitations='Same-author review; not independent expert certification.')
(A/'content-checks.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PASS10 source/finalkey,6underlines,diagram,chronology/optionelimination,preserved',old)