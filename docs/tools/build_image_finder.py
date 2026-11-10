#!/usr/bin/env python3
"""Assemble the Image Finder page, published at dev.cargt.com/image-finder/.

Fills docs/tools/image-maps/template.html and copies in the two data sets it
reads:

  --maps  size and dependency data from image-maps/refresh.sh (the
          image-maps-data branch, checked out at docs/image-maps-data/site)
  --scan  the yocto.cargt.com file listing from scan_yocto.py

into docs/en/_extra/image-finder/, which conf.py adds to html_extra_path.
Without the map data the page is not built, and the docs page says so.

Usage: python3 docs/tools/build_image_finder.py [--maps DIR] [--scan DIR]
"""

import argparse
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.normpath(os.path.join(HERE, ".."))


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--maps", default=os.path.join(DOCS, "image-maps-data", "site"))
    parser.add_argument("--scan", default=os.path.join(DOCS, "image-finder-scan"))
    parser.add_argument("--out", default=os.path.join(DOCS, "en", "_extra", "image-finder"))
    args = parser.parse_args()

    shutil.rmtree(args.out, ignore_errors=True)
    index_path = os.path.join(args.maps, "index.json")
    if not os.path.exists(index_path):
        print(f"warning: no map data in {args.maps}; /image-finder/ is not built", file=sys.stderr)
        return 0

    os.makedirs(args.out)
    for name in ("data", "feeds"):
        shutil.copytree(os.path.join(args.maps, name), os.path.join(args.out, name))
    shutil.copy(os.path.join(args.maps, "installed.json"), args.out)

    date_path = os.path.join(args.maps, "read-date.txt")
    maps_date = open(date_path).read().strip() if os.path.exists(date_path) else "on an unknown date"

    scan_date = "on an unknown date"
    scan_index = os.path.join(args.scan, "index.json")
    if os.path.exists(scan_index):
        shutil.copytree(args.scan, os.path.join(args.out, "yocto"))
        scan_date = json.load(open(scan_index))["generated"][:10]
    else:
        print(f"warning: no file listing in {args.scan}; run scan_yocto.py first", file=sys.stderr)

    page = open(os.path.join(HERE, "image-maps", "template.html")).read()
    index = open(index_path).read().replace("</", "<\\/")
    assert page.count("__INDEX__") == 1
    page = (page.replace("__INDEX__", index)
                .replace("__MAPS_DATE__", maps_date)
                .replace("__SCAN_DATE__", scan_date))
    with open(os.path.join(args.out, "index.html"), "w") as f:
        f.write(page)
    count = len(json.loads(open(index_path).read()))
    print(f"Image Finder: {count} images, sizes read {maps_date}, files read {scan_date}, written to {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
