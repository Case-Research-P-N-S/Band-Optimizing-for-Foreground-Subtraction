import matplotlib.pyplot as plt


class Plotter(object):
    def __init__(self, xval=None, yval=None):
        self.xval = xval
        self.yval = yval
        self.error = None

    def plotthing(self, fig=None, index=1):
        if fig is None:
            fig, ax = plt.subplots(1, 1)
        else:
            ax = fig.add_subplot(2,1,index)
        name = 'curve{}'.format(1)
        name = ax.errorbar(self.xval, self.yval, yerr=self.error, ls='-', label=name)
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels, loc='upper right')
        return fig

    def loneplot(self):
        figure = plt.figure()
        sp = figure.add_subplot(111)
        sp.plot(self.xval, self.yval, 'o-')
        return figure


def compareplots(*args):
    fig = plt.figure()
    for i, val in enumerate(args):
        val.plotthing(fig, i+1)
        plt.title("Measured and Best Fit Function")
    return fig

app1 = Plotter(xval=range(0,10), yval=range(0,10))
plot1 = app1.loneplot()
plot1.savefig('testlong.png')
app2 = Plotter(xval=range(0,11), yval=range(1,12))

thingummy = compareplots(app1, app2)
thingummy.savefig('test.png')


# def plotCorrelation2(MCData):
#     # figuring out grid spacing
#     numParams = len(MCData.params)
#     numPlots = (numParams-1)*(1 + numParams-1)/2
#     numSpaces, numCols = closest_square(numPlots)
#     if numPlots > numSpaces:
#         numRows = numCols + 1
#     else:
#         numRows = numCols

#     choiceList = [numParams-1-x for x in range(numParams-1)]

#     # making plot
#     fig = plt.figure()
#     gs = GridSpec(numRows, numCols)
#     paramChoice, paramIndex = 0, 1
#     for row in range(numRows):
#         for col in range(numCols):
#             ax = plt.subplot(gs[row, col])
#             if paramIndex > numParams-1:
#                 paramChoice += 1
#                 paramIndex = paramChoice + 1
#             print paramChoice, paramIndex
#             if paramChoice < numParams - 1:
#                 correlplot, = ax.plot(MCData.results[:, paramChoice], MCData.results[:, paramIndex], 'bo', label='b by a List')
#             paramIndex += 1
#     plt.savefig('test.png')
#     plt.close(fig)