
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
    "sphinxcontrib.images",
    # "notfound.extension",  # enable if you added sphinx-notfound-page
]
images_config = {
    # Use the explicit `.. thumbnail::` directive for product-photo galleries
    # rather than hijacking every `.. image::`/`.. figure::` on the site.
    "override_image_directive": False,
    "default_image_width": "100%",
}
# Weekly link check (.github/workflows/linkcheck.yml). These hosts reject
# automated requests, so their links must be checked by hand.
linkcheck_ignore = [
    r"https?://<",  # placeholder URLs such as http://<target_ip>:8080/
    r"https://www\.nxp\.(com|jp)/",
    r"https://community\.nxp\.com/",
    r"https://wiki\.linuxfoundation\.org/",
    r"https://(www|wiki)\.st\.com/",
]
linkcheck_timeout = 30
linkcheck_retries = 2

html_logo ="_static/cargt-logo-full-color.svg"  # Path relative to the docs directory
html_favicon = "_static/favicon.ico"
templates_path = ["_templates"]
copyright = "2026, Cargt Inc"
html_theme = "sphinx_rtd_theme" # Read the Docs theme
html_title = "Cargt Developer Documentation"
html_theme_options = {
     'style_nav_header_background': "#F7F9FA",  # Light Gray - keeps the dark-green
                                                 # logo mark and black wordmark legible;
                                                 # the nav menu below stays Kaitoke Green
     'logo_only': True,
     'style_external_links': True,
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
