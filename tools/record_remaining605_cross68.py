import review_remaining605 as r
b=r.folder(68);assert not (b/'own-solves.json').exists();src=r.read(b/'source.json');models=r.read(b/'source-enumerations.json')
rows=[
(4,'성묘70+10−10=70,서울85−10−10=65,만날75(50명은미만아님),빅65+10=75.75이상만날·빅④.',['성묘70제외.','성묘70제외.','서울65제외.','만날75빅75.','서울65제외.']),
(3,'원문상황의256은평문추출오류:실제2의56제곱.2^60/2^56=2^4이므로4회속도배증,100만원+4×10만원=140만원③.',['1회배증부족.','2회배증부족.','4회배증이최소.','6회는필요초과.','10회는필요초과.']),
(5,'Q100에A200/B100필요.A200을위해X200,Y400필요하여1000만원.B100에는원료200필요하며Z4보다W3이싸고단독가능하므로W200으로600만원.합1600⑤.',['A1000+B600미달.','A1000+B600미달.','A1000+B600미달.','A1000+B600미달.','단독W가능하며수율절반까지반영1600.']),
(5,'향종별종료범위甲17~18,乙Parfum17:30~19:30,丙EDP16~19,丁EDT17~19,戊EDP20~23시.戊의최소20시가타인최대19:30보다늦으므로⑤.',['최대18시.','최대19:30.','최대19시.','최대19시.','최소20시로모든경우가장늦음.']),
(3,'총59000원;500원단위9a+11b=118.0≤b≤10에서mod9로2b≡1이므로b5,a7유일.추가금0가능하며총12장③.',['정확교환유일12장.','정확교환유일12장.','4500원7장5500원5장.','13장보다추가금최소를우선.','정확교환유일12장.']),
(3,'중앙기관결과제출3월말,보완요청대상중앙행정기관.지자체소속기관포함평가의무,위원민간≥2/3,계획매년.9×2/3=6명이상③.',['4월말은계획이며결과3월말.','지자체에대한권한근거없음.','9명중민간6명이상.','소속기관포함의무.','격년아닌매년.']),
(4,'공무원c,전문가e,관리m:2c+e+2m≤30,e≤10m.전수정수검산최대1240건은c3,e20,m2유일,총25명④.관리비없이전문가만30명으로세면안됨.',['15공무원은1200건.','17명은최적구성아님.','전문가20명만세면공무원3관리2누락.','3+20+2=25.','전문가24관리3은1200건으로최대아님.']),
(3,'해저광업권국가전용,조광권법인전용.탐사권은연장포함10년상한,채취권은30+5×2=40년상한.설정출원산업통상장관,탐사협의재정경제외교;채취에는해양수산추가.③.',['법인광업권불가.','탐사는연장포함10년.','채취최대40년.','출원산업통상장관.','탐사협의에는해양수산없음.']),
(3,'丁건수35<40,戊만족75<80으로제외.남은甲68+10−1−3=74,乙64+8+3=75,丙68+8+1−1=76으로丙③.',['甲74<76.','乙75<76.','丙76최대.','건수35자격미달.','만족75자격미달.']),
(1,'수요일0과목요일아침금지,금요일저녁금지및다음날제약을모두적용.비트(아침1점심2저녁4)전수검산최대12.월3화7수0목2금3토3일3패턴은2+3+0+1+2+2+2=12,일→월조건도충족.①.',['12가능하고상한.','13불가.','14불가.','15불가.','16불가.'])]
assert models['dogWeeklyMaximum']==12 and models['monitorMaximum']==1240 and models['ticketSolutions']==[[7,5]]
# Wednesday resets the next-day constraints, so no fixed daily weekly pattern is assumed for the upper bound.
import itertools
def ok(a,b):return not ((a==7 and b&3) or (a&6==6 and b&1) or (a==0 and b&1))
max_reset=max(sum(d.bit_count() for d in ds) for ds in itertools.product([0],range(8),range(4),range(8),range(8),range(8),range(8)) if all(ok(a,z) for a,z in zip(ds,ds[1:])))
assert max_reset==12
r.write(b/'own-source-models.json',dict(**models,resetWindowMaximum=max_reset,resetWindowOrder='Wednesday through Tuesday',upperBoundDoesNotRequireFixedDailySchedule=True,investmentScores=[70,65,75,75],complaintEligibleScores=[74,75,76],perfumeEndRanges=[[17,18],[17.5,19.5],[16,19],[17,19],[20,23]],sourceExponent='2^56 visually verified, text extraction256 must not be used'))
r.write(b/'own-solves.json',[dict(id=s['id'],answer=a,reasoning=t,optionReasons=o) for s,(a,t,o) in zip(src,rows)])
r.write(b/'solve-frozen.json',dict(frozenAt=r.now(),sha256=r.sha(b/'own-solves.json'),scope='Ten prior295 source re-solves before current comparison; same author.'))
for q,(a,_,__) in zip(r.read(b/'before.json'),rows):
 print(q['id'],'own',a,'current',q['answer']);print('BODY',q['body']);print('\n'.join(q['steps']));print('\n'.join(q['optionReasons']));print('FIGURES',[(j,f['asset']) for j,f in enumerate(q.get('figures',[]))])
