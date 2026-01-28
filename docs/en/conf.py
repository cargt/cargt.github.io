
# Basic Sphinx config; ESP‑Docs augments defaults behind the scenes.
import os
import sys
html_static_path = ["_static"]
html_css_files = [
    "custom.css",
]

project = "Cargt Developer Documentation"
author = "Cargt"
extensions = [
    "sphinx_copybutton",
    "sphinx_tabs.tabs",
    "numpydoc",
    "sphinx_design",
    # "notfound.extension",  # enable if you added sphinx-notfound-page
]
html_logo = "_static/Cargt-Logo.png"  # Path relative to the docs directory
templates_path = ["_templates"]
copyright = "2025, Cargt Inc"
html_theme = "sphinx_rtd_theme" # Read the Docs theme
html_title = "Cargt Developer Documentation"
html_theme_options = {
     'style_nav_header_background': "#F2F2F2",
}

html_context = {
    "display_github": True,
    "github_user": "cargt",
    "github_repo": "cargt.github.io",
    # github_version usually ends with a trailing slash and includes the docs path prefix
    # For example, if docs are in /docs, and branch is main:
    "github_version": "main/",
    "conf_py_path": "/docs/en/",
}
