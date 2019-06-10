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

import filter_utils
import gae_config
import ndb_data


class SymbolProcessor(object):
    """Class to handle symbols, filter and generating reports."""

    def __init__(self):
        self.report = ndb_data.ReportProperty()

    def Load(self, date):
        self.report = ndb_data.ReportProperty.query(
            ndb_data.ReportProperty.date == date).get()
        if not self.report:
            self.report = ndb_data.ReportProperty()
            self.report.date = date
            return False
        return True

    def Save(self):
        self.report.put()

    def FilterSymbols(self, hard_data_filter, medium_data_filter):
        """Filters symbols using filters. Uses the last date stored in
        report as the reference to pick values from stored symbols"""
        self.report.hard_good_symbols = []
        self.report.medium_good_symbols = []
        symbols = ndb_data.SymbolProperty.query()
        self.report.count_correct_analysis = 0
        self.report.count_total = 0
        all_symbols = []
        for symbol in symbols:
            for analysis in symbol.analysis:
                if analysis.date != self.report.date:
                    continue
                self.report.count_correct_analysis += 1
                data = json.loads(analysis.data)

                if not filter_utils.filter(data, hard_data_filter):
                    self.report.hard_good_symbols.append(data.name)
                if not filter_utils.filter(data, medium_data_filter):
                    self.report.medium_good_symbols.append(data.name)
                break
            self.report.count_total += 1
            all_symbols.append(symbol.name)
        return all_symbols

    def _GenerateSymbolReport(self, symbols):
        """Returns a list of HTML lines with a link to each symbol."""
        html_lines = []
        _HTML_PART = '<a href="%s?q=%s&ei=HejzUoiYBavGwAPk8gE">%s</a><br>'
        for symbol in symbols:
            url_symbol = urllib.quote('LON:%s' % symbol.replace('.L',''))
            html_lines.append(_HTML_PART % (gae_config.WEB_FINANCE, url_symbol,
                                            symbol))
        return html_lines

    def CreateReport(self, all_symbols):
        """Generates an HTML report given good symbols."""
        hard_part = self._GenerateSymbolReport(self.report.hard_good_symbols)
        medium_part = self._GenerateSymbolReport(
            self.report.medium_good_symbols)

        hard_msg_symbols_html = ['%s<br>' % symbol for symbol in hard_part]
        medium_msg_symbols_html = ['%s<br>' % symbol for symbol in medium_part]
        msg_html = """<h2>Stats</h2>
                      <p>Date: %s<br>
                      count_total = %d<br>
                      count_correct_analysis = %d</p>
                      <h2>Hard filtered symbols</h2><p>%s</p>
                      <h2>Medium filtered symbols</h2><p>%s</p>
                      <h2>All symbols</h2><p>%s</p>""" % (
            self.report.date,
            self.report.count_total,
            self.report.count_correct_analysis,
            "".join(hard_msg_symbols_html),
            "".join(medium_msg_symbols_html),
            "<br>".join(all_symbols))
        return msg_html
