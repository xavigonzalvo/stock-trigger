import base_symbol_accessor
import ndb_data
import json


class AppSymbolAccessor(base_symbol_accessor.BaseSymbolAccesor):
  """AppEngine symbol accessor."""

  def __init__(self):
    super(AppSymbolAccessor, self).__init__()

  def load(self, name):
    self._name = name
    self._symbol = ndb_data.SymbolProperty.query(
        ndb_data.SymbolProperty.name == name).get()

  def save(self):
    self._symbol.put()

  def add_analysis(self, date, analysis):
    analysis_db = ndb_data.AnalysisProperty(date=date,
                                            data=json.dumps(analysis))
    if not self._symbol:
      self._symbol = ndb_data.SymbolProperty(name=self._name,
                                             analysis=[analysis_db])
    else:
      self._symbol.analysis.append(analysis_db)
