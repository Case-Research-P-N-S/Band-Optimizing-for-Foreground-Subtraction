# -*- coding: utf-8 -*-

# Plotting Function
import matplotlib.pyplot as plt


def plotScatter(xAxis, yMeasured, errorYMeasured, BMode, dustList, fitCoeff, bestFit, yTheory):
    # Makes a scatter plot
    plt.close('all')
    # Line Plots
    plt.subplot(2, 1, 1)
    plt.plot(xAxis, [y for y in yMeasured])
    plt.plot(xAxis, bestFit)
    plt.title("yMeasured and Best Fit Function")

    plt.subplot(2, 1, 2)
    plt.plot(xAxis, [D*fitCoeff[0] for D in dustList], 'r')
    plt.plot(xAxis, [B*fitCoeff[1] for B in BMode], 'g')
    plt.plot(xAxis, bestFit, 'k')
    plt.plot(xAxis, yTheory, 'b')
    plt.title(fitCoeff)

    plt.savefig("lineplots.png")


def plotBinScatter(lBinCent, yMeasuredBin, errorYMeasuredBin, BModeBin, errorBModeBin, dustBin, errordustBin, fitCoeffBin, bestFitBin, errorBestFitBin):
    # Makes a scatter plot
    plt.close('all')

    # Measured data and best fit
    plt.subplot(2, 1, 1)
    plt.errorbar(lBinCent, yMeasuredBin, yerr=errorYMeasuredBin, ls='')  # plots the mean of each bin at the center of each bin
    plt.errorbar(lBinCent, bestFitBin, yerr=errorBestFitBin, ls='--')  # yMplot[-1][0].set_linestyle('--')
    plt.xticks(lBinCent)
    plt.title("yMeasuredBin and bestFit")

    # compares best fit to adjusted values of theory
    plt.subplot(2, 1, 2)
    plt.errorbar(lBinCent, bestFitBin, yerr=errorBestFitBin, ls='--')
    plt.errorbar(lBinCent, [B*fitCoeffBin[1] for B in BModeBin], yerr=errorBModeBin, ls='--')
    plt.errorbar(lBinCent, [D*fitCoeffBin[0] for D in dustBin], yerr=errordustBin, ls='--')

    plt.savefig("binplots.png")
