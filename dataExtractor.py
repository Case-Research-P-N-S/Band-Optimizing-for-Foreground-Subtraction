from numpy import genfromtxt

outputFile = open("LAMA Data BB", "w")

data = genfromtxt("LAMDA Data")
print data

for i in data:
    outputFile.write(str(i[3]))
    outputFile.write('\n')

outputFile.close()
