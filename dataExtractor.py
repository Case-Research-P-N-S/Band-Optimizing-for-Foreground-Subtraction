from numpy import genfromtxt

outputFile = open("LAMDA Data BB", "w")

data = genfromtxt("Lambda Data")
print data

for i in data:
    outputFile.write(str(i[3]))
    outputFile.write('\n')

outputFile.close()
dataFile.close()
