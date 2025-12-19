# Documentation

This directory contains the technical documentation for the cargt project, built using ESP-Docs.

## Building Documentation Locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Build the HTML documentation:
   ```bash
   cd docs/en
   sphinx-build -b html . ../_build/html
   ```

3. View the generated documentation:
   ```bash
   open _build/html/index.html
   ```

## Directory Structure

- `en/` - English documentation
  - `conf.py` - Language-specific configuration
  - `index.rst` - Main documentation entry point
  - `*.rst` - Documentation pages
- `conf_common.py` - Common configuration for all languages
- `requirements.txt` - Python dependencies
- `_static/` - Static files (images, CSS, etc.)

## Deployment

Documentation is automatically built and deployed to GitHub Pages when changes are pushed to the main branch. The workflow is defined in `.github/workflows/docs.yml`.

## Writing Documentation

Documentation files use reStructuredText (.rst) format. For more information on the syntax, see:
- [Sphinx reStructuredText Primer](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html)
- [ESP-Docs User Guide](https://docs.espressif.com/projects/esp-docs/en/latest/)

## Contributing

When adding new documentation pages:
1. Create a new `.rst` file in the `en/` directory
2. Add the page to the table of contents in `index.rst`
3. Build locally to verify formatting
4. Commit and push your changes
