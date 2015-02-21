from numpy import genfromtxt

outputFile = open("LAMDA Data BB", "w")

data = genfromtxt("LAMDA Data")

for i in data:
    outputFile.write(str(i[3]) + '\n')

outputFile.close()
