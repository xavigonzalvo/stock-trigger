"""Process data of a stock extracting weekly information.

The MIT License (MIT)

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import csv
import logging
import numpy as np
from io import StringIO

import curve_fitting_numpy


def _process_data(fileresource):
  """Process opened file resource and returns a list of week close values.

  Args:
    fileresource: file pointer
  Returns:
    A list of dictionaries, each containing a row of the CSV file.
  """
  reader = csv.reader(fileresource, delimiter=',')
  data = []
  header = []
  for row in reader:
    if not header:
      header = [value.lower() for value in row]
    else:
      values = dict(zip(header, row))
      data.append(values)
  return data


def read_data(filename):
  """Opens file and returns all data as a list and week close values.

  Args:
    filename: input file.
  Returns:
    A list of dictionaries, each containing a row of the CSV file.
  """
  with open(filename, 'rt') as csvfile:
    return _process_data(csvfile)


class DaysProcessor(object):

  def __init__(self, data, period, window=5, symbol=""):
    """Constructor.

    Args:
      data: a dictionary of values for each week in reverse
        order (ie. latest first)
      period: an `int` indicating the number of days used in total.
      window: an `int` indicating the number of days to average over.
      symbol: only used by the polynomial model function
    """
    self._data = data
    self._period = min(period, len(data))
    self._window = window
    self._symbol = symbol

  def process(self):
    """Processes data and computes statistic indicators.

    Returns:
      A tuple containing the percentage change per day, week
      values, mean and std of percetange change per day. Values
      have the latest first.
    """
    window_values = []
    averaged_data = []
    for i in range(self._period):
      window_values.append(self._data[i])
      if len(window_values) == self._window:
        averaged_data.append(np.mean(window_values))
        window_values = []

    percentage_changes_per_day = []
    for i, value in enumerate(averaged_data):
      if i > 0:
        average_change_per_day = (
            abs(averaged_data[i - 1] - averaged_data[i])) / self._window
        percentage_change_per_day = average_change_per_day / averaged_data[i]
        percentage_changes_per_day.append(percentage_change_per_day * 100.)
    return (percentage_changes_per_day, averaged_data,
            np.mean(percentage_changes_per_day),
            np.std(percentage_changes_per_day),
            np.mean(averaged_data))

  def poly_model(self):
    """Models data using polynomial models.

    Returns:
      week_result_pb2.WeekResult
    """
    (percentage_change_per_day, week_values,
     mean, std, mean_value) = self.process()

    rev_week_values = week_values[::-1]
    fitter = curve_fitting_numpy.CurveFittingNumpy(rev_week_values)

    # Store result.
    result = {}
    result["mean"] = mean
    result["std"] = std
    result["name"] = self._symbol
    result["mean_value"] = mean_value
    result["poly"] = []

    (poly, _) = fitter.Linear()
    linear_poly = {}
    linear_poly["order"] = 1
    linear_poly["coef"] = list(poly)
    result["poly"].append(linear_poly)

    poly, error, convex = fitter.Quadratic()
    quadratic_poly = {}
    quadratic_poly["order"] = 2
    quadratic_poly["coef"] = list(poly)
    quadratic_poly["error"] = error
    quadratic_poly["convex"] = convex
    result["poly"].append(quadratic_poly)

    return result
