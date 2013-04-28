import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt


class CurveFitting(object):

    def __init__(self, values):
        self.__values = values
        
    def Cubic(self):
        # Parametric function: 'v' is the parameter vector, 'x' the
        # independent variable.
        fp = lambda v, x: v[0] * x ** 3 + v[1] * x ** 2 + v[2] ** x + v[3]
        self._Fit(fp)

    def Quadratic(self):
        # Parametric function: 'v' is the parameter vector, 'x' the
        # independent variable.
        fp = lambda v, x: v[0] * x ** 2 + v[1] * x + v[2]
        self._Fit(fp)

    def _Fit(self, fp):
        """Curve fitting.

        Args:
          fp: Parametric function.
        """
        # Error function.
        e = lambda v, x, y: (fp(v, x) - y)

        # Initial parameter value.
        v0 = [3., 1, 4., 0.1]

        # Data.
        n = len(self.__values)
        xmin = 0
        xmax = n
        x = np.linspace(xmin, xmax, n)
        y = self.__values

        # Fitting.
        polynomial, success =  optimize.leastsq(e, v0, args=(x, y), maxfev=10000)
        print 'Estimated polynomial: %s' % str(polynomial)
        plt.plot(x, y, 'ro', x, fp(polynomial, x))
        plt.draw()
