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


def CreateReport(hard_data_filter, medium_data_filter):
    report = ndb_data.ReportProperty.query().get()
    symbols = ndb_data.SymbolProperty.query()
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
            
            if not filter_utils.Filter(data, hard_data_filter):
                hard_good_symbols.append(data.name)
                url_symbol = urllib.quote('LON:%s' % data.name.replace('.L',''))
                hard_good_symbols_html.append(
                    '<a href="%s?q=%s&ei=HejzUoiYBavGwAPk8gE">%s</a><br>' % (
                        gae_config.WEB_FINANCE, url_symbol, data.name))
            if not filter_utils.Filter(data, medium_data_filter):
                medium_good_symbols.append(data.name)
                url_symbol = urllib.quote('LON:%s' % data.name.replace('.L',''))
                medium_good_symbols_html.append(
                    '<a href="%s?q=%s&ei=HejzUoiYBavGwAPk8gE">%s</a><br>' % (
                        gae_config.WEB_FINANCE, url_symbol, data.name))
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
    message = mail.EmailMessage(sender=gae_config.SENDER_MAIL,
                                to=gae_config.MAILS,
                                subject=gae_config.WEEKLY_REPORT_SUBJECT)
    message.body = report
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

        report, report_html = CreateReport(hard_data_filter, medium_data_filter)
        SendReport(report, report_html)
        self.response.write(report_html)
        self.response.write('<br>Finished')


application = webapp2.WSGIApplication([
    ('/cron/weekly_best_stocks_report', BestStocksReport),
], debug=True)
