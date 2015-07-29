# -*- coding: utf-8 -*-
# All the Fitting Functions

import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt
from Functions import parameterSplit

# ----- Fit Finders -----


# Line of Best Fit (using Least Squares Regression):
def polyfit(xList, yList, degree=1, rsqr=False):
    ''' Line of Best Fit (using Least Squares Regression):
    Description: A function that takes in two lists of equal length, corresponding
    to the x and y coords of a graph, and returns a list containing
    the intercept, slope and r^2 of the line of best fit to that graph
    '''
    coeffs = np.polyfit(xList, yList, degree)
    b = coeffs[0]  # highest degree
    a = coeffs[1]  # lowest degree
    if rsqr is True:
        # calculating correlation coefficient. r = b *(stdev yList / stdev xList)
        r = b * (np.std(yList)/np.std(xList))
        # calculating r-square value
        rSquare = np.square(r)
        return [a, b, rSquare]
    else:
        return [a, b]


# ---------- Least Squares Regression ----------
class matrixFit(object):
    """docstring for matrixFit"""
    def __init__(self, functionList, fitTo, errorFitTo):
        super(matrixFit, self).__init__()
        self.fList = functionList  # list of funcitons to fit with
        self.fitTo = [fitTo]       # list to fit to (stores all previous versions of self)
        self.d_FitTo = errorFitTo  # error in fitTo
        self.results = []          # list of all best-fit parameters
        self.params = None         # current best-fit parameters

    def fit(self, output='list'):
        ''' Generates normalized A vector using general least squares regression fit
            Description: A function that takes in 3 lists, corresponding to:
                a composite list of usable functions (in the form of y-coordinates)
                the function to which the former composite list should be fit to
                and the error in the function
            Returns a list containing the fit parameters for the composite list of functions.
                if output = 'split', fit will return [[params_BM], [params_d]]
                if output = 'list', fit will return [params_BM[:], params_d[:]]
        '''
        # Creates the A matrix for use in determining the constants
        columns = len(self.fList)
        rows = len(self.d_FitTo)
        # initialize the matrix with float values of 0
        matrixA = np.matrix([[0.0 for i in self.fList] for i in self.d_FitTo])
        # initialize the list used as temporary storage for the row values
        tempList = np.empty(columns)

        for i in range(rows):
            for j in range(columns):
                s = self.d_FitTo[j]
                tempList[j] = self.fList[j][i]/s
            matrixA[i] = tempList

        # initialization and assignment of vector b
        vectorB = np.empty(len(self.fitTo[-1]))
        # fills empty vector with measured/error
        for y, s, i in zip(self.fitTo[-1], self.d_FitTo, range(len(self.fitTo[-1]))):
            vectorB[i] = y/s
        # ((A transpose) dot (A))
        tempA = np.dot(matrixA.T, matrixA)
        # inverse of a matrix
        tempB = tempA.I
        # Dot Product of matrix and b vector
        tempC = np.dot(tempB, matrixA.T)
        # Turns result into python array
        answer = np.dot(tempC, vectorB)

        ampls = np.array(answer)[0]
        self.params = np.array([(1-ampls[0]), 0, (1-ampls[1]), 0, 0])
        self.results.append(self.params)

        if output == 'list':  # fit will return [params_BM[:], params_d[:]] as a unified list
            return self.params
        elif output == 'split':  # fit will return [[params_BM], [params_d]]
            return parameterSplit(self.params)
        elif output == 'combo':
            split = parameterSplit(self.params)
            return self.params, split[0], split[1]

    def finalize(self):
        self.results = np.array(self.results)
        self.params = np.mean(self.results, axis=0)

    # Example for Calling matrixFit
    # matrixFit = fit.matrixFit(Theory.binList.data, Measured.bin.data, Measured.bin.d_data)
    # Theory.bin.parameters, BMode.bin.params, Dust.bin.params = matrixFit.fit('combo')  # ** retire outputs and put in a fn.updata_params?**
    # print Theory.bin.parameters


