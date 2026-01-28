
# ESP-Docs config for ENGLISH ONLY build
from esp_docs.conf_docs import *  # noqa: F403,F401

extensions += [
    'sphinx_copybutton',
    'sphinxcontrib.wavedrom',
]

# Only build English
languages = ['en']

# link roles config
github_repo = 'espressif/esp-idf'

# context used by sphinx_idf_theme
html_context['github_user'] = 'espressif'
html_context['github_repo'] = 'esp-docs'

html_static_path = ['../_static']

# Extra options required by sphinx_idf_theme
project_slug = 'esp-docs'

# Contains info used for constructing target and version selector
versions_url = './_static/docs_version.js'

# Final PDF filename will contains target and version
pdf_file_prefix = u'esp-docs'
