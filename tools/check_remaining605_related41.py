import re,unicodedata
import pdfplumber
import review_remaining605 as r
b=r.folder(41);old={x['id']:x for x in r.read(b/'related295-before.json')};src={x['id']:x for x in r.read(b/'related295-source.json')};own={x['id']:x for x in r.read(b/'related295-own-solves.json')}
def norm(s):return re.sub(r'\s','',unicodedata.normalize('NFKC',re.sub(r'[①②③④⑤「」□]','',s).replace('․','·').replace('ㆍ','·'))).replace('[빈칸]','')
ledger={x['id']:x for x in r.read(r.ROOT/'artifacts/psat_final_quality_20261029/full900/current900-evidence-ledger.json')['questions']};checks=[]
for i,q in old.items():
 s=re.sub(r'책형\s*\d+쪽','',src[i]['sourceText']);s=re.sub(r'^\s*(?:문\s*)?'+str(q['number'])+r'[.]\s*','',s)
 if q['number']==16:
  start=s.index('구분 차량가액');end=s.index('①',start);table=s[start:end]
  assert norm(table)==norm('구분 차량가액(만 원) 차종 유종 甲 160 승용 휘발유 乙 240 승용 경유 丙 250 화물 경유 丁 280 승합 휘발유 戊 300 화물 휘발유')
  assert q['tables'][0]['columns']==['구분','차량가액(만 원)','차종','유종'] and q['tables'][0]['rows']==[['甲','160','승용','휘발유'],['乙','240','승용','경유'],['丙','250','화물','경유'],['丁','280','승합','휘발유'],['戊','300','화물','휘발유']] and q['tables'][0]['afterParagraph']==5
  s=s[:start]+s[end:]
 a,e=norm(s),norm(q['prompt']+q['body']+''.join(q['choices']))
 if a!=e:
  j=next((j for j,(x,y) in enumerate(zip(a,e)) if x!=y),min(len(a),len(e)));raise AssertionError((i,j,a[j:j+120],e[j:j+120]))
 with pdfplumber.open(r.ROOT/ledger[i]['officialKey']) as pdf:pi,t=next((j+1,p.extract_text()) for j,p in enumerate(pdf.pages) if '영역 상황판단' in (p.extract_text() or ''))
 assert q['examDate'][:4] in t and f"책형 {q['book']}" in t.replace('㉮','가').replace('㉯','나').replace('㉵','혁');ans={}
 for line in t.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):z=list(map(int,line.split()));ans.update(zip(z[::2],z[1::2]))
 assert ans[q['number']]==q['answer']==own[i]['answer'];checks.append(dict(id=i,source=src[i]['source'],page=src[i]['page'],key=ledger[i]['officialKey'],keyPage=pi,sourceAllChoicesAndKeyMatch=True))
r.write(b/'related295-source-key-checks.json',dict(status='PASS',checks=checks))
print('2 related direct original/key PASS')
