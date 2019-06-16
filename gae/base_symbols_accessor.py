import abc


class BaseSymbolsAccessor(object):
  """Base class to access symbols."""

  __metaclass__ = abc.ABCMeta

  @abc.abstractmethod
  def get_all_symbols(self, keys_only=True):
    raise NotImplementedError
