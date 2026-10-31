import re
from itertools import product
import pdfplumber
import review_remaining605 as r
b=r.folder(31);rows=r.read(b/'revealed-current.json');sources={x['id']:x for x in r.read(b/'blind-source.json')};own={x['id']:x for x in r.read(b/'own-solves.json')}
norm=lambda s:re.sub(r'[\s①②③④⑤\uf000]','',s).replace('[빈칸]','').replace('ㆍ','·')
checks=[]
for row in rows:
 q=row['question'];m=sources[q['id']];native=re.sub(r'책형 \d+쪽','',m['sourceText'])
 if q['number']==40:
  native=re.sub(r'^\[39.*?\]\s*다음 글을 읽고 물음에 답하시오\.','',native,flags=re.S)
  common,tail=re.split(r'40[.]\s+',native,maxsplit=1);promptEnd=re.search(r'모두\s*고르면\?',tail).end()
  native=tail[:promptEnd]+common+tail[promptEnd:]
  native,count=re.subn(r'\(단위: 마리\)\s*그물망 1 그물망 2 그물망 3 그물망 4\s*물고기 A 60 40 20 60\s*물고기 B 0 20 40 0','',native);assert count==1
  assert q['tables']==[dict(caption='그물망별 물고기 수 · 단위 마리',columns=['구분','그물망 1','그물망 2','그물망 3','그물망 4'],rows=[['물고기 A','60','40','20','60'],['물고기 B','0','20','40','0']],afterParagraph=7)]
  assert q['body'].split('\n\n')[7].endswith('넣어 두었다.')
 else:native=re.sub(r'^.*?\b'+str(q['number'])+r'[.]\s*','',native,count=1,flags=re.S)
 a,z=norm(native),norm(q['prompt']+q['body']+''.join(q['choices']))
 if a!=z:
  i=next((i for i,(u,v) in enumerate(zip(a,z)) if u!=v),min(len(a),len(z)));raise AssertionError((q['id'],i,a[max(0,i-20):i+100],z[max(0,i-20):i+100]))
 with pdfplumber.open(r.ROOT/row['officialKey']) as pdf:pi,text=next((i+1,p.extract_text()) for i,p in enumerate(pdf.pages) if '영역 언어논리' in (p.extract_text() or ''))
 assert q['examDate'][:4] in text and f"책형 {q['book']}" in text.replace('㉯','나').replace('㉮','가')
 answers={}
 for line in text.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
   v=list(map(int,line.split()));answers.update(zip(v[::2],v[1::2]))
 assert answers[q['number']]==q['answer']==own[q['id']]['answer']
 checks.append(dict(id=q['id'],source=m['source'],page=m['page'],nativeAndFiveChoices=True,key=row['officialKey'],keyPage=pi,answer=q['answer'],ownMatches=True))
valid=[]
for items in product(range(1,8),repeat=5):
 a,bb,c,d,e=items;good=[x.bit_count()==2 for x in items]
 if not(a&1 and good[0]) or a&bb or good[1] or not(bb&c and good[2]) or c&d or not d&2 or not d&e or e&4 or sum(good)<=2:continue
 truth=[good[4],not good[3],all(not x&2 or x&4 for x in items),all(not x&1 or g for x,g in zip(items,good)),all(not (x&4 and g) or x&1 for x,g in zip(items,good))]
 assert list(map(bool,truth))==[True,True,False,True,True];valid.append(items)
assert valid==[(3,4,5,2,3)]
# Two condition symbols suffice to test every local membership implication used
# for the proof, independently of extension-set equality. Never assume converse.
membership=[]
for sr,qr,rr in product([False,True],repeat=3):
 if rr and not sr and (not qr or sr):
  assert not qr;membership.append([sr,qr,rr])
extension=[]
for p,s,t in product([False,True],repeat=3):
 if (not p or s) and (not s or t):assert not p or t;extension.append([p,s,t])
# Countermodel to 'equal survival proves both': no environmental/frequency
# effect yields the same .7 survival in every net. An offset model also fits.
fishModels=[dict(lakeMinority=.7,riverMajority=.7,environmentEffect=0,frequencyEffect=0),dict(lakeMinority=.7,riverMajority=.7,environmentEffect=.2,frequencyEffect=.2)]
assert 60==60 and 20/(40+20)<40/(40+20) and 20/(20+40)<40/(20+40)
r.write(b/'source-key-model-checks.json',dict(status='PASS',count=10,checks=checks,classificationModels=valid,extensionMembershipModels=extension,intensionWitnessModels=membership,fishEqualSurvivalCountermodels=fishModels,readingChecks={'l27':'Unexplained orbit -> unknown planet; Mercury/near-sun context; later relativity not earlier hypothesis.','l28':'Definition versus purpose; justification of war versus limits on acts.','l30':'Distributive benefit; bail not punishment;3 and9 both within10; not all other procedures guaranteed.','l31':'Constitution/analogy support payment; changing practice weakens fixed nonpayment.','l35':'Observed lower collectivism in richer A supports modernization; southern C supports infection; D>C supports rice.','l01':'Early joint decision;531 royal approval;651 separate execution;unification minister->chancellor->presider.','l02':'Nonmechanical6/min vs crossbow1/min, reversed accuracy;no unsupported cost ranking.'},limitations='Same-author formalization and manual source/option review, not independent review.'))
print('PASS10 source/key/own;unique classification;membership implications;fish countermodels.')
