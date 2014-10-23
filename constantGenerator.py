import numpy as np
import scipy as sp

# xi = x's from xlist
# yi = y's from ylist
# Yj(xi) = Yth function for x
# Si = error in measured y

# Creating some test values for the YLists. The YList will be an array of values generated by Y functions from the input xList
'''
Y1 Function
    range Y1
Y2 Function 
    range Y2
Y3 Function 
    range Y3
Y4 Function 
    range Y4
'''
#------------------------------------------
# Creating Test Data
yMeasured = [np.random.normal(0, 0.1) for y in range(10)]

# making a test xList and errorYList
xList = [x for x in range(10)]
errorYList = [np.random.normal(0, 0.1) for y in range(10)]

# creating test Ylists. These arrays will actually be generated from given functions Y1, Y2, Y3, Y4, etc.
Y1List = [1,2,3,4,5,6,7,8,9,10]
#Y2List = [10,9,8,7,6,5,4,3,2,1]
#Y3List = [5,6,7,8,9,10,1,2,3,4]
#Y4List = [4,3,2,1,10,9,8,7,6,6]

if len(Y1List) != len(Y2List):
   print "Error: incompatible lists"
   raise Exception("Incompatible List length")

#------------------------------------------
# Matrix Function


# this just makes it easier to refer to all the YLists
YList = [Y1List] #, Y2List, Y3List, Y4List]

def matrixFunction(functionList, errorYList, xList):
    columns = len(functionList)
    rows = len(xList)
    resultMatrix = np.empty([columns, rows])
    tempList = np.empty([columns, 1])
    for i in range(rows):
        for j in range(columns):
            s = errorYList[j]
            tempList = [x/s for x in functionList[j]]
        np.append(resultMatrix, tempList)
    return resultMatrix

# initialization of Matrix A and variable b
matrixA = matrixFunction(YList, errorYList, xList)
print matrixA

VectorB = np.empty([2, len(yMeasured)])

for y, s in zip(yMeasured, errorYList):
    np.append(VectorB, [y/s])

# ((A transpose) dot (A))
tempA = np.dot(matrixA.transpose(), matrixA)

# inverse of a matrix
tempB = sp.linalg.inv(tempA)

# 
tempC = np.dot(matrixA.transpose(), tempB)

finalConstants = np.dot(tempC, VectorB)
