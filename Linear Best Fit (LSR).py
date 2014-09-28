# -*- coding: utf-8 -*-
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt

# Line of Best Fit (using Least Squares Regression):
# Given X and Y values
xList = []
yList = []

# finds number of values in xList and yList
Nx = len(xList)
Ny = len(yList)

# error if xlist and ylist are different lengths
if Nx != Ny:
    print "Error: incompatible lists"
    raise Exception("Incompatible List length")

N = Nx

#the degree of the polynomial equation (we have only solved for degree = 1)
degree = input("Enter the degree of the fitting polynomial: ")

if degree == 1:
    # given x-values, y-values, and relationship degree polyfit returns list of polynomial coefficients starting with coefficient with the highest power
    p = np.polyfit(xList, yList, degree)

    b = p[0] # highest degree
    a = p[degree] #lowest degree

    # calculating correlation coefficient. r = b *(stdev yList / stdev xList)
    r = b / (np.std(yList)/np.std(xList))
    
    # calculating r-square value
    rSquare = np.square(r)

    plt.plot(xList, yList)
    plt.plot(xList, [a + b*x for x in xList])
else:
    print "Error: degree is not 1"
    raise Exception("Unusable degree")
