# -*- coding: utf-8 -*-
# Plotting Function

import matplotlib.pyplot as plt
from Classes import dataClass     # only for testing
'''
need to make the plotScatter, plot___ be callable functions or classes for stuff like scatterPlot, linePlot,
'''


def plotFunction(xAxis, *args, **kwargs):
    # Makes a scatter plot
    fig = plt.figure()
    ax = plt.subplot(1, 1, 1)
    if "style" in kwargs:
        if kwargs.get("style") == "line":   # does it have to be kwargs.get("style") ==, not just style == 
            style = "no error"
        elif kwargs.get("style") == "scatter":
            style = "no error"
            for i, elem in enumerate(args):
                elem.color += 'o'
        elif kwargs.get("style") == "errorbar":
            style = "error"
        elif kwargs.get("style") == "innate":
            style = "innate"
        else:
            style = "innate"
    for i, elem in enumerate(args):
        name = 'f{}'.format(i+1)
        # if "colors" in kwargs:
            # elem.color[0] = colors[i] # make it so can set colors
        # else:
        if style == "innate":
            style = elem.style
        if style == "no error":
            name, = ax.plot(xAxis, elem.data, elem.color, label=elem.name)
        elif style == "error":
            name, = ax.errorbar(xAxis, elem.data, yerr=elem.error, elem.color, label=elem.name)
        else:
            name, = ax.plot(xAxis, elem.data, elem.color, label=elem.name)
    handles, labels = ax.get_legend_handles_labels()
    plt.legend(handles, labels, loc='upper right')
    if "title" in kwargs:
        plt.title(kwargs.get("title"))
    if "name" in kwargs:
        plt.savefig(kwargs.get("name")+'.png')
    else:
        plt.savefig("untitledplot.png")
    plt.close(fig)


def comparePlot(*args, **kwargs):
    # Makes a scatter plot
    numargs = 2                           # number of arguments here
    fig = plt.figure()
    for i, elem in enumerate(args):
        ax = plt.subplot(numargs, 1, i)
        fig = elem

    plt.close(fig)


xAxis = range(100)
y1 = dataClass('y1', [x for x in range(100)])
y2 = dataClass('y2', [x for x in range(10,110)])

plotFunction(xAxis, y1, y2, name='test name', title='test title', style='scatter')
