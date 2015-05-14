# -*- coding: utf-8 -*-
# Main execution file
import numpy as np
import matplotlib.pyplot as plt
from dataExtractor import extractData  # this extracts the data from a txtfile containing the Lamda Data
from GeneralizedLeastSquaresFit import matrixFit	#
from Equations import *
from plottingFunction import *
from MonteCarlo import monteCarloGen

#------------------------------------------
# Creating functions

# making a list with all the angle l values on the x-axis
xMin = 40
xMax = 400
xStep = 20
xAxis = [l for l in range(xMin, xMax)] # min = 2 max = 1501
frequency = [x*(10**9) for x in xAxis]


# Reference table of constants
h = 6.62606957*(10**-34)    # Plancks constant
nu = 90*(10**9)             # Frequency
c = 299792458               # Speed of Light
k = 1.3806488*(10**-23)     # Boltzmann constant
TDust = 19.6                # Temperature of dust in Kelvin
TVac = 2.7                  # Temperature of vacuum in Kelvin
nu0 = 1                     # Arbitrary value to fill space in function


# Function lists
dustofLList = [dustRatio(90*(10**9), 150*(10**9))*dustofL(l) for l in xAxis]   # Dust of l
BBofL = extractData("LAMDA Data")[xMin:xMax]                                   # BB(l)
yTheory = [D+B for D, B in zip(dustofLList,BBofL)]
yMeasured =   [np.random.normal(T,(T)/10) for T in yTheory] #the added noise is fake data until recieve real data
errorYMeasured = [0.2*max(yMeasured) for x in yMeasured]

YList = [dustofLList, BBofL]
vectorA = matrixFit(YList, yMeasured, errorYMeasured)
bestFit = [D*vectorA[0]+B*vectorA[1] for D,B in zip(dustofLList, BBofL)]

# Bin data function lists
lBinCenters = binCenter(lBins = range(xMin, xMax+xStep, xStep))
dustofLBin = binData(dustofLList, xAxis)
errordustofLBin = [0.2*max(dustofLBin) for x in dustofLBin]
BBofLBin = binData(BBofL, xAxis)
errorBBofLBin = [0.2*max(BBofLBin) for x in BBofLBin]
yMeasuredBin = binData(yMeasured, xAxis)
errorYMeasuredBin = [0.2*max(yMeasuredBin) for x in yMeasuredBin]

YListBin = [dustofLBin, BBofLBin]
theoryBin = [D+B for D, B in zip(dustofLBin, BBofLBin)]
vectorABin = matrixFit(YListBin, yMeasuredBin, errorYMeasuredBin)
bestFitBin = [D*vectorABin[0]+B*vectorABin[1] for D, B in zip(dustofLBin, BBofLBin)]
errorBestFitBin = [0.2*max(bestFitBin) for x in bestFitBin]


# Bar chart function lists
# lBarBins = range(xMin, xMax, xStep)
# dustofLBarBin = binBarData(dustofLList, xAxis)
# BBofLBarBin = binBarData(BBofL, xAxis) 
# YListBarBin = [dustofLBarBin, BBofLBarBin] 
# yMeasuredBarBin = binBarData(yMeasured, xAxis)
# errorYMeasuredBarBin = [0.2*max(yMeasuredBarBin) for x in yMeasuredBarBin]
# vectorABarBin = matrixFit(YListBarBin, yMeasuredBarBin, errorYMeasuredBarBin)

print "vectorA: {0}  vectorABin {1}".format(vectorA, vectorABin)

# Plotting Stuff
plotScatter(xAxis, yMeasured, errorYMeasured, BBofL, dustofLList, vectorA, bestFit,yTheory)
plotBinScatter(xAxis, lBinCenters, yMeasuredBin, errorYMeasuredBin, BBofLBin, errorBBofLBin, dustofLBin, errordustofLBin, vectorABin, bestFitBin, errorBestFitBin)
# plotBinBar(lBarBins, dustofLBarBin, BBofLBarBin, yMeasuredBarBin, errorYMeasuredBarBin, vectorABarBin)

# MonteCarlo
monteCarloGen(YListBin, yMeasuredBin, errorYMeasuredBin, iterations = 1000)

