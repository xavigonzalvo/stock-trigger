import csv
import math
import os
import matplotlib.pyplot as plt
import numpy as np

def ReadData(filename):
    """Open file and returns all data as a list and week close values.

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
        self.__data = data
        self.__num_weeks = self._GetNumWeeks(num_weeks)
        
    def _GetNumWeeks(self, num_weeks):
        if num_weeks <= 0:
            num_weeks = len(self.__data) - 1
        else:
            num_weeks = min(num_weeks, len(self.__data) - 1)
        print "Analyzing %d weeks" % num_weeks
        return num_weeks

    def _PlotHist(self, hist, bin_edges):
        plt.bar(bin_edges[:-1], hist, width = 1)
        plt.xlim(min(bin_edges), max(bin_edges))
        return plt

    def Process(self):
        """Processes weeks and computes statistic indicators.

        Returns:
          A tuple containing the week values, mean, std.
        """
        slopes = []
        week_values = []
        for week in range(0, self.__num_weeks):
            current_week = float(self.__data[week]['close'])
            next_week = float(self.__data[week + 1]['close'])
            slope = (current_week - next_week) / 7
            slopes.append(slope)
            week_values.append(current_week)

        hist, bins = np.histogram(slopes,
                                  bins=np.arange(min(slopes),
                                                 max(slopes)), density=True)
        self._PlotHist(hist, bins)
        plt.draw()
        return (week_values, np.mean(slopes), np.std(slopes))