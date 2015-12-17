from distutils.core import setup
setup(
  name = 'stockfighter-io',
  packages = ['stockfighter'],
  version = '0.1.3',
  description = 'An API wrapper for Stockfighter.io',
  author = 'Bobby Larson',
  author_email = 'karma0@gmail.com',
  url = 'https://github.com/karma0/stockfighter-io-trades',
  download_url = 'https://github.com/karma0/stockfighter/tarball/0.1',
  keywords = ['stockfighter', 'exchange', 'trades'], # arbitrary keywords
  classifiers = [],
  install_requires = [
    'requests',
    'ws4py'
  ],
)
