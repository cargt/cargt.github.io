# ESP-Docs Setup Summary

This repository has been configured to use ESP-Docs with GitHub Pages for publishing technical documentation.

## What is ESP-Docs?

ESP-Docs is a documentation framework built on Sphinx, originally developed by Espressif Systems for their ESP-IDF documentation. It provides:

- Professional documentation themes
- Multi-language support
- Rich reStructuredText formatting
- Integration with various Sphinx extensions
- Easy deployment to GitHub Pages

## What Was Set Up

### 1. Documentation Structure

```
docs/
├── README.md              # Documentation build instructions
├── requirements.txt       # Python dependencies
├── conf_common.py        # Common Sphinx configuration
├── en/                   # English documentation
│   ├── conf.py          # Language-specific config
│   ├── index.rst        # Main page
│   ├── introduction.rst # Introduction page
│   └── getting-started.rst # Getting started guide
└── _build/              # Build output (git-ignored)
    └── html/            # Generated HTML files
```

### 2. GitHub Actions Workflow

The workflow (`.github/workflows/docs.yml`) automatically:
- Triggers on pushes to the main branch
- Installs Python dependencies
- Builds the documentation using Sphinx
- Deploys the built HTML to the `gh-pages` branch
- Makes the site available at `https://cargt.github.io`

### 3. Configuration Files

- **docs/conf_common.py**: Main Sphinx configuration with ReadTheDocs theme
- **docs/en/conf.py**: English-specific settings
- **docs/requirements.txt**: Required Python packages
- **.gitignore**: Excludes build artifacts from git

## How to Use

### Building Documentation Locally

1. Install dependencies:
   ```bash
   pip install -r docs/requirements.txt
   ```

2. Build the documentation:
   ```bash
   cd docs/en
   sphinx-build -b html . ../_build/html
   ```

3. View the documentation:
   ```bash
   open ../docs/_build/html/index.html
   ```

### Adding New Pages

1. Create a new `.rst` file in `docs/en/`
2. Add it to the table of contents in `docs/en/index.rst`
3. Build locally to verify
4. Commit and push

Example:
```rst
.. toctree::
   :maxdepth: 2
   :caption: Contents:

   introduction
   getting-started
   your-new-page    # Add this line
```

### Writing Documentation

Documentation uses reStructuredText format. Common syntax:

```rst
Page Title
==========

Section
-------

Subsection
~~~~~~~~~~

**Bold text** and *italic text*

Code blocks:

.. code-block:: python

   def hello():
       print("Hello, World!")

Links:
`Link text <https://example.com>`_

Lists:
- Item 1
- Item 2
```

## Next Steps

### Enable GitHub Pages

After merging this PR, you need to enable GitHub Pages:

1. Go to repository Settings → Pages
2. Under "Source", select:
   - Branch: `gh-pages`
   - Folder: `/ (root)`
3. Click "Save"
4. Wait a few minutes for deployment
5. Visit `https://cargt.github.io`

### Customize the Documentation

You can customize by editing:

- **docs/conf_common.py**: Change theme, add extensions, modify settings
- **docs/en/index.rst**: Update main page content
- Add more `.rst` files for additional pages
- Add images to `docs/en/_static/`

### Supported Features

The current setup supports:

- ✅ Multiple documentation pages
- ✅ Table of contents navigation
- ✅ Search functionality
- ✅ Syntax highlighting
- ✅ Automatic deployment
- ✅ Mobile-responsive theme
- ✅ Direct links to page sections

### Adding More Languages

To add another language (e.g., Spanish):

1. Create `docs/es/` directory
2. Copy `docs/en/conf.py` to `docs/es/conf.py`
3. Change `language = 'es'` in the config
4. Add Spanish `.rst` files
5. Update `docs/conf_common.py` to include the new language

## Resources

- [Sphinx Documentation](https://www.sphinx-doc.org/)
- [reStructuredText Primer](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html)
- [ESP-Docs User Guide](https://docs.espressif.com/projects/esp-docs/en/latest/)
- [ReadTheDocs Theme](https://sphinx-rtd-theme.readthedocs.io/)

## Troubleshooting

### Build Fails Locally

- Ensure Python 3.7+ is installed
- Install dependencies: `pip install -r docs/requirements.txt`
- Check for syntax errors in `.rst` files

### GitHub Actions Fails

- Check the Actions tab in GitHub for error logs
- Verify `docs/requirements.txt` is correct
- Ensure `.rst` files have valid syntax

### Site Not Updating

- Check that changes are pushed to main branch
- Verify GitHub Actions workflow completed successfully
- GitHub Pages may take a few minutes to update
- Try clearing browser cache

## Summary

Your repository is now set up with a professional documentation system that:
- Automatically builds and deploys documentation
- Uses industry-standard tools (Sphinx, ESP-Docs)
- Provides a clean, navigable interface
- Is easy to maintain and extend
- Follows documentation best practices

The documentation will be live at `https://cargt.github.io` once you enable GitHub Pages in the repository settings.
