"""Handles reports for AppEngine."""

import logging

from base_reports_accessor import BaseReportsAccessor
import ndb_data


class AppReportsAccessor(BaseReportsAccessor):

  def __init__(self):
    super(AppReportsAccessor, self).__init__()
    self._reports = ndb_data.ReportsProperty.query().get()
    if not self._reports:
      logging.info('Creating container of reports')
      self._reports = ndb_data.ReportsProperty()

  def add_new_report(self, date):
    self._reports.last = date
    self._reports.put()
    logging.info('New report with date %s', date)

  def last_date(self):
    return self._reports.last
