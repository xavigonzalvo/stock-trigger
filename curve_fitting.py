"""
A curve fitting library.

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

import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt


class CurveFittingError(Exception):
  pass


class CurveFitting(object):

  def __init__(self, values):
    self.__values = values
    self.x = None
    self.y = None
    self._fp_linear = lambda v, x: v[0] * x + v[1]
    self._fp_cubic = lambda v, x: v[0] * x ** 3 + v[1] * x ** 2 + v[2] ** x + v[3]
    self._fp_quadratic = lambda v, x: v[0] * x ** 2 + v[1] * x + v[2]

  def Cubic(self):
    """Cubic polynomial fit (ax3 + bx2 + ...).

    Returns:
      Polynomial coefficients root squared error.
    """
    # Parametric function: 'v' is the parameter vector, 'x' the
    # independent variable.
    (poly, error) = self._Fit(self._fp_cubic, [3., 1, 4., 0.1])
    return (poly, error)

  def Linear(self):
    """Linear regression.

    Returns:
      Polynomial coefficients and root squared error.
    """
    (poly, error) = self._Fit(self._fp_linear, [0.1, 0.1])
    return (poly, error)

  def Quadratic(self):
    """Quadratic polynomial fit (ax2 + bx + c).

    Returns:
      Polynomial coefficients, root squared error and convexity.
    """
    # Parametric function: 'v' is the parameter vector, 'x' the
    # independent variable.
    (poly, error) = self._Fit(self._fp_quadratic, [3., 1, 4.])
    convex = False
    if poly[0] > 0:
      convex = True
    return (poly, error, convex)

  def PlotPolynomial(self, poly):
    """Returns the plot of a polynomial.

    Args:
      fp: Parametric function.
    """
    if len(poly) - 1 == 2:
      fp = self._fp_quadratic
    elif len(poly) - 1 == 3:
      fp = self._fp_cubic
    elif len(poly) - 1 == 1:
      fp = self._fp_linear
    else:
      raise CurveFittingError('Invalid polynomial order')
    plt.plot(self.x, self.y, 'ro', self.x, fp(poly, self.x))
    plt.draw()

  def _Fit(self, fp, v0):
    """Curve fitting.

    Args:
      fp: Parametric function.
      v0: Initial parameter values.

    Returns:
      A tuple with polynomial coefficients and root squared error.
    """
    # Error function.
    e = lambda v, x, y: (fp(v, x) - y)

    # Data.
    n = len(self.__values)
    xmin = 0
    xmax = 1.0
    self.x = np.linspace(xmin, xmax, n)
    self.y = self.__values

    # Fitting.
    poly, cov, infodict, mesg, ier = optimize.leastsq(
        e, v0, args=(self.x, self.y),
        full_output=True,
        maxfev=10000)
    ss_err = (infodict['fvec'] ** 2).sum()
    ss_tot = ((self.y - np.mean(self.y)) ** 2).sum()
    rsquared = 0
    if ss_tot != 0:
      rsquared = 1 - (ss_err / ss_tot)

    return (poly, rsquared)
