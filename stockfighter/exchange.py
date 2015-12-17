from .api.exchange import Exchange
from .utils import dump, pdump


# EXCHANGE

class Market:
  def __init__(self, config):
    self._conf = config

  def api_is_up(self):
    ex = Exchange(self._conf)
    r = ex.heartbeat()
    if r and 'ok' in r:
      return r['ok']
    return False

  def venue_is_up(self):
    ex = Exchange(self._conf)
    r = ex.venue_heartbeat()
    if r and 'ok' in r:
      return r['ok']
    return False

  def stocks(self):
    ex = Exchange(self._conf, method='GET')
    resp = ex.venue_fetch('/stocks')
    if resp and 'symbols' in resp:
      return [ s['symbol'] for s in resp['symbols'] ]
    return resp

  def orderbook(self):
    ex = Exchange(self._conf, method='GET')
    return ex.stock_fetch()

  def quote(self):
    ex = Exchange(self._conf, method='GET')
    return ex.fetch('/quote')

  def ask(self, cost, quantity, direction="sell", order_type='limit'):
    ex = Exchange(self._conf)
    order = {
      "account" : self._conf['account'],
      "venue" : self._conf['venue'],
      "stock" : self._conf['stock'],
      "price" : abs(cost),
      "qty" : quantity,
      "direction" : direction,
      "orderType" : order_type
    }
    return ex.fetch("/orders", data=order, method='POST')

  def bid(self, cost, quantity, order_type='limit'):
    return self.ask(cost, quantity, "buy", order_type)

  def status(self, oid):
    ex = Exchange(self._conf)
    return ex.fetch("/orders/{}".format(oid), method='GET')

  def cancel(self, oid):
    ex = Exchange(self._conf)
    return ex.fetch("/orders/{}".format(oid), method='DELETE')

