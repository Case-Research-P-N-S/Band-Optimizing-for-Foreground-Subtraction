# -*- coding: utf-8 -*-
# Main execution file
import numpy as np
import matplotlib.pyplot as plt
from DataExtractor import extractData
from GeneralizedLeastSquaresFit import matrixFit
from Equations import *

#------------------------------------------
# Creating functions

# making a list with all the angle l values on the x-axis
xAxis = [l for l in range(2, 1501)]
frequency = [x*(10**9) for x in xAxis]

#errorYList = [np.random.normal(0, 0.1) for y in range(10)]
errorYList = [0.1 for i in xAxis]


# Reference table of constants
h = 6.62606957*(10**-34)    # Plancks constant
nu = 90*(10**9)             # Frequency
c = 299792458               # Speed of Light
k = 1.3806488*(10**-23)     # Boltzmann constant
TDust = 19.6                # Temperature of dust in Kelvin
TVac = 2.7                  # Temperature of vacuum in Kelvin
nu0 = 1                     # Arbitrary value to fill space in function


# Function lists
dustofLList = [dustRatio(90*(10**9), 150*(10**9))*dustofL(l) for l in xAxis]    # Dust of l
BBofL = extractData("LAMDA Data")                                               # BB(l)


# this just makes it easier to refer to all the YLists
YList = [dustofLList, BBofL]
yMeasured =   [0.05*x + y for x,y in zip(dustofLList,BBofL)]

vectorA = matrixFit(YList, yMeasured, errorYList)

#plt.plot([l for l in angles],yMeasured)
plt.plot(xAxis, [y*vectorA[0] for y in dustofLList])
plt.plot(xAxis, [y*vectorA[1] for y in BBofL])
#plt.plot(np.log(xAxis), np.log([y + z for y, z in zip([y*vectorA[0] for y in dustofLList], [y*vectorA[1] for y in BBofL])]))
#plt.xlim([0,400])
#plt.ylim([-7,0])