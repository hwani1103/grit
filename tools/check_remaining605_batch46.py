import re,unicodedata,itertools
import pdfplumber
import review_remaining605 as r
b=r.folder(46);rows=r.read(b/'revealed-current.json');src={x['id']:x for x in r.read(b/'blind-source.json')};own={x['id']:x for x in r.read(b/'own-solves.json')}
def norm(s):
 return re.sub(r'\s','',unicodedata.normalize('NFKC',re.sub(r'[①②③④⑤]','',s.replace('ㆍ','·'))))
checks=[]
for row in rows:
 q=row['question'];m=src[q['id']];s=re.sub(r'책형\s*\d+쪽','',m['sourceText']);s=re.sub(r'^\s*'+str(q['number'])+r'[.]\s*','',s,count=1)
 assert norm(s)==norm(q['prompt']+q['body']+''.join(q['choices'])),q['id']
 with pdfplumber.open(r.ROOT/row['officialKey']) as pdf:pi,t=next((j+1,p.extract_text()) for j,p in enumerate(pdf.pages) if '영역 언어논리' in (p.extract_text() or ''))
 assert q['examDate'][:4] in t and f"책형 {q['book']}" in t.replace('㉮','가').replace('㉯','나');ans={}
 for line in t.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):z=list(map(int,line.split()));ans.update(zip(z[::2],z[1::2]))
 assert ans[q['number']]==q['answer']==own[q['id']]['answer'];checks.append(dict(id=q['id'],source=m['source'],page=m['page'],key=row['officialKey'],keyPage=pi,nativeAndAllFiveChoicesMatch=True,ownMatches=True))
# Every distinct bracket and outcome, then all person-department bijections.
worlds=[];people='갑을병정'
for opponent in '을병정':
 rest=[p for p in people if p not in ['갑',opponent]];pairs=[('갑',opponent),tuple(rest)]
 for bits in itertools.product([0,1],repeat=4):
  w=[pairs[j][bits[j]] for j in range(2)];l=[pairs[j][1-bits[j]] for j in range(2)]
  champion=w[bits[2]];runner=w[1-bits[2]];third=l[bits[3]];fourth=l[1-bits[3]]
  games=[(w[j],l[j]) for j in range(2)]+[(champion,runner),(third,fourth)]
  if sum(a=='갑' for a,z in games)!=1 or ('정','을') not in games or ('병','갑') in games or ('병','을') in games:continue
  for departments in itertools.permutations(['인사','연구','자재','영업']):
   d=dict(zip(people,departments))
   if d[champion]!='연구' or d[fourth]!='영업' or any({d[a],d[z]}=={'인사','연구'} for a,z in games):continue
   opts=[runner=='갑' and third=='을',{champion,runner}=={'을','정'},d['병']=='영업' and d['정']=='자재',{d[third],d[fourth]}=={'자재','영업'},set(w)=={'갑','정'}]
   assert opts==[False,True,False,False,False]
   worlds.append(dict(ranking=[champion,runner,third,fourth],departments=d,games=games,options=opts))
assert len(worlds)==1
placements=[]
for old in itertools.permutations('ABCDE'):
 if old[0]!='C':continue
 for new in itertools.permutations('ABCDE'):
  if sum(x==y for x,y in zip(old,new))!=1 or new[2]!=old[3] or new[3]!=old[2] or new[4]!='D' or new[4]==old[4]:continue
  statements=[new[0]==old[0],not(new[1]=='B' and old[1]!='B') or old[4]=='B',old[4]!='E' or 'A' in new[2:4]]
  assert all(statements);placements.append(dict(old=old,new=new,statements=statements))
assert len(placements)==6 and sum(x['new'][1]=='B' for x in placements)==2 and sum(x['old'][4]=='E' for x in placements)==2
r.write(b/'source-key-model-checks.json',dict(status='PASS',count=10,checks=checks,tournament=worlds,departmentPlacements=placements,limits='Own solves preceded reveal; enumerations after reveal independently implement only original constraints. All10 keys had historical exposure, not blind.'))
print('PASS10 native/key checks; unique tournament;6 complete department placements')
