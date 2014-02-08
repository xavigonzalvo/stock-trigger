"""Defines a server to generate weekly reports."""

import gae_setup  # Needs to be first

import urllib

from google.appengine.ext import deferred
from google.appengine.api import mail
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
        self.good_symbols = {}
        self.good_symbols['hard'] = []
        self.good_symbols['medium'] = []
        self.report_date = None
        self.count_correct_analysis = 0
        self.count_total = 0

    def FilterSymbols(self, hard_data_filter, medium_data_filter):
        """Filters symbols using filters. Uses the last date stored in
        report as the reference to pick values from stored symbols"""
        report = ndb_data.ReportProperty.query().get()
        self.report_date = report.last

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


class BestStocksReport(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write('Producing report ...<br><br>')

        hard_data_filter = filter_pb2.Filter()
        gae_utils.ReadTextProto('filters/hard.ascii_proto', hard_data_filter)
        medium_data_filter = filter_pb2.Filter()
        gae_utils.ReadTextProto('filters/medium.ascii_proto', medium_data_filter)
        
        processor = SymbolProcessor()
        processor.FilterSymbols(hard_data_filter, medium_data_filter)
        report_html = processor.CreateReport()
        SendReport(report_html)

        self.response.write(report_html)
        self.response.write('<br>Finished')


application = webapp2.WSGIApplication([
    ('/cron/weekly_best_stocks_report', BestStocksReport),
], debug=True)
