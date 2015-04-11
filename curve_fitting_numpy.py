"""Curve fitting module using numpy.

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


class CurveFittingNumPyError(Exception):
    pass


class CurveFittingNumpy(object):

    def __init__(self, values):
        self.__values = values
        self.x = None
        self.y = None

    def Cubic(self):
        """Cubic polynomial fit (ax3 + bx2 + ...).

        Returns:
          Polynomial coefficients root squared error.
        """
        # Parametric function: 'v' is the parameter vector, 'x' the
        # independent variable.
        poly = self._Fit(3)
        return (poly, 0.0)

    def Linear(self):
        """Linear regression.

        Returns:
          Polynomial coefficients and root squared error.
        """
        poly = self._Fit(1)
        return (poly, 0.0)

    def Quadratic(self):
        """Quadratic polynomial fit (ax2 + bx + c).

        Returns:
          Polynomial coefficients, root squared error and convexity.
        """
        # Parametric function: 'v' is the parameter vector, 'x' the
        # independent variable.
        poly = self._Fit(2)
        convex = False
        if poly[0] > 0:
            convex = True
        return (poly, 0.0, convex)

    def _Fit(self, order):
        """Curve fitting.

        Args:
          fp: Parametric function.
          v0: Initial parameter values.

        Returns:
          A tuple with polynomial coefficients and root squared error.
        """
        # Error function.
        #e = lambda v, x, y: (fp(v, x) - y)

        # Data.
        n = len(self.__values)
        xmin = 0
        xmax = 1.0
        self.x = np.linspace(xmin, xmax, n)
        self.y = self.__values

        # Fitting.
        return np.polyfit(self.x, self.y, order)
