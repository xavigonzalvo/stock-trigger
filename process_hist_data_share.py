import csv
import math
import os
import sys
import matplotlib.pyplot as plt
import numpy as np 

def OpenFile(filename):
    """Open file and returns all data as a list and week close values.
    """
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        first = True
        week_values = []
        data = []
        pos_close = -1
        for row in reader:
            if first:
                header = row
                pos_close = header.index('Close')
                first = False
            else:
                week_values.append(float(row[pos_close]))
                data.append(row)
        return (data, week_values)

        
def _PlotHist(hist, bin_edges):
    plt.bar(bin_edges[:-1], hist, width = 1)
    plt.xlim(min(bin_edges), max(bin_edges))
    return plt


def ProcessWeeks(data, week_values, num_weeks):
    """Processes weeks.

    Args:
      data: values for each week in reverse order (ie. latest first)
      week_values: share price for each week in reverse order
      num_weeks: number of weeks to analyse from latest week
    """
    slopes = []
    if num_weeks <= 0:
        num_weeks = len(week_values) - 1
    else:
        num_weeks = min(num_weeks, len(week_values) - 1)
    print "Analyzing %d weeks" % num_weeks
    for week in range(0, num_weeks):
        slope = (week_values[week] - week_values[week + 1]) / 7
        #print 'w=%d date=%s v=%f m=%f d=%f' % (week,
        #                                       data[week][0],
        #                                       week_values[week],
        #                                       slope,
        #                                       math.atan(slope) * 180 / math.pi)
        slopes.append(slope)
    hist, bins = np.histogram(slopes, bins=np.arange(min(slopes),
                                                     max(slopes)), density=True)
    print "Mean: %f, Std: %f" % (np.mean(slopes), np.std(slopes))
    plt.subplot(211)
    rev_week_values = week_values[::-1]
    plt.plot(rev_week_values[len(week_values) - num_weeks:])
    plt.subplot(212)
    _PlotHist(hist, bins)
    plt.draw()
    return num_weeks


def Basename(path):
    return os.path.basename(os.path.splitext(path)[0])


def main(argv):
    filename = argv[1]
    output_path = argv[2]
    num_weeks = int(argv[3])
    (data, week_values) = OpenFile(filename)
    print '%d weeks for analysis (%d months, %d years)' % (
        len(week_values), len(week_values) / 4, len(week_values) / 4 / 12)
    ProcessWeeks(data, week_values, num_weeks)
    output_figure_path = os.path.join(
        output_path,
        '%s-%s.png' % (Basename(filename),
                       str(num_weeks) if num_weeks > 0 else 'all'))
    plt.savefig(output_figure_path)


if __name__ == "__main__":
    main(sys.argv)