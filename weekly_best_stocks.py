from datetime import date
import StringIO

import urllib
import logging
import os
import sys

import google  # provided by GAE

# add vendorized protobuf to google namespace package
vendor_dir = os.path.join(os.path.dirname(__file__), 'vendor')
google.__path__.append(os.path.join(vendor_dir, 'google'))

# add vendor path
sys.path.insert(0, vendor_dir)

from google.protobuf import text_format
import curve_fitting_numpy
from google.appengine.ext import deferred
from google.appengine.ext import ndb
import webapp2
from google.appengine.api import mail
import yahoo_finance_fetcher as YFetcher
import weeks_processor
import filter
import filter_pb2
import week_result_pb2


_SENDER_MAIL = 'xavigonzalvo@gmail.com'
_MAILS = ['xavigonzalvo@gmail.com, ele.barquero@gmail.com']
_WEEKLY_REPORT_SUBJECT = 'Weekly report'
_WEB_FINANCE = 'https://www.google.co.uk/finance'


class ReportProperty(ndb.Model):
    last = ndb.DateProperty()


class AnalysisProperty(ndb.Model):
    date = ndb.DateProperty()
    data = ndb.BlobProperty()  # serialized protobuf


class SymbolProperty(ndb.Model):
    name = ndb.StringProperty()
    analysis = ndb.StructuredProperty(AnalysisProperty, repeated=True)


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

    symbol_db = SymbolProperty.query(SymbolProperty.name == symbol).get()
    analysis_db = AnalysisProperty(date=current_date,
                                   data=result.SerializeToString())
    if not symbol_db:
        symbol_db = SymbolProperty(name=symbol, analysis=[analysis_db])
    else:
        symbol_db.analysis.append(analysis_db)
    symbol_db.put()


def ProcessSymbols(symbols, period, current_year, from_year, period_type):
    current_date = date.today()
    ReportProperty(last = current_date).put()
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


def CreateReport(hard_data_filter, medium_data_filter):
    report = ReportProperty.query().get()
    symbols = SymbolProperty.query()
    count_correct_analysis = 0
    count_total = 0
    hard_good_symbols = []
    hard_good_symbols_html = []
    medium_good_symbols = []
    medium_good_symbols_html = []
    for symbol in symbols:
        for analysis in symbol.analysis:
            if analysis.date != report.last:
                continue            
            count_correct_analysis += 1
            data = week_result_pb2.WeekResult()
            data.ParseFromString(analysis.data)
            
            if not filter.Filter(data, hard_data_filter):
                hard_good_symbols.append(data.name)
                url_symbol = urllib.quote('LON:%s' % data.name.replace('.L',''))
                hard_good_symbols_html.append(
                    '<a href="%s?q=%s&ei=HejzUoiYBavGwAPk8gE">%s</a><br>' % (
                        _WEB_FINANCE, url_symbol, data.name))
            if not filter.Filter(data, medium_data_filter):
                medium_good_symbols.append(data.name)
                url_symbol = urllib.quote('LON:%s' % data.name.replace('.L',''))
                medium_good_symbols_html.append(
                    '<a href="%s?q=%s&ei=HejzUoiYBavGwAPk8gE">%s</a><br>' % (
                        _WEB_FINANCE, url_symbol, data.name))
            break
        count_total += 1

    msg = ['report last: %s' % report.last,
           'count_total = %d' % count_total,
           'count_correct_analysis = %d' % count_correct_analysis,
           ] + hard_good_symbols_html
    hard_msg_symbols_html = ['%s<br>' % symbol for symbol in hard_good_symbols_html]
    medium_msg_symbols_html = ['%s<br>' % symbol for symbol in medium_good_symbols_html]
    msg_html = """<h2>Stats</h2>
                  <p>Date: %s<br>
                  count_total = %d<br>
                  count_correct_analysis = %d</p>
                  <h2>Hard filtered symbols</h2><p>%s</p>
                  <h2>Medium filtered symbols</h2><p>%s</p>""" % (
        report.last,
        count_total, count_correct_analysis, "".join(hard_msg_symbols_html),
        "".join(medium_msg_symbols_html))    
    return '\n'.join(msg), msg_html


def SendReport(report, report_html):
    message = mail.EmailMessage(sender=_SENDER_MAIL, to=_MAILS,
                                subject=_WEEKLY_REPORT_SUBJECT)
    message.body = report
    message.html = report_html
    message.send()


def ReadTextProto(filename, proto):
    """Reads a protobuf in text mode."""
    with open(filename, 'r') as f:
        text_format.Merge(f.read(), proto)


class BestStocksReport(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write('Producing report ...<br><br>')

        hard_data_filter = filter_pb2.Filter()
        ReadTextProto('filters/hard.ascii_proto', hard_data_filter)
        medium_data_filter = filter_pb2.Filter()
        ReadTextProto('filters/medium.ascii_proto', medium_data_filter)

        report, report_html = CreateReport(hard_data_filter, medium_data_filter)
        SendReport(report, report_html)
        self.response.write(report_html)
        self.response.write('<br>Finished')


application = webapp2.WSGIApplication([
    ('/cron/weekly_best_stocks_process', BestStocksProcess),
    ('/cron/weekly_best_stocks_report', BestStocksReport),
], debug=True)
