"""Library to fetch information from Yahoo.

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

import json
import urllib
import urllib2
import re


class YahooFinanceFetcherError(Exception):
    pass


class YahooFinanceFetcher(object):

    def __init__(self):
        self.__HISTORICAL_SERVER = 'http://ichart.yahoo.com/table.csv'
        self.__QUOTE_SERVER = 'http://download.finance.yahoo.com/d/quotes.csv'
        self.__YQL_SERVER = 'http://query.yahooapis.com/v1/public/yql'

    def _GetData(self, server, values):
        try:
            data = urllib.urlencode(values)
            resp = urllib2.urlopen('%s?%s' % (server, data), timeout=15)
            return resp.read()
        except urllib2.HTTPError:
            raise YahooFinanceFetcherError(
                'Failed to process query "%s"' % data)

    def GetAllSymbols(self):
        """Gets all LSE symbols using a YQL request."""
        values = {
            'q': ('select * from yahoo.finance.industry '
                  'where id in (select industry.id from '
                  'yahoo.finance.sectors)'),
            'env': 'store://datatables.org/alltableswithkeys',
            'format': 'json',
        }
        # TODO(xavigonzalvo): there are some cases where the data
        # doesn't match
        data = json.loads(self._GetData(self.__YQL_SERVER, values))
        industries = data['query']['results']['industry']
        companies = []
        for item in industries:
            if 'company' in item:
                for company in item['company']:
                    if type(company) == dict:
                        symbol = company['symbol']
                        if '.L' in symbol:
                            companies.append(symbol)
                    else:
                        print company
            else:
                print item
        return companies        

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
        # Data is in month, day, year format. Note that month is 0-based.
        values = {'s': symbol,
                  'a': 0,  # January
                  'b': 1,
                  'c': start_year,
                  'd': 11,  # December
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
        if 'N/A' not in info:
            return float(re.findall("\d+.\d+", info)[0])
        return None

    def GetName(self, symbol):
        """Gets name."""
        values = {'s': symbol,
                  'f': 'n0',
                  'e': '.csv'}
        info = self._GetData(self.__QUOTE_SERVER, values)
        return info.strip('\r\n"')
    
