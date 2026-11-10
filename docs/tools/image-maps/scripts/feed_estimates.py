"""Estimate installed size for feed packages that no image ships, from each .deb's xz index.

Usage: python3 -I feed_estimates.py <depmap-all dir>
Writes sizes/feed_est.json: {"<fam>_<rel>|<arch>|<name>|<version>": uncompressed data.tar bytes}
"""
import concurrent.futures as cf
import gzip
import json
import os
import re
import sys
import threading

import requests

base = sys.argv[1]
sys.path.insert(0, os.path.join(base, 'scripts'))
from xzsize import xz_uncompressed  # noqa: E402

SKIP = re.compile(r'-(dbg|src|staticdev|ptest|doc|locale-.+)$')
out_path = os.path.join(base, 'sizes', 'feed_est.json')
done = json.load(open(out_path)) if os.path.exists(out_path) else {}

# Tuples that some image ships (measured exactly from rootfs tarballs instead)
in_images = set()
for f in os.listdir(os.path.join(base, 'manifests')):
    for line in open(os.path.join(base, 'manifests', f)):
        p = line.split()
        if len(p) == 3:
            in_images.add((p[0], p[1], p[2]))


def stanzas(path):
    cur, key = {}, None
    fh = gzip.open(path, 'rt', encoding='utf-8', errors='replace') if path.endswith('.gz') else open(path, encoding='utf-8', errors='replace')
    for line in fh:
        line = line.rstrip('\n')
        if not line:
            if cur:
                yield cur
            cur, key = {}, None
            continue
        if line[0] in ' \t' and key:
            continue
        k, _, v = line.partition(':')
        key = k.strip()
        cur[key] = v.strip()
    if cur:
        yield cur


jobs = []
for famrel in sorted(os.listdir(os.path.join(base, 'feeds'))):
    d = os.path.join(base, 'feeds', famrel)
    if not os.path.isdir(d):
        continue
    fam, rel = famrel.split('_', 1)
    for f in sorted(os.listdir(d)):
        if not f.startswith('Packages-'):
            continue
        arch = f[len('Packages-'):].removesuffix('.gz')
        folder = arch.replace('-', '_') if re.match(r'^(imx|stm32mp)\d', arch) else arch
        for s in stanzas(os.path.join(d, f)):
            n, v = s['Package'], s['Version']
            if SKIP.search(n) or (n, arch, v) in in_images:
                continue
            key = f'{famrel}|{arch}|{n}|{v}'
            if key in done:
                continue
            url = f"https://yocto.cargt.com/{fam}/{rel}/{folder}/{s['Filename'].removeprefix('./')}"
            jobs.append((key, url, int(s.get('Size', 0))))
print('to estimate', len(jobs), 'already done', len(done), flush=True)

local = threading.local()


def session():
    if not hasattr(local, 's'):
        local.s = requests.Session()
    return local.s


def fetch(job):
    key, url, size = job
    want = 2048
    for _ in range(4):
        try:
            r = session().get(url, headers={'Range': f'bytes=-{min(want, size) if size else want}'}, timeout=60)
            if r.status_code not in (200, 206):
                return key, None
            total, need = xz_uncompressed(r.content)
            if total is not None:
                return key, total
            if need and need > want:
                want = need + 64
                continue
            return key, None
        except requests.RequestException:
            continue
    return key, None


lock = threading.Lock()
count = 0
with cf.ThreadPoolExecutor(max_workers=40) as ex:
    for key, total in ex.map(fetch, jobs):
        with lock:
            count += 1
            if total is not None:
                done[key] = total
            if count % 5000 == 0:
                json.dump(done, open(out_path, 'w'))
                print(f'{count}/{len(jobs)}', flush=True)
json.dump(done, open(out_path, 'w'))
print('done', len(done), 'failed', len(jobs) - sum(1 for k, _, _ in jobs if k in done), flush=True)
