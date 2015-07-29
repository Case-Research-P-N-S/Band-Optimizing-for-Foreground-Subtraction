import matplotlib.pyplot as plt


class Plotter(object):
    def __init__(self, xval=None, yval=None):
        self.xval = xval
        self.yval = yval
        self.error = None

    def plotthing(self, fig=None, index=1):
        if fig is None:
            fig = plt.figure()
            ax = plt.subplot(111)
        else:
            ax = fig.add_subplot(2,1,index)
        name = 'curve{}'.format(1)
        name = ax.errorbar(self.xval, self.yval, yerr=self.error, ls='-', label=name)
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels, loc='upper right')
        return fig


def compareplots(*args):
    fig = plt.figure()
    for i, val in enumerate(args):
        val.plotthing(fig, i+1)
        plt.title("Measured and Best Fit Function")
    return fig

app1 = Plotter(xval=range(0,10), yval=range(0,10))
plot1 = app1.plotthing()
plot1.savefig('testlong.png')
app2 = Plotter(xval=range(0,11), yval=range(1,12))

thingummy = compareplots(app1, app2)
thingummy.savefig('test.png')
