"""Build one dependency-graph JSON per image manifest, plus an index.

Usage: python3 -I build_all.py <depmap-all dir> <out dir>
"""
import collections
import gzip
import json
import os
import re
import sys

base, outdir = sys.argv[1], sys.argv[2]
os.makedirs(os.path.join(outdir, 'data'), exist_ok=True)


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


feeds = {}  # "linux-imx_scarthgap" -> {(name, arch): stanza}


# Installed sizes: exact per (name, arch, version) from rootfs dpkg lists, plus xz estimates for the rest
exact, by_na = {}, {}
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
            by_na[(q[0], q[1])] = meas[q[0]]
est_path = os.path.join(sizes_dir, 'feed_est.json')
feed_est = json.load(open(est_path)) if os.path.exists(est_path) else {}
print('exact sizes', len(exact), 'feed estimates', len(feed_est), flush=True)


def installed_size(n, a, v, famrel, stanza, twin=None):
    """Return (bytes, quality) where quality 0 = exact, 1 = estimate, 2 = unknown."""
    if (n, a, v) in exact:
        return exact[(n, a, v)], 0
    if twin and stanza and (twin, a, stanza['Version']) in exact:
        return exact[(twin, a, stanza['Version'])], 1
    if (n, a) in by_na:
        return by_na[(n, a)], 1
    if twin and (twin, a) in by_na:
        return by_na[(twin, a)], 1
    for name, ver in ((n, v), (n, stanza and stanza.get('Version')), (twin, stanza and stanza.get('Version'))):
        if name and ver and f'{famrel}|{a}|{name}|{ver}' in feed_est:
            return feed_est[f'{famrel}|{a}|{name}|{ver}'], 1
    return 0, 2


def feed(fam_rel):
    if fam_rel not in feeds:
        d = os.path.join(base, 'feeds', fam_rel)
        table = {}
        for f in sorted(os.listdir(d)):
            if not f.startswith('Packages-'):
                continue
            folder_arch = f[len('Packages-'):].removesuffix('.gz').removesuffix('.gz')
            for s in stanzas(os.path.join(d, f)):
                pa = s.get('PackageArch', folder_arch).replace('_', '-')
                table[(s['Package'], pa)] = s
        feeds[fam_rel] = table
    return feeds[fam_rel]


def buildinfo(release, machine):
    p = os.path.join(base, 'buildinfo', f'{release}__{machine}.txt')
    info = {}
    if os.path.exists(p):
        for line in open(p, encoding='utf-8', errors='replace'):
            k, _, v = line.partition(':')
            if k.strip() in ('project', 'build-id', 'cycle', 'built', 'manifest'):
                info[k.strip()] = v.strip()
    m = re.search(r'-m (\S+?)\.xml', info.get('manifest', ''))
    info['bsp'] = m.group(1) if m else ''
    return info


def parse_rel(field, prov):
    res = []
    for item in field.split(','):
        item = item.strip()
        if not item:
            continue
        for alt in item.split('|'):
            a = re.sub(r'\(.*?\)', '', alt).strip()
            if a in prov:
                res.extend(sorted(prov[a]))
                break
    return res


def sccs(n, succ):
    """Iterative Tarjan. Returns comp id per node; comps are numbered in reverse topological order."""
    index = [-1] * n
    low = [0] * n
    on = [False] * n
    comp = [-1] * n
    stack, counter, ncomp = [], 0, 0
    for s in range(n):
        if index[s] != -1:
            continue
        work = [(s, 0)]
        while work:
            v, pi = work.pop()
            if pi == 0:
                index[v] = low[v] = counter
                counter += 1
                stack.append(v)
                on[v] = True
            recurse = False
            for k in range(pi, len(succ[v])):
                w = succ[v][k]
                if index[w] == -1:
                    work.append((v, k + 1))
                    work.append((w, 0))
                    recurse = True
                    break
                if on[w]:
                    low[v] = min(low[v], index[w])
            if recurse:
                continue
            if low[v] == index[v]:
                while True:
                    w = stack.pop()
                    on[w] = False
                    comp[w] = ncomp
                    if w == v:
                        break
                ncomp += 1
            if work:
                u = work[-1][0]
                low[u] = min(low[u], low[v])
    return comp, ncomp


def closure_counts(n, succ):
    comp, nc = sccs(n, succ)
    members = [0] * nc
    for v in range(n):
        members[comp[v]] |= 1 << v
    csucc = [set() for _ in range(nc)]
    for v in range(n):
        for w in succ[v]:
            if comp[w] != comp[v]:
                csucc[comp[v]].add(comp[w])
    reach = [0] * nc
    for c in range(nc):  # reverse topological: successors already done
        r = members[c]
        for d in csucc[c]:
            r |= reach[d]
        reach[c] = r
    return [reach[comp[v]].bit_count() - 1 for v in range(n)]


