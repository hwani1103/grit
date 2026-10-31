"""Explicit source-preserving native text/table improvements for batch08."""
from pathlib import Path
import copy,json
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/psat_remaining605_20261030'
read=lambda f:json.loads(f.read_text(encoding='utf-8-sig'))
def write(f,v):f.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert (OUT/'batch08/ratings-frozen.json').exists();assert not(OUT/'changes-batch08.json').exists()
ids={'kr-mpm-2023-07-22-psat-s-20','kr-mpm-2024-07-27-psat-s-23','kr-mpm-2024-07-27-psat-s-24'};changes=[]
for f in (ROOT/'assets/psat').glob('*.json'):
 qs=read(f)
 if not isinstance(qs,list):continue
 dirty=False
 for q in qs:
  if q['id'] not in ids:continue
  old=copy.deepcopy(q);snap=OUT/'before-changes'/f"{q['id']}-r{q['revision']}.json";assert not snap.exists();write(snap,old)
  if q['id']=='kr-mpm-2023-07-22-psat-s-20':
   q['body']='○○국제교육과정 중에 있는 사람은 수료시험에서 5개 과목(A～E) 평균 60점 이상을 받고 한 과목도 과락(50점 미만)이 아니어야 수료할 수 있다.\n\n甲은 수료시험에서 5개 과목 평균 60점을 받았으나 2개 과목이 과락이어서 ○○국제교육과정을 수료하지 못했다. 甲이 돌려받은 답안지에 점수는 기재되어 있지 않았고, 각 문항에 아래와 같은 표시만 되어 있었다. 이는 국적이 서로 다른 각 과목 강사가 자신의 국가에서 사용하는 방식으로 정답ㆍ오답 표시만 해놓은 결과였다.\n\n※ 모든 과목은 각 10문항이며, 각 문항별 배점은 10점이다.\n\n<보기>\n\nㄱ. A: 70점\nㄴ. B: 30점\nㄷ. C: 60점\nㄹ. D: 40점\nㅁ. E: 80점'
   q['tables']=[dict(caption='과목별 답안 표시',columns=['과목']+[str(i)+'번' for i in range(1,11)],rows=[['A','○','○','×','○','×','○','×','○','○','○'],['B','V','×','V','V','V','×','V','×','V','V'],['C','/','○','○','○','○','/','/','○','/','○'],['D','○','○','V','V','V','○','○','V','V','V'],['E','/','/','/','/','×','×','/','/','/','/']],afterParagraph=1)]
   q['figures']=[]
   q['editNote']='공식 원문의 조건·기호·문항별 배점·보기·선택지를 유지했습니다. 본문과 답안 표시 표는 화면의 공통 글자 크기와 어절 줄바꿈으로 표시합니다. 공식 원문 보기에서 원형을 확인할 수 있습니다. 해설은 GRIT에서 별도로 작성했습니다.'
   reason='기본390화면에서긴원문이미지의조건본문까지작게축소되는문제. 동일조건과5행50개기호·배점주석·보기를기존본문/표컴포넌트로전사하여읽기크기를복구한다. 원본과과거이미지삭제없음.'
  elif q['id']=='kr-mpm-2024-07-27-psat-s-24':
   q['body']='甲～丁은 6문제로 구성된 직무능력시험 문제를 풀었다.\n\n○ 정답을 맞힌 경우, 문제마다 기본점수 1점과 난이도에 따른 추가점수를 부여한다.\n\n○ 추가점수는 다음 식에 따라 결정한다.\n추가점수 = (해당 문제를 틀린 사람의 수) / (해당 문제를 맞힌 사람의 수)\n\n○ 6문제의 기본점수와 추가점수를 모두 합한 총합 점수가 5점 이상인 사람이 합격한다.\n\n甲～丁이 6문제를 푼 결과는 다음과 같고, 5번과 6번 문제의 결과는 찢어져 알 수가 없다.\n(○: 정답, ×: 오답)\n\n<보기>\n\nㄱ. 甲이 최종적으로 받을 수 있는 최대 점수는 32/3점이다.\nㄴ. 1～4번 문제에서 받은 점수의 합은 乙이 가장 낮다.\nㄷ. 4명 모두가 합격할 수는 없다.\nㄹ. 4명이 받은 점수의 총합은 24점이다.'
   q['tables']=[dict(caption='시험 결과 (5·6번의 개별 결과는 미상)',columns=['구분','1번','2번','3번','4번','5번','6번'],rows=[['甲','○','×','○','○','미상','미상'],['乙','○','×','○','×','미상','미상'],['丙','○','○','×','×','미상','미상'],['丁','×','○','○','×','미상','미상'],['정답률(%)','75','50','75','25','50','50']],afterParagraph=4)]
   q['figures']=[]
   q['steps'][1]=q['steps'][1].replace('4/3,2,4/3,4','4/3, 2, 4/3, 4').replace('丙·丁은각','丙·丁은 각')
   q['steps'][2]=q['steps'][2].replace('乙·丙,6번','乙·丙, 6번')
   q['optionReasons'][1]=q['optionReasons'][1].replace('乙·丙,6번','乙·丙, 6번')
   q['editNote']='공식 원문의 조건·정답/오답 기호·정답률·보기·선택지를 유지했습니다. 본문·분수식과 시험 결과는 공통 글자 크기로 표시하며, 찢어져 알 수 없는 5·6번의 개별 결과는 ‘미상’으로 구분했습니다. 분수는 정확한 나눗셈 표기(/)를 사용합니다. 공식 원문 보기에서 원형을 확인할 수 있습니다. 해설은 GRIT에서 별도로 작성했습니다.'
   reason='기본화면에서본문과분수식까지이미지와함께작아지는문제. 동일배점식·16개확정기호·8개미상칸·6정답률·4보기를기존본문/표로옮긴다. 미상은오답/0으로대체하지않으며원문찢어진표와모든과거자산보존. 해설붙은띄어쓰기도정리.'
  else:
   assert '9,900L,6일' in q['steps'][1]
   q['steps'][1]=q['steps'][1].replace('4월 5일은 9,900L,6일은 10,000L에 도달한다.','4월 5일에는 급수 후 9,900L가 된다. 4월 6일에는 급수 중 10,000L에 도달하여 물 채우기를 멈춘다.')
   reason='붙은날짜9,900L,6일을분리하고5일급수후와6일급수중의최대량·충전정지를분명히표현한다.'
  fields=sorted(k for k in old.keys()|q.keys() if old.get(k)!=q.get(k));q['revision']+=1;dirty=True
  changes.append(dict(id=q['id'],file=f.relative_to(ROOT).as_posix(),oldRevision=old['revision'],newRevision=q['revision'],changedFields=fields,beforeSnapshot=snap.relative_to(ROOT).as_posix(),reason=reason,status='repaired_pending_reverification'))
 if dirty:write(f,qs)
assert {c['id'] for c in changes}==ids;write(OUT/'changes-batch08.json',changes)
print('Revised3questions;2native text/tables,1dateflow;oldsourceimages/assets preserved.')
