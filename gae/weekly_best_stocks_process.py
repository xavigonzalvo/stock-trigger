"""Defines a server to process stocks.

The MIT License (MIT)

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import datetime
import cgi
import logging
import time

from google.appengine.ext import deferred
from google.appengine.ext import ndb
from app_reports_accessor import AppReportsAccessor
from app_symbol_accessor import AppSymbolAccessor
from days_processor import DaysProcessor
from finance_fetcher_factory import FinanceFetcherFactory
import gae_config
import gae_utils
import webapp2


def _worker_fn(finance_fetcher, symbol, current_date, fetch_period,
               process_period, process_window):
  try:
    time.sleep(0.5)
    data = finance_fetcher.get_historical(symbol, fetch_period)
  except Exception, e:
    logging.error("Symbol %s couldn't be processed: %s", symbol, e)
    return

  if not data:
    logging.error('No data retrieved for symbol %s', symbol)
    return

  # Fit model.
  processor = DaysProcessor(data, process_period, process_window, symbol)
  result = processor.poly_model()

  market_cap = finance_fetcher.get_market_cap(symbol)
  if market_cap:
    result["market_cap"] = market_cap

  # Save symbol.
  symbol_accessor = AppSymbolAccessor()
  symbol_accessor.load(symbol)
  symbol_accessor.add_analysis(current_date, result)
  symbol_accessor.save()


def _process_symbols_fn(symbols, fetch_period, process_period, process_window):
  """Processes information of all symbols and stores each one."""
  current_date = datetime.datetime.now()
  reports = AppReportsAccessor()
  reports.add_new_report(current_date)
  finance_fetcher = FinanceFetcherFactory.create()
  for symbol in symbols:
    deferred.defer(_worker_fn, finance_fetcher, symbol, current_date,
                   fetch_period, process_period, process_window)


class BestStocksProcess(webapp2.RequestHandler):

    def get(self):
      self.response.headers['Content-Type'] = 'text/html'

      test = self.request.get('test')
      if test:
        num = int(cgi.escape(self.request.get('test')))
        symbols = gae_utils.SafeReadLines('config/symbols.test%d' % num)
      else:
        symbols = gae_utils.SafeReadLines('config/symbols_weekly')

      fetch_period = self.request.get('fetch_period')
      if not fetch_period:
        fetch_period = '3m'
      process_period = self.request.get('process_period')
      if not process_period:
        process_period = '40'
      process_window = self.request.get('process_window')
      if not process_window:
        process_window = '3'

      self.response.write('<p>Processing %d symbols</p>' % len(symbols))
      self.response.write('<p>Fetch period: %s</p>' % fetch_period)
      self.response.write('<p>Process period: %s</p>' % process_period)
      self.response.write('<p>Process window: %s</p>' % process_window)
      self.response.write('<br><p><a href="/">Home</a></p>')

      deferred.defer(_process_symbols_fn, symbols, fetch_period,
                     int(process_period), int(process_window))


application = webapp2.WSGIApplication([
    ('/cron/weekly_best_stocks_process', BestStocksProcess),
], debug=True)
