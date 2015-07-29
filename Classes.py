# -*- coding: utf-8 -*-
# All the Classes

import numpy as np
import matplotlib.pyplot as plt
from types import FunctionType, NoneType

'''
PROBLEM with _model. Can't get it to access all the data in DataClass
'''


class DataClass(object):
    ''' must give a name
        can give a model (ex raw), fullname, and info
        - all model properties must be args
        - all non-model properties must be kw
        - Model Properties:
            - must be an arg
            - must be a dict
            - must have a material property types with key 'model'
            - may have data with key 'data
            - may have params with key 'params'
            - may have error with key 'error'
            ex: {'model': 'modelname', 'data': [data], 'error': 2}
        - fullname, and info must be strings
    '''
    def __init__(self, name, *args, **kw):
        super(DataClass, self).__init__()
        self.name = name
        self.fullname = name
        # Models
        for i, Dict in enumerate(args):
            self.add_model(Dict)

        # Non-Model Properties
        if 'fullname' in kw:                     # full name
            self.fullname = kw.get('fullname')
        if 'info' in kw:                         # info is any note. should be str
            self.info = kw.get('info')
        else:
            self.info = None

    def add_info(self, info=None, **kw):
        'adds info to a given model. if no info passed, adds as None'
        if 'info' in kw:
            self.info = kw.get('info')
        else:
            self.info = info

    def add_fullname(self, fullname=None, **kw):
        'adds fullname to a given model. if no fullname passed, adds as None'
        if 'fullname' in kw:
            self.fullname = kw.get('fullname')
        else:
            self.fullname = fullname

    def add_model(self, Dict, **kw):
        ''' adds a data model
            needs: modelname (as kwarg or in main dict)
            can be given any of: data, params, & error
                - in main dict or in kwarg
            data must be a list
            ex: add_model({'matProp': 'thermCond', 'name'= 'NIST', 'eq': lambda x: x, 'eqinput': [1, 23]})
            add_model supports: data as data in dict or kwarg
                                params as params in dict or kwarg
                                error as error in dict or kwarg
            kwarg has highest priority, then arg, then dict entries
        '''

        if not isinstance(Dict, (dict, NoneType)):
            if Dict is None:
                Dict = {}
            else:
                print 'Error: dict needs to be type dict or None'
                return

        # Model
        if 'model' in kw:
            model_name = kw.get('model')
        elif 'model' in Dict:
            model_name = Dict['model']
        else:
            print 'Error: need to pass a model name'
            return
        if isinstance(model_name, str):
            setattr(self, model_name, _model(self.name, model_name))  # *** temporary solution? ***
        else:
            print 'Error: model must be str'
            return

        # Equation
        if 'equation' in kw:
            equation = kw.get('equation')
        elif 'equation' in Dict:
            equation = Dict['equation']
        else:
            equation = None
        if isinstance(equation, (FunctionType, NoneType, list, np.ndarray)):
            self.add_equation(model_name, equation)
        else:
            print "Error: equation needs to be type function, None or list"
            print self.name, type(equation)
            return

        # eqinput
        if 'eqinput' in kw:
            eqinput = kw.get('eqinput')
        elif 'eqinput' in Dict:
            eqinput = Dict['eqinput']
        else:
            eqinput = None
        self.add_eqinput(model_name, eqinput)  # *** prob need some ifinstance() check ***

        # params
        if 'params' in kw:
            parameters = kw.get('params')
        elif 'params' in Dict:
            parameters = Dict['params']
        else:
            parameters = None
        if isinstance(parameters, (list, np.ndarray, NoneType)):
            self.add_params(model_name, parameters)
        else:
            print 'Error: params needs to be type list or None'
            return

        # Data
        if 'data' in kw:
            data = kw.get('data')
        elif 'data' in Dict:
            data = Dict['data']
        else:
            try:
                data = equation(eqinput, parameters)
            except:
                data = None
        if isinstance(data, (list, np.ndarray, NoneType)):
            self.add_data(model_name, data)
        else:
            print 'Error: data needs to be type list or None'
            print self.name
            return

        # Error
        # needs to be after eq, eqinput, params, and data since it can use those to calculate the error
        if 'error' in kw:
            error = kw.get('error')
        elif 'error' in Dict:
            error = Dict['error']
        else:
            error = None
        if isinstance(error, (int, float, list, np.ndarray, FunctionType, NoneType)):
            self.add_error(model_name, error)
        else:
            print 'Error: error nees to be type number, list, function or None'
            print self.name
            return

        # Error in Data
        if 'd_data' in kw:
            d_data = kw.get('d_data')
        elif 'd_data' in Dict:
            d_data = Dict['d_data']
        else:
            d_data = None
        if isinstance(d_data, (int, float, list, np.ndarray, NoneType)):
            self.add_d_data(model_name, d_data)
        else:
            print 'Error: d_data nees to be type number, list, or None'
            return

        # Fit Data
        if 'fitdata' in kw:
            fitdata = kw.get('fitdata')
        elif 'fitdata' in Dict:
            fitdata = Dict['fitdata']
        else:
            fitdata = None
        if isinstance(fitdata, (list, np.ndarray, NoneType)):
            self.add_fitdata(model_name, fitdata)
        else:
            print 'Error: fitdata needs to be type list or None'
            print self.name
            return

        # Error in Fit Data
        if 'd_fitdata' in kw:
            d_fitdata = kw.get('d_fitdata')
        elif 'd_fitdata' in Dict:
            d_fitdata = Dict['d_fitdata']
        else:
            d_fitdata = None
        if isinstance(d_fitdata, (list, np.ndarray, NoneType)):
            self.add_d_fitdata(model_name, d_fitdata)
        else:
            print 'Error: d_fitdata needs to be type list or None'
            print self.name
            return

        # xaxis
        if 'xaxis' in kw:
            xaxis = kw.get('xaxis')
        elif 'xaxis' in Dict:
            xaxis = Dict['xaxis']
        else:
            xaxis = None
        if isinstance(xaxis, (list, np.ndarray, NoneType)):
            self.add_xaxis(model_name, xaxis)
        else:
            print 'Error: xaxis nees to be type list or None'
            print self.name
            return

    def add_equation(self, *args, **kw):
        ''' add an equation to a model.
            called material.add_equation(property, modelname, equation) (with either as a kwarg)
            note: modelname must be a string
            Cannot give something as both an arg and a kwarg!
        '''
        arg_count = 0
        if 'model' in kw:
            model = getattr(self, kw.get('model'))
        else:
            model = getattr(self, args[arg_count])
            arg_count += 1
        if 'equation' in kw:
            equation = kw.get('equation')
        else:
            equation = args[arg_count]
            arg_count += 1
        model.equation = equation

    def add_eqinput(self, *args, **kw):
        ''' adds equation input to a model.
            called as material.add_params(property, modelname, params)  (with either as a kwarg)
            Cannot give something as both an arg and a kwarg!
        '''
        arg_count = 0
        if 'model' in kw:
            model = getattr(self, kw.get('model'))
        else:
            model = getattr(self, args[arg_count])
            arg_count += 1
        if 'eqinput' in kw:
            eqinput = kw.get('eqinput')
        else:
            eqinput = args[arg_count]
            arg_count += 1
        model.eqinput = eqinput

    def add_params(self, *args, **kw):
        ''' adds equation input to a model.
            called as material.add_params(property, modelname, params)  (with either as a kwarg)
            Cannot give something as both an arg and a kwarg!
        '''
        arg_count = 0
        if 'model' in kw:
            model = getattr(self, kw.get('model'))
        else:
            model = getattr(self, args[arg_count])
            arg_count += 1
        if 'params' in kw:
            params = kw.get('params')
        else:
            params = args[arg_count]
            arg_count += 1
        model.params = params

    def add_error(self, *args, **kw):
        ''' adds error equation to a model.
            Cannot give something as both an arg and a kwarg!
        '''
        arg_count = 0
        if 'model' in kw:
            model = getattr(self, kw.get('model'))
        else:
            model = getattr(self, args[arg_count])
            arg_count += 1
        if 'error' in kw:
            error = kw.get('error')
        else:
            error = args[arg_count]
            arg_count += 1
        model.error = error

    def add_data(self, *args, **kw):
        ''' adds the data to a model.
            called material.add_data(property, modelname, equation)  (with either as a kwarg)
            note:  modelname must be a string
            Cannot give something as both an arg and a kwarg!
        '''
        arg_count = 0
        if 'model' in kw:
            model = getattr(self, kw.get('model'))
        else:
            model = getattr(self, args[arg_count])
            arg_count += 1
        if 'data' in kw:
            data = kw.get('data')
        else:
            data = args[arg_count]
            arg_count += 1
        model.data = np.array(data)

    def add_d_data(self, *args, **kw):
        ''' adds error to the data.
            adding d_data as None makes it first try to add as model.error(model.data)
            not giving a d_data makes it first try to add as model.error(model.data) then as model.error
            Cannot give something as both an arg and a kwarg!
        '''
        arg_count = 0
        if 'model' in kw:
            model = getattr(self, kw.get('model'))
        else:
            model = getattr(self, args[arg_count])
            arg_count += 1
        if 'd_data' in kw:
            d_data = kw.get('d_data')
            model.d_data = np.array(d_data)
        else:  # d_data not a kw
            try:  # d_data maybe arg
                d_data = args[arg_count]
            except:  # d_data not given anywhere
                try:  # evaulate for the error in the data
                    model.d_data = np.array(model.error(model.data))
                except TypeError:  # already list, so add error in data
                    model.d_data = np.array(model.error)
            else:  # error is an arg
                if d_data is None:
                    try:  # evaulate for the error in the data
                        model.d_data = np.array(model.error(model.data))
                    except TypeError:  # already list, so add error in data
                        model.d_data = np.array(model.error)
                else:
                    model.d_data = np.array(d_data)

    def add_fitdata(self, *args, **kw):
        ''' adds the data, evaulated with the best fit parameters, to a model.
            called material.add_fitdata(property, modelname, equation)  (with either as a kwarg)
            note:  modelname must be a string
            Cannot give something as both an arg and a kwarg!
        '''
        arg_count = 0
        if 'model' in kw:
            model = getattr(self, kw.get('model'))
        else:
            model = getattr(self, args[arg_count])
            arg_count += 1
        if 'fitdata' in kw:
            fitdata = kw.get('fitdata')
            model.fitdata = np.array(fitdata)
        else:  # fitdata not a kw
            try:  # fitdata maybe arg
                fitdata = args[arg_count]
            except:  # fitdata not given anywhere
                try:  # evaulate equation with parameters
                    model.fitdata = np.array(model.equation(model.eqinput, model.params))
                except:
                    print model.name, model.modelname, 'fitdata added as None'
                    model.fitdata = None
            else:  # fitdata is an arg
                if fitdata is None:
                    try:  # evaulate equation with parameters
                        model.fitdata = np.array(model.equation(model.eqinput, model.params))
                    except:  # already list, so add error in data
                        print model.name, model.modelname, 'fitdata added as None'
                        model.fitdata = None
                else:
                    model.fitdata = np.array(fitdata)

    def add_d_fitdata(self, *args, **kw):
        ''' adds error to fitdata.
            Cannot give something as both an arg and a kwarg!
        '''
        arg_count = 0
        if 'model' in kw:
            model = getattr(self, kw.get('model'))
        else:
            model = getattr(self, args[arg_count])
            arg_count += 1
        if 'd_fitdata' in kw:
            d_fitdata = kw.get('d_fitdata')
            model.d_fitdata = np.array(d_fitdata)
        else:  # d_fitdata not a kw
            try:  # d_fitdata maybe arg
                d_fitdata = args[arg_count]
            except:  # d_fitdata not given anywhere
                try:  # evaulate equation with parameters
                    model.d_fitdata = np.array(model.error(model.fitdata))
                except:
                    print model.name, model.modelname, 'd_fitdata added as d_data'
                    model.d_fitdata = model.d_data
            else:  # d_fitdata is an arg
                if d_fitdata is None:
                    try:  # evaulate equation with parameters
                        model.d_fitdata = np.array(model.error(model.fitdata))
                    except:  # already list, so add error in data
                        print model.name, model.modelname, 'd_fitdata added as d_data'
                        model.d_fitdata = model.d_data
                else:
                    model.d_fitdata = np.array(d_fitdata)

    def add_xaxis(self, *args, **kw):
        ''' adds an axis to a model.
            called material.add_axis(modelname, equation)  (with either as a kwarg)
            note:  modelname must be a string
            Cannot give something as both an arg and a kwarg!
        '''
        arg_count = 0
        if 'model' in kw:
            model = getattr(self, kw.get('model'))
        else:
            model = getattr(self, args[arg_count])
            arg_count += 1
        if 'xaxis' in kw:
            xaxis = kw.get('xaxis')
        else:
            xaxis = args[arg_count]
            arg_count += 1
        model.xaxis = np.array(xaxis)


