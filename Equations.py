# -*- coding: utf-8 -*-
# Equations

import numpy as np


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


def binData(data, xData, xStep=[20]):
    # averages the given data into bins of the given size

    if len(xStep) == 1:                                               # makes xStep a list
        for i in range((len(xData)-(len(xData) % xStep))/xStep):    # yields the floor of the division of (len(nData))/xStep
            xStep.append(xStep[0])
    outList = []
    index, binnum = 0                                                 # index steps through every datapoint. binnum is current bin number
    for i in range((len(xData)-(len(xData) % xStep))/xStep):          # steps throu the bins
        temp = []
        for j in range(xStep[binnum]):                                # steps thru data in each bin
            temp.append(data[index])                                  # appends data to temp list
            index += 1                                                # index always increases, never reset
        binnum += 1                                                   # steps through the xStep for that bin
        outList.append(np.mean(temp))                                 # appends average of current temp list to the outList
    return outList
