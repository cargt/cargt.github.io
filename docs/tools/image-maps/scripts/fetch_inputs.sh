#!/bin/bash
# Download image folder listings, rootfs manifests, BUILD-INFO.txt files and the deb feed
# indexes the images need from yocto.cargt.com into a work directory.
#
# Usage: bash scripts/fetch_inputs.sh <work dir>
# Directory listings on yocto.cargt.com are slow (15-60 s each), so this takes a few minutes.
set -euo pipefail
D="${1:?usage: fetch_inputs.sh <work dir>}"
B=https://yocto.cargt.com
mkdir -p "$D"/{listings,manifests,buildinfo,feeds}
strip() { sed -e 's/<[^>]*>/ /g' | tr -s ' \t' ' ' | grep -v '^\s*$' | grep -v 'Index of\|Parent Directory\|Name Last modified' || true; }

# 1. Release folders under images/
for r in scarthgap wrynose wrynose-rt; do
  curl -sS -L --max-time 300 "$B/images/$r/" -o "$D/listings/images_$r.html"
done

# 2. Every board folder in each release (in parallel)
for r in scarthgap wrynose wrynose-rt; do
  for m in $(strip < "$D/listings/images_$r.html" | awk '{print $1}' | grep '/$' | tr -d '/'); do
    curl -sS -L --max-time 300 "$B/images/$r/$m/" -o "$D/listings/m_${r}__${m}.html" &
  done
done
wait

# 3. Rootfs manifests (initramfs and ST partition images left out)
: > "$D/listings/manifests.txt"
for f in "$D"/listings/m_*.html; do
  k=$(basename "$f" .html); k=${k#m_}; r=${k%%__*}; m=${k#*__}
  strip < "$f" | awk '{print $1, $2}' | grep '\.rootfs\.manifest' | grep -v initrd | while read -r n d; do echo "$r $m $n $d"; done
done >> "$D/listings/manifests.txt"
while read -r r m n d; do
  curl -sS --max-time 300 "$B/images/$r/$m/$n" -o "$D/manifests/${r}__${n}" &
done < "$D/listings/manifests.txt"
wait

# 4. BUILD-INFO.txt per board folder
cut -d' ' -f1,2 "$D/listings/manifests.txt" | sort -u | while read -r r m; do
  curl -sS --max-time 120 "$B/images/$r/$m/BUILD-INFO.txt" -o "$D/buildinfo/${r}__${m}.txt"
done

# 5. Feed indexes for every package architecture the images use.
#    wrynose-rt has no feed of its own, so it uses linux-imx/wrynose.
for f in "$D"/manifests/*; do
  b=$(basename "$f"); r=${b%%__*}
  case "$b" in *stm32mp*) fam=openstlinux ;; *) fam=linux-imx ;; esac
  [ "$r" = wrynose-rt ] && r=wrynose
  awk -v k="$fam $r" '{print k, $2}' "$f"
done | sort -u > "$D/feeds/needed.txt"
while read -r fam rel arch; do
  case "$arch" in imx*|stm32mp*) dir=$(echo "$arch" | tr '-' '_') ;; *) dir=$arch ;; esac
  mkdir -p "$D/feeds/${fam}_${rel}"
  curl -sS --max-time 300 "$B/$fam/$rel/$dir/Packages.gz" -o "$D/feeds/${fam}_${rel}/Packages-${arch}.gz" &
done < "$D/feeds/needed.txt"
wait
echo "Inputs ready in $D: $(wc -l < "$D/listings/manifests.txt") manifests, $(wc -l < "$D/feeds/needed.txt") feed folders"
