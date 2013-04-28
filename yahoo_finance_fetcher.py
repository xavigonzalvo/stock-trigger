import urllib
import urllib2


class YahooFinanceFetcher(object):

    def __init__(self):
        self.__HISTORICAL_SERVER = 'http://ichart.yahoo.com/table.csv'

    def _GetData(self, server, values):
        data = urllib.urlencode(values)
        resp = urllib2.urlopen('%s?%s' % (server, data))
        return resp.read()

    def GetHistorical(self, symbol, start_year, end_year, period):
        """Gets historical values.

        Args:
          symbol: stock symbol
          start_year: from year
          end_year: to year
          period: 'd'=day, 'w'=week, 'm'=month
        """
        values = {'s': symbol,
                  'a': 0,
                  'b': 1,
                  'c': start_year,
                  'd': 0,
                  'e': 31,
                  'f': end_year,
                  'g': period,
                  'ignore': '.csv'}
        self._GetData(self.__HISTORICAL_SERVER, values)
