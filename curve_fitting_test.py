import unittest
from curve_fitting import *
import logging
import matplotlib.pyplot as plt
import numpy as np


class CurveFittingTest(unittest.TestCase):

    @staticmethod
    def Equals(l1, l2, eps=0.001):
        if len(l1) != len(l2):
            return False
        for i in range(1, len(l1)):
            if abs(l1[i] - l2[i]) > eps:
                logging.error('Element differs: %s %s' % (
                    str(l1[i]), str(l2[i])))
                return False
        return True

    def testFit(self):
        self.__cf = CurveFitting(np.arange(0, 1.1, 0.1))
        poly, error, convex = self.__cf.Quadratic()
        self.assertTrue(self.Equals(poly, [0, 1.0, 0]))

    def testFit2(self):
        values = [0.0, 0.01, 0.04, 0.09, 0.16, 0.25, 0.36, 0.49, 0.64, 0.81, 1.]
        self.__cf = CurveFitting(values)
        poly, error, convex = self.__cf.Quadratic()
        self.assertTrue(self.Equals(poly, [1.0, 0, 0]))
        self.assertTrue(convex)

    def testFit3(self):
        values = [10., 11., 13., 15., 12., 14., 12.]
        self.__cf = CurveFitting(values)
        poly, error, convex = self.__cf.Quadratic()
        self.assertTrue(self.Equals(poly, [-10.71, 13.0714, 9.7619]))
        self.assertFalse(convex)


if __name__ == '__main__':
    unittest.main()
