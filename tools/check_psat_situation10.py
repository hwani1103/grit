from pathlib import Path
import json,re,hashlib,pdfplumber,itertools as it,math
from PIL import Image
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/situation10';P=R/'assets/psat/situation10.json';bank=json.loads((P if P.exists() else A/'authored-situation10.json').read_text(encoding='utf-8'));tr=json.loads((A/'source-transcripts.json').read_text(encoding='utf-8'));proof={}
models=[(a,b,c) for a,b,c in it.permutations(range(6),3) if b%2==1 and c in [2,4] and b<a]
opts=[lambda a,b,c:c//2==b//2+1,lambda a,b,c:a%2==0 and a<c,lambda a,b,c:a>c,lambda a,b,c:min(a,b,c)>=2,lambda a,b,c:c>max(a,b)]
solutions=[[v for v in models if f(*v)] for f in opts];assert list(map(len,solutions))==[4,1,7,3,2] and solutions[1]==[(2,1,4)];proof['21']={'allOptionSolutions':solutions,'slotOrder':['MonLunch','MonDinner','TueLunch','TueDinner','WedLunch','WedDinner']}
# exhaustive strings and an independent absorbing-state recurrence
paths=[''.join(x) for x in it.product('01',repeat=5) if '111' in ''.join(x)];first={d:sum(s.index('111')+3==d for s in paths) for d in [3,4,5]};assert len(paths)==8 and first=={3:4,4:2,5:2}
states=[1,0,0,0]
for day in range(5):states=[sum(states[:3]),states[0],states[1],states[2]+2*states[3]]
assert sum(states)==32 and states[3]==len(paths) and states[3]*200000//32==50000;proof['22']={'installPatterns':paths,'firstDayPaths':first,'absorbingCounts':states,'totalInstalled':50000}
# every legal membership size and sex composition, with exact inequality at half
committees=[(n,m,n-m) for n in range(4,11) for m in range(n+1) if 3*(n-4)>=n and 2*m>n-m and 2*(n-m)>m];assert min(n for n,m,f in committees)==6 and (7,3,4) in committees
attendance8=[a for a in range(1,9) if 3*a>=2*8];assert min(attendance8)==6 and min(math.ceil(2*a/3) for a in attendance8)==4
assert all(3*7>=2*n for n in range(7,11)) and 3*5>=2*7
proof['18']={'legalMemberships':committees,'attendanceAt8':attendance8,'minYesAt8':4,'fiveYesTwoWritten':'always quorate for legal board total7..10 and5/7yes>=2/3','optionTruth':[True,True,True,False,True]}
def allowed(kind,x,y,s):
 avg,one={'general':(100,120),'english':(30,50),'practice':(20,None)}[kind];factor=90 if s>=90 else 100
 return (x+y)*100>=2*avg*factor or (one is not None and max(x,y)*100>=one*factor)
assert not allowed('general',100,80,85)
assert all(s<90 for s in range(101) if not allowed('english',10,45,s))
assert [x for x in range(201) if not allowed('practice',20,x,92)]==list(range(16));assert allowed('practice',20,16,92)
proof['19']={'truth':[False,True,True],'englishMinSatisfactionToAllow':90,'practiceMaxDisallowedAttendance':15}
old=[[10,5,5],[5,5],[7,3],[5,5]];new=[[10,10,5],[5,5,5],[3,7],[]];assert list(map(sum,old))==[20,10,10,10] and list(map(sum,new))==[25,15,10,0] and sum(map(sum,new))==50
assert old[2]!=new[2];proof['20']={'consistent':[False,True,True,False,True],'old':old,'new':new,'totalUnchangedDoesNotEnsureSubcriteriaUnchanged':True}
num=4*6+3*2+1;count=4+3;each=math.ceil(num/count);assert (num,count,each,each*count)==(31,7,5,35);proof['24']={'targetCount':4,'supervisingCount':3,'relatedCount':7,'beforeCeil':'31/7','each':5,'total':35}
assert 100000//50==2000;proof['23']={'signaturesAt100000':2000,'manual':'minister-requested referendum exception;all submissions via governor;localchief+councilrecommend;no preapproval requirement','answer':1}
codeopts=[('10020','10021'),('10020','10033'),('10033','10034'),('10050','10027'),('20030','10035')]
valid=[a[:2]=='10' and a[2:4]!='03' and a[-1]=='0' and b[:4]=='1003' and b[-1]!='0' for a,b in codeopts];assert valid==[False,True,False,False,False];proof['25']={'valid':valid,'unknownBLastDigit':'can choose another nonzero district marker'}
proof['16']={'classification':['other','statutory'],'manual':'separateapplication/notificationexceptions;mandatorytransfer;statutoryexcludedrepeatclosure','answer':4}
proof['17']={'permitAuthority':['district','metropolitan'],'restrictionAuthority':['minister','governor'],'manual':'procedure cannot confer authority;area15e4triggersmetro;maxrestriction2+1','incorrect':3}
keys={}
with pdfplumber.open(next((R/'artifacts/psat600_20261028/sources/3982').glob('*.pdf'))) as pdf:
 t=next(p.extract_text() for p in pdf.pages if '영역 상황판단' in p.extract_text());assert '2021' in t and '나 책형' in t
 for line in t.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
   v=list(map(int,line.split()));keys.update(zip(v[::2],v[1::2]))
assert [keys[n] for n in range(16,26)]==[4,3,4,5,5,2,5,1,2,2]
norm=lambda s:re.sub(r'[\s□·․]+','',s)
for q in bank:
 n=q['number'];src=tr[q['id']];assert norm(q['prompt'])==norm(src['prompt']) and all(norm(x)==norm(y) for x,y in zip(q['choices'],src['choices'])),(n,'prompt/choice')
 if n==20:assert q['body']=='' and len(q['figures'])==3
 else:assert norm(q['body'])==norm(src['body']),(n,'body')
 assert q['answer']==keys[n] and len(q['steps'])==len(q['optionReasons'])==5
 for s,prefix in zip(q['steps'],['착안점: ','실전 풀이: ','답 확정 기준: ','정석 근거: ','적용 한계: ']):assert s.startswith(prefix) and len(s)>40
 assert not any('\ue000'<=c<='\uf8ff' or c in '\ufffd\u2060\u2024' for c in json.dumps(q,ensure_ascii=False))
assert bank[7]['body']==bank[8]['body'].split('\n\n<상황>')[0] and '㉠ □' in bank[5]['body'] and bank[9]['choiceNote']=='㉠ → ㉡'
for c in json.loads((A/'crop-manifest.json').read_text(encoding='utf-8')):
 source=R/c['source'];assert hashlib.sha256(source.read_bytes()).hexdigest()==c['sha256']
 with pdfplumber.open(source) as pdf:
  p=pdf.pages[c['page1based']-1];ref=p.crop(c['rect']).to_image(resolution=c['resolution'],antialias=True).original.convert('RGB');path=R/c['asset'] if P.exists() else A/'staged'/c['asset'];im=Image.open(path).convert('RGB');assert im.size==ref.size and im.tobytes()==ref.tobytes(),c['asset']
  if '/figures/' in c['asset']:
   x0,y0,x1,y1=c['rect']
   for w in p.extract_words():
    if w['x1']<=x0 or w['x0']>=x1 or w['bottom']<=y0 or w['top']>=y1:continue
    assert w['x0']>=x0-.5 and w['x1']<=x1+.5 and w['top']>=y0-.5 and w['bottom']<=y1+.5,(c['asset'],w)
seen=set();old=0
for path in (R/'assets/psat').glob('*.json'):
 if path.name in ['sets.json','situation10.json']:continue
 obj=json.loads(path.read_text(encoding='utf-8'))
 if isinstance(obj,list):
  for q in obj:
   k=(q.get('examDate',q['source'][:10].replace('.','-')),q['subject'],q['number']);assert k not in seen;seen.add(k);old+=1
for q in bank:
 k=(q['examDate'],q['subject'],q['number']);assert k not in seen;seen.add(k)
for path,digest in json.loads((A/'before-situation10-hashes.json').read_text(encoding='utf-8')).items():
 if path!='assets/psat/sets.json':assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
proof.update(status='PASS',count=10,officialFinalKeys=10,sourceComparison='allnativeprompt/body/options;sharedcomplete;blankrestored;13pixelcomparisons;3figurewordboundaries',preservedExisting=old,limitations='Same-author original/manual rule review plus independent-form exhaustive calculations;not independent expert review.')
(A/'content-checks.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PASS10source/key/original;exhaustive models;preserved',old)
