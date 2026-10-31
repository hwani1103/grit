"""Freeze a stratified audit sample before judging question quality."""
from pathlib import Path
import random, json, hashlib

R = Path(__file__).resolve().parents[1]
A = R / 'artifacts/psat_quality_audit_20261029'
A.mkdir(exist_ok=True)
assert not (A/'sample15.json').exists(), 'Frozen sample must not be replaced'
bank = {}
files = {}
for path in sorted((R/'assets/psat').glob('*.json')):
    value = json.loads(path.read_text(encoding='utf-8'))
    if isinstance(value, list):
        for q in value:
            bank[q['id']] = q
            files[q['id']] = path.relative_to(R).as_posix()
sets = json.loads((R/'assets/psat/sets.json').read_text(encoding='utf-8'))['sets']
rng = random.Random(2026102901)
selected = []
for subject in ('언어논리','상황판단','자료해석'):
    tags = set()
    for low in (1,5,9,13,17):
        pool = [(s,bank[i]) for s in sets if s['subject']==subject and low<=s['order']<low+4 for i in s['questionIds']]
        fresh = [(s,q) for s,q in pool if q['tag'] not in tags]
        s,q = rng.choice(fresh or pool)
        tags.add(q['tag'])
        selected.append(dict(id=q['id'],subject=subject,setId=s['id'],setOrder=s['order'],
                             stratum=[low,low+3],tag=q['tag'],difficulty=s['difficulty'],
                             file=files[q['id']],questionSha256=hashlib.sha256(json.dumps(q,ensure_ascii=False,sort_keys=True).encode()).hexdigest()))
manifest = dict(seed=2026102901,rule='Each subject: one random question from each Set range 1-4/5-8/9-12/13-16/17-20; prefer previously unselected tag within stratum; no answer or quality criterion used',sample=selected)
(A/'sample15.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(A/'baseline-bank.json').write_text(json.dumps(bank,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for subject,stem in [('언어논리','verbal'),('상황판단','situation'),('자료해석','data')]:
    qs=[bank[x['id']] for x in selected if x['subject']==subject]
    blind=[{k:v for k,v in q.items() if k not in ('answer','steps','optionReasons','pitfall','transfer')} for q in qs]
    (A/f'{stem}-blind.json').write_text(json.dumps(blind,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (A/f'{stem}-authored.json').write_text(json.dumps(qs,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(manifest,ensure_ascii=False,indent=2))
