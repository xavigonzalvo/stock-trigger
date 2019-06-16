import base_symbol_accessor
import ndb_data


class AppSymbolAccessor(base_symbol_accessor.BaseSymbolAccesor):
  """AppEngine symbol accessor."""

  def __init__(self):
    super(AppSymbolAccessor, self).__init__()

  def load(self, name):
    self._symbol = ndb_data.SymbolProperty.query(
        ndb_data.SymbolProperty.name == name).get()

  def save(self):
    self._symbol.put()

  def add_analysis(self, analysis_db):
    if not self._symbol:
      self._symbol = ndb_data.SymbolProperty(name=symbol,
                                             analysis=[analysis_db])
    else:
      self._symbol.analysis.append(analysis_db)
