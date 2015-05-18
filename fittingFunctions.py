# -*- coding: utf-8 -*-
# Generalized Least Squares Regression Fit

import numpy as np


def linearFit(xList, yList, degree=1):
    # Line of Best Fit (using Least Squares Regression):
    '''
    Description: A function that takes in two lists of equal length, corresponding
    to the x and y coords of a graph, and returns a list containing
    the intercept, slope and r^2 of the line of best fit to that graph
    '''
    # error if xlist and ylist are different lengths
    if len(xList) != len(yList):
        print "Error: incompatible lists"
        raise Exception("Incompatible List Lengths")

    '''
    given x-values, y-values, and relationship degree,
    polyfit returns list of polynomial coefficients
    starting with coefficient with the highest power
    '''
    p = np.polyfit(xList, yList, degree)
    b = p[0]  # highest degree
    a = p[1]  # lowest degree
    # calculating correlation coefficient. r = b *(stdev yList / stdev xList)
    r = b * (np.std(yList)/np.std(xList))
    # calculating r-square value
    rSquare = np.square(r)
    return [a, b, rSquare]


def matrixFit(functionList, fitTo, errorFitTo):
    # Generates normalized A vector using general least squares regression fit

    # Creates the A matrix for use in determining the constants
    columns = len(functionList)
    rows = len(errorFitTo)
    # initialize the matrix with float values of 0
    matrixA = np.matrix([[0.0 for i in functionList] for i in errorFitTo])
    # initialize the list used as temporary storage for the row values
    tempList = np.empty(columns)

    for i in range(rows):
        for j in range(columns):
            s = errorFitTo[j]
            tempList[j] = functionList[j][i]/s
        matrixA[i] = tempList

    # initialization and assignment of vector b
    vectorB = np.empty(len(fitTo))
    # fills empty vector with measured/error
    for y, s, i in zip(fitTo, errorFitTo, range(len(fitTo))):
        vectorB[i] = y/s
    # ((A transpose) dot (A))
    tempA = np.dot(matrixA.T, matrixA)
    # inverse of a matrix
    tempB = tempA.I
    # Dot Product of matrix and b vector
    tempC = np.dot(tempB, matrixA.T)
    # Turns result into python array
    finalTemp = np.dot(tempC, vectorB)
    fitCoeff = np.array(finalTemp)[0]

    return fitCoeff


def avgMatrixFit(functionList, data, std, iterate=1000):
# Generates average normalized A vector by iterating and averaging matrixFit (least squares regression fit)
    aList = []
    bList = []
    for i in range(iterate):
        # adding noise to the data
        noisyData = [np.random.normal(m, err) for m, err in zip(data, std)]
        # getting best fit
        results = matrixFit(functionList, noisyData, std)
        # creating list of fit coeffictients
        aList.append(results[0])
        bList.append(results[1])
    # getting the mean of fit coefficients
    aMean = np.mean(aList, dtype=np.float64)
    bMean = np.mean(bList, dtype=np.float64)
    # getting error in the fit coefficients
    aStd = np.std(aList)
    bStd = np.std(bList)

    return [aMean, bMean, aStd, bStd]
