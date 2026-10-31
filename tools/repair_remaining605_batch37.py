import re
import review_remaining605 as r
b=r.folder(37);old={x['question']['id']:x['question'] for x in r.read(b/'revealed-current.json')}
assert 'All tests passed!' in (b/'host-before.log').read_text(encoding='utf-8-sig') and r.read(b/'source-key-model-checks.json')['status']=='PASS'
key=lambda q:('26' if '2026-03' in q['id'] else '25')+'-'+str(q['number'])
notes={'26-23':'제시문 내 합의·시범·상용운항,생산/사용지원,2030비율을 개별 확인했다. 본문 퍼센트 어절과⑤2030의 설명 공백을 정리한다.','26-24':'공동체 사업주체와 국가 생산지원·재원 마련이라는 두 축 및 다섯 오답범위를 대조했다. 원문 줄갈이로 갈라진 선지 복지비용을 연결한다.','26-37':'답②는 새풀이와 공식키가 일치한다. 다만 해설이③을 영양 장기 주장처럼 묶었고 원문의3시간이상과 정의의3시간초과를 같은 장기 관측으로 단정했다. 복합자극의 인과 분리와 가장 잘 설명한다는 범위도 보완한다.','25-1':'규정과 실제 허용,감독관과학생,진사·생원 대체경로를 모두 정확히 대조했다. 발견된 개선사항 없음.','25-2':'등록과원본의 보존효율·유형제한부재·의궤의독립편찬을 정확히 구분한다. 발견된 개선사항 없음.','25-3':'장비우위·전술숙련과 창의행별각도·방패좌우범위가 일치한다. 해설③2행 표기의 붙어쓰기를 정리한다.','25-4':'사업정산과사적채권 분리,공동출자주체·훈련자·손실추론의한계를 확인했다. 역자이교지와한자괄호의 줄갈이 공백을 복원한다.','25-5':'당사자합의에도 자녀복리로 개입가능,양육비와권리 병존·공동양육가능을 대조했다. 선지 면접교섭권의 줄갈이 어절을 복원한다.','25-8':'세빈칸을 정의·사례·결론과 맞추고고가매수/캡슐프로그램을 구분했다.30%와본문 빈칸뒤조사 및해설괄호앞의 어절을 정리한다.','25-9':'일터예시의필수화,사적이익관철,선거중심한계,부분근거와핵심주장을 구분했다. 원문 줄갈이로 나뉜 이해관계를 연결한다.'}
score=lambda q:3 if key(q)=='26-37' else 5 if key(q) in ['25-1','25-2'] else 4
ratings=[dict(id=i,scoreBeforeFix=score(q),assessment=notes[key(q)],needsChange=score(q)<5,deduction='선지내용 오분류 및 관측 경계·인과범위 과도한 단정' if key(q)=='26-37' else '발견 없음' if score(q)==5 else '원문 어절·해설 공백 개선') for i,q in old.items()]
assert not (b/'ratings-before.json').exists();r.write(b/'ratings-before.json',dict(method='Same-author original solve, all5 options, direct source/key and pre-edit host review; experimental boundary concern frozen before reveal.',ratings=ratings));r.write(b/'ratings-frozen.json',dict(frozenAt=r.now(),ratingsSha256=r.sha(b/'ratings-before.json'),total=41,count=10,beforeChanges=True))
steps37=[
'착안점: 아라비노스는 맛만, 설탕은 맛과 영양을 함께 준다. 같은 자극에서 정상과 α 차단 X의 반응을 먼저 비교한다. 영양만 주는 조건은 없으므로 두 자극의 차이를 영양의 모든 효과를 따로 측정한 것으로 확대하지 않는다.',
'실전 풀이: 맛만 주면 정상은 3분 동안 강화되고 X는 빈도 변화가 없다. 맛의 단기 강화에 α 경로가 관여한다는 설명을 지지한다. 설탕에서는 X도 강화가 3시간 이상 유지되어, 영양이 추가된 조건의 지속 효과를 α 외 경로로 설명하는 ②가 가장 적절하다.',
'답 확정 기준: ②는 맛 단기 반응의 소실과 설탕 반응의 지속을 함께 설명한다. ④는 여기에 영양 단기도 α 경로라는 확인되지 않은 주장을 더한다. 관측된 차이를 설명하면서 미측정 효과를 추가하지 않는 ②를 고른다.',
'정석 근거: ①은 영양의 단기와 장기 모두를 α에 두어 차단 X의 지속 반응을 설명하기 어렵다. ③은 영양 단기 및 맛 단기·장기를 α에 두지만, 영양 단기와 맛 장기는 이 결과로 확인되지 않는다. ⑤는 맛 단기를 다른 경로에 두고 영양 장기를 α에 두어 두 대조 결과와 맞지 않는다. ③이 영양 장기를 주장한 것으로 읽지 않는다.',
'적용 한계: 원문은 장기를 3시간 초과로 정의하지만 실험1은 3시간 이상이라고 보고한다. 정확히 3시간인 경우를 배제할 수 없으므로 장기 정의를 반드시 충족했다고 단정하지 않는다. 이 문항은 두 결과에 가장 적절한 경로 설명을 고르는 문제다. 영양만의 효과·자극 간 상호작용·모든 경로의 필요충분조건까지 확정한 것은 아니다.']
reasons37=[
'맛 단기의 α 관여는 지지되지만, 영양의 단기·장기 모두를 α에 두면 α가 차단된 X에서도 설탕 반응이 지속된 관측을 설명하기 어렵다.',
'맛만 주었을 때 α 차단으로 3분 반응이 사라지고, 영양이 더해진 설탕에서는 지속 반응이 남는다. 이 차이를 가장 적절하게 설명한다.',
'③은 영양 단기와 맛 단기·장기를 α에 둔다. 맛 단기 외에 영양 단기와 맛 장기는 확인되지 않았으며, 설탕에서 X의 반응이 지속된 차이를 설명하지 못한다.',
'맛 단기와 영양 관련 지속 효과를 설명하는 부분은 ②와 같지만, 영양 단기도 α라는 추가 주장은 분리해 측정되지 않았다.',
'맛 단기를 α 외 경로로 설명하면 X의 아라비노스 반응 소실과 맞지 않고, 영양 장기를 α에 두면 X의 설탕 지속 반응도 설명하기 어렵다.']
changes=[]
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  if q['id'] not in old or score(q)==5:continue
  prev=old[q['id']];assert q==prev;k=key(q);snap=r.OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();r.write(snap,prev)
  if k=='26-23':q['body']=re.sub(r'(?<=\d)\s+(?=%)','',q['body']);q['steps']=[s.replace('⑤2030','⑤ 2030') for s in q['steps']]
  if k=='26-24':q['choices']=[s.replace('복지 비용','복지비용') for s in q['choices']]
  if k=='26-37':q['steps']=steps37;q['optionReasons']=reasons37;q['transfer']='통제된 자극·경로 차단의 차이로 설명을 비교하되, 복합 자극에만 있는 요소의 효과를 단독으로 확정하지 않는다. 결과의 시간 범위와 정의의 경계도 따로 대조한다.'
  if k=='25-3':q['steps']=[s.replace('③2행','③ 2행') for s in q['steps']]
  if k=='25-4':q['body']=q['body'].replace('역자이교지 (','역자이교지(')
  if k=='25-5':q['choices']=[s.replace('면접 교섭권','면접교섭권') for s in q['choices']]
  if k=='25-8':
   q['body']=q['body'].replace('30 %','30%').replace('[빈칸] 까지','[빈칸]까지').replace('[빈칸] 에','[빈칸]에').replace('[빈칸] (이)','[빈칸](이)')
   q['steps']=[s.replace('이므로(나)','이므로 (나)').replace('이므로(다)','이므로 (다)') for s in q['steps']]
  if k=='25-9':q['body']=q['body'].replace('이해 관계','이해관계')
  fields=sorted(k for k in q if q[k]!=prev[k]);assert fields;q['revision']+=1;touched=True
  assert re.sub(r'\s','',q['body'])==re.sub(r'\s','',prev['body']) and [re.sub(r'\s','',s) for s in q['choices']]==[re.sub(r'\s','',s) for s in prev['choices']]
  changes.append(dict(id=q['id'],file=p.relative_to(r.ROOT).as_posix(),oldRevision=prev['revision'],newRevision=q['revision'],changedFields=fields,beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason=notes[k],status='repaired_pending_reverification'))
 if touched:r.write(p,data)
assert len(changes)==8;r.write(r.OUT/'changes-batch37.json',changes)
r.write(b/'repair-semantic-checks.json',dict(status='PASS',count=8,sourceBodyChoicesAndAnswersPreserved=True,experimentSourceBoundaryNotAltered=True,originalChoice3MappedCorrectly=True,explanationClaimsLimitedToBestExplanation=True))
print('Frozen41/50;8 repairs; experiment score3; original body/options/answers preserved')