class _model(DataClass):
    ''''''
    def __init__(self, name, modelname):  # this solution is temporary
        # super(_model,self).__init__()
        self.name = name                  # this solution is temporary
        self.modelname = modelname
        # data as equation and inputs and error
        self.equation = None
        self.eqinput = None
        self.params = None
        self.error = None
        # original data as a list for easy access
        self.data = None
        self.d_data = None
        # data evaulated with best fit parameters, as a list for easy access
        self.fitdata = None
        self.d_fitdata = None
        # plotting axis
        self.xaxis = None

    def _plot(self, fig=None, ax=111, xaxis=None, **kw):  # come up with better name
        ''' creates a plot of self.
            can create a figure not passing any args
            can add to an existing figure by passing a figure
                can specify which axis with a second arg as the number
            can add to an existing subplots py passing the fig and the axis
        '''
        if 'name' in kw:
            name = kw.get('name')
        else:
            name = self.name  # this solution is temporary
        if fig is None:                     # no figure given
            fig = plt.figure()
            ax = plt.subplot(ax)
        elif isinstance(ax, (int, float)):  # figure given
            ax = fig.add_subplot(ax)
        else:                               # figure and axis give
            pass
        if xaxis is None:
            xaxis = self.xaxis
        name = ax.errorbar(xaxis, self.data, yerr=self.error, ls='-', label=name)
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels, loc='upper right')
        return fig
