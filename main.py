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
YList = [dustofLList, BBofL]

yMeasured =   [x+y+np.random.normal(x+y,(x+y)/10) for x,y in zip(dustofLList,BBofL)] #the added noise is fake data until r
errorYMeasured = [0.1 for i in xAxis]

vectorA = matrixFit(YList, yMeasured, errorYMeasured)

plt.close('all')
plt.subplot(3,1,1)
plt.plot(xAxis,[y for y in yMeasured])
plt.subplot(3,1,2)
plt.plot(xAxis, [y*vectorA[0] for y in dustofLList])
plt.plot(xAxis, [y*vectorA[1] for y in BBofL])
plt.subplot(3,1,3)
plt.yscale('log')
plt.xscale('log')
plt.plot(xAxis,[y*vectorA[0] for y in dustofLList])
plt.plot(xAxis, [y*vectorA[1] for y in BBofL])

print vectorA