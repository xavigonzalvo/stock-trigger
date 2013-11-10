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
    hist, bins = np.histogram(values,
                              bins=np.arange(min(values),
                                             max(values)), density=True)        
    plt.bar(bins[:-1], hist, width = 1)
    plt.xlim(min(bins), max(bins))
    return plt.draw()


def GetSymbolFromFilename(filename):
    return re.search("(.*?)\-", os.path.basename(filename)).groups()[0]