def dominators(n, roots, succ):
    ROOT = n
    allsucc = succ + [list(roots)]
    order, seen = [], [False] * (n + 1)
    stack = [(ROOT, iter(allsucc[ROOT]))]
    seen[ROOT] = True
    while stack:
        v, it = stack[-1]
        for w in it:
            if not seen[w]:
                seen[w] = True
                stack.append((w, iter(allsucc[w])))
                break
        else:
            order.append(v)
            stack.pop()
    po = {v: i for i, v in enumerate(order)}
    preds = collections.defaultdict(list)
    for u in range(n + 1):
        for w in allsucc[u]:
            preds[w].append(u)
    idom = {ROOT: ROOT}

    def intersect(a, b):
        while a != b:
            while po[a] < po[b]:
                a = idom[a]
            while po[b] < po[a]:
                b = idom[b]
        return a
    changed = True
    rpo = list(reversed(order))
    while changed:
        changed = False
        for v in rpo[1:]:
            ps = [p for p in preds[v] if p in idom]
            new = ps[0]
            for p in ps[1:]:
                new = intersect(p, new)
            if idom.get(v) != new:
                idom[v] = new
                changed = True
    return idom, order


def build(release, machine, fname, date):
    fam = 'openstlinux' if machine.startswith('stm32mp') else 'linux-imx'
    feed_rel = 'wrynose' if release == 'wrynose-rt' else release
    table = feed(f'{fam}_{feed_rel}')
    man = [l.split() for l in open(os.path.join(base, 'manifests', f'{release}__{fname}')) if l.strip()]
    image = fname.replace('.rootfs.manifest', '').replace('-' + machine, '')
    names = sorted({m[0] for m in man})
    arch_of = {m[0]: m[1] for m in man}
    ver_of = {m[0]: m[2] for m in man}
    st, exact, newer, missing, inferred = {}, 0, 0, 0, set()
    # Kernel packages carry the kernel release string in their names. When the image was built
    # with a different kernel than the current feed, map each missing kernel package to its
    # counterpart in the feed and swap the release string back in.
    kre = re.compile(r'^kernel-(\d+\.\d+\.\d+\S*)$')
    k_img = next((kre.match(n).group(1) for n in names if kre.match(n) and arch_of[n] == machine), None)
    k_feed = next((kre.match(k[0]).group(1) for k in table if k[1] == machine and kre.match(k[0])), None)
    for nme in names:
        s = table.get((nme, arch_of[nme]))
        if s is None and k_img and k_feed and k_img != k_feed and k_img in nme:
            twin = table.get((nme.replace(k_img, k_feed), arch_of[nme]))
            if twin is not None:
                s = {k: (v.replace(k_feed, k_img) if k in ('Package', 'Depends', 'Recommends', 'Provides') else v) for k, v in twin.items()}
                inferred.add(nme)
        if s is not None and nme not in inferred and k_img and k_feed and k_img != k_feed and any(k_feed in s.get(f, '') for f in ('Depends', 'Recommends')):
            s = {k: (v.replace(k_feed, k_img) if k in ('Depends', 'Recommends') else v) for k, v in s.items()}
        if s is None:
            missing += 1
            st[nme] = None
        else:
            st[nme] = s
            if nme in inferred:
                pass
            elif s['Version'] == ver_of[nme]:
                exact += 1
            else:
                newer += 1
    idx = {n: i for i, n in enumerate(names)}
    N = len(names)
    prov = collections.defaultdict(set)
    for nme in names:
        prov[nme].add(nme)
        s = st[nme]
        if s:
            for p in s.get('Provides', '').split(','):
                p = re.sub(r'\(.*?\)', '', p).strip()
                if p:
                    prov[p].add(nme)
    dep, rec = [], []
    for nme in names:
        s = st[nme] or {}
        d = sorted({idx[m] for m in parse_rel(s.get('Depends', ''), prov)} - {idx[nme]})
        r = sorted({idx[m] for m in parse_rel(s.get('Recommends', ''), prov)} - {idx[nme]} - set(d))
        dep.append(d)
        rec.append(r)
    succ = [dep[i] + rec[i] for i in range(N)]
    indeg = [0] * N
    for i in range(N):
        for j in succ[i]:
            indeg[j] += 1
    roots = [i for i in range(N) if indeg[i] == 0]

    def reachable(rs):
        seen = set(rs)
        stk = list(rs)
        while stk:
            u = stk.pop()
            for w in succ[u]:
                if w not in seen:
                    seen.add(w)
                    stk.append(w)
        return seen
    rset = reachable(roots)
    while len(rset) < N:  # cycles nothing else depends on
        roots.append(min(i for i in range(N) if i not in rset))
        rset = reachable(roots)
    idom, order = dominators(N, roots, succ)
    famrel = f'{fam}_{feed_rel}'
    size, quality = [], []
    for n in names:
        twin = n.replace(k_img, k_feed) if (n in inferred and k_img and k_feed) else None
        b, qy = installed_size(n, arch_of[n], ver_of[n], famrel, st[n], twin)
        size.append(b); quality.append(qy)
    kids = collections.defaultdict(list)
    for v, d in idom.items():
        if v != N:
            kids[d].append(v)
    ret, rc = [0] * N, [0] * N
    for v in order:
        if v == N:
            continue
        ret[v] = size[v] + sum(ret[c] for c in kids[v])
        rc[v] = 1 + sum(rc[c] for c in kids[v])
    fw = closure_counts(N, succ)
    rsucc = [[] for _ in range(N)]
    for i in range(N):
        for j in succ[i]:
            rsucc[j].append(i)
    rv = closure_counts(N, rsucc)
    idom_list = [(-1 if idom[i] == N else idom[i]) for i in range(N)]
    rootset = set(roots)
    shared = [i for i in range(N) if idom_list[i] == -1 and i not in rootset]
    recipes = sorted({(st[n] or {}).get('OE', '?') for n in names})
    ri = {r: i for i, r in enumerate(recipes)}
    sections = sorted({(st[n] or {}).get('Section', '?') for n in names})
    si = {s: i for i, s in enumerate(sections)}
    archs = sorted(set(arch_of.values()))
    ai = {a: i for i, a in enumerate(archs)}

    def desc(n):
        s = st[n]
        if s is None:
            return 'Not found in the current feed, so its dependencies are unknown.'
        if n in inferred:
            t = re.sub(r'\s+', ' ', s.get('Description', '').split('\n')[0]).strip()[:80]
            return t + ' (links inferred from the same module in the current feed)'
        t = re.sub(r'\s+', ' ', s.get('Description', '').split('\n')[0]).strip()
        return t[:110] + ('…' if len(t) > 110 else '')
    bi = buildinfo(release, machine)
    slug = re.sub(r'[^a-z0-9-]+', '-', f'{release}-{image}-{machine}'.lower())
    meta = {'slug': slug, 'image': image, 'machine': machine, 'release': release, 'family': fam,
            'feed': f'{fam}/{feed_rel}', 'manifestDate': date, 'manifestFile': fname,
            'buildId': bi.get('build-id', ''), 'bsp': bi.get('bsp', ''), 'project': bi.get('project', '').split(' ')[0],
            'match': {'exact': exact, 'newer': newer, 'inferred': len(inferred), 'missing': missing}, 'kernel': k_img or '', 'feedKernel': k_feed or '', 'sizes': {'exact': quality.count(0), 'estimate': quality.count(1), 'unknown': quality.count(2)}}
    data = {'meta': meta, 'n': names, 'r': recipes, 's': sections, 'a': archs,
            'oe': [ri[(st[n] or {}).get('OE', '?')] for n in names],
            'sec': [si[(st[n] or {}).get('Section', '?')] for n in names],
            'ar': [ai[arch_of[n]] for n in names], 'v': [ver_of[n] for n in names],
            'fv': [('' if st[n] is None or st[n]['Version'] == ver_of[n] else st[n]['Version']) for n in names],
            'miss': [i for i, n in enumerate(names) if st[n] is None],
            'inf': [i for i, n in enumerate(names) if n in inferred],
            'za': [i for i in range(N) if quality[i] == 1], 'zu': [i for i in range(N) if quality[i] == 2],
            'd': [desc(n) for n in names], 'sz': size, 'ret': ret, 'rc': rc, 'fw': fw, 'rv': rv,
            'dep': dep, 'rec': rec, 'idom': idom_list, 'roots': roots}
    with open(os.path.join(outdir, 'data', slug + '.json'), 'w') as fh:
        json.dump(data, fh, separators=(',', ':'), ensure_ascii=False)
    nonloc = [i for i in roots if '-locale-' not in names[i]]
    top = sorted(nonloc, key=lambda i: -ret[i])[:3]
    summary = dict(meta)
    summary.update({'packages': N, 'recipes': len(recipes), 'roots': len(roots), 'bytes': sum(size),
                    'sharedBytes': sum(ret[i] for i in shared), 'sharedCount': sum(rc[i] for i in shared),
                    'links': sum(map(len, dep)) + sum(map(len, rec)),
                    'top': [[names[i], ret[i]] for i in top]})
    return summary


index = []
for line in open(os.path.join(base, 'listings', 'manifests.txt')):
    release, machine, fname, date = line.split()
    s = build(release, machine, fname, date)
    m = s['match']
    print(f"{release:10s} {s['image'][:34]:34s} {machine:30s} pkgs {s['packages']:5d} roots {s['roots']:3d} "
          f"{s['bytes']/1e6:7.1f} MB inst ({s['sizes']['exact']}/{s['sizes']['estimate']}/{s['sizes']['unknown']})  exact {m['exact']} newer {m['newer']} inferred {m['inferred']} missing {m['missing']}", flush=True)
    index.append(s)
with open(os.path.join(outdir, 'index.json'), 'w') as fh:
    json.dump(index, fh, separators=(',', ':'))
