
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
html_logo = "_static/Cargt-Logo.png"  # Path relative to the docs directory
templates_path = ["_templates"]
copyright = "2025, Cargt Inc"
html_theme = "sphinx_rtd_theme"  # ESP‑Docs aligns with Espressif’s theme tooling
html_title = "Cargt Developer Documentation"
html_theme_options = {
    'style_nav_header_background': "#7b8ea1",  # Deep blue-gray, complements green/yellow in Cargt-Logo.png
}

html_context = {
    "display_github": True,
    "github_user": "cargt",
    "github_repo": "cargt.github.io",
    # github_version usually ends with a trailing slash and includes the docs path prefix
    # For example, if docs are in /docs, and branch is main:
    "github_version": "main/",
    "conf_py_path": "/docs/",
}
