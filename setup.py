from distutils.core import setup
setup(
  name = 'stockfighter-io-trades',
  packages = ['stockfighter-io-trades'],
  version = '0.1.3',
  description = 'An API wrapper for the Stockfighter.io Trades.Exec() system.',
  author = 'Bobby Larson',
  author_email = 'karma0@gmail.com',
  url = 'https://github.com/karma0/stockfighter-io-trades',
  download_url = 'https://github.com/karma0/stockfighter-io-trades/tarball/0.1', # I'll explain this in a second
  keywords = ['stockfighter', 'exchange', 'trades'], # arbitrary keywords
  classifiers = [],
  install_requires = [
    'requests',
    'ws4py'
  ],
)
