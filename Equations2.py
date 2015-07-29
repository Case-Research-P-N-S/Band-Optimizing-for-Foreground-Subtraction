# -*- coding: utf-8 -*-
# Equations

'''
THERE IS SOMETHING VERY WRONG WITH THESE EQUATIONS
Make sure the two parameters exp and dustT are going to the right places
     dustT could be actually teh parameter for dust**-0.42
** All 'master' equations are designated with Signal and must only accept 2 inputs
This file holds all the functions for making the theoretical CMB dust data
'''

import numpy as np
from Functions import parameterSplit



##########################################################################################
                                    # BMode

def BModeSignal(BMode, parameters):
    ''' Fits BMode with equation a*BMode+b
        parameters:
            - must be a list of length 1
            - amplitude = paramss[:]

       add +c to the parameters?
    '''
    ampl = parameters
    BModeSignal = (ampl)*BMode
    return np.array(BModeSignal)


##########################################################################################
                                    # Dust

def dustSignal((lList, const), parameters):
    ''' Creates the dust signal
        format: ((lList, const), parameters)
        const holds the constants
        parameters is the list of fit parameters.
            parameters = [amplitude, exponent, dust temperature]
            They are *added* to their respetive theoretical values
            ex: (1+amplitude)*somefunction()

        add +c to the parameters?
    '''
    ampl, exp, dustT = parameters[:]
    dustSignal = [(ampl)*dustPreFactor(const, exp, dustT)*dust(l) for l in lList]
    return np.array(dustSignal)


def dust(lList):  # CHANGE THIS NAME
    ''' Exponential dust function '''
    lList = np.float64(lList)
    dust = (lList/80)**(-0.42)
    return dust


def dustPreFactor(const, exp, dustT):
    '''
        SHOULD NOT BE NU1!!
    '''
    # getting out the constants
    nu1, nu0, List = const['nu1'], const['nu0'], const['List']     # ** SHOULD NOT BE NU1!! **
    # finding the dust frequency powerlaw
    powerlaw = dustFreqPowLaw(nu1, nu0, exp)
    # finding the blackbody curve
    blackbody = blackbody_convert(nu1, List, dustT)
    # makeing the dust pre-factor
    dustPreFactor = powerlaw*blackbody
    return dustPreFactor


def dustFreqPowLaw(nu, nu0, exp):
    '''
        the exponent is added to the theoretical value of 1.59

        should exponent be np.float64 ?
    '''
    nu, nu0 = np.float64(nu), np.float64(nu0)
    powerlaw = (nu/nu0)**(1.59+exp)
    return powerlaw


def blackbody_nu(nu, List, T):
    ''' Another Planck's Law equation
        nu, h=6.62606957*(10**-34), c=299792458, k=1.3806488*(10**-23), T=2.7
        the T is added to the mean dust value of 19.6 K
    '''
    h, c, k, TVac, TDust = List[:]
    blackbody_Nu = (2*(h*(nu**3))/(c**2))*(1/(np.exp((h*(nu))/(k*(TDust+T))) - 1))
    return blackbody_Nu


def blackbody_convert(nu, List, T):
    ''' A Plancks Law frequency function to convert the Black Body equation to the right units
        nu,  const = [h, c, k, TVac, TDust]
        TDust=19.6, h=6.62606957*(10**-34), c=299792458, k=1.3806488*(10**-23), TVac = 2.7
    '''
    h, c, k, TVac, TDust = List[:]
    return 2*(h**2)*(nu**4)*np.exp((h*nu)/(k*TVac))/(k*(TVac**2)*(c**2)*((np.exp((h*nu)/(k*TVac)) - 1)**2))



##########################################################################################
                                    # Total Signal

def totalSignal((lList, const, BMode_data), parameters):  # Change name of inputs
    ''' Creates the total theoretical signal
    '''
    # creating parameter inputs
    params_BM, params_d = parameterSplit(parameters)
    # getting functions
    BMode = BModeSignal(BMode_data, params_BM)
    dust = dustSignal((lList, const), params_d)
    # adding into one signal
    signal = dust+BMode
    return np.array(signal)
