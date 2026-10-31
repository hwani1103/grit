import review_remaining605 as r
b=r.folder(28);before={x['question']['id']:x['question'] for x in r.read(b/'revealed-current.json')};own={x['id']:x for x in r.read(b/'own-solves.json')}
notes={25:'보도·유료정류장·운행 중의 해석을 각 쟁점에 독립 적용한다. 시간과 운전자 이탈, 예외 여부를 구별한 풀이와 다섯 조합 근거가 정확하다.',13:'모든 자격 조합과 채용 쌍을 열거하여 유일한 자격 구성 및 B/D 채용을 확인했다. 대우와 역의 구별, 미채용E의 미술 자격 반례가 명확하다.',14:'존재 증인과 포함 방향, 네 오답의 공통 반례는 정확하다. 원문 PDF 밑줄은 존재한다까지이며 마침표를 포함하지 않으므로 끝 경계를 보정한다.',33:'A공집합 반례, B/비B 스마트팜 두 증인의 구별, 세 농민 정밀농업 반례가 모두 타당하다.',34:'2^16 추천 행렬을 전수 열거하여 기존 해설의49개와 ㄱㄷ 필연성을 확인했다. 사람별 진위 결합과 유일 최다 득표자 조건을 정확히 보존한다.',15:'필요조건과 충분조건, 강화와 입증의 구별 및 ㄱㄴ 제거시 단일선지 확정은 정확하다. 개별 선지 설명 일부가 단순 정오 판정에 그쳐 각 선택지에서 구체적 변경 요인과 반박 이유를 다시 명시한다.',16:'S−E 순위 증명과 최적 크기 미확정 설명은 정확하다. 원문 밑줄은 화학적 증강은 금속 A에서 가장 작다는 주장까지인데 기존은 작다에서 잘려 주장 범위를 원형대로 복원한다.',17:'집단·개인 구별과 책임→원인의 방향, 갑의 집단책임 논증 한계까지 정확하다. 개별 선지 일부에 근거를 보강하고 PDF 줄갈이에서 생긴 기후 위기의 단어 분리를 원문 어절 기후위기로 복원한다.',20:'현실/재현 구별에 대한 직접 반박과 효용·정밀도 사례를 구별한다. 인간과 AI 능력의 동등성까지 증명했다는 과도한 결론을 피한다.',26:'의도적 선택과 악의적 선택, 변조와 위조를 구별한다. 학자들의 입장 요약을 역사적 최종 판단이나 자료 임의 제외 허용으로 확대하지 않는다.'}
fixed={14,15,16,17}
ratings=[dict(id=qid,scoreBeforeFix=4 if q['number'] in fixed else 5,assessment=notes[q['number']],deduction={14:'밑줄 끝 마침표 범위',15:'개별 선지의 구체적 근거 보강',16:'밑줄 끝 주장 범위 누락',17:'개별 선지 근거와 줄갈이 어절 경계'}.get(q['number'],'발견 없음'),needsChange=q['number'] in fixed) for qid,q in before.items()]
assert not (b/'ratings-before.json').exists();r.write(b/'ratings-before.json',dict(method='Same-author original/own solve/key/all options/models/host assessment before edits.',ratings=ratings));r.write(b/'ratings-frozen.json',dict(frozenAt=r.now(),ratingsSha256=r.sha(b/'ratings-before.json'),total=46,count=10,beforeChanges=True))
changes=[]
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  if q['id'] not in before or q['number'] not in fixed:continue
  old=before[q['id']];assert old==q
  snap=r.OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();r.write(snap,old)
  if q['number']==14:q['underlines']=['『근역서화징』에 기록된 작품인 18세기 이전 고지도가 존재한다']
  if q['number']==16:q['underlines']=['화학적 증강은 금속 A에서 가장 작다는 주장']
  if q['number'] in [15,17]:q['optionReasons']=own[q['id']]['optionReasons']
  if q['number']==17:
   assert q['body'].count('기후 위기')==1;q['body']=q['body'].replace('기후 위기','기후위기')
  fields=[k for k in q if q[k]!=old[k]];q['revision']+=1;touched=True
  changes.append(dict(id=q['id'],file=p.relative_to(r.ROOT).as_posix(),oldRevision=old['revision'],newRevision=q['revision'],changedFields=fields,beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason=notes[q['number']],status='repaired_pending_reverification'))
 if touched:r.write(p,data)
assert len(changes)==4;r.write(r.OUT/'changes-batch28.json',changes)
print('Frozen46/50;four targets repaired;answers and original assets unchanged.')
