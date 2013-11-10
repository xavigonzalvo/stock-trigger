import csv
import numpy as np


def ReadData(filename):
    """Opens file and returns all data as a list and week close values.

    Args:
      filename: input file.
    Returns:
      A list of dictionaries, each containing a row of the CSV file.
    """
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        data = []
        header = []
        for row in reader:
            if not header:
                header = [value.lower() for value in row]
            else:
                values = dict(zip(header, row))
                data.append(values)
        return data


class WeeksProcessor(object):

    def __init__(self, data, num_weeks):
        """Constructor.

        Args:
          data: values for each week in reverse order (ie. latest first)
          num_weeks: number of weeks to analyse from latest week
        """
        self._NUM_DAYS_IN_WEEK = 5
        self.__data = data
        self.__num_weeks = self._GetNumWeeks(num_weeks)
        
    def _GetNumWeeks(self, num_weeks):
        if num_weeks <= 0:
            num_weeks = len(self.__data) - 1
        else:
            num_weeks = min(num_weeks, len(self.__data) - 1)
        print "Analyzing %d weeks" % num_weeks
        return num_weeks

    def Process(self):
        """Processes weeks and computes statistic indicators.

        Returns:
          A tuple containing the slopes, week values, mean and std.
        """
        slopes = []
        week_values = []
        for week in range(0, self.__num_weeks):
            current_week = float(self.__data[week]['close'])
            next_week = float(self.__data[week + 1]['close'])
            slope = (current_week - next_week) / self._NUM_DAYS_IN_WEEK
            slopes.append(slope)
            week_values.append(current_week)
        return (slopes, week_values, np.mean(slopes), np.std(slopes))
