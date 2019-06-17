import logging

from base_report_accessor import BaseReportAccessor
import ndb_data


class AppReportAccessor(BaseReportAccessor):

  def __init__(self):
    super(AppReportAccessor, self).__init__()

  def create(self, date):
    self._report = ndb_data.ReportProperty(date=date)

  def save(self):
    self._report.put()

  def load(self, date):
    """Returns True if the report exists and sets the internal variable."""
    report = ndb_data.ReportProperty.query(
        ndb_data.ReportProperty.date == date).get()
    if not report:
      logging.info('Report not found (date %s)', date)
      return False
    self._report = report
    return True
