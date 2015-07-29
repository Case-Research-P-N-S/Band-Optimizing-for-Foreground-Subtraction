# -*- coding: utf-8 -*-
# Main execution file

'''
Document Info
- Function of L
'''

import matplotlib.pyplot as plt
import fittingFunctions as fit         # best fit functions
import Equations2 as eqn               # file with most of the used equations
import Functions as fn                 # file with most of the functions
import plottingFunctions as pltfn      # handles all plotting
# import numpy as np
from Classes import DataClass          # all the classes
from Dictionaries import make_lDict, make_Const  # lDict and constants


##########################################################################################
                            # Files, Constants & Parameters

# Files
lamda_data_filename = 'LAMDA Data'
measured_bin_filename = 'results.txt'

# making a dictionary with all the angle l values as the x-axis
lDict = make_lDict(lamda_data_filename)

# Reference dictionary of constants
const = make_Const()

# Best Fit Parameter Inputs
params_BM = fn.npFloat([1])
params_D = fn.npFloat([1, 0, 0])
parameters = fn.concatenate(params_BM, params_D)



##########################################################################################
                                      # Data

# ----------------------------------------
            # Theory Data
# BMode
BMode = DataClass('BMode',       {'model': 'raw',
                                  'equation': eqn.BModeSignal,
                                  'eqinput': fn.extractData(lamda_data_filename, 3)[lDict['refMin']:lDict['refMax']], 'params': params_BM,
                                  'error': lambda x: fn.error(x, pct=0.2, mtd=1),
                                  'data': fn.extractData(lamda_data_filename, 3)[lDict['refMin']:lDict['refMax']],
                                  'xaxis': lDict['lList']})
BMode.add_model(                 {'model': 'bin',
                                  'equation': eqn.BModeSignal,  # is this the equation?
                                  'eqinput': fn.binData(BMode.raw.data, lDict['lList'], lDict['lStep']), 'params': params_BM,
                                  'error': lambda x: fn.error(x, pct=0.2, mtd=1),
                                  'data': fn.binData(BMode.raw.data, lDict['lList'], lDict['lStep']),
                                  'xaxis': lDict['lBinCent']})

# Dust
Dust = DataClass('Dust',         {'model': 'raw',
                                  'equation': eqn.dustSignal,
                                  'eqinput': (lDict['lList'], const), 'params': params_D,
                                  'error': lambda x: fn.error(x, pct=0.2, mtd=1),
                                  'xaxis': lDict['lList']})
Dust.add_model(                  {'model': 'bin',
                                  'equation': eqn.dustSignal,  # is this the equation or fn.binData?
                                  'eqinput': (lDict['lBinCent'], const), 'params': params_D,
                                  'data': fn.binData(Dust.raw.data, lDict['lList'], lDict['lStep']), # binning data & re-evaluating are < 1% different
                                  'error': lambda x: fn.error(x, pct=0.2, mtd=1),
                                  'xaxis': lDict['lBinCent']})

# Theory
Theory = DataClass('Theory',     {'model': 'raw',
                                  'equation': eqn.totalSignal,
                                  'eqinput': (lDict['lList'], const, BMode.raw.data),
                                  'params': parameters,
                                  'data': BMode.raw.data + Dust.raw.data,  # it's faster to add than re-evaluate with the equation
                                  'd_data': BMode.raw.d_data + Dust.raw.d_data,
                                  'xaxis': lDict['lList']},
                                 {'model': 'bin',
                                  'equation': eqn.totalSignal,
                                  'eqinput': (lDict['lBinCent'], const, BMode.bin.data), 'params': parameters,
                                  'data': BMode.bin.data + Dust.bin.data,  # it's faster to add than re-evaluate with the equation
                                  'd_data': BMode.bin.d_data + Dust.bin.d_data,
                                  'xaxis': lDict['lBinCent']},
                                 {'model': 'rawList',
                                  # 'equation': [BMode.raw.equation, Dust.raw.equation],
                                  # 'params': [params_BM, params_D],
                                  'data': [BMode.raw.data, Dust.raw.data],
                                  'error': [BMode.raw.d_data, Dust.raw.d_data]},  # *** d_data or error?
                                 {'model': 'binList',
                                  # 'equation': [BMode.bin.equation, Dust.bin.equation],
                                  # 'params': [params_BM, params_D],
                                  'data': [BMode.bin.data, Dust.bin.data],
                                  'error': [BMode.bin.d_data, Dust.bin.d_data]})  # *** d_data or error?

# ----------------------------------------
            # Measured Data
