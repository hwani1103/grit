import review_remaining605 as r
b=r.folder(46)
rows=[(3,'다민이 재무가 아니면 가영총무와 라민인사, 가영총무에서 나영인사까지 나와 나영라민 동시인사 금지에 모순이므로 다민재무 필수다. 총무1 및 같은 수 과 하나로 인원수는1/1/3이다. 가영총무 나영인사 나머지재무의 완전 배치로 라민총무 필수라는ㄴ반례가 된다. 나영재무면 마영재무와 다민재무로 재무3명 꽉 차고 가영총무는 나영인사 강제라 불가하여 가영인사다. ㄱㄷ③.', ['다민재무는 맞지만 나영재무일 때 가영인사인ㄷ도 반드시 참이라 누락이다.','가영총무 나영인사 다민라민마영재무라는 반례에서 라민은 재무라ㄴ거짓이다.','다민재무 필수와 나영재무일 때 재무3명 포화·가영총무불가를 결합해 ㄱㄷ참이다.','ㄷ은 참이지만 라민총무를 보장하는 조건은 없어ㄴ을 포함하면 틀린다.','ㄱㄷ만 필수이고 가영총무인 가능 배치가ㄴ반례여서 세 명제 모두가 아니다.']),
(5,'㉠지칭대상=의미와㉡동일지칭이면㉢동일의미가 따라 ㄱ참. 동일지칭㉡인데 다른의미㉥면㉠이예측하는동일의미와충돌해㉠거짓이라 ㄴ참. ㄷ은 추가전제 인지차이→의미차이와㉣인지차이의 전건긍정으로㉤의미차이가 나온다. 일반적 철학주장의 진실을 외부에서 판단하는 것이 아니라 각 보기가 제공한 전제와 지문 관계를 연결한다. 세 명제 모두 참⑤이며 원래 문장 의미의 합성 전제도 보존한다.', ['ㄴ은 맞지만 동일지칭과 의미 정의로ㄱ, 추가조건의 전건긍정으로ㄷ도 맞는다.','ㄷ은 맞지만 지칭적 의미론의 예측과 그 반례인ㄱㄴ도 모두 적절하다.','ㄱㄴ은 맞지만 인지차이→의미차이 추가전제로ㄷ도 참이라 누락이다.','ㄱㄷ은 맞지만 같은 지칭·다른 의미는 지칭적 의미론의 반례여서ㄴ도 참이다.','정의 대입ㄱ, 동일 지칭·다른 의미 반례ㄴ, 조건문의 전건긍정ㄷ 모두 참이다.'])]
src=r.read(b/'related295-source.json');assert not (b/'related295-own-solves.json').exists()
r.write(b/'related295-own-solves.json',[dict(id=s['id'],answer=a,reasoning=x,optionReasons=o) for s,(a,x,o) in zip(src,rows)])
r.write(b/'related295-solve-frozen.json',dict(frozenAt=r.now(),sha256=r.sha(b/'related295-own-solves.json'),beforeKeyAndExplanationReveal=True))
bank=r.bank();r.write(b/'related295-before.json',[bank[s['id']] for s in src])
for s in src:
 q=bank[s['id']];print(q['id'],q['answer']);print(q.get('underlines'));print('\n'.join(q['steps']));print('\n'.join(q['optionReasons']))
