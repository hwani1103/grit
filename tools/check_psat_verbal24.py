from pathlib import Path
from itertools import permutations,product
import json
from psat_batch_tools import validate,norm
R=Path(__file__).resolve().parents[1];A=R/'artifacts/psat600_20261028/verbal24'
bank=json.loads((A/'authored-verbal24.json').read_text(encoding='utf-8'));own=json.loads((A/'own-solve-before-key.json').read_text(encoding='utf-8'));proof={}
qs={q['number']:q for q in bank}
anchors={6:['사이토카인을 생성하여','수와 다양성이 적정 수준으로 유지된다면','적정 수준으로 회복되어 증상이 개선될 수 있다'],7:['그런데 최근의 연구 결과들은','태어났을 때는','소득 불평등으로 이어질 가능성이 크다'],8:['자리에서 담당하는 일을 뜻한다','평생을 두고 내가 고민하고 추구해야 하는 가치 있는 일','업을 찾지 못하면'],9:['감염 사슬이 유지될 수 있을 정도로','인구밀도는 17세기 이전까지','오래전부터 인구밀도가 높았고'],10:['결과의 좋고 나쁨만으로','당시 주어진 정보에 따른 의사결정 과정의 정당성을 반영해야'],11:['제작자의 창조 의도가 필요하다','창조 의도만 있다고 해서','나뭇가지를 전혀 변형시키지 않았기','예술 작품일 수는 있어도 창조된 것은 아니다'],12:['실험의 정밀성을 인정하더라도','[빈칸]','기존에 알려진 원소의 스펙트럼에 속하지 않는','원소의 결합과는 무관하고 구성 원소에 의해 결정'],15:['동일시될 수 없다','둘 다 무의미하지만','사용 빈도에 대한 통계적 순위','무의미함에도 불구하고 문법적이라면']}
for n,parts in anchors.items():
 for part in parts:assert norm(part) in norm(qs[n]['body']),(n,part)
 proof[str(n)]={'reviewedSourceAnchors':parts,'directRationale':own[str(n)]['rationale'],'reviewLimit':'Evidence anchors corroborate transcription;they do not replace human review of inference and all five option reasons.'}
# Rank-based independent enumeration: 1 beats 2 in final, 3 beats 4 in consolation.
models=[]
for ranks in permutations('갑을병정'):
 a,b,c,d=ranks
 for cross in [False,True]:
  semis=[(a,d),(b,c)] if cross else [(a,c),(b,d)]
  matches=semis+[(a,b),(c,d)]
  if sum(w=='갑' for w,l in matches)!=1 or ('정','을') not in matches or any(('병',x) in matches for x in ['갑','을']):continue
  for depts in permutations(['인사','연구','자재','영업']):
   dept=dict(zip('갑을병정',depts))
   if dept[a]!='연구' or dept[d]!='영업' or any({dept[w],dept[l]}=={'인사','연구'} for w,l in matches):continue
   models.append(dict(ranks=ranks,depts=dept,matches=matches))
assert len(models)==1 and models[0]['ranks']==tuple('정을갑병')
assert models[0]['depts']==dict(zip('갑을병정',['인사','자재','영업','연구']))
proof['13']={'independentRankModels':models,'shortPath':'Nonmeeting HR is3rd;zero-win Byeong;Jeong champion;Eul lost toJeong cannotHR3rd=>Eul2nd.','earlierHandGuessRejectedBeforeOfficialKey':True}
models14=[]
for old in permutations('ABCDE'):
 if old[0]!='C':continue
 for perm in permutations(range(5)):
  new=tuple(old[i] for i in perm)
  if sum(x==y for x,y in zip(old,new))!=1 or new[2]!=old[3] or new[3]!=old[2] or new[4]!='D' or old[4]=='D':continue
  assert new[0]=='C' and new[1]==old[4] and old[1]=='D'
  assert new[1]!='B' or old[4]=='B'
  assert old[4]!='E' or 'A' in new[2:4]
  models14.append({'old':old,'new':new})
assert len(models14)==6
proof['14']={'independentPermutationModels':models14,'truth':[True,True,True]}
for n,truth,answer in [(14,[True,True,True],5),(15,[False,True,False],2)]:
 actual=[i for i,c in enumerate(qs[n]['choices'],1) if [k in c for k in 'ㄱㄴㄷ']==truth];assert actual==[answer]
 assert own[str(n)]['truth']==truth
assert [q['answer'] for q in bank]==[own[str(q['number'])]['answer'] for q in bank]==[4,3,5,1,2,4,5,2,5,2]
assert len(qs[8]['underlines'])==5 and len(qs[15]['underlines'])==2
assert '산소(O₂)' in qs[12]['body'] and '“[빈칸]?”' in qs[12]['body']
validate('verbal24',{'semanticAndModelProof':proof,'ownSolveBeforeKey':'own-solve-before-key.json','manualOriginalReview':'10 original columns read visually;Q8 five underlined ranges,Q15 two ranges,Q12 oxygen subscript and blank restored without changing source claims.'},[('2024-03-02',n) for n in range(6,16)],0)
