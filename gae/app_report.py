import logging

import base_report
import ndb_data


class AppReport(base_report.BaseReport):

  def __init__(self):
    super(AppReport, self).__init__()
    self._report = ndb_data.ReportProperty()

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
