"""Export compact per-folder feed JSON for the lookup, plus board feed lists and an installed-in map.

Usage: python3 -I export_feeds.py <depmap-all dir> <site dir>
"""
import collections
import gzip
import json
import os
import re
import sys

base, site = sys.argv[1], sys.argv[2]
os.makedirs(os.path.join(site, 'feeds'), exist_ok=True)
SKIP = re.compile(r'-(dbg|src|staticdev|ptest|doc|locale-.+)$')


def stanzas(path):
    cur, key = {}, None
    with (gzip.open(path, 'rt', encoding='utf-8', errors='replace') if path.endswith('.gz') else open(path, encoding='utf-8', errors='replace')) as fh:
        for line in fh:
            line = line.rstrip('\n')
            if not line:
                if cur:
                    yield cur
                cur, key = {}, None
                continue
            if line[0] in ' \t' and key:
                cur[key] += '\n' + line.strip()
                continue
            k, _, v = line.partition(':')
            key = k.strip()
            cur[key] = v.strip()
    if cur:
        yield cur


def rel(field):
    groups = []
    for item in field.split(','):
        alts = [re.sub(r'\(.*?\)', '', a).strip() for a in item.split('|')]
        alts = [a for a in alts if a]
        if alts:
            groups.append('|'.join(alts))
    return ','.join(groups)


def short(desc):
    t = re.sub(r'\s+', ' ', desc.split('\n')[0]).strip()
    return t[:90] + ('…' if len(t) > 90 else '')


exact = {}
sizes_dir = os.path.join(base, 'sizes')
for f in sorted(os.listdir(sizes_dir)):
    if '__' not in f or not f.endswith('.json'):
        continue
    rel_, stem = f[:-5].split('__', 1)
    man_path = os.path.join(base, 'manifests', f'{rel_}__{stem}.rootfs.manifest')
    if not os.path.exists(man_path):
        continue
    meas = json.load(open(os.path.join(sizes_dir, f)))['pkgs']
    for line in open(man_path):
        q = line.split()
        if len(q) == 3 and q[0] in meas:
            exact[(q[0], q[1], q[2])] = meas[q[0]]
est_path = os.path.join(sizes_dir, 'feed_est.json')
feed_est = json.load(open(est_path)) if os.path.exists(est_path) else {}
quality_count = collections.Counter()

written = {}
total = 0
for famrel in sorted(os.listdir(os.path.join(base, 'feeds'))):
    d = os.path.join(base, 'feeds', famrel)
    if not os.path.isdir(d):
        continue
    fam, rel_name = famrel.split('_', 1)
    for f in sorted(os.listdir(d)):
        if not f.startswith('Packages-'):
            continue
        arch = f[len('Packages-'):].removesuffix('.gz')
        key = f'{fam}-{rel_name}-{arch}'
        rows = [s for s in stanzas(os.path.join(d, f)) if not SKIP.search(s['Package'])]
        rows.sort(key=lambda s: s['Package'])
        recipes = sorted({s.get('OE', '?') for s in rows})
        ri = {r: i for i, r in enumerate(recipes)}
        sections = sorted({s.get('Section', '?') for s in rows})
        si = {x: i for i, x in enumerate(sections)}
        data = {'key': key, 'feed': f'{fam}/{rel_name}', 'arch': arch,
                'n': [s['Package'] for s in rows], 'v': [s['Version'] for s in rows],
                'rl': recipes, 'r': [ri[s.get('OE', '?')] for s in rows],
                'sl': sections, 's': [si[s.get('Section', '?')] for s in rows],
                'sz': [], 'za': [], 'zu': [], 'd': [short(s.get('Description', '')) for s in rows],
                'dep': [rel(s.get('Depends', '')) for s in rows], 'rec': [rel(s.get('Recommends', '')) for s in rows],
                'prov': [rel(s.get('Provides', '')) for s in rows]}
        for i, s in enumerate(rows):
            t = (s['Package'], arch, s['Version'])
            if t in exact:
                data['sz'].append(exact[t]); quality_count['exact'] += 1
            elif f"{famrel}|{arch}|{s['Package']}|{s['Version']}" in feed_est:
                data['sz'].append(feed_est[f"{famrel}|{arch}|{s['Package']}|{s['Version']}"]); data['za'].append(i); quality_count['estimate'] += 1
            else:
                data['sz'].append(0); data['zu'].append(i); quality_count['unknown'] += 1
        out = os.path.join(site, 'feeds', key + '.json')
        with open(out, 'w') as fh:
            json.dump(data, fh, separators=(',', ':'), ensure_ascii=False)
        written[key] = (len(rows), os.path.getsize(out))
        total += os.path.getsize(out)

# Board feed lists and installed-in map
index = json.load(open(os.path.join(site, 'index.json')))
order = {'all': 0}
board_archs = collections.defaultdict(set)
for x in index:
    data = json.load(open(os.path.join(site, 'data', x['slug'] + '.json')))
    board_archs[(x['release'], x['machine'])].update(data['a'])
installed = collections.defaultdict(list)
slugs = [x['slug'] for x in index]
for k, x in enumerate(index):
    data = json.load(open(os.path.join(site, 'data', x['slug'] + '.json')))
    for n in data['n']:
        installed[n].append(k)
    fam, frel = x['feed'].split('/')
    archs = board_archs[(x['release'], x['machine'])]

    def rank(a, machine=x['machine']):
        return 0 if a == 'all' else 3 if a == machine else 2 if re.search(r'-mx\d', a) else 1
    keys = [f'{fam}-{frel}-{a}' for a in sorted(archs, key=lambda a: (rank(a), a))]
    x['feedFiles'] = [k2 for k2 in keys if k2 in written]
    x['feedCount'] = sum(written[k2][0] for k2 in x['feedFiles'])
with open(os.path.join(site, 'index.json'), 'w') as fh:
    json.dump(index, fh, separators=(',', ':'))
with open(os.path.join(site, 'installed.json'), 'w') as fh:
    json.dump({'slugs': slugs, 'pk': installed}, fh, separators=(',', ':'))
print('feed sizes', dict(quality_count))
print('feed files', len(written), 'total MB', round(total / 1e6, 1), 'largest', max(v[1] for v in written.values()) // 1000, 'kB')
print('installed.json kB', os.path.getsize(os.path.join(site, 'installed.json')) // 1000, 'names', len(installed))
for x in index[:3] + index[-3:]:
    print(x['slug'], x['feedFiles'], x['feedCount'])
