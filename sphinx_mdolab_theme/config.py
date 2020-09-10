# -- Project information -----------------------------------------------------
copyright = "2020, MDO Lab"

# -- General configuration -----------------------------------------------------

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ["_build"]

# The master toctree document.
master_doc = "index"

# -- Options for HTML output ---------------------------------------------------

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_context = {
    "css_files": [
        "_static/theme_overrides.css",  # override wide tables in RTD theme
    ],
}
