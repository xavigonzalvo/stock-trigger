"""Main entry for the application."""

import gae_setup  # Needs to be first

from datetime import datetime

from google.appengine.api import users
from google.appengine.datastore.datastore_query import Cursor
import ndb_data
import gae_symbol_processor
import webapp2


def CreateSummary(report):
    percentage = 0.0
    if report.count_total > 0:
        percentage = len(report.hard_good_symbols) / float(report.count_total)
    return '%s (total=%d, good=%.2f%%, ...)' % (report.date, report.count_total,
                                                percentage)


class StocksReport(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        # Print one report.
        report_date_req = self.request.get('date')
        if report_date_req:
            report_date = datetime.strptime(
                report_date_req, '%Y-%m-%d %H:%M:%S.%f')
            processor = gae_symbol_processor.SymbolProcessor()
            processor.Load(report_date)
            report_html = processor.CreateReport()
            self.response.write(report_html)
            return

        # List of reports.
        self.response.write('<h1>Reports</h1>')
        curs = Cursor(urlsafe=self.request.get('cursor'))
        reports, next_curs, more = (
            ndb_data.ReportProperty.query().
            order(-ndb_data.ReportProperty.date).
            fetch_page(10, start_cursor=curs))
        for report in reports:
            self.response.write('<p><a href="/stocks_report?date=%s">%s</a></p>' %
                                (report.date, CreateSummary(report)))
        if more and next_curs:
            self.response.out.write('<a href="/stocks_report?cursor=%s">More...</a>' %
                                    next_curs.urlsafe())


class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        if user:
            greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                        (user.nickname(), users.create_logout_url('/')))
            self.response.out.write('<html><body>%s' % greeting)
            self.response.write('<p><a href="/stocks_report">All reports</a></p>')
            self.response.write('<p><a href="/cron/weekly_best_stocks_process">Run symbol processor</a></p>')
            self.response.write('<p><a href="/cron/weekly_best_stocks_report">Run symbol report</a></p>')
        else:
            greeting = ('<a href="%s">Sign in or register</a>.' %
                        users.create_login_url('/'))
            self.response.out.write('<html><body>%s' % greeting)


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/stocks_report', StocksReport),
], debug=True)
