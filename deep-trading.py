import webapp2

class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write('<a href="/cron/weekly_best_stocks_process">Run symbol processor</a><br>')
        self.response.write('<a href="/cron/weekly_best_stocks_report">Run symbol report</a><br>')


application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
