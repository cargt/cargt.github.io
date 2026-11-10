#!/usr/bin/env python3
"""Snapshot the nightly images on yocto.cargt.com for the Image Finder page.

yocto.cargt.com sends no CORS headers, so the page on dev.cargt.com cannot
read its directory listings from the browser. This script reads them once,
read-only, and writes JSON that the page loads:

  <out>/index.json                   releases, boards, images and files
  <out>/<release>/<machine>.json     package lists from each image's .manifest

Usage: python3 docs/tools/scan_yocto.py [--out docs/en/_static/data/yocto]

Standard library only, so it runs in the docs CI job without extra packages.
"""

import argparse
import concurrent.futures
import datetime
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

BASE = "https://yocto.cargt.com"
# Releases are the folders under /images/. These come first, in this order
# (as on releases.rst); any other release folder follows, by name.
RELEASE_ORDER = ["wrynose", "wrynose-rt", "scarthgap"]

# SOM / carrier names and catalog pages, as on releases.rst. A MACHINE that
# is published but not listed here is shown by its MACHINE name.
BOARDS = {
    "imx8mp-cargt-00377-00365": ("00377 i.MX 8M Plus", "00365",
                                 "catalog/soms/00377-imx8mplus-osml-iw612"),
    "imx91-cargt-00363-00365": ("00363 i.MX 91", "00365",
                                "catalog/soms/00363-91-imx91-osml-iw612"),
    "imx93-cargt-00363-00365": ("00363 i.MX 93", "00365",
                                "catalog/soms/00363-93-imx93-osml-iw612"),
    "imx93-cargt-00363-00428": ("00363 i.MX 93", "00428",
                                "catalog/soms/00363-93-imx93-osml-iw612"),
    "imx93-cargt-00324-00326": ("00324 i.MX 93 SODIMM", "00326",
                                "catalog/soms/00324-imx93-sodimm"),
    "imx93-cargt-00359-00406": ("00359 i.MX 93 LGA", "00406",
                                "catalog/soms/00359-lga-murata2el"),
    "imx95-cargt-00414-00365": ("00414 i.MX 95", "00365",
                                "catalog/soms/00414-imx95-osml"),
    "imx95-cargt-00414-00428": ("00414 i.MX 95", "00428",
                                "catalog/soms/00414-imx95-osml"),
    "imx95-15x15-lpddr4x-frdm": ("NXP FRDM i.MX 95", "", ""),
    "imx95-19x19-lpddr5-frdm-pro": ("NXP FRDM Pro i.MX 95", "", ""),
    "stm32mp25-cargt-00395-02-00365": ("00395-02 STM32MP257F", "00365",
                                       "catalog/soms/00395-stm32mp257f-osml-iw610"),
    "stm32mp25-cargt-00395-01-00365": ("00395-01 STM32MP257F", "00365",
                                       "catalog/soms/00395-stm32mp257f-osml-iw610"),
    "stm32mp25-cargt-00395-00365v3": ("00395 STM32MP257F", "00365 revision 3",
                                      "catalog/soms/00395-stm32mp257f-osml-iw610"),
}

