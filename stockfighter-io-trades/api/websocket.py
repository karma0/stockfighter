from ws4py.client.threadedclient import WebSocketClient
import time

class WebSock(WebSocketClient):
  def __init__(self, config, output=print):
    self.url = self.url.format(**config)
    super(WebSock, self).__init__(self.url, protocols=['http-only', 'chat'])
    self.call = output

  def received_message(self, message):
    self.call(message)

  def closed(self):
    print("### closed ###")

  def opened(self):
    print("Opened websocket")

class Executions(WebSock):
  url = "{root_ws}/{account}/venues/{venue}/executions"

class StockExecutions(WebSock):
  url = "{root_ws}/{account}/venues/{venue}/executions/stocks/{stock}"

class Quotes(WebSock):
  url = "{root_ws}/{account}/venues/{venue}/tickertape"

class StockQuotes(WebSock):
  url = "{root_ws}/{account}/venues/{venue}/tickertape/stocks/{stock}"

if __name__ == "__main__":
  conf = {
    'root_ws':'wss://www.stockfighter.io/ob/api/ws',
    'venue': 'TESTEX',
    'stock': 'FOOBAR',
    'account': 'EXB123456'
  }
  try:
    e = Quotes(conf)
    e.connect()
    e.run_forever()
  except:
    e.close()

