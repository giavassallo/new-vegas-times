# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
import django


sys.path.insert(0, os.path.abspath('../../news_application'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'news_site.news_site.settings'

from django.conf import settings 

settings.DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': ':memory',
}

django.setup()


project = 'News_Application'
copyright = '2026, Gia V'
author = 'Gia V'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
