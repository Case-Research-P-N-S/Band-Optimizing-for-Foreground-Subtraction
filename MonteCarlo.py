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


# ------------------------------------------------
# Creating Best Fit Line, storing, and reiterating.

xList = [1,2,3,4,5]
# Creating yList for using in linerFit function
yList = [aTrue + bTrue*x + np.random.normal(x, std) for x in xList]
# storing values
resultsList = fit.linearFit(xList, yList)

print resultsList
