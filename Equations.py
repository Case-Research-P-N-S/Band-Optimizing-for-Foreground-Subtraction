# -*- coding: utf-8 -*-
# Equations
import numpy as np

# Equation Functions


def dustFreqPowLaw(nu, nu0=1):
    # The power law used in some dust equations (mostly a filler function)
    return (nu/nu0)**1.59


def blackbodyConvertofNu(nu, h=6.62606957*(10**-34), c=299792458, k=1.3806488*(10**-23), T=2.7):
    # A Plancks Law frequency function to convert the Black Body equation to the right units
    return 2*(h**2)*(nu**4)*np.exp((h*nu)/(k*T))/(k*(T**2)*(c**2)*((np.exp((h*nu)/(k*T)) - 1)**2))


def blackbody(nu, h=6.62606957*(10**-34), c=299792458, k=1.3806488*(10**-23), T=2.7):
    # Another Plankcs Law equation
    return (2*(h*(nu**3))/(c**2))*(1/(np.exp((h*(nu))/(k*T)) - 1))


def dustofL(l):
    # Exponential dust function
    return (l/80.0)**(-0.42)


def dustRatio(nu1, nu2):
    # Provides the ratio to multiply the dust by when given two frequencies of blackbody
    return (dustFreqPowLaw(nu1)*blackbodyConvertofNu(nu2))/(dustFreqPowLaw(nu2)*blackbodyConvertofNu(nu1))


def binCenter(lBins):
    out = []
    temp = [lBins[0]]
    for i, x in enumerate(lBins[1:]):
        temp.append(x)
        out.append(0.5*(temp[i]+temp[i+1]))
    return out


def binData(data, xData, xStep=20, bounds="false", bot=0, top=360):
    # averages the given data into bins of the given size
    #  This function breaks the data into bins and averages over that bin.
    #  It currently only does evenly sized bins.
    #  Check out Bar Chart function for better bethod?
    if bounds == "true":
        xData = xData[bot:top]
    out = []
    index = 0
    for i in range((len(xData)-(len(xData) % xStep))/xStep):  # this yields the floor of the division of (len(nData))/xStep
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
