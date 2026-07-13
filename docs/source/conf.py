# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

import os
import sys
sys.path.insert(0, os.path.abspath('../../src/pysas/'))


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'pySAS'
copyright = '2026, XMM Guest Observer Facility'
author = 'Ryan Tanner'
release = '2.5.2'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.napoleon',
              'sphinx.ext.viewcode',
              'sphinx_rtd_theme',
              'myst_parser']

templates_path = ['_templates']
exclude_patterns = []

source_suffix = {'.rst': 'restructuredtext',
                 '.md': 'markdown',
                }

# This should turn off including typehints in the function signatures in autodoc. That information is already in 
#  the docstring and can look extremely confusing
autodoc_typehints = 'none'
# This will make sure the classes aren't sorted in alphabetical order
autodoc_member_order = 'bysource'


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme' # 'alabaster'
html_static_path = ['_static']