# One row of an Apache "?F=1" listing: link, then date, time and size.
ROW_RE = re.compile(
    r'<a href="([^"?/][^"?]*)">[^<]*</a>\s*(?:</td><td[^>]*>)?\s*'
    r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\s*(?:</td><td[^>]*>)?\s*([\d.]+[KMGT]?|-)')
HREF_RE = re.compile(r'href="([^"?/][^"?]*)"')


def get(url, timeout=120, tries=3):
    req = urllib.request.Request(url, headers={"User-Agent": "dev.cargt.com image finder"})
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read().decode("utf-8", "replace")
        except urllib.error.HTTPError:
            raise  # a 404 is an answer, not a network problem
        except OSError:
            if attempt == tries - 1:
                raise
            time.sleep(5 * (attempt + 1))


def listing(path):
    """Return {name: {"date", "size"}} for a directory; subdirectories end in /."""
    html = get(f"{BASE}/{path}?F=1")
    rows = {}
    for name, date, size in ROW_RE.findall(html):
        rows[name] = {"date": date, "size": "" if size == "-" else size}
    # Fall back to bare links if the row format ever changes.
    for name in HREF_RE.findall(html):
        rows.setdefault(name, {"date": "", "size": ""})
    return rows


def parse_build_info(text):
    info = {}
    for line in text.splitlines():
        m = re.match(r"^([a-z-]+):\s+(.*?)\s*(?:\(.*\))?$", line)
        if m and m.group(2):
            info[m.group(1)] = m.group(2)
    return info


def parse_manifest(text):
    pkgs = []
    for line in text.splitlines():
        parts = line.split()
        if len(parts) == 3:
            pkgs.append(parts)
    return pkgs


def file_entry(path, name, rows):
    row = rows[name]
    return {"name": name, "url": f"{BASE}/{path}{name}",
            "date": row["date"], "size": row["size"]}


def scan_board(release, machine, feed_root, feed_dirs):
    path = f"images/{release}/{machine}/"
    rows = listing(path)
    names = sorted(rows)
    stm32 = machine.startswith("stm32")
    som, carrier, doc = BOARDS.get(machine, (machine, "", ""))
    board = {
        "machine": machine,
        "som": som,
        "carrier": carrier,
        "doc": doc,
        "family": "stm32mp2" if stm32 else "imx",
        "folder": f"{BASE}/{path}",
        "build_info": {},
        "images": [],
        "bootloader": None,
        "bundles": [],
        "flash_layouts": [],
        "device_trees": [],
    }

    if "BUILD-INFO.txt" in rows:
        board["build_info"] = parse_build_info(get(f"{BASE}/{path}BUILD-INFO.txt"))
        board["build_info"]["file"] = file_entry(path, "BUILD-INFO.txt", rows)

    for boot in ("imx-boot.tagged", "imx-boot-tagged"):
        if boot in rows:
            board["bootloader"] = file_entry(path, boot, rows)
            break

    board["bundles"] = [file_entry(path, n, rows) for n in names if n.endswith(".raucb")]

    # Flashable images are the ones with a .wic; containers and Xen guests have none.
    image_names = sorted({n.split(f"-{machine}.rootfs.wic")[0]
                          for n in names if f"-{machine}.rootfs.wic" in n})
    packages = {}
    for image in image_names:
        prefix = f"{image}-{machine}.rootfs"
        files = {}
        for key, suffix in (("wic_zst", ".wic.zst"), ("wic_bz2", ".wic.bz2"),
                            ("wic", ".wic"), ("bmap", ".wic.bmap"),
                            ("manifest", ".manifest"), ("sbom", ".spdx.json"),
                            ("sbom", ".spdx.tar.zst"), ("rootfs", ".tar.zst"),
                            ("rootfs", ".tar.xz"), ("licenses", "-license_content.html")):
            if prefix + suffix in rows and key not in files:
                files[key] = file_entry(path, prefix + suffix, rows)
        # i.MX: <image>-swu-<machine>.rootfs.swu updates to <image>.
        swu = f"{image}-swu-{machine}.rootfs.swu"
        if swu in rows:
            files["swu"] = file_entry(path, swu, rows)

        entry = {"name": image, "files": files, "feeds": [], "package_count": 0}
        if "manifest" in files:
            pkgs = parse_manifest(get(files["manifest"]["url"]))
            packages[image] = pkgs
            entry["package_count"] = len(pkgs)
            if feed_root:
                archs = sorted({p[1] for p in pkgs})
                for arch in archs:
                    for d in (arch, arch.replace("-", "_")):
                        if d + "/" in feed_dirs:
                            entry["feeds"].append(f"{BASE}/{feed_root}{d}")
                            break
        board["images"].append(entry)

    # Device trees: i.MX keeps them in the folder, STM32MP2 in kernel/. Each
    # one is there twice, once with a -<machine> suffix.
    dt_names = listing(path + "kernel/") if stm32 and "kernel/" in rows else rows
    board["device_trees"] = sorted(
        n for n in dt_names
        if n.endswith(".dtb") and not n.endswith(f"-{machine}.dtb"))

    # STM32MP2 flash layouts: flashlayout_<image>/optee/*.tsv, where the
    # folder name is the start of the image name (cargt-image-dev for
    # cargt-image-dev-cargt-openstlinux-weston).
    for fl in (n for n in names if n.startswith("flashlayout_") and n.endswith("/")):
        base_image = fl[len("flashlayout_"):-1]
        image = next((i for i in image_names if i.startswith(base_image)), None)
        if image and "optee/" in listing(path + fl):
            for n in sorted(listing(f"{path}{fl}optee/")):
                if n.endswith(".tsv"):
                    board["flash_layouts"].append({
                        "image": image,
                        "path": f"{fl}optee/{n}",
                        "url": f"{BASE}/{path}{fl}optee/{n}",
                    })

    return board, packages


def scan(out):
    os.makedirs(out, exist_ok=True)
    found = [n.rstrip("/") for n in listing("images/") if n.endswith("/")]
    known = [r for r in RELEASE_ORDER if r in found]
    release_names = known + sorted(r for r in found if r not in known)

    feed_roots = {"imx": {}, "stm32mp2": {}}
    for release in release_names:
        for fam, root in (("imx", f"linux-imx/{release}/"),
                          ("stm32mp2", f"openstlinux/{release}/")):
            try:
                feed_roots[fam][release] = (root, set(listing(root)))
            except Exception:
                feed_roots[fam][release] = (None, set())

    jobs = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        releases = []
        for release in release_names:
            # Boards in BOARDS order (as on releases.rst), then any others.
            order = list(BOARDS)
            machines = sorted((n.rstrip("/") for n in listing(f"images/{release}/")
                               if n.endswith("/")),
                              key=lambda m: (order.index(m) if m in order else len(order), m))
            releases.append({"name": release, "machines": machines})
            for machine in machines:
                fam = "stm32mp2" if machine.startswith("stm32") else "imx"
                root, dirs = feed_roots[fam][release]
                jobs[(release, machine)] = pool.submit(scan_board, release, machine, root, dirs)

        index = {
            "generated": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
            "base": BASE,
            "releases": [],
        }
        failed = []
        for rel in releases:
            boards = []
            for machine in rel["machines"]:
                try:
                    board, packages = jobs[(rel["name"], machine)].result()
                except Exception as exc:
                    failed.append(f"{rel['name']}/{machine}: {exc}")
                    continue
                if not board["images"]:
                    continue
                boards.append(board)
                os.makedirs(os.path.join(out, rel["name"]), exist_ok=True)
                with open(os.path.join(out, rel["name"], machine + ".json"), "w") as f:
                    json.dump(packages, f, separators=(",", ":"))
            index["releases"].append({"name": rel["name"], "boards": boards})

    with open(os.path.join(out, "index.json"), "w") as f:
        json.dump(index, f, indent=1)
    for msg in failed:
        print("warning:", msg, file=sys.stderr)
    count = sum(len(r["boards"]) for r in index["releases"])
    print(f"{count} boards in {len(index['releases'])} releases written to {out}")
    # Any failed folder is an error, so a scheduled deploy keeps the last
    # complete list instead of publishing a partial one.
    return 0 if count and not failed else 1


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", default=os.path.join(here, "..", "en", "_static", "data", "yocto"))
    args = parser.parse_args()
    return scan(os.path.normpath(args.out))


if __name__ == "__main__":
    sys.exit(main())
