"""Pick the fewest rootfs tarballs that cover every distinct package build across all images.

Usage: python3 -I scripts/plan_rootfs.py <work dir>
Reads listings/ and manifests/ from fetch_inputs.sh and writes sizes/plan.json for run_rootfs.sh.
Packages built for the same CPU are identical across boards, so one tarball can cover many images;
machine-specific packages (kernel modules, firmware, device trees) still need each board's own rootfs.
"""
import json
import os
import re
import sys

base = sys.argv[1]
os.makedirs(os.path.join(base, 'sizes'), exist_ok=True)


def strip(html):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]*>', ' ', html))


units = {'K': 1e3, 'M': 1e6, 'G': 1e9}


def megabytes(text):
    return float(text[:-1]) * units[text[-1]] / 1e6 if text[-1] in units else float(text) / 1e6


tars, builds = {}, {}
for line in open(os.path.join(base, 'listings', 'manifests.txt')):
    release, machine, fname, _date = line.split()
    stem = fname.replace('.rootfs.manifest', '')
    html = open(os.path.join(base, 'listings', f'm_{release}__{machine}.html')).read()
    m = re.search(re.escape(stem) + r'\.rootfs\.tar\.(zst|xz)\s+\S+\s+\S+\s+([\d.]+[KMG]?)', strip(html))
    if not m:
        continue  # container and Xen guest images publish no rootfs tarball
    tars[(release, fname)] = {'release': release, 'manifest': fname, 'machine': machine,
                              'tar': f'{stem}.rootfs.tar.{m.group(1)}', 'kind': m.group(1), 'mb': megabytes(m.group(2))}
    man = os.path.join(base, 'manifests', f'{release}__{fname}')
    builds[(release, fname)] = {tuple(l.split()) for l in open(man) if len(l.split()) == 3}

covered, chosen = set(), []
while True:
    best = max(tars, key=lambda k: (len(builds[k] - covered), -tars[k]['mb']))
    if not builds[best] - covered:
        break
    chosen.append(best)
    covered |= builds[best]
plan = [{k: v for k, v in tars[c].items() if k != 'mb'} for c in chosen]
json.dump(plan, open(os.path.join(base, 'sizes', 'plan.json'), 'w'), indent=1)
print(f'{len(chosen)} tarballs, about {round(sum(tars[c]["mb"] for c in chosen))} MB to stream')
