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

import logging
import sys
import json
import re
import urlparse
from urllib import urlencode
from urllib2 import urlopen, HTTPError, URLError


class FinanceFetcher(object):

  def __init__(self, api_key=None):
    self._api_key = api_key
    self._SERVER = 'https://cloud.iexapis.com'

  def _get_data(self, symbol, period="1m"):
    """Returns the json representation of the data in the given period.

    Args:
      symbol: a symbol name.
      period: e.g., 1m

    Returns:
      The data as a list.

    Raises:
      Exception: if response doesn't contain the data.
    """
    # Prepare request.
    items = {
      "token": self._api_key,
    }
    server_values = urlencode(items)
    items = {
        "server": self._SERVER,
        "symbol": symbol,
        "range": period,
        "server_values": server_values
    }
    req = '{server}/stable/stock/{symbol}/chart/{range}?{server_values}'.format(
        **items)

    try:
      response = urlopen(req, timeout=15)
    except URLError, e:
      logging.error('Error getting response for historical data: %s', e)
      raise Exception
    data = json.loads(response.read())
    historical_close_values = []
    for day in data:
      historical_close_values.append(float(day["close"]))
    return historical_close_values

  def get_all_symbols(self):
    """Gets all symbols from the finance sector."""
    raise NotImplementedError

  def get_historical(self, symbol, period):
    """Gets historical values.

    Args:
      symbol: stock symbol
      period: e.g., 1m, 1y

    Returns:
      A string containing the data.
    """
    # Data is in month, day, year format. Note that month is 0-based.
    data = self._get_data(symbol, period)
    return data[::-1]

  def get_market_cap(self, symbol):
    values = {
      'token': self._api_key,
    }
    values = urlencode(values)
    info = {
      'url': self._SERVER,
      'symbol': symbol,
      'values': values
    }
    req = '{url}/stable/stock/{symbol}/stats?{values}'.format(**info)
    try:
      response = urlopen(req, timeout=15)
    except URLError, e:
      logging.error('Error getting response for market cap: %s', e)
      return None
    data = json.loads(response.read())
    if 'marketcap' in data and data['marketcap'] is not None:
      return data['marketcap'] / 1000000
    logging.error('Wrong data contains: %s', data)
    return None

  def get_name(self, symbol):
    values = {
        'token': self._api_key,
    }
    values = urlencode(values)
    info = {
        'url': self._SERVER,
        'symbol': symbol,
        'values': values
    }
    req = '{url}/stable/stock/{symbol}/company?{values}'.format(**info)
    try:
      response = urlopen(req, timeout=15)
    except URLError, e:
      logging.error('Error getting response for name: %s', e)
      return ""
    data = json.loads(response.read())
    if 'companyName' in data:
      return data['companyName']
    logging.error('Wrong data contains: %s', data)
    return ""
