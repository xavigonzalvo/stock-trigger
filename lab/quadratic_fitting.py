from pylab import *
from numpy import *
from scipy.optimize import leastsq

## Parametric function: 'v' is the parameter vector, 'x' the independent varible
fp = lambda v, x: v[0] * x ** 2 + v[1] * x + v[2]

## Noisy function (used to generate data to fit)
v_real = [1.5, 0.1, 2.]
fn = lambda x: fp(v_real, x)

## Error function
e = lambda v, x, y: (fp(v,x) - y)

## Generating noisy data to fit
n = 30
xmin = 0.1
xmax = 5
x = linspace(xmin,xmax,n)
y = fn(x) + rand(len(x)) * 0.05 * (fn(x).max() - fn(x).min())

## Initial parameter value
v0 = [3., 1, 4.]

## Fitting
v, success = leastsq(e, v0, args=(x,y), maxfev=10000)

## Plot
def plot_fit():
    print 'Estimated parameters: ', v
    print 'Real parameters: ', v_real
    print 'Success: ' + str(success)
    X = linspace(xmin,xmax,n*5)
    plot(x,y,'ro', X, fp(v,X))


plot_fit()
show()