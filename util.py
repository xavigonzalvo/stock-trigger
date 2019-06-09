"""A set of utils.

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

import json
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


def read_json(filename):
  """Reads a json in text mode."""
  with open(filename, 'r') as f:
    return json.loads(f.read())
