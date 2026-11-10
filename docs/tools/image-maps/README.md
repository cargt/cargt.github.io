# Image Finder data and page

The Image Finder at `dev.cargt.com/image-finder/` combines two things:

- **Package size and dependency maps** for every image on yocto.cargt.com, by
  Mark Vogt, from `cargt-internal/yocto-utils/yocto-image-tools`
  (`image-builder-planning/dependency-maps/work`, commit `be3a628`,
  2026-11-08). `scripts/` here is a copy of his scripts, except that
  `make_site.sh` is replaced by `refresh.sh` and `build_image_finder.py`.
  `template.html` started as his `template_all.html`.
- **Downloads, flashing and update commands** for each image, from
  `../scan_yocto.py`.

## Pieces

| File | What it does |
|---|---|
| `scripts/` | Mark's pipeline: fetch listings, manifests and feeds; measure installed sizes from the rootfs tarballs; estimate feed-only packages; build each image's dependency data |
| `refresh.sh` | Runs that pipeline into an output folder, keeping `sizes/` between runs |
| `stale_sizes.py` | Drops measured sizes whose rootfs tarball has changed since it was measured |
| `template.html` | The page |
| `../build_image_finder.py` | Fills the template and copies the map data and the `scan_yocto.py` snapshot into `docs/en/_extra/image-finder/`, which Sphinx publishes at `/image-finder/` |

## Where the data lives

The map data is about 31 MB and the size cache about 7.5 MB, so neither is on
`main`. The `refresh-image-maps.yml` workflow runs `refresh.sh` weekly and
force-pushes the result to the `image-maps-data` branch as a single commit:

```
image-maps-data
├── site/    data/, feeds/, index.json, installed.json, read-date.txt
└── work/sizes/   measured sizes, feed estimates, tarball dates
```

The deploy workflow checks that branch out into `docs/image-maps-data/` and
runs `build_image_finder.py` before Sphinx. Without it, the site builds
without `/image-finder/` and the docs page says the tool is not available.

## Build it locally

```bash
git fetch origin image-maps-data
git worktree add docs/image-maps-data origin/image-maps-data
python3 docs/tools/scan_yocto.py
python3 docs/tools/build_image_finder.py
rm -rf docs/_build/en && (cd docs && build-docs -l en)
```
