import csv
import math
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize

def OpenFile(filename):
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


def _PlotHist(hist, bin_edges):
    plt.bar(bin_edges[:-1], hist, width = 1)
    plt.xlim(min(bin_edges), max(bin_edges))
    return plt


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
        _PlotHist(hist, bins)
        plt.draw()
        return (week_values, np.mean(slopes), np.std(slopes))


def Basename(path):
    return os.path.basename(os.path.splitext(path)[0])


def QuadraticFitting(values):
    # Parametric function: 'v' is the parameter vector, 'x' the
    # independent variable
    #fp = lambda v, x: v[0] * x ** 2 + v[1] * x + v[2]
    fp = lambda v, x: v[0] * x ** 3 + v[1] * x ** 2 + v[2] ** x + v[3]
    # Error function
    e = lambda v, x, y: (fp(v, x) - y)

    # Initial parameter value
    v0 = [3., 1, 4., 0.1]

    # Data.
    n = len(values)
    xmin = 0
    xmax = len(values)
    x = np.linspace(xmin, xmax, n)
    y = values

    # Fitting.
    polynomial, success =  optimize.leastsq(e, v0, args=(x, y), maxfev=10000)
    print 'Estimated polynomial: %s' % str(polynomial)
    plt.plot(x, y, 'ro', x, fp(polynomial, x))
    plt.draw()


def main(argv):
    filename = argv[1]
    output_path = argv[2]
    num_weeks = int(argv[3])

    # Read data.
    data = OpenFile(filename)
    total_num_weeks = len(data)
    print '%d weeks for analysis (%d months, %d years)' % (
        total_num_weeks, total_num_weeks / 4, total_num_weeks / 4 / 12)

    # Process.
    runner = WeeksProcessor(data, num_weeks)
    plt.subplot(311)
    (week_values, mean, std) = runner.Process()
    print "Mean: %f, Std: %f" % (mean, std)

    plt.subplot(312)
    rev_week_values = week_values[::-1]
    plt.plot(rev_week_values)

    plt.subplot(313)
    QuadraticFitting(rev_week_values)

    # Save figures
    output_figure_path = os.path.join(
        output_path,
        '%s-%s.png' % (Basename(filename),
                       str(num_weeks) if num_weeks > 0 else 'all'))
    plt.savefig(output_figure_path)


if __name__ == "__main__":
    main(sys.argv)