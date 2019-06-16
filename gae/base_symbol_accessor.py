import abc


class BaseSymbolAccesor(object):
  """Base symbol accessor."""

  __metaclass__ = abc.ABCMeta

  def __init__(self):
    self._symbol = None

  @abc.abstractmethod
  def load(self, name):
    raise NotImplementedError

  @abc.abstractmethod
  def save(self):
    raise NotImplementedError

  @abc.abstractmethod
  def add_analysis(self, analysis_db):
    raise NotImplementedError

  @property
  def symbol(self):
    return self._symbol
