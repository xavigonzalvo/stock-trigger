"""Defines a server to process stocks."""

from datetime import date
import StringIO

import logging
import os
import sys

import google  # provided by GAE

# add vendorized protobuf to google namespace package
vendor_dir = os.path.join(os.path.dirname(__file__), 'vendor')
google.__path__.append(os.path.join(vendor_dir, 'google'))

# add vendor path
sys.path.insert(0, vendor_dir)

import curve_fitting_numpy
from google.appengine.ext import deferred
from google.appengine.ext import ndb
import webapp2
from google.appengine.api import mail
import yahoo_finance_fetcher as YFetcher
import weeks_processor
import week_result_pb2
import ndb_data


def SafeReadLines(filename):
    """Reads all lines from a file making.

    It makes sure there are no spaces at the beginning and end.
    """
    lines = []
    with open(filename) as f:
        for line in f.readlines():
            lines.append(line.strip())
    return lines


def Worker(symbol, current_date, period, current_year, from_year,
           period_type):    
    fetcher = YFetcher.YahooFinanceFetcher()
    try:
        data = fetcher.GetHistorical(symbol, from_year,
                                     current_year, period_type)
    except YFetcher.YahooFinanceFetcherError, e:
        logging.error('Symbol %s not found', symbol)
        return

    # Process CSV data.
    f = StringIO.StringIO(data)
    csv_data = weeks_processor.ProcessData(f)
    f.close()

    # Fit model.
    processor = weeks_processor.WeeksProcessor(csv_data, period)
    (percentual_change, week_values, mean, std) = processor.Process()
    rev_week_values = week_values[::-1]
    fitter = curve_fitting_numpy.CurveFittingNumpy(rev_week_values)

    # Store result.
    result = week_result_pb2.WeekResult()
    result.mean = mean
    result.std = std
    result.name = symbol

    (poly, _) = fitter.Linear()
    linear_poly = result.poly.add()
    linear_poly.order = 1
    linear_poly.coef.extend(list(poly))
    
    poly, error, convex = fitter.Quadratic()
    quadratic_poly = result.poly.add()
    quadratic_poly.order = 2
    quadratic_poly.coef.extend(list(poly))
    quadratic_poly.error = error
    quadratic_poly.convex = convex
    
    fetcher = YFetcher.YahooFinanceFetcher()
    market_cap = fetcher.GetMarketCap(symbol)
    if market_cap:
        result.market_cap = market_cap

    symbol_db = ndb_data.SymbolProperty.query(ndb_data.SymbolProperty.name == symbol).get()
    analysis_db = ndb_data.AnalysisProperty(date=current_date,
                                   data=result.SerializeToString())
    if not symbol_db:
        symbol_db = ndb_data.SymbolProperty(name=symbol, analysis=[analysis_db])
    else:
        symbol_db.analysis.append(analysis_db)
    symbol_db.put()


def ProcessSymbols(symbols, period, current_year, from_year, period_type):
    current_date = date.today()
    ndb_data.ReportProperty(last = current_date).put()
    for symbol in symbols:
        deferred.defer(Worker, symbol, current_date, period, current_year,
                       from_year, period_type)


class BestStocksProcess(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'

        test = self.request.get('test')
        if test:
            symbols = SafeReadLines('config/symbols_test')
        else:
            symbols = SafeReadLines('config/symbols_little')
        self.response.write('Processing %d symbols\n' % len(symbols))

        current_year = date.today().year
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
                       from_year, period_type)


application = webapp2.WSGIApplication([
    ('/cron/weekly_best_stocks_process', BestStocksProcess),
], debug=True)
