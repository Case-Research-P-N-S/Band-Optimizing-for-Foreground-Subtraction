# -*- coding: utf-8 -*-
# Monte Carlo

import numpy as np
import matplotlib.pyplot as plt
import fittingFunctions as fit


def MonteCarlo(TList, measured, std, iterate=10**4):
# matrix Fit doesn't make an r-square value
    aList = []
    bList = []
    # rSquareList = []

    for i in range(iterate):
        # generating yList
        yList = [np.random.normal(m, err) for m, err in zip(measured, std)]
        # applying lines of best fit
        fitCoeff = fit.matrixFit(TList, yList, std)
        # creating an aList, bList, and rSquareList for later analysis
        aList.append(fitCoeff[0])
        bList.append(fitCoeff[1])
        # rSquareList.append(fitCoeff[2])

    # Making the histogram bins
    if iterate < 100:
        binNumber = int(iterate/10)
    else:
        binNumber = 100
    histoDataA = np.histogram(aList, binNumber)
    histoDataB = np.histogram(bList, binNumber)

    plotFit, aMean, bMean = MonteCarloAnalyze(aList, bList)
    plotHisto(histoDataA, histoDataB, aMean, bMean)
    plotCorrelation(aList, bList, plotFit, aMean, bMean)
    # plotRSquare(plotFit)


def MonteCarloAnalyze(aList, bList):
    plotFit = fit.linearFit(aList, bList)
    aMean = np.mean(aList, dtype=np.float64)
    bMean = np.mean(bList, dtype=np.float64)

    return plotFit, aMean, bMean


def plotCorrelation(aList, bList, plotFit, aMean, bMean):
    # Makes a correlation plot between _________________
    fig = plt.figure()
    ax = plt.subplot(1, 1, 1)
    # Correlation plot
    correlplot, = ax.plot(aList, bList, 'bo', label='b by a List')
    # best fit plot
    plotList = [x for x in np.arange(min(aList), max(aList), 0.1)]
    bestfit, = ax.plot(plotList, [plotFit[0] + plotFit[1]*x for x in plotList], 'r-', label='bestfit')
    # mean plots
    bmean = ax.axhline(y=bMean, c='k', linestyle='dashed', linewidth=1, label='b mean')
    amean = ax.axvline(x=aMean, c='k', linestyle='dashed', linewidth=1, label='a mean')

    plt.title('bList by aList')
    plt.xlabel('aList')
    plt.ylabel('bList')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels, loc='upper right')
    plt.savefig('aList by bList.png')
    plt.close(fig)


def plotHisto(histoDataA, histoDataB, aMean, bMean):
    # Makes a histogram of the binned lists done in the correlation plot using histogram data made in MonteCarlo
    fig = plt.figure()
    # A List Subplot
    ax1 = plt.subplot(2, 1, 1)
    ahist = ax1.bar(histoDataA[1][0:-1], histoDataA[0], histoDataA[1][1]-histoDataA[1][0], label='A Hist')
    amean = ax1.axvline(x=aMean, c='r', linestyle='dashed', label='A Mean')

    plt.title('aList')
    handles, labels = ax1.get_legend_handles_labels()
    ax1.legend(handles, labels, loc='upper right')

    # B List Subplot
    ax2 = plt.subplot(2, 1, 2)
    bhist = ax2.bar(histoDataB[1][0:-1], histoDataB[0], histoDataB[1][1]-histoDataB[1][0], label='B Hist')
    bmean = ax2.axvline(x=bMean, c='r', linestyle='dashed', label='B Mean')
    plt.title('bList')
    handles, labels = ax2.get_legend_handles_labels()
    ax2.legend(handles, labels, loc='upper right')

    plt.savefig('aList, bList histograms.png')
    plt.close(fig)
