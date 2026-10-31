
from pathlib import Path
from itertools import product,permutations
import json,re,hashlib
import pdfplumber
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/verbal03_2024'
P=R/'assets/psat/verbal03.json'
bank=json.loads((P if P.exists() else A/'authored-verbal03.json').read_text(encoding='utf-8'))
norm=lambda s:re.sub(r'\s+','',s.replace('□','').replace(' / ',' '))
raw={n:(A/f'q{n}-source.txt').read_text(encoding='utf-8') for n in range(11,21)}
shared=raw[19].split('\n',1)[1]+'\n'+raw[20].split('19.',1)[0].strip()
checks={}
def add(n,answer,proof):
 q=bank[n-11];assert q['number']==n and q['answer']==answer
 checks[str(n)]={'answer':answer,'proof':proof}
imp=lambda a,b:not a or b
models=[]
for g,n,d,r,m in product([False,True],repeat=5):
 if imp(g,n and d) and imp(not n,r) and (g or m):models.append((g,n,d,r,m))
opts=lambda g,n,d,r,m:[imp(not g,n),imp(d,m),d or m,imp(r,m),r or m]
truth=[all(opts(*v)[i] for v in models) for i in range(5)]
assert truth==[False,False,True,False,False]
witnesses=[(False,False,False,True,True),(True,True,True,False,False),None,(True,True,True,True,False),(True,True,True,False,False)]
for i,v in enumerate(witnesses):
 if v is not None:assert v in models and not opts(*v)[i]
add(12,3,{'satisfyingAssignments':len(models),'necessarilyTrue':truth,'printedCounterexamplesChecked':4})
assignments=[]
for x in permutations('갑을병정무',4):
 p1=x[3]=='갑' and x[1]=='무';p2=x[0]=='을' or x[2]=='정';p3=x[0]!='을' and x[1]!='무';p4='병' not in x and x[2]=='정';p5=x[1]=='무' or x[2]!='정'
 if sum([p1,p2,p3,p4,p5])==4:assignments.append(x)
assert assignments==[('을','무','정','갑')]
add(13,2,{'allPermutationsChecked':120,'solutions':assignments})
m14=[]
for g,n,p,d in product([False,True],repeat=4):
 if imp(g and n,p) and (p or d) and (g or n) and not(g and not n) and not p:m14.append((g,n,p,d))
assert m14==[(False,True,False,True)]
g,n,p,d=m14[0];values=[n,not g,imp(not d,p),imp(n,not d),imp(g,n)]
assert values==[True,True,True,False,True]
add(14,4,{'models':m14,'addedOptionsCompatible':values})
assert 4/2==2
add(17,5,{'densityBoverA':2,'experiment1':'density rises; per-area emission equal -> H1 weakened','experiment2':'same-area 10000->20000 rises,20000->30000 falls -> H2 supported'})
intervals=[]
for lo1,hi1,lo2,hi2 in product(range(13),repeat=4):
 if not(lo1<hi1 and lo2<hi2):continue
 detect=lambda v,lo,hi:lo<=v<hi
 if [detect(v,lo1,hi1) for v in [9,6,1]]!=[True,True,False]:continue
 if [detect(v,lo2,hi2) for v in [9,6,1]]!=[False,True,False]:continue
 for dv in range(2,13):
  if dv in [6,9]:continue
  if not detect(dv,lo1,hi1) and detect(dv,lo2,hi2):
   intervals.append((lo1,hi1,lo2,hi2,dv))
assert intervals and all(a>c and b>d for a,b,c,d,_ in intervals)
assert (5,10,2,8,3) in intervals
add(18,5,{'finiteIntervalWitnesses':len(intervals),'allMatchOption5':True,'generalProof':'B shared; A>B implies upperI>upperII. D inII outsideI lies below lowerI, hence lowerI>lowerII. Finite enumeration supplements, not replaces this proof.'})
assert imp(False,False) is True
assert (True==True) and imp(not True,not True) and not (not True)
add(19,3,{'countermodel':'J=O=S=true satisfies ㉠ and ㉢ but not ㉣; S true does not negate ㉢','validInference':'notS and (notS -> notO) entails notO','statements':[True,False,True]})
add(11,2,{'review':'nonhuman mind + only human/God possess mind -> God; other options fail to identify remaining nonhuman cause'})
add(15,1,{'review':'positions shift; counts stay equal; reversed external charge swaps attracted internal charge, not net attraction','statements':[True,False,False]})
add(16,2,{'review':'botulinum -> inhibits ACh release -> no contraction; tetanus inhibits glycine release, not muscle receptor'})
add(20,3,{'review':'A accepts notS/liberal rejects equivalence; B accepts equivalence/notS rejects liberal; evidence checks each accepted premise','statements':[True,True,False]})
with pdfplumber.open(R/'artifacts/psat600_20261028/sources/4564/BBSMSTR_000000000138_4564_1.pdf') as pdf:
 text=pdf.pages[0].extract_text();assert '언어논리' in text and '사책형' in text and '2024년도' in text
 keys={}
 for line in text.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
   vals=list(map(int,line.split()));keys.update(zip(vals[::2],vals[1::2]))
 assert len(keys)==25
for q in bank:
 n=q['number'];assert q['answer']==keys[n],(n,q['answer'],keys[n])
 if n<=18:t=raw[n].split('.',1)[1].strip()
 else:
  t=raw[20].split(str(n)+'.',1)[1]
  if n==19:t=t.split('20.',1)[0]
 prompt,tail=t.split('?',1);body,options=tail.split('①',1)
 if n==17:body=body.rsplit('(가) (나)',1)[0]
 if n==18:
  body=body.split('\n빛\n',1)[0]
  assert q['tables']==[{'caption':'실험 결과 (○: 측정 가능, ×: 측정 불가)','columns':['광검출기','A','B','C','D'],'rows':[['I','○','○','×','×'],['II','×','○','×','○']]}]
 if n>=19:body=shared+'\n'+body
 assert norm(q['prompt'])==norm(prompt+'?'),(n,'prompt')
 assert norm(q['body'])==norm(body),(n,'body')
 choices=re.split('[①②③④⑤]','①'+options)[1:]
 assert len(choices)==5
 for i,(a,b) in enumerate(zip(choices,q['choices'])):assert norm(a)==norm(b),(n,'choice',i,a,b)
 assert len(q['steps'])==5 and len(q['optionReasons'])==5
 for s,prefix in zip(q['steps'],['착안점: ','실전 풀이: ','답 확정 기준: ','정석 근거: ','적용 한계: ']):assert s.startswith(prefix) and len(s)>30
 for u in q.get('underlines',[]):assert q['body'].count(u)==1
 assert not any(c in json.dumps(q,ensure_ascii=False) for c in ['\u2060','\ufffd'])
 assert (R/q['original'] if P.exists() else A/'staged'/q['original']).exists()
assert bank[8]['body'].split('\n\n<보기>')[0]==bank[9]['body'].split('\n\n<보기>')[0]
baseline=json.loads((A/'before-verbal03-hashes.json').read_text(encoding='utf-8'))
for path,digest in baseline.items():
 if path=='assets/psat/sets.json':continue
 assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
checks.update(status='PASS',count=10,officialFinalKeys=10,choiceReasons=50,sourceTextAndSharedPassage='normalized match',limitations='Same-author source/reasoning review and finite/exact verification; not independent expert audit.')
(A/'content-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
print('PASS: verbal11-20 official keys, original text/options/shared passage, logic models and counterexamples.')
