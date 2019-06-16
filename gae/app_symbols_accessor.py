import base_symbols_accessor
import ndb_data


class AppSymbolsAccessor(base_symbols_accessor.BaseSymbolsAccessor):
  """AppEngine class to handle symbols."""

  def get_all_symbols(self, keys_only=True):
    return ndb_data.SymbolProperty.query()
