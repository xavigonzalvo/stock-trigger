"""Class to process symbols in the GAE.

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
import logging

from app_symbols_accessor import AppSymbolsAccessor
import filter_utils
import gae_config


class SymbolProcessor(object):
  """Class to handle symbols, filter and generating reports."""

  def __init__(self, report_accessor):
    self._report_accessor = report_accessor

  def filter_symbols(self, hard_data_filter, medium_data_filter):
    """Filters symbols using filters.

    Uses the last date stored in report as the reference to pick values
    from stored symbols.
    """
    report = self._report_accessor.report
    report.hard_good_symbols = []
    report.medium_good_symbols = []
    report.count_correct_analysis = 0
    report.count_total = 0

    symbols_accessor = AppSymbolsAccessor()
    symbols = symbols_accessor.get_all_symbols(keys_only=False)
    for symbol in symbols:
      for analysis in symbol.analysis:
        if analysis.date != report.date:
          continue
        report.count_correct_analysis += 1
        data = json.loads(analysis.data)

        if not filter_utils.filter(data, hard_data_filter):
          report.hard_good_symbols.append(data["name"])
        if not filter_utils.filter(data, medium_data_filter):
          report.medium_good_symbols.append(data["name"])
        break  # we've processed the analysis of the correct date
      report.count_total += 1

  def _generate_symbol_report(self, symbols):
    """Returns a list of HTML lines with a link to each symbol."""
    html_lines = []
    HTML_PART = '<a href="%s?q=%s&ei=HejzUoiYBavGwAPk8gE">%s</a><br>'
    for symbol in symbols:
      url_symbol = urllib.quote('%s' % symbol.replace('.L',''))
      html_lines.append(HTML_PART % (gae_config.WEB_FINANCE, url_symbol,
                                     symbol))
    return html_lines

  def generate_html_report(self):
    """Generates an HTML report given good symbols."""
    report = self._report_accessor.report
    hard_section = self._generate_symbol_report(report.hard_good_symbols)
    medium_section = self._generate_symbol_report(report.medium_good_symbols)

    hard_msg_symbols_html = ['%s<br>' % symbol for symbol in hard_section]
    medium_msg_symbols_html = ['%s<br>' % symbol
                               for symbol in medium_section]
    msg_html = """<h2>Stats</h2>
                  <p>Date: %s<br>
                  count_total = %d<br>
                  count_correct_analysis = %d</p>
                  <h2>Hard filtered symbols</h2><p>%s</p>
                  <h2>Medium filtered symbols</h2><p>%s</p>""" % (
        report.date,
        report.count_total,
        report.count_correct_analysis,
        "".join(hard_msg_symbols_html),
        "".join(medium_msg_symbols_html))
    return msg_html
