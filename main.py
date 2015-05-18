# -*- coding: utf-8 -*-
# Main execution file

import numpy as np
from dataExtractor import extractData                  # this extracts the data from a txtfile containing the Lamda Data
import fittingFunctions as fit                         # best fit functions
import Equations as eqn                                # file with most of the used equations
import plottingFunction as pltfn                       # handles all plotting
from MonteCarlo import MonteCarlo                      # runs the monte carlo

'''
Document Info
- Function of L
'''

'''
Notes to Self
Should the l related values (with more distinctive names)?
the function sometimes doesn't work if errorMeasured isn't a constant
should all the errors be 0.2*max(value)?
change nu0 to a real value?
the MonteCarlo function first does a plt.hist then passes that to a plt.bar. Change that.
    make the bins be the same as in lBins(histoDataA, histoDataB, aMean, bMean
rename stuff better
	ref_  --> something else
the first best fit section isn't necessary since the data will always be binned.
'''


# ------------------------------------------
# Constants

# making a list with all the angle l values as the x-axis
xMin = 40                               # minimum l value used
xMax = 400                              # maxiumm l value used
xStep = 20                              # l-step value used for binning. This doesn't have to be a constant
lList = [l for l in range(xMin, xMax)]  # min = 2 max = 1501
lBinCent = eqn.binCenter(lBins=range(xMin, xMax+xStep, xStep))  # finding the centers of the bins to plot binned data

# Reference table of constants
nu1 = 90.0*(10**9)                      # Frequency 1
nu2 = 150.0*(10**9)                     # Frequency 2
nu0 = 1.0                               # ** Arbitrary value to fill space in function **
h = 6.62606957*(10**-34)                # Planck's constant
c = 299792458                           # speed of Light
k = 1.3806488*(10**-23)                 # Boltzmann constant
TVac = 2.7                              # temperature of vacuum in Kelvin
TDust = 19.6                            # temperature of dust in Kelvin        # This value is never called, should it be?
const = [h, c, k, TVac, TDust]          # constants assembled in a list


# ------------------------------------------
# Creating functions

# ----- Function Lists -----
# Theory data
dustList = [eqn.dustRatio(nu1, nu2, nu0, const)*eqn.dust(l) for l in lList]           # Dust of l
BMode = extractData("LAMDA Data")[xMin:xMax]                                          # BB(l) extracted from file
Theory = [D+B for D, B in zip(dustList, BMode)]                                       # the theoretical curve
# Measured data
Measured = [np.random.normal(T, (T)/10) for T in Theory]                              # the added noise is fake data until recieve real data
errorMeasured = [0.2*max(Measured) for x in Measured]                                 # the error in the measured data
# Best fit. Not for important use since not binned
ref_theoryConcat = [dustList, BMode]                                                  # concatenation of Dust and BB
ref_fitCoeff = fit.matrixFit(ref_theoryConcat, Measured, errorMeasured)               # getting the best fit coefficients of theory to measured data
ref_bestFit = [D*ref_fitCoeff[0]+B*ref_fitCoeff[1] for D, B in zip(dustList, BMode)]  # best fit to measured by multiplying theory by coefficnts

# -----  Binned Function Lists -----
# Theory data
dustBin = eqn.binData(dustList, lList)                                                # binned Dust
errordustBin = [0.2*max(dustBin) for x in dustBin]                                    # error in binned Dust
BModeBin = eqn.binData(BMode, lList)                                                  # binned BB
errorBModeBin = [0.2*max(BModeBin) for x in BModeBin]                                 # error in binned BB
TheoryBin = [D+B for D, B in zip(dustBin, BModeBin)]                                  # the theoretical curve
errorTheoryBin = [0.05*max(TheoryBin) for x in TheoryBin]                             # error in theoretical curve      # Important for MonteCarlo
# Measured data
MeasuredBin = eqn.binData(Measured, lList)                                            # binned measured data
errorMeasuredBin = [0.2*max(MeasuredBin) for x in MeasuredBin]                        # error in binned measured data
# Best Fit
theoryBinConcat = [dustBin, BModeBin]                                                 # concatenation of binned Dust and binned BB
fitCoeff = fit.avgMatrixFit(theoryBinConcat, MeasuredBin, errorMeasuredBin, 10**4)    # best fit of Measured Bin to
bestFit = [D*fitCoeff[0]+B*fitCoeff[1] for D, B in zip(dustBin, BModeBin)]            # best fit to MeasuredBin by multiplying theory by coefficnts
errorBestFit = [0.2*max(bestFit) for x in bestFit]                                    # error in best fit

# seeing some outputs
print "ref_fitCoeff: {0}  fitCoeff {1}".format(ref_fitCoeff, fitCoeff)

# ------------------------------------------
# Plotting Stuff

# Fit Plots
pltfn.plotScatter(lList, Measured, errorMeasured, BMode, dustList, ref_fitCoeff, ref_bestFit, Theory)
pltfn.plotBinScatter(lBinCent, MeasuredBin, errorMeasuredBin, BModeBin, errorBModeBin, dustBin, errordustBin, fitCoeff, bestFit, errorBestFit)

# MonteCarlo
MonteCarlo(theoryBinConcat, TheoryBin, errorTheoryBin, iterate=10**4)                 # Monte Carlo of _________
