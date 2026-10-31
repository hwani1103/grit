import re
import review_remaining605 as r
b=r.folder(31);old={x['question']['id']:x['question'] for x in r.read(b/'revealed-current.json')};related=r.read(b/'related295-before.json')[0]
notes={27:'천왕성의 잔차→미지행성 간섭을 수성 근처에 대응하고 태양 근처 관측과 후대 상대성이론을 구별했다. 원문 빈칸·5선지·해설이 일치한다.',28:'직접 정의와 평화 지향, 전쟁 명분과 전투 제약을 구별한다. (가)로4/5, (나)로4의 유일 선택 경로와 오답 근거가 정확하다.',30:'세 정의와 혜택 특혜·보석 판단·10일 기한을 대응한다. 답2와 유일 중단 기준은 맞지만 일부 개별 선지의 틀린 이유가 단순 판정에 그쳐 보강한다.',31:'헌법·민법 유추·관행 변화의 근거 방향이 모두 맞다. 두 밑줄은 원문의 의견까지 포함한다. PDF 줄갈이에서 생긴 구성원 들을 원래 어절로 복원한다.',35:'집단주의와 개인주의 방향, 소득/위도 통제, 경쟁 가설의 반대 예측을 확인했다. 경제 특구·집단 주의의 줄갈이 공백과 일부 개별 이유를 보완한다.',40:'1/4환경만 변화,2/3소수종 우위,ㄷ혼재효과를 검산했다. 공통지문의70 %/95 % 및 그물망3 에서는의 어절 경계와 개별 이유를 개선한다. 공통39번도 새 풀이로 교차확인한다.',33:'일곱 비공집합 속성 조합을 다섯 물품에 전수 대입하여 유일한YS/W/YW/S/YS를 얻었다.4번 고정 반례로3번을 즉시 확정하는 조건과 나머지 네 선지 참이 맞다.',34:'외연P⊆S⊆T, T의Q밖 증인, 내포R의S밖 증인과Q⊆S를 따로 검산했다. 외연같음→내포같음의 역추론을 배제한 해설이 타당하다.',1:'초기 공동결정·531년 재가·651년 집행·통일기 상재상 주재를 모두 대응했다. 원문 줄갈이에 따른 박· 석 및 통일 신라기의 공백을 복원한다.',2:'기병/보병, 기계/비기계, 속도6:1/명중률, 비용비교 대상을 분리한다. 포함→다른부대배제와 제시되지 않은 비용 순위 추론을 배제한 해설이 정확하다.'}
fix={30,31,35,40,1}
ratings=[dict(id=qid,scoreBeforeFix=4 if q['number'] in fix else 5,assessment=notes[q['number']],needsChange=q['number'] in fix,deduction='어절 경계 또는 개별 선지 근거 보완' if q['number'] in fix else '발견 없음') for qid,q in old.items()]
assert not (b/'ratings-before.json').exists();r.write(b/'ratings-before.json',dict(method='Same-author original-only solve then selected key/native/exhaustive models/host pre-edit review.',ratings=ratings));r.write(b/'ratings-frozen.json',dict(frozenAt=r.now(),ratingsSha256=r.sha(b/'ratings-before.json'),total=45,count=10,beforeChanges=True))
historic=next(x for x in r.read(r.PREP/'previously-scored295.json')['questions'] if x['id']==related['id']);assert historic['scoreBeforeFix']==5
r.write(b/'related295-assessment-before.json',dict(id=related['id'],historicalScorePreserved=5,currentBeforeScore=4,assessment='공통지문70 %/95 %와 선지 음성빈도 선택의 줄갈이 공백을 원문에 맞춰 복원한다. 내용·정답·5단계·5선지 근거는 새 풀이와 일치한다.',historicalEvidence=historic['evidence'],notReplacementOfHistoricalScore=True))
old[related['id']]=related
reasons={30:['정당한 이유 없이 한 피고인에게만 특실이라는 혜택을 주면 분배적 정의가 침해된다. 따라서 ㄱ은 틀리다.','3일과 9일은 모두 정해진 10일 이내다. 기간 차이만으로 절차 위반이 되지 않으므로 ㄷ만 맞다.','ㄱ의 특실 편파 제공은 분배적 침해이며, ㄴ의 보석 결정은 유죄에 대한 형벌이 아니다. 두 판단 모두 틀리다.','ㄷ은 맞지만 보석은 공판 출석 가능성을 판단하므로 범죄 가능성만으로 응보 위반을 말하는 ㄴ은 틀리다.','ㄱ은 혜택의 편파 배분을 무시하고, ㄴ은 보석을 범죄에 대한 상벌로 오인한다. ㄷ만 적절하므로 모두를 고를 수 없다.'],35:['A의 소득이 더 높고 집단주의 지표는 낮으므로 근대화 가설에 부합한다. 약화라는 ㄱ의 평가는 틀리다.','벼농사에 집중한 D가 벼농사를 하지 않은 C보다 집단주의 지표가 높다는 사실은 벼농사 가설을 지지한다. ㄷ만 맞다.','ㄱ의 높은 소득·낮은 지표는 근대화 가설과, ㄴ의 더 남쪽·높은 지표는 전염병 가설과 각각 일치하여 약화가 아니다.','ㄷ은 맞지만 더 남쪽인 C의 지표가 B보다 높다는 것은 전염병 가설의 예측과 같으므로 ㄴ은 틀리다.','ㄱ과 ㄴ은 각 가설에 맞는 관찰을 약화로 잘못 평가했다. 벼농사 유무와 지표 방향을 맞게 연결한 ㄷ만 적절하다.'],40:['A만 60마리인 1·4에서 환경 효과가 없으면 ㄱ은 맞다. 각 그물망에서 소수종이 우세한 ㄴ도 맞으므로 ㄱ만 고를 수 없다.','ㄷ은 B의 환경과 개체 비율이 동시에 바뀐 비교다. 생존율이 같아도 두 효과가 모두 없거나 상쇄될 수 있어 두 가설을 모두 강화하지 않는다.','ㄱ은 동일한 구성에서 환경 적응의 이점이 없다는 관찰이고, ㄴ은 두 환경 각각에서 소수종의 생존율이 높다는 관찰이다. 두 평가 모두 맞다.','ㄴ은 맞지만 ㄷ은 환경·비율의 효과를 분리하지 못한다. 가설 1의 예측을 약화하는 ㄱ도 빠뜨렸다.','ㄱ·ㄴ은 맞지만 B의 환경과 비율을 함께 바꾸어 생존율만 비교한 ㄷ으로는 두 가설을 모두 강화할 수 없다.']}
changes=[]
for p in (r.ROOT/'assets/psat').glob('*.json'):
 data=r.read(p)
 if not isinstance(data,list):continue
 touched=False
 for q in data:
  if q['id'] not in old or q['number'] not in fix|{39}:continue
  before=old[q['id']];assert q==before;snap=r.OUT/f"before-changes/{q['id']}-r{q['revision']}.json";assert not snap.exists();r.write(snap,before)
  if q['number']==31:q['body']=q['body'].replace('구성원 들에게','구성원들에게')
  if q['number']==35:q['body']=q['body'].replace('경제 특구','경제특구').replace('집단 주의','집단주의')
  if q['number'] in [39,40]:q['body']=q['body'].replace('70 %','70%').replace('95 %','95%').replace('그물망 3 에서는','그물망 3에서는')
  if q['number']==39:q['choices']=[s.replace('음성빈도 선택','음성빈도선택') for s in q['choices']]
  if q['number']==1:q['body']=q['body'].replace('박· 석·김','박·석·김').replace('통일 신라기','통일신라기')
  if q['number'] in reasons:q['optionReasons']=reasons[q['number']]
  assert q!=before;q['revision']+=1;touched=True
  changes.append(dict(id=q['id'],file=p.relative_to(r.ROOT).as_posix(),oldRevision=before['revision'],newRevision=q['revision'],changedFields=sorted(k for k in q if k!='revision' and q[k]!=before[k]),beforeSnapshot=snap.relative_to(r.ROOT).as_posix(),reason='Original word/percent boundaries and substantive option reasons. Source words, answer and existing five-step proof preserved.',cohort='prior295' if q['number']==39 else 'fixed605',status='repaired_pending_reverification'))
 if touched:r.write(p,data)
assert len(changes)==6;r.write(r.OUT/'changes-batch31.json',changes)
r.write(b/'sample-with-related.json',dict(sample=[dict(id=q['id']) for q in r.batch(31)]+[dict(id=related['id'])]))
print('Frozen45/50;5 target and1 prior295 repairs.')
