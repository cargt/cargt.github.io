#!/bin/bash
# Stream each planned rootfs tarball through rootfs_sizes.py, four at a time.
D="$1"
python3 -I -c "
import json, sys
for p in json.load(open(sys.argv[1])): print(p['release'], p['machine'], p['tar'], p['kind'], p['manifest'])
" "$D/sizes/plan.json" | xargs -P 4 -L 1 bash -c '
  rel=$0 mach=$1 tar=$2 kind=$3 man=$4
  out="$D/sizes/${rel}__${man%.rootfs.manifest}.json"
  [ -s "$out" ] && grep -q removeprefix "$D/scripts/rootfs_sizes.py" && [ "$out" -nt "$D/scripts/rootfs_sizes.py" ] && { echo "skip $out"; exit 0; }
  for try in 1 2 3; do
    curl -sS --max-time 1500 "https://yocto.cargt.com/images/$rel/$mach/$tar" | python3 -I "$D/scripts/rootfs_sizes.py" "$out" "$kind" && exit 0
    echo "retry $try $tar"; sleep 5
  done; echo "FAILED $tar"'
echo ALL-DONE
