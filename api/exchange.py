import requests
import json
from .utils import validate


class Exchange:
  def __init__(self, config, method="POST", base_url=None):
    self._method = method
    if config:
      self._conf = config
      self._root_path = config['api_url']
      self._venue_path = self._root_path + "/venues/{venue}".format(**config)
      self._stock_path = self._root_path + \
            "/venues/{venue}/stocks/{stock}".format(**config)
    else:
      self._base_url = base_url

  def _get_headers(self, hdrs=None):
    if not hdrs:
      hdrs = {}
    if not 'X-Starfighter-Authorization' in hdrs:
      hdrs['X-Starfighter-Authorization'] = self._conf['apikey']
    if not 'Cookie' in hdrs:
      hdrs['Cookie'] = 'apikey='+self._conf['gm_apikey']
    if not 'Content-type' in hdrs:
      hdrs['Content-type'] = 'application/json'
    if not 'Accept' in hdrs:
      hdrs['Accept'] = 'text/plain'
    return hdrs

  def fetch(self, path='', config=None, hdrs=None, data=None,
            method=None, root=None):
    """Basic fetch from API"""
    config = config if not config is None else self._conf
    method = method if not method is None else self._method
    root   = root if not root is None else self._stock_path
    url = root+path

    hdrs = self._get_headers()

    if 'debug' in self._conf and self._conf['debug']:
      print("""URL: {}
               Data: {}
               Headers: {}""".format(url, data, hdrs))

    if method == "GET":
      return validate(requests.get(url, data=data, headers=hdrs))
    elif method == "POST":
      return validate(requests.post(url, data=json.dumps(data), headers=hdrs))
    else:
      return validate(requests.request(method, url, data=json.dumps(data),
                                      headers=hdrs))


  def stock_fetch(self, path='', config=None, hdrs=None, data=None,
                  method=None, root=None):
    """Request something of the stock"""
    # Functionally, identical to fetch
    return self.fetch(path, config, hdrs, data, method, root=self._stock_path)

  def venue_fetch(self, path='', config=None, hdrs=None, data=None,
                  method=None, root=None):
    """Request something of the venue"""
    return self.fetch(path, config, hdrs, data, method, root=self._venue_path)

  def root_fetch(self, path='', config=None, hdrs=None, data=None,
                  method=None, root=None):
    """Request something of the API"""
    return self.fetch(path, config, hdrs, data, method, root=self._root_path)


  def venue_heartbeat(self):
    """Fetch exchange alive status"""
    return self.venue_fetch('/heartbeat', method='GET')

  def heartbeat(self):
    """Fetch alive status"""
    return self.root_fetch('/heartbeat', method='GET')

