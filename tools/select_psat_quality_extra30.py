"""Freeze the additional 30 before reading their answers or changing questions."""
from pathlib import Path
import json, random, hashlib
R=Path(__file__).resolve().parents[1]
A=R/'artifacts/psat_quality_audit_20261029'
E=A/'extra30'
E.mkdir(exist_ok=True)
assert not (E/'sample30.json').exists()
bank=json.loads((A/'baseline-bank.json').read_text(encoding='utf-8'))
excluded={x['id'] for x in json.loads((A/'sample15.json').read_text(encoding='utf-8'))['sample']}
sets=json.loads((R/'assets/psat/sets.json').read_text(encoding='utf-8'))['sets']
files={}
for p in (R/'assets/psat').glob('*.json'):
    v=json.loads(p.read_text(encoding='utf-8'))
    if isinstance(v,list):
        for q in v: files[q['id']]=p.relative_to(R).as_posix()
rng=random.Random(2026102902)
selected=[]
for subject,stem in [('언어논리','verbal'),('상황판단','situation'),('자료해석','data')]:
    tags=set()
    for low in (1,5,9,13,17):
        used_sets=set()
        for _ in range(2):
            pool=[(s,bank[i]) for s in sets if s['subject']==subject and low<=s['order']<low+4 and s['id'] not in used_sets for i in s['questionIds'] if i not in excluded]
            fresh=[(s,q) for s,q in pool if q['tag'] not in tags]
            s,q=rng.choice(fresh or pool)
            tags.add(q['tag']);used_sets.add(s['id']);excluded.add(q['id'])
            selected.append(dict(id=q['id'],subject=subject,setId=s['id'],setOrder=s['order'],stratum=[low,low+3],tag=q['tag'],difficulty=s['difficulty'],file=files[q['id']],questionSha256=hashlib.sha256(json.dumps(q,ensure_ascii=False,sort_keys=True).encode()).hexdigest()))
    qs=[bank[x['id']] for x in selected if x['subject']==subject]
    blind=[{k:v for k,v in q.items() if k not in ('answer','steps','optionReasons','pitfall','transfer','title','tag')} for q in qs]
    (E/f'{stem}-blind.json').write_text(json.dumps(blind,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (E/f'{stem}-authored.json').write_text(json.dumps(qs,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(E/'sample30.json').write_text(json.dumps(dict(seed=2026102902,rule='2 questions from different Sets per 4-Set stratum per subject; exclude first15; prefer fresh tags; selected before answer review',sample=selected),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps([dict(id=x['id'],subject=x['subject'],set=x['setOrder']) for x in selected],ensure_ascii=False,indent=2))
