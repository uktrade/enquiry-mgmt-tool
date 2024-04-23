# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import re
import sys

import django

sys.path[0:0] = [
    os.path.abspath('.'),
    os.path.abspath('../../'),
]

os.environ['DJANGO_SETTINGS_MODULE'] = 'app.settings.djangotest'
django.setup()

# -- Project information -----------------------------------------------------

project = 'Enquiry Management'
copyright = '2020, FIXME, provide author names'
author = 'FIXME, provide author names'

# The full version, including alpha/beta/rc tags
release = '1.0.0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "celery.contrib.sphinx",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    # 'canonical_url': '',
    # 'logo_only': False,
    # 'display_version': True,
    # 'prev_next_buttons_location': 'bottom',
    # 'style_external_links': False,
    # 'vcs_pageview_mode': '',
    # 'style_nav_header_background': 'white',
    # Toc options
    # 'collapse_navigation': True,
    # 'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# The link substitutions, are defined in the README for it to work on GitHub,
# we extract everything after the ".. rst_prolog" comment from the README
# so the substitutions work everywhere, including docstrings. Due to this,
# the doc compilation shows "Duplicate substitution definition" warnings.
rst_prolog = re.search(r'rst_prolog.*?$(.*)',
                       open('../../README.rst').read(),
                       re.MULTILINE | re.DOTALL).group(1)

intersphinx_mapping = {
    "python": ("https://docs.python.org/3.12", None),
    "django": (
        "https://docs.djangoproject.com/en/dev/",
        "https://docs.djangoproject.com/en/dev/_objects/",
    ),
    "requests": (
        "https://requests.readthedocs.io/en/master/",
        "https://requests.readthedocs.io/en/master/objects.inv",
    ),
    "mohawk": (
        "https://mohawk.readthedocs.io/en/latest/",
        "https://mohawk.readthedocs.io/en/latest/objects.inv",
    ),
}

autodoc_inherit_docstrings = False
