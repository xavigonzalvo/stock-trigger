"""Defines a server to generate weekly reports.

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

from google.appengine.api import mail

from app_reports import AppReports
import gae_config
import gae_symbol_processor
import gae_utils
import webapp2


def _send_report(report_html):
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
    hard_data_filter = gae_utils.read_json('filters/hard.json')
    medium_data_filter = gae_utils.read_json('filters/medium.json')

    # Generate a report and regenerate it if it exists.
    reports = AppReports()
    processor = gae_symbol_processor.SymbolProcessor()
    if processor.load(reports.last_date()):
      self.response.write('<p>Regenerating report</p>')

    processor.filter_symbols(hard_data_filter, medium_data_filter)
    processor.save()
    report_html = processor.generate_report()
    _send_report(report_html)

    self.response.write(report_html)


application = webapp2.WSGIApplication([
    ('/cron/weekly_best_stocks_report', LastStocksReport),
], debug=True)
