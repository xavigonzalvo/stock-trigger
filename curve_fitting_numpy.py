"""Curve fitting module using numpy."""

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