# Measured
Measured = DataClass('Measured', {'model': 'raw',
                                  'data': fn.dudata(Theory.raw.data, 0.1),
                                  'error': fn.extractData(measured_bin_filename, 2)[lDict['refMin']:lDict['refMax']],
                                  'xaxis': lDict['lList']})
Measured.add_model(              {'model': 'bin',
                                  'data': fn.binData(Measured.raw.data, lDict['lList'], lDict['lStep']),
                                  'error': lambda x: fn.error(x, pct=0.02, mtd=1),  # *** replace with real errors
                                  'xaxis': lDict['lBinCent']})

# ----------------------------------------
            # Processed Data
# Fit Coefficients
ChiSqFit = fit.ChiSqOpt(BMode.bin, Dust.bin, Measured.bin, Theory.bin.params)
Theory.bin.parameters, BMode.bin.params, Dust.bin.params = ChiSqFit.fit('combo', method='Nelder-Mead')  # ** retire outputs and put in a fn.updata_params?**
print Theory.bin.parameters

# Best Fit
# BestFit = DataClass('Best Fit', {'model': 'raw', 'data': (Dust.raw.data*Dust.raw.params + BMode.raw.data*BMode.raw.params)})
BestFit = DataClass('Best Fit')
BestFit.add_model({'model': 'bin',  # different than Theory since parameters changed
                   'equation': eqn.totalSignal,
                   'eqinput': (lDict['lBinCent'], const, BMode.bin.data), 'params': Theory.bin.parameters,
                   'error': lambda x: fn.error(x, pct=0.02, mtd=1),
                   'xaxis': lDict['lBinCent']})

# Temporary:
BMode.raw.params, Dust.raw.params = BMode.bin.params, Dust.bin.params

# Updating Fit Data & d_Fit Data
fn.update_fitdata((BMode, 'raw', 'bin'), (Dust, 'raw', 'bin'), (Theory, 'raw', 'bin', 'rawList', 'binList'))
fn.update_d_fitdata((BMode, 'raw', 'bin'), (Dust, 'raw', 'bin'), (Theory, 'raw', 'bin', 'rawList', 'binList'))



##########################################################################################
                                    # Monte Carlo
# performing MC
MCData = fit.MCChiSqFit(BMode.bin, Dust.bin, Theory.bin, iterate=1e3, method='Nelder-Mead')  # Monte Carlo of _________
# plotting histograms and parameter correlations
pltfn.plotHisto(MCData, [BMode.bin.params, Dust.bin.params])
pltfn.plotCorrelation(MCData)




##########################################################################################
                                    # Outputs

# ----------------------------------------
            # Plotting Stuff
# Fit Plots:
pltfn.plotErrorbar(lDict['lBinCent'], Measured.bin, BMode.bin, Dust.bin, BestFit.bin, Theory.bin)
# pltfn.plotScatter(lDict['lList'], Measured.raw, BMode.raw, Dust.raw, BestFit.raw, Theory.raw)

# Quick Plots
fig = plt.figure()
plt.plot(lDict['lList'], BMode.raw.data, label='Raw')
plt.plot(lDict['lList'], BMode.raw.fitdata, label='Fit')
plt.legend()
plt.title('BMode')
fig.savefig('BMode.png')

fig = plt.figure()
plt.plot(lDict['lList'], Measured.raw.data, label='Measured.raw')
plt.plot(lDict['lBinCent'], Measured.bin.data, label='Measured.bin')
plt.legend()
plt.title('Measured')
fig.savefig('Measured.png')

# ----------------------------------------
            # seeing some outputs
print "params {}".format([BMode.bin.params, Dust.bin.params])
print "BMode Ampl - Ampl Mean = {}".format(BMode.bin.params[0] - MCData.params[0])
print "Dust Ampl - Ampl Mean = {}".format(Dust.bin.params[0] - MCData.params[2])

# New-Style Plots
# figure, axis = pltfn.makePlot(lDict['lList'], Measured.raw, BestFit.raw)
# figure2, axis2 = pltfn.makePlot(lDict['lList'], Measured.raw, BMode.raw, Dust.raw, BestFit.raw, Theory.raw)
# pltfn.ComparePlots(axis, axis2)


''' NEED TO DO:
- make Equations like Equations 2, so that can switch from Equations 2 to Equations.
- change dust equation to something else
- Make better best fitter for the correlation plots


    Maybe Do:
- make all params be in form [[BMode[:]], [Dust[:]]] rather than [BMode[:], Dust[:]]
- Then wouldn't need paramsList in plotHisto. replace with MCData.parameters
'''
