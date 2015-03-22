import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from dataExtractor import extractData

#------------------------------------------
# Creating Test Data

# making a list with all the angle l values on the x-axis
angles = [l for l in range(2, 1501)]

#errorYList = [np.random.normal(0, 0.1) for y in range(10)]
errorYList = [0.1 for i in angles]

# creating test Ylists. These arrays will actually be generated from given functions Y1, Y2, Y3, Y4, etc.
Y1List = [l**1.9 for l in angles]
Y2List = [5.67**(10**-8)*(l**4) for l in angles]
#Y3List = [5,6,7,8,9,10,1,2,3,4]
#Y4List = [4,3,2,1,10,9,8,7,6,6]

yMeasured = extractData("LAMDA Data")

#------------------------------------------
# Matrix Function


# this just makes it easier to refer to all the YLists
YList = [Y1List, Y2List] #[Y1List, Y2List, Y3List, Y4List]

# Creates the A matrix for use in determining the constants
def matrixFunction(functionList, errorYList):
    columns = len(functionList)
    rows = len(errorYList)
    # initialize the matrix with float values of 0
    resultMatrix = np.matrix([[0.0 for i in functionList] for i in errorYList])
    # initialize the list used as temporary storage for the row values
    tempList = np.empty(columns)
    
    for i in range(rows):
        for j in range(columns):
            s = errorYList[j]
            tempList[j] = functionList[j][i]/s
        resultMatrix[i] = tempList
    return resultMatrix


# initialization of Matrix A
matrixA = matrixFunction(YList, errorYList)

# initialization and assignment of vector b
vectorB = np.empty(len(yMeasured))

for y, s, i in zip(yMeasured, errorYList, range(len(yMeasured))):
    vectorB[i] = y/s

# ((A transpose) dot (A))
tempA = np.dot(matrixA.T, matrixA)

# inverse of a matrix
tempB = tempA.I

# Dot Product of matrix and b vector
tempC = np.dot(matrixA.T, vectorB)

finalTemp = np.dot(tempC, tempB)
vectorA = np.array(finalTemp)[0]
print vectorA
plt.plot([l for l in range(2,1501)],yMeasured)
plt.plot([l for l in range(2,1501)],Y1List)
plt.plot([l for l in range(2,1501)],Y2List)
