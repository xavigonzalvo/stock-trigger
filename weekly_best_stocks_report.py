"""Defines a server to generate weekly reports."""

import gae_setup  # Needs to be first

from google.appengine.ext import deferred
from google.appengine.api import mail
import filter_pb2
import gae_config
import gae_utils
import gae_symbol_processor
import ndb_data
import webapp2
    

def SendReport(report_html):
    message = mail.EmailMessage(sender=gae_config.SENDER_MAIL,
                                to=gae_config.MAILS,
                                subject=gae_config.WEEKLY_REPORT_SUBJECT)
    message.html = report_html
    message.send()

        
class LastStocksReport(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write('<h1>Report</h1>')

        # Load filters.
        hard_data_filter = filter_pb2.Filter()
        gae_utils.ReadTextProto('filters/hard.ascii_proto', hard_data_filter)
        medium_data_filter = filter_pb2.Filter()
        gae_utils.ReadTextProto('filters/medium.ascii_proto',
                                medium_data_filter)

        # Regenerate report if it exists.
        report_info = ndb_data.ReportsProperty.query().get()
        processor = gae_symbol_processor.SymbolProcessor()
        if processor.Load(report_info.last):
            self.response.write('<p>Regenerating report</p>')

        processor.FilterSymbols(hard_data_filter, medium_data_filter)
        processor.Save()
        report_html = processor.CreateReport()
        SendReport(report_html)

        self.response.write(report_html)


application = webapp2.WSGIApplication([
    ('/cron/weekly_best_stocks_report', LastStocksReport),
], debug=True)
