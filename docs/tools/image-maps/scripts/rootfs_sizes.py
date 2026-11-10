"""Stream a rootfs tarball from stdin and compute each package's installed size from dpkg's file lists.

Usage: curl ... | python3 -I rootfs_sizes.py <out.json> <zst|xz>
Writes {"pkgs": {name: bytes}, "files": n, "total": bytes, "dpkg": bool}.
"""
import json
import sys
import tarfile

out = sys.argv[1]
kind = sys.argv[2]
if kind == 'zst':
    import zstandard
    src = zstandard.ZstdDecompressor().stream_reader(sys.stdin.buffer, read_size=1 << 20)
else:
    import lzma
    src = lzma.open(sys.stdin.buffer)
sizes = {}      # normalized path -> size (regular files)
links = {}      # hard link path -> target path
lists = {}      # package -> [paths]
total = 0
with tarfile.open(fileobj=src, mode='r|') as tf:
    for m in tf:
        p = '/' + m.name.removeprefix('./').lstrip('/')
        if m.isreg():
            sizes[p] = m.size
            total += m.size
            if p.startswith('/var/lib/dpkg/info/') and p.endswith('.list'):
                pkg = p[len('/var/lib/dpkg/info/'):-len('.list')].split(':')[0]
                data = tf.extractfile(m).read().decode('utf-8', 'replace')
                lists[pkg] = [line.strip() for line in data.splitlines() if line.strip()]
        elif m.islnk():
            links[p] = '/' + m.linkname.removeprefix('./').lstrip('/')
seen = set()
pk = {}
for pkg, paths in lists.items():
    s = 0
    for path in paths:
        q = links.get(path, path)
        if q in sizes and (pkg, q) not in seen:
            seen.add((pkg, q))
            s += sizes[q]
    pk[pkg] = s
with open(out, 'w') as fh:
    json.dump({'pkgs': pk, 'files': len(sizes), 'total': total, 'dpkg': bool(lists)}, fh)
print(f'{out}: files {len(sizes)} total {total/1e6:.1f} MB, dpkg lists {len(lists)}, attributed {sum(pk.values())/1e6:.1f} MB')
