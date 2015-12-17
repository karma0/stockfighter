#/usr/bin/env python3

from itertools import repeat
from statistics import mean, variance
import time

from .exchange import Market
from .utils import *

def get_top_ask(config):
  mkt = Market(config)
  quote = mkt.quote()
  if quote:
    if 'ask' in quote and quote['ask'] > 0:
      return quote['ask']
    else:
      print("No orderbook data...?")
      print(json.dumps(book, indent=2))
      return 1 # Bid a penny ... why not?
  return None

def get_top_bid(config):
  mkt = Market(config)
  book = mkt.orderbook()
  #print(json.dumps(book, indent=2))
  if book:
    if 'asks' in book and book['asks'] and len(book['asks']) > 0:
      return book['asks'][0]['price']
    else:
      print("No orderbook data...?")
      print(json.dumps(book, indent=2))
      return 1 # Bid a penny ... why not?
  return None

def find_spread():
  book = orderbook()
  if book:
    if 'asks' in book and book['asks'] and len(book['asks']) > 0 and \
       'bids' in book and book['bids'] and len(book['bids']) > 0:
      return {'bids': book['bids'], 'asks': book['asks']}
    else:
      print("No orderbook data...?")
      print(json.dumps(book, indent=2))
      return 1 # Bid a penny ... why not?
  return None

def sample(sample_size=10):
  print("Sampling {} top asks".format(sample_size), end="")

  samples = []
  for i in repeat(None, sample_size):
    samples.append(get_top_asking())
    print(".", end="", flush=True)
    time.sleep(CONF['dayrate'])
  print()

  m = mean(samples)
  print("Sampled mean: {}".format(m))
  var = variance(samples, m)
  print("Sampled variance: {}".format(var))
  return m, var

def check_unfulfilled(order, max_trys=20, depth=1):
  print("Checking unfulfilled.")
  if not order['ok']:
    print("Order NOT OK")
    print(json.dumps(order, indent=2))
    return

  if order['opened']:
    time.sleep(CONF['dayrate'])
    check_unfulfilled(answer, depth=depth+1)
    return answer['totalFilled']
  else:
    return answer['totalFilled']

def mass_order(quantity, max_ask=1000, amount=None):
  if not amount:
    (amount, var) = sample() # amount == mean of sampled max value for asks
    if var > 2:
      print("Variance is running a little high: {}".format(var))

  ask_avg = [var]
  left = quantity
  while left > 0:
    qty = max_ask if left > max_ask else left
    answer = ask(amount, qty)
    if not answer: break
    less = check_unfulfilled(answer)
    if not less: break
    left -= less
    # Verify that we're not driving the price up
    (new_amount, v) = sample()
    ask_avg.append(v)
    while new_amount - amount > mean(ask_avg):
      time.sleep(10)
      (new_amount, v) = sample()
      ask_avg.append(v)

  if left > 0:
    print("A problem seems to have occurred.")

#CONF['account'] = 'SA85997409'
#CONF['venue'] = 'OKMPEX'
#CONF['tick'] = 'LMC'

#level = start_level('chock_a_block')
#print(json.dumps(level, indent=2))
#mass_order(100000, max_ask=300)

