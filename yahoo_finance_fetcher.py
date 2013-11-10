"""Library to fetch information from Yahoo."""

import urllib
import urllib2
import re


class YahooFinanceFetcherError(Exception):
    pass


class YahooFinanceFetcher(object):

    def __init__(self):
        self.__HISTORICAL_SERVER = 'http://ichart.yahoo.com/table.csv'
        self.__QUOTE_SERVER = 'http://download.finance.yahoo.com/d/quotes.csv'

    def _GetData(self, server, values):
        try:
            data = urllib.urlencode(values)
            resp = urllib2.urlopen('%s?%s' % (server, data))
            return resp.read()
        except urllib2.HTTPError:
            raise YahooFinanceFetcherError('Not found')

    def GetHistorical(self, symbol, start_year, end_year, period):
        """Gets historical values.

        Args:
          symbol: stock symbol
          start_year: from year
          end_year: to year
          period: 'd'=day, 'w'=week, 'm'=month

        Returns:
          A string containing the data.
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
        return self._GetData(self.__HISTORICAL_SERVER, values)

    def GetMarketCap(self, symbol):
        """Gets market capitalization in millions."""
        values = {'s': symbol,
                  'f': 'j1',
                  'e': '.csv'}
        info = self._GetData(self.__QUOTE_SERVER, values)
        return float(re.findall("\d+.\d+", info)[0])
