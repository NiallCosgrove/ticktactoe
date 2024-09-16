import os
import sys
sys.path.insert(0, os.path.abspath('../'))  # Adjust path to point to repo root

# Sphinx configuration
project = 'TickTacToe'
author = 'Niall Cosgrove'
extensions = ['myst_parser', 'sphinx.ext.autodoc']
templates_path = ['_templates']
exclude_patterns = []

# HTML output options
html_theme = 'alabaster'
html_static_path = ['_static']

