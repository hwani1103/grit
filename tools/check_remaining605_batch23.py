import re,unicodedata
import pdfplumber
import review_remaining605 as r
b=r.folder(23);rows=r.read(b/'revealed-current.json');sources={x['id']:x for x in r.read(b/'blind-source.json')};own={x['id']:x for x in r.read(b/'own-solves.json')}
norm=lambda s:re.sub(r'[\sㆍ·「」『』]','',unicodedata.normalize('NFKC',re.sub(r'[①②③④⑤ㆍ·]','',s)))
tables={
7:[dict(columns=['구분','1회차','2회차','3회차','4회차','5회차','6회차'],rows=[['甲','가위','?','엄지척','?','?','보'],['乙','?','?','?','가위','?','?']],afterParagraph=5)],
19:[dict(columns=['시설','면적(m²)','정원(명)','사용료(만 원)','비고'],rows=[['A','200','250','1,800','－'],['B','250','300','2,000','－'],['C','600','400','3,600','300 m²씩 분리해 별개의 시설로 사용 가능하며, 이 경우 각 200명씩 수용 가능'],['D','450','350','2,500','A와 동시 예약 시 D 사용료의 30% 할인'],['E','350','200','2,000','B와 동시 예약 시 E 사용료의 25% 할인']],afterParagraph=3)],
20:[dict(columns=['제조사','점수'],rows=[['甲','10'],['乙','8'],['丙','8'],['丁','7']],afterParagraph=0),dict(columns=['크기','점수'],rows=[['대형','7'],['중형','8'],['준중형','9'],['소형','6']],afterParagraph=0),dict(columns=['색상','점수'],rows=[['흰색','10'],['검은색','10'],['회색','7'],['파란색','9']],afterParagraph=0),dict(columns=['가격','점수'],rows=[['1,000만 원 이상 2,500만 원 미만','9'],['2,500만 원 이상 4,000만 원 미만','8'],['4,000만 원 이상','7']],afterParagraph=0),dict(columns=['구분','제조사','크기','색상','가격(만 원)'],rows=[['A','乙','중형','회색','2,400'],['B','丁','대형','검은색','3,000'],['C','甲','소형','회색','4,500'],['D','丙','대형','흰색','5,000'],['E','丁','준중형','파란색','4,700']],afterParagraph=1)]}
blocks={7:['구분 1회차 2회차 3회차 4회차 5회차 6회차 甲 가위 ? 엄지척 ? ? 보 乙 ? ? ? 가위 ? ?'],19:['면적 정원 사용료 시설 비고 (m2) (명) (만 원) A 200 250 1,800 B 250 300 2,000 300m2씩 분리해 별개의 C 600 400 3,600 시설로 사용 가능하며, 이 경우 각 200명씩 수용 가능 A와 동시 예약 시 D 450 350 2,500 D 사용료의 30% 할인 B와 동시 예약 시 E 350 200 2,000 E 사용료의 25% 할인'],20:['제조사 甲 乙 丙 丁 점수 10 8 8 7 크기 대형 중형 준중형 소형 점수 7 8 9 6 색상 흰색 검은색 회색 파란색 점수 10 10 7 9 1,000만 원 이상 2,500만 원 이상 가격 4,000만 원 이상 2,500만 원 미만4,000만 원 미만 점수 9 8 7','구분 제조사 크기 색상 가격(만 원) A 乙 중형 회색 2,400 B 丁 대형 검은색 3,000 C 甲 소형 회색 4,500 D 丙 대형 흰색 5,000 E 丁 준중형 파란색 4,700']}
checks=[]
for item in rows:
 q=item['question'];n=q['number'];m=sources[q['id']];raw=m['sourceText']
 assert not q['figures']
 if n==9:
  common,raw=re.split(r'\n9\.\s*',raw,maxsplit=1)
  common=re.sub(r'^\[9[～~ ]+10\].*?\n','',common)
  common=re.sub(r'책형\s*5쪽','',common)
  assert norm(common)==norm(q['body'])
  expected=norm(q['prompt']+''.join(q['choices']))
 else:
  raw=re.sub(r'^.*?\b'+str(n)+r'\.\s*','',raw,count=1,flags=re.S)
  expected=norm(q['prompt']+q['body']+''.join(q['choices']))
 native=norm(raw)
 if n in tables:
  assert [{k:t[k] for k in ['columns','rows','afterParagraph']} for t in q['tables']]==tables[n]
  for block in blocks[n]:
   assert native.count(norm(block))==1,(n,'table block');native=native.replace(norm(block),'',1)
 if n==19:
  assert native.count(norm('전시 세미나'))==1;native=native.replace(norm('전시 세미나'),'')
  # Original headings identify the choice roles; check their app rendering separately.
  assert q['choices']==['B · A','C · C','D · A','D · B','E · B']
  expected=norm(q['prompt']+q['body']+'B A C C D A D B E B')
 if native!=expected:
  i=next((i for i,(a,c) in enumerate(zip(native,expected)) if a!=c),min(len(native),len(expected)))
  raise AssertionError((n,i,native[max(0,i-30):i+120],expected[max(0,i-30):i+120]))
 checks.append(dict(id=q['id'],source=m['source'],page=m['page'],nativeTextAndFiveChoices=True,tablesAndPlacementChecked=len(q['tables'])))
key=rows[0]['officialKey']
with pdfplumber.open(r.ROOT/key) as pdf:
 pi,t=next((i+1,p.extract_text()) for i,p in enumerate(pdf.pages) if '영역 상황판단' in (p.extract_text() or ''))
assert '2025' in t and '책형 혁' in t
answers={}
for line in t.splitlines():
 if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
  z=list(map(int,line.split()));answers.update(zip(z[::2],z[1::2]))
for item in rows:
 q=item['question'];assert answers[q['number']]==q['answer']==own[q['id']]['answer']
related=r.read(b/'related295-shared10-before.json');relatedOwn=r.read(b/'related295-own-solves.json')[0]
source=r.ROOT/sources[rows[0]['question']['id']]['source']
with pdfplumber.open(source) as pdf:
 p=pdf.pages[4];rt=p.crop((p.width/2,0,p.width,p.height)).extract_text().split('\n10.',1)[1]
common=next(x['question']['body'] for x in rows if x['question']['number']==9)
assert related['body'].startswith(common+'\n\n')
assert norm(rt)==norm(related['prompt']+related['body'][len(common):]+''.join(related['choices']))
assert related['answer']==relatedOwn['answer']==answers[10]==2
r.write(b/'source-key-model-checks.json',dict(status='PASS',count=10,checks=checks,officialKey=key,keyPage=pi,tenOwnAnswersMatch=True,relatedPrior295=dict(id=related['id'],commonAndQuestionAndFiveChoicesExact=True,ownAndOfficialAnswer=2),limitations='Same-author original-source content checks. Given legal/health prose is an exam premise, not current guidance.'))
print('PASS10 full original/native/tables/choice matches and direct official keys; related prior29510 checked.')
