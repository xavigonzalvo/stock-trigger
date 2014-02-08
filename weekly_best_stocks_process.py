"""Defines a server to process stocks."""

import gae_setup  # Needs to be first

import datetime
import cgi
import StringIO
import logging

from google.appengine.ext import deferred
from google.appengine.ext import ndb
import curve_fitting_numpy
import ndb_data
import gae_utils
import yahoo_finance_fetcher as YFetcher
import weeks_processor
import week_result_pb2
import webapp2


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
    (percentual_change, week_values, mean, std, mean_value) = processor.Process()
    rev_week_values = week_values[::-1]
    fitter = curve_fitting_numpy.CurveFittingNumpy(rev_week_values)

    # Store result.
    result = week_result_pb2.WeekResult()
    result.mean = mean
    result.std = std
    result.name = symbol
    result.mean_value = mean_value

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
    current_date = datetime.datetime.now()
    report_info = ndb_data.ReportsProperty.query().get()
    if not report_info:
        report_info = ndb_data.ReportsProperty()
    report_info.last = current_date
    report_info.put()
    for symbol in symbols:
        deferred.defer(Worker, symbol, current_date, period, current_year,
                       from_year, period_type)


class BestStocksProcess(webapp2.RequestHandler):

    def get(self):        
        self.response.headers['Content-Type'] = 'text/plain'

        test = self.request.get('test')
        if test:
            num = int(cgi.escape(self.request.get('test')))
            symbols = gae_utils.SafeReadLines('config/symbols_test%d' % num)
        else:
            symbols = gae_utils.SafeReadLines('config/symbols_little')
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
                       from_year, period_type)


application = webapp2.WSGIApplication([
    ('/cron/weekly_best_stocks_process', BestStocksProcess),
], debug=True)
