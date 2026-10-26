# cargt.github.io

Source for the Cargt Developer Documentation, published at
[dev.cargt.com](https://dev.cargt.com/). Pages are written in
reStructuredText and built with [Sphinx](https://www.sphinx-doc.org/) through
the [ESP-Docs](https://github.com/espressif/esp-docs) `build-docs` front end.

## Prerequisites

- Python 3.10 or newer, with [pip](https://pip.pypa.io/en/stable/)
- [git](https://git-scm.com/) and [Git LFS](https://git-lfs.com/) (images are stored in LFS)

## Building Locally

```sh
git clone git@github.com:cargt/cargt.github.io.git
cd cargt.github.io
git lfs pull
python3 -m venv .venv
. .venv/bin/activate
pip install -r docs/requirements.txt
cd docs
build-docs -l en
```

The HTML output is written to `docs/_build/en/generic/html/`. Open
`index.html` there in a browser.

Before opening a pull request, check that the build has no warnings:

```sh
cat docs/_build/en/generic/sphinx-warning-log.txt
```

The same check runs in CI on every pull request. Warnings listed in
`docs/sphinx-known-warnings.txt` are ignored.

## Documentation Structure

- `docs/en/index.rst` - home page
- `docs/en/core/index.rst` - main developer guide
- `docs/en/core/catalog/` - SOM and carrier board pages
- `docs/en/core/*.rst` - standalone topic pages (real-time Linux, RAUC, ...)
- `docs/en/references/` - external references
- `docs/en/_static/` - images, CSS, fonts
- `docs/en/conf.py` - Sphinx configuration

## Release

Merging to `main` runs the `Build & Deploy ESP-Docs (GitHub Pages)` workflow,
which publishes the site to dev.cargt.com within a few minutes. Check the
workflow run in the repository's Actions tab if the site does not update.

A separate weekly workflow checks external links and reports broken ones.

## Troubleshooting

- Missing Python modules: make sure the virtual environment is active and
  `pip install -r docs/requirements.txt` completed.
- Images show as small text files: run `git lfs pull`.
- For Sphinx or ESP-Docs errors, see the
  [Sphinx documentation](https://www.sphinx-doc.org/en/master/usage/troubleshooting.html)
  or [ESP-Docs issues](https://github.com/espressif/esp-docs/issues).
