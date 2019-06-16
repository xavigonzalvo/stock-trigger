import abc


class BaseReport(object):
  """A handler of reports."""

  __metaclass__ = abc.ABCMeta

  def __init__(self):
    self._report = None

  @abc.abstractmethod
  def save(self):
    raise NotImplementedError

  @abc.abstractmethod
  def load(self, date):
    raise NotImplementedError

  def report(self):
    return self._report
