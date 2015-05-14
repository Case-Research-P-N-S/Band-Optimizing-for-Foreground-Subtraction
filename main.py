# -*- coding: utf-8 -*-
# Main execution file

import numpy as np
from dataExtractor import extractData               # this extracts the data from a txtfile containing the Lamda Data
from GeneralizedLeastSquaresFit import matrixFit    # best fit function
import Equations as eqn                             # file with most of the used equations
import plottingFunction as pltfn                    # handles all plotting
from MonteCarlo import monteCarloGen as monteCarlo  # runs the monte carlo

'''
Should the l related values and the reference table of constants be made into global variables (with more distinctive names)?
the function sometimes doesn't work if errorYMeasured isn't a constant
should all the errors be 0.2*max(value)?
change nu0
'''

# ------------------------------------------
# Creating functions

# making a list with all the angle l values as the x-axis
xMin = 40                               # minimum l value used
xMax = 400                              # maxiumm l value used
xStep = 20                              # l-step value used for binning
xAxis = [l for l in range(xMin, xMax)]  # min = 2 max = 1501

# Reference table of constants
h = 6.62606957*(10**-34)                # Plancks constant
nu1 = 90*(10**9)                        # Frequency 1
nu2 = 150*(10**9)                       # Frequency 2
c = 299792458                           # Speed of Light
k = 1.3806488*(10**-23)                 # Boltzmann constant
TDust = 19.6                            # Temperature of dust in Kelvin
TVac = 2.7                              # Temperature of vacuum in Kelvin
nu0 = 1                                 # ** Arbitrary value to fill space in function **


# Function lists
dustofLList = [eqn.dustRatio(nu1, nu2)*eqn.dustofL(l) for l in xAxis]          # Dust of l
BBofL = extractData("LAMDA Data")[xMin:xMax]                                   # BB(l) extracted from file
yTheory = [D+B for D, B in zip(dustofLList, BBofL)]                            # the theoretical curve
yMeasured = [np.random.normal(T, (T)/10) for T in yTheory]                     # the added noise is fake data until recieve real data
errorYMeasured = [0.2*max(yMeasured) for x in yMeasured]                       # the error in the measured data

YList = [dustofLList, BBofL]                                                   # concatenation of Dust and BB
vectorA = matrixFit(YList, yMeasured, errorYMeasured)                          # getting the best fit coefficients of theory to measured data
bestFit = [D*vectorA[0]+B*vectorA[1] for D, B in zip(dustofLList, BBofL)]      # best fit to measured by multiplying theory by coefficnts

# Bin data function lists
lBinCenters = eqn.binCenter(lBins=range(xMin, xMax+xStep, xStep))              # finding the centers of the bins to plot binned data
dustofLBin = eqn.binData(dustofLList, xAxis)                                   # binned Dust
errordustofLBin = [0.2*max(dustofLBin) for x in dustofLBin]                    # error in binned Dust
BBofLBin = eqn.binData(BBofL, xAxis)                                           # binned BB
errorBBofLBin = [0.2*max(BBofLBin) for x in BBofLBin]                          # error in binned BB
yMeasuredBin = eqn.binData(yMeasured, xAxis)                                   # binned measured data
errorYMeasuredBin = [0.2*max(yMeasuredBin) for x in yMeasuredBin]              # error in binned measured data

YListBin = [dustofLBin, BBofLBin]                                              # concatenation of binned Dust and binned BB
theoryBin = [D+B for D, B in zip(dustofLBin, BBofLBin)]                        # concatenation of binned Dust and binned BB
vectorABin = matrixFit(YListBin, yMeasuredBin, errorYMeasuredBin)
bestFitBin = [D*vectorABin[0]+B*vectorABin[1] for D, B in zip(dustofLBin, BBofLBin)]  # best fit to measured by multiplying theory by coefficnts
errorBestFitBin = [0.2*max(bestFitBin) for x in bestFitBin]                    # error in best fit

# seeing some outputs
print "vectorA: {0}  vectorABin {1}".format(vectorA, vectorABin)

# ------------------------------------------
# Plotting Stuff

# Fit Plots
pltfn.plotScatter(xAxis, yMeasured, errorYMeasured, BBofL, dustofLList, vectorA, bestFit, yTheory)
pltfn.plotBinScatter(xAxis, lBinCenters, yMeasuredBin, errorYMeasuredBin, BBofLBin, errorBBofLBin, dustofLBin, errordustofLBin, vectorABin, bestFitBin, errorBestFitBin)

# MonteCarlo
monteCarlo(YListBin, yMeasuredBin, errorYMeasuredBin, iterations=10**4)       # Monte Carlo of _________
