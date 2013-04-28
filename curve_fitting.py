import numpy as np
from scipy import optimize
import random
import matplotlib.pyplot as plt


class CurveFitting(object):

    def __init__(self, values):
        self.__values = values
        
    def Cubic(self):
        """Cubic polynomial fit.

        Returns:
          Polynomial coefficients.
        """
        # Parametric function: 'v' is the parameter vector, 'x' the
        # independent variable.
        fpa = lambda v, x: v[0] * x ** 3 + v[1] * x ** 2 + v[2] ** x + v[3]
        return self._Fit(fpa, [3., 1, 4., 0.1])

    def Quadratic(self):
        """Quadratic polynomial fit.

        Returns:
          Polynomial coefficients.
        """
        # Parametric function: 'v' is the parameter vector, 'x' the
        # independent variable.
        fpc = lambda v, x: v[0] * x ** 2 + v[1] * x + v[2]
        return self._Fit(fpc, [3., 1, 4.])

    def _Fit(self, fp, v0):
        """Curve fitting.

        Args:
          fp: Parametric function.
          v0: Initial parameter values.

        Returns:
          Polynomial coefficients.
        """
        # Error function.
        e = lambda v, x, y: (fp(v, x) - y)

        # Data.
        n = len(self.__values)
        xmin = 0
        xmax = n
        x = np.linspace(xmin, xmax, n)
        y = self.__values

        # Fitting.
        polynomial, success =  optimize.leastsq(e, v0, args=(x, y),
                                                maxfev=10000)
        plt.plot(x, y, 'ro', x, fp(polynomial, x))
        plt.draw()

        return polynomial