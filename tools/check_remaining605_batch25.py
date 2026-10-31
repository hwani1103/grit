import re
import pdfplumber
import review_remaining605 as r
b=r.folder(25);rows=r.read(b/'revealed-current.json');sources={x['id']:x for x in r.read(b/'blind-source.json')};own={x['id']:x for x in r.read(b/'own-solves.json')}
def norm(s):return re.sub(r'[\s①②③④⑤·ㆍ․/\uf000『』]','',s.replace('\ue09d','α').replace('\ue09e','β'))
checks=[]
for row in rows:
 q=row['question'];m=sources[q['id']];native=re.sub(r'^.*?\b'+str(q['number'])+r'[.]\s*','',m['sourceText'],count=1,flags=re.S)
 if q['number']==10:
  native,n=re.subn(r'유형 연령 취업 여부.*?전환형 34세 이상 49세 이하 상관 없음','',native,count=1,flags=re.S);assert n==1
  assert q['tables']==[dict(caption='바우처 유형별 지급 대상',columns=['유형','연령','취업 여부'],rows=[['준비형','19세 이상 34세 미만','미취업'],['성장형','19세 이상 34세 미만','취업'],['전환형','34세 이상 49세 이하','상관 없음']],afterParagraph=0)]
 if q['number']==23:
  native=native.replace('<일반 지원 프로그램>','').replace('<긴급 지원 프로그램>','')
  expected_rows=[[['1','지자체','신청 접수'],['2','㉠','현장 평가'],['3','㉡','㉣'],['4','A 위원회','㉤'],['5','㉢','사업비 교부'],['6','지자체','사업 추진']],[['1','A 위원회','신청 접수'],['2','㉥','㉦'],['3','○○청','사업비 교부'],['4','지자체','사업 추진']]]
  assert [t['rows'] for t in q['tables']]==expected_rows
  assert all(t['columns']==['순서','담당 기관','절차'] and t['afterParagraph']==2 for t in q['tables'])
 if q['number'] in [14,19]:
  header='(가) (나)' if q['number']==14 else '(가) (나) (다)'
  assert q['choiceNote']==header.replace(' ', ' → ')
  native,n=re.subn(re.escape(header), '',native,count=1);assert n==1
 expected=q['prompt']+q['body']+''.join(q['choices'])
 a,z=norm(native),norm(expected)
 if a!=z:
  i=next((i for i,(u,v) in enumerate(zip(a,z)) if u!=v),min(len(a),len(z)));raise AssertionError((q['id'],i,a[max(0,i-20):i+100],z[max(0,i-20):i+100]))
 with pdfplumber.open(r.ROOT/row['officialKey']) as pdf:
  pi,text=next((i+1,p.extract_text()) for i,p in enumerate(pdf.pages) if '영역 언어논리' in (p.extract_text() or ''))
 assert q['examDate'][:4] in text and f"책형 {q['book']}" in text
 answers={}
 for line in text.splitlines():
  if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
   v=list(map(int,line.split()));answers.update(zip(v[::2],v[1::2]))
 assert answers[q['number']]==q['answer']==own[q['id']]['answer']
 checks.append(dict(id=q['id'],source=m['source'],page=m['page'],nativeAndFiveChoices=True,key=row['officialKey'],keyPage=pi,answer=q['answer'],ownMatches=True))
strokes=[]
for n,y,expected in [(6,89.574,'전이'),(9,482.404,'자료 조사')]:
 m=sources[f'kr-mpm-2026-07-18-psat-l-{n:02}']
 with pdfplumber.open(r.ROOT/m['source']) as pdf:
  p=pdf.pages[m['page']-1];lines=[l for l in p.lines if abs(l['top']-y)<.01 and abs(l['top']-l['bottom'])<.1];assert len(lines)==1;l=lines[0]
  s=''.join(c['text'] for c in p.chars if l['x0']<=(c['x0']+c['x1'])/2<=l['x1'] and l['top']-10<c['bottom']<l['top']+2)
  assert s==expected;strokes.append(dict(number=n,y=y,text=s))
r.write(b/'source-key-model-checks.json',dict(status='PASS',count=10,checks=checks,underlineStrokes=strokes,models={'l04':'Shared improvement possibility, different necessary route; 5.','l06':{'classification':['유용','침입','배제'],'truth':[True,False,False]},'l09':'Three distinct proposals map to proportion/course count/volunteer completion comparison. Relevance is not causal identification.','l10':'Age19/34/49 boundaries; residency applies to all; large firm excludes growth independently of use conditions.','l11':{'implications':['N→Q','R→G','S→H'],'countermodelToSufficiency':{'H':True,'S':False}},'l13':'A asserts inner states necessary; B questions criterion without asserting state existence.','l14':{'wavelength':'C>B>A','frequencyAndEnergy':'A>B>C','size':'A<B<C','minima':['A','C']},'l19':['short wavelength improves','large aperture worsens','heavier atoms worsen'],'l20':{'P':['+','−'],'Q':['0','+'],'R':['−','0'],'truth':[True,True,True]},'l23':{'labels':{'㉠':'지자체','㉡':'○○청','㉢':'○○청','㉣':'서류 평가','㉤':'심의','㉥':'A 위원회','㉦':'심의'},'diagramNodesManuallyComparedToOriginal':True}},limitations='Same-author review; separate host, repair and preservation evidence required.'))
print('PASS10 native/source/key/own answers, three native tables and two precise original underline strokes.')
