import requests
from ..utils import *
from .utils import validate

class Game:
  def __init__(self, config, level, method="POST", base_url=None):
    self._method = method
    self._conf = config
    self._root_path = config['gm_url']
    self.instance_id = config['levelInstances'][level]
    self.level = level

  def _get_headers(self, hdrs=None):
    if not hdrs:
      hdrs = {}
    if not 'Cookie' in hdrs:
      hdrs['Cookie'] = 'api_key='+self._conf['gm_apikey']
    return hdrs

  def fetch(self, path='', config=None, hdrs=None, data=None, method=None, root=None):
    """Basic fetch from API"""
    config = config if not config is None else self._conf
    method = method if not method is None else self._method
    root = root if not root is None else self._root_path

    hdrs = self._get_headers()

    if method == "GET":
      return validate(requests.get(root+path, data=data, headers=hdrs))
    elif method == "POST":
      return validate(requests.post(root+path, data=data, headers=hdrs))

  def restart_level(self):
    resp = self.fetch(path="/instances/{}/restart".format(self.instance_id))
    if not resp:
      print("A problem occurred while attempting to restart level.")
    return resp

  def stop_level(self):
    resp = self.fetch(path="/instances/{}/stop".format(self.instance_id))
    if not resp:
      print("A problem occurred while attempting to restart level.")
    return resp

  def start_level(self):
    level = self.fetch(path="/levels/{}".format(self.level))
    print("Retrieved level: ")
    pdump(level)
    if level and 'ok' in level:
      if level['ok']:
        self._conf['instanceId'] = level['instanceId']
        self._conf['dayrate'] = level['secondsPerTradingDay']
        self._conf['account'] = level['account']
        self._conf['venues'] = level['venues']
        self._conf['tickers'] = level['tickers']
        self._conf['venue'] = level['venues'][0]
        self._conf['stock'] = level['tickers'][0]
      return level
    else: return None

  def resume_level(self):
    level = \
      self.fetch(path="/instances/{}/resume".format(self.instance_id))
    if level and 'ok' in level:
      if level['ok']:
        self._conf['instanceId'] = level['instanceId']
        self._conf['dayrate'] = level['secondsPerTradingDay']
        self._conf['account'] = level['account']
        self._conf['venues'] = level['venues']
        self._conf['tickers'] = level['tickers']
        self._conf['venue'] = level['venues'][0]
        self._conf['stock'] = level['tickers'][0]
      return level
    else: return None

  def level_status(self):
    status = \
      self.fetch(path="/instances/{}".format(self.instance_id), method='GET')
    if status and 'ok' in status and status['ok']:
      pdump(status)
    return status

