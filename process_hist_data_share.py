import csv
import math
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


def ProcessWeeks(data, week_values):
    slopes = []
    for week in range(0, len(week_values) - 1):
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
    plt.plot(week_values[::-1])
    plt.subplot(212)
    _PlotHist(hist, bins)
    plt.draw()


def main(argv):
    (data, week_values) = OpenFile(argv[1])
    print '%d weeks for analysis (%d months, %d years)' % (
        len(week_values), len(week_values) / 4, len(week_values) / 4 / 12)
    ProcessWeeks(data, week_values)
    plt.show(block=False)

if __name__ == "__main__":
    main(sys.argv)