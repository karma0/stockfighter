from .api.exchange import Exchange
from .api.websockets import Quotes, Executions
from .utils import dump, pdump

import json

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

  def websocket(self, callback=pdump, on_error=None, objclass=Quotes):
    def process(m):
      if m.is_text:
        data = m.data.decode("utf-8")
        out = json.loads(data)
        if 'ok' in out and out['ok']:
          q = out['quote']
          callback(q)
    try:
      e = objclass(self._conf, process)
      e.connect()
      e.run_forever()
    except:
      if on_error:
        on_error()
    finally:
      e.close()

  def quotes(self, callback=pdump, on_error=None):
    self.websocket(callback, on_error, objclass=Quotes)

  def executions(self, callback=pdump, on_error=None):
    self.websocket(callback, on_error, objclass=Executions)

