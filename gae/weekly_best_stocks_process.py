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
import StringIO
import logging

from google.appengine.ext import deferred
from google.appengine.ext import ndb
from app_reports import AppReports
from app_symbol_accessor import AppSymbolAccessor
import gae_config
import gae_utils
import finance_fetcher as FinanceFetcher
import weeks_processor
import webapp2


def _worker_fn(symbol, current_date, period, current_year, from_year,
               period_type):
  fetcher = FinanceFetcher.FinanceFetcher(
      api_key=gae_config.ALPHA_ADVANTAGE_API,
      iexcloud_token=gae_config.IEXCLOUD_TOKEN)
  try:
    data = fetcher.get_historical(symbol, from_year,
                                  current_year, period_type)
  except FinanceFetcher.Error, e:
    logging.error("Symbol %s couldn't be processed", symbol)
    return

  # Process CSV data.
  f = StringIO.StringIO(data)
  csv_data = weeks_processor.ProcessData(f)
  f.close()

  # Fit model.
  processor = weeks_processor.WeeksProcessor(csv_data, period, symbol)
  result = processor.PolynomialModel()

  market_cap = fetcher.get_market_cap(symbol)
  if market_cap:
    result["market_cap"] = market_cap

  # Save symbol.
  symbol_accessor = AppSymbolAccessor()
  symbol_accessor.load(symbol)
  symbol_accessor.add_analysis(current_date, result)
  symbol_accessor.save()


def _process_symbols_fn(symbols, period, current_year, from_year, period_type):
  """Processes information of all symbols and stores each one."""
  current_date = datetime.datetime.now()
  reports = AppReports()
  reports.add_new_report(current_date)
  for symbol in symbols:
    deferred.defer(_worker_fn, symbol, current_date, period, current_year,
                   from_year, period_type)


class BestStocksProcess(webapp2.RequestHandler):

    def get(self):
      self.response.headers['Content-Type'] = 'text/plain'

      test = self.request.get('test')
      if test:
        num = int(cgi.escape(self.request.get('test')))
        symbols = gae_utils.SafeReadLines('config/symbols.test%d' % num)
      else:
        symbols = gae_utils.SafeReadLines('config/symbols_weekly')
      self.response.write('Processing %d symbols\n' % len(symbols))

      current_year = datetime.date.today().year
      from_year = self.request.get('from_year')
      if not from_year:
        from_year = current_year - 2
      period_type = self.request.get('period_type')
      if not period_type:
        period_type = 'w'
      period = self.request.get('period')
      if not period:
        period = 4  # for example, 4 weeks

      deferred.defer(_process_symbols_fn, symbols, period, current_year,
                     from_year, period_type)


application = webapp2.WSGIApplication([
    ('/cron/weekly_best_stocks_process', BestStocksProcess),
], debug=True)
