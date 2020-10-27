# -- Project information -----------------------------------------------------
copyright = "2020, MDO Lab"

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
]

# tell autoclass to document the __init__ methods
autoclass_content = "both"

# if using numpydoc, this hides a bunch of warnings
numpydoc_show_class_members = False 

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = "sphinx_mdolab_theme"

html_theme_options = {
#     "titles_only": True, # hide headings from the sidebar, only show separate pages
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_context = {
    "css_files": [
        "_static/theme_overrides.css",  # override wide tables in RTD theme
    ],
}
