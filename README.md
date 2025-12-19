# cargt.github.io

Technical documentation site powered by ESP-Docs and hosted on GitHub Pages.

## Documentation

The documentation is available at: https://cargt.github.io

## Building Locally

To build the documentation locally:

```bash
pip install -r docs/requirements.txt
cd docs/en
sphinx-build -b html . ../_build/html
```

The generated HTML will be in `docs/_build/html/`.

## Contributing

Documentation is written in reStructuredText format. See the `docs/` directory for more information.

## Deployment

Documentation is automatically built and deployed to GitHub Pages when changes are pushed to the main branch.