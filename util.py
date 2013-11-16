"""A set of utils."""

import os.path
import matplotlib.pyplot as plt
import numpy as np
import re


def Basename(path):
    return os.path.basename(os.path.splitext(path)[0])


def PlotHistogram(values):
    """Returns a plotted histogram of values.

    Args:
      values: a list of values.
    """
    desired_bins = np.arange(min(values) - 0.001, max(values) + 0.001, 0.1)
    hist, bins = np.histogram(values, bins=desired_bins, density=True)
    plt.bar(bins[:-1], hist, width=0.1)
    plt.xlim(min(bins), max(bins))
    return plt.draw()


def GetSymbolFromFilename(filename):
    return re.search("(.*?)\-", os.path.basename(filename)).groups()[0]


def SafeReadLines(filename):
    """Reads all lines from a file making.

    It makes sure there are no spaces at the beginning and end.
    """
    lines = []
    with open(filename) as f:
        for line in f.readlines():
            lines.append(line.strip())
    return lines
