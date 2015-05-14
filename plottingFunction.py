# -*- coding: utf-8 -*-

# Plotting Function
import numpy as np
import matplotlib.pyplot as plt
from Equations import *
from GeneralizedLeastSquaresFit import matrixFit
from LinearBestFitFunction import linearFit

def plotScatter(xAxis, yMeasured, errorYMeasured, BBofL, dustofLList, vectorA, bestFit,yTheory):
	plt.close('all')

	# Line Plots
	plt.subplot(2, 1, 1)
	plt.plot(xAxis, [y for y in yMeasured])
	plt.plot(xAxis, bestFit)
	plt.title("yMeasured and Best Fit Function")

	plt.subplot(2, 1, 2)
	plt.plot(xAxis, [D*vectorA[0] for D in dustofLList],'r')
	plt.plot(xAxis, [B*vectorA[1] for B in BBofL],'g')
	plt.plot(xAxis,bestFit,'k')
	plt.plot(xAxis,yTheory,'b')
	plt.title(vectorA)

	plt.savefig("lineplots.png")

def plotBinScatter(xAxis, lBinCenters, yMeasuredBin, errorYMeasuredBin, BBofLBin, errorBBofLBin, dustofLBin, errordustofLBin, vectorABin, bestFitBin, errorBestFitBin): # is xAxis necessary?
	plt.close('all')

	# Bin Scatter Plots
	plt.subplot(2, 1, 1)
	plt.errorbar(lBinCenters, yMeasuredBin, yerr = errorYMeasuredBin, ls = '--') # plots the mean of each bin at the center of each bin
	plt.errorbar(lBinCenters,bestFitBin,yerr = errorBestFitBin, ls = '--')  # yMplot[-1][0].set_linestyle('--')
	plt.xticks(lBinCenters)
	plt.title("yMeasuredBin and bestFit")

	plt.subplot(2, 1, 2)
	plt.errorbar(lBinCenters,bestFitBin,yerr = errorBestFitBin, ls = '--')
	plt.errorbar(lBinCenters,[B*vectorABin[1] for B in BBofLBin],yerr = errorBBofLBin, ls = '--')
	plt.errorbar(lBinCenters,[D*vectorABin[0] for D in dustofLBin],yerr = errordustofLBin, ls = '--')

	plt.savefig("binplots.png")

def plotCorrelation(aList,bList):
	plt.close('all')
	plotFit = linearFit(aList, bList)
	plotList = [x for x in np.arange(min(aList), max(aList), 0.1)]
	plt.plot(aList, bList, 'bo')
	plt.plot(plotList, [plotFit[0] + plotFit[1]*x for x in plotList], 'r-')
	plt.title('bList by aList')
	plt.savefig('aList by bList.png')

def plotxListHisto(histoDataA,histoDataB):
	plt.close('all')
	plt.subplot(2,1,1)
	plt.bar(histoDataA[1][0:-1], histoDataA[0], histoDataA[1][1]-histoDataA[1][0])
	plt.title('aList')
	plt.legend('aList Binned',loc='upper right')

	plt.subplot(2,1,2)
	plt.bar(histoDataB[1][0:-1], histoDataB[0], histoDataB[1][1]-histoDataB[1][0])
	plt.title('bList')
	plt.legend('bList Binned',loc='upper right')

	plt.savefig('aList, bList histograms.png')


