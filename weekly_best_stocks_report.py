"""Defines a server to generate weekly reports."""

import gae_setup  # Needs to be first

import urllib

from google.appengine.ext import deferred
from google.appengine.api import mail
from google.appengine.datastore.datastore_query import Cursor
import filter_utils
import filter_pb2
import gae_config
import gae_utils
import ndb_data
import week_result_pb2
import webapp2


class SymbolProcessor(object):
    """Class to handle symbols, filter and generating reports."""

    def __init__(self):
        self.report_date = None
        self.good_symbols = {}
        self.good_symbols['hard'] = []
        self.good_symbols['medium'] = []
        self.count_correct_analysis = 0
        self.count_total = 0

    def Save(self):
        """Saves a report."""
        report_ndb = ndb_data.ReportProperty()
        report_ndb.date = self.report_date
        report_ndb.hard_good_symbols = self.good_symbols['hard']
        report_ndb.medium_good_symbols = self.good_symbols['medium']
        report_ndb.count_correct_analysis = self.count_correct_analysis
        report_ndb.count_total = self.count_total
        report_ndb.put()

    def Load(self, date):
        # TODO(xavigonzalvo): load by date.
        pass

    def FilterSymbols(self, date,hard_data_filter, medium_data_filter):
        """Filters symbols using filters. Uses the last date stored in
        report as the reference to pick values from stored symbols"""
        self.report_date = date

        symbols = ndb_data.SymbolProperty.query()
        self.count_correct_analysis = 0
        self.count_total = 0
        for symbol in symbols:
            for analysis in symbol.analysis:
                if analysis.date != self.report_date:
                    continue            
                self.count_correct_analysis += 1
                data = week_result_pb2.WeekResult()
                data.ParseFromString(analysis.data)
                
                if not filter_utils.Filter(data, hard_data_filter):
                    self.good_symbols['hard'].append(data.name)
                if not filter_utils.Filter(data, medium_data_filter):
                    self.good_symbols['medium'].append(data.name)
                break
            self.count_total += 1

    def _GenerateSymbolReport(self, symbols):
        """Returns a list of HTML lines with a link to each symbol."""
        html_lines = []
        _HTML_PART = '<a href="%s?q=%s&ei=HejzUoiYBavGwAPk8gE">%s</a><br>'
        for symbol in symbols:
            url_symbol = urllib.quote('LON:%s' % symbol.replace('.L',''))
            html_lines.append(_HTML_PART % (gae_config.WEB_FINANCE, url_symbol,
                                            symbol))
        return html_lines

    def SetReport(self, report):
        self.date = report.date
        self.good_symbols['hard'] = report.hard_good_symbols
        self.good_symbols['medium'] = report.medium_good_symbols
        self.count_correct_analysis = report.count_correct_analysis
        self.count_total = report.count_total

    def CreateSummary(self, report):
        return '%s' % report.date

    def CreateReport(self):
        """Generates an HTML report given good symbols."""
        hard_part = self._GenerateSymbolReport(self.good_symbols['hard'])
        medium_part = self._GenerateSymbolReport(self.good_symbols['medium'])            
    
        hard_msg_symbols_html = ['%s<br>' % symbol for symbol in hard_part]
        medium_msg_symbols_html = ['%s<br>' % symbol for symbol in medium_part]
        msg_html = """<h2>Stats</h2>
                      <p>Date: %s<br>
                      count_total = %d<br>
                      count_correct_analysis = %d</p>
                      <h2>Hard filtered symbols</h2><p>%s</p>
                      <h2>Medium filtered symbols</h2><p>%s</p>""" % (
            self.report_date,
            self.count_total,
            self.count_correct_analysis,
            "".join(hard_msg_symbols_html),
            "".join(medium_msg_symbols_html))    
        return msg_html


def SendReport(report_html):
    message = mail.EmailMessage(sender=gae_config.SENDER_MAIL,
                                to=gae_config.MAILS,
                                subject=gae_config.WEEKLY_REPORT_SUBJECT)
    message.html = report_html
    message.send()


class StocksReport(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        # Print one report.
        report_date = self.request.get('date')
        if report_date:
            self.response.write('<p>Not implemented yet</p>')
            # TODO(xavigonzalvo): load a report on a date
            return

        # List of reports.
        self.response.write('<h1>Reports</h1>')
        curs = Cursor(urlsafe=self.request.get('cursor'))
        reports, next_curs, more = ndb_data.ReportProperty.query().fetch_page(10, start_cursor=curs)  #.order(report.last)
        processor = SymbolProcessor()
        for report in reports:
            self.response.write('<p><a href="/stocks_report?date=%s">%s</a></p>' %
                                (report.date, processor.CreateSummary(report)))
        if more and next_curs:
            self.response.out.write('<a href="/stocks_report?cursor=%s">More...</a>' %
                                    next_curs.urlsafe())

        
class LastStocksReport(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write('Producing report ...<br><br>')

        # Generate report.
        report_info = ndb_data.ReportsProperty.query().get()
        self.response.write('<h1>Report</h1>')
        hard_data_filter = filter_pb2.Filter()
        gae_utils.ReadTextProto('filters/hard.ascii_proto', hard_data_filter)
        medium_data_filter = filter_pb2.Filter()
        gae_utils.ReadTextProto('filters/medium.ascii_proto',
                                medium_data_filter)
        
        processor = SymbolProcessor()
        processor.FilterSymbols(report_info.last, hard_data_filter,
                                medium_data_filter)
        processor.Save()
        report_html = processor.CreateReport()
        SendReport(report_html)

        self.response.write(report_html)
        self.response.write('<br>Finished')


application = webapp2.WSGIApplication([
    ('/cron/weekly_best_stocks_report', LastStocksReport),
    ('/stocks_report', StocksReport),
], debug=True)
