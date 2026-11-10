#!/usr/bin/env python3
"""Keep measured rootfs sizes only while the tarball they came from is unchanged.

run_rootfs.sh skips a tarball whose sizes/<release>__<image>-<machine>.json
already exists, so a rebuilt rootfs would keep its old sizes. Before the run,
this deletes each sizes file whose tarball date in the listing differs from
the date recorded when it was measured. With --record, after the run, it
records the dates of the tarballs that now have sizes.

Usage: python3 -I stale_sizes.py [--record] <work dir>
"""
import json
import os
import re
import sys

record = sys.argv[1] == "--record"
base = sys.argv[-1]
dates_path = os.path.join(base, "sizes", "tar-dates.json")
dates = json.load(open(dates_path)) if os.path.exists(dates_path) else {}
plan = json.load(open(os.path.join(base, "sizes", "plan.json")))

stale = 0
for p in plan:
    html = open(os.path.join(base, "listings", f"m_{p['release']}__{p['machine']}.html")).read()
    text = re.sub(r"\s+", " ", re.sub(r"<[^>]*>", " ", html))
    m = re.search(re.escape(p["tar"]) + r" (\d{4}-\d{2}-\d{2} \d{2}:\d{2})", text)
    date = m.group(1) if m else ""
    out = os.path.join(base, "sizes", f"{p['release']}__{p['manifest'].removesuffix('.rootfs.manifest')}.json")
    if record:
        if os.path.exists(out):
            dates[out.rsplit("/", 1)[1]] = date
            # run_rootfs.sh also skips only files newer than rootfs_sizes.py
            os.utime(out)
    elif os.path.exists(out):
        if dates.get(out.rsplit("/", 1)[1]) != date:
            os.remove(out)
            stale += 1
        else:
            # refresh.sh has just copied the scripts in, and run_rootfs.sh
            # only skips sizes files newer than rootfs_sizes.py
            os.utime(out)

if record:
    json.dump(dates, open(dates_path, "w"), indent=1, sort_keys=True)
    print(f"recorded {len(dates)} tarball dates")
else:
    print(f"{stale} measured rootfs out of date, {len(plan)} in the plan")
