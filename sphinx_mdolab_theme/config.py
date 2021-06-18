import os
from .ext.optionslist import TEMP_FILE

# -- Project information -----------------------------------------------------
copyright = "2021, MDO Lab"

# -- General configuration -----------------------------------------------------

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ["_build"]

# The master toctree document.
master_doc = "index"

# -- Options for HTML output ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "numpydoc",
    "sphinx-prompt",
    "sphinxcontrib.bibtex",
    "sphinxcontrib.autoprogram",
    "sphinx_copybutton",
    "sphinx_mdolab_theme.ext.optionstable",
    "sphinx_mdolab_theme.ext.optionslist",
]

# tell autoclass to document the __init__ methods
autoclass_content = "both"
# disable showing type annotations for now
autodoc_typehints = "none"

# if using numpydoc, this hides a bunch of warnings
numpydoc_show_class_members = False

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = "sphinx_mdolab_theme"

html_theme_options = {
    #     "titles_only": True, # hide headings from the sidebar, only show separate pages
}

# This is the MDO Lab logo
# A default version is provided by the package but this parameter can be overwritten to use
# a custom logo for a specific documentation site
html_logo = os.path.join(os.path.dirname(__file__), "static/MDO_Lab_logo_RTD.png")

# this is required for sphinxcontrib.bibtex
bibtex_bibfiles = []

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    TEMP_FILE,  # this is a temporary file used by the optionslist extension we exclude it here
    "_build",
    "Thumbs.db",
    ".DS_Store",
]


def setup(app):
    app.add_css_file("theme_overrides.css")
