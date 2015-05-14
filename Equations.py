# -*- coding: utf-8 -*-
# Equations
import numpy as np

# Equation Functions

# The power law used in some dust equations (mostly a filler function)
def dustFreqPowLaw(nu, nu0 = 1):
    return (nu/nu0)**1.59

# A Plancks Law frequency function to convert the Black Body equation to the right units
def blackbodyConvertofNu(nu, h = 6.62606957*(10**-34), c = 299792458, k = 1.3806488*(10**-23), T = 2.7):
    return 2*(h**2)*(nu**4)*np.exp((h*nu)/(k*T))/(k*(T**2)*(c**2)*((np.exp((h*nu)/(k*T)) - 1)**2))

# Another Plankcs Law equation
def blackbody(nu, h = 6.62606957*(10**-34), c = 299792458, k = 1.3806488*(10**-23), T = 2.7):
    return (2*(h*(nu**3))/(c**2))*(1/(np.exp((h*(nu))/(k*T)) - 1))

# Exponential dust function
def dustofL(l):
    return (l/80.0)**(-0.42)

# Provides the ratio to multiply the dust by when given two frequencies of blackbody
def dustRatio(nu1, nu2):
    return (dustFreqPowLaw(nu1)*blackbodyConvertofNu(nu2))/(dustFreqPowLaw(nu2)*blackbodyConvertofNu(nu1))

def binCenter(lBins):
    out = []
    temp = [lBins[0]]
    for i,x in enumerate(lBins[1:]):
        temp.append(x)
        out.append(0.5*(temp[i]+temp[i+1]))
    return out

# averages the given data into bins of the given size
def binData(data, xData, xStep = 20, bounds = "false", bot = 0, top = 360):
    # This function breaks the data into bins and averages over that bin. It currently only does evenly sized bins.
    if bounds == "true": xData = xData[bot:top]
    out = []
    index = 0
    for i in range((len(xData)-(len(xData)%xStep))/xStep):  # this yields the floor of the division of (len(nData))/xStep
        temp = []
        for j in range(xStep):
            temp.append(data[index])
            index += 1
        out.append(np.mean(temp))
    return out  

# FOR BAR Charts averages the given data into bins of the given size
# def binBarData(data, xData, step = 20):
#     x1 = xData[0]
#     x2 = xData[0] + step
#     out = []
#     temp = []
#     j = 0
#     while x2 <= xData[-1]:
#         temp = []
#         while x1 < x2:
#             temp.append(data[j])
#             j += 1
#             x1 = xData[j]
#         out.append(np.mean(temp))
#         x2 += step
#     while j < len(data):
#         temp.append(data[j])
#         j += 1
#     out.append(np.mean(temp))
#     return out

# returns every nth value of an array
# def everynthlabel(a, start = 0, n = 2):
#     newarray = []
#     for i, x in enumerate(a[start:]):
#         if i%n == 0:
#             newarray.append(x)
#         else:
#             newarray.append('')
#     return newarray
