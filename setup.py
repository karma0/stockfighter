from setuptools import setup, find_packages

setup(
  name = 'stockfighter-io',
  packages = find_packages(exclude=['dist']),
  version = '0.1.8',
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
