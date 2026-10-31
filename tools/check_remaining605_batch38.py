import re,itertools
from fractions import Fraction as F
import pdfplumber
import review_remaining605 as r
b=r.folder(38);rows=r.read(b/'revealed-current.json');src={x['id']:x for x in r.read(b/'blind-source.json')};own={x['id']:x for x in r.read(b/'own-solves.json')}
def norm(s):
 return re.sub(r'[\s①②③④⑤「」\uf000\uf02c^]','',s).replace('[빈칸]','').replace('ㆍ','·').replace('\ue0a8','μ').replace('\ue09e','β').replace('\ue0fc','x').replace('∼','～')
checks=[]
for row in rows:
 q=row['question'];m=src[q['id']];native=re.sub(r'책형\s*\d+쪽','',m['sourceText']);native=re.sub(r'^\s*\[\d+～\s*\d+\] 다음 글을 읽고 물음에 답하시오[.]\s*','',native)
 native=re.sub(r'(?m)^\s*'+str(q['number'])+r'[.]\s*','',native,count=1)
 if q['number']==12 and '2026-' in q['id']:
  start=native.index('<라운드별');end=native.index('①',start);table=native[start:end]
  t=q['tables'][0];assert norm(table)==norm('<'+t['caption']+'>'+''.join(t['columns'])+''.join(''.join(z) for z in t['rows']));native=native[:start]+native[end:]
 if q['number']==8 and '2025-' in q['id']:
  assert native.count('(가) (나)')==1;native=native.replace('(가) (나)','');assert q['choiceNote']=='(가) → (나)'
 # Shared source paragraphs precede the question prompt in the PDF.
 if q['id'].endswith('2026-03-07-psat-s-19') or q['id'].endswith('2026-03-07-psat-s-40'):
  prompt=re.search(r'윗글.*?\?',native,re.S).group();assert norm(prompt)==norm(q['prompt']);native=native.replace(prompt,'',1);expected=q['body']+''.join(q['choices'])
 else:expected=q['prompt']+q['body']+''.join(q['choices'])
 actual,expected=norm(native),norm(expected)
 if actual!=expected:
  i=next((i for i,(a,c) in enumerate(zip(actual,expected)) if a!=c),min(len(actual),len(expected)));raise AssertionError((q['id'],i,actual[i:i+100],expected[i:i+100]))
 with pdfplumber.open(r.ROOT/row['officialKey']) as pdf:pi,t=next((i+1,p.extract_text()) for i,p in enumerate(pdf.pages) if '영역 상황판단' in (p.extract_text() or ''))
 assert q['examDate'][:4] in t and f"책형 {q['book']}" in t.replace('㉯','나').replace('㉮','가')
 ans={}
 for line in t.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
   z=list(map(int,line.split()));ans.update(zip(z[::2],z[1::2]))
 assert ans[q['number']]==q['answer']==own[q['id']]['answer']
 checks.append(dict(id=q['id'],source=m['source'],page=m['page'],nativeAndFiveChoices=True,key=row['officialKey'],keyPage=pi,ownAnswerMatches=True))
# Independent exhaustive integer score/strike enumeration, at most six hits per 13 points.
possible=[(3*h+2*d,h+d,h,d) for h in range(5) for d in range(7) if 0<3*h+2*d<=13]
triples=[z for z in itertools.product(possible,repeat=3) if sum(a[0] for a in z)==13]
games=[(a,c) for a in triples for c in triples if a[2][0]==7 and c[1][0]==5 and a[0][0]>c[0][0] and a[1][0]<c[1][0] and a[2][0]>c[2][0] and sum(x[1] for x in a)<sum(x[1] for x in c)]
assert len(games)==1 and [x[0] for x in games[0][0]]==[3,3,7] and [x[0] for x in games[0][1]]==[2,5,6]
assert F(2,100)*1000/F(25,10)==8
def response(tribe,other,ate):
 rule=other if tribe=='C' else tribe
 return ('아니' if ate else '응') if rule=='A' else ('응' if ate else '아니')
cases=[(a,c,h,k) for a,c in itertools.permutations('ABC',2) for h,k in itertools.product([False,True],repeat=2) if response(a,c,h)=='아니' and response(c,a,k)=='응']
assert len(cases)==6 and ('A','B',True,True) in cases and ('A','C',True,False) in cases and ('B','A',False,False) in cases
assert [F(7,10)*F(6,10)*(F(3,10)*s+10) for s in [150,180,215,300,330]]==list(map(F,['23.1','26.88','31.29','42','45.78']))
volumes=[30*7,30*5,int(60*F(5,2)),40*9,20];assert sum(100<=v<200 for v in volumes)==2
assert 1000-760==240 and (1+40//10)*760==3800
assert 75-50==50-25==25 and 51-26==26-1
r.write(b/'source-key-model-checks.json',dict(status='PASS',count=10,checks=checks,scoreStrikeGames=games,tribeCases=cases,coffeeVolumes=volumes,lawScope='Supplied exam rules only; original plan creator/confirmer/notifier is minister, opinion providers are heads of related central agencies and governors.',sourceBookQuotes='s03 PDF visual confirms「外래어 표기법」; normalized only quote glyph extraction, existing app preserves proper Korean title.',ratioProof='p>=20 μm and 0<d<=2.5 μm imply p/d>=20/2.5=8; no area or volume substitution.'))
r.write(b/'post-reveal-reasoning-correction.json',dict(id='kr-mpm-2025-03-08-psat-s-01',answerBefore=5,answerAfter=5,issue='Own first reasoning inverted plan creator and opinion providers and described20-day notification as opinion submission. Published explanation already correct. Original own file remains immutable.',corrected='국토교통부장관이 기본계획 수립·변경·확정하고 관계기관장 및 시도지사에게 의견을 듣는다. 확정일부터20일 이내 통보·공고도 장관이다. 예외외20%증가에는 의견청취와위원회심의가필요하다.',source='Article00 paragraphs1–3, source image original-pair1.png.',notAnAppDefect=True))
p=r.read(r.OUT/'progress.json');p.setdefault('postRevealReasoningCorrections',{})['kr-mpm-2025-03-08-psat-s-01']='batch38/post-reveal-reasoning-correction.json';r.write(r.OUT/'progress.json',p)
print('PASS10 original/native/key checks; integer games, six tribe cases, exact arithmetic. Own s01 subject correction explicitly retained.')
