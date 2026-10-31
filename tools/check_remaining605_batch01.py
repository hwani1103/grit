"""Independent finite models and direct official-PDF comparison for review batch01."""
from pathlib import Path
from itertools import product, combinations_with_replacement
import hashlib
import json
import re
import pdfplumber

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/psat_remaining605_20261030/batch01'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
rows = read(OUT / 'revealed-current.json')
solves = {s['id']: s for s in read(OUT / 'own-solves.json')}
sources = {s['id']: s for s in read(OUT / 'blind-source.json')}
norm = lambda s: re.sub(r'[\s①②③④⑤·ㆍ․]', '', s)
checks = []
for row in rows:
    q = row['question']
    current = next(x for x in read(ROOT / next(x['file'] for x in read(ROOT / 'artifacts/psat_remaining605_20261030/preparation/targets605.json')['batches'][0]['questions'] if x['id'] == q['id'])) if x['id'] == q['id'])
    # Current source fields may have whitespace/paragraph repair; semantic text must match.
    src = sources[q['id']]['sourceText']
    src = re.sub(r'^책형\s*\d+쪽\s*', '', src)
    src = re.sub(r'^언어논리영역\s*', '', src)
    src = re.sub(r'^\d+\.\s*', '', src)
    assert norm(src) == norm(current['prompt'] + current['body'] + ''.join(current['choices'])), q['id']
    with pdfplumber.open(ROOT / row['officialKey']) as pdf:
        matches = [(i+1, p.extract_text() or '') for i, p in enumerate(pdf.pages)]
        page_number, text = next((i,t) for i,t in matches if f"영역 {q['subject']}" in t)
    assert ('2023' if q['id'].startswith('2023') else '2024') in text
    assert f"책형 {q['book']}" in text
    answers = {}
    for line in text.splitlines():
        if re.fullmatch(r'\d+ [1-5](?: \d+ [1-5])?', line):
            tokens = list(map(int, line.split()))
            answers.update(zip(tokens[::2], tokens[1::2]))
    assert len(answers) == 25
    assert answers[q['number']] == solves[q['id']]['answer'] == current['answer']
    checks.append(dict(id=q['id'], officialKey=row['officialKey'], keyPage=page_number,
                       answer=answers[q['number']], directPdfKeyMatch=True,
                       sourceTextMatchIgnoringWhitespaceAndDotStyle=True))

# All 32 course assignments, no expected answer baked into model construction.
course_models = []
for P,L,G,J,E in product([False,True], repeat=5):
    if ((not P or L) and (not G or (J and E)) and (not L or not E)):
        course_models.append(((P,L,G,J,E), (not P or not G, J or not G, not P)))
course_truth = [all(v[i] for _,v in course_models) for i in range(3)]
assert course_truth == [True,True,False]

# All attendance models on a 3-person domain; explicit false-conclusion witnesses for alternatives.
attendance = []
universe = set(range(3))
sets = [set(i for i in range(3) if mask >> i & 1) for mask in range(8)]
for M,T,W,H in product(sets, repeat=4):
    if M <= W and not T & W and W & H:
        options = [bool(universe-M),bool(universe-T),bool(W-H),bool(M-H),not bool(M&H)]
        attendance.append((dict(M=sorted(M),T=sorted(T),W=sorted(W),H=sorted(H)), options, bool(H-M)))
attendance_sufficiency = [all(goal for _,opts,goal in attendance if opts[i]) for i in range(5)]
assert attendance_sufficiency == [False,False,False,False,True]
attendance_counterexamples = [next(m for m,opts,goal in attendance if opts[i] and not goal) for i in range(4)]

# Person labels irrelevant: enumerate every multiset of locally valid policy positions.
local = [(a,b,c,d) for a,b,c,d in product([False,True],repeat=4)
         if 1<=sum((a,b,c,d))<=3 and (not a or b) and not(b and d) and (not d or c)]
policy_models = []
for people in combinations_with_replacement(local,5):
    totals = [sum(p[i] for p in people) for i in range(4)]
    if totals[0] != 2 or totals[3] != 2:
        continue
    if sum(p[1] and p[2] for p in people) != sum(p[1] and not p[2] for p in people):
        continue
    truths = [any(sum(p)==1 for p in people), totals[1]==2, totals[2]>max(totals[0],totals[1],totals[3])]
    policy_models.append(dict(people=people, totals=totals, truths=truths))
assert policy_models and all(all(m['truths']) for m in policy_models)

result = dict(status='PASS', sourceAndOfficialKeyChecks=checks,
              course=dict(validAssignments=len(course_models), necessarilyTrue=course_truth,
                          counterexampleToThird=next(m for m,v in course_models if not v[2])),
              attendance=dict(validModels=len(attendance), sufficientOptions=attendance_sufficiency,
                              counterexamplesToFirstFour=attendance_counterexamples),
              policies=dict(localPositions=len(local), validUnlabelledModels=len(policy_models), models=policy_models),
              totalVsIndividual=dict(A=[10],B=[1]*11,individualDominance='A',totalDominance='B'),
              limitations='Finite models verify selected formal claims; textual semantic/visual review remains separate.')
(OUT/'source-key-model-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PASS:10 direct official-PDF keys/source texts; course32, attendance4096, exhaustive unlabelled5-person policies.')
