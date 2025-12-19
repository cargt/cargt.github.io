
# Basic Sphinx config; ESP‑Docs augments defaults behind the scenes.
import os
import sys

project = "Cargt Developer Documentation"
author = "Cargt"
extensions = [
    "sphinx_copybutton",
    "sphinx_tabs.tabs",
    "numpydoc",
    # "notfound.extension",  # enable if you added sphinx-notfound-page
]

templates_path = ["_templates"]
html_static_path = ["_static"]
html_theme = "sphinx_rtd_theme"  # ESP‑Docs aligns with Espressif’s theme tooling
html_title = "Cargt DeveloperDocumentation"

html_context = {
    "display_github": True,
    "github_user": "cargt",
    "github_repo": "cargt.github.io",
    # github_version usually ends with a trailing slash and includes the docs path prefix
    # For example, if docs are in /docs, and branch is main:
    "github_version": "main/",
    "conf_py_path": "/docs/",
}
