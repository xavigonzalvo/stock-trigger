"""Handles reports for AppEngine."""

import logging

import base_reports
import ndb_data


class AppReports(base_reports.BaseReports):

  def __init__(self):
    super(AppReports, self).__init__()
    self._reports = ndb_data.ReportsProperty.query().get()
    if not self._reports:
      logging.info('Creating container of reports')
      self._reports = ndb_data.ReportsProperty()

  def add_new_report(self, date):
    self._reports.last = date
    self._reports.put()

  def last_date(self):
    return self._reports.last
