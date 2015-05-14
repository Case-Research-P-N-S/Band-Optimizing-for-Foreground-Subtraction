# -*- coding: utf-8 -*-
import numpy as np
# Data extractor for BB
def extractData(filename, columnNumber = 3):
    data = np.genfromtxt(filename)
    outputList = []
    
    for i in data:
        outputList.append(i[3])
        
    return outputList
