#!/usr/bin/env python3
"""Raknar riktvarden for varje matt i matt.py pa forebilderna.
Grupper: sabb (6 artiklar), topp (2 artiklar lasta i sin helhet),
vinn19 (12 vinnare 2019-2025), ej19 (ovriga uppsatser 2019-2025)."""
import json, os, re, sys, glob
import numpy as np
from scipy import stats
sys.path.insert(0, os.path.dirname(__file__))
import matt

REPO = '/home/claude/uvangludvig-ship-it/financethesisv2/reference'
rows = []

def add(grp, name, raw, year=None):
    t = matt.prosa(raw)
    if matt.ord_antal(t) < (1200 if grp in ('sabb','topp') else 2500):
        return
    r = {'grp': grp, 'id': name, 'year': year}
    r.update(matt.takter(t)); r.update(matt.dokmatt(raw if grp in ('sabb', 'topp') else raw))
    rows.append(r)

for f in sorted(glob.glob('/home/claude/raw/*.txt')):
    add('sabb', os.path.basename(f)[:12], open(f, errors='ignore').read())
for f in sorted(glob.glob('/home/claude/top/*.md')):
    add('topp', os.path.basename(f), open(f, errors='ignore').read())
for f in sorted(glob.glob(REPO + '/old_winners/text/*.txt')):
    y = int(os.path.basename(f)[:4])
    add('vinn', os.path.basename(f)[:-4], open(f, errors='ignore').read(), y)
cat = json.load(open(REPO + '/non_winners/catalogue_index.json'))['records']
ymap = {}
for r in cat:
    mid = r.get('mediumid') or r.get('MediumId') or r.get('medium_id')
    if mid is not None:
        try: ymap[str(mid)] = int(str(r.get('year'))[:4])
        except Exception: pass
for f in sorted(glob.glob(REPO + '/non_winners/text/*.txt')):
    mid = os.path.basename(f)[:-4]
    y = ymap.get(mid)
    grp = 'vinn' if mid == '6338' else 'ej'
    add(grp, mid, open(f, errors='ignore').read(), y)

json.dump(rows, open('/home/claude/matt/alla_matt.json', 'w'))
G = {
 'sabb': [r for r in rows if r['grp'] == 'sabb'],
 'topp': [r for r in rows if r['grp'] == 'topp'],
 'vinn19': [r for r in rows if r['grp'] == 'vinn' and r['year'] and r['year'] >= 2019],
 'ej19': [r for r in rows if r['grp'] == 'ej' and r['year'] and r['year'] >= 2019],
 'vinn_alla': [r for r in rows if r['grp'] == 'vinn'],
 'ej_alla': [r for r in rows if r['grp'] == 'ej'],
}
print({k: len(v) for k, v in G.items()})
keys = [k for k in rows[0] if k not in ('grp', 'id', 'year')]
out = {'n': {k: len(v) for k, v in G.items()}, 'matt': {}}
for k in keys:
    e = {}
    for g, rs in G.items():
        v = [r[k] for r in rs if r.get(k) is not None]
        if not v: continue
        v = np.array(v, float)
        e[g] = {'median': float(np.median(v)), 'p25': float(np.percentile(v, 25)), 'p75': float(np.percentile(v, 75)),
                'min': float(v.min()), 'max': float(v.max()), 'medel': float(v.mean()), 'n': int(len(v))}
    a = np.array([r[k] for r in G['vinn19'] if r.get(k) is not None], float)
    b = np.array([r[k] for r in G['ej19'] if r.get(k) is not None], float)
    if k.startswith('D') and set(np.unique(np.concatenate([a, b]))) <= {0.0, 1.0}:
        tab = [[int(a.sum()), int(len(a) - a.sum())], [int(b.sum()), int(len(b) - b.sum())]]
        e['test'] = {'typ': 'fisher', 'p': float(stats.fisher_exact(tab)[1])}
    elif len(a) > 2 and len(b) > 2:
        e['test'] = {'typ': 'mannwhitney', 'p': float(stats.mannwhitneyu(a, b, alternative='two-sided')[1])}
    out['matt'][k] = e
FEL = ['R02', 'R03', 'R04', 'R05', 'R06', 'R08', 'R10', 'R11', 'R14', 'R15']
e = {}
for g, rs in G.items():
    v = np.array([sum(r[k] for k in FEL) for r in rs])
    e[g] = {'median': float(np.median(v)), 'p25': float(np.percentile(v, 25)), 'p75': float(np.percentile(v, 75)), 'min': float(v.min()), 'max': float(v.max()), 'medel': float(v.mean()), 'n': int(len(v))}
e['test'] = {'typ': 'mannwhitney', 'p': float(stats.mannwhitneyu([sum(r[k] for k in FEL) for r in G['vinn19']], [sum(r[k] for k in FEL) for r in G['ej19']])[1])}
art = [sum(r[k] for k in FEL) for r in G['sabb'] + G['topp']]; ups = [sum(r[k] for k in FEL) for r in G['vinn19'] + G['ej19']]
e['test_artiklar_mot_uppsatser'] = {'typ': 'mannwhitney', 'p': float(stats.mannwhitneyu(art, ups)[1]), 'n': [len(art), len(ups)]}
out['matt']['FELSUMMA'] = e; out['felsumma_regler'] = FEL
keys = keys + ['FELSUMMA']
for path in ('/home/claude/matt/riktvarden.json', '/home/claude/scripts/riktvarden.json'):
    json.dump(out, open(path, 'w'), indent=1)

def f(x): return '   .' if x is None else f'{x:6.2f}'
print(f"{'matt':34s} {'sabb med':>8s} {'sabb min-max':>14s} {'topp':>7s} {'vinn19':>7s} {'(p25-p75)':>14s} {'ej19':>7s} {'p':>6s}")
for k in keys:
    e = out['matt'][k]
    s = e.get('sabb'); t = e.get('topp'); w = e.get('vinn19'); n = e.get('ej19')
    stat = 'medel' if k.startswith('D') else 'median'
    if k == 'FELSUMMA': print('artiklar mot uppsatser', e['test_artiklar_mot_uppsatser'])
    print(f"{k:34s} {f(s and s[stat])} {f(s and s['min'])}-{f(s and s['max'])} {f(t and t[stat])} {f(w and w[stat])} {f(w and w['p25'])}-{f(w and w['p75'])} {f(n and n[stat])} {e.get('test',{}).get('p',float('nan')):6.3f}")
