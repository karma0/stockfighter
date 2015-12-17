from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
  long_description = f.read()

setup(
  name = 'stockfighter-io',
  packages = find_packages(exclude=['dist']),
  version = '0.1.4',
  description = 'An API wrapper for Stockfighter.io',
  author = 'Bobby Larson',
  author_email = 'karma0@gmail.com',
  url = 'https://github.com/karma0/stockfighter',
  download_url = 'https://github.com/karma0/stockfighter/tarball/0.1',
  keywords = ['stockfighter', 'exchange', 'trades'],
  classifiers = [],
  install_requires = [
    'requests',
    'ws4py'
  ],
)
