# -*- coding: utf-8 -*-
# Line of Best Fit (using Least Squares Regression):

import numpy as np


def linearFit(xList, yList, degree=1):
    # Line of Best Fit (using Least Squares Regression):
    '''
    Description:
    A function that takes in two lists of equal length corresponding
    the x-coords and y-coords of a graph and returns a list containing
    the intercept, slope and r^2 of the line of best fit to that graph
    '''

    # error if xlist and ylist are different lengths
    if len(xList) != len(yList):
        print "Error: incompatible lists"
        raise Exception("Incompatible List Lengths")

    '''
    given x-values, y-values, and relationship degree,
    polyfit returns list of polynomial coefficients
    starting with coefficient with the highest power
    '''
    p = np.polyfit(xList, yList, degree)
    b = p[0]  # highest degree
    a = p[1]  # lowest degree

    # calculating correlation coefficient. r = b *(stdev yList / stdev xList)
    r = b * (np.std(yList)/np.std(xList))

    # calculating r-square value
    rSquare = np.square(r)

    return [a, b, rSquare]
