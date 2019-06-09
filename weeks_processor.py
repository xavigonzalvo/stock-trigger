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
import numpy as np
from io import StringIO

import curve_fitting_numpy


def ProcessData(fileresource):
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


def ReadData(filename):
    """Opens file and returns all data as a list and week close values.

    Args:
      filename: input file.
    Returns:
      A list of dictionaries, each containing a row of the CSV file.
    """
    with open(filename, 'rt') as csvfile:
        return ProcessData(csvfile)


class WeeksProcessor(object):

    def __init__(self, data, num_weeks, symbol=""):
        """Constructor.

        Args:
          data: a dictionary of values for each week in reverse
                order (ie. latest first)
          num_weeks: number of weeks to analyse from latest week
          symbol: only used by the polynomial model function
        """
        self._NUM_DAYS_IN_WEEK = 5  # only working days
        self.__data = data
        self.__num_weeks = self._GetNumWeeks(num_weeks)
        self.__symbol = symbol

    def _GetNumWeeks(self, num_weeks):
        if num_weeks <= 0:
            num_weeks = len(self.__data) - 1
        else:
            num_weeks = min(num_weeks, len(self.__data) - 1)
        return num_weeks

    def Process(self):
        """Processes weeks and computes statistic indicators.

        Returns:
          A tuple containing the percentage change per day, week
          values, mean and std of percetange change per day. Values
          have the latest first.
        """
        percentage_changes_per_day = []
        week_values = []
        # Loop over all weeks + 1 in order to compute the gradient. Delete
        # extra week value at the end.
        for week in range(0, self.__num_weeks + 1):
            # Week values.
            current_week_value = float(self.__data[week]['close'])
            week_values.append(current_week_value)

            # Slopes.
            if week > 0:
                next_week_value = float(self.__data[week - 1]['close'])
                change_per_day = (next_week_value -
                                  current_week_value) / self._NUM_DAYS_IN_WEEK
                percentage_change_per_day = (
                    change_per_day / current_week_value * 100)
                percentage_changes_per_day.append(percentage_change_per_day)
        del week_values[-1]
        return (percentage_changes_per_day, week_values,
                np.mean(percentage_changes_per_day),
                np.std(percentage_changes_per_day),
                np.mean(week_values))

    def PolynomialModel(self):
        """Models data using polynomial models.

        Returns:
          week_result_pb2.WeekResult
        """
        (percentage_change_per_day, week_values,
         mean, std, mean_value) = self.Process()

        rev_week_values = week_values[::-1]
        fitter = curve_fitting_numpy.CurveFittingNumpy(rev_week_values)

        if "poly" not in result:
            result["poly"] = []

        # Store result.
        result = {}
        result["mean"] = mean
        result["std"] = std
        result["name"] = self.__symbol
        result["mean_value"] = mean_value

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
