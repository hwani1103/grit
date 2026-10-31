"""Preserve original questions while allowing the explicitly reviewed explanation revision."""
import hashlib
import json

EXPLANATION_KEYS = {'steps', 'optionReasons', 'pitfall', 'transfer', 'revision'}

def verify_legacy_assets(root, expected_hashes):
    unchanged, revised = 0, []
    for relative, expected in expected_hashes.items():
        source = root / relative
        if hashlib.sha256(source.read_bytes()).hexdigest() == expected.lower():
            unchanged += 1
            continue
        assert relative.replace('\\', '/') in {
            'assets/psat/batch01.json', 'assets/psat/data01.json'
        }, ('unapproved original asset change', relative)
        baseline = root / 'artifacts/psat_explanations_20261028/before' / source.name
        assert hashlib.sha256(baseline.read_bytes()).hexdigest() == expected.lower(), relative
        old = json.loads(baseline.read_text(encoding='utf-8'))
        new = json.loads(source.read_text(encoding='utf-8'))
        assert len(old) == len(new), relative
        for before, after in zip(old, new):
            protected = lambda q: {k:v for k,v in q.items() if k not in EXPLANATION_KEYS}
            assert protected(before) == protected(after), before['id']
            assert after['revision'] == before['revision'] + 1, before['id']
            assert len(after['steps']) == 5 and len(after['optionReasons']) == 5
        revised.append(relative)
    return {'unchangedFiles': unchanged, 'explanationOnlyFiles': revised,
            'originalQuestionFieldsPreserved': True}
