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
        xmax = 1.0
        x = np.linspace(xmin, xmax, n)
        y = self.__values

        # Fitting.
        poly, cov, infodict, mesg, ier = optimize.leastsq(
            e, v0, args=(x, y),
            full_output=True,
            maxfev=10000)
        ss_err = (infodict['fvec'] ** 2).sum()
        ss_tot = ((y - np.mean(y)) ** 2).sum()
        rsquared = 1 - (ss_err / ss_tot)

        # Plot.
        plt.plot(x, y, 'ro', x, fp(poly, x))
        plt.draw()

        return (poly, rsquared)