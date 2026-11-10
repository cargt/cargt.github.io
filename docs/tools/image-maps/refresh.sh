#!/bin/bash
# Refresh the Image Finder's size and dependency data from yocto.cargt.com.
#
# Usage: bash docs/tools/image-maps/refresh.sh <work dir> <out dir>
#
# <work dir> keeps sizes/ between runs (measured installed sizes and feed
# estimates), so only rootfs tarballs that changed are streamed again and only
# new feed package versions are estimated. A first run streams about 8.5 GB and
# takes one to two hours. <out dir> gets data/, feeds/, index.json,
# installed.json and read-date.txt, which build_image_finder.py turns into the
# page. Needs Python 3.10+, curl, and pip packages zstandard and requests.
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
D=${1:?usage: refresh.sh <work dir> <out dir>}
OUT=${2:?usage: refresh.sh <work dir> <out dir>}
mkdir -p "$D/sizes" "$OUT"

# Fresh inputs every run; only sizes/ carries over.
rm -rf "$D/scripts" "$D/listings" "$D/manifests" "$D/buildinfo" "$D/feeds"
cp -r "$HERE/scripts" "$D/scripts"

bash "$D/scripts/fetch_inputs.sh" "$D"
python3 -I "$D/scripts/plan_rootfs.py" "$D"
python3 -I "$HERE/stale_sizes.py" "$D"
bash "$D/scripts/run_rootfs.sh" "$D"
python3 -I "$HERE/stale_sizes.py" --record "$D"
python3 -I "$D/scripts/feed_estimates.py" "$D"

rm -rf "$OUT/data" "$OUT/feeds"
python3 -I "$D/scripts/build_all.py" "$D" "$OUT" | tail -5
python3 -I "$D/scripts/export_feeds.py" "$D" "$OUT" | head -3
date -u +%Y-%m-%d > "$OUT/read-date.txt"
echo "Image Finder data written to $OUT"
