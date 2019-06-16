import abc


class BaseReports(object):
  """Base class to handle the reports container."""

  __metaclass__ = abc.ABCMeta

  def __init__(self):
    self._reports = None

  @abc.abstractmethod
  def add_new_report(self, date):
    raise NotImplementedError

  @abc.abstractmethod
  def last_date(self):
    raise NotImplementedError
