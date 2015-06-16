# -*- coding: utf-8 -*-
# All the Classes

import numpy as np


class dataClass(object):
    '''Standard class for all data. Includes name, data, error, fit, and line properties'''
    def __init__(self, name, data, *args, **kwargs):
        self.name = name                             # name of the data

        self.data = np.array(data)                   # the data

        if len(args) > 0:                            # error given as argument
            self.error = args[0]
        elif "error" in kwargs:                      # error given as kwarg
            self.error = kwargs.get("error")
        else:                                        # error manually defined as 0 until later changed
            self.error = 0.0

        if len(args) > 1:                            # fit coefficient given as argument
            self.fitCoeff = args[1]
        elif "fitCoeff" in kwargs:                   # fit coefficient given as kwarg
            self.fitCoeff = kwargs.get("fitCoeff")
        else:                                        # fit manually defined as 1 until later changed
            self.fitCoeff = 1.0

        if len(args) > 2:                            # style given as argument
            self.style = args[2]
        elif "style" in kwargs:                      # style given as kwarg
            self.style = kwargs.get("style")
        else:                                        # style manually defined as scatter until later changed
            self.style = 'scatter'

        if len(args) > 3:                            # line style given as argument
            self.ls = args[3]
        elif "ls" in kwargs:                         # style given as kwarg
            self.ls = kwargs.get("ls")
        else:                                        # color autoset as black
            self.ls = 'b'
