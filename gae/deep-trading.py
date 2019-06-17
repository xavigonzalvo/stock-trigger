"""Main entry for the application.

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

from datetime import datetime
from google.appengine.ext import ndb

from google.appengine.api import users
from google.appengine.datastore.datastore_query import Cursor
from app_report_accessor import AppReportAccessor
import ndb_data
import gae_symbol_processor
import webapp2


def _create_symmary(report):
  percentage = 0.0
  if report.count_total > 0:
    percentage = len(report.hard_good_symbols) / float(report.count_total)
  return '%s (total=%d, good=%.2f%%, ...)' % (report.date, report.count_total,
                                              percentage)


class SymbolsTool(webapp2.RequestHandler):
  """A set of tools to manage symbols."""

  def get(self):
    action = self.request.get('action')

    num_symbols = None
    error = None
    if action == 'count':
      symbols = ndb_data.SymbolProperty.query().fetch(keys_only=True)
      num_symbols = 0
      for _ in symbols:
        num_symbols += 1
      message = "<p>Number of symbols: {}</p>".format(num_symbols)
    elif action == 'list':
      symbols = ndb_data.SymbolProperty.query().fetch(10)
      all_symbols = []
      for symbol in symbols:
        all_symbols.append(symbol.name)
      message = "<p>Some symbols: {}</p>".format(map(str, all_symbols))
    elif action == 'delete':
      ndb.delete_multi(
          ndb_data.SymbolProperty.query().fetch(keys_only=True))
      message = "<p>Deleted</p>"
    else:
      message = "No valid action: {}".format(action)

    html = r"""<html><body>{}</body></html>""".format(message)
    self.response.headers['Content-Type'] = 'text/html'
    self.response.write(html)


class ReportsTool(webapp2.RequestHandler):
  """A set of tools to manage reports."""

  def get(self):
    action = self.request.get('action')

    num_symbols = None
    error = None
    if action == 'count':
      reports = ndb_data.ReportProperty.query().fetch(keys_only=True)
      num_reports = 0
      for _ in reports:
        num_reports += 1
      last_report_date = "no report"
      if num_reports > 0:
        last_report = ndb_data.ReportProperty.query().order(
            -ndb_data.ReportProperty.date).fetch(limit=1)[0]
        last_report_date = last_report.date
      reports_container = ndb_data.ReportsProperty.query().fetch()[0]
      message = r"""<p>Number of reports: {}</p>
      <p>Last date container: {}</p>
      <p>Last report date: {}</p>
      """.format(num_reports, reports_container.last, last_report_date)
    elif action == 'delete':
      ndb.delete_multi(
          ndb_data.ReportProperty.query().fetch(keys_only=True))
      message = "<p>Deleted</p>"
    else:
      message = "No valid action: {}".format(action)

    html = r"""<html><body>{}</body></html>""".format(message)
    self.response.headers['Content-Type'] = 'text/html'
    self.response.write(html)


class StocksReport(webapp2.RequestHandler):
  """Prints a list of reports and a specific report by date."""

  def get(self):
    self.response.headers['Content-Type'] = 'text/html'

    # Print one report.
    report_date_req = self.request.get('date')
    if report_date_req:
      report_date = datetime.strptime(
          report_date_req, '%Y-%m-%d %H:%M:%S.%f')
      report_accessor = AppReportAccessor()
      if not report_accessor.load(report_date):
        logging.info("Couldn't find report with date %s", date)
        return
      processor = gae_symbol_processor.SymbolProcessor(report_accessor)
      report_html = processor.generate_html_report()
      self.response.write("Loaded report")
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
                          (report.date, _create_symmary(report)))
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
      self.response.write('<p>Symbols tool</p>')
      self.response.write('<ul>')
      self.response.write('<li><a href="/symbols_tool?action=count">Count symbols</a></li>')
      self.response.write('<li><a href="/symbols_tool?action=list">List symbols</a></li>')
      self.response.write('<li><a href="/symbols_tool?action=delete">Delete all symbols</a></li>')
      self.response.write('</ul>')
      self.response.write('<p>Reports tool</p>')
      self.response.write('<ul>')
      self.response.write('<li><a href="/reports_tool?action=count">Count reports</a></li>')
      self.response.write('<li><a href="/stocks_report">List reports</a></li>')
      self.response.write('<li><a href="/reports_tool?action=delete">Delete all reports</a></li>')
      self.response.write('</ul>')
      self.response.write('<p><a href="/cron/weekly_best_stocks_process?test=2">Test symbol processor</a></p>')
      self.response.write('<hr><p><a href="/cron/weekly_best_stocks_process">Run symbols processor</a></p>')
      self.response.write('<p><a href="/cron/weekly_best_stocks_report">Run symbols report</a></p>')
    else:
      greeting = ('<a href="%s">Sign in or register</a>.' %
                  users.create_login_url('/'))
      self.response.out.write('<html><body>%s' % greeting)


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/symbols_tool', SymbolsTool),
    ('/reports_tool', ReportsTool),
    ('/stocks_report', StocksReport),
], debug=True)
