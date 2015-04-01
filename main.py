import numpy as np
import matplotlib.pyplot as plt
from dataExtractor import extractData
from GeneralizedLeastSquaresFit import matrixFit

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

# Equation Functions
def dustFreqPowLaw(nu, nu0 = 1):
    return (nu/nu0)**1.59

def blackbodyConvertofNu(nu, h = 6.62606957*(10**-34), c = 299792458, k = 1.3806488*(10**-23), T = 2.7):
    return 2*(h**2)*(nu**4)*np.exp((h*nu)/(k*T))/(k*(T**2)*(c**2)*((np.exp((h*nu)/(k*T)) - 1)**2))

def blackbody(nu, h = 6.62606957*(10**-34), c = 299792458, k = 1.3806488*(10**-23), T = 2.7):
    return (2*(h*(nu**3))/(c**2))*(1/(np.exp((h*(nu))/(k*T)) - 1))

def dustofL(l):
    return (l/80.0)**-0.42

def dustRatio(nu1, nu2):
    return (dustFreqPowLaw(nu1)*blackbodyConvertofNu(nu2))/(dustFreqPowLaw(nu2)*blackbodyConvertofNu(nu1))


# Function lists
dustofLList = [dustRatio(90*(10**9), 150*(10**9))*dustofL(l) for l in xAxis]    # Dust of l
BBofL = extractData("LAMDA Data")                                               # BB(l)


#------------------------------------------
# Matrix Function


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