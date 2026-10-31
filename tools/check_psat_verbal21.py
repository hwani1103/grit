from psat_batch_tools import validate,read,ROOT
from itertools import product
from fractions import Fraction as F
from pathlib import Path
import re,hashlib,pdfplumber
A=ROOT/'artifacts/psat600_20261028/verbal21'
own=read(A/'own-solve-before-key.json');bank=read(A/'authored-verbal21.json')
assert len(bank)==10 and [q['answer'] for q in bank]==[own[str(q['number'])]['answer'] for q in bank]
imp=lambda a,b:not a or b
# Test the proposed missing premise against every truth assignment, not just the intended conclusion.
models=[]
for i in range(5):
    worlds=[]
    for a,b,t in product([False,True],repeat=3):
        premises=[imp(not b,not a),imp(t,b),imp(not t,a),imp(b,not t),imp(not a,not t)]
        if a==b and t and premises[i]:worlds.append((a,b,t))
    models.append(dict(option=i+1,worlds=worlds,entailsNotB=bool(worlds) and all(not b for a,b,t in worlds)))
assert [m['entailsNotB'] for m in models]==[False,False,False,True,False]
# Positive finite resistance is a genuine boundary: r=0 would destroy the strict inequality.
for base in range(1,101):
    for r in [F(base,4),F(base,2),F(3*base,4)]:
        sa=(2*base-r)/(2*base);sb=(base-r)/base
        assert sa-sb==r/(2*base)>0
q16=next(q for q in bank if q['number']==16)
assert [i+1 for i,c in enumerate(q16['choices']) if 'ㄱ' in c and 'ㄴ' not in c]==[4]
# Only stated interactions are added; sets represent observed kinds, not intensity.
def spectrum(a,b,extra=()):return sorted(set(a)|set(b)|set(extra))
assert spectrum([1,2],[3])==[1,2,3] and spectrum([1,2],[2])==[1,2]
assert spectrum([2],[3])==[2,3]
assert spectrum([1,2],[3],[3])==[1,2,3]
assert spectrum([1,2],[2],[3])!=[1,2]
for high in range(2,20):
    for low in range(1,high):
        assert (high+1)-low>high-low and high-(low-1)>high-low
assert 21835*2<43929 and 76782*2<189153 and 43929-21835==22094 and 189153-76782==112371
assert 25+3==28
for n,truth in [(15,[True,False,False]),(16,[True,False,True]),(17,[True,False,True]),(18,[False,True,False])]:
    q=next(q for q in bank if q['number']==n)
    expected={label for label,yes in zip('ㄱㄴㄷ',truth) if yes}
    assert [i+1 for i,c in enumerate(q['choices']) if {x for x in 'ㄱㄴㄷ' if x in c}==expected]==[q['answer']]
q12=bank[0];assert q12['body'].count('aⁿ＋bⁿ＝cⁿ')==2 and q12['body'].count('[빈칸]')==1
assert 'SnO₂' in q16['body'] and len(q16['underlines'])==2
q17=next(q for q in bank if q['number']==17);assert len(q17['underlines'])==1
q19,q20=[next(q for q in bank if q['number']==n) for n in (19,20)]
assert q19['body']==q20['body'] and q19['body'].count('[빈칸]')==2
assert '[kɔ́ːfi]' in q19['body'] and '[píːtsə]' in q20['choices'][2]
proof=dict(missingPremiseTruthTable=models,sensitivity='For all R>0 and 0<r<R, MA-MB=r/(2R)>0; r=0 excluded by finite maximum conductivity.',
    combinationStops={'16':'ㄱ true and ㄴ false leave only option4 in the actual choices'},
    spectroscopy={'initialAB':[1,2,3],'initialAC':[1,2],'case1AB':[2,3],'case2AB':[1,2,3],'case3AC':[1,2,3]},
    mice='Initial I>II; increase I or decrease II increases the gap; both hypotheses predict increased K.',
    semanticReview={str(q['number']):own[str(q['number'])]['proof'] for q in bank},
    difficultyReview={str(q['number']):[q['difficulty'],q['difficultyReason']] for q in bank},
    sourceVisualReview='All selected columns and the common 19/20 page examined; source underlines, exponent, subscript and phonetic glyphs retained.',
    officialKeySourceSha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'artifacts/psat600_20261028/sources/4684').glob('*.pdf')})
validate('verbal21',proof,[('2025-03-08',n) for n in [12,15,16,17,18,19,20,21,22,23]])
