# -*- coding: utf-8 -*-
# Monte Carlo

import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt
import "https://raw.githubusercontent.com/Case-Research-P-N-S/Band-Optimizing-for-Foreground-Subtraction/master/Linear%20Best%20Fit%20Function%20(LSR).py" as fit
import xList

# ---------------------------------------------
# Finding a random integer for the Monte Carlo

mean = 1
# we think this is a function based off of the 
std = 1
# rndint creates the false data for the Monte Carlo
rndInt = np.random.normal(mean, std)


# ---------------------------------------------------
# Theoretical Values for a and b (slope and intercept)

aTrue = 1
bTrue = 1


# ------------------------------------------------
# Creating Best Fit Line, storing, and reiterating.

# Creating yList for using in linerFit function
yList = [aTrue + bTrue*x + rndint for x in xList]
# storing values
[a, b, rSquare] = fit.linearFit(xList, yList)
