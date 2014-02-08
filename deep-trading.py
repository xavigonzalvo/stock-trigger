import webapp2

class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write('<p><a href="/stocks_report">All reports</a></p>')
        self.response.write('<p><a href="/cron/weekly_best_stocks_process">Run symbol processor</a></p>')
        self.response.write('<p><a href="/cron/weekly_best_stocks_report">Run symbol report</a></p>')


application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
