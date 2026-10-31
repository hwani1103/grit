"""2026-10-28: actual 50-question explanation revision, exact shortcut checks and official keys.
This is self-review evidence; prose semantics and rendered UI require separate review.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import hashlib, json, re
import pdfplumber
R=Path(__file__).resolve().parents[1]
A=R/'artifacts/psat_explanations_20261028'
FILES=['batch01.json','data01.json','verbal02.json','situation02.json']
allowed={'steps','transfer','revision'}
bank={}
for name in FILES:
    before=json.loads((A/'before'/name).read_text(encoding='utf-8'))
    after=json.loads((R/'assets/psat'/name).read_text(encoding='utf-8'))
    assert len(before)==len(after)
    for old,q in zip(before,after):
        assert {k:v for k,v in old.items() if k not in allowed}=={k:v for k,v in q.items() if k not in allowed},q['id']
        assert q['revision']==old['revision']+1
        assert len(q['steps'])==5
        for text,prefix in zip(q['steps'],['착안점: ','실전 풀이: ','답 확정 기준: ','정석 근거: ','적용 한계: ']):
            assert text.startswith(prefix) and len(text)>30
            assert not any(c in text for c in ['\u2060','\ufffd'])
        assert all(s in q['steps'][3] for s in old['steps']),q['id']
        assert q['id'] not in bank
        bank[q['id']]=q
assert len(bank)==50
hashes=json.loads((A/'before-hashes.json').read_text(encoding='utf-8-sig'))
preserved=0
for path,digest in hashes.items():
    if path in ['assets/psat/'+f for f in FILES]:continue
    assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
    preserved+=1
# Read the final key itself, with year, subject and book checks.
keys={}
for year,path,subjects,book in [
    (2023,R/'artifacts/psat_batch01_20261028/sources/4342_e8e66da6cb48.pdf',['언어논리','자료해석','상황판단'],'인'),
    (2024,R/'artifacts/psat600_20261028/sources/4564/BBSMSTR_000000000138_4564_1.pdf',['언어논리','상황판단','자료해석'],'사')
]:
    with pdfplumber.open(path) as pdf:
        for p,subject in zip(pdf.pages,subjects):
            text=p.extract_text()
            assert str(year)+'년도' in text and subject in text
            assert book+'책형' in re.sub(r'\s+','',text)
            answers={}
            for line in text.splitlines():
                if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?',line):
                    parts=list(map(int,line.split()))
                    answers.update(zip(parts[::2],parts[1::2]))
            assert len(answers)==25
            keys[(year,subject)]=answers
for q in bank.values():
    year=2023 if q['id'].startswith('2023-') else 2024
    assert q['answer']==keys[(year,q['subject'])][q['number']],q['id']
# Selection stopping rules actually leave exactly one printed option.
partial={
 '2023-07-22-l-08':{'ㄱ':False,'ㄷ':False},
 '2023-07-22-l-11':{'ㄴ':False,'ㄷ':False},
 '2023-07-22-l-12':{'ㄱ':False,'ㄷ':True},
 '2023-07-22-l-14':{'ㄴ':True,'ㄷ':False},
 '2023-07-22-d-09':{'ㄴ':False,'ㄹ':False},
 '2023-07-22-d-14':{'ㄴ':True,'ㄹ':False},
 '2023-07-22-d-17':{'ㄱ':False,'ㄷ':False},
 '2023-07-22-d-19':{'ㄴ':False,'ㄷ':False},
 'kr-mpm-2024-07-27-psat-s-09':{'ㄱ':True,'ㄴ':False}
}
for ident,facts in partial.items():
    q=bank[ident]
    remaining=[i for i,c in enumerate(q['choices'],1) if all((k in c)==v for k,v in facts.items())]
    assert remaining==[q['answer']],(ident,remaining)
# Independent exact checks of the NEW reduced calculations (not only final answer constants).
proofs={}
def record(name,value):proofs[name]=value
assert F(4)*F(3,4)*F(1,2)==F(3,2)
assert [x for x in range(1,20) if 15-2*x>=10]==[1,2]
assert [15-3*2,15-2*2,10-3*2,5,5-3*2]==[9,11,4,5,-1]
assert 20*25*2==1000 and max(d for d in range(1,25) if 1000%d==0)==20
record('component_remainder_and_integer_bounds','exact')
# d03: no full-total divisions for losing candidates.
crop={'콩':(2593,105340,246117),'건고추':(2483,78437,86097),'땅콩':(2260,8219,26146),'참깨':(2024,12986,76812),'팥':(2020,7102,42418)}
assert sum(crop['땅콩'])==36625 and F(2260,36625)>F(1,20)
for name in ['참깨','팥']:assert crop[name][0]<2260 and crop[name][2]>36625
for name in ['콩','건고추']:assert crop[name][0]<2600 and crop[name][2]>52000 and F(crop[name][0],sum(crop[name]))<F(1,20)
record('d03_threshold','peanut > 5%; bean/chili < 5%; remaining two dominated')
# d04 weighted differences.
assert 90>60 and 50>45
assert 2*(50-90)+3*(80-50)==10
assert 2*(180-80)+3*(0-60)==20
assert 2*(180-100)+3*(0-40)==40
record('d04_weighted_differences',[10,20,40])
assert F('.20')>2*F('.07') and F('4.97')<2*F('2.85')
assert F('.20')/F('4.97')>F('.07')/F('2.85')
record('d06_double_comparison','ratio A > ratio B without division')
assert F(100,150)<F(100,100)
assert -150+150+12==12 and 300-150-54==96 and -150+150+15==15
record('d11_cost_differences',[12,96,15])
patents=[[3,25],[1,3,20],[3,2,10,5,6],[12,21,15],[6,56,4,12]]
assert [sum(v) for v in patents]==[28,24,26,48,78]
assert [F(sum(v),len(v)) for v in patents]==[14,8,F(26,5),16,F(39,2)]
assert 32235+38976+7718+1636==80565
assert 58451-32627-20840-3497==1487
assert 1487-1240==247 and 32627-28522==4105
assert 247*6>1240 and 4105*6<28522
record('d14_one_sixth_threshold','oak > 1/6 > moth')
assert F(1800,5200)<F(660,1320)==F(1,2)
assert 55058-sum([2930,33008,9520,350,240])==9010
assert 9010*5<55058
assert 33008+32594-55058==10544
assert F(10544,10)>1000
record('d17_threshold_and_overlap',{'land':9010,'overlapLowerBound':10544})
assert 13899<3*4722 and 16652>3*5197
assert 684>502 and 684*40<30706 and 502*40>16652
assert sum([195,502,320,684])==1701 and 1701*4<8010
assert 8010>60*133 and 320<20*17
record('d19_three_safe_thresholds',{'GDPperPerson':3,'defenseShare':'1/40','militaryPerPerson':[60,20]})
# s06: prove decimal digit-sum property by coefficients, then enumerate only actual blank digits.
assert all((10**p-1)%9==0 for p in range(5))
visible=[5701,84098,83004,6715]
assert sum(sum(map(int,str(x))) for x in visible)==76
assert sum(map(int,str(199998)))==45
assert [x for x in range(13,18) if (76+x-45)%9==0]==[14]
solutions=[(a,b,c,d,e) for a,b,c,d,e in product(range(10),repeat=5)
 if 10000*a+5701+84098+100*b+83004+100*c+10*d+10000*e+6715==199998]
assert len(solutions)==15 and {sum(v) for v in solutions}=={14}
assert 15701+84098+83484+16715==199998
record('2024_s06_mod9',{'solutions':len(solutions),'uniqueSum':14,'singleOptionAfterResidue':14})
triples=[v for v in product(range(4),range(3),range(3)) if sum(v)==3 and sum(x>0 for x in v)>=2 and sum(x*w for x,w in zip(v,[30,40,50]))<=100]
assert triples==[(2,1,0)]
assert 2**59<2**60 and 2**56*2**4==2**60
assert 1000000+(60-56)*100000==1400000
record('2024_s07_forced_triple',triples)
record('2024_s10_minimum',1400000)
report={'status':'PASS','questionsRevised':50,'officialFinalKeysReadAndMatched':50,'optionReasonsPreserved':250,
'nonExplanationFieldsPreserved':True,'unchangedPreexistingAssetsCodeTests':preserved,
'combinationStoppingRulesChecked':len(partial),'exactShortcutProofs':proofs,
'limits':'Automated exact checks plus same-author prose review; not independent expert review or real-device approval.'}
(A/'revision-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
