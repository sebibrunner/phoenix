"""
Configuration file for the Sphinx documentation builder.

This file only contains a selection of the most common options. For a full
list see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

# -- Path setup --------------------------------------------------------------

import os
import sys

import phoenix

# Path setup for autodoc
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(BASE_DIR, "src", "phoenix"))
sys.path.insert(0, os.path.join(BASE_DIR, "packages", "phoenix-evals", "src", "phoenix"))
sys.path.insert(0, os.path.join(BASE_DIR, "packages", "phoenix-otel", "src", "phoenix"))


# -- Generation setup --------------------------------------------------------


def clean_doc_output(app, docname, source):
    """
    Process .rst sources generated by autodoc to remove unwanted text outside
    automodule blocks and adjust formatting for Sphinx.
    """

    if source:
        processed, in_automodule = [], False
        for line in source[0].split("\n"):
            # Check for the start of the automodule block
            if ".. automodule::" in line:
                in_automodule = True

            # Check if we are still in the automodule block
            if in_automodule and line.strip() == "":
                processed.append(line)
                continue

            # Check if we are out of the automodule block
            if in_automodule and line.strip() and not line.startswith("   "):
                in_automodule = False

            # Clean up text outside automodule blocks
            if not in_automodule:
                if "Submodules" in line:
                    continue
                if "package" in line:
                    line = line.replace(" package", "")
                if "module" in line:
                    line = line.replace(" module", "")
                if "Subpackages" in line:
                    line = line.replace("Subpackages", "")

            processed.append(line)

        source[0] = "\n".join(processed)


def setup(app):
    app.add_css_file("custom.css")
    app.add_js_file("custom.js")
    app.connect("source-read", clean_doc_output)  # Remove unnecessary headers


# -- Project information -----------------------------------------------------

project = "Phoenix API Reference"
copyright = "2024, Arize AI"
author = "Arize AI"

# -- General configuration ---------------------------------------------------

source_suffix = [".rst", ".md", ".txt"]

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "myst_parser",
    "sphinx_design",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files
# and directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

add_module_names = False

# -- Extension configuration -------------------------------------------------

# Napoleon
napoleon_google_docstring = True
napoleon_numpy_docstring = True

# Autosummary
autosummary_generate = True  # Generate API documentation when building

# MyST
# This allows us to use ::: to denote directives, useful for admonitions
myst_enable_extensions = ["colon_fence", "linkify", "substitution"]
myst_heading_anchors = 2
myst_substitutions = {"rtd": "[Read the Docs](https://readthedocs.org/)"}

# Autodoc
# autodoc_class_signature = 'separated'  # Separate the signature from the class title
autoclass_content = "class"  # Only include the class docstring, not the __init__ method docstring
autodoc_typehints = "none"
add_function_parentheses = False
add_module_names = False
autodoc_preserve_defaults = True
autodoc_typehints_description_target = "documented_params"

autodoc_default_options = {
    "members": True,
    "private-members": False,
    "special-members": "",
    "undoc-members": False,
    "inherited-members": False,
    "show-inheritance": False,
}

# -- Internationalization ----------------------------------------------------

# specifying the natural language populates some key tags
language = "en"

# -- Versioning --------------------------------------------------------------

json_url = "https://arize-phoenix.readthedocs.io/en/latest/_static/switcher.json"

# Based off the pydata theme config file:
# https://github.com/pydata/pydata-sphinx-theme/blob/main/docs/conf.py

# Define the version we use for matching in the version switcher.
version_match = os.environ.get("READTHEDOCS_VERSION")
release = phoenix.__version__

# If READTHEDOCS_VERSION doesn't exist, we're not on RTD
# If it is an integer, we're in a PR build and the version isn't correct.
# If it's "latest" → change to "dev" (that's what we want the switcher to call it)
if not version_match or version_match.isdigit() or version_match == "stable":
    version_match = f"v{release}"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_js_files = ["custom.js"]
html_show_sphinx = False
# html_favicon = "favicon.ico"
# pygments_style = "sphinx"  # Name of the Pygments (syntax highlighting) style to use.

html_theme_options = {
    "logo": {
        "text": "Phoenix API",
        "image_light": "logo.png",
        "image_dark": "logo.png",
    },
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/Arize-ai/phoenix",
            "icon": "fa-brands fa-github",
        },
        {
            "name": "Twitter",
            "url": "https://x.com/ArizePhoenix",
            "icon": "fa-brands fa-twitter",
        },
    ],
    "external_links": [
        {"name": "Docs", "url": "https://docs.arize.com/phoenix"},
    ],
    "navbar_align": "content",
    "navbar_start": ["navbar-logo", "version-switcher"],
    "switcher": {
        "json_url": json_url,
        "version_match": version_match,
    },
    "secondary_sidebar_items": [],
    "footer_start": [],
    "footer_end": ["copyright"],
    "navigation_depth": 3,
    "collapse_navigation": True,
}

html_sidebars = {
    "**": ["custom_sidebar.html"],
    "index": [],
}
