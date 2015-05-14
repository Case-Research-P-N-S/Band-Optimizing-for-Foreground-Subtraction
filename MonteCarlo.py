# -*- coding: utf-8 -*-
# Monte Carlo

import numpy as np
from GeneralizedLeastSquaresFit import matrixFit
from plottingFunction import plotCorrelation, plotxListHisto

def monteCarloGen(TList, measured, std, iterations=1000):
# matrix Fit doesn't make an r-square value 
    # ---------------------------------------------------
    # Theoretical Values for a and b (slope and intercept)

    aList = []
    bList = []
    # rSquareList = []

    # ------------------------------------------------
    # Creating Best Fit Line, storing, and reiterating.

    # assuming x's are constant, may later generate x's from a normal distribution
    # how many times the Monte Carlo is repeated

    for i in range(iterations):
        # generating yList
        yList = [np.random.normal(m, err) for m, err in zip(measured, std)]
        # applying lines of best fit
        results = matrixFit(TList, yList, std)
        # creating an aList, bList, and rSquareList for later analysis
        aList.append(results[0])
        bList.append(results[1])
        # rSquareList.append(results[2])

    if iterations < 100:
        binNumber = int(iterations/10)
    else:
        binNumber = 100

    histoDataA = np.histogram(aList, binNumber)
    histoDataB = np.histogram(bList, binNumber)

    plotCorrelation(aList, bList)
    plotxListHisto(histoDataA, histoDataB)
