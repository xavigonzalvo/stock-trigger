"""Process data of a stock extracting weekly information."""

import csv
import numpy as np
import StringIO 


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
    with open(filename, 'rb') as csvfile:
        return ProcessData(csvfile)


class WeeksProcessor(object):

    def __init__(self, data, num_weeks):
        """Constructor.

        Args:
          data: a dictionary of values for each week in reverse
                order (ie. latest first)
          num_weeks: number of weeks to analyse from latest week
        """
        self._NUM_DAYS_IN_WEEK = 5  # only working days
        self.__data = data
        self.__num_weeks = self._GetNumWeeks(num_weeks)
        
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
