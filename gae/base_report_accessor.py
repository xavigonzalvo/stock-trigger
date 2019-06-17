import abc


class BaseReportAccessor(object):
  """A handler of reports."""

  __metaclass__ = abc.ABCMeta

  def __init__(self):
    self._report = None

  @abc.abstractmethod
  def create(self, date):
    raise NotImplementedError

  @abc.abstractmethod
  def save(self):
    raise NotImplementedError

  @abc.abstractmethod
  def load(self, date):
    raise NotImplementedError

  @property
  def report(self):
    return self._report
