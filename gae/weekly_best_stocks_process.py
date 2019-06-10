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

import json

import gae_setup

import datetime
import cgi
import StringIO
import logging

from google.appengine.ext import deferred
from google.appengine.ext import ndb
import ndb_data
import gae_config
import gae_utils
import finance_fetcher as FinanceFetcher
import weeks_processor
import webapp2


def Worker(symbol, current_date, period, current_year, from_year,
           period_type, test_mode):
  fetcher = FinanceFetcher.FinanceFetcher(
      api_key=gae_config.ALPHA_ADVANTAGE_API,
      iexcloud_token=gae_config.IEXCLOUD_TOKEN)
  try:
    data = fetcher.GetHistorical(symbol, from_year,
                                 current_year, period_type, test_mode)
  except FinanceFetcher.Error, e:
    logging.error('Symbol %s not found', symbol)
    return

  # Process CSV data.
  f = StringIO.StringIO(data)
  csv_data = weeks_processor.ProcessData(f)
  f.close()

  # Fit model.
  processor = weeks_processor.WeeksProcessor(csv_data, period, symbol)
  result = processor.PolynomialModel()

  market_cap = fetcher.GetMarketCap(symbol)
  if market_cap:
    result["market_cap"] = market_cap

  symbol_db = ndb_data.SymbolProperty.query(
      ndb_data.SymbolProperty.name == symbol).get()
  analysis_db = ndb_data.AnalysisProperty(date=current_date,
                                          data=json.dumps(result))
  if not symbol_db:
    symbol_db = ndb_data.SymbolProperty(name=symbol, analysis=[analysis_db])
  else:
    symbol_db.analysis.append(analysis_db)
  symbol_db.put()


def ProcessSymbols(symbols, period, current_year, from_year, period_type,
                   test_mode):
  current_date = datetime.datetime.now()
  report_info = ndb_data.ReportsProperty.query().get()
  if not report_info:
    report_info = ndb_data.ReportsProperty()
  report_info.last = current_date
  report_info.put()
  for symbol in symbols:
    deferred.defer(Worker, symbol, current_date, period, current_year,
                   from_year, period_type, test_mode)


class BestStocksProcess(webapp2.RequestHandler):

    def get(self):
      self.response.headers['Content-Type'] = 'text/plain'

      test = self.request.get('test')
      test_mode = False
      if test:
        num = int(cgi.escape(self.request.get('test')))
        if num == 2:
          test_mode = True
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

      deferred.defer(ProcessSymbols, symbols, period, current_year,
                     from_year, period_type, test_mode=False)


application = webapp2.WSGIApplication([
    ('/cron/weekly_best_stocks_process', BestStocksProcess),
], debug=True)