# ---------- Chi Square Optimizer ----------
class ChiSqOpt(object):
    """docstring for ChiSqOpt
    """
    def __init__(self, BMode, Dust, Measured, parameters):
        ''' takes all of the input necessary to do a Chi-Sq  optimization
        '''
        self.BMode = BMode  # BMode object -- BMode.data, BMode.equation, BMode.eqinput (Bmode.data is faster), BMode.params
        self.dust = Dust  # Dust object -- Dust.data, Dust.equation, Dust.eqinput, Dust.params
        self.measured = Measured  # measured object -- Measured.data, Measured.d_data
        self.params = parameters  # current best fit parameters
        self.results = []  # empty list of results

    # Theory Constructions of the Data for fits
    def residual(self, params_BM, params_d):
        '''
            needs parameters as input since they will be changed by the fitter
        '''
        # finding the model
        model = self.BMode.equation(self.BMode.data, params_BM)
        model += self.dust.equation(self.dust.eqinput, params_d)
        # finding the residual
        residual = self.measured.data - model
        return residual

    def chisqfc(self, parameters):
        # preparing inputs
        params_BM, params_d = parameterSplit(parameters)
        # finding the residual
        residual = self.residual(params_BM, params_d)
        # finding the chi-squared
        chisq = np.sum((residual/self.measured.d_data)**2)
        return chisq

    def fit(self, output='list', **kw):
        ''' needs scipy.optimize imported as opt
        '''
        # selection of optimizaiton method
        method, options = self.optimization_options(kw)

        result = opt.minimize(self.chisqfc, self.params, method=method, options=options)
        self.params = np.array(result.x)
        self.results.append(result.x)  # appending results to self.results

        if output == 'list':  # fit will return [params_BM[:], params_d[:]] as a unified list
            return self.params
        elif output == 'split':  # fit will return [[params_BM], [params_d]]
            return parameterSplit(self.params)
        elif output == 'combo':
            split = parameterSplit(self.params)
            return self.params, split[0], split[1]

    def optimization_options(self, kw):
        if 'method' in kw:
            method = kw.get('method')
        else:
            method = 'nelder-mead'  # choose a better method as default?
        if method is None:
            method = 'nelder-mead'
        # giving a full dict of options
        if 'options' in kw:
            options = kw.get('options')
            if options is None:
                options = {'maxiter': 1e5, 'maxfev': 1e5}  # pre-populating options
                if 'maxiter' in kw:  # maximum number of iterations
                    options['maxiter'] = kw.get('maxiter')
                if 'maxfev' in kw: # maximum number of function evaluations
                    options['maxfev'] = kw.get('maxfev')
        else:  # giving options individually
            options = {'maxiter': 1e5, 'maxfev': 1e5}  # pre-populating options
            if 'maxiter' in kw:  # maximum number of iterations
                options['maxiter'] = kw.get('maxiter')
            if 'maxfev' in kw: # maximum number of function evaluations
                options['maxfev'] = kw.get('maxfev')
        return method, options

    def finalize(self):
        self.results = np.array(self.results)
        self.params = np.mean(self.results, axis=0)

    # def fit_1line(self, method, options):
    #     '''
    #     '''
    #     result = opt.minimize(self.chisqfc, self.params, method=method, options=options)
    #     self.results.append(result.x) # appending results to self.results
    #     return result

    # def optimize_0in(self):
    #     '''
    #     '''
    #     result = opt.minimize(self.function, self.params)
    #     self.results.append(result.x) # appending results to self.results
    #     return result

    def _plot(self, xdata):
        '''
        '''
        params_BM = self.params[0, 1]
        params_d = self.params[2:]

        fig = plt.figure()
        theplot = fig.add_axes((.1, .28, .8, .65))
        theplot.set_xticklabels([])
        measured, = plt.plot(xdata, self.measured, label='measured')
        fit, = plt.plot(xdata, self.BModefc(params_BM)+self.dust(params_d), label='fit')
        plt.legend()
        plt.grid()

        fig.add_axes((.1, .1, .8, .15))
        plt.plot(xdata, self.residual(params_BM, params_d), label='residual')
        plt.locator_params(nbins=4)

        fig.savefig('ChiSqOpt Plot.png')




#######################################################################################
#                                 Monte-Carlos

# Matrix Fit
def MCMatrixFit(TList, measured, std, iterate=10**4, **kw):
    '''
    '''
    # Initializing Fit
    MC = matrixFit(TList, None, std)
    # Monte Carlo Method
    for i in range(iterate):
        # generating yList
        yList = [np.random.normal(m, err) for m, err in zip(measured, std)]
        # adding new fake 'measured' data
        MC.fitTo.append(yList)
        # Doing the best fit
        MC.fit()
    # Finalizing Fit
    MC.finalize()

    return MC

    # Example:
    # MCData = fit.MCMatrixFit(Theory.binList.data, Theory.bin.fitdata, Theory.bin.d_fitdata, iterate=10**4)  # Monte Carlo of _________


def MCChiSqFit(BMode, Dust, measured, iterate=10**4, **kw):
    '''
    '''
    if 'method' in kw:
        method = kw.get('method')
    else:
        method = None
    # Initializing Fit
    MC = ChiSqOpt(BMode, Dust, measured, measured.params)
    MC.measured.data = []
    # Monte Carlo Method
    for i in range(int(iterate)):
        print i
        # generating yList
        yList = [np.random.normal(m, err) for m, err in zip(measured.fitdata, measured.d_fitdata)]
        # adding new fake 'measured' data
        MC.measured.data = yList
        # Doing the best fit
        MC.fit(method=method)
    # Finalizing Fit
    MC.finalize()

    return MC
