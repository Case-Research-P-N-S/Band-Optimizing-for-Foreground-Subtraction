# -*- coding: utf-8 -*-
# Monte Carlo

import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt

try:
    import LinearBestFitFunction.py as fit
except:
    import site
    site.addsitedir("https://raw.githubusercontent.com/Case-Research-P-N-S/Band-Optimizing-for-Foreground-Subtraction/master/LinearBestFitFunction.py")


# ---------------------------------------------
# Finding a standard deviation value for the Monte Carlo 
# it's probably a function. don't know yet
std = 1


# ---------------------------------------------------
# Theoretical Values for a and b (slope and intercept)

aTrue = 1
bTrue = 1

aList = []
bList = []
rSquareList = []

# ------------------------------------------------
# Creating Best Fit Line, storing, and reiterating.


xList = [1,2,3,4,5]


# assuming x's are constant, may later generate x's from a normal distribution
for i in range(100):
    yList = [aTrue + bTrue*x + np.random.normal(0, std) for x in xList]
    results = fit.linearFit(xList, yList)
    aList.append(results[0])
    bList.append(results[1])
    rSquareList.append(results[2])

print "aTrue = %d, aAverage = %d\nbTrue = %d, bAverage = %d" % (aTrue, np.average(aList), bTrue, np.average(bList))