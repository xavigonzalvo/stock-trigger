"""Library to fetch financial information from AlphaAdvantage.

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
import urllib.error
import urllib.parse
import urllib.request
import re


class Error(Exception):
    pass


class FinanceFetcher(object):

    def __init__(self, api_key=None, iexcloud_token=None):
        self._SERVER = 'https://www.alphavantage.co/query'
        self._TIME_SERIES = {
            'd': 'TIME_SERIES_DAILY',
            'w': 'TIME_SERIES_WEEKLY',
            'm': 'TIME_SERIES_MONTHLY'
        }
        self._KEY_TIME_SERIES = {
            'd': 'Daily Time Series',
            'w': 'Weekly Time Series',
            'm': 'Monthly Time Series'
        }
        self._api_key = api_key
        self._IEXCLOUD_SERVER = 'https://cloud.iexapis.com'
        self._iexcloud_token = iexcloud_token

    def _GetData(self, values, period):
        """Returns the json representation of the data in the given period.

        Args:
          values: a dict with 'symbol' and 'datatype'.
          period: one of 'd', 'w' or 'm'.

        Returns:
          The data as a list.
        """
        try:
            values['function'] = self._TIME_SERIES[period]
            values['apikey'] = self._api_key
            values = urllib.parse.urlencode(values)
            req = '{}?{}'.format(self._SERVER, values)
            with urllib.request.urlopen(req, timeout=15) as response:
                data = json.loads(response.read())
                time_series_key = self._KEY_TIME_SERIES[period]
                time_data = data[time_series_key]
                sorted(time_data, key=lambda k: k, reverse=False)
                data = []
                for _, values_per_period in time_data.items():
                    data.append(values_per_period['4. close'])
                return data
        except urllib.error.HTTPError as e:
            raise Error('Failed to process query "{}" with error {}'.format(
                values, e.code))

    def GetAllSymbols(self):
      raise NotImplemented("Missing for AlphaAdvantage")
    #     """Gets all LSE symbols using a YQL request."""
    #     values = {
    #         'q': ('select * from yahoo.finance.industry '
    #               'where id in (select industry.id from '
    #               'yahoo.finance.sectors)'),
    #         'env': 'store://datatables.org/alltableswithkeys',
    #         'format': 'json',
    #     }
    #     # TODO(xavigonzalvo): there are some cases where the data
    #     # doesn't match
    #     data = json.loads(self._GetData(self.__YQL_SERVER, values))
    #     industries = data['query']['results']['industry']
    #     companies = []
    #     for item in industries:
    #         if 'company' in item:
    #             for company in item['company']:
    #                 if type(company) == dict:
    #                     symbol = company['symbol']
    #                     if '.L' in symbol:
    #                         companies.append(symbol)
    #                 else:
    #                     print company
    #         else:
    #             print item
    #     return companies

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
        values = {'symbol': symbol, 'datatype': 'json'}
        data = self._GetData(values, period)
        data.insert(0, "close")
        return '\n'.join(data)

    def GetMarketCap(self, symbol):
      values = {
        'token': self._iexcloud_token,
      }
      values = urllib.parse.urlencode(values)
      info = {
        'url': self._IEXCLOUD_SERVER,
        'symbol': symbol,
        'values': values
      }
      req = '{url}/stable/stock/{symbol}/stats?{values}'.format(**info)
      with urllib.request.urlopen(req, timeout=15) as response:
        data = json.loads(response.read())
        return data['marketcap']
