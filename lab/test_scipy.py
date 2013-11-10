#  == METHOD 2 ==
from numpy import *
from scipy import optimize

x = r_[  9, 35, -13,  10,  23,   0]
y = r_[ 34, 10,   6, -14,  27, -10]
basename = 'circle'

# x = r_[36, 36, 19, 18, 33, 26]
# y = r_[14, 10, 28, 31, 18, 26]
# basename = 'arc'

# # Code to generate random data points
# R0 = 25
# nb_pts = 40
# dR = 1
# angle =10*pi/5
# theta0 = random.uniform(0, angle, size=nb_pts)
# x = (10 + R0*cos(theta0) + dR*random.normal(size=nb_pts)).round()
# y = (10 + R0*sin(theta0) + dR*random.normal(size=nb_pts)).round()


# == METHOD 1 ==
method_1 = 'algebraic'

# coordinates of the barycenter
x_m = mean(x)
y_m = mean(y)

method_2 = "leastsq"

def calc_R(xc, yc):
    """ calculate the distance of each 2D points from the center (xc, yc) """
    return sqrt((x-xc)**2 + (y-yc)**2)

def f_2(c):
    """ calculate the algebraic distance between the data points and the mean circle centered at c=(xc, yc) """
    Ri = calc_R(*c)
    return Ri - Ri.mean()

center_estimate = x_m, y_m
center_2, ier = optimize.leastsq(f_2, center_estimate)

xc_2, yc_2 = center_2
Ri_2       = calc_R(*center_2)
R_2        = Ri_2.mean()
residu_2   = sum((Ri_2 - R_2)**2)

print "xc=%f, yc=%f" % (xc_2, yc_2)
print "Ri=" + str(Ri_2)
print "R=%f" % R_2
print "res=%f" % residu_2

# PLOT

from matplotlib import pyplot as p, cm, colors
p.close('all')

def plot_all(residu2=False):
    """ Draw data points, best fit circles and center for the three methods,
    and adds the iso contours corresponding to the fiel residu or residu2
    """
    f = p.figure( facecolor='white')  #figsize=(7, 5.4), dpi=72,
    p.axis('equal')
    theta_fit = linspace(-pi, pi, 180)

    x_fit2 = xc_2 + R_2*cos(theta_fit)
    y_fit2 = yc_2 + R_2*sin(theta_fit)
    p.plot(x_fit2, y_fit2, 'k--', label=method_2, lw=2)
    p.plot([xc_2], [yc_2], 'gD', mec='r', mew=1)

    # plot the residu fields
    nb_pts = 100
    p.draw()
    xmin, xmax = p.xlim()
    ymin, ymax = p.ylim()

    vmin = min(xmin, ymin)
    vmax = max(xmax, ymax)

    xg, yg = ogrid[vmin:vmax:nb_pts*1j, vmin:vmax:nb_pts*1j]
    xg = xg[..., newaxis]
    yg = yg[..., newaxis]
    
    Rig    = sqrt( (xg - x)**2 + (yg - y)**2 )
    Rig_m  = Rig.mean(axis=2)[..., newaxis]
    residu = sum( (Rig**2 - Rig_m**2)**2 ,axis=2)

    lvl = exp(linspace(log(residu.min()), log(residu.max()), 15))
    p.contourf(xg.flat, yg.flat, residu.T, lvl, alpha=0.4, cmap=cm.Purples_r)
    cbar = p.colorbar(fraction=0.175, format='%.f')
    cbar.set_label('Residu_2 - algebraic approximation')
    
    p.plot(x, y, 'ro', label='data', ms=8, mec='b', mew=1)
    p.legend(loc='best',labelspacing=0.1 )

    p.xlim(xmin=vmin, xmax=vmax)
    p.ylim(ymin=vmin, ymax=vmax)
    p.grid()
    p.title('Least Squares Circle')
    
#plot_all()
#p.show()