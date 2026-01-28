# cargt.github.io

## Building Documentation Locally

To build the documentation locally, follow these steps:

```sh
git clone git@github.com:cargt/cargt.github.io.git
cd cargt.github.io/docs
git checkout feature/build-docs
pip install -r requirements.txt
build-docs -l en
```


## Project Overview

This repository contains the source and build scripts for the Cargt Developer Documentation. Documentation is written in reStructuredText and built using [Sphinx](https://www.sphinx-doc.org/) and [ESP-Docs](https://github.com/espressif/esp-docs).

## Prerequisites

- Python 3.7 or newer
- [pip](https://pip.pypa.io/en/stable/)
- [git](https://git-scm.com/)

All required Python packages are listed in `docs/requirements.txt`.

## Build Output

After running the build commands above, the generated HTML documentation will be located in:

- `docs/_build/en/generic/html/` (when using ESP-Docs CLI)

Open `index.html` in that directory to view the documentation locally in your browser.

## Troubleshooting

- If you encounter missing dependencies, ensure you are using the correct Python version and that all requirements are installed.
- For Sphinx or ESP-Docs errors, consult the [Sphinx documentation](https://www.sphinx-doc.org/en/master/usage/troubleshooting.html) or [ESP-Docs issues](https://github.com/espressif/esp-docs/issues).

## Documentation Structure

- Source files: `docs/en/`
- Static assets: `docs/en/_static/`
- Configuration: `docs/en/conf.py`, `docs/conf_common.py`

## Additional Resources

- [Cargt Developer Documentation (Online)](https://cargt.github.io/)
- [ESP-Docs Documentation](https://docs.espressif.com/projects/esp-docs/en/latest/)
- [Sphinx Documentation](https://www.sphinx-doc.org/)

