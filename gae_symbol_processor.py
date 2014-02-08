"""Class to process symbols in the GAE."""

import urllib

import filter_utils
import gae_config
import ndb_data
import week_result_pb2


class SymbolProcessor(object):
    """Class to handle symbols, filter and generating reports."""

    def __init__(self):
        self.report = None

    def Load(self, date):
        self.report = ndb_data.ReportProperty.query(
            ndb_data.ReportProperty.date == date).get()
        if not self.report:
            self.report = ndb_data.ReportProperty()
            self.report.date = date
            return False
        self.report.hard_good_symbols = []
        self.report.medium_good_symbols = []
        return True

    def Save(self):
        self.report.put()

    def FilterSymbols(self, hard_data_filter, medium_data_filter):
        """Filters symbols using filters. Uses the last date stored in
        report as the reference to pick values from stored symbols"""
        symbols = ndb_data.SymbolProperty.query()
        self.report.count_correct_analysis = 0
        self.report.count_total = 0
        for symbol in symbols:
            for analysis in symbol.analysis:
                if analysis.date != self.report.date:
                    continue            
                self.report.count_correct_analysis += 1
                data = week_result_pb2.WeekResult()
                data.ParseFromString(analysis.data)
                
                if not filter_utils.Filter(data, hard_data_filter):
                    self.report.hard_good_symbols.append(data.name)
                if not filter_utils.Filter(data, medium_data_filter):
                    self.report.medium_good_symbols.append(data.name)
                break
            self.report.count_total += 1

    def _GenerateSymbolReport(self, symbols):
        """Returns a list of HTML lines with a link to each symbol."""
        html_lines = []
        _HTML_PART = '<a href="%s?q=%s&ei=HejzUoiYBavGwAPk8gE">%s</a><br>'
        for symbol in symbols:
            url_symbol = urllib.quote('LON:%s' % symbol.replace('.L',''))
            html_lines.append(_HTML_PART % (gae_config.WEB_FINANCE, url_symbol,
                                            symbol))
        return html_lines

    def CreateReport(self):
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
                      <h2>Medium filtered symbols</h2><p>%s</p>""" % (
            self.report.date,
            self.report.count_total,
            self.report.count_correct_analysis,
            "".join(hard_msg_symbols_html),
            "".join(medium_msg_symbols_html))    
        return msg_html
